import hashlib,json,re,subprocess,sys,unittest,xml.etree.ElementTree as ET
from pathlib import Path
import pymupdf
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'assets/pressroom';S=ROOT/'atlas/samples/pressroom'
class PressroomTests(unittest.TestCase):
 def test_seven_self_contained_svg(self):
  files=list(A.glob('*.svg'));self.assertEqual(len(files),7)
  for p in files:
   root=ET.parse(p).getroot();ids={e.attrib['id'] for e in root.iter() if 'id' in e.attrib};self.assertEqual(root.attrib['role'],'img');self.assertNotRegex(p.read_text(),r'<(?:script|image|foreignObject|animate)\b')
   for e in root.iter():
    for k,v in e.attrib.items():
     if k.endswith('href'):self.assertTrue(v.startswith('#'));self.assertIn(v[1:],ids)
 def test_motion_and_static(self):
  for suffix in ['','-mobile']:
   motion=(A/f'motion{suffix}.svg').read_text();still=(A/f'still{suffix}.svg').read_text();self.assertIn('@media(prefers-reduced-motion:reduce)',motion);self.assertIn('@media print',motion);self.assertEqual(motion.count('animation:register-'),3);self.assertNotIn('<style>',still);self.assertEqual(re.sub(r'<style>.*?</style>','',motion,flags=re.S),still)
 def test_plate_files(self):
  for n in ['one','two','three']:
   root=ET.parse(A/f'plate-{n}.svg').getroot();plates=[e.attrib['data-plate'] for e in root.iter() if 'data-plate' in e.attrib];self.assertEqual(plates,[n]);self.assertNotIn('<style>',(A/f'plate-{n}.svg').read_text())
 def test_timing(self):
  t=json.loads((A/'timing.json').read_text());self.assertEqual(t['duration_seconds'],16);self.assertAlmostEqual((t['aligned_through_percent']-t['aligned_from_percent'])/100*16,t['aligned_hold_seconds']);self.assertGreater(t['aligned_hold_seconds'],8);self.assertEqual(len(t['initial_offsets']),3)
 def test_png_pdf(self):
  for name,size in [('still.png',(1440,900)),('still-mobile.png',(720,1000))]:
   with Image.open(A/name) as im:self.assertEqual(im.size,size)
  with pymupdf.open(A/'print-a4.pdf') as doc:self.assertEqual(len(doc),1);self.assertAlmostEqual(doc[0].rect.width,595.2756,places=2);self.assertAlmostEqual(doc[0].rect.height,841.8898,places=2)
 def test_manifest_and_research(self):
  data=json.loads((A/'manifest.json').read_text());self.assertEqual(len(data),10)
  for name,digest in data.items():self.assertEqual(hashlib.sha256((A/name).read_bytes()).hexdigest(),digest)
  rows=json.loads((S/'sources.json').read_text());self.assertEqual(len(rows),8)
  for r in rows:self.assertRegex(r['commit'],r'^[0-9a-f]{40}$');self.assertTrue(r['scope'])
 def test_readme_sources_and_order(self):
  text=(ROOT/'README.md').read_text();block=(S/'readme-block.md').read_text();self.assertIn(block,text);self.assertNotIn('<style>',block);self.assertIn('(max-width: 640px) and (prefers-reduced-motion: reduce)',block);self.assertLess(text.index('## Световой стол'),text.index('## Ночной тираж'));self.assertLess(text.index('## Ночной тираж'),text.index('## Один шаг — один изменённый бит'))
 def test_regeneration_readonly_readme(self):
  before={p.name:p.read_bytes() for p in A.iterdir()};readme=(ROOT/'README.md').read_bytes();subprocess.run([sys.executable,str(S/'generate.py')],capture_output=True,check=True);self.assertEqual(before,{p.name:p.read_bytes() for p in A.iterdir()});self.assertEqual(readme,(ROOT/'README.md').read_bytes())
