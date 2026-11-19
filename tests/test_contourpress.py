"""Synthetic contour geometry and static publication contracts; no GIS claims."""
import csv
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];ART=ROOT/'assets/contourpress';SRC=ROOT/'atlas/samples/contourpress'
spec=importlib.util.spec_from_file_location('contourpress',SRC/'generate.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
class ContourpressTest(unittest.TestCase):
 def test_grid_and_triangles(self):
  pts=g.grid();self.assertEqual(len(pts),141*113)
  tris=list(g.triangles());self.assertEqual(len(tris),31360)
  for x,y,z in pts:self.assertTrue(math.isfinite(z));self.assertAlmostEqual(z,g.field(x,y))
  for tri in tris:
   self.assertEqual(len(set(tri)),3)
   self.assertTrue(all(0<=i<len(pts) for i in tri))
 def test_closed_contours_and_approximation(self):
  self.assertEqual(len(g.LEVELS),18)
  for level in g.LEVELS:
   chains=g.contours(level);self.assertGreater(len(chains),0)
   for chain in chains:
    self.assertEqual(chain[0],chain[-1]);self.assertGreater(len(chain),3)
    self.assertEqual(len(set(chain[:-1])),len(chain)-1)
    for x,y in chain:
     self.assertTrue(-3.5<x<3.5 and -2.8<y<2.8)
     self.assertLess(abs(g.field(x,y)-level),.003)
 def test_edge_interpolation(self):
  # Every tested crossing is exactly at level in the linear edge model.
  for a,b,c in list(g.triangles())[::29]:
   p,q=g.grid()[a],g.grid()[b]
   if abs(p[2]-q[2])<1e-10:continue
   level=p[2]*.37+q[2]*.63
   x,y=g.crossing(a,b,level)
   self.assertAlmostEqual(x,p[0]*.37+q[0]*.63)
   self.assertAlmostEqual(y,p[1]*.37+q[1]*.63)
 def test_profile_is_same_grid_row(self):
  with (ART/'profile.csv').open() as f:rows=list(csv.DictReader(f))
  self.assertEqual(len(rows),141);self.assertEqual(len(g.section_points()),141)
  for r,(x,z) in zip(rows,g.section_points()):
   self.assertEqual(float(r['y']),0);self.assertAlmostEqual(float(r['x']),x,places=8);self.assertAlmostEqual(float(r['z']),z,places=11)
 def test_shared_geometry_and_audit(self):
  self.assertIn(g.map_art(340,304,1040),g.hero())
  self.assertIn(g.map_art(24,300,672),g.hero(True))
  d=json.loads((ART/'audit.json').read_text());self.assertEqual(d['grid'],[141,113]);self.assertEqual(d['triangles'],31360)
  for r,level in zip(d['levels'],g.LEVELS):
   self.assertEqual(r['closed_chains'],len(g.contours(level)));self.assertEqual(r['vertices'],sum(len(c)-1 for c in g.contours(level)))
 def test_safe_svg_dimensions(self):
  boxes={'hero.svg':'0 0 1440 1180','hero-mobile.svg':'0 0 720 1100','profile.svg':'0 0 1440 520','profile-mobile.svg':'0 0 720 620','contours.svg':'0 0 1400 1120'}
  self.assertEqual({p.name for p in ART.glob('*.svg')},set(boxes))
  for name,box in boxes.items():
   root=ET.parse(ART/name).getroot();self.assertEqual(root.attrib['viewBox'],box);self.assertEqual(root.attrib['role'],'img')
   self.assertIsNotNone(root.find('{*}title'));self.assertIsNotNone(root.find('{*}desc'))
   for e in root.iter():
    self.assertNotIn(e.tag.split('}')[-1],['script','image','foreignObject','animate','filter','a','style'])
    self.assertFalse(any(k.startswith('on') or k.endswith('href') for k in e.attrib))
    self.assertNotIn('url(',str(e.attrib))
 def test_manifest_research_and_readme(self):
  m=json.loads((ART/'manifest.json').read_text());self.assertEqual(len(m),7)
  for name,digest in m.items():self.assertEqual(hashlib.sha256((ART/name).read_bytes()).hexdigest(),digest)
  records=json.loads((SRC/'sources.json').read_text());self.assertEqual(len(records),6)
  for r in records:self.assertRegex(r['commit'],r'^[a-f0-9]{40}$');self.assertIn(r['commit'],r['url']);self.assertTrue(r['scope'])
  b=(SRC/'readme-block.md').read_text();self.assertEqual((ROOT/'README.md').read_text().count(b),1);self.assertIn('не реальные геоданные',b)
  self.assertEqual(b.count('<source '),2)
 def test_regeneration_read_only_readme(self):
  files=[*ART.iterdir(),SRC/'readme-block.md',ROOT/'README.md'];before={p:p.read_bytes() for p in files}
  subprocess.run([sys.executable,str(SRC/'generate.py')],check=True,cwd=ROOT)
  self.assertEqual(before,{p:p.read_bytes() for p in files})
