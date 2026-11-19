import copy,csv,importlib.util,json,subprocess,sys,tempfile,unittest,zipfile
from fractions import Fraction
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'atlas/samples/simpson';A=ROOT/'assets/simpson'
def load(name):
 spec=importlib.util.spec_from_file_location('simpson_'+name,S/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
m=load('model');v=load('verify')
class SimpsonTests(unittest.TestCase):
 def test_all_compositions(self):
  reverse=0
  for a in range(1,10):
   for b in range(1,10):
    c=m.construct(a,b);r=v.verify(c);reverse+=r['reversal'];self.assertEqual(r['reversal'],b-a>=2);self.assertNotEqual(r['total_cross'],0);self.assertEqual(r['aggregate_A'],[30+6*a,100]);self.assertEqual(r['aggregate_B'],[20+6*b,100])
  self.assertEqual(reverse,28)
 def test_expanded_observations_oracle(self):
  for a in range(1,10):
   for b in range(1,10):
    c=m.construct(a,b);results=[]
    for k in [0,2]:
     trials=[]
     for row in c['rows']:trials.extend([True]*row[k]+[False]*(row[k+1]-row[k]))
     self.assertEqual(len(trials),100);results.append(Fraction(sum(trials),len(trials)))
    self.assertEqual(results[0]<results[1],c['reversal'])
 def test_common_weights_exact(self):
  for a in range(1,10):
   for b in range(1,10):
    for entry in m.construct(a,b)['common_weights']:self.assertEqual(Fraction(*entry['A'])-Fraction(*entry['B']),Fraction(1,10))
 def test_examples(self):
  for name,a,b in [('reversal',1,9),('equal-mix',5,5),('near',4,5)]:self.assertEqual(m.construct(a,b),json.loads((A/(name+'.json')).read_text()))
  self.assertEqual(v.verify(m.construct(1,9))['aggregate_A'],[36,100]);self.assertEqual(v.verify(m.construct(1,9))['aggregate_B'],[74,100]);self.assertFalse(v.verify(m.construct(4,5))['reversal'])
 def test_tamper(self):
  c=m.construct()
  for field,value in [('group_cross',[1,1]),('total_cross',True),('total_cross',0),('reversal',False),('rows',[[True,10,8,90],c['rows'][1]]),('rows',[[11,10,8,90],c['rows'][1]])]:
   bad=copy.deepcopy(c);bad[field]=value
   with self.assertRaises(ValueError):v.verify(bad)
  bad=copy.deepcopy(c);bad['common_weights'][5]['A']=[61,100]
  with self.assertRaises(ValueError):v.verify(bad)
  bad=copy.deepcopy(c);bad['common_weights'][0]['easy_tenths']=True
  with self.assertRaises(ValueError):v.verify(bad)
 def test_strict_inputs(self):
  for value in [True,0,10,-1,1.0,'1',None,[]]:
   with self.assertRaises(ValueError):m.construct(value,5)
   with self.assertRaises(ValueError):m.construct(5,value)
  for row in [[1,0,1,10],[1,1000001,1,10],[1,10,2,10],['1',10,0,10]]:
   bad=m.construct();bad['rows'][0]=row
   with self.assertRaises(ValueError):v.verify(bad)
 def test_assets_and_cli(self):
  with Image.open(A/'mix.gif') as im:self.assertEqual(im.n_frames,8);self.assertEqual(im.size,(1000,660))
  with (A/'grid.csv').open() as f:self.assertEqual(len(list(csv.DictReader(f))),81)
  with tempfile.TemporaryDirectory() as tmp:
   with zipfile.ZipFile(A/'bench.zip') as z:z.extractall(tmp)
   for name in ['reversal','equal-mix','near']:
    r=subprocess.run([sys.executable,'-S',str(Path(tmp)/'verify.py'),str(Path(tmp)/(name+'.json'))],capture_output=True,text=True);self.assertEqual(r.returncode,0,r.stderr);self.assertTrue(json.loads(r.stdout)['verified'])
 def test_regeneration(self):
  before={p.name:p.read_bytes() for p in A.iterdir()};subprocess.run([sys.executable,str(S/'generate.py')],check=True,capture_output=True);self.assertEqual(before,{p.name:p.read_bytes() for p in A.iterdir()})
