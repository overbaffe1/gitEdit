"""Portable SVG room: reproducibility, data integrity and README wiring."""
import csv
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'assets/afterlight'
GEN = ROOT / 'atlas/samples/afterlight/generate.py'
NS = {'s': 'http://www.w3.org/2000/svg'}
NAMES = {'moire', 'pendulum', 'harmonograph', 'phyllotaxis', 'contours', 'metaballs',
         'guilloche', 'truchet', 'textpath', 'spirograph', 'phase', 'paper'}


class AfterlightTest(unittest.TestCase):
    def test_clean_reprint_has_no_readme_side_effect(self):
        before = (ROOT / 'README.md').read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'print'
            subprocess.run([sys.executable, str(GEN), '--output', str(out)], check=True, cwd=tmp)
            self.assertEqual({p.name for p in out.iterdir()}, {p.name for p in ART.iterdir()})
            for file in ART.iterdir():
                self.assertEqual(file.read_bytes(), (out / file.name).read_bytes(), file.name)
        self.assertEqual((ROOT / 'README.md').read_bytes(), before)

    def test_twelve_self_contained_accessible_svgs(self):
        self.assertEqual({p.stem for p in ART.glob('*.svg')}, NAMES)
        for file in ART.glob('*.svg'):
            svg = ET.parse(file).getroot()
            self.assertEqual(svg.attrib['viewBox'], '0 0 960 360')
            self.assertTrue(svg.find('s:title', NS).text)
            self.assertTrue(svg.find('s:desc', NS).text)
            ids = {n.attrib['id'] for n in svg.iter() if 'id' in n.attrib}
            for node in svg.iter():
                self.assertNotIn(node.tag.rsplit('}', 1)[-1], {'script', 'foreignObject', 'image', 'animate', 'animateMotion'})
                for key, value in node.attrib.items():
                    self.assertFalse(key.startswith('on'), (file, key))
                    if key.rsplit('}', 1)[-1] == 'href':
                        self.assertTrue(value.startswith('#'), (file, value))
                        self.assertIn(value[1:], ids)
                    for ref in re.findall(r'url\(#([^)]+)\)', value):
                        self.assertIn(ref, ids)
            self.assertLess(file.stat().st_size, 150_000)

    def test_motion_is_css_only_with_visible_base_state(self):
        animated = []
        for file in ART.glob('*.svg'):
            source = file.read_text()
            self.assertIn('@media(prefers-reduced-motion:reduce){.moving{animation:none!important}}', source)
            if '@keyframes' in source:
                animated.append(file.stem)
            self.assertNotIn('opacity="0"', source)
        self.assertEqual(len(animated), 7)
        # Even without CSS, moire keeps an actual angle between its gratings.
        self.assertIn('transform="rotate(7 480 195)"', (ART / 'moire.svg').read_text())

    def test_catalogs_agree_and_report_real_byte_counts(self):
        tables = []
        for extension, delimiter in [('csv', ','), ('tsv', '\t')]:
            tables.append(list(csv.DictReader(io.StringIO((ART / f'catalog.{extension}').read_text()), delimiter=delimiter)))
        self.assertEqual(tables[0], tables[1])
        self.assertEqual({row['exhibit'] for row in tables[0]}, NAMES)
        for row in tables[0]:
            self.assertEqual(int(row['bytes']), (ART / (row['exhibit'] + '.svg')).stat().st_size)

    def test_notebook_contains_saved_output_matching_its_code(self):
        nb = json.loads((ART / 'phyllotaxis.ipynb').read_text())
        self.assertEqual(nb['nbformat'], 4)
        cell = nb['cells'][1]
        self.assertEqual(cell['execution_count'], 1)
        saved = ''.join(cell['outputs'][0]['data']['image/svg+xml'])
        self.assertEqual(len(ET.fromstring(saved).findall('s:circle', NS)), 420)
        # Replace IPython's display objects, then execute our own shipped code.
        code = ''.join(cell['source']).replace('from IPython.display import SVG, display', '')
        captured = []
        exec(compile(code, 'phyllotaxis.ipynb', 'exec'), {'SVG': lambda x: x, 'display': captured.append})
        self.assertEqual(captured, [saved])

    def test_readme_embeds_every_plate_and_links_to_native_files(self):
        readme = (ROOT / 'README.md').read_text()
        room = readme.split('## Afterlight · ещё двенадцать способов удивить\n', 1)[1].split('## Две карты\n', 1)[0]
        embeds = re.findall(r'<img src="assets/afterlight/([^"]+)"[^>]+alt="([^"]+)"', room)
        self.assertEqual({Path(name).stem for name, _ in embeds}, NAMES)
        self.assertEqual(len(embeds), 12)
        for _, alt in embeds:
            self.assertGreater(len(alt), 30)
        for name in ['catalog.csv', 'catalog.tsv', 'phyllotaxis.ipynb']:
            self.assertIn(f'](assets/afterlight/{name})', room)
        self.assertIn('](atlas/afterlight.md)', room)
        self.assertIn('](atlas/samples/afterlight/surfaces.mmd)', room)
