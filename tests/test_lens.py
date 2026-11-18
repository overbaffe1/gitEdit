"""Analytic, raster and packaging checks for an explicitly limited thin-lens model."""
import csv
import importlib.util
import io
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'assets/lens'
GEN=ROOT/'atlas/samples/lens/generate.py'
spec=importlib.util.spec_from_file_location('lens',GEN)
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)


class Lens(unittest.TestCase):
    def test_mapping_matches_scalar_point_mass_formula_and_handles_singularity(self):
        for x,y,e in ((.7,.4,1),(1.8,-.2,.75),(-.32,1.2,1.3)):
            bx,by=gen.lens_map(x,y,e)
            self.assertAlmostEqual(float(bx),x-e*e*x/(x*x+y*y))
            self.assertAlmostEqual(float(by),y-e*e*y/(x*x+y*y))
        bx,by=gen.lens_map(0,0,1)
        self.assertTrue(np.isnan(bx));self.assertTrue(np.isnan(by))
        with self.assertRaises(ValueError):gen.lens_map(1,1,-1)
        with self.assertRaises(ValueError):gen.point_images(0,0)
        for size in (384,192):
            x,y=gen.coordinates(size)
            self.assertTrue(np.all(x*x+y*y>0))

    def test_both_analytic_images_map_to_same_source_with_opposite_parity(self):
        for beta in ((.55,0),(.12,.37),(-.8,.2)):
            for e in (.3,1,1.3):
                images=gen.point_images(*beta,e)
                self.assertEqual(len(images),2)
                for index,(x,y) in enumerate(images):
                    bx,by=gen.lens_map(x,y,e)
                    np.testing.assert_allclose([bx,by],beta,atol=1e-13)
                    determinant=1-e**4/(x*x+y*y)**2
                    self.assertGreater(determinant,0) if index==0 else self.assertLess(determinant,0)
                self.assertAlmostEqual(images[0][0]*images[1][1]-images[0][1]*images[1][0],0,places=12)
        rows=list(csv.DictReader(io.StringIO((ART/'images.csv').read_text())))
        self.assertEqual(len(rows),8)
        for row in rows:
            x=float(row['theta_x']);y=float(row['theta_y']);b=float(row['source_beta_x'])
            self.assertAlmostEqual(x-x/(x*x+y*y),b,places=12)
            self.assertAlmostEqual(float(row['mapped_beta_x']),b,places=12)
            self.assertEqual(float(row['mapped_beta_y']),0)

    def test_entire_einstein_circle_maps_to_origin_and_is_radially_critical(self):
        for e in (.3,1,1.3):
            angles=np.linspace(0,2*np.pi,256,endpoint=False)
            bx,by=gen.lens_map(e*np.cos(angles),e*np.sin(angles),e)
            np.testing.assert_allclose(bx,0,atol=1e-14)
            np.testing.assert_allclose(by,0,atol=1e-14)
            # Independent finite-difference Jacobian determinant on the circle.
            h=1e-5;x=e*.8;y=e*.6
            xp=np.array(gen.lens_map(x+h,y,e));xm=np.array(gen.lens_map(x-h,y,e))
            yp=np.array(gen.lens_map(x,y+h,e));ym=np.array(gen.lens_map(x,y-h,e))
            matrix=np.column_stack(((xp-xm)/(2*h),(yp-ym)/(2*h)))
            self.assertAlmostEqual(float(np.linalg.det(matrix)),0,places=7)

    def test_zero_lens_is_pixel_identity_not_a_different_scene(self):
        for offset in (-.85,0,.71):
            source,lensed=gen.render(64,offset,0)
            self.assertTrue(np.array_equal(source,lensed))
            same_source,_=gen.render(64,offset,1)
            self.assertTrue(np.array_equal(source,same_source))
        x,y=gen.coordinates(40);bx,by=gen.lens_map(x,y,0)
        self.assertTrue(np.array_equal(x,bx));self.assertTrue(np.array_equal(y,by))

    def test_exported_pngs_are_same_surface_brightness_sampled_at_lens_coordinates(self):
        x,y=gen.coordinates(384);bx,by=gen.lens_map(x,y)
        expected=gen.encode_rgb(gen.background(bx,by)+gen.galaxy(bx,by,0))
        with Image.open(ART/'ring.png') as image:
            self.assertEqual(image.size,(384,384));self.assertTrue(np.array_equal(np.array(image),expected))
        for size,a,b in ((384,'source.png','ring.png'),(192,'bench-source.png','bench-ring.png')):
            source,lensed=gen.render(size)
            for name,pixels in ((a,source),(b,lensed)):
                with Image.open(ART/name) as image:self.assertTrue(np.array_equal(np.array(image),pixels))

    def test_frames_motion_and_still_poster_wiring(self):
        info=json.loads((ART/'facts.json').read_text())
        self.assertEqual(len(info['source_offsets']),32)
        self.assertEqual(info['source_offsets'][0],0)
        for i,offset in enumerate(info['source_offsets']):self.assertAlmostEqual(offset,.85*math.sin(2*math.pi*i/32))
        with Image.open(ART/'poster.png') as poster,Image.open(ART/'crossing.gif') as gif:
            self.assertEqual(poster.size,(1000,600));self.assertEqual(gif.n_frames,32)
            self.assertEqual(gif.info['duration'],140);self.assertEqual(gif.info['loop'],0)
            difference=np.abs(np.array(poster).astype(float)-np.array(gif.convert('RGB')).astype(float))
            self.assertLess(float(difference.mean()),2)
        text=(ROOT/'README.md').read_text().split('## Одна галактика',1)[1].split('\n## ',1)[0]
        self.assertIn('prefers-reduced-motion: reduce',text)
        self.assertIn('srcset="assets/lens/poster.png"',text)
        self.assertIn('href="assets/lens/ring.png"',text)

    def test_live_html_has_no_prerendered_frames_and_research_scope_is_pinned(self):
        with zipfile.ZipFile(ART/'bench.zip') as archive:
            self.assertEqual(archive.namelist(),['bench.html'])
            self.assertEqual(archive.read('bench.html'),(ART/'bench.html').read_bytes())
            self.assertEqual(archive.getinfo('bench.html').date_time,(2026,11,18,0,0,0))
        html=(ART/'bench.html').read_text()
        self.assertNotRegex(html,r'https?://|fetch\(|XMLHttpRequest|\.png|\.gif|data:image|localStorage|setInterval|requestAnimationFrame')
        self.assertIn('createImageData',html);self.assertIn('aria-live="polite"',html)
        rows=json.loads((ROOT/'atlas/samples/lens/sources.json').read_text())
        self.assertEqual(len(rows),8)
        self.assertEqual(sum('source_file' in row for row in rows),3)
        for row in rows:
            self.assertEqual(row['status'],'README screening')
            self.assertRegex(row['commit'],r'^[a-f0-9]{40}$')
            self.assertIn('/blob/'+row['commit']+'/',row['url'])
            if 'source_file' in row:self.assertIn('/blob/'+row['commit']+'/',row['source_url'])

    def test_clean_reprint_is_byte_identical(self):
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run([sys.executable,str(GEN),'--output',tmp],check=True,capture_output=True)
            self.assertEqual({p.name for p in Path(tmp).iterdir()},{p.name for p in ART.iterdir()})
            for file in ART.iterdir():self.assertEqual(file.read_bytes(),(Path(tmp)/file.name).read_bytes(),file.name)
