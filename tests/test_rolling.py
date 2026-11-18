"""Validate rolling geometry, no-slip angular ratios and true still fallbacks."""
import importlib.util
import math
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT/'atlas/samples/rolling/generate.py'
ART = ROOT/'assets/rolling'
spec = importlib.util.spec_from_file_location('rolling',GEN)
gen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)
NS = {'s':'http://www.w3.org/2000/svg'}


class RollingTest(unittest.TestCase):
    def test_contact_and_marker_on_wheel(self):
        for _,R,r,kind,_ in gen.SPECS.values():
            for t in (0,.2,.7,1.5,3.2,6.1):
                cx,cy,angle,x,y=gen.geometry(kind,R,r,t)
                self.assertAlmostEqual(math.hypot(x-cx,y-cy),r)
                if kind=='inside':
                    self.assertAlmostEqual(math.hypot(cx,cy)+r,R)
                elif kind=='outside':
                    self.assertAlmostEqual(math.hypot(cx,cy)-r,R)
                else:
                    self.assertAlmostEqual(cy,-r)

    def test_no_slip_at_instantaneous_contact(self):
        # Contact point is not generally the highlighted marker. Compute its
        # velocity as center velocity + angular velocity crossed with radius.
        for _,R,r,kind,_ in gen.SPECS.values():
            for t in (.2,.9,2.1,4.5):
                cx,cy,omega,_,_=gen.geometry(kind,R,r,t)
                if kind=='inside':
                    distance=R-r
                    vx,vy=-distance*math.sin(t),distance*math.cos(t)
                    qx,qy=r*math.cos(t),r*math.sin(t)
                    omega=-(R-r)/r
                elif kind=='outside':
                    distance=R+r
                    vx,vy=-distance*math.sin(t),distance*math.cos(t)
                    qx,qy=-r*math.cos(t),-r*math.sin(t)
                    omega=(R+r)/r
                else:
                    vx,vy=r,0
                    qx,qy=0,r
                    omega=1
                self.assertAlmostEqual(vx-omega*qy,0)
                self.assertAlmostEqual(vy+omega*qx,0)

    def test_tusi_and_astroid_identities(self):
        for i in range(101):
            t=i*math.tau/100
            *_,x,y=gen.geometry('inside',150,75,t)
            self.assertAlmostEqual(x,150*math.cos(t))
            self.assertAlmostEqual(y,0)
            *_,x,y=gen.geometry('inside',150,37.5,t)
            self.assertAlmostEqual(x,150*math.cos(t)**3)
            self.assertAlmostEqual(y,150*math.sin(t)**3)

    def test_closed_curves_and_cycloid_reset(self):
        for _,R,r,kind,_ in gen.SPECS.values():
            a=gen.geometry(kind,R,r,0)
            b=gen.geometry(kind,R,r,math.tau)
            if kind=='line':
                self.assertAlmostEqual(b[3]-a[3],math.tau*r)
                self.assertAlmostEqual(a[4],b[4])
            else:
                self.assertAlmostEqual(a[3],b[3])
                self.assertAlmostEqual(a[4],b[4])
                self.assertAlmostEqual(math.cos(a[2]),math.cos(b[2]))
                self.assertAlmostEqual(math.sin(a[2]),math.sin(b[2]))

    def test_css_angular_ratios_match_geometry(self):
        for name,(_,R,r,kind,_) in gen.SPECS.items():
            svg=(ART/f'{name}.svg').read_text()
            match=re.search(r'@keyframes spin\{from\{transform:rotate\(([-\d.]+)deg\)\}to\{transform:rotate\(([-\d.]+)deg\)',svg)
            self.assertIsNotNone(match)
            start,end=map(float,match.groups())
            expected=360 if kind=='line' else 360*R/r*(-1 if kind=='inside' else 1)
            self.assertAlmostEqual(end-start,expected,places=6)
            self.assertIn('14s linear infinite',svg)
            self.assertNotIn('animation-delay',svg)
            self.assertEqual(len(re.findall(r' L',svg)),720)

    def test_true_stills_picture_wiring_and_safety(self):
        readme=(ROOT/'README.md').read_text()
        expected={f'{name}{suffix}.svg' for name in gen.SPECS for suffix in ('','-still')}
        self.assertEqual({p.name for p in ART.iterdir()},expected)
        for name in gen.SPECS:
            still=(ART/f'{name}-still.svg').read_text()
            self.assertNotIn('@keyframes',still)
            self.assertNotIn('animation:',still)
            motion=(ART/f'{name}.svg').read_text()
            self.assertIn('@media(prefers-reduced-motion:reduce)',motion)
            pattern=rf'<source media="\(prefers-reduced-motion: reduce\)" srcset="assets/rolling/{name}-still.svg"><img src="assets/rolling/{name}.svg"[^>]+alt="[^"]{{30,}}"'
            self.assertRegex(readme,pattern)
            for source in (still,motion):
                svg=ET.fromstring(source)
                self.assertTrue(svg.find('s:title',NS).text)
                self.assertTrue(svg.find('s:desc',NS).text)
                for node in svg.iter():
                    self.assertNotIn(node.tag.rsplit('}',1)[-1],{'script','image','foreignObject','animate','animateMotion'})
                    for attr,value in node.attrib.items():
                        self.assertFalse(attr.startswith('on'))
                        self.assertNotIn('http',value)

    def test_clean_reprint(self):
        before=(ROOT/'README.md').read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run([sys.executable,str(GEN),'--output',tmp],cwd=tmp,check=True)
            self.assertEqual({p.name for p in Path(tmp).iterdir()},{p.name for p in ART.iterdir()})
            for file in ART.iterdir():
                self.assertEqual(file.read_bytes(),(Path(tmp)/file.name).read_bytes(),file.name)
        self.assertEqual(before,(ROOT/'README.md').read_bytes())
