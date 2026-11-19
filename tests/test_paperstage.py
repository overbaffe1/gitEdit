"""Static paper-theatre geometry/publication contracts, not manufacturing tests."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];ART=ROOT/'assets/paperstage';SRC=ROOT/'atlas/samples/paperstage'
spec=importlib.util.spec_from_file_location('paperstage',SRC/'generate.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
class PaperstageTest(unittest.TestCase):
 def test_four_safe_svgs(self):
  self.assertEqual(len(list(ART.glob('*.svg'))),4)
  for p in ART.glob('*.svg'):
   root=ET.parse(p).getroot();self.assertEqual(root.attrib['role'],'img')
   self.assertIsNotNone(root.find('{*}title'));self.assertIsNotNone(root.find('{*}desc'))
   for e in root.iter():
    self.assertNotIn(e.tag.split('}')[-1],['script','image','foreignObject','animate','filter','a','style'])
    self.assertFalse(any(k.startswith('on') or k.endswith('href') for k in e.attrib))
    self.assertNotIn('url(',str(e.attrib))
 def test_painter_order(self):
  self.assertEqual(re.findall(r'data-layer="(\d)"',g.scene()),['5','4','3','2','1'])
  self.assertLess(g.scene().index(g.back()),g.scene().index('data-layer="5"'))
  self.assertEqual(re.findall(r'data-layer="(\d)"',g.exploded()),list('123456'))
 def test_shared_contours_and_colors(self):
  for mobile in [False,True]:
   self.assertIn(g.scene(),g.hero(mobile))
   for i,c in enumerate(g.COLORS):
    self.assertIn(g.frame(i),g.hero(mobile));self.assertIn(g.frame(i,False),g.exploded(mobile))
   self.assertIn(g.back(),g.exploded(mobile))
  self.assertEqual(g.FRAME,g.OUTER+g.HOLE)
  self.assertIn('fill-rule="evenodd"',g.frame(0))
 def test_layouts_and_numbered_parts(self):
  for name,box in [('hero.svg','0 0 1440 1120'),('hero-mobile.svg','0 0 720 1040'),('layers.svg','0 0 1440 800'),('layers-mobile.svg','0 0 720 1680')]:
   self.assertEqual(ET.parse(ART/name).getroot().attrib['viewBox'],box)
  for mobile in [False,True]:
   s=g.exploded(mobile)
   for i in range(1,7):self.assertIn(f'{i:02} / ',s)
 def test_scene_metadata(self):
  d=json.loads((ART/'scene.json').read_text());self.assertEqual(len(d['frames']),5)
  self.assertEqual([f['color'] for f in d['frames']],g.COLORS)
  self.assertEqual([f['dx'] for f in d['frames']],[i*32 for i in range(5)])
  self.assertEqual(d['outer_path'],g.OUTER);self.assertEqual(d['hole_path'],g.HOLE);self.assertEqual(d['back']['id'],6)
 def test_manifest_and_readme(self):
  m=json.loads((ART/'manifest.json').read_text());self.assertEqual(len(m),5)
  for name,digest in m.items():self.assertEqual(hashlib.sha256((ART/name).read_bytes()).hexdigest(),digest)
  b=(SRC/'readme-block.md').read_text();self.assertEqual((ROOT/'README.md').read_text().count(b),1)
  self.assertEqual(b.count('<picture>'),2);self.assertEqual(b.count('<source '),2)
  self.assertIn('не выкройка',b);self.assertTrue((ROOT/'atlas/paperstage.md').is_file())
 def test_pinned_research(self):
  sources=json.loads((SRC/'sources.json').read_text());self.assertEqual(len(sources),8)
  for s in sources:
   self.assertRegex(s['commit'],r'^[a-f0-9]{40}$');self.assertIn(s['commit'],s['url']);self.assertTrue(s['scope'])
 def test_regeneration_does_not_edit_readme(self):
  files=[*ART.iterdir(),SRC/'readme-block.md',ROOT/'README.md'];before={p:p.read_bytes() for p in files}
  subprocess.run([sys.executable,str(SRC/'generate.py')],check=True,cwd=ROOT)
  self.assertEqual(before,{p:p.read_bytes() for p in files})
