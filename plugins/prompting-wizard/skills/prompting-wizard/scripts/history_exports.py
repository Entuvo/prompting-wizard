"""Readers for learner-supplied data exports (ChatGPT, Claude apps). Standard library only.

Exports are files the learner requested from their provider and chose to supply. Formats are not formally
specified, so readers validate shape and fail closed with a clear message instead of guessing.
"""
import time

DAY_MS = 24 * 60 * 60 * 1000

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
