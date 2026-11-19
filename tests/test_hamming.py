import copy,csv,importlib.util,json,subprocess,sys,tempfile,unittest,zipfile
from itertools import product,combinations
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'atlas/samples/hamming';A=ROOT/'assets/hamming'
def load(name):
 spec=importlib.util.spec_from_file_location('hamming_'+name,S/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
c=load('codec');v=load('verify')
def flip(s,p):return ''.join(('1' if b=='0' else '0') if i in p else b for i,b in enumerate(s,1))
class HammingTests(unittest.TestCase):
 def test_full_space(self):
  by_weight=[dict(weight=i,cases=0,recovered=0,zero_syndrome=0) for i in range(8)];count=0
  for data in map(''.join,product('01',repeat=4)):
   for mask in range(128):
    positions=[p for p in range(1,8) if mask&(1<<(p-1))];cert=c.certificate(data,flip(c.encode(data),positions));r=v.verify(cert);row=by_weight[len(positions)];row['cases']+=1;row['recovered']+=r['candidate_equals_sent'];row['zero_syndrome']+=not r['syndrome'];self.assertEqual(r['true_errors_known_to_demo'],len(positions));self.assertEqual(r['candidate_equals_sent'],len(positions)<=1);count+=1
  self.assertEqual(count,2048);self.assertEqual(by_weight,json.loads((A/'audit.json').read_text())['byWeight'])
 def test_code_distance_and_spheres(self):
  book=v.codebook();self.assertEqual(len(book),16);self.assertEqual(min(v.distance(a,b) for a,b in combinations(book,2)),3);self.assertEqual(set(book),{c.encode(f'{i:04b}') for i in range(16)})
  for received in map(''.join,product('01',repeat=7)):
   nearest=[w for w in book if v.distance(w,received)<=1];self.assertEqual(nearest,[c.decode(received)['candidate']])
 def test_positions_and_syndromes(self):
  self.assertEqual(c.encode('1011'),'0110011')
  for data in map(''.join,product('01',repeat=4)):
   sent=c.encode(data)
   for i in range(1,8):self.assertEqual(c.syndrome(flip(sent,[i])),i)
   for i,j in combinations(range(1,8),2):self.assertEqual(c.syndrome(flip(sent,[i,j])),i^j)
 def test_double_and_undetected_examples(self):
  for name in ['clean','single','double','undetected']:
   cert=json.loads((A/(name+'.json')).read_text());r=v.verify(cert);self.assertEqual(r['candidate_equals_sent'],name in ['clean','single'])
  cert=json.loads((A/'double.json').read_text());self.assertEqual(cert['syndrome'],6);self.assertEqual(c.syndrome(cert['candidate']),0)
  cert=json.loads((A/'undetected.json').read_text());self.assertEqual(cert['syndrome'],0)
 def test_tamper(self):
  good=json.loads((A/'single.json').read_text())
  for field,value in [('sent','0000000'),('data','0000'),('syndrome',True),('syndrome',4),('candidate',good['received']),('candidate_data','0000'),('format','bad')]:
   bad=copy.deepcopy(good);bad[field]=value
   with self.assertRaises(ValueError):v.verify(bad)
 def test_strict_inputs(self):
  for value in [None,True,4,[], '000','00000','abc1']:
   with self.assertRaises(ValueError):c.encode(value)
  for value in [None,True,7,[],'000000','00000000','abcdefg']:
   with self.assertRaises(ValueError):c.decode(value)
   cert=json.loads((A/'single.json').read_text());cert['received']=value
   with self.assertRaises(ValueError):v.verify(cert)
 def test_assets_and_cli(self):
  with Image.open(A/'checks.gif') as im:self.assertEqual(im.n_frames,11);self.assertEqual(im.size,(1000,660))
  with (A/'sweep.csv').open() as f:self.assertEqual(len(list(csv.DictReader(f))),2048)
  with tempfile.TemporaryDirectory() as tmp:
   with zipfile.ZipFile(A/'bench.zip') as z:z.extractall(tmp)
   for name in ['clean','single','double','undetected']:
    r=subprocess.run([sys.executable,'-S',str(Path(tmp)/'verify.py'),str(Path(tmp)/(name+'.json'))],capture_output=True,text=True);self.assertEqual(r.returncode,0,r.stderr);self.assertTrue(json.loads(r.stdout)['verified'])
 def test_regeneration(self):
  before={p.name:p.read_bytes() for p in A.iterdir()};subprocess.run([sys.executable,str(S/'generate.py')],check=True,capture_output=True);self.assertEqual(before,{p.name:p.read_bytes() for p in A.iterdir()})
