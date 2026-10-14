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


# --- scoring hand-off and results (see references/history.md) ---------------------------------------------

LEVERS = ('noun', 'verb', 'adjective', 'adverb', 'preposition', 'pronoun', 'conjunction', 'determiner', 'numeral',
          'interjection', 'particle')
GAP_KEYS = set(LEVERS) | {'role-framing', 'few-shot-examples', 'output-schemas', 'task-decomposition',
                          'reasoning-scaffolds', 'negative-constraints', 'context-ordering', 'system-prompts',
                          'agent-and-tool-prompting', 'self-critique-loops', 'writing-evals', 'token-economy',
                          'failure-diagnosis'}
TASK_TYPES = {'build', 'debug', 'research', 'write', 'review', 'plan', 'ops', 'question', 'other'}
ROLES = {'opener', 'steer', 'answer', 'paste', 'meta'}
OUTCOMES = {'clean', 'clarification', 'redirected', 'corrected', 'frustrated', 'interrupted', 'unclear'}
COSTLY = ('frustrated', 'corrected', 'interrupted', 'redirected', 'clarification')
BATCH_SIZE, TOKENS_PER_EPISODE, RETENTION_DAYS = 70, 1400, 30


def _clip(text, n):
    text = (text or '').strip()
    return text if len(text) <= n else text[:n] + f' …[+{len(text) - n} chars]'


def write_batches(sample, episodes, directory):
    """Scoring batches in session order, each episode with the reply that preceded it."""
    previous = {}
    by_session = collections.defaultdict(list)
    for ep in episodes:
        by_session[ep['session']].append(ep)
    for chain in by_session.values():
        chain.sort(key=lambda e: e['turn'])
        for a, b in zip(chain, chain[1:]):
            previous[b['id']] = a['reply_last'] or a['reply_first']
    rows = sorted(sample, key=lambda e: (e['created_at'], e['session'], e['turn']))
    paths = []
    for n, start in enumerate(range(0, len(rows), BATCH_SIZE), 1):
        path = directory / f'{n:02d}.md'
        with open(path, 'w', encoding='utf-8') as fh:
            for ep in rows[start:start + BATCH_SIZE]:
                tok = '?' if ep['out_tokens'] is None else ep['out_tokens']
                fh.write(f"### id={ep['id']} · turn {ep['turn']} · hint={ep['outcome_hint']} · "
                         f"tools={ep['tool_calls']} · out_tok={tok}"
                         f"{' · cmd=/' + ep['command'] if ep['command'] else ''}{' · +image' if ep['has_image'] else ''}\n")
                if ep['id'] in previous:
                    fh.write(f"PREV ASSISTANT: {_clip(previous[ep['id']], 300)}\n")
                fh.write(f"PROMPT:\n{_clip(ep['prompt'], 1500)}\nREPLY (start): {_clip(ep['reply_first'], 300)}\n")
                if ep['reply_last']:
                    fh.write(f"REPLY (end): {_clip(ep['reply_last'], 250)}\n")
                fh.write(f"NEXT USER PROMPT: {_clip(ep['next_prompt'], 300) or '— (session ended)'}\n\n")
        paths.append(path)
    return paths


def validate_score(row):
    errors = []
    if not isinstance(row.get('id'), int):
        errors.append('id')
    if row.get('task_type') not in TASK_TYPES:
        errors.append('task_type')
    if row.get('role') not in ROLES:
        errors.append('role')
    if row.get('outcome') not in OUTCOMES:
        errors.append('outcome')
    gaps = row.get('gaps')
    if not isinstance(gaps, list) or len(gaps) > 3:
        errors.append('gaps')
    else:
        errors += [f"gap {g.get('key')}" for g in gaps
                   if not isinstance(g, dict) or g.get('key') not in GAP_KEYS or g.get('score') not in (1, 2, 3, 4, 5)]
    levers = row.get('levers')
    if row.get('role') == 'opener':
        if not isinstance(levers, dict) or set(levers) != set(LEVERS) or \
                any(v not in (None, 1, 2, 3, 4, 5) for v in levers.values()):
            errors.append('levers')
    elif levers is not None:
        errors.append('levers only for openers')
    if row.get('teach') not in (0, 1, 2, 3):
        errors.append('teach')
    return errors


def merge_scores(run):
    """-> (scored rows, problems). Every sampled id must be scored exactly once."""
    with open(run / 'sample.jsonl', encoding='utf-8') as fh:
        sample = {e['id']: e for e in map(json.loads, fh)}
    scored, problems = {}, []
    for path in sorted((run / 'scores').glob('*.jsonl')):
        with open(path, encoding='utf-8') as fh:
            lines = fh.readlines()
        for ln, line in enumerate(lines, 1):
            try:
                row = json.loads(line)
            except ValueError:
                problems.append(f'{path.name}:{ln} not JSON')
                continue
            errors = validate_score(row) + ([] if row.get('id') in sample else ['unknown id'])
            if row.get('id') in scored:
                errors.append('duplicate id')
            if errors:
                problems.append(f"{path.name}:{ln} {', '.join(errors)}")
            else:
                scored[row['id']] = {**sample[row['id']], **row}
    problems += [f'id {i} not scored' for i in sorted(set(sample) - set(scored))]
    return [scored[i] for i in sorted(scored)], problems


