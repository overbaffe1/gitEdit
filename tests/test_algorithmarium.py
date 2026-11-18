"""Check the algorithms behind the decoration, not just file presence."""
import csv
import importlib.util
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'assets/algorithmarium'
GEN = ROOT / 'atlas/samples/algorithmarium/generate.py'
spec = importlib.util.spec_from_file_location('algorithmarium', GEN)
gen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)
NAMES = {'rule90', 'hilbert', 'sorting', 'bezier', 'fourier', 'voronoi', 'tree', 'interference'}
NS = {'s': 'http://www.w3.org/2000/svg'}


class AlgorithmariumTest(unittest.TestCase):
    def test_clean_reprint(self):
        readme = (ROOT / 'README.md').read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run([sys.executable, str(GEN), '--output', tmp], cwd=tmp, check=True)
            self.assertEqual({p.name for p in ART.iterdir()}, {p.name for p in Path(tmp).iterdir()})
            for file in ART.iterdir():
                self.assertEqual(file.read_bytes(), (Path(tmp) / file.name).read_bytes(), file.name)
        self.assertEqual(readme, (ROOT / 'README.md').read_bytes())

    def test_xor_automaton(self):
        rows = gen.rule90()
        self.assertEqual(len(rows), 55)
        self.assertEqual(sum(rows[0]), 1)
        self.assertEqual(rows[0][55], 1)
        for a,b in zip(rows, rows[1:]):
            self.assertEqual(len(b), 111)
            for x,cell in enumerate(b):
                self.assertEqual(cell, (a[x-1] if x else 0) ^ (a[x+1] if x<110 else 0))

    def test_hilbert_coverage_and_neighbors(self):
        for order in range(1,6):
            points = gen.hilbert(order)
            n = 2**order
            self.assertEqual(set(points), {(x,y) for x in range(n) for y in range(n)})
            self.assertEqual(len(points), n*n)
            for (x,y),(u,v) in zip(points, points[1:]):
                self.assertEqual(abs(x-u)+abs(y-v), 1)

    def test_sorting_is_real_adjacent_swaps(self):
        values = [8,3,10,1,7,4,9,2,6,5]
        states = gen.sorting_states(values)
        inversions = sum(a>b for i,a in enumerate(values) for b in values[i+1:])
        self.assertEqual(len(states)-1, inversions)
        self.assertEqual(states[0], values)
        self.assertEqual(states[-1], sorted(values))
        for a,b in zip(states,states[1:]):
            self.assertEqual(sorted(a), sorted(b))
            changed = [i for i in range(len(a)) if a[i]!=b[i]]
            self.assertEqual(len(changed), 2)
            i,j = changed
            self.assertEqual(j,i+1)
            self.assertEqual((a[i],a[j]), (b[j],b[i]))
            self.assertGreater(a[i],a[j])

    def test_bezier_matches_bernstein_form(self):
        p = [(70,320),(200,100),(690,100),(880,320)]
        self.assertEqual(gen.bezier(p,0), p[0])
        self.assertEqual(gen.bezier(p,1), p[-1])
        for t in (.2,.5,.8):
            coeff = [(1-t)**3,3*(1-t)**2*t,3*(1-t)*t*t,t**3]
            expected = tuple(sum(c*q[axis] for c,q in zip(coeff,p)) for axis in (0,1))
            for a,b in zip(gen.bezier(p,t),expected):
                self.assertAlmostEqual(a,b)

    def test_voronoi_halfplanes_and_total_area(self):
        seeds = [(75+(i*197)%830,122+(i*83)%210) for i in range(23)]
        cells = gen.voronoi(seeds)
        area = 0
        for seed,cell in zip(seeds,cells):
            self.assertGreaterEqual(len(cell),3)
            area += abs(sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(cell,cell[1:]+cell[:1])))/2
            for x,y in cell:
                self.assertTrue(40-1e-7<=x<=920+1e-7 and 100-1e-7<=y<=360+1e-7)
                own = (x-seed[0])**2+(y-seed[1])**2
                for q in seeds:
                    self.assertLessEqual(own,(x-q[0])**2+(y-q[1])**2+1e-6)
        self.assertAlmostEqual(area,880*260,places=5)

    def test_tree_and_catalog(self):
        self.assertEqual(len(gen.tree_segments()),255)
        with (ART / 'catalog.csv').open() as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual({r['exhibit'] for r in rows},NAMES)
        for row in rows:
            self.assertEqual(int(row['bytes']), (ART / (row['exhibit']+'.svg')).stat().st_size)
        self.assertEqual(sum(r['animation']=='once' for r in rows),1)

    def test_svg_safety_and_readme_wiring(self):
        readme = (ROOT / 'README.md').read_text()
        self.assertEqual({p.stem for p in ART.glob('*.svg')}, NAMES)
        for file in ART.glob('*.svg'):
            tree = ET.parse(file).getroot()
            self.assertTrue(tree.find('s:title',NS).text)
            self.assertTrue(tree.find('s:desc',NS).text)
            for node in tree.iter():
                self.assertNotIn(node.tag.rsplit('}',1)[-1], {'script','image','foreignObject','animate','animateMotion'})
                for attr,value in node.attrib.items():
                    self.assertFalse(attr.startswith('on'))
                    self.assertNotIn('http',value)
            self.assertIn('@media(prefers-reduced-motion:reduce)',file.read_text())
            pattern = rf'<img src="assets/algorithmarium/{file.name}"[^>]+alt="[^"]{{30,}}"'
            self.assertRegex(readme,pattern)
        self.assertIn('](atlas/algorithmarium.md)', readme)
