import hashlib,json,re,subprocess,sys,unittest
from html.parser import HTMLParser
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'assets/lighttable';S=ROOT/'atlas/samples/lighttable'
class Tags(HTMLParser):
 def __init__(self):super().__init__();self.tags=[]
 def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
class LighttableTests(unittest.TestCase):
 def test_six_real_sources(self):
  rows=json.loads((A/'catalog.json').read_text());self.assertEqual(len(rows),6);self.assertEqual(len({r['id'] for r in rows}),6)
  for i,r in enumerate(rows,1):self.assertEqual(i,r['number']);self.assertTrue((ROOT/r['target']).is_file());self.assertEqual(hashlib.sha256((ROOT/r['source']).read_bytes()).hexdigest(),r['source_sha256']);self.assertEqual(r['preview_size'],[1000,800]);self.assertEqual(len(r['crop']),4);self.assertTrue(0<=r['crop'][0]<r['crop'][2]<=1);self.assertTrue(0<=r['crop'][1]<r['crop'][3]<=1)
 def test_twelve_images(self):
  files=list(A.glob('*.png'));self.assertEqual(len(files),12);self.assertLess(sum(p.stat().st_size for p in files),3000000)
  for p in files:
   with Image.open(p) as im:self.assertEqual(im.size,(1000,800));self.assertEqual(im.mode,'P');self.assertEqual(getattr(im,'n_frames',1),1)
 def test_manifest(self):
  data=json.loads((A/'manifest.json').read_text());self.assertEqual(len(data),12)
  for name,digest in data.items():self.assertEqual(hashlib.sha256((A/name).read_bytes()).hexdigest(),digest)
 def test_native_table_and_captions(self):
  parser=Tags();text=(S/'readme-block.md').read_text();parser.feed(text);tags=parser.tags;self.assertEqual(sum(t=='table' for t,a in tags),1);self.assertEqual(sum(t=='td' for t,a in tags),6);self.assertEqual(sum(t=='tr' for t,a in tags),3);self.assertEqual(sum(t=='source' for t,a in tags),6);self.assertEqual(sum(t=='strong' for t,a in tags),6)
  for t,a in tags:
   self.assertNotIn(t,['script','iframe','style']);self.assertNotIn('style',a)
   if t=='img':self.assertTrue(a['alt']);self.assertTrue((ROOT/a['src']).is_file());self.assertEqual(a['width'],'100%')
   if t=='source':self.assertEqual(a['media'],'(prefers-color-scheme: dark)');self.assertTrue((ROOT/a['srcset']).is_file())
   if t=='a':self.assertTrue((ROOT/a['href']).is_file())
 def test_theme_pairs_differ(self):
  rows=json.loads((A/'catalog.json').read_text())
  for r in rows:self.assertNotEqual((A/(r['id']+'-light.png')).read_bytes(),(A/(r['id']+'-dark.png')).read_bytes())
  with Image.open(A/'contact-sheet.jpg') as im:self.assertEqual(im.size,(1600,2200))
 def test_readme_preserves_foyer_and_contains_block(self):
  text=(ROOT/'README.md').read_text();self.assertIn((S/'readme-block.md').read_text(),text);self.assertIn((ROOT/'atlas/samples/foyer/readme-block.md').read_text(),text);self.assertTrue(text.startswith('<p align="center"><a href="assets/night-shift/fold.gif">'));self.assertLess(text.index('## Бюро странных вещей'),text.index('## Световой стол'));self.assertLess(text.index('## Световой стол'),text.index('## Один шаг — один изменённый бит'))
 def test_research_scope(self):
  rows=json.loads((S/'sources.json').read_text());self.assertEqual(len(rows),8)
  for r in rows:self.assertRegex(r['commit'],r'^[0-9a-f]{40}$');self.assertIn(r['commit'],r['url']);self.assertTrue(r['scope'])
 def test_regeneration_readonly_sources_and_readme(self):
  source={r['source']:(ROOT/r['source']).read_bytes() for r in json.loads((A/'catalog.json').read_text())};readme=(ROOT/'README.md').read_bytes();before={p.name:p.read_bytes() for p in A.iterdir()};block=(S/'readme-block.md').read_bytes();subprocess.run([sys.executable,str(S/'generate.py')],check=True,capture_output=True);self.assertEqual(before,{p.name:p.read_bytes() for p in A.iterdir()});self.assertEqual(block,(S/'readme-block.md').read_bytes());self.assertEqual(readme,(ROOT/'README.md').read_bytes())
  for name,data in source.items():self.assertEqual(data,(ROOT/name).read_bytes())
