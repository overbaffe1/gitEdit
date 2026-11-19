import hashlib,json,re,subprocess,sys,unittest,xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote,urlsplit
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'assets/foyer';S=ROOT/'atlas/samples/foyer'
class Tags(HTMLParser):
 def __init__(self):super().__init__();self.tags=[]
 def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
class FoyerTests(unittest.TestCase):
 def test_sixteen_self_contained_svgs(self):
  files=list(A.glob('*.svg'));self.assertEqual(len(files),16)
  for p in files:
   root=ET.parse(p).getroot();self.assertEqual(root.attrib['role'],'img');self.assertIsNotNone(root.find('{http://www.w3.org/2000/svg}title'))
   self.assertNotRegex(p.read_text(),r'<(?:script|image|foreignObject|animate|style)\b');self.assertNotIn('@font-face',p.read_text());ids={e.attrib['id'] for e in root.iter() if 'id' in e.attrib}
   for e in root.iter():
    for key,value in e.attrib.items():
     if key.endswith('href'):self.assertTrue(value.startswith('#'));self.assertIn(value[1:],ids)
   self.assertGreater(len(list(root.iter('{http://www.w3.org/2000/svg}use'))),20)
 def test_mobile_composition_not_crop(self):
  for theme in ['light','dark']:
   self.assertEqual(ET.parse(A/f'cover-{theme}.svg').getroot().attrib['viewBox'],'0 0 1440 760');self.assertEqual(ET.parse(A/f'cover-{theme}-mobile.svg').getroot().attrib['viewBox'],'0 0 720 920')
   for name in ['look','make','prove']:self.assertEqual(ET.parse(A/f'{name}-{theme}-mobile.svg').getroot().attrib['viewBox'],'0 0 720 354')
 def test_manifest(self):
  data=json.loads((A/'manifest.json').read_text());self.assertEqual(len(data),16)
  for name,digest in data.items():self.assertEqual(hashlib.sha256((A/name).read_bytes()).hexdigest(),digest)
 def test_picture_sources(self):
  parser=Tags();parser.feed((S/'readme-block.md').read_text());sources=[a for t,a in parser.tags if t=='source'];images=[a for t,a in parser.tags if t=='img'];self.assertEqual(len(sources),12);self.assertEqual(len(images),4)
  for i in range(0,12,3):self.assertIn('(max-width: 640px) and (prefers-color-scheme: dark)',sources[i]['media']);self.assertEqual(sources[i+1]['media'],'(max-width: 640px)');self.assertEqual(sources[i+2]['media'],'(prefers-color-scheme: dark)')
  for image in images:self.assertTrue(image['alt']);self.assertTrue((ROOT/image['src']).is_file())
 def test_routes_and_links(self):
  routes=json.loads((A/'routes.json').read_text());self.assertEqual([r['id'] for r in routes],['look','make','prove'])
  for route in routes:self.assertTrue((ROOT/route['target']).is_file())
  for p in [ROOT/'atlas/foyer.md',*(ROOT/'atlas').glob('foyer-*.md'),S/'readme-block.md']:
   for href in re.findall(r'(?:href="|src="|srcset="|\]\()([^"\s)]+)',p.read_text()):
    u=urlsplit(href)
    if not u.scheme and not u.netloc:
     base=ROOT if p.name=='readme-block.md' else p.parent;self.assertFalse(u.fragment);self.assertTrue((base/unquote(u.path)).is_file(),(p,href))
 def test_readme_has_full_block(self):
  text=(ROOT/'README.md').read_text();self.assertIn((S/'readme-block.md').read_text(),text);self.assertTrue(text.startswith('<p align="center"><a href="assets/night-shift/fold.gif">'));self.assertIn('## Один шаг — один изменённый бит',text)
 def test_research_scope(self):
  rows=json.loads((S/'sources.json').read_text());self.assertEqual(len(rows),13)
  for r in rows:self.assertRegex(r['commit'],r'^[0-9a-f]{40}$');self.assertIn(r['commit'],r['url']);self.assertTrue(r['scope'])
 def test_regeneration_never_edits_readme(self):
  old=(ROOT/'README.md').read_bytes();before={p.name:p.read_bytes() for p in A.iterdir()};block=(S/'readme-block.md').read_bytes();subprocess.run([sys.executable,str(S/'generate.py')],check=True,capture_output=True);self.assertEqual(old,(ROOT/'README.md').read_bytes());self.assertEqual(block,(S/'readme-block.md').read_bytes());self.assertEqual(before,{p.name:p.read_bytes() for p in A.iterdir()})
