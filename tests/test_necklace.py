import copy,csv,importlib.util,json,subprocess,sys,tempfile,unittest,zipfile
from collections import Counter
from itertools import product
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'atlas/samples/necklace';A=ROOT/'assets/necklace'
def load(name):
 spec=importlib.util.spec_from_file_location('necklace_'+name,S/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
c=load('construct');v=load('verify')
def cert(s,n=5):return dict(format='binary-necklace-v1',bits=s,order=n)
class NecklaceTests(unittest.TestCase):
 def test_orders(self):
  for n in range(1,11):
   s=c.construct(n);r=v.verify(cert(s,n));self.assertEqual(r['distinct_words'],2**n);self.assertEqual(len(s),2**n)
 def test_all_words_independent_linear_oracle(self):
  s=c.construct();linear=s+s[:4];windows=[linear[i:i+5] for i in range(32)];self.assertEqual(Counter(windows),Counter(''.join(p) for p in product('01',repeat=5)));self.assertEqual(len(linear),36);self.assertEqual(len(set(s[i:i+5] for i in range(28))),28)
 def test_rotations_reverse_complement(self):
  s=c.construct()
  for base in [s,s[::-1],''.join('1' if b=='0' else '0' for b in s)]:
   for i in range(32):self.assertTrue(v.verify(cert(base[i:]+base[:i]))['verified'])
 def test_all_single_bit_errors_rejected(self):
  s=c.construct()
  for i in range(32):
   t=s[:i]+('1' if s[i]=='0' else '0')+s[i+1:]
   with self.assertRaises(ValueError):v.verify(cert(t))
 def test_strict_input(self):
  for n in [True,0,11,-1,5.0,'5',None]:
   with self.assertRaises(ValueError):c.construct(n)
   with self.assertRaises(ValueError):v.verify(cert('0'*32,n))
  for s in [None,[],0,'0'*32,'1'*32,c.construct()[:-1],c.construct()+'0','x'+c.construct()[1:]]:
   with self.assertRaises(ValueError):v.verify(cert(s))
  with self.assertRaises(ValueError):v.verify({})
 def test_assets_zip_and_cli(self):
  certificate=json.loads((A/'certificate.json').read_text());self.assertEqual(certificate,cert(c.construct()));self.assertEqual(v.verify(certificate),json.loads((A/'audit.json').read_text()))
  with (A/'words.csv').open() as f:self.assertEqual(len(list(csv.DictReader(f))),32)
  with Image.open(A/'scan.gif') as im:self.assertEqual(im.n_frames,32);self.assertEqual(im.size,(1000,660))
  with tempfile.TemporaryDirectory() as tmp:
   with zipfile.ZipFile(A/'bench.zip') as z:z.extractall(tmp)
   r=subprocess.run([sys.executable,'-S',str(Path(tmp)/'verify.py'),str(Path(tmp)/'certificate.json')],capture_output=True,text=True);self.assertEqual(r.returncode,0,r.stderr);self.assertTrue(json.loads(r.stdout)['verified'])
 def test_edge_overlap(self):
  s=c.construct();r=v.verify(cert(s));self.assertEqual(sorted(r['positions'].values()),list(range(32)))
  for word,pos in r['positions'].items():
   nxt=''.join(s[(pos+1+j)%32] for j in range(5));self.assertEqual(word[1:],nxt[:4])
 def test_regeneration(self):
  before={p.name:p.read_bytes() for p in A.iterdir()};subprocess.run([sys.executable,str(S/'generate.py')],check=True,capture_output=True);self.assertEqual(before,{p.name:p.read_bytes() for p in A.iterdir()})
