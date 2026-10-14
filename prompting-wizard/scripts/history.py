"""Learning from past work history: episodes, filtering and outcome hints.

Pure functions over normalized sessions; host access lives in history_hosts.py.
A session is {'host', 'session_id', 'cwd', 'created_at' (ms), 'messages': [
  {'role': 'user'|'assistant', 'id', 'content': str|list, 'subagent': bool, 'out_tokens': int, 'msg_id'}]}.
See design/history-analysis.md. Raw excerpts written here are local learner data.
"""
import collections
import json
import re
import tempfile

BUILTIN_COMMANDS = {'model', 'clear', 'compact', 'config', 'effort', 'fast', 'login', 'logout', 'mcp', 'resume',
                    'exit', 'permissions', 'cost', 'status', 'help', 'doctor', 'hooks', 'memory', 'init', 'plugin',
                    'plugins', 'agents', 'context', 'usage', 'rename', 'add-dir', 'ide', 'output-style', 'theme',
                    'vim', 'bashes', 'export', 'rewind', 'terminal-setup'}
NOISE_PREFIXES = ('<task-notification', '<local-command-', '<bash-input', '<bash-stdout', '<bash-stderr',
                  '<system-reminder', '[Image: original', '[Usage limit', 'Caveat:',
                  'This session is being continued from a previous')
INTERRUPT = '[Request interrupted by user'
HEALTH_CHECKS = {'respond with hello', 'say hello', 'hello', 'hi', 'ping', 'test'}
ACK = re.compile(r"^\s*(y|yes|yep|ok|okay|done|go|proceed|continue|keep going|approved|lgtm|sure|check|next|"
                 r"go ahead|do it|commit|[a-d1-9])\b[\s.!,]*(as recommended|with recommendations?|ahead)?[\s.!]*$", re.I)
CORRECTION = re.compile(
    r"^\s*(no\b|nope|not\b|wrong|stop\b|wait\b|actually|instead|undo|revert)|"
    r"\b(i meant|that'?s not|not what i|you missed|you forgot|didn'?t work|doesn'?t work|still (not|broken|failing|"
    r"wrong|the same|getting|seeing)|why did you|why are you|i said|i asked|not working|same (issue|error|problem)|"
    r"too (big|long|much|many|verbose)|why can'?t you|confus|keeps? (stopping|failing|breaking|asking)|"
    r"tired of|waste|should have|supposed to|not right|incorrect|makes no sense|fuck|shit)", re.I)
