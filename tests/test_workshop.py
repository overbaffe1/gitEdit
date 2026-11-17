"""Offline regression checks for the print workshop. Run: python3 -m unittest discover -s tests"""
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
SVG = '{http://www.w3.org/2000/svg}'


class WorkshopTest(unittest.TestCase):
    def test_clean_reprint(self):
        jobs = {'polar-press': 'polar-*.svg', 'print-ring': 'ring-*.svg',
                'maker-seals': 'seal-*.svg', 'tile-frieze': 'tile-*.svg'}
        # Generate in an empty tree: the check must not overwrite the artist's originals.
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'assets'
            scripts = Path(tmp) / 'atlas' / 'samples'
            scripts.mkdir(parents=True)
            output.mkdir()
            for job, pattern in jobs.items():
                script = shutil.copy(ROOT / 'atlas' / 'samples' / f'{job}.py', scripts)
                subprocess.run([sys.executable, script], check=True, capture_output=True)
                files = sorted(p.name for p in ASSETS.glob(pattern))
                self.assertTrue(files, pattern)
                self.assertEqual(sorted(p.name for p in output.glob(pattern)), files)
                for name in files:
                    with self.subTest(name=name):
                        self.assertEqual((output / name).read_bytes(), (ASSETS / name).read_bytes())
                        svg = ET.parse(output / name).getroot()
                        self.assertTrue(svg.findtext(SVG+'title') and svg.findtext(SVG+'desc'))
                        self.assertFalse(any(el.tag in (SVG+'image', SVG+'script', SVG+'foreignObject') for el in svg.iter()))

    def test_motion_is_opt_in(self):
        for name in ('polar-cover', 'polar-cover-compact'):
            motion = (ASSETS / f'{name}.svg').read_text(encoding='utf-8')
            still = (ASSETS / f'{name}-still.svg').read_text(encoding='utf-8')
            self.assertIn('prefers-reduced-motion: no-preference', motion)
            self.assertNotIn('@keyframes', still)
            # Same complete illustration, not a blank or different reduced-motion placeholder.
            self.assertEqual(motion.split('</style>')[1], still.split('</style>')[1])

    def test_printed_route(self):
        # Walk the midpoints in the exported artwork, independently of the typesetter's solver.
        def arcs(data):
            return [(int(x), int(y), int(x)+int(dx), int(y)+int(dy)) for x,y,dx,dy in
                    re.findall(r'M(\d+) (\d+)a20 20 0 0 [01] (-?\d+) (-?\d+)', data)]

        paths = ET.parse(ASSETS / 'tile-route.svg').findall('.//'+SVG+'g[@clip-path]/'+SVG+'path')
        base, _, overlay = paths
        gallery = ET.parse(ASSETS / 'tile-frieze.svg').find('.//'+SVG+'g[@clip-path]/'+SVG+'path')
        self.assertEqual(base.get('d'), gallery.get('d'))
        edges = defaultdict(list)
        for x,y,xx,yy in arcs(base.get('d')):
            edges[x,y].append((xx, yy))
            edges[xx,yy].append((x, y))
        previous, current = None, (47, 77)  # Entrance A in this edition.
        visited = set()
        while True:
            onward = [p for p in edges[current] if p != previous]
            if not onward:
                break
            self.assertEqual(len(onward), 1)
            previous, current = current, onward[0]
            edge = frozenset((previous, current))
            self.assertNotIn(edge, visited)
            visited.add(edge)
        self.assertEqual((len(visited), current), (30, (407, 117)))  # Exit 3.
        self.assertEqual(visited, {frozenset(((x,y), (xx,yy))) for x,y,xx,yy in arcs(overlay.get('d'))})


if __name__ == '__main__':
    unittest.main()
