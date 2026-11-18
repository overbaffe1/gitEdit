import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1];SAMPLE=ROOT/'atlas/samples/echo';ASSETS=ROOT/'assets/echo'
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result);return result
w=module('echo_wave_local',SAMPLE/'wave_local.py');sys.modules['wave_local']=w
g=module('echo_generate',SAMPLE/'generate.py');resume=module('echo_resume',SAMPLE/'resume.py')

class EchoTests(unittest.TestCase):
    def test_operator_symmetry_and_walls(self):
        u,v,fixed=g.initial();rng=np.random.default_rng(82);a=rng.normal(size=u.shape);b=rng.normal(size=u.shape);a[fixed]=b[fixed]=0
        self.assertAlmostEqual(float(np.sum(a*w.laplacian(b,fixed))),float(np.sum(b*w.laplacian(a,fixed))),places=10)
        self.assertLess(float(np.sum(a*w.laplacian(a,fixed))),0)
        u,v=w.step(a,b,fixed);self.assertTrue(np.all(u[fixed]==0));self.assertTrue(np.all(v[fixed]==0))

    def test_one_step_time_symmetry(self):
        u,v,fixed=g.initial();rng=np.random.default_rng(7);v=rng.normal(size=v.shape);v[fixed]=0
        a,b=w.step(u,v,fixed);back,velocity=w.step(a,b,fixed,dt=-w.DT)
        np.testing.assert_allclose(back,u,atol=1e-15);np.testing.assert_allclose(velocity,v,atol=1e-15)
        back,velocity=w.step(a,-b,fixed);np.testing.assert_allclose(back,u,atol=1e-15);np.testing.assert_allclose(velocity,-v,atol=1e-15)

    def test_discrete_eigenmode(self):
        n=25;y,x=np.mgrid[:n,:n];u=np.sin(2*np.pi*x/(n-1))*np.sin(3*np.pi*y/(n-1));v=np.zeros_like(u)
        fixed=(x==0)|(x==n-1)|(y==0)|(y==n-1);u[fixed]=0;source=u.copy()
        eigenvalue=4*np.sin(np.pi/(n-1))**2+4*np.sin(3*np.pi/(2*(n-1)))**2
        angle=np.arccos(1-.5*w.DT*w.DT*eigenvalue)
        for _ in range(70):u,v=w.step(u,v,fixed)
        np.testing.assert_allclose(u,source*np.cos(70*angle),atol=1e-13)

    def test_checkpoint_only_and_metrics(self):
        source,_,fixed=g.initial();facts=json.loads((ASSETS/'facts.json').read_text())
        for mode in ('reverse','zero','keep'):
            u,v=resume.resume(ASSETS/'checkpoint.npz',mode)
            self.assertAlmostEqual(np.linalg.norm(u-source)/np.linalg.norm(source),facts['branches'][mode]['relative_displacement_error'],places=12)
            np.testing.assert_array_equal(np.asarray(g.field(u,fixed)),np.asarray(Image.open(ASSETS/(mode+'.png'))))
        self.assertLess(facts['branches']['reverse']['relative_displacement_error'],1e-12)
        self.assertLess(facts['max_relative_energy_drift'],.007)
        self.assertLess(facts['max_relative_modified_energy_drift'],1e-12)

    def test_zero_velocity_is_half_forward_plus_half_reverse(self):
        backward,_=resume.resume(ASSETS/'checkpoint.npz','reverse');forward,_=resume.resume(ASSETS/'checkpoint.npz','keep');zero,_=resume.resume(ASSETS/'checkpoint.npz','zero')
        np.testing.assert_allclose(zero,.5*(backward+forward),atol=2e-15)
        # Thus losing velocities leaves partial refocusing: not a claim of total destruction.

    def test_standalone_resume_without_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp=Path(tmp)
            for name in ('resume.py','wave_local.py'):shutil.copy(SAMPLE/name,tmp/name)
            shutil.copy(ASSETS/'checkpoint.npz',tmp/'checkpoint.npz')
            subprocess.run([sys.executable,str(tmp/'resume.py'),str(tmp/'checkpoint.npz'),'--output',str(tmp/'out.npz')],check=True,cwd=tmp,capture_output=True)
            with np.load(tmp/'out.npz') as data:
                source,_,_=g.initial();np.testing.assert_allclose(data['u'],source,atol=2e-14)

    def test_research_and_container(self):
        records=json.loads((SAMPLE/'sources.json').read_text());self.assertEqual(len(records),8);self.assertEqual(sum('source_file' in r for r in records),3)
        for row in records:self.assertRegex(row['commit'],r'^[a-f0-9]{40}$');self.assertIn(row['commit'],row['url'])
        with Image.open(ASSETS/'return.gif') as im:self.assertEqual(im.n_frames,61);self.assertEqual(im.size,(1000,610))
        with zipfile.ZipFile(ASSETS/'bench.zip') as z:self.assertEqual(z.namelist(),['bench.html']);self.assertEqual(z.read('bench.html'),(ASSETS/'bench.html').read_bytes())
        html=(ASSETS/'bench.html').read_text();self.assertNotIn('<script src',html);self.assertNotIn('requestAnimationFrame',html);self.assertNotIn('setInterval',html);self.assertNotIn('data:image',html)

    def test_byte_identical_generation(self):
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run([sys.executable,str(SAMPLE/'generate.py'),'--output',tmp],check=True,capture_output=True)
            for file in ASSETS.iterdir():self.assertEqual(file.read_bytes(),(Path(tmp)/file.name).read_bytes(),file.name)

if __name__=='__main__':unittest.main()
