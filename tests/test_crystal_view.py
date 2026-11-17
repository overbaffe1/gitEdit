"""The shared crystal link must be useful before (or without) a 3D viewer."""
import re
import unittest
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Tags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.by_tag = defaultdict(list)

    def handle_starttag(self, tag, attrs):
        self.by_tag[tag].append(dict(attrs))


class CrystalViewTest(unittest.TestCase):
    def test_stable_landing_and_opt_in_model(self):
        before, after = (ROOT / 'README.md').read_text(encoding='utf-8').split('\n### Покрути кристалл\n')
        self.assertIn('href="#покрути-кристалл"', before)
        section = re.split(r'^#{1,3} ', after, maxsplit=1, flags=re.M)[0]
        tags = Tags()
        tags.feed(section)
        self.assertNotIn('```stl', section.lower())
        self.assertNotIn('iframe', tags.by_tag)
        self.assertIn('](atlas/samples/crystal.stl)', section)
        self.assertTrue((ROOT / 'atlas/samples/crystal.stl').is_file())

        panels = tags.by_tag['details']
        self.assertEqual(len(panels), 4)
        group = panels[0].get('name')
        self.assertTrue(group)
        self.assertTrue(all(p.get('name') == group for p in panels))
        self.assertEqual(['open' in p for p in panels], [True, False, False, False])
        images = [i['src'] for i in tags.by_tag['img']]
        self.assertEqual(len(images), len(set(images)))
        self.assertEqual(len(images), len(panels))
        # Matching intrinsic sizes keep the slot the same height between turns.
        headers = [(ROOT / src).read_bytes()[:24] for src in images]
        self.assertTrue(all(h.startswith(b'\x89PNG\r\n\x1a\n') for h in headers))
        self.assertEqual(len({h[16:24] for h in headers}), 1)
