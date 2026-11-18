import csv
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

ROOT=Path(__file__).resolve().parents[1];SAMPLE=ROOT/'atlas/samples/metamer';ASSETS=ROOT/'assets/metamer'
def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
m=load_module('metamer_model',SAMPLE/'model.py');sys.modules['model']=m
measure=load_module('metamer_measure',SAMPLE/'measure.py')

class MetamerTests(unittest.TestCase):
    def test_standard_tables_and_attribution(self):
        s=m.load();self.assertEqual(s['wavelength_nm'],list(range(380,781,5)))
        self.assertEqual(len(s['cmf']),81);i=s['wavelength_nm'].index(555)
        self.assertEqual(s['cmf'][i][1],1.0)
        i=s['wavelength_nm'].index(560);self.assertEqual(s['D65'][i],100);self.assertEqual(s['A'][i],100)
        self.assertIn('Copyright 2013 Colour Developers',(SAMPLE/'COLOUR-LICENSE.txt').read_text())
        self.assertEqual((SAMPLE/'COLOUR-LICENSE.txt').read_bytes(),(ASSETS/'COLOUR-LICENSE.txt').read_bytes())

    def test_daylight_match_before_display_rounding(self):
        s,p=measure.load_csv(ASSETS/'spectra.csv');self.assertGreaterEqual(np.min(p),0);self.assertLessEqual(np.max(p),1)
        self.assertGreater(np.linalg.norm(np.array(p[0])-p[1]),2)
        result=m.evaluate(s,p,0);np.testing.assert_allclose(result['xyz'][0],result['xyz'][1],atol=3e-14)
        self.assertLess(result['delta_e76'],1e-10);self.assertEqual(result['rgb8'],[[188,188,188]]*2)

    def test_illuminant_mismatch_and_unclipped_path(self):
        s,p=measure.load_csv(ASSETS/'spectra.csv');facts=json.loads((ASSETS/'facts.json').read_text())
        result=m.evaluate(s,p,1);self.assertGreater(result['delta_e76'],40)
        self.assertAlmostEqual(result['delta_e76'],facts['illuminant_A']['delta_e76'],places=11)
        self.assertEqual(result['rgb8'],[[218,172,196],[148,202,178]])
        for t in np.linspace(0,1,101):self.assertFalse(m.evaluate(s,p,float(t))['gamut_clipped'])

    def test_white_and_neutral_adaptation(self):
        s=m.load()
        for key in ('D65','A'):
            op=m.operator(s,s[key]);white=op@np.ones(81);cat=m.adaptation(white)
            np.testing.assert_allclose(cat@white,m.D65_WHITE,atol=1e-14)
            np.testing.assert_allclose(cat@(op@np.full(81,.5)),m.D65_WHITE*.5,atol=1e-14)
        np.testing.assert_allclose(m.lab(m.D65_WHITE),[100,0,0],atol=1e-12)
        np.testing.assert_allclose(m.srgb(np.array([0,.0031308,1])),[0,.040449936,1],atol=1e-12)

    def test_illuminant_scale_invariance_and_input_rejection(self):
        s=m.load();a=np.array(s['A']);np.testing.assert_allclose(m.operator(s,a),m.operator(s,a*12),atol=1e-14)
        for light in (np.zeros(81),-a,np.full(81,np.nan),a[:4]):
            with self.assertRaises(ValueError):m.operator(s,light)
        with self.assertRaises(ValueError):m.evaluate(s,[np.ones(81)]*2,1.1)

    def test_published_measurement_table(self):
        s,p=measure.load_csv(ASSETS/'spectra.csv')
        with (ASSETS/'measurements.csv').open() as f:rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),202)
        for row in rows:
            r=m.evaluate(s,p,float(row['mix_A']),row['adapt']=='True')
            self.assertAlmostEqual(r['delta_e76'],float(row['delta_e76']),places=10)
            self.assertEqual(r['rgb8'][0],[int(row[key]) for key in ('A_R','A_G','A_B')])

    def test_csv_only_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp=Path(tmp)
            for name in ('model.py','measure.py'):shutil.copy(SAMPLE/name,tmp/name)
            shutil.copy(ASSETS/'spectra.csv',tmp/'spectra.csv')
            result=subprocess.run([sys.executable,str(tmp/'measure.py'),str(tmp/'spectra.csv'),'--mix','1'],capture_output=True,text=True,check=True,cwd=tmp)
            self.assertEqual(json.loads(result.stdout)['rgb8'],[[218,172,196],[148,202,178]])
            (tmp/'spectra.csv').write_text('bad\n')
            result=subprocess.run([sys.executable,str(tmp/'measure.py'),str(tmp/'spectra.csv')],capture_output=True,text=True,cwd=tmp)
            self.assertNotEqual(result.returncode,0)

    def test_containers_and_research_scope(self):
        sources=json.loads((SAMPLE/'sources.json').read_text());self.assertEqual(len(sources),8)
        for record in sources:self.assertRegex(record['commit'],r'^[a-f0-9]{40}$');self.assertIn(record['commit'],record['url'])
        with zipfile.ZipFile(ASSETS/'bench.zip') as archive:
            self.assertEqual(set(archive.namelist()),{'bench.html','COLOUR-LICENSE.txt'})
            for name in archive.namelist():self.assertEqual(archive.read(name),(ASSETS/name).read_bytes())
        with Image.open(ASSETS/'illuminants.gif') as im:self.assertEqual(im.n_frames,40);self.assertEqual(im.size,(1000,680))
        html=(ASSETS/'bench.html').read_text();self.assertNotIn('<script src',html);self.assertNotIn('data:image',html);self.assertNotIn('requestAnimationFrame',html)

    def test_identical_regeneration(self):
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run([sys.executable,str(SAMPLE/'generate.py'),'--output',tmp],check=True,capture_output=True)
            for path in ASSETS.iterdir():self.assertEqual(path.read_bytes(),(Path(tmp)/path.name).read_bytes(),path.name)

if __name__=='__main__':unittest.main()
