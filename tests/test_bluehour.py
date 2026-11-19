"""Contracts for the original static botanical-inspired editorial plates."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'assets/bluehour';SRC=ROOT/'atlas/samples/bluehour'
spec=importlib.util.spec_from_file_location('bluehour',SRC/'generate.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
class BluehourTest(unittest.TestCase):
 def test_seven_safe_self_contained_svgs(self):
  self.assertEqual(len(list(ART.glob('*.svg'))),7)
  for p in ART.glob('*.svg'):
   root=ET.parse(p).getroot();self.assertEqual(root.attrib['role'],'img')
   self.assertIsNotNone(root.find('{*}title'));self.assertIsNotNone(root.find('{*}desc'))
   for e in root.iter():
    self.assertNotIn(e.tag.split('}')[-1],['script','image','foreignObject','animate','filter','a','style'])
    self.assertFalse(any(k.startswith('on') or k.endswith('href') for k in e.attrib))
    self.assertNotIn('url(',str(e.attrib))
 def test_mobile_recomposed_not_scaled(self):
  for name,dims in [('hero.svg','0 0 1440 1080'),('hero-mobile.svg','0 0 720 1220'),('contact.svg','0 0 1440 880'),('contact-mobile.svg','0 0 720 2140')]:
   self.assertEqual(ET.parse(ART/name).getroot().attrib['viewBox'],dims)
  self.assertIn('translate(338 310)',(ART/'hero-mobile.svg').read_text())
  self.assertNotEqual(g.hero(),g.hero(True))
 def test_same_geometry_across_layouts(self):
  for slug,fn in g.FORMS.items():
   self.assertIn(fn(),g.plate(slug));self.assertIn(fn(),g.contact());self.assertIn(fn(),g.contact(True))
  self.assertIn(g.fern(),g.hero());self.assertIn(g.fern(),g.hero(True))
 def test_geometry_is_deterministic_and_distinct(self):
  self.assertEqual(len({fn() for fn in g.FORMS.values()}),3)
  for fn in g.FORMS.values():
   self.assertEqual(fn(),fn());self.assertNotIn('nan',fn());self.assertNotIn('inf',fn())
  self.assertEqual(g.grain(720,1220),g.grain(720,1220))
 def test_manifest_and_size(self):
  m=json.loads((ART/'manifest.json').read_text());self.assertEqual(len(m),7)
  for name,digest in m.items():self.assertEqual(hashlib.sha256((ART/name).read_bytes()).hexdigest(),digest)
  self.assertLess(sum(p.stat().st_size for p in ART.iterdir()),1_500_000)
 def test_readme_links_and_scope(self):
  b=(SRC/'readme-block.md').read_text();self.assertEqual((ROOT/'README.md').read_text().count(b),1)
  self.assertEqual(b.count('<picture>'),2);self.assertEqual(b.count('<source '),2)
  self.assertIn('не фотография',b);self.assertIn('ботаническую точность',b)
  for _,_,slug in g.LABELS:self.assertIn(f'assets/bluehour/{slug}.svg',b)
 def test_pinned_readme_research(self):
  s=json.loads((SRC/'sources.json').read_text());self.assertEqual(len(s),8)
  for r in s:
   self.assertRegex(r['commit'],r'^[a-f0-9]{40}$');self.assertIn(r['commit'],r['url']);self.assertTrue(r['scope']);self.assertTrue(r['observation'])
 def test_regeneration_does_not_edit_readme(self):
  files=[*ART.iterdir(),SRC/'readme-block.md',ROOT/'README.md'];before={p:p.read_bytes() for p in files}
  subprocess.run([sys.executable,str(SRC/'generate.py')],check=True,cwd=ROOT)
  self.assertEqual(before,{p:p.read_bytes() for p in files})
