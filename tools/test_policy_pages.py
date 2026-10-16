import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_policy_pages as pages


class PolicyPageTests(unittest.TestCase):
    def test_published_pages_are_current(self):
        self.assertEqual(pages.main(check=True), 0)

    def test_links_become_site_or_repository_urls(self):
        html = pages.inline('See [privacy](PRIVACY.md), [setup](COACHING.md#controls) and https://example.com/a.')
        self.assertIn('href="../privacy/"', html)
        self.assertIn('href="https://github.com/Entuvo/prompting-wizard/blob/main/COACHING.md#controls"', html)
        self.assertIn('<a href="https://example.com/a">https://example.com/a</a>.', html)

    def test_text_is_escaped(self):
        self.assertEqual(pages.inline('a <b> & `x<y>`'), 'a &lt;b&gt; &amp; <code>x&lt;y&gt;</code>')

    def test_unsupported_markdown_fails(self):
        for block in ('### Deep heading', '| a | b |', '> quote', '```\ncode\n```', '1. step'):
            with self.assertRaises(ValueError, msg=block):
                pages.blocks(f'# Title\n\n{block}\n')
        with self.assertRaises(ValueError):
            pages.inline('[up](../outside.md)')


if __name__ == '__main__':
    unittest.main()
