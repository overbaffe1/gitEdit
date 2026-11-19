import hashlib,importlib.util,json,struct,subprocess,sys,unittest
from collections import Counter
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'assets/materials';S=ROOT/'atlas/samples/materials'
spec=importlib.util.spec_from_file_location('materials_render',S/'render.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
class MaterialsTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.v,cls.n,cls.f=r.mesh()
 def test_closed_oriented_mesh(self):
  v,n,f=self.v,self.n,self.f;self.assertEqual(v.shape,(4480,3));self.assertEqual(f.shape,(8960,3));self.assertTrue(np.isfinite(v).all());self.assertTrue(np.allclose(np.linalg.norm(n,axis=1),1));self.assertTrue((f>=0).all() and (f<len(v)).all());edges=Counter(tuple(sorted((int(row[k]),int(row[(k+1)%3])))) for row in f for k in range(3));self.assertEqual(set(edges.values()),{2});self.assertEqual(len(v)-len(edges)+len(f),0);directed=Counter((int(row[k]),int(row[(k+1)%3])) for row in f for k in range(3));self.assertTrue(all(directed[(b,a)]==count for (a,b),count in directed.items()));tri=v[f];self.assertGreater(np.einsum('ij,ij->i',tri[:,0],np.cross(tri[:,1],tri[:,2])).sum(),0)
 def test_connected(self):
  adjacency=[set() for _ in self.v]
  for a,b,c in self.f:adjacency[a].update([b,c]);adjacency[b].update([a,c]);adjacency[c].update([a,b])
  reached={0};stack=[0]
  while stack:
   for j in adjacency[stack.pop()]-reached:reached.add(j);stack.append(j)
  self.assertEqual(len(reached),len(self.v))
 def test_shared_visibility_and_styles(self):
  d,n,xy,z=r.buffers(self.v,self.n,self.f,300,280);mask=np.isfinite(d);self.assertGreater(mask.sum(),10000);images=[np.array(r.shading(d,n,name)) for name in ['matte','metal','wire']]
  for im in images:self.assertTrue(np.array_equal(im[:,:,3]>0,mask))
  self.assertFalse(np.array_equal(images[0],images[1]));wire=np.array(r.wire_overlay(Image.fromarray(images[2]),xy,z,d));self.assertTrue(np.array_equal(wire[:,:,3],images[2][:,:,3]));self.assertGreater(np.count_nonzero(wire[:,:,:3]!=images[2][:,:,:3]),100)
 def test_obj_and_binary_stl(self):
  lines=(A/'form.obj').read_text().splitlines();vv=np.array([[float(x) for x in s.split()[1:]] for s in lines if s.startswith('v ')]);self.assertTrue(np.allclose(vv,self.v,atol=1e-9));self.assertEqual(sum(s.startswith('vn ') for s in lines),4480);self.assertEqual(sum(s.startswith('f ') for s in lines),8960);data=(A/'form.stl').read_bytes();count=struct.unpack_from('<I',data,80)[0];self.assertEqual(count,8960);self.assertEqual(len(data),84+count*50)
  for i in [0,100,5000,8959]:
   values=struct.unpack_from('<12fH',data,84+i*50);self.assertTrue(np.allclose(np.array(values[3:12]).reshape(3,3),self.v[self.f[i]],atol=1e-6))
 def test_jpeg_layouts(self):
  sizes={'hero.jpg':(1440,1020),'hero-mobile.jpg':(720,1120),'comparison.jpg':(1440,586),'comparison-mobile.jpg':(720,2160),'matte.jpg':(1100,1000),'metal.jpg':(1100,1000),'wire.jpg':(1100,1000)}
  for name,size in sizes.items():
   with Image.open(A/name) as im:self.assertEqual(im.size,size);self.assertEqual(getattr(im,'n_frames',1),1)
 def test_manifest_and_research(self):
  data=json.loads((A/'manifest.json').read_text());self.assertEqual(len(data),9)
  for name,digest in data.items():self.assertEqual(hashlib.sha256((A/name).read_bytes()).hexdigest(),digest)
  sources=json.loads((S/'sources.json').read_text());self.assertEqual(len(sources),8)
  for row in sources:self.assertRegex(row['commit'],r'^[0-9a-f]{40}$');self.assertTrue(row['scope'])
 def test_readme_insertion(self):
  text=(ROOT/'README.md').read_text();block=(S/'readme-block.md').read_text();self.assertIn(block,text);self.assertNotIn('<script',block);self.assertNotIn('<style',block);self.assertLess(text.index('## Ночной тираж'),text.index('## Материальная проба'));self.assertLess(text.index('## Материальная проба'),text.index('## Один шаг — один изменённый бит'))
 def test_regeneration_readonly_readme(self):
  before={p.name:p.read_bytes() for p in A.iterdir()};old=(ROOT/'README.md').read_bytes();subprocess.run([sys.executable,str(S/'generate.py')],check=True,capture_output=True);self.assertEqual(before,{p.name:p.read_bytes() for p in A.iterdir()});self.assertEqual(old,(ROOT/'README.md').read_bytes())
