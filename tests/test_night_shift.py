"""Offline checks for the exhibition's physical patterns, no third-party packages."""
import csv
import math
import sys
import unittest
import xml.etree.ElementTree as ET
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'atlas/samples/night_shift'))
import crystal
import projector
import tape

ART = ROOT/'assets/night-shift'
SVG = '{http://www.w3.org/2000/svg}'


def overlap(a, b, tolerance=.02):
    # Separating-axis test for the printed convex triangles and trapezoids (mm).
    for poly in (a,b):
        for u,v in zip(poly, poly[1:]+poly[:1]):
            dx,dy = crystal.unit(crystal.sub(v,u))
            aa,bb = ([x*dy-y*dx for x,y in part] for part in (a,b))
            if min(max(aa),max(bb))-max(min(aa),min(bb)) <= tolerance:
                return False
    return True


class NightShiftTest(unittest.TestCase):
    def test_hinges(self):
        net = crystal.Net()
        self.assertEqual(len(net.hinges),7)
        self.assertEqual(net.pose(0),net.faces)
        for t in (.25,.5,.75,1):
            pose = net.pose(t)
            for i, parent in enumerate(crystal.PARENT):
                for j,k in ((0,1),(1,2),(2,0)):
                    self.assertAlmostEqual(math.dist(net.faces[i][j],net.faces[i][k]), math.dist(pose[i][j],pose[i][k]))
                if parent is not None:
                    for v in set(net.faces[i]) & set(net.faces[parent]):
                        self.assertLess(math.dist(pose[i][net.faces[i].index(v)],pose[parent][net.faces[parent].index(v)]), 1e-8)
        depths = [p[2] for tri in net.project(1) for p in tri]
        self.assertLess(max(depths)-min(depths),1e-8)

    def test_printable_net(self):
        src = (ART/'crystal-net.svg').read_text(encoding='utf-8')
        self.assertEqual(crystal.cutting_sheet(crystal.Net()),src)
        page = ET.fromstring(src)
        self.assertEqual((page.get('width'), page.get('height')), ('297mm','210mm'))
        polys = [[tuple(map(float,p.split(','))) for p in el.get('points').split()] for el in page.iter(SVG+'polygon')]
        self.assertEqual([len(p) for p in polys], [3]*8+[4]*5)
        for a,b in combinations(polys,2): self.assertFalse(overlap(a,b))
        for poly in polys:
            self.assertTrue(all(5<x<292 and 25<y<187 for x,y in poly))
        labels = [el.text for el in page.iter(SVG+'text')]
        for letter in 'ABCDE': self.assertEqual(labels.count(letter),2)

    def test_tape_reads_back_to_csv(self):
        with (ROOT/'atlas/samples/snake-weeks.csv').open() as f:
            daily = [int(d['commits']) for d in csv.DictReader(f)]
        expected = [sum(daily[i:i+7]) for i in range(0,len(daily),7)]
        self.assertEqual((sum(expected),expected[6],expected[14]),(398,44,45))
        for compact in (False,True):
            name = 'weeks-tape-compact' if compact else 'weeks-tape'
            raw = (ART/(name+'.svg')).read_text(encoding='utf-8')
            self.assertEqual(tape.strip(tape.weeks(),compact),raw)
            holes = list(ET.fromstring(raw).iter(SVG+'circle'))
            for i,n in enumerate(expected,1):
                channels=[int(e.get('data-track')) for e in holes if e.get('data-week')==str(i)]
                self.assertEqual(len(channels),len(set(channels)))
                self.assertEqual(channels.count(0),1)  # transport channel, no data
                self.assertEqual(sum(channels),n)

    def test_optical_pair(self):
        paper = ET.parse(ART/'moth-paper.svg').getroot()
        bars = ET.parse(ART/'moth-grille.svg').getroot()
        for e in (paper,bars):
            self.assertEqual((e.get('width'),e.get('height'),e.get('viewBox')), ('120mm','72mm','0 0 240 144'))
        patterns = list(paper.iter(SVG+'pattern'))
        grille = next(bars.iter(SVG+'pattern')); opaque=grille.find(SVG+'rect')
        period=int(grille.get('width')); slit=int(opaque.get('x'))
        self.assertEqual(slit+int(opaque.get('width')),period)
        self.assertEqual(slit*120/240,1)  # one millimetre per advance
        self.assertEqual(len(patterns),4)
        for phase,p in enumerate(patterns):
            rect = p.find(SVG+'rect')
            self.assertEqual((int(p.get('width')),int(rect.get('x')),int(rect.get('width'))), (period,slit*phase,slit))
            for x in range(240):
                clear = (x-phase*slit)%period < slit
                self.assertEqual(clear,x%period//slit==phase)
        for compact in (False,True):
            suffix='-compact' if compact else ''
            for name,animated in [('moth-projector', True),('moth-still',False)]:
                svg=(ART/(name+suffix+'.svg')).read_text(encoding='utf-8')
                self.assertEqual(svg,projector.player(animated,compact))
                self.assertEqual('@keyframes' in svg,animated)


if __name__=='__main__': unittest.main()
