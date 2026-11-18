"""Read back the colour specimens and the two portable palettes, independently of the printer."""

import csv
import re
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

try:
    from PIL.GimpPaletteFile import GimpPaletteFile
except ImportError:
    GimpPaletteFile = None

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'assets/inkbook'
SAMPLES = ROOT / 'atlas/samples'
SVG = '{http://www.w3.org/2000/svg}'
PAIRS = [('press', 'Ризограф', 'Фосфор'), ('blueprint', 'Чертёж', 'Чертёж'), ('orbit', 'Созвездие', 'Созвездие')]
ROLES = ['Фон', 'Текст', 'Акцент']


def ratio(a, b):
    def luminance(hex_colour):
        channels = [c / 255 for c in bytes.fromhex(hex_colour[1:])]
        linear = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in channels]
        return sum(x * w for x, w in zip(linear, (.2126, .7152, .0722), strict=True))

    low, high = sorted((luminance(a), luminance(b)))
    return (high + .05) / (low + .05)


class InkbookTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (SAMPLES / 'palettes.csv').open(encoding='utf-8', newline='') as src:
            cls.rows = {(r['Палитра'], r['Тема']): r for r in csv.DictReader(src)}
        cls.section = (ROOT / 'README.md').read_text(encoding='utf-8').split('#### Картотека красок\n')[1].split('\n#### ')[0]

    def test_two_impressions_and_selectable_recipes(self):
        for key, light, dark in PAIRS:
            card = ET.parse(ART / f'{key}.svg').getroot()
            self.assertTrue(card.findtext(SVG + 'title') and card.findtext(SVG + 'desc'))
            self.assertIn(f'<a href="assets/inkbook/{key}.svg"><img src="assets/inkbook/{key}.svg"', self.section)
            cells = []
            for half, row in [('light', self.rows[light, 'светлая']), ('dark', self.rows[dark, 'тёмная'])]:
                band = card.find(f'.//{SVG}g[@clip-path="url(#{half})"]')
                self.assertEqual(band.find(SVG + 'rect').get('fill'), row['Фон'])
                self.assertEqual((band.get('color'), band.get('fill')), (row['Текст'], row['Акцент']))
                self.assertIsNotNone(band.find(f'{SVG}use[@href="#plate"]'))  # same plate across the fold
                cells.append(f"**{row['Палитра']}**<br>" + ' '.join(f'`{row[k]}`' for k in ROLES))
            self.assertIn(' | '.join(cells), self.section)
        self.assertNotIn('<details', self.section)

    def test_labels_and_css_theme_pairs(self):
        css = (ART / 'inkbook.css').read_text().split('@media (prefers-color-scheme: dark) {')
        self.assertEqual(len(css), 2)
        for key, light, dark in PAIRS:
            labels = [e.text for e in ET.parse(ART / f'{key}.svg').iter(SVG + 'text') if e.text.endswith(':1')]
            for rules, label, name, mode in zip(css, labels, (light, dark), ('светлая', 'тёмная'), strict=True):
                rule = re.search(rf'\[data-inkbook="{key}"\]\s*\{{([^}}]*)\}}', rules)[1]
                values = dict(re.findall(r'--ge-(\w+):\s*(#[0-9A-F]{6});', rule))
                row = self.rows[name, mode]
                self.assertEqual([values[k] for k in ('paper', 'ink', 'accent')], [row[k] for k in ROLES])
                self.assertEqual(label, f"{ratio(values['paper'], values['ink']):.2f}:1".replace('.', ','))
                use_accent = ratio(values['paper'], values['accent']) >= 4.5
                self.assertEqual(values['link'], values['accent'] if use_accent else values['ink'])
                self.assertGreaterEqual(ratio(values['paper'], values['link']), 4.5)

    @unittest.skipUnless(GimpPaletteFile, 'Pillow needed for an independent GIMP palette reader')
    def test_importable_named_swatches(self):
        path = ART / 'inkbook.gpl'
        with path.open('rb') as src:
            pixels, mode = GimpPaletteFile(src).getpalette()
        rows = [self.rows[name, mode] for _, light, dark in PAIRS for name, mode in [(light, 'светлая'), (dark, 'тёмная')]]
        expected = b''.join(bytes.fromhex(r[k][1:]) for r in rows for k in ROLES)
        # Some older Pillow versions pad the palette out to 256 entries.
        self.assertEqual((mode, pixels[:len(expected)]), ('RGB', expected))
        fields = path.read_text(encoding='utf-8').splitlines()
        self.assertIn('Columns: 3', fields)
        self.assertEqual([s.split('\t')[-1] for s in fields if '\t' in s],
                         [f"{r['Палитра']} / {r['Тема']} / {k.lower()}" for r in rows for k in ROLES])

    def test_clean_reprint(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            subprocess.run([sys.executable, SAMPLES / 'inkbook/print.py', '--out', out], check=True)
            self.assertEqual({p.name for p in out.iterdir()}, {p.name for p in ART.iterdir()})
            for p in out.iterdir():
                self.assertEqual(p.read_bytes(), (ART / p.name).read_bytes(), p.name)
