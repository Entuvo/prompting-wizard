"""Host readers for history.py. Documented SDK interfaces only; never parse private transcript files.

Claude Code: claude_agent_sdk.list_sessions / get_session_messages (pip install claude-agent-sdk).
Codex: openai_codex Codex.thread_list + the app-server thread/read method (pip install openai-codex).
"""
import time

DAY_MS = 24 * 60 * 60 * 1000


class HostUnavailable(RuntimeError):
    pass


def _field(obj, name, default=None):
    return obj.get(name, default) if isinstance(obj, dict) else getattr(obj, name, default)


def normalize_claude_message(m):
    raw = _field(m, 'message') or {}
    usage = _field(raw, 'usage') or {}
    return {'role': _field(m, 'type'), 'id': _field(m, 'uuid'), 'content': _field(raw, 'content', raw),
            'subagent': _field(m, 'parent_tool_use_id') is not None,
            'out_tokens': _field(usage, 'output_tokens', 0) or 0, 'msg_id': _field(raw, 'id')}


def claude_code_sessions(days=90, now_ms=None, excluded=lambda cwd: False, sdk=None):
    """Yield normalized sessions modified in the last `days`, skipping excluded workspaces."""
    if sdk is None:
        try:
            import claude_agent_sdk as sdk
        except ImportError as exc:
            raise HostUnavailable('Reading Claude Code history needs the Claude Agent SDK: '
                                  'pip install claude-agent-sdk') from exc
    since = (now_ms or int(time.time() * 1000)) - days * DAY_MS
    for info in sdk.list_sessions():
        if (_field(info, 'last_modified') or 0) < since:
            continue
        cwd = _field(info, 'cwd') or ''
        if cwd and excluded(cwd):
            continue
        sid = _field(info, 'session_id')
        yield {'host': 'claude-code', 'session_id': sid, 'cwd': cwd,
               'created_at': _field(info, 'created_at') or _field(info, 'last_modified') or 0,
               'messages': [normalize_claude_message(m) for m in sdk.get_session_messages(sid)]}


CODEX_SOURCES = ['cli', 'vscode', 'appServer']  # interactive threads; exec and sub-agent threads are not hand-typed
CODEX_TOOL_ITEMS = {'commandExecution', 'fileChange', 'mcpToolCall', 'dynamicToolCall', 'webSearch',
                    'functionCallOutput', 'collabAgentToolCall', 'subAgentActivity', 'imageGeneration', 'imageView'}


def _ms(value):
    return (value * 1000 if value and value < 10 ** 12 else value) or 0


def _root(item):
    return getattr(item, 'root', item)


def normalize_codex_turns(turns):
    """Codex turns/items -> history.py messages. Codex reports no per-turn output tokens."""
    messages = []
    for turn in turns or []:
        for item in _field(turn, 'items') or []:
            item = _root(item)
            kind, iid = _field(item, 'type'), _field(item, 'id')
            if kind == 'userMessage':
                parts = [_root(p) for p in _field(item, 'content') or []]
                text = '\n'.join(_field(p, 'text', '') for p in parts if _field(p, 'type') == 'text')
                image = any(_field(p, 'type') not in ('text', None) for p in parts)
                content = [{'type': 'text', 'text': text}] + ([{'type': 'image'}] if image else [])
                messages.append({'role': 'user', 'id': iid, 'content': content, 'subagent': False,
                                 'out_tokens': None, 'msg_id': iid})
            elif kind == 'agentMessage':
                messages.append({'role': 'assistant', 'id': iid, 'subagent': False, 'out_tokens': None,
                                 'msg_id': iid, 'content': [{'type': 'text', 'text': _field(item, 'text', '')}]})
            elif kind in CODEX_TOOL_ITEMS:
                messages.append({'role': 'assistant', 'id': iid, 'subagent': False, 'out_tokens': None,
                                 'msg_id': iid, 'content': [{'type': 'tool_use', 'name': kind}]})
        status = _field(turn, 'status')
        if getattr(status, 'value', status) == 'interrupted':
            messages.append({'role': 'user', 'id': None, 'subagent': False, 'out_tokens': None, 'msg_id': None,
                             'content': '[Request interrupted by user]'})
    return messages


