import copy
import importlib.util
import itertools
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT=Path(__file__).resolve().parents[1];SAMPLE=ROOT/'atlas/samples/transport';ASSETS=ROOT/'assets/transport'
def load(name):
    spec=importlib.util.spec_from_file_location('transport_'+name,SAMPLE/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
s=load('solve');v=load('verify')

class TransportTests(unittest.TestCase):
    def test_bruteforce(self):
        rng=random.Random(20261118)
        for n in range(1,8):
            for trial in range(10):
                p={'cost':'squared_euclidean','source':[[rng.randrange(-10,11),rng.randrange(-10,11)] for _ in range(n)],'target':[[rng.randrange(-10,11),rng.randrange(-10,11)] for _ in range(n)]}
                matrix=s.costs(p['source'],p['target']);c=s.hungarian(matrix);r=v.verify(p,c)
                self.assertTrue(r['optimal_proved']);self.assertEqual(r['primal_cost'],min(sum(matrix[i][j] for i,j in enumerate(a)) for a in itertools.permutations(range(n))))
    def test_published(self):
        p=json.loads((ASSETS/'problem.json').read_text());c=json.loads((ASSETS/'certificate.json').read_text());r=v.verify(p,c)
        self.assertTrue(r['optimal_proved']);self.assertEqual(r['primal_cost'],47854);self.assertEqual(len(set(map(tuple,p['source']))),64);self.assertEqual(len(set(map(tuple,p['target']))),64)
        matrix=s.costs(p['source'],p['target']);self.assertEqual(sum(matrix[i][j] for i,j in enumerate(s.greedy(matrix))),62850)
    def test_tampering(self):
        p=json.loads((ASSETS/'problem.json').read_text());c=json.loads((ASSETS/'certificate.json').read_text())
        for field in ['u','v']:
            for delta in [-1,1]:
                bad=copy.deepcopy(c);bad[field][0]+=delta;self.assertFalse(v.verify(p,bad)['optimal_proved'])
        bad=copy.deepcopy(c);bad['assignment'][0]=bad['assignment'][1]
        with self.assertRaises(ValueError):v.verify(p,bad)
        bad=copy.deepcopy(c);bad['assignment'][0],bad['assignment'][1]=bad['assignment'][1],bad['assignment'][0]
        self.assertFalse(v.verify(p,bad)['optimal_proved'])
    def test_strict_input(self):
        p={'cost':'squared_euclidean','source':[[0,0]],'target':[[1,1]]};c=s.hungarian([[2]])
        for value in [True,1.0,'1',10001]:
            bad=copy.deepcopy(p);bad['source'][0][0]=value
            with self.assertRaises(ValueError):v.verify(bad,c)
        for value in [True,1.0,'0']:
            bad=copy.deepcopy(c);bad['assignment'][0]=value
            with self.assertRaises(ValueError):v.verify(p,bad)
        for matrix in [[],[[1,2]],[[True]],[[-1]]]:
            with self.assertRaises(ValueError):s.hungarian(matrix)
    def test_ties_and_greedy_order(self):
        self.assertEqual(s.hungarian([[0]*4 for _ in range(4)])['assignment'],list(range(4)))
        matrix=[[1,4],[0,9]];self.assertEqual(sum(matrix[i][j] for i,j in enumerate(s.greedy(matrix))),10)
        self.assertEqual(sum(matrix[i][j] for i,j in enumerate(s.hungarian(matrix)['assignment'])),4)
    def test_standalone_zip(self):
        with tempfile.TemporaryDirectory() as tmp:
            with zipfile.ZipFile(ASSETS/'bench.zip') as z:z.extractall(tmp)
            result=subprocess.run([sys.executable,'-S',str(Path(tmp)/'verify.py'),str(Path(tmp)/'problem.json'),str(Path(tmp)/'certificate.json')],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr);self.assertTrue(json.loads(result.stdout)['optimal_proved'])
    def test_regeneration(self):
        before={p.name:p.read_bytes() for p in ASSETS.iterdir()}
        subprocess.run([sys.executable,str(SAMPLE/'generate.py')],check=True,capture_output=True)
        self.assertEqual(before,{p.name:p.read_bytes() for p in ASSETS.iterdir()})
