import copy
import csv
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];SAMPLE=ROOT/'atlas/samples/domino';ASSETS=ROOT/'assets/domino'
def module(name):
    spec=importlib.util.spec_from_file_location('domino_'+name,SAMPLE/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
c=module('construct');v=module('verify')

def maximum_matching(holes):
    # Independent generic bipartite augmenting-path oracle, no cycle construction.
    remaining=set(range(64))-set(holes);left=[i for i in remaining if (i//8+i%8)%2==0];matched={}
    neighbors={i:[j for j in remaining if abs(i//8-j//8)+abs(i%8-j%8)==1] for i in left}
    def augment(i,seen):
        for j in neighbors[i]:
            if j in seen:continue
            seen.add(j)
            if j not in matched or augment(matched[j],seen):matched[j]=i;return True
        return False
    return sum(augment(i,set()) for i in left)

class DominoTests(unittest.TestCase):
    def test_all_pairs(self):
        tileable=impossible=placements=0
        for holes in combinations(range(64),2):
            cert=c.construct(list(holes));r=v.verify(cert)
            if r['tileable']:tileable+=1;placements+=r['dominoes'];self.assertEqual(r['remaining_colors'],[31,31])
            else:impossible+=1;self.assertEqual(sorted(r['remaining_colors']),[30,32])
        self.assertEqual((tileable,impossible,placements),(1024,992,31744))
    def test_independent_matching_oracle(self):
        for holes in combinations(range(64),2):self.assertEqual(maximum_matching(holes)==31,c.construct(list(holes))['tileable'])
    def test_cycle_and_chain_parities(self):
        route=c.cycle();self.assertEqual(route,json.loads((ASSETS/'cycle.json').read_text()));self.assertTrue(v.check_cycle(route)['cycle_verified']);self.assertTrue(v.check_cycle(route[::-1])['cycle_verified'])
        for h in combinations(range(64),2):
            parts=c.paths(list(h),route);self.assertEqual(sum(map(len,parts)),62);self.assertEqual(len(parts[0])%2,c.color(h[0])==c.color(h[1]));self.assertEqual(sorted(parts[0]+parts[1]),[i for i in range(64) if i not in h])
    def test_adjacent_holes_and_order(self):
        for a,b in [(0,1),(0,8),(0,62),(0,63)]:self.assertEqual(c.construct([a,b]),c.construct([b,a]))
        self.assertEqual([len(x) for x in c.paths([0,1],c.cycle())],[0,62]);self.assertTrue(v.verify(c.construct([0,1]))['tileable'])
        self.assertEqual(c.construct([0,62]),json.loads((ASSETS/'possible.json').read_text()));self.assertEqual(c.construct([0,63]),json.loads((ASSETS/'impossible.json').read_text()))
    def test_tamper(self):
        cert=c.construct([0,62])
        for field,value in [('remaining_colors',[30,32]),('remaining_colors',[True,31]),('tileable',False),('dominoes',cert['dominoes'][:-1]),('holes',[0,63])]:
            bad=copy.deepcopy(cert);bad[field]=value
            with self.assertRaises(ValueError):v.verify(bad)
        for pair in [[0,1],[1,1],[1,63],[True,2]]:
            bad=copy.deepcopy(cert);bad['dominoes'][0]=pair
            with self.assertRaises(ValueError):v.verify(bad)
        route=c.cycle();route[0],route[1]=route[1],route[0]
        with self.assertRaises(ValueError):v.check_cycle(route)
    def test_strict_inputs(self):
        for holes in [None,[],[0],[0,0],[0,64],[-1,0],[True,1],[0.0,1],'01']:
            with self.assertRaises(ValueError):c.construct(holes)
            bad=c.construct([0,62]);bad['holes']=holes
            with self.assertRaises(ValueError):v.verify(bad)
    def test_standalone_assets(self):
        with Image.open(ASSETS/'tiling.gif') as im:self.assertEqual(im.n_frames,32);self.assertEqual(im.size,(1000,660))
        ns={'s':'http://www.w3.org/2000/svg'};self.assertEqual(len(ET.parse(ASSETS/'pieces-a4.svg').findall('.//s:rect',ns)),32)
        with (ASSETS/'pairs.csv').open() as f:self.assertEqual(len(list(csv.DictReader(f))),2016)
        with tempfile.TemporaryDirectory() as tmp:
            with zipfile.ZipFile(ASSETS/'bench.zip') as z:z.extractall(tmp)
            for name in ['possible.json','impossible.json']:
                result=subprocess.run([sys.executable,'-S',str(Path(tmp)/'verify.py'),str(Path(tmp)/name),'--cycle',str(Path(tmp)/'cycle.json')],capture_output=True,text=True);self.assertEqual(result.returncode,0,result.stderr);self.assertTrue(json.loads(result.stdout)['certificate_verified'])
    def test_regeneration(self):
        before={p.name:p.read_bytes() for p in ASSETS.iterdir()};subprocess.run([sys.executable,str(SAMPLE/'generate.py')],capture_output=True,check=True);self.assertEqual(before,{p.name:p.read_bytes() for p in ASSETS.iterdir()})
