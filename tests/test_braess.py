import copy
import csv
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];SAMPLE=ROOT/'atlas/samples/braess';ASSETS=ROOT/'assets/braess'
def module(name):
    spec=importlib.util.spec_from_file_location('braess_'+name,SAMPLE/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
m=module('model');v=module('verify')
class BraessTests(unittest.TestCase):
    def test_every_integer_demand(self):
        for q in range(1,10001):
            a=m.equilibrium(q,False);b=m.equilibrium(q,True)
            self.assertTrue(v.verify(a)['equilibrium_verified']);self.assertTrue(v.verify(b)['equilibrium_verified']);delta=F(b['time'])-F(a['time']);self.assertEqual(delta>0,3000<q<9000)
    def test_witness_and_thresholds(self):
        a=json.loads((ASSETS/'closed.json').read_text());b=json.loads((ASSETS/'open.json').read_text());self.assertEqual(a,m.equilibrium(4000,False));self.assertEqual(b,m.equilibrium(4000,True));self.assertEqual(a['time'],'65');self.assertEqual(b['time'],'80');self.assertEqual(b['route_times'],{'SAT':'85','SBT':'85','SABT':'80'})
        for q in [3000,9000,10000]:self.assertEqual(m.equilibrium(q,False)['time'],m.equilibrium(q,True)['time'])
        self.assertEqual(m.equilibrium(4500,True)['flows']['SABT'],'4500');self.assertEqual(m.equilibrium(9000,True)['flows']['SABT'],'0')
    def test_independent_potential_grid(self):
        # Beckmann potential is not total travel time. A finite coarse-grid sanity check.
        for q in [2000,4000,6000,10000]:
            c=m.equilibrium(q,True);p=c['flows'];x,y,z=(F(p[k]) for k in ['SAT','SBT','SABT'])
            def potential(x,y,z):return F((x+z)**2+(y+z)**2,200)+45*(x+y)
            value=potential(x,y,z)
            for xx in range(0,q+1,500):
                for yy in range(0,q-xx+1,500):self.assertLessEqual(value,potential(xx,yy,q-xx-yy))
    def test_tampering(self):
        c=m.equilibrium(4000,True)
        for key,value in [('time','79'),('route_times',{'SAT':'85','SBT':'85','SABT':'79'}),('flows',{'SAT':'1','SBT':'0','SABT':'3999'})]:
            bad=copy.deepcopy(c);bad[key]=value;self.assertFalse(v.verify(bad)['equilibrium_verified'])
        # Correctly claimed costs, conserved flow, but used routes are not equally cheapest.
        bad=copy.deepcopy(c);bad['flows']={'SAT':'1000','SBT':'1000','SABT':'2000'};bad['route_times']={'SAT':'75','SBT':'75','SABT':'60'};bad['time']='60';self.assertFalse(v.verify(bad)['wardrop'])
    def test_strict_input(self):
        for q in [True,1.0,0,-1,10001,'4000']:
            with self.assertRaises(ValueError):m.equilibrium(q,True)
            c=m.equilibrium(4000,True);c['demand']=q
            with self.assertRaises(ValueError):v.verify(c)
        for value in [True,4,'nan','1/0','1e4',[]]:
            c=m.equilibrium(4000,True);c['flows']['SAT']=value
            with self.assertRaises(ValueError):v.verify(c)
        for flows in [{'SAT':'-1','SBT':'1','SABT':'4000'},{'SAT':'0','SBT':'0','SABT':'1'},{}]:
            c=m.equilibrium(4000,True);c['flows']=flows
            with self.assertRaises(ValueError):v.verify(c)
    def test_published_sweep_and_assets(self):
        sweep=json.loads((ASSETS/'sweep.json').read_text());self.assertEqual(len(sweep),91)
        for q,pair in sweep.items():
            for i,c in enumerate(pair):self.assertEqual(c,m.equilibrium(int(q),bool(i)));self.assertTrue(v.verify(c)['equilibrium_verified'])
        with (ASSETS/'sweep.csv').open() as f:self.assertEqual(len(list(csv.DictReader(f))),91)
        with Image.open(ASSETS/'roads.gif') as im:self.assertEqual(im.n_frames,60);self.assertEqual(im.size,(920,560))
    def test_standalone_zip(self):
        with tempfile.TemporaryDirectory() as tmp:
            with zipfile.ZipFile(ASSETS/'bench.zip') as z:z.extractall(tmp)
            for name in ['closed.json','open.json']:
                r=subprocess.run([sys.executable,'-S',str(Path(tmp)/'verify.py'),str(Path(tmp)/name)],capture_output=True,text=True);self.assertEqual(r.returncode,0,r.stderr);self.assertTrue(json.loads(r.stdout)['equilibrium_verified'])
    def test_regeneration(self):
        before={p.name:p.read_bytes() for p in ASSETS.iterdir()};subprocess.run([sys.executable,str(SAMPLE/'generate.py')],capture_output=True,check=True);self.assertEqual(before,{p.name:p.read_bytes() for p in ASSETS.iterdir()})