def codex_sessions(days=90, now_ms=None, excluded=lambda cwd: False, client=None):
    """Yield normalized Codex threads updated in the last `days`, skipping excluded workspaces.
    `client` needs thread_list(...) and thread_read(id, include_turns=True), as the SDK's client has."""
    if client is None:
        try:
            import openai_codex
        except ImportError as exc:
            raise HostUnavailable('Reading Codex history needs the Codex SDK: pip install openai-codex') from exc
        with openai_codex.Codex() as codex:
            # thread/read is a documented app-server method; the SDK exposes it on its client.
            yield from codex_sessions(days, now_ms, excluded, _CodexClient(codex))
        return
    since = (now_ms or int(time.time() * 1000)) - days * DAY_MS
    for archived in (False, True):
        cursor = None
        while True:
            page = client.thread_list(archived=archived, cursor=cursor, limit=100, source_kinds=CODEX_SOURCES)
            for thread in _field(page, 'data') or []:
                updated = _ms(_field(thread, 'updated_at') or _field(thread, 'created_at'))
                cwd = str(_field(thread, 'cwd') or '')
                if updated < since or (cwd and excluded(cwd)) or _field(thread, 'ephemeral'):
                    continue
                tid = _field(thread, 'id')
                full = _field(client.thread_read(tid, include_turns=True), 'thread')
                yield {'host': 'codex', 'session_id': tid, 'cwd': cwd,
                       'created_at': _ms(_field(thread, 'created_at')),
                       'forked_from': _field(thread, 'forked_from_id'),
                       'messages': normalize_codex_turns(_field(full, 'turns'))}
            cursor = _field(page, 'next_cursor')
            if not cursor:
                break


class _CodexClient:
    def __init__(self, codex):
        self.codex = codex

    def thread_list(self, **kw):
        return self.codex.thread_list(**kw)

    def thread_read(self, thread_id, include_turns):
        return self.codex._client.thread_read(thread_id, include_turns=include_turns)


# --- learner-supplied data exports (ChatGPT, Claude apps) ----------------------------------------------------
# Exports are files the learner requested from their provider and chose to supply. Formats are not formally
# specified, so readers validate shape and fail closed with a clear message instead of guessing.

EXPORT_MAX_BYTES = 512 * 1024 * 1024


def load_export(path):
    """conversations*.json from a .json file or an export .zip (read in memory; nothing is extracted)."""
    import json
    import zipfile
    from pathlib import Path
    path = Path(path)
    if not path.is_file():
        raise ValueError(f'Export not found: {path}')
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as archive:
            members = sorted(i for i in archive.infolist() if i.filename.rsplit('/', 1)[-1].startswith('conversations')
                             and i.filename.endswith('.json') and not i.is_dir())
            if not members:
                raise ValueError('No conversations.json in this export archive')
            conversations = []
            for info in members:
                if info.file_size > EXPORT_MAX_BYTES:
                    raise ValueError(f'{info.filename} is larger than 512 MiB')
                data = json.loads(archive.read(info).decode('utf-8'))
                conversations += data if isinstance(data, list) else [data]
            return conversations
    if path.stat().st_size > EXPORT_MAX_BYTES:
        raise ValueError('Export file is larger than 512 MiB')
    data = json.loads(path.read_text(encoding='utf-8'))
    return data if isinstance(data, list) else [data]


def _since(days, now_ms):
    return (now_ms or int(time.time() * 1000)) - days * DAY_MS


def _iso_ms(value):
    import datetime
    try:
        return int(datetime.datetime.fromisoformat(str(value).replace('Z', '+00:00')).timestamp() * 1000)
    except ValueError:
        return 0


