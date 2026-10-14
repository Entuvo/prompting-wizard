import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'prompting-wizard' / 'scripts'))
import history
import history_hosts

NOW = 1_760_000_000_000
MIN = 60 * 1000


def user(uid, content, **kw):
    return {'type': 'user', 'uuid': uid, 'message': {'role': 'user', 'content': content}, **kw}


def assistant(uid, text, tools=0, out=10, mid=None):
    blocks = [{'type': 'tool_use', 'name': 'Bash', 'input': {}}] * tools + [{'type': 'text', 'text': text}]
    return {'type': 'assistant', 'uuid': uid, 'parent_tool_use_id': None,
            'message': {'id': mid or 'm-' + uid, 'role': 'assistant', 'content': blocks,
                        'usage': {'output_tokens': out}}}


class FakeSDK:
    """Stands in for claude_agent_sdk: list_sessions() / get_session_messages(session_id)."""
    def __init__(self, sessions):
        self.sessions = sessions

    def list_sessions(self):
        return [s['info'] for s in self.sessions]

    def get_session_messages(self, session_id):
        return next(s['messages'] for s in self.sessions if s['info']['session_id'] == session_id)


def session(sid, cwd, created, messages, modified=None):
    return {'info': {'session_id': sid, 'cwd': cwd, 'created_at': created, 'last_modified': modified or created},
            'messages': messages}


WORK = [
    user('u1', 'Summarise the incident log for the on-call channel'),
    assistant('a1', 'Here is a summary of every incident.', tools=2, out=300),
    user('t1', [{'type': 'tool_result', 'content': 'ok'}]),
    user('u2', 'no, I meant only the outage on Tuesday, in three bullets'),
    assistant('a2', 'Tuesday outage: ...', out=80),
    user('n1', '<task-notification>background job done</task-notification>'),
    user('c1', '<command-name>/model</command-name><command-args>opus</command-args>'),
    user('c2', '<command-message>review</command-message>\n<command-name>/review</command-name>\n'
               '<command-args>the payments diff</command-args>'),
    assistant('a3', 'Reviewing.', tools=1),
    {**assistant('s1', 'subagent chatter', tools=5), 'parent_tool_use_id': 'toolu_1'},
    user('i1', [{'type': 'text', 'text': '[Request interrupted by user for tool use]'}]),
    user('u3', 'yes'),
    user('u4', 'deploy with token=abcd1234efgh5678 and mail ops@example.com'),
]


def fixture():
    template = 'Read BRIEF.md in the current directory and complete the task it describes. ' * 3
    sessions = [session('work', '/srv/ana/app', NOW - 10 * MIN, WORK)]
    # A resumed session replays u1 with the same uuid, and a fork re-sends u2 under a new id a minute later.
    sessions.append(session('resumed', '/srv/ana/app', NOW - 9 * MIN, [WORK[0], WORK[1]]))
    sessions.append(session('fork', '/srv/ana/app', NOW - 9 * MIN, [user('u2b', WORK[3]['message']['content']),
                                                                       assistant('a2b', 'Tuesday outage', out=5)]))
    for i in range(5):  # harness prompt repeated across sessions
        sessions.append(session(f'run{i}', f'/srv/ana/runs/{i}', NOW - (300 + i) * MIN,
                                [user(f'h{i}', template), assistant(f'ha{i}', 'done')]))
    sessions.append(session('probe', '/private/var/folders/xy/T/probe-1', NOW - 2 * MIN,
                            [user('p1', 'List exactly five risks.'), assistant('pa', 'risks')]))
    sessions.append(session('ping', '/srv/ana/app', NOW - 3 * MIN, [user('g1', 'Respond with hello.'),
                                                                      assistant('ga', 'hello')]))
    sessions.append(session('old', '/srv/ana/app', NOW - 200 * 24 * 60 * MIN, [user('o1', 'ancient prompt')]))
    sessions.append(session('secret', '/srv/ana/private', NOW - 1 * MIN, [user('x1', 'excluded work')]))
    return FakeSDK(sessions)


def read(**kw):
    excluded = lambda cwd: cwd.startswith('/srv/ana/private')
    return list(history_hosts.claude_code_sessions(days=90, now_ms=NOW, excluded=excluded, sdk=fixture(), **kw))


