"""Persistence contracts: losing evidence or accepting stale progress must fail."""
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
import uuid

SCRIPTS = Path(__file__).resolve().parents[1] / 'prompting-wizard/scripts'
sys.path.insert(0, str(SCRIPTS))
try:
    from store import Store, RevisionConflict
except ImportError:
    Store = None
    RevisionConflict = RuntimeError


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(Store, 'Shared learner store is not implemented')
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'learner'
        self.clock = 1000000.0
        self.store = Store(self.root, clock=lambda: self.clock)
        self.workspace = str(Path(self.temp.name) / 'work $(not-a-command)')
        self.store.configure(self.workspace, 'lesson-only')

    def observation(self, **changes):
        record = dict(id=str(uuid.uuid4()), host='claude', session_id='synthetic',
                      turn_id=None, workspace=self.workspace, model_id=None,
                      prompt='Summarize the supplied report', result='Three findings',
                      context_complete=False, skill=None)
        record.update(changes)
        return record

    def lesson(self, ids, **changes):
        record = dict(id=str(uuid.uuid4()), kind='lesson', schema_version=1,
                      observation_ids=ids, skill='noun', explanation='Name the artifact',
                      reflection='I will name the report', confirmed=True,
                      source_revisions=[], approved_excerpt='')
        record.update(changes)
        return record

    def test_duplicate_ids_are_idempotent_but_same_text_is_not(self):
        a = self.observation()
        self.store.add_observation(a)
        self.store.add_observation(a)
        self.store.add_observation(self.observation())
        self.assertEqual(len(self.store.pending()), 2)
        self.assertTrue(self.store.claim_coaching(a['id']))
        self.assertFalse(self.store.claim_coaching(a['id']))

    def test_pause_and_parent_exclusion_reject_content_preserve_mode(self):
        self.store.configure(None, 'after-result')
        self.store.set_paused(True)
        self.assertIsNone(self.store.add_observation(self.observation()))
        self.store.set_paused(False)
        self.assertEqual(self.store.mode(self.workspace), 'lesson-only')
        self.store.configure(self.workspace+'/child','lesson-only')
        self.store.set_excluded(self.workspace, True)
        self.assertIsNone(self.store.add_observation(self.observation(workspace=self.workspace+'/child')))
        self.assertEqual(self.store.pending(), [])

    def test_explicit_inclusion_uses_default_until_overridden(self):
        workspace=str(Path(self.temp.name)/'another-workspace')
        self.store.configure(None,'after-result')
        self.store.set_excluded(workspace,False)
        self.assertEqual(self.store.mode(workspace),'after-result')
        self.store.configure(workspace,'lesson-only')
        self.store.configure(None,'after-result')
        self.assertEqual(self.store.mode(workspace),'lesson-only')

    def test_unknown_workspace_requires_explicit_enablement(self):
        self.assertIsNone(self.store.add_observation(self.observation(workspace='/different')))

    def test_expiry_removes_raw_and_derivative_but_not_reviewed(self):
        a,b = self.observation(), self.observation()
        for x in (a,b): self.store.add_observation(x)
        self.store.add_finding(dict(id=str(uuid.uuid4()), observation_id=a['id'],
                                   skill='noun', explanation='Name report', source_revisions=[]))
        self.store.commit_lesson(self.lesson([b['id']]), 0)
        self.clock += 30 * 86400
        self.assertEqual(self.store.pending(), [])
        self.assertIsNone(self.store.evidence(a['id']))
        self.assertEqual(len(self.store.list_records('reviewed')['records']), 1)
        with sqlite3.connect(self.root/'learner.sqlite3') as db:
            self.assertEqual(db.execute('SELECT count(*) FROM findings').fetchone()[0], 0)

    def test_stale_lesson_keeps_evidence_and_success_deletes_raw(self):
        a,b = self.observation(), self.observation()
        for x in (a,b): self.store.add_observation(x)
        self.assertEqual(self.store.commit_lesson(self.lesson([a['id']]), 0), 1)
        with self.assertRaises(RevisionConflict): self.store.commit_lesson(self.lesson([b['id']]), 0)
        self.assertIsNotNone(self.store.evidence(b['id']))
        self.assertIsNone(self.store.evidence(a['id']))
        with self.assertRaises(ValueError): self.store.commit_lesson(self.lesson([b['id']], confirmed=False), 1)

    def test_unicode_excerpt_bounded_without_broken_encoding(self):
        a = self.observation(prompt='é'*10000)
        self.store.add_observation(a)
        got = self.store.evidence(a['id'])
        self.assertLessEqual(len(got['prompt'].encode()), 16384)
        self.assertTrue(got['truncated'])

    def test_queue_limit_visible_without_evicting_old_examples(self):
        for _ in range(1000): self.store.add_observation(self.observation())
        self.assertIsNone(self.store.add_observation(self.observation()))
        self.assertEqual(self.store.status()['pending'], 1000)
        self.assertEqual(self.store.status()['warning'], 'pending_queue_full')

    def test_untrusted_record_fields_rejected_before_write(self):
        for changes in [dict(host='invented'),dict(context_complete='yes'),dict(skill='invented'),dict(result=[]),dict(extra='bad')]:
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                self.store.add_observation(self.observation(**changes))
        self.assertEqual(self.store.pending(), [])

    def test_permissions_and_symlinks(self):
        self.assertEqual(self.root.stat().st_mode & 0o777, 0o700)
        self.assertEqual((self.root/'learner.sqlite3').stat().st_mode & 0o777, 0o600)
        link = Path(self.temp.name)/'link'
        link.symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(ValueError): Store(link)
        db = self.root/'learner.sqlite3'
        db.rename(self.root/'original')
        db.symlink_to(self.root/'original')
        with self.assertRaises(ValueError): self.store.pending()

    def test_newer_schema_and_corrupt_database_never_reset(self):
        dbpath=self.root/'learner.sqlite3'
        with sqlite3.connect(dbpath) as db: db.execute('PRAGMA user_version=99')
        original=dbpath.read_bytes()
        with self.assertRaises(ValueError): Store(self.root)
        self.assertEqual(dbpath.read_bytes(), original)
        dbpath.write_bytes(b'not sqlite')
        with self.assertRaises((ValueError, sqlite3.DatabaseError)): Store(self.root)
        self.assertEqual(dbpath.read_bytes(), b'not sqlite')

    def test_inspection_pagination_and_bulk_deletion(self):
        for _ in range(105): self.store.add_observation(self.observation())
        first=self.store.list_records('all')
        second=self.store.list_records('all',first['cursor'])
        self.assertEqual(len(first['records'])+len(second['records']),105)
        self.store.delete(workspace=self.workspace)
        self.assertEqual(self.store.list_records('all')['records'],[])
        with self.assertRaises(ValueError): self.store.delete()

    def test_session_lease_expires(self):
        token=self.store.register_session('claude','native',self.workspace)
        self.store.enter_session(token)
        self.assertTrue(self.store.in_lesson('claude','native'))
        self.clock+=7200
        self.assertFalse(self.store.in_lesson('claude','native'))
        with self.assertRaises(ValueError): self.store.enter_session(str(uuid.uuid4()))

    def test_progress_preserves_exact_baseline_and_conflicts(self):
        original=('# Progress\nlevel: working\ncurrent_day: 1\n\n## Levers\n'
                  'noun: 3 verb: 3 adjective: 3 adverb: 3 pronoun: 3 preposition: 3 conjunction: 3 determiner: 3 numeral: 3 interjection: 3 particle: 3\n## Tasks\n- Reports\n- Emails\n- Reviews\n## Log\n- Day 0 — assessment — baseline noun 3, verb 3, adjective 3, adverb 3, pronoun 3, preposition 3, conjunction 3, determiner 3, numeral 3, interjection 3, particle 3\n')
        source=Path(self.temp.name)/'PROGRESS.md'; source.write_text(original)
        digest=self.store.import_progress(source)
        self.assertEqual(self.store.import_progress(source),digest)
        target=Path(self.temp.name)/'export.md'; self.store.export_progress(target)
        self.assertEqual(target.read_bytes(),source.read_bytes())
        source.write_text(original.replace('current_day: 1','current_day: 2'))
        with self.assertRaises(RevisionConflict): self.store.import_progress(source)
        self.store.export_progress(target)
        self.assertEqual(target.read_text(),original)

    def test_rebuilt_completed_progress_roundtrips_without_invented_baseline(self):
        source=Path(self.temp.name)/'rebuilt.md'
        text=('# Progress\nlevel: advanced\ncurrent_day: 31\n## Levers\n'
              'noun: 4 verb: 4 adjective: 4 adverb: 4 pronoun: 4 preposition: 4 conjunction: 4 determiner: 4 numeral: 4 interjection: 4 particle: 4\n'
              '## Tasks\n- Reports\n- Emails\n- Reviews\n## Log\n')
        source.write_text(text)
        self.store.import_progress(source)
        target=Path(self.temp.name)/'roundtrip.md'; self.store.export_progress(target)
        self.assertEqual(target.read_text(), text)

    def test_malformed_progress_is_not_accepted(self):
        source=Path(self.temp.name)/'bad.md'
        source.write_text('# Progress\ncurrent_day: 1\n- Day 0 — baseline noun 3\n')
        with self.assertRaises(ValueError): self.store.import_progress(source)

    def test_journal_symlink_rejected_without_target_mutation(self):
        target=Path(self.temp.name)/'valuable'; target.write_text('keep me')
        Path(str(self.root/'learner.sqlite3')+'-journal').symlink_to(target)
        with self.assertRaises(ValueError): self.store.pending()
        self.assertEqual(target.read_text(),'keep me')

    def test_duplicate_id_with_changed_content_is_conflict(self):
        a=self.observation(); self.store.add_observation(a)
        with self.assertRaises(RevisionConflict): self.store.add_observation(dict(a,result='different'))
        self.assertEqual(self.store.evidence(a['id'])['result'],'Three findings')

    def test_expired_read_does_not_resurrect_with_old_clock_argument(self):
        self.store.add_observation(self.observation())
        self.clock+=30*86400
        self.assertEqual(self.store.pending(now=1000000),[])

    def test_lesson_updates_current_course_but_preserves_original_baseline(self):
        original=('# Progress\nlevel: working\ncurrent_day: 1\n## Levers\n'
                  'noun: 3 verb: 3 adjective: 3 adverb: 3 pronoun: 3 preposition: 3 conjunction: 3 determiner: 3 numeral: 3 interjection: 3 particle: 3\n'
                  '## Tasks\n- Reports\n- Emails\n- Reviews\n## Log\n'
                  '- Day 0 — assessment — baseline noun 3, verb 3, adjective 3, adverb 3, pronoun 3, preposition 3, conjunction 3, determiner 3, numeral 3, interjection 3, particle 3\n')
        source=Path(self.temp.name)/'progress.md';source.write_text(original)
        self.store.import_progress(source)
        item=self.observation();self.store.add_observation(item)
        updated=original.replace('current_day: 1','current_day: 2')+'- Day 1 — noun — rubric 4\n'
        wrong=updated.replace('baseline noun 3','baseline noun 5')
        with self.assertRaises(ValueError):self.store.commit_lesson(self.lesson([item['id']],progress_text=wrong),0)
        self.assertIsNotNone(self.store.evidence(item['id']))
        self.store.commit_lesson(self.lesson([item['id']],progress_text=updated),0)
        output=Path(self.temp.name)/'updated.md';self.store.export_progress(output)
        self.assertEqual(output.read_text(),updated)
        self.store.import_progress(output)  # Current exported state is not a conflicting history.
        with sqlite3.connect(self.root/'learner.sqlite3') as db:
            self.assertEqual(db.execute('SELECT original FROM progress').fetchone()[0],original.encode())
        self.assertNotIn('progress_text',self.store.list_records('reviewed')['records'][0]['data'])
        source.write_text(original)
        with self.assertRaises(RevisionConflict):self.store.import_progress(source)
        next_item=self.observation();self.store.add_observation(next_item)
        rewritten=updated.replace('current_day: 2','current_day: 3').replace('- Day 1 — noun — rubric 4\n','')+'- Day 2 — verb — exercise 4\n'
        with self.assertRaises(ValueError):self.store.commit_lesson(self.lesson([next_item['id']],progress_text=rewritten),1)

    def test_empty_example_lesson_advances_shared_progress(self):
        original=('# Progress\nlevel: working\ncurrent_day: 1\n## Levers\n'
                  'noun: 3 verb: 3 adjective: 3 adverb: 3 pronoun: 3 preposition: 3 conjunction: 3 determiner: 3 numeral: 3 interjection: 3 particle: 3\n'
                  '## Tasks\n- Reports\n- Emails\n- Reviews\n## Log\n')
        source=Path(self.temp.name)/'progress.md';source.write_text(original)
        self.store.import_progress(source)
        updated=original.replace('current_day: 1','current_day: 2')+'- Day 1 — noun — exercise 4\n'
        record=self.lesson([],workspace=self.workspace,progress_text=updated)
        self.store.commit_lesson(record,0)
        self.store.export_progress(source)
        self.assertEqual(source.read_text(),updated)
        self.store.import_progress(source)
        with self.assertRaises(RevisionConflict):self.store.commit_lesson(record,0)
        external=updated.replace('current_day: 2','current_day: 3')+'- Day 2 — verb — exercise 4\n'
        source.write_text(external)
        with self.assertRaises(RevisionConflict):self.store.import_progress(source)
        self.store.import_progress(source,expected_revision=1)
        self.assertEqual(self.store.status()['revision'],2)
        self.store.export_progress(source);self.assertEqual(source.read_text(),external)
        source.write_text(external.replace('- Day 1 — noun — exercise 4\n',''))
        with self.assertRaises(ValueError):self.store.import_progress(source,expected_revision=2)

    def test_finding_id_cannot_alias_source_and_typed_delete_is_precise(self):
        item=self.observation();self.store.add_observation(item)
        finding=dict(id=item['id'],observation_id=item['id'],skill='noun',explanation='Name artifact',source_revisions=[])
        with self.assertRaises(ValueError):self.store.add_finding(finding)
        finding['id']=str(uuid.uuid4());self.store.add_finding(finding)
        self.store.delete(id=finding['id'],kind='finding')
        self.assertIsNotNone(self.store.evidence(item['id']))

    def test_pending_exposes_newest_examples_beyond_first_page(self):
        for index in range(101):
            self.clock+=1;item=self.observation(prompt=str(index));self.store.add_observation(item)
        self.assertEqual(self.store.pending()[0]['prompt'],'100')

    def test_saved_hypothesis_is_available_in_matching_lesson(self):
        item=self.observation();self.store.add_observation(item)
        finding=dict(id=str(uuid.uuid4()),observation_id=item['id'],skill='verb',explanation='Name the operation',source_revisions=[])
        self.store.add_finding(finding)
        self.assertEqual(self.store.pending('noun'),[])
        self.assertEqual(self.store.pending('verb')[0]['findings'][0]['explanation'],'Name the operation')
        self.store.delete(id=finding['id'])
        self.assertEqual(self.store.pending('noun')[0]['findings'],[])

    def test_data_root_cannot_be_inside_captured_workspace(self):
        with self.assertRaises(ValueError): self.store.configure(self.temp.name,'lesson-only')

    def test_concurrent_lessons_claim_only_one_revision(self):
        records=[self.observation(),self.observation()]
        for item in records:self.store.add_observation(item)
        script=("from store import Store,RevisionConflict; import json,sys; "
                "s=Store(__import__('pathlib').Path(sys.argv[1]),clock=lambda:1000000.0); "
                "r=json.loads(sys.argv[2]); "
                "exec('try: s.commit_lesson(r,0)\\nexcept RevisionConflict: sys.exit(2)')")
        env=dict(os.environ,PYTHONPATH=str(SCRIPTS))
        children=[subprocess.Popen([sys.executable,'-c',script,str(self.root),json.dumps(self.lesson([r['id']]))],env=env) for r in records]
        self.assertEqual(sorted(c.wait() for c in children),[0,2])
        self.assertEqual(len(self.store.pending()),1)
        self.assertEqual(len(self.store.list_records('reviewed')['records']),1)

    def test_disappearing_optional_journal_does_not_reject_valid_database(self):
        from unittest.mock import patch
        original=Store._check_path
        def check(path,directory=False):
            if str(path).endswith('-journal'): raise FileNotFoundError('Journal committed by concurrent writer')
            return original(path,directory)
        journal=Path(str(self.store.path)+'-journal');journal.touch(mode=0o600)
        try:
            with patch.object(Store,'_check_path',side_effect=check):self.store._check_files()
        finally:journal.unlink()

    def test_concurrent_processes_do_not_lose_observations(self):
        script = 'from store import Store; import json,sys; Store(__import__("pathlib").Path(sys.argv[1])).add_observation(json.loads(sys.argv[2]))'
        env=dict(os.environ,PYTHONPATH=str(SCRIPTS))
        children=[subprocess.Popen([sys.executable,'-c',script,str(self.root),json.dumps(self.observation())],env=env) for _ in range(8)]
        self.assertEqual([child.wait() for child in children],[0]*len(children))
        self.assertEqual(len(self.store.pending()),8)


if __name__=='__main__': unittest.main()
