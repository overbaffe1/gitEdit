"""Local editorial map contract, not a geographic or shortest-path claim."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'assets/wayfinding'
SRC=ROOT/'atlas/samples/wayfinding'
spec=importlib.util.spec_from_file_location('wayfinding',SRC/'generate.py')
g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)

class WayfindingTest(unittest.TestCase):
 def test_nine_unique_local_destinations(self):
  stops=[s for r in g.ROUTES for s in r[3]]
  self.assertEqual(len(stops),9)
  self.assertEqual(len({s[2] for s in stops}),9)
  self.assertEqual([s[0] for s in stops],[f'{i:02}' for i in range(1,10)])
  for _,_,slug in stops:self.assertTrue((ROOT/f'atlas/{slug}.md').is_file())
 def test_svg_safety(self):
  for p in ART.glob('*.svg'):
   root=ET.fromstring(p.read_text())
   self.assertEqual(root.attrib['role'],'img')
   self.assertEqual(len(root.findall('{*}circle')),9)
   for el in root.iter():
    self.assertNotIn(el.tag.split('}')[-1],['script','image','foreignObject','animate','a'])
    self.assertFalse(any(k.startswith('on') or k.endswith('href') for k in el.attrib))
 def test_four_layouts_and_text(self):
  self.assertEqual(len(list(ART.glob('*.svg'))),4)
  for p in ART.glob('*.svg'):
   root=ET.parse(p).getroot()
   self.assertEqual(root.attrib['viewBox'],'0 0 720 1700' if 'mobile' in p.name else '0 0 1440 1020')
   texts=' '.join(e.text or '' for e in root.findall('{*}text'))
   for _,_,_,stops in g.ROUTES:
    for num,label,_ in stops:self.assertIn(label,texts);self.assertIn(num,texts)
 def test_labels_stay_inside_page(self):
  # Generous conservative character-width estimate; browser additionally verifies overflow.
  for p in ART.glob('*.svg'):
   root=ET.parse(p).getroot(); w=int(root.attrib['width']); h=int(root.attrib['height'])
   for e in root.findall('{*}text'):
    x,y,size=map(float,[e.attrib['x'],e.attrib['y'],e.attrib['font-size']])
    self.assertGreaterEqual(x,0);self.assertLess(y,h)
    self.assertLessEqual(x+len(e.text or '')*size*.8,w)
 def test_manifest(self):
  manifest=json.loads((ART/'manifest.json').read_text())
  self.assertEqual(len(manifest),5)
  for name,digest in manifest.items():self.assertEqual(hashlib.sha256((ART/name).read_bytes()).hexdigest(),digest)
 def test_readme_block_and_accessible_links(self):
  block=(SRC/'readme-block.md').read_text()
  self.assertEqual((ROOT/'README.md').read_text().count(block),1)
  self.assertEqual(block.count('<source '),3)
  for _,_,_,stops in g.ROUTES:
   for num,label,slug in stops:self.assertIn(f'[{num} {label}](atlas/{slug}.md)',block)
 def test_pinned_research(self):
  records=json.loads((SRC/'sources.json').read_text());self.assertEqual(len(records),8)
  for r in records:
   self.assertRegex(r['commit'],r'^[a-f0-9]{40}$');self.assertIn(r['commit'],r['url']);self.assertTrue(r['scope'])
 def test_reproducible_read_only_generation(self):
  files=[*ART.iterdir(),SRC/'readme-block.md',ROOT/'README.md']
  before={p:p.read_bytes() for p in files}
  subprocess.run([sys.executable,str(SRC/'generate.py')],check=True,cwd=ROOT)
  self.assertEqual(before,{p:p.read_bytes() for p in files})
