"""Static correctness + preservation; opt-in browser script checks real currentSrc."""
import hashlib
from html.parser import HTMLParser
import importlib.util
import json
import math
from pathlib import Path
import re
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];SRC=ROOT/'atlas/samples/resize_scan';ART=ROOT/'assets/resize-scan'
spec=importlib.util.spec_from_file_location('resize_scan',SRC/'generate.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
class Picture(HTMLParser):
 def __init__(self):super().__init__();self.sources=[];self.images=[];self.pictures=0
 def handle_starttag(self,t,a):
  if t=='picture':self.pictures+=1
  if t=='source':self.sources.append(dict(a))
  if t=='img':self.images.append(dict(a))
class ResizeScanTest(unittest.TestCase):
 def test_ordered_source_queries_cover_exactly_thirteen_frames(self):
  p=Picture();p.feed(g.picture());self.assertEqual(p.pictures,1);self.assertEqual(len(p.sources),12);self.assertEqual(len(p.images),1)
  self.assertEqual([x['media'] for x in p.sources],[f'(max-width: {599+80*i}px)' for i in range(12)])
  self.assertEqual([Path(x['srcset']).name for x in p.sources],[f'slice-{i:02}.svg' for i in range(12)]);self.assertTrue(p.images[0]['src'].endswith('slice-12.svg'))
 def test_all_integer_and_fractional_boundaries(self):
  self.assertEqual(g.selected(390),0);self.assertEqual(g.selected(1600),12)
  for i in range(12):
   b=599+80*i;self.assertEqual(g.selected(b),i);self.assertEqual(g.selected(b+.5),i+1);self.assertEqual(g.selected(b+1),i+1)
  self.assertEqual({g.selected(w) for w in range(320,1921)},set(range(13)))
 def test_frame_positions_on_analytic_channel(self):
  for i in range(13):
   f=g.frame(i);self.assertEqual(f['z'],i/12);self.assertAlmostEqual(f['cx'],.9*math.cos(math.tau*i/12));self.assertAlmostEqual(f['cy'],.9*math.sin(math.tau*i/12));self.assertLess(math.hypot(f['cx'],f['cy'])+.55,2.2)
  for i in [-1,13,'5',None]:
   with self.assertRaises(ValueError):g.frame(i)
 def test_svg_hole_and_outer_circle_match_geometry(self):
  for i in range(13):
   root=ET.parse(ART/f'slice-{i:02}.svg').getroot();circles=root.findall('.//{*}circle');self.assertEqual(len(circles),16)
   hole=next(c for c in circles if c.get('stroke')=='#ecdbbb');self.assertAlmostEqual(float(hole.get('cx')),270+76*.9*math.cos(math.tau*i/12),places=5);self.assertAlmostEqual(float(hole.get('cy')),245-76*.9*math.sin(math.tau*i/12),places=5);self.assertAlmostEqual(float(hole.get('r')),76*.55)
   self.assertIn(f'SLICE {i+1:02} / 13',''.join(root.itertext()));self.assertIsNotNone(root.find('{*}desc'));self.assertEqual(root.get('role'),'img')
 def test_media_are_static_no_external_resources_or_scripts(self):
  for p in ART.glob('*.svg'):
   for e in ET.parse(p).getroot().iter():
    self.assertNotIn(e.tag.split('}')[-1],['script','image','foreignObject','animate','animateMotion','set','style']);self.assertFalse(any(k.startswith('on') or k.endswith('href') for k in e.attrib))
  text=g.block();self.assertNotRegex(text,r'<(?:script|iframe|input|form|video|audio)\b');self.assertNotIn('https://',text);self.assertIn('13 заранее вычисленных',text);self.assertIn('не настоящий range',text)
 def test_contact_sheet_and_data_and_copy(self):
  sheet=ET.parse(ART/'all-slices.svg').getroot();self.assertEqual(sheet.get('viewBox'),'0 0 1260 1100');self.assertEqual(len(sheet.findall('{*}g')),13)
  data=json.loads((ART/'frames.json').read_text());self.assertEqual(data['count'],13);self.assertEqual(data['frames'],[g.frame(i) for i in range(13)])
  self.assertEqual((ART/'picture.txt').read_text(),g.picture());self.assertIn(g.picture(),(SRC/'readme-block.md').read_text())
 def test_sources_manifest_and_links(self):
  sources=json.loads((SRC/'sources.json').read_text());self.assertEqual(len(sources),5)
  for s in sources:self.assertRegex(s['commit'],r'^[a-f0-9]{40}$');self.assertIn(s['commit'],s['url'])
  m=json.loads((ART/'manifest.json').read_text());self.assertEqual(len(m),17)
  for name,digest in m.items():self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),digest)
  for href in re.findall(r'(?:src="|srcset="|\]\()([^"\s)]+)',g.block()):self.assertTrue((ROOT/href).is_file(),href)
 def test_entire_previous_readme_and_workflow_unchanged(self):
  ref=json.loads((SRC/'config.json').read_text())['base_commit']
  if subprocess.run(['git','cat-file','-e',ref],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode:self.skipTest('Fetch pinned base '+ref)
  now=(ROOT/'README.md').read_bytes();b=(SRC/'readme-block.md').read_bytes();self.assertEqual(now.count(b),1);self.assertEqual(now.replace(b,b'',1),subprocess.check_output(['git','show',ref+':README.md'],cwd=ROOT));self.assertEqual(subprocess.check_output(['git','diff',ref,'--','.github/workflows'],cwd=ROOT),b'')
 def test_regeneration_deterministic_and_root_readme_readonly(self):
  files=[*ART.iterdir(),SRC/'readme-block.md',ROOT/'README.md'];before={p:p.read_bytes() for p in files};subprocess.run([sys.executable,str(SRC/'generate.py')],check=True,cwd=ROOT);self.assertEqual(before,{p:p.read_bytes() for p in files})
 def test_browser_check_and_documented_limits(self):
  script=(SRC/'check-browser.cjs').read_text();self.assertIn("context:'overbaffe1/gitEdit'",script);self.assertIn('setViewportSize',script);self.assertIn('currentSrc',script);self.assertIn('img.decode()',script);self.assertIn('documents,1',script)
  doc=(ROOT/'atlas/resize-scan.md').read_text();self.assertIn('не авторизованная production',doc);self.assertIn('не именно наше управление viewport',doc);self.assertIn('104 проверки',doc)
