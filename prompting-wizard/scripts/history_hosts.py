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