HOST_VARS = ('CODEX_THREAD_ID', 'CODEX_SESSION_ID', 'CLAUDE_CODE_SESSION_ID', 'CLAUDECODE')


def setUpModule():
    """Tests must not depend on which coding host runs them (history.provider_guard reads these)."""
    import os
    global SAVED_HOST_VARS
    SAVED_HOST_VARS = {k: os.environ.pop(k) for k in HOST_VARS if k in os.environ}


def tearDownModule():
    import os
    os.environ.update(SAVED_HOST_VARS)


class HistoryTests(unittest.TestCase):
    def setUp(self):
        self.sample, self.episodes, self.counts = history.build(read())
        self.by_prompt = {e['prompt']: e for e in self.episodes}

    def test_window_and_exclusions_skip_sessions_before_reading(self):
        ids = {s['session_id'] for s in read()}
        self.assertNotIn('old', ids)
        self.assertNotIn('secret', ids)

    def test_only_human_prompts_become_episodes(self):
        prompts = [e['prompt'] for e in self.episodes]
        self.assertNotIn('subagent chatter', ' '.join(e['reply_first'] for e in self.episodes))
        self.assertFalse(any(p.startswith(('<task-notification', '<command-name>')) for p in prompts))
        self.assertIn('the payments diff', prompts)  # skill command with arguments is a prompt
        self.assertEqual(self.by_prompt['the payments diff']['command'], 'review')
        self.assertNotIn('opus', prompts)  # built-in command is not

    def test_correction_and_interrupt_hints(self):
        first = self.by_prompt['Summarise the incident log for the on-call channel']
        self.assertEqual(first['outcome_hint'], 'corrected')
        self.assertEqual(first['tool_calls'], 2)
        self.assertEqual(first['out_tokens'], 300)
        self.assertEqual(self.by_prompt['the payments diff']['outcome_hint'], 'interrupted')
        self.assertEqual(self.by_prompt['yes']['kind'], 'ack')

    def test_replays_are_dropped(self):
        texts = [e['prompt'] for e in self.episodes]
        self.assertEqual(texts.count('Summarise the incident log for the on-call channel'), 1)
        self.assertEqual(texts.count('no, I meant only the outage on Tuesday, in three bullets'), 1)

    def test_automated_prompts_are_marked_not_sampled(self):
        automated = [e for e in self.episodes if e['source'] == 'automated']
        self.assertEqual(len(automated), 7)  # 5 harness runs, 1 temp-dir probe, 1 health check
        self.assertFalse(any(e['source'] == 'automated' for e in self.sample))

    def test_secrets_are_masked(self):
        text = ' '.join(e['prompt'] for e in self.episodes)
        self.assertNotIn('abcd1234efgh5678', text)
        self.assertNotIn('ops@example.com', text)

    def test_sample_cap_keeps_most_recent(self):
        sample, _, counts = history.build(read(), cap=1)
        self.assertEqual(len(sample), 1)
        self.assertEqual(counts['sample'], 1)
        self.assertEqual(sample[0]['session'], 'work')

    def test_missing_sdk_says_how_to_install(self):
        import builtins
        real = builtins.__import__
        def no_sdk(name, *a, **kw):
            if name == 'claude_agent_sdk':
                raise ImportError(name)
            return real(name, *a, **kw)
        builtins.__import__ = no_sdk
        try:
            with self.assertRaisesRegex(history_hosts.HostUnavailable, 'pip install claude-agent-sdk'):
                next(history_hosts.claude_code_sessions())
        finally:
            builtins.__import__ = real



SEC = NOW // 1000


def item(kind, iid, **kw):
    return {'type': kind, 'id': iid, **kw}


def ask(iid, text, image=False):
    content = [{'type': 'text', 'text': text}] + ([{'type': 'localImage', 'path': 'x.png'}] if image else [])
    return item('userMessage', iid, content=content)


