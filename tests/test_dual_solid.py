"""Independent STL silhouette/volume checks; no CAD dependency or remote viewer claim."""
from collections import Counter
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];SRC=ROOT/'atlas/samples/dual_solid';ART=ROOT/'assets/dual-solid';PLAY=ROOT/'atlas/dual-solid/README.md'
spec=importlib.util.spec_from_file_location('dual_solid',SRC/'generate.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def triangles():
 values=[tuple(map(int,x.split())) for x in re.findall(r'\bvertex ([^\n]+)',(ART/'ai-3d.stl').read_text())]
 return [tuple(values[i:i+3]) for i in range(0,len(values),3)]
def cross2(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def inside(p,t):
 if cross2(*t)==0:return False
 signs=[cross2(a,b,p) for a,b in zip(t,t[1:]+t[:1])]
 return all(x>=0 for x in signs) or all(x<=0 for x in signs)
class DualSolidTest(unittest.TestCase):
 def test_independent_silhouettes_from_actual_stl_triangles(self):
  ts=triangles()
  for axis,expected in [(0,['0100111','1010010','1110010','1010010','1010111']),(2,['1110110','0010101','1110101','0010101','1110110'])]:
   projected=[tuple((v[axis],v[1]) for v in t) for t in ts]
   actual=[''.join('1' if any(inside((2*x-6,4-2*y),t) for t in projected) else '0' for x in range(7)) for y in range(5)]
   self.assertEqual(actual,expected)
 def test_mask_intersection_and_coverage_condition(self):
  cells=g.voxels();self.assertEqual(len(cells),83)
  for rows in [g.mask('AI'),g.mask('3D')]:self.assertTrue(all('1' in r for r in rows))
  for x in range(7):
   for y in range(5):
    for z in range(7):self.assertEqual((x,y,z) in cells,g.mask('AI')[4-y][x]=='1' and g.mask('3D')[4-y][z]=='1')
 def test_triangle_winding_area_and_normals(self):
  normals=[tuple(map(int,v.split())) for v in re.findall('facet normal ([^\n]+)',(ART/'ai-3d.stl').read_text())];ts=triangles();self.assertEqual(len(normals),len(ts));self.assertEqual(len(ts),632)
  for n,(a,b,c) in zip(normals,ts):
   u=[b[i]-a[i] for i in range(3)];v=[c[i]-a[i] for i in range(3)];cross=(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
   self.assertEqual(sum(i*i for i in n),1);self.assertEqual(cross,tuple(4*i for i in n))
 def test_signed_volume_independent_of_voxel_generator(self):
  six=0
  for a,b,c in triangles():six+=a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])
  self.assertEqual(Fraction(six,6),664)
 def test_exposed_surface_and_honest_nonmanifold_stats(self):
  cells=g.voxels();neighbors=sum((x+dx,y+dy,z+dz) in cells for x,y,z in cells for (dx,dy,dz),_ in g.FACES)
  self.assertEqual(len(triangles()),2*(6*83-neighbors))
  edges=Counter(tuple(sorted((a,b))) for t in triangles() for a,b in zip(t,t[1:]+t[:1]));self.assertEqual(Counter(edges.values()),{2:932,4:8})
  stats=json.loads((ART/'geometry.json').read_text());self.assertEqual(stats,g.stats());self.assertEqual(len(stats['face_connected_components']),8);self.assertEqual(sum(stats['face_connected_components']),83)
 def test_full_stl_embedded_and_api_size_bounded(self):
  scene=PLAY.read_text();payload=re.findall(r'^```stl\n(.*?)^```',scene,re.M|re.S);self.assertEqual(payload,[(ART/'ai-3d.stl').read_text()]);self.assertLess((ART/'ai-3d.stl').stat().st_size,100_000);self.assertEqual(scene.count('```stl'),1)
  for href in re.findall(r'\]\(([^)]+)\)',scene):self.assertTrue((PLAY.parent/href).is_file(),href)
 def test_proof_svg_recovered_from_same_geometry_and_safe(self):
  svg=ET.parse(ART/'projections.svg').getroot();self.assertIsNotNone(svg.find('{*}desc'));self.assertEqual(len(svg.findall('{*}rect')),1+sum(r.count('1') for axis in ['xy','zy'] for r in g.projection(axis)))
  for el in svg.iter():self.assertNotIn(el.tag.split('}')[-1],['script','image','foreignObject','animate']);self.assertFalse(any(k.startswith('on') or k.endswith('href') for k in el.attrib))
 def test_manifest_sources_and_boundaries(self):
  m=json.loads((ART/'manifest.json').read_text());self.assertEqual(len(m),5)
  for file,digest in m.items():self.assertEqual(hashlib.sha256((ROOT/file).read_bytes()).hexdigest(),digest)
  sources=json.loads((SRC/'sources.json').read_text());self.assertEqual(len(sources),5)
  for s in sources:self.assertRegex(s['commit'],r'^[a-f0-9]{40}$');self.assertIn(s['commit'],s['url'])
  block=g.block();self.assertIn('не ещё один движок',block);self.assertIn('не готовая модель',block);self.assertNotIn('```stl',block)
  doc=(ROOT/'atlas/dual-solid.md').read_text();self.assertIn('не проверялись',doc);self.assertIn('не найдена',doc);self.assertIn('кратностью 4',doc)
 def test_entire_previous_readme_and_workflows_preserved(self):
  ref=json.loads((SRC/'config.json').read_text())['base_commit']
  if subprocess.run(['git','cat-file','-e',ref],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode:self.skipTest('Fetch pinned base '+ref)
  scan=(ROOT/'atlas/samples/resize_scan/readme-block.md').read_bytes();now=(ROOT/'README.md').read_bytes();self.assertEqual(now.count(scan),1)
  block=(SRC/'readme-block.md').read_bytes();self.assertEqual(now.count(block),1);self.assertEqual(now.replace(scan,b'',1).replace(block,b'',1),subprocess.check_output(['git','show',ref+':README.md'],cwd=ROOT));self.assertEqual(subprocess.check_output(['git','diff',ref,'--','.github/workflows'],cwd=ROOT),b'')
 def test_deterministic_regeneration_leaves_root_readme(self):
  files=[*ART.iterdir(),PLAY,SRC/'readme-block.md',ROOT/'README.md'];before={p:p.read_bytes() for p in files};subprocess.run([sys.executable,str(SRC/'generate.py')],check=True,cwd=ROOT);self.assertEqual(before,{p:p.read_bytes() for p in files})
