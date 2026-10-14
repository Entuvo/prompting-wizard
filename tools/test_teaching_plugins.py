"""Contracts for the native teaching plugin, independent of host UI availability."""
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))


class TeachingPluginTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('build_teaching_plugins'),
                             'Native teaching plugin builder missing')
        import build_teaching_plugins
        self.builder = build_teaching_plugins
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for name in ('prompting-wizard', 'plugins/prompting-wizard-teacher', 'assets/listing', '.claude-plugin', '.agents/plugins'):
            shutil.copytree(ROOT / name, self.root / name)
        shutil.copy2(ROOT / 'LICENSE', self.root / 'LICENSE')

    def test_self_contained_identical_teaching_payloads(self):
        paths = self.builder.build(self.root, self.root / 'dist')
        self.assertEqual(len(paths), 2)
        payloads = []
        for path in paths:
            with zipfile.ZipFile(path) as z:
                names = z.namelist()
                self.assertIn('skills/learn/SKILL.md', names)
                self.assertIn('skills/learn/references/guide.md', names)
                self.assertIn('skills/learn/references/empty-card.md', names)
                self.assertFalse(any(n.endswith('.py') or 'hooks' in n or 'mcp' in n for n in names))
                payloads.append({n: z.read(n) for n in names if n.startswith('skills/')})
                manifest = json.loads(z.read('plugin.json' if 'chatgpt' in path.name else '.claude-plugin/plugin.json'))
                self.assertEqual(manifest['name'], 'prompting-wizard-teacher')
                self.assertEqual(manifest['version'], '0.2.0')
                self.assertIn('LICENSE', names)
                self.assertIn('README.md', names)
                self.assertEqual(z.read('README.md'),
                                 (self.root / 'plugins/prompting-wizard-teacher/README.md').read_bytes())
        self.assertEqual(*payloads)
        guide = payloads[0]['skills/learn/references/guide.md'].decode()
        self.assertEqual(guide.count('**Measures:**'), 26)
        sys.path.insert(0, str(ROOT / 'prompting-wizard/scripts'))
        import learning
        from datetime import date
        card = learning.parse_card(payloads[0]['skills/learn/references/empty-card.md'].decode(), date(2026, 10, 12))
        self.assertEqual(card['events'], [])

    def test_deterministic_allowlist_excludes_accidental_state(self):
        plugin = self.root / 'plugins/prompting-wizard-teacher'
        (plugin / 'LEARNING.md').write_text('PRIVATE STATE')
        a = [p.read_bytes() for p in self.builder.build(self.root, self.root / 'a')]
        b = [p.read_bytes() for p in self.builder.build(self.root, self.root / 'b')]
        self.assertEqual(a, b)
        for path in (self.root / 'a').glob('*.zip'):
            with zipfile.ZipFile(path) as z:
                self.assertNotIn('LEARNING.md', z.namelist())
                self.assertFalse(any(b'PRIVATE STATE' in z.read(n) for n in z.namelist()))

    def test_symlink_source_rejected_before_archives(self):
        for name in ('plugins/prompting-wizard-teacher/skills/learn/SKILL.md',
                     'plugins/prompting-wizard-teacher/README.md',
                     'assets/listing/logo.png', 'LICENSE'):
            p = self.root / name
            old = p.read_bytes()
            other = self.root / 'outside'; other.write_bytes(old)
            p.unlink(); p.symlink_to(other)
            with self.assertRaises(ValueError):
                self.builder.build(self.root, self.root / 'dist')
            self.assertFalse(list((self.root / 'dist').glob('*.zip')))
            p.unlink(); p.write_bytes(old)

    def test_generated_tree_detects_drift_and_extras(self):
        self.builder.sync(self.root)
        self.assertEqual(self.builder.check(self.root), [])
        path = self.root / 'plugins/prompting-wizard-teacher/skills/learn/references/guide.md'
        path.write_text('stale')
        self.assertTrue(self.builder.check(self.root))
        self.builder.sync(self.root)
        path.parent.joinpath('private.md').write_text('private')
        self.assertTrue(self.builder.check(self.root))

    def test_sync_rejects_symlink_destination(self):
        p = self.root / 'plugins/prompting-wizard-teacher/skills/learn/references'
        shutil.rmtree(p)
        outside = self.root / 'outside'; outside.mkdir()
        p.symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ValueError):
            self.builder.sync(self.root)
        self.assertEqual(list(outside.iterdir()), [])

    def test_marketplace_mismatch_is_reported(self):
        path = self.root / '.agents/plugins/marketplace.json'
        data = json.loads(path.read_text())
        data['plugins'][-1]['version'] = '9.9.9'
        path.write_text(json.dumps(data))
        self.assertTrue(self.builder.check(self.root))

    def test_manifest_version_mismatch_prevents_output(self):
        path = self.root / 'plugins/prompting-wizard-teacher/.claude-plugin/plugin.json'
        data = json.loads(path.read_text()); data['version'] = '9.9.9'
        path.write_text(json.dumps(data))
        with self.assertRaises(ValueError):
            self.builder.build(self.root, self.root / 'dist')
        self.assertFalse(list((self.root / 'dist').glob('*.zip')))

    def test_long_skill_description_prevents_packaging(self):
        path = self.root / 'plugins/prompting-wizard-teacher/skills/learn/SKILL.md'
        text = path.read_text()
        old = next(line for line in text.splitlines() if line.startswith('description:'))
        path.write_text(text.replace(old, 'description: ' + 'x' * 201))
        with self.assertRaisesRegex(ValueError, '200-character'):
            self.builder.build(self.root, self.root / 'dist')
        self.assertFalse(list((self.root / 'dist').glob('*.zip')))

    def test_listing_readme_requires_40_words_outside_code_blocks(self):
        path = self.root / 'plugins/prompting-wizard-teacher/README.md'
        for fence in ('```', '~~~~'):
            path.write_text('Short listing.\n' + fence + '\n' + 'word ' * 50 + '\n' + fence + '\n')
            with self.assertRaisesRegex(ValueError, 'README.*40 words'):
                self.builder.build(self.root, self.root / 'dist')
            self.assertFalse(list((self.root / 'dist').glob('*.zip')))

    def test_canonical_policy_change_reaches_both_packages(self):
        p = self.root / 'prompting-wizard/references/learning-policy.md'
        p.write_text(p.read_text() + '\nUnique policy revision.\n')
        for path in self.builder.build(self.root, self.root / 'dist'):
            with zipfile.ZipFile(path) as z:
                self.assertIn(b'Unique policy revision.', z.read('skills/learn/references/guide.md'))


if __name__ == '__main__':
    unittest.main()