def _chatgpt_message(node):
    """-> normalized message or None. Hidden context, system and empty nodes are skipped."""
    msg = (node or {}).get('message') or {}
    role = (msg.get('author') or {}).get('role')
    content = msg.get('content') or {}
    ctype = content.get('content_type')
    meta = msg.get('metadata') or {}
    if not msg or meta.get('is_visually_hidden_from_conversation') or ctype in (
            'user_editable_context', 'model_editable_context') or role not in ('user', 'assistant', 'tool'):
        return None
    parts = content.get('parts') or []
    text = '\n'.join(p for p in parts if isinstance(p, str)) or content.get('text') or ''
    image = any(isinstance(p, dict) for p in parts)
    base = {'id': msg.get('id') or node.get('id'), 'subagent': False, 'out_tokens': None, 'msg_id': msg.get('id')}
    if role == 'user':
        return {**base, 'role': 'user', 'content': [{'type': 'text', 'text': text}] + ([{'type': 'image'}] if image else [])}
    if role == 'tool' or ctype in ('code', 'execution_output') or msg.get('recipient', 'all') != 'all':
        return {**base, 'role': 'assistant', 'content': [{'type': 'tool_use', 'name': ctype or 'tool'}]}
    return {**base, 'role': 'assistant', 'content': [{'type': 'text', 'text': text}]} if text.strip() else None


def chatgpt_export_sessions(path, days=90, now_ms=None):
    """ChatGPT export: each conversation is a message tree; read the current branch, and keep each prompt the
    learner edited away (an abandoned sibling) as its own message marked `edited`, followed by its first reply."""
    since, sessions = _since(days, now_ms), []
    for conv in load_export(path):
        mapping, current = conv.get('mapping'), conv.get('current_node')
        if not isinstance(mapping, dict) or current not in mapping:
            raise ValueError('This does not look like a ChatGPT conversations.json export')
        updated = int((conv.get('update_time') or conv.get('create_time') or 0) * 1000)
        if updated < since:
            continue
        chain, node = [], current
        while node in mapping:
            chain.append(node)
            node = mapping[node].get('parent')
        chain.reverse()
        on_chain, messages = set(chain), []
        for nid in chain:
            msg = _chatgpt_message(mapping[nid])
            if msg is None:
                continue
            if msg['role'] == 'user':
                parent = mapping.get(mapping[nid].get('parent')) or {}
                for sib in parent.get('children') or []:
                    old = _chatgpt_message(mapping.get(sib)) if sib not in on_chain else None
                    if old and old['role'] == 'user':
                        messages.append({**old, 'edited': True})
                        reply = next((m for c in mapping[sib].get('children') or []
                                      if (m := _chatgpt_message(mapping.get(c))) and m['role'] == 'assistant'), None)
                        if reply:
                            messages.append(reply)
            messages.append(msg)
        sessions.append({'host': 'chatgpt', 'session_id': conv.get('conversation_id') or conv.get('id') or '',
                         'cwd': '', 'created_at': int((conv.get('create_time') or 0) * 1000), 'messages': messages})
    return sessions


def claude_export_sessions(path, days=90, now_ms=None):
    """Claude app export: each conversation has a list of chat_messages from `human` and `assistant`."""
    since, sessions = _since(days, now_ms), []
    for conv in load_export(path):
        chat = conv.get('chat_messages')
        if not isinstance(chat, list):
            raise ValueError('This does not look like a Claude conversations.json export')
        if _iso_ms(conv.get('updated_at') or conv.get('created_at')) < since:
            continue
        messages = []
        for m in chat:
            role = {'human': 'user', 'assistant': 'assistant'}.get(m.get('sender'))
            if role is None:
                continue
            blocks = [b for b in m.get('content') or [] if isinstance(b, dict)]
            if not any(b.get('type') == 'text' for b in blocks) and m.get('text'):
                blocks.append({'type': 'text', 'text': m['text']})
            if role == 'user':
                blocks = [b for b in blocks if b.get('type') == 'text'] + ([{'type': 'image'}] if m.get('files') else [])
            messages.append({'role': role, 'id': m.get('uuid'), 'content': blocks, 'subagent': False,
                             'out_tokens': None, 'msg_id': m.get('uuid')})
        sessions.append({'host': 'claude', 'session_id': conv.get('uuid') or '', 'cwd': '',
                         'created_at': _iso_ms(conv.get('created_at')), 'messages': messages})
    return sessions
