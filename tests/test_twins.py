import csv
import importlib.util
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1];SAMPLE=ROOT/'atlas/samples/twins';ASSETS=ROOT/'assets/twins'
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result);return result
c=module('twins_certify',SAMPLE/'certify.py');h=module('twins_heat',SAMPLE/'heat.py')
def pair():return [c.load(ASSETS/(name+'.csv')) for name in ('rook','shrikhande')]
def polynomial(roots):
    coefficients=[1]
    for root in roots:
        new=[0]*(len(coefficients)+1)
        for i,value in enumerate(coefficients):new[i]+=value;new[i+1]-=root*value
        coefficients=new
    return coefficients

class TwinsTests(unittest.TestCase):
    def test_exact_integer_certificates(self):
        for a in pair():
            report=c.certify(a);self.assertEqual(report['edges'],48);self.assertEqual(report['degrees'],[6]*16);self.assertTrue(report['connected']);self.assertTrue(report['A_squared_equals_4I_plus_2J'])
            self.assertEqual(report['adjacency_characteristic_descending'],polynomial([6]+[2]*6+[-2]*9))
            self.assertEqual(report['laplacian_characteristic_descending'],polynomial([0]+[4]*6+[8]*9))
            np.testing.assert_allclose(np.linalg.eigvalsh(a),[-2]*9+[2]*6+[6],atol=1e-12)
        self.assertEqual(c.characteristic([[0,1],[1,0]]),[1,0,-1])
        self.assertEqual(c.characteristic([[0,1,1],[1,0,1],[1,1,0]]),[1,0,-3,-2])

    def test_nonisomorphism_witness_and_relabelling(self):
        left,right=pair();self.assertEqual(len(c.cliques4(left)),8);self.assertEqual(c.cliques4(right),[])
        self.assertIn([0,1,2,3],c.cliques4(left));permutation=[(i*5+3)%16 for i in range(16)]
        for a in (left,right):
            relabelled=[[a[i][j] for j in permutation] for i in permutation]
            self.assertEqual(c.characteristic(relabelled),c.characteristic(a));self.assertEqual(len(c.cliques4(relabelled)),len(c.cliques4(a)))

    def test_heat_against_independent_eigendecomposition(self):
        for a in pair():
            a=np.array(a);laplacian=np.diag(a.sum(axis=1))-a;values,vectors=np.linalg.eigh(laplacian)
            for time in (0,.03,.25,.7,2):
                actual=h.kernel(a,time);expected=(vectors*np.exp(-time*values))@vectors.T
                np.testing.assert_allclose(actual,expected,atol=4e-15)
                np.testing.assert_allclose(actual,h.exact_regular_kernel(a,time),atol=2e-15)
                np.testing.assert_allclose(actual.sum(axis=0),np.ones(16),atol=2e-15)
                self.assertGreaterEqual(actual.min(),0)
                self.assertAlmostEqual(np.trace(actual),1+6*math.exp(-4*time)+9*math.exp(-8*time),places=12)
            np.testing.assert_allclose(h.kernel(a,.2)@h.kernel(a,.3),h.kernel(a,.5),atol=2e-15)

    def test_labelled_kernel_not_identical_despite_equal_trace(self):
        a,b=pair();ka,kb=h.kernel(a,.25),h.kernel(b,.25)
        self.assertAlmostEqual(float(np.trace(ka)),float(np.trace(kb)),places=14)
        self.assertGreater(np.linalg.norm(ka-kb),.1)
        # In this strongly regular pair even sorted heat values coincide for a single source.
        np.testing.assert_allclose(np.sort(ka[:,0]),np.sort(kb[:,0]),atol=1e-15)

    def test_edge_deletion_recomputes_generator(self):
        left,right=pair();right[0][1]=right[1][0]=0;report=c.certify(right)
        self.assertEqual(report['edges'],47);self.assertFalse(report['A_squared_equals_4I_plus_2J'])
        self.assertNotEqual(c.certify(left)['laplacian_characteristic_descending'],report['laplacian_characteristic_descending'])
        a=np.array(right);values,vectors=np.linalg.eigh(np.diag(a.sum(axis=1))-a)
        np.testing.assert_allclose(h.kernel(a,.25),(vectors*np.exp(-.25*values))@vectors.T,atol=2e-15)
        self.assertGreater(abs(np.trace(h.kernel(a,.25))-np.trace(h.kernel(left,.25))),.12)

    def test_csv_and_bad_inputs(self):
        a,b=pair();broken=[row[:] for row in b];broken[0][1]=broken[1][0]=0
        with (ASSETS/'heat-trace.csv').open() as f:rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),101)
        for row in rows:
            t=float(row['time']);self.assertAlmostEqual(float(row['shared_exact_formula']),np.trace(h.kernel(a,t)),places=12)
            self.assertAlmostEqual(float(row['deleted_edge_trace']),np.trace(h.kernel(broken,t)),places=12)
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'bad.csv'
            for text in ('','vertex,0,1\n0,1,1\n1,1,0\n','vertex,0,1\n0,0,1\n1,0,0\n','vertex,0\n0,0.0\n'):
                path.write_text(text)
                with self.assertRaises(ValueError):c.load(path)
        with self.assertRaises(ValueError):h.kernel(a,-1)
        with self.assertRaises(ValueError):h.kernel(a,float('nan'))

    def test_checker_without_generator_or_dependencies(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp=Path(tmp);shutil.copy(SAMPLE/'certify.py',tmp);shutil.copy(ASSETS/'shrikhande.csv',tmp)
            completed=subprocess.run([sys.executable,'-I',str(tmp/'certify.py'),str(tmp/'shrikhande.csv')],cwd=tmp,capture_output=True,text=True,check=True)
            self.assertEqual(json.loads(completed.stdout),c.certify(pair()[1]))

    def test_containers_research_and_reproducibility(self):
        records=json.loads((SAMPLE/'sources.json').read_text());self.assertEqual(len(records),8)
        for record in records:self.assertRegex(record['commit'],r'^[a-f0-9]{40}$');self.assertIn(record['commit'],record['url'])
        self.assertEqual(sum('source_file' in r for r in records),3)
        with zipfile.ZipFile(ASSETS/'bench.zip') as z:self.assertEqual(z.namelist(),['bench.html']);self.assertEqual(z.read('bench.html'),(ASSETS/'bench.html').read_bytes())
        with Image.open(ASSETS/'twins.gif') as im:self.assertEqual(im.n_frames,32);self.assertEqual(im.size,(1000,730))
        html=(ASSETS/'bench.html').read_text();self.assertNotIn('<script src',html);self.assertNotIn('data:image',html);self.assertNotIn('requestAnimationFrame',html)
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run([sys.executable,str(SAMPLE/'generate.py'),'--output',tmp],capture_output=True,check=True)
            for path in ASSETS.iterdir():self.assertEqual(path.read_bytes(),(Path(tmp)/path.name).read_bytes(),path.name)

if __name__=='__main__':unittest.main()
