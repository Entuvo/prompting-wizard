"""Host readers for history.py. Documented SDK interfaces only; never parse private transcript files.

Claude Code: claude_agent_sdk.list_sessions / get_session_messages (pip install claude-agent-sdk).
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
