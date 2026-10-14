"""Offline tests for the end-to-end harness: parsers, checks, judge parsing and API runners. No model calls."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import e2e_hosts as e

CARD = {'schema_version': 1, 'profile_id': '33333333-3333-4333-8333-333333333333', 'revision': 0,
        'preferences': {'frequency': 'occasional', 'mode': 'everyday'}, 'events': [], 'retracted_ids': []}


class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.work = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_claude_stream_text_and_bash_commands(self):
        lines = [{'type': 'assistant', 'message': {'content': [
                     {'type': 'tool_use', 'name': 'Bash', 'input': {'command': 'python3 scripts/history.py scan'}},
                     {'type': 'tool_use', 'name': 'Read', 'input': {'file_path': 'x'}}]}},
                 {'type': 'result', 'result': 'Found 2 prompts.'}]
        r = e.parse_claude_stream('\n'.join(map(json.dumps, lines)) + '\nnot json')
        self.assertEqual((r['text'], r['commands']), ('Found 2 prompts.', ['python3 scripts/history.py scan']))

    def test_codex_stream_text_and_commands(self):
        lines = [{'type': 'item.completed', 'item': {'type': 'command_execution', 'command': 'ls'}},
                 {'type': 'item.completed', 'item': {'type': 'agent_message', 'text': 'done'}}]
        r = e.parse_codex_stream('\n'.join(map(json.dumps, lines)))
        self.assertEqual((r['text'], r['commands']), ('done', ['ls']))

    def test_rule_checks(self):
        result = {'text': 'History is available. Learn more.', 'commands': ['python3 history.py scan --root x']}
        checks = {'contains_all': ['history', 'learn'], 'not_matches': ['(?i)has been saved'],
                  'command': r'history\.py.*\bscan\b', 'no_command': r'history\.py\s+merge', 'run_created': True}
        got = {c['check']: c['pass'] for c in e.rule_checks(checks, result, self.work)}
        self.assertEqual(list(got.values()), [True, True, True, True, True, False])  # no run dir exists
        (self.work / 'data' / 'history' / 'r1').mkdir(parents=True)
        (self.work / 'data' / 'history' / 'r1' / 'sample.jsonl').write_text('')
        self.assertTrue(e.rule_checks({'run_created': True}, result, self.work)[0]['pass'])

    def test_card_check_validates_and_requires_fresh_id(self):
        text = 'Here is your card:\n```json\n' + json.dumps(CARD) + '\n```\nSave it yourself.'
        got = e.rule_checks({'card_valid': True}, {'text': text, 'commands': []}, self.work)
        self.assertEqual([c['pass'] for c in got], [True, True])
        stale = json.dumps(CARD | {'profile_id': '11111111-1111-4111-8111-111111111111'})
        got = e.rule_checks({'card_valid': True}, {'text': f'```json\n{stale}\n```', 'commands': []}, self.work)
        self.assertEqual([c['pass'] for c in got], [True, False])
        bad = e.rule_checks({'card_valid': True}, {'text': 'no card', 'commands': []}, self.work)
        self.assertEqual([c['pass'] for c in bad], [False])

    def test_judge_parsing_and_failure(self):
        result = {'text': 'out', 'commands': []}
        ok = e.judge(['a', 'b'], result, ask=lambda p: 'x {"results": [{"pass": true}, {"pass": false, "reason": "no"}]}')
        self.assertEqual([c['pass'] for c in ok], [True, False])
        broken = e.judge(['a'], result, ask=lambda p: 'not json')
        self.assertEqual(broken[0]['detail'], 'judge returned no usable verdict')

    def test_api_runners_skip_without_keys_and_parse_responses(self):
        scenario = {'id': 's', 'plugin': 'everyday', 'prompt': 'hi'}
        env = dict(e.os.environ)
        try:
            e.os.environ.pop('ANTHROPIC_API_KEY', None)
            e.os.environ.pop('OPENAI_API_KEY', None)
            self.assertIn('skipped', e.run_claude_api(scenario, self.work))
            self.assertIn('skipped', e.run_openai_api(scenario, self.work))
            e.os.environ['ANTHROPIC_API_KEY'] = e.os.environ['OPENAI_API_KEY'] = 'test'
            seen = []
            def post(url, headers, body):
                seen.append((url, body))
                if 'anthropic' in url:
                    return {'content': [{'type': 'text', 'text': 'claude says'}]}
                return {'output': [{'content': [{'type': 'output_text', 'text': 'gpt says'}]}]}
            self.assertEqual(e.run_claude_api(scenario, self.work, post)['text'], 'claude says')
            self.assertEqual(e.run_openai_api(scenario, self.work, post)['text'], 'gpt says')
            self.assertIn('Bundled guide', seen[0][1]['system'])
        finally:
            e.os.environ.clear()
            e.os.environ.update(env)

    def test_scenarios_are_well_formed(self):
        scenarios = json.loads((e.FIXTURES / 'scenarios.json').read_text())
        self.assertEqual(len({s['id'] for s in scenarios}), len(scenarios))
        for s in scenarios:
            self.assertTrue(set(s['hosts']) <= set(e.HOSTS), s['id'])
            self.assertIn(s['plugin'], ('course', 'everyday'))
            self.assertTrue(s.get('expect') or s.get('checks'), s['id'])
            if s.get('write'):
                self.assertFalse(set(s['hosts']) & {'claude-api', 'openai-api'})


if __name__ == '__main__':
    unittest.main()