class FakeCodex:
    """Stands in for the Codex SDK client: thread_list(...) pages and thread_read(id, include_turns)."""
    def __init__(self, threads):
        self.threads, self.calls = threads, []

    def thread_list(self, archived, cursor, limit, source_kinds):
        self.calls.append(source_kinds)
        rows = [t['meta'] for t in self.threads if t['meta'].get('archived', False) == archived]
        start = int(cursor or 0)
        nxt = str(start + 2) if start + 2 < len(rows) else None
        return {'data': rows[start:start + 2], 'next_cursor': nxt}

    def thread_read(self, thread_id, include_turns):
        assert include_turns
        t = next(t for t in self.threads if t['meta']['id'] == thread_id)
        return {'thread': {'turns': t['turns']}}


def thread(tid, cwd, created_s, turns, **meta):
    return {'meta': {'id': tid, 'cwd': cwd, 'created_at': created_s, 'updated_at': created_s, **meta},
            'turns': turns}


def codex_fixture():
    main = [{'id': 't1', 'items': [ask('i1', 'Draft the release notes for v2 from the changelog'),
                                   item('commandExecution', 'c1', command='cat CHANGELOG.md'),
                                   item('agentMessage', 'r1', text='Release notes: ...')]},
            {'id': 't2', 'items': [ask('i2', "that's not what I asked, only user-facing changes", image=True),
                                   item('commandExecution', 'c2', command='git log')], 'status': 'interrupted'},
            {'id': 't3', 'items': [ask('i7', '<scheduled-task name="nightly">run the report</scheduled-task>'),
                                   item('agentMessage', 'r7', text='ok')]}]
    return FakeCodex([
        thread('main', '/srv/ana/app', SEC - 600, main),
        thread('fork', '/srv/ana/app', SEC - 60, main, forked_from_id='main'),
        thread('archived', '/srv/ana/app', SEC - 3600, [{'id': 't', 'items': [
            ask('i3', 'Rename the config flag everywhere'), item('agentMessage', 'r3', text='Done.')]}], archived=True),
        thread('scratch', '/srv/ana/app', SEC - 30, [{'id': 't', 'items': [ask('i4', 'tmp')]}], ephemeral=True),
        thread('old', '/srv/ana/app', SEC - 200 * 86400, [{'id': 't', 'items': [ask('i5', 'ancient')]}]),
        thread('secret', '/srv/ana/private', SEC - 10, [{'id': 't', 'items': [ask('i6', 'excluded')]}]),
    ])


class CodexTests(unittest.TestCase):
    def setUp(self):
        self.fake = codex_fixture()
        excluded = lambda cwd: cwd.startswith('/srv/ana/private')
        self.sessions = list(history_hosts.codex_sessions(days=90, now_ms=NOW, excluded=excluded, client=self.fake))
        self.sample, self.episodes, _ = history.build(self.sessions)

    def test_reads_interactive_threads_in_window_across_pages_and_archive(self):
        self.assertEqual({s['session_id'] for s in self.sessions}, {'main', 'fork', 'archived'})
        self.assertTrue(all(kinds == history_hosts.CODEX_SOURCES for kinds in self.fake.calls))
        self.assertEqual(self.sessions[0]['created_at'], (SEC - 600) * 1000)

    def test_episodes_tools_and_correction(self):
        first = next(e for e in self.episodes if e['prompt'].startswith('Draft the release notes'))
        self.assertEqual((first['tool_calls'], first['out_tokens'], first['outcome_hint']), (1, None, 'corrected'))
        second = next(e for e in self.episodes if e['prompt'].startswith("that's not"))
        self.assertTrue(second['has_image'])
        self.assertEqual(second['outcome_hint'], 'interrupted')

    def test_machine_wrapped_prompts_are_automated(self):
        task = next(e for e in self.episodes if e['prompt'].startswith('<scheduled-task'))
        self.assertEqual(task['source'], 'automated')

    def test_fork_does_not_duplicate_prompts(self):
        self.assertEqual(sum(e['prompt'].startswith('Draft the release notes') for e in self.episodes), 1)



