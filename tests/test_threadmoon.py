"""Verify the physical route, not just the presence of a decorative image."""
import csv
import importlib.util
import json
import io
import math
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

import numpy as np
from PIL import Image
import fitz

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'assets/threadmoon'
GEN=ROOT/'atlas/samples/threadmoon/generate.py'
spec=importlib.util.spec_from_file_location('threadmoon',GEN)
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)


class ThreadMoon(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.facts=json.loads((ART/'facts.json').read_text())
        cls.route=cls.facts['route']

    def test_one_continuous_route_and_real_csv(self):
        rows=list(csv.DictReader(io.StringIO((ART/'route.csv').read_text())))
        self.assertEqual(len(rows),459)
        self.assertEqual(self.route[0],0)
        self.assertEqual(len(self.route),460)
        for i,row in enumerate(rows,1):
            self.assertEqual(int(row['step']),i)
            self.assertEqual(int(row['from_pin']),self.route[i-1])
            self.assertEqual(int(row['to_pin']),self.route[i])
            self.assertTrue(gen.valid(self.route[i-1],self.route[i]))
            self.assertTrue(0<=self.route[i]<144)
        self.assertEqual(self.facts['stop'],'no positive local gain')

    def test_every_transition_reduces_actual_squared_error(self):
        points=gen.nails();target=gen.target().ravel();density=np.zeros(target.size)
        self.assertAlmostEqual(float(np.sum(target**2)),self.facts['initial_sse'])
        previous=self.facts['initial_sse']
        for i,(a,b) in enumerate(zip(self.route,self.route[1:]),1):
            ix=gen.chord(points[a],points[b])
            self.assertEqual(len(ix),len(set(ix)))
            density[ix]=np.minimum(1,density[ix]+gen.STRENGTH)
            current=float(np.sum((target-density)**2))
            self.assertLess(current,previous)
            self.assertAlmostEqual(current,self.facts['sse_by_step'][i],places=8)
            previous=current
        self.assertAlmostEqual(previous,self.facts['final_sse'])
        self.assertLess(previous,.35*self.facts['initial_sse'])
        self.assertTrue(np.array_equal(density.reshape(gen.SIZE,gen.SIZE),gen.reconstruct(self.route)))

    def test_local_stop_is_honest_no_teleport(self):
        points=gen.nails();density=gen.reconstruct(self.route).ravel();target=gen.target().ravel();a=self.route[-1]
        for b in range(gen.COUNT):
            if not gen.valid(a,b):continue
            ix=gen.chord(points[a],points[b]);old=density[ix];new=np.minimum(1,old+gen.STRENGTH)
            gain=float(np.sum((target[ix]-old)**2-(target[ix]-new)**2))
            self.assertLessEqual(gain,1e-12)

    def test_lengths_use_exact_physical_circle_not_pixel_rounding(self):
        rows=list(csv.DictReader(io.StringIO((ART/'route.csv').read_text())));total=0
        for row,a,b in zip(rows,self.route,self.route[1:]):
            length=160*abs(math.sin(math.pi*(a-b)/144));total+=length/1000
            self.assertAlmostEqual(float(row['chord_mm']),length,places=5)
            self.assertAlmostEqual(float(row['cumulative_m']),total,places=5)
        self.assertAlmostEqual(total,self.facts['ideal_chord_length_m'])
        self.assertAlmostEqual(total,65.37152156998579)
        points=gen.nails()
        self.assertEqual(len(set(points)),144)
        self.assertEqual(points[0],(96,8))
        for a in range(144):
            b=(a+65)%144
            self.assertTrue(np.array_equal(gen.chord(points[a],points[b]),gen.chord(points[b],points[a])))

    def test_final_image_is_full_route_and_gif_final_is_same_model(self):
        expected=gen.plate(gen.reconstruct(self.route),459,459)
        with Image.open(ART/'moon.png') as source:
            actual=source.convert('RGB')
        self.assertTrue(np.array_equal(np.array(actual),np.array(expected)))
        gif=Image.open(ART/'winding.gif')
        self.assertEqual(gif.n_frames,36)
        self.assertEqual(gif.info['loop'],0)
        gif.seek(35)
        self.assertEqual(gif.info['duration'],2400)
        last=gif.convert('RGB');gif.close()
        final=gen.plate(gen.reconstruct(self.route),459,459,512)
        delta=np.abs(np.array(last).astype(float)-np.array(final).astype(float))
        self.assertLess(float(delta.mean()),1.5)
        self.assertIn('prefers-reduced-motion: reduce',(ROOT/'README.md').read_text())
        self.assertIn('srcset="assets/threadmoon/moon.png"',(ROOT/'README.md').read_text())

    def test_pdf_is_true_a4_numbered_template_with_scale(self):
        with fitz.open(ART/'pins-a4.pdf') as pdf:
            self.assertEqual(len(pdf),1)
            page=pdf[0]
            self.assertAlmostEqual(page.rect.width,210*72/25.4,places=3)
            self.assertAlmostEqual(page.rect.height,297*72/25.4,places=3)
            text=page.get_text()
            for i in range(144):self.assertIn(f'{i:03}',text)
            self.assertIn('50 mm',text)
            self.assertIn('160 mm',text)
            circles=[p for p in page.get_drawings() if abs(p['rect'].width-160*72/25.4)<.01 and abs(p['rect'].height-160*72/25.4)<.01]
            self.assertEqual(len(circles),1)

    def test_counter_contains_same_route_no_network_or_hidden_playback(self):
        html=(ART/'counter.html').read_text()
        data=json.loads(re.search(r'const data=(.*?);const slider',html).group(1))
        self.assertEqual(data['route'],self.route)
        self.assertEqual(data['pins'],[list(p) for p in gen.nails()])
        self.assertIn('aria-live="polite"',html)
        self.assertIn('type="range"',html)
        self.assertNotRegex(html,r'fetch\(|XMLHttpRequest|https?://|setInterval|requestAnimationFrame|localStorage|<script[^>]+src')
        sources=json.loads((ROOT/'atlas/samples/threadmoon/sources.json').read_text())
        self.assertEqual(len(sources),8)
        self.assertEqual(sum('source_file' in s for s in sources),2)
        for row in sources:
            self.assertRegex(row['commit'],r'^[a-f0-9]{40}$')
            self.assertIn('/blob/'+row['commit']+'/',row['url'])
            if 'source_file' in row:self.assertIn('/blob/'+row['commit']+'/',row['source_url'])

    def test_clean_reprint_all_deliverables_byte_identical(self):
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run([sys.executable,str(GEN),'--output',tmp],check=True,capture_output=True)
            self.assertEqual({p.name for p in Path(tmp).iterdir()},{p.name for p in ART.iterdir()})
            for source in ART.iterdir():
                self.assertEqual(source.read_bytes(),(Path(tmp)/source.name).read_bytes(),source.name)
