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


if __name__ == '__main__':
    unittest.main()
