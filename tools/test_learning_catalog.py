import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'prompting-wizard'
sys.path.insert(0, str(SKILL / 'scripts'))
import store

class CatalogTests(unittest.TestCase):
    def test_catalog_covers_actual_rubrics_and_lessons(self):
        path = SKILL / 'references/learning-catalog.json'
        self.assertTrue(path.is_file(), 'Everyday curriculum catalog missing')
        entries = json.loads(path.read_text())
        self.assertEqual(len(entries), 26)
        self.assertEqual({e['skill'] for e in entries}, store.SKILLS)
        rubrics = (SKILL / 'rubrics.md').read_text()
        anchors = [h.lower().replace(' ', '-') for h in re.findall(r'^## (.+)$', rubrics, re.M)]
        for e in entries:
            self.assertEqual(set(e), {'skill', 'label', 'lesson', 'rubric'})
            self.assertEqual(e['rubric'], 'rubrics.md#' + e['skill'])
            self.assertEqual(anchors.count(e['skill']), 1)
            self.assertTrue((SKILL / e['lesson']).is_file())
            self.assertIn('## Concept', (SKILL / e['lesson']).read_text())
        by_id = {e['skill']: e for e in entries}
        for skill, day in [('noun', 1), ('writing-evals', 25), ('capstone', 29)]:
            self.assertEqual(by_id[skill]['lesson'], f'days/{day:02d}.md')

if __name__ == '__main__':
    unittest.main()
