import copy
import csv
import importlib.util
import io
import itertools
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];SAMPLE=ROOT/'atlas/samples/dice';ASSETS=ROOT/'assets/dice'
def module(name):
    spec=importlib.util.spec_from_file_location('dice_'+name,SAMPLE/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
exact=module('exact');verifier=module('verify')
class DiceTests(unittest.TestCase):
    def test_full_published_audit(self):
        dice=json.loads((ASSETS/'dice.json').read_text());report=json.loads((ASSETS/'audit.json').read_text());self.assertTrue(verifier.verify(dice,report));self.assertEqual(exact.audit(dice),report)
        for pair in ['AB','BC','CD','DA']:
            self.assertEqual(report['modes']['1']['pairs'][pair],{'wins':24,'ties':0,'losses':12,'total':36,'probability':'2/3'})
        for pair in ['AB','BC']:self.assertEqual(report['modes']['2']['pairs'][pair]['probability'],'4/9')
        for pair in ['CD','DA']:self.assertEqual(report['modes']['2']['pairs'][pair]['probability'],'5/9')
    def test_random_arrays_against_face_enumeration(self):
        rng=random.Random(123)
        for trial in range(12):
            dice={a:[rng.randrange(-8,9) for _ in range(6)] for a in 'ABCD'}
            self.assertTrue(verifier.verify(dice,exact.audit(dice)))
        for n in range(1,5):
            f=[-1,-1,0,2,4,4];counts=exact.distribution(f,n);outcomes=list(map(sum,itertools.product(f,repeat=n)));self.assertEqual(sum(counts.values()),6**n)
            for total,count in counts.items():self.assertEqual(count,outcomes.count(total))
    def test_symmetry_and_ties(self):
        r=exact.audit(exact.DICE)
        for mode in r['modes'].values():
            for a in 'ABCD':
                for b in 'ABCD':
                    p=mode['pairs'][a+b];q=mode['pairs'][b+a];self.assertEqual(p['wins'],q['losses']);self.assertEqual(p['ties'],q['ties']);self.assertEqual(p['wins']+p['ties']+p['losses'],p['total'])
        self.assertEqual(r['modes']['1']['pairs']['BB']['ties'],36)
        equal={a:[7]*6 for a in 'ABCD'};self.assertTrue(verifier.verify(equal,exact.audit(equal)))
    def test_tampering(self):
        r=exact.audit(exact.DICE)
        for path,value in [(['modes','1','pairs','AB','wins'],23),(['modes','2','pairs','AB','probability'],'2/3'),(['modes','1','best_response','A'],'B'),(['modes','2','distributions','A','8'],15),(['dice','A'],[0]*6),(['modes','1','pairs','BB','wins'],False)]:
            bad=copy.deepcopy(r);obj=bad
            for key in path[:-1]:obj=obj[key]
            obj[path[-1]]=value;self.assertFalse(verifier.verify(exact.DICE,bad))
        for bad in [None,[],{}, {'dice':[]}]:self.assertFalse(verifier.verify(exact.DICE,bad))
    def test_strict_inputs(self):
        for value in [True,2.0,'4',101]:
            dice=copy.deepcopy(exact.DICE);dice['A'][0]=value
            with self.assertRaises(ValueError):exact.audit(dice)
            with self.assertRaises(ValueError):verifier.verify(dice,{})
        for n in [0,5,True,1.0]:
            with self.assertRaises(ValueError):exact.distribution([1]*6,n)
    def test_assets(self):
        with Image.open(ASSETS/'cycle.gif') as im:self.assertEqual(im.n_frames,48);self.assertEqual(im.size,(920,600))
        tree=ET.parse(ASSETS/'nets-a4.svg');ns={'s':'http://www.w3.org/2000/svg'};self.assertEqual(len(tree.findall('.//s:rect',ns)),25)
        rows=list(csv.DictReader(io.StringIO((ASSETS/'pairs.csv').read_text())));self.assertEqual(len(rows),32)
        self.assertEqual(sum(int(row['total']) for row in rows),21312)
    def test_standalone_zip(self):
        with tempfile.TemporaryDirectory() as tmp:
            with zipfile.ZipFile(ASSETS/'table.zip') as z:z.extractall(tmp)
            r=subprocess.run([sys.executable,'-S',str(Path(tmp)/'verify.py'),str(Path(tmp)/'dice.json'),str(Path(tmp)/'audit.json')],capture_output=True,text=True);self.assertEqual(r.returncode,0,r.stderr);self.assertIn('VERIFIED',r.stdout)
    def test_regeneration(self):
        before={p.name:p.read_bytes() for p in ASSETS.iterdir()};subprocess.run([sys.executable,str(SAMPLE/'generate.py')],capture_output=True,check=True);self.assertEqual(before,{p.name:p.read_bytes() for p in ASSETS.iterdir()})
