"""The catalogue uses GitHub's two views of the same portable Markdown file."""

import re
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'templates/README.md'
BLOCKS = CATALOG.parent / 'blocks'
FORMS = ROOT / '.github/ISSUE_TEMPLATE'
PAIR = re.compile(r'\[Вид\]\(([^)]+)\) · \[Код\]\(([^)]+)\)')


class ReadmeKit(unittest.TestCase):
    def test_one_file_per_block_in_template_catalogue(self):
        expected = set(BLOCKS.glob('*.md'))
        self.assertTrue(expected)
        # Only the live menu, not the copyable example inside a disclosure.
        menu = CATALOG.read_text().partition('<details>')[0]
        seen = []
        for view, code in PAIR.findall(menu):
            a, b = urlsplit(view), urlsplit(code)
            self.assertFalse(a.scheme or a.netloc or a.query or a.fragment)
            self.assertEqual(code, view + '?plain=1')
            self.assertEqual(parse_qs(b.query), {'plain': ['1']})
            seen.append((CATALOG.parent / a.path).resolve())
        self.assertCountEqual(seen, expected)

    def test_portable_blocks_have_no_image_dependency(self):
        for file in BLOCKS.glob('*.md'):
            text = file.read_text()
            self.assertNotRegex(text, r'<(?:img|picture|iframe|script|style)\b|!\[')
            # Root-relative links must continue to work when a snippet is moved into the root README.
            for link in re.findall(r'\]\((/[^)]+)\)', text):
                self.assertTrue((ROOT / urlsplit(link).path.lstrip('/')).exists(), (file, link))

    def test_instruction_panels_share_one_group_and_one_default(self):
        block = (BLOCKS / 'quickstart.md').read_text()
        groups = re.findall(r'^<details name="([^"]+)"( open)?>$', block, re.MULTILINE)
        self.assertEqual(len(groups), 2)
        self.assertEqual(groups[0][0], groups[1][0])
        self.assertEqual([bool(opened) for _, opened in groups], [True, False])
        self.assertEqual(block.count('</details>'), len(groups))
        self.assertIn('git show HEAD:templates/blocks/header.md', block)

    def test_proposal_opens_a_form_without_submitting_anything(self):
        for page in (CATALOG, BLOCKS / 'header.md'):
            links = re.findall(
                r'\]\((https://github\.com/overbaffe1/gitEdit/issues/new\?[^)]+)\)', page.read_text()
            )
            self.assertTrue(links, page)
            for link in links:
                (name,) = parse_qs(urlsplit(link).query)['template']
                self.assertEqual(FORMS / name, FORMS / 'readme-block.yml')
                self.assertTrue((FORMS / name).is_file())

    @unittest.skipUnless(yaml, 'install PyYAML to check the issue form schema')
    def test_issue_form_collects_intent_and_preserves_optional_markup(self):
        form = yaml.safe_load((FORMS / 'readme-block.yml').read_text())
        self.assertTrue(form['name'] and form['description'])
        fields = form['body']
        ids = [field['id'] for field in fields]
        self.assertEqual(len(ids), len(set(ids)))
        by_id = dict(zip(ids, fields, strict=True))
        self.assertEqual(by_id['surface']['type'], 'dropdown')
        self.assertGreaterEqual(len(by_id['surface']['attributes']['options']), 2)
        self.assertEqual(
            {f['id'] for f in fields if f.get('validations', {}).get('required')}, {'surface', 'purpose'}
        )
        self.assertEqual(by_id['markup']['attributes']['render'], 'markdown')
        self.assertIs(yaml.safe_load((FORMS / 'config.yml').read_text())['blank_issues_enabled'], True)
