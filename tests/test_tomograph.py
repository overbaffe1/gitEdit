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

ROOT=Path(__file__).resolve().parents[1]
SAMPLE=ROOT/'atlas/samples/tomograph'
spec=importlib.util.spec_from_file_location('reconstruct',SAMPLE/'reconstruct.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
sys.modules['reconstruct']=r
spec=importlib.util.spec_from_file_location('tomo_generate',SAMPLE/'generate.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
ASSETS=ROOT/'assets/tomograph'

class TomographTests(unittest.TestCase):
    def test_circle_integral(self):
        s=np.array([-.6,0,.6,1.1]);angles=np.array([0,.6,2.1])
        actual=g.analytic_projections(s,angles,[(2,0,0,1,1,0)])
        expected=4*np.sqrt(np.maximum(0,1-s*s))
        np.testing.assert_allclose(actual,np.tile(expected,(3,1)),atol=1e-14)

    def test_mass_and_geometry(self):
        s,a,p=r.load(ASSETS/'projections.csv')
        self.assertEqual(p.shape,(120,256));self.assertTrue(np.all(p>=0))
        mass=sum(v*math.pi*x*y for v,_,_,x,y,_ in g.ELLIPSES)
        np.testing.assert_allclose(np.trapezoid(p,s,axis=1),mass,rtol=.0007)
        self.assertGreaterEqual(g.phantom().min(),0)
        np.testing.assert_allclose(p,g.analytic_projections(s,a),atol=1e-7)

    def test_metrics_raw_and_missing_angles(self):
        s,a,p=r.load(ASSETS/'projections.csv');source=g.phantom()
        error=lambda arr:np.linalg.norm(arr-source)/np.linalg.norm(source)
        full=r.reconstruct(s,a,p);few=r.reconstruct(s,a,p,8)
        limited=r.backproject(s,a[:60],r.ramp_filter(p,s[1]-s[0])[:60],span=math.pi/2)
        facts=json.loads((ASSETS/'facts.json').read_text())
        self.assertAlmostEqual(error(full),facts['filtered_nrmse'],places=12)
        self.assertAlmostEqual(error(few),facts['eight_views_nrmse'],places=12)
        self.assertAlmostEqual(error(limited),facts['limited_90deg_nrmse'],places=12)
        self.assertLess(error(full),.11);self.assertGreater(error(few),.5);self.assertGreater(error(limited),.6)
        self.assertLess(full.min(),0) # no metric clipping

    def test_selections_and_input_rejection(self):
        for n in g.COUNTS:
            indices=r.selected(120,n);self.assertEqual(len(set(indices)),n)
            self.assertTrue(np.all(np.diff(np.r_[indices,120])==120//n))
        for n in (0,7,121,-1):
            with self.assertRaises(ValueError):r.selected(120,n)
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'bad.csv'
            for text in ('','bad,angle_0,angle_90\n','detector_s,angle_0,angle_90\n0,1,1\n1,nan,1\n2,1,1\n3,1,1\n',
                         'detector_s,angle_0,angle_90\n0,1,1\n1,1,1\n3,1,1\n4,1,1\n'):
                path.write_text(text)
                with self.assertRaises(ValueError):r.load(path)

    def test_reconstructor_is_independent(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp=Path(tmp);shutil.copy(SAMPLE/'reconstruct.py',tmp);shutil.copy(ASSETS/'projections.csv',tmp)
            subprocess.run([sys.executable,str(tmp/'reconstruct.py'),str(tmp/'projections.csv'),'--output',str(tmp/'out.png')],check=True,cwd=tmp,capture_output=True)
            self.assertEqual((tmp/'out.png').read_bytes(),(ASSETS/'reconstruction.png').read_bytes())

    def test_animation_zip_pins(self):
        with Image.open(ASSETS/'recover.gif') as image:self.assertEqual(image.n_frames,len(g.COUNTS));self.assertEqual(image.size,(1000,560))
        with zipfile.ZipFile(ASSETS/'bench.zip') as archive:
            self.assertEqual(archive.namelist(),['bench.html'])
            self.assertEqual(archive.read('bench.html'),(ASSETS/'bench.html').read_bytes())
        html=(ASSETS/'bench.html').read_text()
        self.assertNotIn('ELLIPSES',html);self.assertNotIn('source.png',html);self.assertNotIn('<script src',html)
        sources=json.loads((SAMPLE/'sources.json').read_text());self.assertEqual(len(sources),8)
        for source in sources:self.assertRegex(source['commit'],r'^[a-f0-9]{40}$');self.assertIn(source['commit'],source['url'])

    def test_regenerate_identical(self):
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run([sys.executable,str(SAMPLE/'generate.py'),'--output',tmp],check=True,capture_output=True)
            for path in ASSETS.iterdir():self.assertEqual(path.read_bytes(),(Path(tmp)/path.name).read_bytes(),path.name)

if __name__=='__main__':unittest.main()
