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
ROOT=Path(__file__).resolve().parents[1];SAMPLE=ROOT/'atlas/samples/matching';ASSETS=ROOT/'assets/matching'
def module(name):
    spec=importlib.util.spec_from_file_location('matching_'+name,SAMPLE/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
s=module('solve');v=module('verify')
class MatchingTests(unittest.TestCase):
    def setUp(self):self.problem=json.loads((ASSETS/'problem.json').read_text());self.cert=json.loads((ASSETS/'certificate.json').read_text())
    def test_full_enumeration(self):
        r=v.audit(self.problem,self.cert['A_assignment'],self.cert['B_assignment'],self.cert['all_stable']);self.assertEqual(r,json.loads((ASSETS/'audit.json').read_text()));self.assertEqual(r['stable_count'],5);self.assertEqual(r['changed_pairs'],7);self.assertTrue(r['A_proposer_optimal']);self.assertTrue(r['B_proposer_optimal'])
    def test_random_small_instances(self):
        rng=random.Random(12345)
        for n in range(1,7):
            for trial in range(4):
                p={side:[rng.sample(range(n),n) for _ in range(n)] for side in ['A','B']};a=s.deferred(p,'A')['assignment'];b=s.deferred(p,'B')['assignment'];r=v.audit(p,a,b);self.assertTrue(r['A_proposer_optimal']);self.assertTrue(r['B_proposer_optimal'])
    def test_event_replay(self):
        logs=json.loads((ASSETS/'events.json').read_text())
        for side in ['A','B']:
            self.assertEqual(logs[side],s.deferred(self.problem,side));held={};seen=set();opposite='B' if side=='A' else 'A';choices=[0]*8
            for e in logs[side]['events']:
                p,r=e['proposer'],e['receiver'];self.assertNotIn((p,r),seen);seen.add((p,r));self.assertNotIn(p,held.values());self.assertEqual(r,self.problem[side][p][choices[p]]);choices[p]+=1;old=held.get(r,-1);row=self.problem[opposite][r];accepted=old==-1 or row.index(p)<row.index(old);self.assertEqual(e['accepted'],accepted);self.assertEqual(e['displaced'],old if accepted else -1)
                if accepted:held[r]=p
                expected=[-1]*8
                for receiver,proposer in held.items():expected[proposer if side=='A' else receiver]=receiver if side=='A' else proposer
                self.assertEqual(e['assignment'],expected)
            self.assertLessEqual(len(seen),64);self.assertEqual(len(held),8);self.assertEqual(expected,logs[side]['assignment'])
    def test_manual_swap_and_witness(self):
        broken=json.loads((ASSETS/'broken.json').read_text());pairs=v.blocking(self.problem,broken['assignment']);self.assertEqual(pairs,broken['blocking_pairs']);self.assertEqual(len(pairs),6)
        for m in self.cert['all_stable']:self.assertEqual(v.blocking(self.problem,m),[])
    def test_tampering(self):
        a=self.cert['A_assignment'];b=self.cert['B_assignment']
        with self.assertRaises(ValueError):v.audit(self.problem,a,b,self.cert['all_stable'][:-1])
        wrong=copy.deepcopy(self.cert['all_stable']);wrong[0][0]=True
        with self.assertRaises(ValueError):v.audit(self.problem,a,b,wrong)
        reversed=v.audit(self.problem,b,a);self.assertFalse(reversed['A_proposer_optimal']);self.assertFalse(reversed['B_proposer_optimal'])
    def test_strict_inputs(self):
        for value in [True,1.0,'1',8]:
            p=copy.deepcopy(self.problem);p['A'][0][0]=value
            with self.assertRaises(ValueError):s.deferred(p)
            with self.assertRaises(ValueError):v.enumerate_stable(p)
        for m in [[0]*8,[True]+list(range(1,8)),list(range(7))]:
            with self.assertRaises(ValueError):v.blocking(self.problem,m)
        for p in [{},{'A':[],'B':[]},{'A':[[0]],'B':[]}]:
            with self.assertRaises(ValueError):s.deferred(p)
    def test_standalone_assets(self):
        with Image.open(ASSETS/'proposals.gif') as im:self.assertEqual(im.n_frames,16);self.assertEqual(im.size,(920,620))
        with tempfile.TemporaryDirectory() as tmp:
            with zipfile.ZipFile(ASSETS/'bench.zip') as z:z.extractall(tmp)
            result=subprocess.run([sys.executable,'-S',str(Path(tmp)/'verify.py'),str(Path(tmp)/'problem.json'),str(Path(tmp)/'certificate.json')],capture_output=True,text=True);self.assertEqual(result.returncode,0,result.stderr);self.assertTrue(json.loads(result.stdout)['A_proposer_optimal'])
    def test_regeneration(self):
        before={p.name:p.read_bytes() for p in ASSETS.iterdir()};subprocess.run([sys.executable,str(SAMPLE/'generate.py')],capture_output=True,check=True);self.assertEqual(before,{p.name:p.read_bytes() for p in ASSETS.iterdir()})