def score_row(i, role='opener', outcome='corrected', gap='preposition'):
    row = {'id': i, 'task_type': 'plan', 'role': role, 'outcome': outcome,
           'gaps': [{'key': gap, 'score': 2, 'evidence': 'scope came next turn'}] if outcome != 'clean' else [],
           'missing_info': None, 'teach': 3 if outcome != 'clean' else 0, 'exemplar': outcome == 'clean', 'note': ''}
    if role == 'opener':
        row['levers'] = dict.fromkeys(history.LEVERS, None) | {'noun': 2, 'adjective': 1}
    return row


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        import json, os, tempfile
        self.json, self.os = json, os
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / 'data'
        self.run = self.root / 'history' / 'r1'
        (self.run / 'scores').mkdir(parents=True)
        history.write_jsonl(self.run / 'sample.jsonl', [{'id': 0, 'prompt': 'a'}, {'id': 1, 'prompt': 'b'}])

    def tearDown(self):
        self.tmp.cleanup()

    def cli(self, *args):
        import contextlib, io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = history.main([args[0], '--root', str(self.root), *args[1:]])
        return code, self.json.loads(buf.getvalue())

    def test_merge_reports_baseline_without_prompt_text(self):
        history.write_jsonl(self.run / 'scores' / '01.jsonl', [score_row(0), score_row(1, 'steer', 'clean')])
        code, out = self.cli('merge', '--run', 'r1')
        self.assertEqual((code, out['ok']), (0, True))
        b = out['baseline']
        self.assertEqual((b['prompts'], b['costly_rate'], b['by_role']['opener']['costly_rate']), (2, 0.5, 1.0))
        self.assertEqual(b['levers']['adjective'], {'mean': 1.0, 'n': 1})
        self.assertEqual(b['costly_gaps'], {'preposition': 1})
        self.assertNotIn('"prompt"', (self.run / 'baseline.json').read_text())

    def test_merge_rejects_missing_duplicate_and_invalid_rows(self):
        bad = score_row(1, 'steer') | {'levers': {'noun': 9}}
        history.write_jsonl(self.run / 'scores' / '01.jsonl', [score_row(0), score_row(0), bad, {'id': 7}])
        code, out = self.cli('merge', '--run', 'r1')
        self.assertEqual((code, out['ok']), (0, False))
        text = ' '.join(out['problems'])
        for expected in ('duplicate id', 'levers only for openers', 'unknown id', 'id 1 not scored'):
            self.assertIn(expected, text)
        self.assertFalse((self.run / 'scored.jsonl').exists())

    def test_cases_pick_costliest_gaps_with_lessons_and_followups(self):
        episodes = [{'id': i, 'session': 's', 'turn': i, 'kind': 'prompt', 'prompt': f'p{i}', 'reply_first': f'r{i}',
                     'reply_last': '', 'out_tokens': 10 * i, 'tool_calls': i} for i in range(6)]
        history.write_jsonl(self.run / 'episodes.jsonl', episodes)
        rows = [episodes[i] | score_row(i, gap='preposition') for i in range(4)]
        rows += [episodes[4] | score_row(4, gap='noun'), episodes[5] | score_row(5, 'steer', 'clean')]
        history.write_jsonl(self.run / 'scored.jsonl', rows)
        code, out = self.cli('cases', '--run', 'r1')
        self.assertEqual(code, 0)
        self.assertEqual([t['key'] for t in out['themes']], ['preposition'])  # noun has < 3 costly prompts
        self.assertEqual(out['themes'][0]['lesson'], 'days/05.md')
        text = (self.run / 'cases' / 'preposition.md').read_text()
        self.assertIn('USER +1: p1', text)
        self.assertTrue((self.run / 'cases' / 'exemplars.md').exists())

    def test_cases_need_merged_scores(self):
        code, out = self.cli('cases', '--run', 'r1')
        self.assertEqual((code, out['ok']), (1, False))

    def test_cli_runs_in_python_isolated_mode(self):
        import os, subprocess
        export = Path(self.tmp.name) / 'c.json'
        export.write_text('[]')
        script = Path(history.__file__)
        env = {k: v for k, v in os.environ.items() if not k.startswith(('CODEX_', 'CLAUDE_CODE')) and k != 'CLAUDECODE'}
        proc = subprocess.run([sys.executable, '-I', str(script), 'scan', '--root', str(self.root), '--host', 'claude',
                               '--file', str(export)], capture_output=True, text=True, env=env)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(self.json.loads(proc.stdout)['counts']['episodes'], 0)

    def test_provider_guard(self):
        codex, claude = {'CODEX_THREAD_ID': 't'}, {'CLAUDE_CODE_SESSION_ID': 's'}
        self.assertIsNone(history.provider_guard('chatgpt', codex))
        self.assertIsNone(history.provider_guard('codex', codex))
        self.assertIn('Codex reviews only ChatGPT', history.provider_guard('claude', codex))
        self.assertIn('Claude Code', history.provider_guard('claude-code', codex))
        self.assertIsNone(history.provider_guard('claude', claude))
        self.assertIn('Claude Code reviews only Claude', history.provider_guard('chatgpt', claude))
        self.assertIsNone(history.provider_guard('chatgpt', {}))  # unknown host: the procedure decides
        self.assertEqual(history.current_provider(codex | claude), 'ambiguous')  # one host launched from the other
        for source in ('claude', 'chatgpt', 'codex', 'claude-code'):
            self.assertIn('Cannot tell', history.provider_guard(source, codex | claude))

    def test_scan_refuses_other_providers_export(self):
        import os
        export = Path(self.tmp.name) / 'c.json'
        export.write_text('[]')
        old = dict(os.environ)
        try:
            os.environ.pop('CLAUDE_CODE_SESSION_ID', None); os.environ.pop('CLAUDECODE', None)
            os.environ['CODEX_THREAD_ID'] = 't'
            code, out = self.cli('scan', '--host', 'claude', '--file', str(export))
            self.assertEqual((code, out['ok']), (1, False))
            self.assertIn('Codex reviews only ChatGPT', out['error'])
            self.assertFalse(any((self.root / 'history').glob('*-claude')))
        finally:
            os.environ.clear(); os.environ.update(old)

    def test_unknown_gap_key_is_rejected(self):
        self.assertIn('gap agent_tool', history.validate_score(score_row(0, gap='agent_tool')))

    def test_delete_and_retention(self):
        old = self.root / 'history' / 'r0'
        old.mkdir()
        self.os.utime(old, (0, 0))
        code, out = self.cli('delete', '--run', 'r1')
        self.assertEqual(out['purged'], ['r0'])
        self.assertEqual(out['deleted'], ['r1'])
        self.assertEqual(list((self.root / 'history').iterdir()), [])
        code, out = self.cli('delete', '--run', '../../etc')
        self.assertEqual(code, 1)