SECRETS = [
    (re.compile(r'\b(sk-[A-Za-z0-9_-]{16,}|gh[pousr]_[A-Za-z0-9]{20,}|xox[abpr]-[A-Za-z0-9-]{10,}|'
                r'AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{30,})'), '[SECRET]'),
    (re.compile(r'(?i)\b(bearer|token|api[_-]?key|password|passwd|secret)(\s*[:=]\s*|\s+)["\']?[^\s"\']{8,}'),
     r'\1=[SECRET]'),
    (re.compile(r'\b[A-Fa-f0-9]{40,}\b'), '[HEX]'),
    (re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+'), '[EMAIL]'),
]
PROMPT_CAP, REPLAY_WINDOW_MS, TEMPLATE_SESSIONS, TEMPLATE_CHARS = 6000, 5 * 60 * 1000, 5, 150
MACHINE_WRAPPER = re.compile(r'^<[a-z][\w-]*(\s[^>]*)?>')  # e.g. <scheduled-task name=...>: generated, not typed
TEMP_ROOTS = ('/tmp/', '/private/tmp/', '/var/folders/', '/private/var/folders/', tempfile.gettempdir().rstrip('/') + '/')


def mask(text):
    for pattern, replacement in SECRETS:
        text = pattern.sub(replacement, text)
    return text


def text_of(content):
    """-> (text, has_image, has_tool_result) for a message's content."""
    if isinstance(content, str):
        return content, False, False
    if not isinstance(content, list):
        return '', False, False
    blocks = [b for b in content if isinstance(b, dict)]
    types = {b.get('type') for b in blocks}
    return '\n'.join(b.get('text', '') for b in blocks if b.get('type') == 'text'), 'image' in types, 'tool_result' in types


def classify(text):
    """-> ('prompt', text, command) | ('interrupt',) | ('noise',)"""
    t = text.strip()
    m = re.search(r'<command-name>/?([^<]+)</command-name>', t)
    if m:  # skill/command invocations; the arguments are the prompt
        args = re.search(r'<command-args>(.*?)</command-args>', t, re.S)
        args = args.group(1).strip() if args else ''
        cmd = m.group(1).strip()
        return ('noise',) if cmd in BUILTIN_COMMANDS or not args else ('prompt', args, cmd)
    if not t or t.startswith(NOISE_PREFIXES + ('<command-message>',)):
        return ('noise',)
    if t.startswith(INTERRUPT):
        return ('interrupt',)
    return ('prompt', t, None)


def kind_of(text):
    return 'ack' if ACK.match(text) or len(text.split()) <= 2 else 'prompt'


def outcome_hint(episode, next_prompt):
    if episode['interrupted']:
        return 'interrupted'
    if next_prompt is None:
        return 'session_end'
    if CORRECTION.search(next_prompt[:400]):
        return 'corrected'
    return 'accepted' if kind_of(next_prompt) == 'ack' else 'followup'


def session_episodes(session):
    episodes, current, seen = [], None, set()
    for msg in session['messages']:
        if msg.get('subagent'):
            continue
        if msg['role'] == 'user':
            text, image, tool_result = text_of(msg['content'])
            if tool_result and not text.strip():
                continue
            c = classify(text)
            if c[0] == 'interrupt':
                if current:
                    current['interrupted'] = True
                continue
            if c[0] == 'noise':
                continue
            current = {'msg_id': msg.get('id'), 'host': session['host'], 'session': session['session_id'],
                       'forked_from': session.get('forked_from'),
                       'created_at': session.get('created_at') or 0, 'workspace': session.get('cwd') or '',
                       'command': c[2], 'prompt': mask(c[1][:PROMPT_CAP]), 'prompt_chars': len(c[1]),
                       'has_image': image, 'replies': [], 'tool_calls': 0, 'out_tokens': 0, 'interrupted': False}
            episodes.append(current)
        elif msg['role'] == 'assistant' and current:
            if msg.get('out_tokens') is None:  # host does not report output tokens
                current['out_tokens'] = None
            elif current['out_tokens'] is not None and (msg.get('msg_id') is None or msg['msg_id'] not in seen):
                seen.add(msg.get('msg_id'))
                current['out_tokens'] += msg['out_tokens']
            content = msg['content'] if isinstance(msg['content'], list) else [{'type': 'text', 'text': msg['content']}]
            for block in content:
                if isinstance(block, dict) and block.get('type') == 'tool_use':
                    current['tool_calls'] += 1
                elif isinstance(block, dict) and block.get('type') == 'text' and block.get('text', '').strip():
                    current['replies'].append(block['text'].strip())
    for i, ep in enumerate(episodes):
        nxt = episodes[i + 1]['prompt'] if i + 1 < len(episodes) else None
        replies = ep.pop('replies')
        ep.update(turn=i, kind=kind_of(ep['prompt']), next_prompt=(nxt or '')[:400],
                  outcome_hint=outcome_hint(ep, nxt), reply_first=mask(replies[0][:400]) if replies else '',
                  reply_last=mask(replies[-1][-600:]) if len(replies) > 1 else '')
    return episodes


def drop_replays(episodes):
    """Resumed or forked sessions replay earlier prompts: same message id, same text in the session it was
    forked from, same text in a session started within five minutes, or an empty copy of text already kept."""
    kept, ids, by_text = [], set(), collections.defaultdict(list)
    for ep in sorted(episodes, key=lambda e: (e['created_at'], e['session'], e['turn'])):
        mid = ep['msg_id']
        if mid and mid in ids:
            continue
        ids.add(mid)
        earlier = by_text[ep['prompt'].strip()]
        empty = not ep['out_tokens'] and not ep['tool_calls'] and not ep['reply_first']
        if ep['source'] == 'human' and earlier and (empty or any(
                e['session'] != ep['session'] and (e['session'] == ep['forked_from'] or
                                                   abs(e['created_at'] - ep['created_at']) < REPLAY_WINDOW_MS)
                for e in earlier)):
            continue
        earlier.append(ep)
        kept.append(ep)
    return kept


def mark_source(episodes):
    """Hand-typed vs automated: long text sent as many distinct messages, temp-dir workspaces, health checks.
    Counts distinct message ids so a replayed prompt (same id) is not mistaken for a template."""
    sessions = collections.defaultdict(set)
    for ep in episodes:
        if ep['prompt_chars'] >= TEMPLATE_CHARS:
            sessions[ep['prompt'][:80]].add(ep['msg_id'] or ep['session'])
    for ep in episodes:
        automated = (ep['prompt_chars'] >= TEMPLATE_CHARS and len(sessions[ep['prompt'][:80]]) >= TEMPLATE_SESSIONS
                     or (ep['workspace'] + '/').startswith(TEMP_ROOTS)
                     or MACHINE_WRAPPER.match(ep['prompt'])
                     or ep['prompt'].strip().lower().rstrip('.!') in HEALTH_CHECKS)
        ep['source'] = 'automated' if automated else 'human'
    return episodes


def build(sessions, cap=300):
    """-> (scoring sample: the `cap` most recent hand-typed prompts, all episodes, counts)."""
    episodes = drop_replays(mark_source([ep for s in sessions for ep in session_episodes(s)]))
    for n, ep in enumerate(episodes):
        ep['id'] = n
        del ep['msg_id'], ep['forked_from']
    human = [e for e in episodes if e['source'] == 'human' and e['kind'] == 'prompt']
    sample = sorted(human, key=lambda e: (e['created_at'], e['turn']))[-cap:] if cap else human
    counts = dict(sessions=len({e['session'] for e in episodes}), episodes=len(episodes), human_prompts=len(human),
                  acks=sum(e['kind'] == 'ack' for e in episodes),
                  automated=sum(e['source'] == 'automated' for e in episodes), sample=len(sample),
                  workspaces=len({e['workspace'] for e in sample}),
                  hints=dict(collections.Counter(e['outcome_hint'] for e in sample)))
    return sample, episodes, counts


def write_jsonl(path, rows):
    with open(path, 'w', encoding='utf-8') as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + '\n')
