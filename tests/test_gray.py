import copy,csv,importlib.util,json,subprocess,sys,tempfile,unittest,zipfile,xml.etree.ElementTree as ET
from itertools import product
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'atlas/samples/gray';A=ROOT/'assets/gray'
def load(name):
 spec=importlib.util.spec_from_file_location('gray_'+name,S/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
m=load('model');v=load('verify')
class GrayTests(unittest.TestCase):
 def test_all_edges(self):
  c=m.construct();r=v.verify(c);self.assertEqual(r,json.loads((A/'audit.json').read_text()));self.assertEqual(c,json.loads((A/'certificate.json').read_text()));self.assertEqual(r['binary_bit_changes'],126);self.assertEqual(r['gray_bit_changes'],64);self.assertEqual(r['binary_nonendpoint_readings'],320)
 def test_reflection_and_decode(self):
  words=v.reflected(6);self.assertEqual(len(set(words)),64)
  for i,w in enumerate(words):self.assertEqual(int(w,2),m.gray(i));self.assertEqual(m.decode(int(w,2)),i)
  self.assertEqual(words[-1],'100000');self.assertEqual(m.decode(16),31)
 def test_independent_all_source_masks(self):
  c=m.construct();words=v.reflected(6)
  for row in c['transitions']:
   i,j=row['from'],row['to'];binary=set();gray=set()
   for mask in range(64):
    flags=f'{mask:06b}';b=''.join(y if flag=='1' else x for x,y,flag in zip(f'{i:06b}',f'{j:06b}',flags));g=''.join(y if flag=='1' else x for x,y,flag in zip(words[i],words[j],flags));binary.add(int(b,2));gray.add(words.index(g))
   self.assertEqual(sorted(binary),row['binary_reads']);self.assertEqual(sorted(gray),row['gray_reads']);self.assertEqual(gray,{i,j})
 def test_worst_edges_and_counts(self):
  c=m.construct()
  for i in [31,63]:self.assertEqual(c['transitions'][i]['binary_reads'],list(range(64)))
  self.assertEqual(sum(len(r['binary_reads']) for r in c['transitions']),448);self.assertEqual(sum(len(r['gray_reads']) for r in c['transitions']),128)
 def test_tamper(self):
  for mutate in [lambda c:c['words'].__setitem__(1,'000000'),lambda c:c['transitions'][0].__setitem__('from',False),lambda c:c['transitions'][0].__setitem__('to',2),lambda c:c['transitions'][31].__setitem__('binary_reads',[31,32]),lambda c:c['transitions'][0].__setitem__('gray_reads',[0,True]),lambda c:c['transitions'][0].__setitem__('gray_reads',[1,0])]:
   bad=copy.deepcopy(m.construct());mutate(bad)
   with self.assertRaises(ValueError):v.verify(bad)
 def test_strict_inputs(self):
  for value in [True,-1,64,0.0,'0',None,[]]:
   with self.assertRaises(ValueError):m.decode(value)
  for value in [None,{},[],{'format':'bad'},{'format':'reflected-gray-six-v1','words':['0']}]:
   with self.assertRaises(ValueError):v.verify(value)
 def test_assets_and_cli(self):
  with Image.open(A/'scan.gif') as im:self.assertEqual(im.n_frames,7);self.assertEqual(im.size,(1000,660))
  ns={'s':'http://www.w3.org/2000/svg'};paths=ET.parse(A/'disk-a4.svg').findall('.//s:path',ns);self.assertEqual(len(paths),384)
  words=v.reflected(6)
  for path in paths:self.assertEqual(path.attrib['data-value'],words[int(path.attrib['data-position'])][int(path.attrib['data-bit'])])
  with (A/'transitions.csv').open() as f:self.assertEqual(len(list(csv.DictReader(f))),64)
  with tempfile.TemporaryDirectory() as tmp:
   with zipfile.ZipFile(A/'bench.zip') as z:z.extractall(tmp)
   r=subprocess.run([sys.executable,'-S',str(Path(tmp)/'verify.py'),str(Path(tmp)/'certificate.json')],capture_output=True,text=True);self.assertEqual(r.returncode,0,r.stderr);self.assertTrue(json.loads(r.stdout)['verified'])
 def test_regeneration(self):
  before={p.name:p.read_bytes() for p in A.iterdir()};subprocess.run([sys.executable,str(S/'generate.py')],check=True,capture_output=True);self.assertEqual(before,{p.name:p.read_bytes() for p in A.iterdir()})