def gpt_node(nid, parent, children, role=None, text='', ctype='text', hidden=False, parts=None, recipient='all'):
    message = None if role is None else {
        'id': nid, 'author': {'role': role}, 'recipient': recipient,
        'content': {'content_type': ctype, 'parts': parts if parts is not None else [text]},
        'metadata': {'is_visually_hidden_from_conversation': hidden}}
    return {'id': nid, 'parent': parent, 'children': children, 'message': message}


def chatgpt_export():
    m = {
        'root': gpt_node('root', None, ['sys']),
        'sys': gpt_node('sys', 'root', ['u1'], 'system', 'You are ChatGPT', hidden=True),
        'u1': gpt_node('u1', 'sys', ['a1'], 'user', 'Write a launch email for the beta'),
        'a1': gpt_node('a1', 'u1', ['u2old', 'u2'], 'assistant', 'Subject: Big news! ...'),
        'u2old': gpt_node('u2old', 'a1', ['a2old'], 'user', 'make it better'),
        'a2old': gpt_node('a2old', 'u2old', [], 'assistant', 'Subject: Even bigger news!'),
        'u2': gpt_node('u2', 'a1', ['t1'], 'user', 'shorter, for existing customers only, no hype',
                       parts=['shorter, for existing customers only, no hype', {'asset_pointer': 'file-1'}]),
        't1': gpt_node('t1', 'u2', ['a3'], 'assistant', 'print(1)', ctype='code', recipient='python'),
        'a3': gpt_node('a3', 't1', [], 'assistant', 'Hi — the beta opens Monday.'),
    }
    return [{'conversation_id': 'c1', 'title': 'Launch email', 'create_time': (NOW - 5 * MIN) / 1000,
             'update_time': (NOW - 4 * MIN) / 1000, 'mapping': m, 'current_node': 'a3'},
            {'conversation_id': 'old', 'create_time': 1, 'update_time': 1,
             'mapping': {'r': gpt_node('r', None, [])}, 'current_node': 'r'}]