def baseline(rows):
    """Aggregates only: no prompt text. Safe to show in chat."""
    def rate(xs):
        return round(sum(r['outcome'] in COSTLY for r in xs) / len(xs), 2) if xs else None
    openers = [r for r in rows if r['role'] == 'opener']
    levers = {}
    for k in LEVERS:
        values = [r['levers'][k] for r in openers if r['levers'].get(k)]
        levers[k] = {'mean': round(sum(values) / len(values), 2), 'n': len(values)} if values else {'mean': None, 'n': 0}
    costly = [r for r in rows if r['outcome'] in COSTLY]
    count = collections.Counter
    return {
        'prompts': len(rows), 'costly_rate': rate(rows), 'frustrated': sum(r['outcome'] == 'frustrated' for r in rows),
        'by_role': {k: {'n': len(x), 'costly_rate': rate(x)} for k in sorted(ROLES)
                    if (x := [r for r in rows if r['role'] == k])},
        'by_task': {k: {'n': len(x), 'costly_rate': rate(x)} for k in sorted(TASK_TYPES)
                    if (x := [r for r in rows if r['task_type'] == k])},
        'levers': levers,
        'costly_gaps': dict(count(g['key'] for r in costly for g in r['gaps']).most_common()),
        'frustration_gaps': dict(count(g['key'] for r in rows if r['outcome'] == 'frustrated'
                                       for g in r['gaps']).most_common()),
        'teaching_cases': sum(r['teach'] == 3 for r in rows), 'exemplars': sum(bool(r.get('exemplar')) for r in rows),
    }


def purge(history_root, now=None):
    """Raw history runs follow the 30-day raw-evidence rule."""
    import shutil
    import time
    cutoff = (now or time.time()) - RETENTION_DAYS * 86400
    removed = []
    for run in history_root.glob('*/'):
        if run.stat().st_mtime < cutoff:
            shutil.rmtree(run)
            removed.append(run.name)
    return removed


def _excluder(root):
    """Honor coaching exclusions when a learner profile exists in ROOT."""
    if not (root / 'learner.sqlite3').exists():
        return lambda cwd: False
    from store import Store
    store, cache = Store(root), {}
    def excluded(cwd):
        if cwd not in cache:
            cache[cwd] = bool(store.status(workspace=cwd).get('excluded'))
        return cache[cwd]
    return excluded


def main(argv=None):
    import argparse
    import datetime
    import os
    import sys
    from pathlib import Path
    import history_hosts

    parser = argparse.ArgumentParser(description='Learn from past work history. See references/history.md.')
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('scan', 'merge', 'delete'):
        cmd = sub.add_parser(name)
        cmd.add_argument('--root', required=True, type=Path)
        if name == 'scan':
            cmd.add_argument('--host', required=True, choices=['claude-code', 'codex'])
            cmd.add_argument('--days', type=int, default=90)
            cmd.add_argument('--cap', type=int, default=300)
        if name == 'merge':
            cmd.add_argument('--run', required=True)
        if name == 'delete':
            group = cmd.add_mutually_exclusive_group(required=True)
            group.add_argument('--run')
            group.add_argument('--all', action='store_true')
    args = parser.parse_args(argv)
    root = args.root
    if not root.is_absolute() or root.is_symlink():
        parser.error('--root must be an absolute, non-symlink directory')
    os.umask(0o077)
    history_root = root / 'history'
    history_root.mkdir(mode=0o700, parents=True, exist_ok=True)
    out = {'purged': purge(history_root)}
    try:
        if args.command == 'scan':
            reader = history_hosts.claude_code_sessions if args.host == 'claude-code' else history_hosts.codex_sessions
            sessions = list(reader(days=args.days, excluded=_excluder(root)))
            sample, episodes, counts = build(sessions, cap=args.cap)
            run = history_root / f"{datetime.datetime.now(datetime.timezone.utc):%Y%m%dT%H%M%SZ}-{args.host}"
            (run / 'batches').mkdir(parents=True)
            (run / 'scores').mkdir()
            write_jsonl(run / 'episodes.jsonl', episodes)
            write_jsonl(run / 'sample.jsonl', sample)
            batches = write_batches(sample, episodes, run / 'batches')
            out.update(run=run.name, host=args.host, days=args.days, counts=counts, batches=len(batches),
                       estimated_scoring_tokens=len(sample) * TOKENS_PER_EPISODE,
                       coverage_note=('Claude Code returns each session\'s current conversation; earlier branches of '
                                      'compacted or rewound sessions are not available.' if args.host == 'claude-code'
                                      else 'Codex does not report per-turn output tokens.'))
        elif args.command == 'merge':
            run = history_root / args.run
            rows, problems = merge_scores(run)
            if problems:
                out.update(ok=False, problems=problems[:50], problem_count=len(problems))
            else:
                write_jsonl(run / 'scored.jsonl', rows)
                summary = baseline(rows)
                (run / 'baseline.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
                out.update(ok=True, run=run.name, baseline=summary)
        else:
            import shutil
            targets = [history_root / args.run] if args.run else [p for p in history_root.glob('*/')]
            for target in targets:
                if target.parent != history_root or not target.is_dir():
                    raise ValueError(f'No such history run: {target.name}')
                shutil.rmtree(target)
            out.update(deleted=[t.name for t in targets])
    except (history_hosts.HostUnavailable, ValueError, OSError) as exc:
        print(json.dumps({**out, 'ok': False, 'error': str(exc)}))
        return 1
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
