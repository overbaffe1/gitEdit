import copy,csv,importlib.util,json,subprocess,sys,tempfile,unittest,zipfile
from itertools import product
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'atlas/samples/coins';A=ROOT/'assets/coins'
def load(name):
 spec=importlib.util.spec_from_file_location('coins_'+name,S/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
c=load('construct');v=load('verify')
class CoinsTests(unittest.TestCase):
 def test_plan_all_cases(self):
  plan=c.construct();r=v.verify(plan);self.assertEqual(r,json.loads((A/'audit.json').read_text()));self.assertEqual(r['distinct_traces'],24);self.assertEqual(r['pan_sizes'],[[4,4,4]]*3);self.assertEqual(plan,json.loads((A/'plan.json').read_text()))
 def test_variable_mass_oracle(self):
  plan=c.construct()
  for case in plan['cases']:
   for deviation in [1,3,99,101,1000]:
    masses=[100]*12;masses[case['coin']-1]+=deviation if case['kind']=='heavy' else -1 # independently vary valid positive light masses below
    if case['kind']=='light':masses[case['coin']-1]=max(1,100-min(deviation,99))
    trace=[]
    for row in plan['rows']:
     left=[i for i in range(12) if row[i]==1];right=[i for i in range(12) if row[i]==-1];x=sum(masses[i] for i in left)-sum(masses[i] for i in right);trace.append((x>0)-(x<0))
    self.assertEqual(trace,case['outcomes'])
 def test_prefixes_and_unused(self):
  plan=c.construct()
  for case in plan['cases']:
   for n in range(4):self.assertIn(case,[x for x in plan['cases'] if x['outcomes'][:n]==case['outcomes'][:n]])
   self.assertEqual(len([x for x in plan['cases'] if x['outcomes']==case['outcomes']]),1)
  used={tuple(x['outcomes']) for x in plan['cases']};unused=set(product((-1,0,1),repeat=3))-used;self.assertEqual(len(unused),3);self.assertIn((0,0,0),unused)
 def test_thirteen_bound(self):
  rows=v.thirteen_bound();self.assertEqual(rows,json.loads((A/'thirteen.json').read_text()));self.assertFalse(any(x['both_branches_fit'] for x in rows));self.assertTrue(all(x['unbalanced_hypotheses']>9 or x['balanced_hypotheses']>9 for x in rows));self.assertLess(3**2,24);self.assertGreaterEqual(3**3,26)
 def test_plan_symmetries(self):
  plan=c.construct()
  for p in [plan,{'format':plan['format'],'rows':plan['rows'][::-1],'cases':[{**x,'outcomes':x['outcomes'][::-1]} for x in plan['cases']]},{'format':plan['format'],'rows':[[-v for v in r] for r in plan['rows']],'cases':[{**x,'outcomes':[-v for v in x['outcomes']]} for x in plan['cases']]}]:self.assertTrue(v.verify(p)['verified'])
 def test_tamper_and_inputs(self):
  for mutate in [lambda p:p['rows'][0].__setitem__(0,1),lambda p:p['rows'][0].__setitem__(0,True),lambda p:p['cases'][0]['outcomes'].__setitem__(0,1),lambda p:p['cases'][0].__setitem__('coin',True),lambda p:p['cases'][0].__setitem__('kind','normal'),lambda p:p['cases'].__setitem__(1,p['cases'][0]),lambda p:p['rows'].__setitem__(1,p['rows'][0])]:
   bad=copy.deepcopy(c.construct());mutate(bad)
   with self.assertRaises(ValueError):v.verify(bad)
  for bad in [None,{},[],{'format':'twelve-coins-v1','rows':[]}, {'format':'bad'}]:
   with self.assertRaises(ValueError):v.verify(bad)
 def test_assets_and_cli(self):
  with Image.open(A/'weigh.gif') as im:self.assertEqual(im.n_frames,8);self.assertEqual(im.size,(1000,660))
  with (A/'cases.csv').open() as f:self.assertEqual(len(list(csv.DictReader(f))),24)
  with tempfile.TemporaryDirectory() as tmp:
   with zipfile.ZipFile(A/'bench.zip') as z:z.extractall(tmp)
   r=subprocess.run([sys.executable,'-S',str(Path(tmp)/'verify.py'),str(Path(tmp)/'plan.json')],capture_output=True,text=True);self.assertEqual(r.returncode,0,r.stderr);self.assertTrue(json.loads(r.stdout)['verified'])
 def test_regeneration(self):
  before={p.name:p.read_bytes() for p in A.iterdir()};subprocess.run([sys.executable,str(S/'generate.py')],check=True,capture_output=True);self.assertEqual(before,{p.name:p.read_bytes() for p in A.iterdir()})