def claude_export():
    return [{'uuid': 'k1', 'name': 'Board memo', 'created_at': '2025-10-09T08:00:00Z', 'updated_at': '2025-10-09T08:10:00Z',
             'chat_messages': [
                 {'uuid': 'h1', 'sender': 'human', 'text': 'Summarise the board deck', 'files': [{'file_name': 'deck.png'}],
                  'content': [{'type': 'text', 'text': 'Summarise the board deck'}]},
                 {'uuid': 'b1', 'sender': 'assistant', 'text': 'Here are 12 points...',
                  'content': [{'type': 'tool_use', 'name': 'web_search'}, {'type': 'text', 'text': 'Here are 12 points...'}]},
                 {'uuid': 'h2', 'sender': 'human', 'text': 'too long, 3 bullets for the CFO', 'content': []},
             ]}]


class ExportTests(unittest.TestCase):
    def setUp(self):
        import json, tempfile, zipfile
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.gpt = self.dir / 'chatgpt.zip'
        with zipfile.ZipFile(self.gpt, 'w') as z:
            z.writestr('chat.html', '<html></html>')
            z.writestr('conversations.json', json.dumps(chatgpt_export()))
        self.claude = self.dir / 'conversations.json'
        self.claude.write_text(json.dumps(claude_export()))
        self.json = json

    def tearDown(self):
        self.tmp.cleanup()

    def test_chatgpt_branch_edits_tools_and_window(self):
        sessions = history_hosts.chatgpt_export_sessions(self.gpt, days=90, now_ms=NOW)
        self.assertEqual([s['session_id'] for s in sessions], ['c1'])
        _, eps, _ = history.build(sessions)
        prompts = [e['prompt'] for e in eps]
        self.assertEqual(prompts, ['Write a launch email for the beta', 'make it better',
                                   'shorter, for existing customers only, no hype'])
        edited = eps[1]
        self.assertEqual((edited['outcome_hint'], edited['next_prompt'][:7], edited['reply_first'][:8]),
                         ('edited', 'shorter', 'Subject:'))
        self.assertEqual((eps[2]['tool_calls'], eps[2]['has_image']), (1, True))
        self.assertNotIn('You are ChatGPT', ' '.join(prompts))

    def test_claude_export(self):
        sessions = history_hosts.claude_export_sessions(self.claude, days=90, now_ms=NOW)
        _, eps, _ = history.build(sessions)
        first = eps[0]
        self.assertEqual((first['host'], first['tool_calls'], first['has_image']), ('claude', 1, True))
        self.assertEqual(first['outcome_hint'], 'corrected')  # "too long, ..."
        self.assertEqual(eps[1]['prompt'], 'too long, 3 bullets for the CFO')

    def test_wrong_format_fails_closed(self):
        with self.assertRaisesRegex(ValueError, 'ChatGPT'):
            history_hosts.chatgpt_export_sessions(self.claude)
        with self.assertRaisesRegex(ValueError, 'Claude'):
            history_hosts.claude_export_sessions(self.gpt)
        empty = self.dir / 'empty.zip'
        import zipfile
        with zipfile.ZipFile(empty, 'w') as z:
            z.writestr('notes.txt', 'x')
        with self.assertRaisesRegex(ValueError, 'No conversations.json'):
            history_hosts.load_export(empty)

    def test_cli_scan_from_export(self):
        import contextlib, io
        root = self.dir / 'data'
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = history.main(['scan', '--root', str(root), '--host', 'claude', '--file', str(self.claude),
                                 '--days', '36500'])
        out = self.json.loads(buf.getvalue())
        self.assertEqual((code, out['counts']['human_prompts'], out['batches']), (0, 2, 1))
        self.assertEqual(out['ask'], 'Score these 2 prompts now? (yes/no)')
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = history.main(['scan', '--root', str(root), '--host', 'chatgpt'])
        self.assertEqual((code, self.json.loads(buf.getvalue())['ok']), (1, False))


if __name__ == '__main__':
    unittest.main()
