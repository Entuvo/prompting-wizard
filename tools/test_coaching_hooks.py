"""CLI safety contracts; automatic host adapters remain behind live verification."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT=Path(__file__).resolve().parents[1]/'prompting-wizard/scripts/wizard.py'

class CLITests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)/'profile'

    def run_cli(self,*args,input=None,env=None):
        return subprocess.run([sys.executable,str(SCRIPT),*args,'--root',str(self.root)],input=input,text=True,capture_output=True,env=env)

    def result(self,*args,input=None):
        r=self.run_cli(*args,input=input)
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertTrue(r.stdout.strip(),'CLI returned no result')
        return json.loads(r.stdout)

    def test_configuration_pause_and_status(self):
        self.result('configure','--mode','lesson-only','--workspace',str(Path(self.temp.name)/'work'))
        self.result('pause');self.assertTrue(self.result('status')['paused'])
        self.result('resume');self.assertFalse(self.result('status')['paused'])
        self.assertEqual(self.result('list','--kind','all')['records'],[])

    def test_status_exposes_effective_workspace_mode_and_progress_presence(self):
        work = str(Path(self.temp.name) / 'work')
        self.result('configure', '--mode', 'after-result')
        status = self.result('status', '--workspace', work)
        self.assertIsNone(status['effective_mode'])
        self.assertFalse(status['has_progress'])
        self.result('include', '--workspace', work)
        self.assertEqual(self.result('status', '--workspace', work)['effective_mode'], 'after-result')
        self.result('configure', '--workspace', work, '--mode', 'lesson-only')
        self.assertEqual(self.result('status', '--workspace', work)['workspace_mode'], 'lesson-only')
        self.result('pause')
        self.assertIsNone(self.result('status', '--workspace', work)['effective_mode'])

    def test_guidance_uses_host_session_identity_without_an_observation(self):
        sys.path.insert(0, str(SCRIPT.parent))
        from store import Store
        store = Store(self.root)
        work = str(Path(self.temp.name) / 'work')
        event = dict(hook_event_name='SessionStart', session_id='guidance', cwd=work, model='gpt-6-astra')
        token = store.session_event('codex', event)['token']
        plain = self.result('guidance', '--token', token)
        self.assertEqual(plain['model_id'], 'gpt-6-astra')
        self.assertEqual(plain['guidance_candidates'], [])
        scoped = self.result('guidance', '--token', token, '--task-tag', 'agentic-work')
        self.assertEqual(scoped['guidance_candidates'][0]['id'], 'astra-task-boundaries')
        self.assertEqual(store.pending(), [])
        token = store.session_event('claude', dict(event, model=None))['token']
        unknown = self.result('guidance', '--token', token, '--task-tag', 'agentic-work')
        self.assertIsNone(unknown['model_id'])
        self.assertEqual(unknown['guidance_candidates'], [])
        self.assertNotEqual(self.run_cli('guidance', '--token', 'missing').returncode, 0)

    def test_progress_read_returns_current_state_without_export_file(self):
        sys.path.insert(0, str(SCRIPT.parent))
        from store import Store
        store = Store(self.root)
        self.assertIsNone(self.result('progress-read')['progress_text'])
        original = ('# Progress\nlevel: working\ncurrent_day: 1\n\n## Levers\n'
                    'noun: 3 verb: 3 adjective: 3 adverb: 3 pronoun: 3 preposition: 3 conjunction: 3 determiner: 3 numeral: 3 interjection: 3 particle: 3\n'
                    '## Tasks\n- Reports\n- Emails\n- Reviews\n## Log\n')
        source = Path(self.temp.name) / 'PROGRESS.md'
        source.write_text(original)
        store.import_progress(source)
        before = set(Path(self.temp.name).rglob('*'))
        self.assertEqual(self.result('progress-read')['progress_text'], original)
        self.assertEqual(set(Path(self.temp.name).rglob('*')), before)
        self.assertEqual(store.status()['revision'], 0)

    def test_after_result_preference_is_saved(self):
        self.result('configure','--mode','after-result')
        self.assertEqual(self.result('status')['default_mode'],'after-result')

    def test_invalid_hook_fails_open_without_creating_profile(self):
        r=self.run_cli('hook','--host','claude',input='{"hook_event_name":"Stop","session_id":"x"}')
        self.assertEqual(r.returncode,0)
        self.assertEqual(json.loads(r.stdout),{})
        self.assertIn('unavailable',r.stderr)
        self.assertFalse(self.root.exists())

    def test_recorded_event_shapes_and_negative_fixtures(self):
        sys.path.insert(0,str(SCRIPT.parent))
        from wizard import validate_event
        fixtures=SCRIPT.parents[2]/'tools/fixtures/coaching'
        for path in (fixtures/'valid').glob('*.json'):
            self.assertTrue(validate_event(path.name.split('-')[0],json.loads(path.read_text())),path.name)
        for path in (fixtures/'invalid').glob('*.json'):
            result=self.run_cli('hook','--host','codex',input=path.read_text())
            self.assertEqual(result.returncode,0)
            self.assertEqual(json.loads(result.stdout),{})
            self.assertFalse(self.root.exists())

    def test_experiment_guard_has_no_writes_context_or_warning(self):
        env=dict(os.environ,PROMPTING_WIZARD_EXPERIMENT='1')
        r=self.run_cli('hook','--host','codex',input='not even json',env=env)
        self.assertEqual(r.returncode,0)
        self.assertEqual(json.loads(r.stdout),{})
        self.assertEqual(r.stderr,'')
        self.assertFalse(self.root.exists())

    def test_invalid_and_oversized_records_are_content_free_errors(self):
        for raw in ('SECRET DATA','{"secret":"SECRET DATA"}','x'*1048577):
            r=self.run_cli('record',input=raw)
            self.assertNotEqual(r.returncode,0)
            self.assertNotIn('SECRET DATA',r.stderr)
            self.assertNotIn(raw[:20],r.stderr)

    def test_structured_argument_saves_same_validated_finding_without_shell(self):
        sys.path.insert(0,str(SCRIPT.parent))
        from store import Store
        import uuid
        store=Store(self.root);workspace=str(Path(self.temp.name)/'work');store.configure(workspace,'lesson-only')
        oid=str(uuid.uuid4())
        store.add_observation(dict(id=oid,host='claude',session_id='test',turn_id=None,workspace=workspace,model_id=None,prompt='Synthetic',result='Synthetic',context_complete=False,skill=None))
        payload={'record':dict(id=str(uuid.uuid4()),observation_id=oid,skill='numeral',explanation="Count the learner's supported items; $(not-a-command)",source_revisions=[])}
        self.result('record','--json',json.dumps(payload))
        self.assertEqual(store.pending()[0]['findings'][0]['explanation'],payload['record']['explanation'])
        result=self.run_cli('record','--json','{"untrusted":"SECRET DATA"}')
        self.assertNotEqual(result.returncode,0)
        self.assertNotIn('SECRET DATA',result.stderr)

    def test_evidence_requires_task_scope_and_returns_distinct_finding_id(self):
        sys.path.insert(0,str(SCRIPT.parent))
        from store import Store
        import uuid
        store=Store(self.root);workspace=str(Path(self.temp.name)/'work');store.configure(workspace,'lesson-only')
        oid=str(uuid.uuid4())
        store.add_observation(dict(id=oid,host='codex',session_id='test',turn_id=None,workspace=workspace,model_id='gpt-6-astra',prompt='Summarize',result='Summary',context_complete=False,skill=None))
        plain=self.result('evidence','--id',oid)
        self.assertEqual(plain['guidance_candidates'],[])
        self.assertNotEqual(plain['finding_id'],oid)
        scoped=self.result('evidence','--id',oid,'--task-tag','agentic-work')
        self.assertTrue(scoped['guidance_candidates'])

    def test_unknown_command_and_conflicting_delete_rejected(self):
        self.assertNotEqual(self.run_cli('invented').returncode,0)
        self.assertNotEqual(self.run_cli('delete','--all','--id','x').returncode,0)



class AdapterTests(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0,str(SCRIPT.parent))
        import wizard
        from store import Store
        self.handler=getattr(wizard,'handle_event',None)
        self.assertIsNotNone(self.handler,'Host event adapter not implemented')
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.store=Store(Path(self.temp.name)/'profile')
        self.workspace=str(Path(self.temp.name)/'work')
        self.store.configure(self.workspace,'after-result')

    def event(self,name,**fields):
        return dict(hook_event_name=name,session_id='main',cwd=self.workspace,**fields)

    def start(self,host):
        output=self.handler(host,self.event('SessionStart',source='startup'),self.store)
        self.assertIn('additionalContext',output['hookSpecificOutput'])

    def submit(self,host,prompt='Do synthetic work'):
        return self.handler(host,self.event('UserPromptSubmit',prompt=prompt),self.store)

    def stop(self,host,active=False,result='Completed synthetic work'):
        return self.handler(host,self.event('Stop',stop_hook_active=active,last_assistant_message=result),self.store)

    def test_wizard_commands_are_not_captured_and_next_work_is(self):
        for host in ('claude', 'codex'):
            for command in ('/pw', '/pw progress', '/prompting-wizard:pw feedback off',
                            '$pw help', '$prompting-wizard:pw examples',
                            '/pw help me write clearer instructions'):
                with self.subTest(host=host, command=command):
                    self.start(host)
                    self.submit(host, command)
                    self.assertEqual(self.stop(host), {})
                    self.assertEqual(self.store.pending(), [])
            self.submit(host, 'Explain how /pw works in my draft article')
            self.assertEqual(self.stop(host).get('decision'), 'block')
            self.assertEqual(len(self.store.pending()), 1)
            self.store.delete(all_data=True)

    def test_paused_profile_still_supplies_context_for_resume_without_capture(self):
        self.store.set_paused(True)
        self.start('claude')
        self.submit('claude', 'Synthetic work while paused')
        self.assertEqual(self.stop('claude'), {})
        self.assertEqual(self.store.pending(), [])

    def test_model_reports_update_while_capture_is_suppressed(self):
        for mode in ('paused', 'excluded', 'unconfigured', 'tutor'):
            with self.subTest(mode=mode):
                self.store.set_paused(False)
                self.store.set_excluded(self.workspace, False)
                workspace = self.workspace + '/unconfigured' if mode == 'unconfigured' else self.workspace
                start = dict(self.event('SessionStart', model='gpt-6-astra'), cwd=workspace)
                token = self.store.session_event('codex', start)['token']
                if mode == 'paused': self.store.set_paused(True)
                if mode == 'excluded': self.store.set_excluded(workspace, True)
                if mode == 'tutor': self.store.enter_session(token)
                event = dict(self.event('UserPromptSubmit', prompt='$pw model', model='claude-opus-5-5'), cwd=workspace)
                self.store.session_event('codex', event)
                self.assertEqual(self.store.session_model(token), 'claude-opus-5-5')
                self.assertEqual(self.store.pending(), [])
                self.store.session_event('codex', dict(event, model=None))
                self.assertIsNone(self.store.session_model(token))

    def test_command_steering_discards_incomplete_work_pair(self):
        self.start('codex')
        self.submit('codex', 'Draft synthetic work')
        self.submit('codex', '$pw pause')
        self.assertEqual(self.stop('codex'), {})
        self.assertEqual(self.store.pending(), [])

    def test_each_host_preserves_one_observation_and_requests_once(self):
        for host in ('claude','codex'):
            self.start(host);self.submit(host)
            self.assertEqual(self.stop(host).get('decision'),'block')
            self.assertEqual(self.stop(host),{})
            self.assertEqual(self.stop(host,True),{})
        self.assertEqual(len(self.store.pending()),2)

    def test_visible_feedback_reason_contains_no_internal_paths_or_commands(self):
        self.start('codex');self.submit('codex')
        reason=self.stop('codex')['reason']
        self.assertLess(len(reason),180)
        self.assertNotIn(str(self.store.root),reason)
        self.assertNotIn('python',reason)

    def test_real_steering_during_feedback_is_not_swallowed(self):
        self.start('codex');self.submit('codex');self.stop('codex')
        self.submit('codex','New task during coaching')
        self.assertEqual(self.stop('codex',True,'New task result'),{})
        rows=self.store.pending()
        self.assertEqual(len(rows),2)
        self.assertEqual(rows[0]['result'],'New task result')
        self.assertFalse(rows[0]['context_complete'])

    def test_same_text_after_completed_turn_is_new_attempt(self):
        self.start('claude')
        for _ in range(2):self.submit('claude');self.stop('claude')
        rows=self.store.pending();self.assertEqual(len(rows),2)
        self.assertNotEqual(rows[0]['id'],rows[1]['id'])

    def test_lesson_mode_and_experiment_do_not_collect(self):
        self.start('claude')
        with self.store._db() as db:token=db.execute('SELECT token FROM sessions').fetchone()[0]
        self.store.enter_session(token)
        self.submit('claude');self.assertEqual(self.stop('claude'),{})
        self.assertEqual(self.store.pending(),[])
        self.store.exit_session(token)
        old=os.environ.get('PROMPTING_WIZARD_EXPERIMENT')
        os.environ['PROMPTING_WIZARD_EXPERIMENT']='1'
        try:
            self.assertEqual(self.handler('claude',self.event('SessionStart'),self.store),{})
            self.submit('claude');self.stop('claude')
        finally:
            if old is None:os.environ.pop('PROMPTING_WIZARD_EXPERIMENT')
            else:os.environ['PROMPTING_WIZARD_EXPERIMENT']=old
        self.assertEqual(self.store.pending(),[])

    def test_lesson_only_saves_without_continuation(self):
        self.store.configure(self.workspace,'lesson-only')
        self.start('claude');self.submit('claude')
        self.assertEqual(self.stop('claude'),{})
        self.assertEqual(len(self.store.pending()),1)

    def test_missing_result_and_unknown_context_never_request_scoring(self):
        self.start('claude');self.submit('claude')
        self.assertEqual(self.stop('claude',result=None),{})
        self.assertFalse(self.store.pending()[0]['context_complete'])
        self.assertIsNone(self.store.pending()[0]['model_id'])

    def test_malformed_payload_does_not_write(self):
        for event in ([],self.event('UserPromptSubmit',prompt=[]),self.event('Stop',stop_hook_active='false')):
            with self.assertRaises(ValueError):self.handler('claude',event,self.store)
        self.assertEqual(self.store.pending(),[])

    def test_session_start_identity_cannot_stand_in_for_completion_identity(self):
        self.handler('claude',self.event('SessionStart',source='startup',model='claude-opus-5-5'),self.store)
        self.submit('claude');self.stop('claude')
        self.assertIsNone(self.store.pending()[0]['model_id'])

    def test_pause_exclusion_and_session_boundaries_clear_drafts(self):
        self.start('claude');self.submit('claude')
        self.store.set_paused(True);self.stop('claude');self.store.set_paused(False)
        self.assertEqual(self.stop('claude'),{})
        self.submit('claude');self.handler('claude',self.event('SessionStart',source='clear'),self.store)
        self.assertEqual(self.stop('claude'),{})
        self.assertEqual(self.store.pending(),[])

if __name__=='__main__':unittest.main()
