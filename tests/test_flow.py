import copy
import csv
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];SAMPLE=ROOT/'atlas/samples/flow';ASSETS=ROOT/'assets/flow'
def module(name):
    spec=importlib.util.spec_from_file_location('flow_'+name,SAMPLE/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
s=module('solve');v=module('verify')
class FlowTests(unittest.TestCase):
    def test_full_grid(self):
        cases=json.loads((ASSETS/'scenarios.json').read_text());self.assertEqual(len(cases),169)
        for a in range(13):
            for b in range(13):
                c=s.solve(a,b);self.assertEqual(c,cases[f'{a},{b}']);r=v.verify(c,True);self.assertTrue(r['exhaustive_agrees']);self.assertEqual(r['cuts_enumerated'],64)
                if a<12:self.assertLessEqual(c['value'],cases[f'{a+1},{b}']['value'])
                if b<12:self.assertLessEqual(c['value'],cases[f'{a},{b+1}']['value'])
    def test_presets(self):
        for name,a,b,value in [('baseline',7,6,12),('inlet',9,6,12),('outlet',7,8,12),('both',9,8,14),('wide',12,12,14)]:
            c=json.loads((ASSETS/(name+'.json')).read_text());self.assertEqual(c,s.solve(a,b));self.assertEqual(c['value'],value)
        r=v.verify(s.solve(12,12),True);self.assertEqual(r['all_minimum_cuts'],[[0,1,2,3,4,6]])
    def test_all_minimum_cuts_are_valid_certificates(self):
        for a,b in [(0,0),(7,6),(9,8),(12,12)]:
            c=s.solve(a,b);cuts=v.all_cuts(a,b);self.assertEqual(len(cuts),64);self.assertEqual(len({tuple(x['source_side']) for x in cuts}),64)
            for cut in cuts:
                changed=copy.deepcopy(c);changed['cut']=cut['source_side'];r=v.verify(changed);self.assertGreaterEqual(r['gap'],0);self.assertEqual(r['maximum_proved'],cut['capacity']==c['value'])
    def test_augmentation_logs(self):
        for a in range(13):
            for b in range(13):
                c=s.solve(a,b);g=s.edges(a,b);residual=[[0]*8 for _ in range(8)]
                for u,w,cap in g:residual[u][w]=cap
                value=0
                for event in c['augmentations']:
                    path=event['path'];delta=event['delta'];self.assertEqual(path[0],0);self.assertEqual(path[-1],7);self.assertEqual(len(path),len(set(path)));self.assertGreater(delta,0);self.assertEqual(delta,min(residual[u][w] for u,w in zip(path,path[1:])))
                    for u,w in zip(path,path[1:]):residual[u][w]-=delta;residual[w][u]+=delta
                    value+=delta
                self.assertEqual(value,c['value']);self.assertEqual([cap-residual[u][w] for u,w,cap in g],c['flows'])
    def test_tampering(self):
        c=s.solve(7,6);bad=copy.deepcopy(c);bad['flows'][0]-=1;self.assertFalse(v.verify(bad)['maximum_proved']);bad=copy.deepcopy(c);bad['value']-=1;self.assertFalse(v.verify(bad)['maximum_proved'])
        bad=copy.deepcopy(c);bad['flows'][0]+=1
        with self.assertRaises(ValueError):v.verify(bad)
        # The proof is the final flow/cut, not a trusted algorithm trace.
        del c['augmentations'];self.assertTrue(v.verify(c)['maximum_proved'])
    def test_strict_input(self):
        for value in [True,1.0,-1,13,'7',None]:
            with self.assertRaises(ValueError):s.solve(value,6)
            bad=s.solve(7,6);bad['valve_a']=value
            with self.assertRaises(ValueError):v.verify(bad)
        for cut in [[0,7],[1],[0,0],[False],[0,8]]:
            c=s.solve(7,6);c['cut']=cut
            with self.assertRaises(ValueError):v.verify(c)
        for value in [True,1.0,-1,100]:
            c=s.solve(7,6);c['flows'][0]=value
            with self.assertRaises(ValueError):v.verify(c)
    def test_assets_and_standalone(self):
        with Image.open(ASSETS/'valves.gif') as im:self.assertEqual(im.n_frames,40);self.assertEqual(im.size,(1000,620))
        with (ASSETS/'cuts.csv').open() as f:self.assertEqual(len(list(csv.DictReader(f))),10816)
        with tempfile.TemporaryDirectory() as tmp:
            with zipfile.ZipFile(ASSETS/'bench.zip') as z:z.extractall(tmp)
            r=subprocess.run([sys.executable,'-S',str(Path(tmp)/'verify.py'),str(Path(tmp)/'baseline.json'),'--all-cuts'],capture_output=True,text=True);self.assertEqual(r.returncode,0,r.stderr);self.assertTrue(json.loads(r.stdout)['exhaustive_agrees'])
    def test_regeneration(self):
        before={p.name:p.read_bytes() for p in ASSETS.iterdir()};subprocess.run([sys.executable,str(SAMPLE/'generate.py')],capture_output=True,check=True);self.assertEqual(before,{p.name:p.read_bytes() for p in ASSETS.iterdir()})
