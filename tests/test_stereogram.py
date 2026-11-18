"""Check binocular correspondences and a recovery that cannot see the source map."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'assets/stereogram'
GEN=ROOT/'atlas/samples/stereogram/generate.py'
spec=importlib.util.spec_from_file_location('stereogram',GEN)
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)


class Stereogram(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.facts=json.loads((ART/'facts.json').read_text())
        with Image.open(ART/'stereogram.png') as image:cls.pixels=np.array(image)

    def test_depth_is_original_analytic_geometry(self):
        depth=gen.depthmap()
        self.assertEqual(depth.shape,(480,960))
        self.assertTrue(np.all((depth>=0)&(depth<=1)))
        self.assertAlmostEqual(depth[245,465],0)  # open hole, not a solid disk
        self.assertAlmostEqual(depth[245,589],.9)
        self.assertAlmostEqual(depth[129,688],.75)
        self.assertEqual(depth[0,0],0)
        with Image.open(ART/'depth.png') as image:published=np.array(image)
        self.assertTrue(np.array_equal(published,np.uint8(np.round(depth*255))))
        self.assertEqual(int(gen.separation(0)),80)
        self.assertEqual(int(np.min(gen.separation(depth))),62)
        values=gen.separation(np.linspace(0,1,100))
        self.assertTrue(np.all(np.diff(values)<=0))

    def test_every_accepted_pair_has_equal_exported_rgb_and_no_order_inversion(self):
        depth=gen.depthmap();counts=[]
        for y,row in enumerate(depth):
            roots,edges=gen.links_for_row(row)
            counts.append(len(edges))
            ordered=sorted(edges,key=lambda edge:edge[1])
            self.assertEqual(len({e[1] for e in edges}),len(edges))
            self.assertEqual(len({e[2] for e in edges}),len(edges))
            if len(ordered)>1:self.assertTrue(np.all(np.diff([e[2] for e in ordered])>0))
            for x,l,r,s in edges:
                self.assertTrue(0<=l<r<960)
                self.assertEqual(r-l,s)
                self.assertEqual(l,x-s//2)
                self.assertEqual(roots[l],roots[r])
            left=[e[1] for e in edges];right=[e[2] for e in edges]
            self.assertTrue(np.array_equal(self.pixels[y,left],self.pixels[y,right]))
        self.assertEqual(counts,self.facts['edges_per_row'])
        _,middle=gen.links_for_row(depth[240])
        self.assertEqual([list(e) for e in sorted(middle)],self.facts['sample_row_edges'])

    def test_blind_png_recovery_reproduces_published_metric_and_image(self):
        with patch.object(gen,'depthmap',side_effect=AssertionError('decoder read source')), \
             patch.object(gen,'links_for_row',side_effect=AssertionError('decoder read links')), \
             patch.object(gen,'noise',side_effect=AssertionError('decoder read noise')):
            lag,cost=gen.decode(self.pixels)
        self.assertEqual(lag.shape,(480,960))
        self.assertTrue(np.all((cost>=0)&(cost<=1)))
        expected=gen.separation(gen.depthmap());y,x=np.mgrid[:480,:960]
        interior=(x>=100)&(x<860)&(y>=10)&(y<470)
        error=float(np.mean(np.abs(lag.astype(float)-expected)[interior]))
        foreground=(expected<77)&interior;recovered=(lag<77)&interior
        iou=float(np.sum(foreground&recovered)/np.sum(foreground|recovered))
        self.assertGreater(iou,.95)
        self.assertLess(error,.12)
        self.assertAlmostEqual(error,self.facts['decode']['mean_absolute_lag_error_px'])
        self.assertAlmostEqual(iou,self.facts['decode']['foreground_iou'])
        with Image.open(ART/'recovered.png') as image:actual=np.array(image)
        self.assertTrue(np.array_equal(actual,np.uint8(np.round(gen.lag_to_depth(lag)*255))))
        # Regression: uint8 multiplication must not wrap bright recovered relief to near-black.
        self.assertGreater(int(actual[245,589]),200)
        self.assertLess(abs(float(gen.lag_to_depth(lag)[245,589])-.9),.08)

    def test_constant_planes_and_new_noise_seed(self):
        for height in (0,.75):
            plane=np.full((25,320),height)
            pixels,_,_=gen.encode(plane)
            lag,_=gen.decode(pixels)
            self.assertTrue(np.all(lag[4:-4,100:-100]==int(gen.separation(height))))
        plane=np.full((25,320),.75)
        first,_,_=gen.encode(plane)
        with patch.object(gen,'SEED',gen.SEED+917):
            second,_,_=gen.encode(plane)
        self.assertFalse(np.array_equal(first,second))
        lag,_=gen.decode(second)
        self.assertTrue(np.all(lag[4:-4,100:-100]==int(gen.separation(.75))))

    def test_still_png_no_alpha_no_hidden_animation_and_correct_readme_reveal(self):
        with Image.open(ART/'stereogram.png') as image:
            self.assertEqual(image.mode,'RGB')
            self.assertEqual(image.size,(960,480))
            self.assertEqual(image.n_frames,1)
        digest=hashlib.sha256((ART/'stereogram.png').read_bytes()).hexdigest()
        self.assertEqual(digest,self.facts['sha256'])
        readme=(ROOT/'README.md').read_text()
        self.assertIn('<a href="assets/stereogram/proof.png"><img src="assets/stereogram/stereogram.png"',readme)
        section=readme.split('## Скрытый рельеф',1)[1].split('\n## ',1)[0]
        self.assertNotRegex(section,r'<script|<iframe|\.gif|onmouseover')
        with Image.open(ART/'proof.png') as proof:
            self.assertEqual(proof.size,(1040,1160))
            expected_lag,_=gen.decode(self.pixels)
            self.assertTrue(np.array_equal(np.array(proof),np.array(gen.proof(gen.depthmap(),expected_lag))))

    def test_offline_zip_is_self_contained_and_has_exact_link_data(self):
        with zipfile.ZipFile(ART/'bench.zip') as archive:
            self.assertEqual(set(archive.namelist()),{'bench.html','stereogram.png','depth.png'})
            for name in archive.namelist():
                self.assertEqual(archive.read(name),(ART/name).read_bytes())
                self.assertEqual(archive.getinfo(name).date_time,(2026,11,18,0,0,0))
        html=(ART/'bench.html').read_text()
        data=json.loads(re.search(r'const data=(.*?);const c=',html).group(1))
        self.assertEqual(data['pairs'],self.facts['sample_row_edges'])
        self.assertEqual(data['row'],240)
        self.assertIn('aria-live="polite"',html)
        self.assertNotRegex(html,r'https?://|fetch\(|XMLHttpRequest|localStorage|setInterval|requestAnimationFrame|<script[^>]+src')
        self.assertIn("pattern.src='stereogram.png'",html)
        self.assertIn("depth.src='depth.png'",html)

    def test_sources_are_pinned_and_scope_does_not_count_failed_lookup(self):
        sources=json.loads((ROOT/'atlas/samples/stereogram/sources.json').read_text())
        self.assertEqual(len(sources['readmes']),7)
        self.assertEqual(len(sources['unavailable']),1)
        self.assertFalse(sources['unavailable'][0]['counted_as_reviewed'])
        self.assertEqual(sum('source_file' in s for s in sources['readmes']),3)
        for item in sources['readmes']:
            self.assertRegex(item['commit'],r'^[a-f0-9]{40}$')
            self.assertIn('/blob/'+item['commit']+'/',item['url'])
            if 'source_file' in item:self.assertIn('/blob/'+item['commit']+'/',item['source_url'])

    def test_cli_decoder_does_not_regenerate_assets(self):
        with tempfile.TemporaryDirectory() as tmp:
            # Only the exported input is supplied. No facts, source depth or link files.
            source=Path(tmp)/'input.png';source.write_bytes((ART/'stereogram.png').read_bytes())
            dest=Path(tmp)/'decoded.png'
            subprocess.run([sys.executable,str(GEN),'--decode',str(source),'--output',str(dest)],check=True)
            self.assertEqual(dest.read_bytes(),(ART/'recovered.png').read_bytes())
            self.assertEqual({p.name for p in Path(tmp).iterdir()},{'input.png','decoded.png'})

    def test_reprint_is_byte_identical(self):
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run([sys.executable,str(GEN),'--output',tmp],check=True,capture_output=True)
            self.assertEqual({p.name for p in Path(tmp).iterdir()},{p.name for p in ART.iterdir()})
            for source in ART.iterdir():
                self.assertEqual(source.read_bytes(),(Path(tmp)/source.name).read_bytes(),source.name)
