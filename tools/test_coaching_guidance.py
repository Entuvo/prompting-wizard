import copy
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'prompting-wizard/scripts'))
try:
    from wizard import select_guidance
except ImportError:
    select_guidance=None

class GuidanceTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(select_guidance,'Guidance selector missing')
        self.manifest={'schema_version':1,'entries':[dict(id='claude-long',models=['claude-opus-5-5'],
            task_tags=['long-context'],source_url='https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices',
            checked_at='2026-10-08',revision='2026-10-08.1',lessons=[21],skills=['context-ordering'],text='Place long documents before the query.') ]}

    def test_exact_identity_and_task_scope(self):
        self.assertEqual(len(select_guidance('claude-opus-5-5',['long-context'],self.manifest)),1)
        for model in (None,'opus','claude-opus-5-5-custom','claude-opus-6'):
            self.assertEqual(select_guidance(model,['long-context'],self.manifest),[])
        self.assertEqual(select_guidance('claude-opus-5-5',[],self.manifest),[])

    def test_malformed_manifest_rejected_even_without_match(self):
        for changes in ({'source_url':'https://platform.claude.com.evil.test/doc'}, {'source_url':'https://platform.claude.com@evil.test/doc'}, {'checked_at':'tomorrow'}, {'skills':['imaginary']}, {'models':'*'}, {'lessons':[100]}):
            m=copy.deepcopy(self.manifest);m['entries'][0].update(changes)
            with self.subTest(changes=changes),self.assertRaises(ValueError): select_guidance(None,[],m)
        m=copy.deepcopy(self.manifest);m['entries']*=2
        with self.assertRaises(ValueError): select_guidance(None,[],m)

    def test_stale_sources_are_flagged_without_silent_remapping(self):
        from datetime import date
        result=select_guidance('claude-opus-5-5',['long-context'],self.manifest,today=date(2027,10,8))
        self.assertTrue(result[0]['needs_review'])
        self.assertNotIn('needs_review',self.manifest['entries'][0])

    def test_shipped_manifest_valid(self):
        path=Path(__file__).resolve().parents[1]/'prompting-wizard/references/model-guidance/manifest.json'
        self.assertTrue(path.is_file(),'Reviewed source manifest missing')
        select_guidance(None,[],json.loads(path.read_text()))

if __name__=='__main__': unittest.main()
