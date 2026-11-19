import copy
import importlib.util
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest
import zipfile
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];SAMPLE=ROOT/'atlas/samples/lights';ASSETS=ROOT/'assets/lights'
def module(name):
    spec=importlib.util.spec_from_file_location('lights_'+name,SAMPLE/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
c=module('core');v=module('verify')

def chase(board):
    solutions=[]
    for first in range(32):
        cells=[(board>>i)&1 for i in range(25)];pressed=0
        def press(r,col):
            nonlocal pressed
            pressed^=1<<(r*5+col)
            for rr,cc in [(r,col),(r-1,col),(r+1,col),(r,col-1),(r,col+1)]:
                if 0<=rr<5 and 0<=cc<5:cells[rr*5+cc]^=1
        for col in range(5):
            if first>>col&1:press(0,col)
        for r in range(1,5):
            for col in range(5):
                if cells[(r-1)*5+col]:press(r,col)
        if not any(cells):solutions.append(pressed)
    return sorted(solutions,key=lambda x:(x.bit_count(),x))

class LightsTests(unittest.TestCase):
    def setUp(self):self.cert=json.loads((ASSETS/'certificate.json').read_text())
    def test_full_certificate(self):
        result=v.check(self.cert,json.loads((ASSETS/'solution.json').read_text()));self.assertEqual(result,json.loads((ASSETS/'audit.json').read_text()));self.assertEqual(result['rank'],23);self.assertEqual(result['nullity'],2);self.assertEqual(result['operations_replayed'],202);self.assertEqual(self.cert,c.certificate())
    def test_against_independent_first_row_enumeration(self):
        rng=random.Random(20261118);classes=set()
        for board in [0,(1<<25)-1,1,c.apply((1<<25)-1)]+[rng.randrange(1<<25) for _ in range(120)]:
            solution=c.solve(board,self.cert);self.assertEqual(solution['candidates'],chase(board));classes.add(tuple(solution['syndrome']));v.check(self.cert,solution)
        self.assertEqual(len(classes),4)
    def test_invariants_and_double_click(self):
        rng=random.Random(12)
        for _ in range(30):
            board=rng.randrange(1<<25);before=c.solve(board,self.cert)['syndrome']
            for i,effect in enumerate(c.moves()):
                self.assertEqual(c.solve(board^effect,self.cert)['syndrome'],before);self.assertEqual(board^effect^effect,board)
    def test_nullspace_and_minimum_witness(self):
        a,b=self.cert['kernel'];self.assertEqual(len({0,a,b,a^b}),4)
        for pattern in [0,a,b,a^b]:self.assertEqual(c.apply(pattern),0)
        solution=json.loads((ASSETS/'solution.json').read_text());self.assertEqual(solution['minimum'],9);self.assertEqual([x.bit_count() for x in solution['candidates']],[9,13,13,25]);self.assertEqual(solution['board'],c.apply((1<<25)-1));self.assertEqual(solution['candidates'][-1],(1<<25)-1)
        bad=json.loads((ASSETS/'impossible.json').read_text());self.assertFalse(bad['solvable']);self.assertEqual(bad['syndrome'],[0,1]);self.assertTrue(v.check(self.cert,bad)['board_witness_verified'])
    def test_tamper(self):
        for field in ['rref','transform','kernel','checks','pivots']:
            bad=copy.deepcopy(self.cert);bad[field][0]^=1
            with self.assertRaises(ValueError):v.check(bad)
        bad=copy.deepcopy(self.cert);bad['operations'][0]=['xor',0,0]
        with self.assertRaises(ValueError):v.check(bad)
        witness=json.loads((ASSETS/'solution.json').read_text())
        for field,value in [('minimum',10),('minimum',True),('chosen',witness['candidates'][1]),('candidates',witness['candidates'][:-1]),('board',True)]:
            bad=copy.deepcopy(witness);bad[field]=value
            with self.assertRaises(ValueError):v.check(self.cert,bad)
    def test_strict_input(self):
        for value in [True,1.0,-1,1<<25,'1',None]:
            with self.assertRaises(ValueError):c.solve(value,self.cert)
            with self.assertRaises(ValueError):c.apply(value)
        for op in [['xor',False,1],['xor',25,1],['what',0,1]]:
            bad=copy.deepcopy(self.cert);bad['operations'][0]=op
            with self.assertRaises(ValueError):v.check(bad)
    def test_standalone_and_assets(self):
        with Image.open(ASSETS/'switches.gif') as im:self.assertEqual(im.n_frames,10);self.assertEqual(im.size,(920,620))
        route=json.loads((ASSETS/'route.json').read_text());self.assertEqual(route[-1]['board'],0);self.assertEqual(len(route),10)
        with tempfile.TemporaryDirectory() as tmp:
            with zipfile.ZipFile(ASSETS/'bench.zip') as z:z.extractall(tmp)
            for name in ['solution.json','impossible.json']:
                result=subprocess.run([sys.executable,'-S',str(Path(tmp)/'verify.py'),str(Path(tmp)/'certificate.json'),str(Path(tmp)/name)],capture_output=True,text=True);self.assertEqual(result.returncode,0,result.stderr);self.assertTrue(json.loads(result.stdout)['matrix_certificate_verified'])
    def test_regeneration(self):
        before={p.name:p.read_bytes() for p in ASSETS.iterdir()};subprocess.run([sys.executable,str(SAMPLE/'generate.py')],capture_output=True,check=True);self.assertEqual(before,{p.name:p.read_bytes() for p in ASSETS.iterdir()})
