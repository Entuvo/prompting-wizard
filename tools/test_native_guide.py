import importlib.util
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))

class NativeGuideTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('build_native_guide'), 'Native guide builder missing')
        import build_native_guide
        self.builder=build_native_guide
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        shutil.copytree(ROOT/'prompting-wizard',self.root/'prompting-wizard')

    def test_standalone_complete_deterministic_guide_and_card(self):
        a=self.builder.build(self.root,self.root/'dist')
        first=a.read_bytes(); b=self.builder.build(self.root,self.root/'other')
        self.assertEqual(first,b.read_bytes())
        text=first.decode();skill=self.root/'prompting-wizard'
        instructions=(skill/'references/native-instructions.txt').read_text()
        self.assertLessEqual(len(instructions),1400)
        self.assertIn(instructions.strip(),text)
        for e in json.loads((skill/'references/learning-catalog.json').read_text()):
            self.assertIn(e['label'],text)
            self.assertIn('(#'+e['skill']+')',text)
        self.assertEqual(text.count('**Measures:**'),26)
        self.assertFalse(re.findall(r'\]\((?!#|https://)[^)]+\)',text))
        sys.path.insert(0,str(ROOT/'prompting-wizard/scripts'))
        import learning
        import datetime
        card=learning.parse_card((a.parent/'prompting-wizard-learning-card.md').read_text(),datetime.date(2026,10,11))
        self.assertEqual(card['events'],[])
        self.assertEqual(card['preferences']['frequency'],'occasional')

    def test_source_changes_appear_in_generated_guide(self):
        source=self.root/'prompting-wizard/references/learning-policy.md'
        source.write_text(source.read_text()+'\nUnique policy update.\n')
        self.assertIn('Unique policy update.',self.builder.build(self.root,self.root/'dist').read_text())

    def test_missing_or_duplicate_anchor_fails_before_output(self):
        rubric=self.root/'prompting-wizard/rubrics.md';original=rubric.read_text()
        for content in [original.replace('## Noun','## Missing'),original+'\n## Noun\n']:
            rubric.write_text(content)
            with self.assertRaises(ValueError):self.builder.build(self.root,self.root/'dist')
            self.assertFalse((self.root/'dist/prompting-wizard-native-guide.md').exists())

    def test_symlink_source_rejected(self):
        source=self.root/'prompting-wizard/references/learning-policy.md'
        external=self.root/'private.md';external.write_text('private');source.unlink();source.symlink_to(external)
        with self.assertRaises(ValueError):self.builder.build(self.root,self.root/'dist')

if __name__=='__main__':unittest.main()
