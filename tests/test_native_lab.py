"""Actual native inputs, history-backed image diff and README preservation."""
import collections
import csv
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path
import re
import subprocess
import sys
import unittest
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];ART=ROOT/'assets/native-lab';SRC=ROOT/'atlas/samples/native_lab'
spec=importlib.util.spec_from_file_location('native_lab',SRC/'generate.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
class NativeLabTest(unittest.TestCase):
 def test_mesh_topology_and_components(self):
  vs,fs=g.mesh();self.assertEqual(len(vs),78);self.assertEqual(len(fs),152)
  edges=collections.Counter(tuple(sorted((a,b))) for f in fs for a,b in zip(f,f[1:]+f[:1]))
  self.assertEqual(len(edges),228);self.assertEqual(set(edges.values()),{2})
  adj={i:set() for i in range(len(vs))}
  for a,b in edges:adj[a].add(b);adj[b].add(a)
  remaining=set(adj);components=[]
  while remaining:
   seen={min(remaining)};todo=list(seen)
   while todo:
    for n in adj[todo.pop()]-seen:seen.add(n);todo.append(n)
   remaining-=seen;components.append(len(seen))
  self.assertEqual(sorted(components),[6,72])
 def test_stl_normals_and_shared_vertices(self):
  s=(ART/'orbit.stl').read_text();self.assertEqual(s,g.stl())
  vs,fs=g.mesh()
  for f in fs:
   n=g.normal(*(vs[i] for i in f));self.assertAlmostEqual(sum(x*x for x in n),1)
   center=[sum(vs[v][i] for v in f)/3 for i in range(3)]
   if max(f)<72:
    u=math.atan2(center[1],center[0]);reference=[center[0]-2*math.cos(u),center[1]-2*math.sin(u),center[2]]
   else:reference=center
   self.assertGreater(sum(a*b for a,b in zip(n,reference)),0)
  parsed=[tuple(map(float,m.split())) for m in re.findall(r'\bvertex ([^\n]+)',s)]
  self.assertEqual(len(parsed),152*3);self.assertEqual(len(set(parsed)),78)
 def test_live_fences_match_distributed_files(self):
  b=(SRC/'readme-block.md').read_text()
  chunks=re.findall(r'^```(\w+)\n(.*?)\n```',b,re.M|re.S)
  self.assertEqual(collections.Counter(lang for lang,_ in chunks),{'stl':1,'geojson':1,'topojson':1,'mermaid':5,'math':1})
  for lang,filename in [('stl','orbit.stl'),('geojson','survey.geojson'),('topojson','sheets.topojson')]:self.assertEqual(next(s for l,s in chunks if l==lang)+'\n',(ART/filename).read_text())
  self.assertEqual([s+'\n' for l,s in chunks if l=='mermaid'],list(g.SCHEMES.values()))
  for name,s in g.SCHEMES.items():self.assertEqual((ART/(name+'.mmd')).read_text(),s)
 def test_maps_and_cluster_data(self):
  for name in ['survey.geojson','sheets.topojson']:self.assertEqual((ART/name).read_bytes(),(ROOT/'assets'/name).read_bytes())
  data=json.loads((ART/'clusters.geojson').read_text());self.assertEqual(data['type'],'FeatureCollection');self.assertEqual(len(data['features']),800)
  coords=[]
  for f in data['features']:
   self.assertEqual(f['geometry']['type'],'Point');lon,lat=f['geometry']['coordinates'];self.assertTrue(-180<=lon<=180 and -90<=lat<=90);coords.append((lon,lat))
  self.assertEqual(len(set(coords)),800)
 def test_catalog_notebook_and_formats(self):
  with (ART/'catalog.csv').open() as f:a=list(csv.reader(f))
  with (ART/'catalog.tsv').open() as f:b=list(csv.reader(f,delimiter='\t'))
  self.assertEqual(a,b);self.assertEqual(len(a),7);self.assertTrue(all(len(r)==5 for r in a))
  for r in a[1:]:self.assertTrue((ART/r[-1]).is_file())
  nb=json.loads((ART/'mesh.ipynb').read_text());self.assertEqual(nb['nbformat'],4)
  cell=nb['cells'][1];self.assertEqual(cell['outputs'][0]['text'],['2\n']);self.assertIn('78, 228, 152',''.join(cell['source']))
  for ext in ['rst','adoc','org']:self.assertGreater((ART/('notes.'+ext)).stat().st_size,80)
 def test_real_history_backed_image_diff(self):
  cfg=json.loads((SRC/'config.json').read_text());sha=cfg['image_diff_commit'];self.assertRegex(sha,r'^[a-f0-9]{40}$')
  def image(ref):return Image.open(io.BytesIO(subprocess.check_output(['git','show',ref+':assets/native-lab/revision.png'],cwd=ROOT))).convert('RGB')
  old,new=image(sha+'^'),image(sha)
  self.assertEqual(old.size,new.size);self.assertNotEqual(old.tobytes(),new.tobytes());self.assertEqual(new.tobytes(),Image.open(ART/'revision.png').convert('RGB').tobytes())
  self.assertIn('/commit/'+sha,(SRC/'readme-block.md').read_text())
 def test_entire_original_readme_preserved(self):
  cfg=json.loads((SRC/'config.json').read_text());old=subprocess.check_output(['git','show',cfg['base_commit']+':README.md'],cwd=ROOT)
  b=(SRC/'readme-block.md').read_bytes();now=(ROOT/'README.md').read_bytes();self.assertEqual(now.count(b),1);self.assertEqual(now.replace(b,b'',1),old)
  self.assertLess(now.index(b),now.index('## Бюро странных вещей'.encode()))
 def test_manifest_and_primary_sources(self):
  m=json.loads((ART/'manifest.json').read_text());self.assertEqual(set(m),{p.name for p in ART.iterdir() if p.name!='manifest.json'})
  for name,digest in m.items():self.assertEqual(hashlib.sha256((ART/name).read_bytes()).hexdigest(),digest)
  sources=json.loads((SRC/'sources.json').read_text());self.assertEqual(len(sources),8)
  for s in sources:self.assertRegex(s['commit'],r'^[a-f0-9]{40}$');self.assertIn(s['commit'],s['url'])
 def test_documented_boundaries_not_fake_embeds(self):
  b=(SRC/'readme-block.md').read_text();doc=(ROOT/'atlas/native-lab.md').read_text()
  self.assertNotRegex(b,r'<(?:script|iframe|video|canvas|input)\b')
  self.assertIn('<details open>',b);self.assertIn('[^native-lab-note]',b)
  self.assertIn('видео-вложение не загружено',doc);self.assertIn('не виджет внутри README',b)
  for kind in ['NOTE','TIP','IMPORTANT','WARNING','CAUTION']:self.assertIn('[!'+kind+']',doc)
 def test_regeneration_read_only_readme(self):
  files=[*ART.iterdir(),SRC/'readme-block.md',ROOT/'README.md'];before={p:p.read_bytes() for p in files}
  subprocess.run([sys.executable,str(SRC/'generate.py')],check=True,cwd=ROOT)
  self.assertEqual(before,{p:p.read_bytes() for p in files})
