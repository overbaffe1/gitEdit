import csv
import importlib.util
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];SAMPLE=ROOT/'atlas/samples/puzzle';ASSETS=ROOT/'assets/puzzle'
def module(name):
    spec=importlib.util.spec_from_file_location('puzzle_'+name,SAMPLE/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
c=module('core');v=module('verify')
class PuzzleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.table=(ASSETS/'distances.bin').read_bytes()
    def test_independent_full_certificate(self):
        actual=v.check(self.table);expected=json.loads((ASSETS/'certificate.json').read_text());expected.pop('witness');self.assertEqual(actual,expected);self.assertEqual(actual['directed_edges_checked'],483840);self.assertEqual(actual['histogram']['31'],2)
    def test_all_ranks_and_parity(self):
        for index,board in enumerate(itertools.permutations(range(9))):
            self.assertEqual(c.rank(board),index);self.assertEqual(self.table[index]==255,bool(c.parity(board)))
    def test_route_legal_and_shortest(self):
        route=json.loads((ASSETS/'route.json').read_text());self.assertEqual(route[0],list(c.HARD));self.assertEqual(route[-1],list(c.GOAL));self.assertEqual(len(route),32)
        for i,board in enumerate(route):
            self.assertEqual(self.table[c.rank(board)],31-i)
            if i:self.assertIn(tuple(board),list(c.neighbors(tuple(route[i-1]))))
        self.assertEqual(c.path(c.HARD,self.table),list(map(tuple,route)))
        swapped=tuple(2 if x==1 else 1 if x==2 else x for x in c.HARD)
        with self.assertRaises(ValueError):c.path(swapped,self.table)
    def test_small_ball_against_independent_breadth_search(self):
        current={c.GOAL};seen=set(current)
        for depth in range(10):
            self.assertTrue(all(self.table[c.rank(board)]==depth for board in current));following=set()
            for board in current:
                z=board.index(0)
                for j in range(9):
                    if abs(j//3-z//3)+abs(j%3-z%3)!=1:continue
                    b=list(board);b[z],b[j]=b[j],b[z];b=tuple(b)
                    if b not in seen:following.add(b)
            seen|=following;current=following
    def test_tamper(self):
        for index,value in [(c.rank(c.GOAL),1),(0,0),(c.rank(c.HARD),29),(1,0)]:
            bad=bytearray(self.table);bad[index]=value
            with self.assertRaises(ValueError):v.check(bad)
        with self.assertRaises(ValueError):v.check(self.table[:-1])
    def test_strict_board(self):
        for board in [[],list(range(8)),[0]*9,[False]+list(range(1,9)),[0.0]+list(range(1,9)),'123456780']:
            with self.assertRaises(ValueError):c.validate(board)
    def test_assets_and_standalone_zip(self):
        with Image.open(ASSETS/'route.gif') as im:self.assertEqual(im.n_frames,94);self.assertEqual(im.size,(920,560))
        with (ASSETS/'route.csv').open() as f:self.assertEqual(len(list(csv.DictReader(f))),32)
        with tempfile.TemporaryDirectory() as tmp:
            with zipfile.ZipFile(ASSETS/'bench.zip') as z:z.extractall(tmp)
            result=subprocess.run([sys.executable,'-S',str(Path(tmp)/'verify.py'),str(Path(tmp)/'distances.bin')],capture_output=True,text=True);self.assertEqual(result.returncode,0,result.stderr);self.assertTrue(json.loads(result.stdout)['exact_distances_proved'])
    def test_regeneration(self):
        before={p.name:p.read_bytes() for p in ASSETS.iterdir()};subprocess.run([sys.executable,str(SAMPLE/'generate.py')],capture_output=True,check=True);self.assertEqual(before,{p.name:p.read_bytes() for p in ASSETS.iterdir()})
