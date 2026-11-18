"""Verify ordinary overlay, exact recovery, ideal conditional masks and public-seed limits."""
from collections import Counter
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import numpy as np
from PIL import Image
import fitz

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'assets/veil'
GEN=ROOT/'atlas/samples/veil/generate.py'
spec=importlib.util.spec_from_file_location('veil',GEN)
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)


class Veil(unittest.TestCase):
    def test_every_share_block_has_exactly_two_opaque_black_subpixels(self):
        for name in ('sheet-a.png','sheet-b.png'):
            with Image.open(ART/name) as image:
                self.assertEqual(image.mode,'RGBA');self.assertEqual(image.size,(256,192))
                data=np.array(image)
            self.assertTrue(np.all(data[:,:,:3]==0))
            self.assertEqual(set(np.unique(data[:,:,3])),{0,255})
            bits=data[:,:,3]==255
            self.assertTrue(np.all(gen.block_counts(bits)==2))
            self.assertEqual(int(bits.sum()),24576)

    def test_all_six_masks_have_equal_ideal_conditional_distributions(self):
        patterns=gen.PATTERNS
        self.assertEqual(len(set(patterns)),6)
        self.assertTrue(all(sum(p)==2 for p in patterns))
        distributions={}
        for secret in (False,True):
            a=Counter();b=Counter()
            for pattern in patterns:
                other=tuple(1-v for v in pattern) if secret else pattern
                a[pattern]+=1;b[other]+=1
                self.assertEqual(sum(x or y for x,y in zip(pattern,other)),4 if secret else 2)
            distributions[secret]=(a,b)
        self.assertEqual(distributions[False],distributions[True])
        self.assertEqual(set(distributions[True][1].values()),{1})

    def test_stack_is_plain_alpha_compositing_of_emitted_shares(self):
        with Image.open(ART/'sheet-a.png') as a,Image.open(ART/'sheet-b.png') as b:
            white=Image.new('RGBA',a.size,'white');white.alpha_composite(a);white.alpha_composite(b)
            with Image.open(ART/'stack.png') as actual:
                self.assertTrue(np.array_equal(np.array(white.convert('RGB')),np.array(actual)))
            masks=np.maximum(np.array(a)[:,:,3],np.array(b)[:,:,3])==255
        counts=gen.block_counts(masks);secret=gen.boat()
        self.assertTrue(np.all(counts[secret]==4));self.assertTrue(np.all(counts[~secret]==2))

    def test_recovery_reads_only_flattened_png_and_matches_every_pixel(self):
        with tempfile.TemporaryDirectory() as tmp:
            source=Path(tmp)/'stack.png';source.write_bytes((ART/'stack.png').read_bytes())
            dest=Path(tmp)/'recovered.png'
            with patch.object(gen,'boat',side_effect=AssertionError('read source')),patch.object(gen,'split',side_effect=AssertionError('read shares')),patch.object(gen,'choice',side_effect=AssertionError('read seed')):
                recovered=gen.recover_file(source,dest)
            self.assertTrue(np.array_equal(recovered,gen.boat()))
            self.assertEqual(dest.read_bytes(),(ART/'source.png').read_bytes())
            self.assertEqual(dest.read_bytes(),(ART/'recovered.png').read_bytes())
            dest.unlink()
            subprocess.run([sys.executable,str(GEN),'--decode',str(source),'--output',str(dest)],check=True)
            self.assertEqual(dest.read_bytes(),(ART/'recovered.png').read_bytes())
            self.assertEqual({p.name for p in Path(tmp).iterdir()},{'stack.png','recovered.png'})

    def test_public_seed_really_breaks_confidentiality_of_single_b(self):
        # A does not depend on the hidden drawing. Anyone with the published seed
        # can regenerate A from an all-white drawing and reveal published B alone.
        blank=np.zeros((96,128),dtype=bool)
        known_a,_=gen.split(blank,gen.SEED)
        true_a,_=gen.split(gen.boat(),gen.SEED)
        self.assertTrue(np.array_equal(known_a,true_a))
        with Image.open(ART/'sheet-b.png') as b:
            bbits=np.array(b)[:,:,3]==255
        reconstructed=gen.block_counts(known_a|bbits)==4
        self.assertTrue(np.array_equal(reconstructed,gen.boat()))
        with Image.open(ART/'sheet-a.png') as a:
            self.assertTrue(np.array_equal(np.array(a)[:,:,3]==255,known_a))
        other,_=gen.split(blank,gen.SEED+' different')
        self.assertFalse(np.array_equal(other,known_a))

    def test_pdf_a4_pages_have_same_bits_and_calibration(self):
        with fitz.open(ART/'sheets-a4.pdf') as pdf:
            self.assertEqual(len(pdf),2)
            yy,xx=np.mgrid[:192,:256]
            # PDF points → top-origin raster coordinates, exact cell centers.
            scale=2;factor=72/25.4*scale
            sample_x=((41+(xx+.5)*.5)*factor).astype(int)
            sample_y=((297-(115+(192-yy-.5)*.5))*factor).astype(int)
            for page,name in zip(pdf,('sheet-a.png','sheet-b.png')):
                self.assertAlmostEqual(page.rect.width,210*72/25.4,places=3)
                self.assertAlmostEqual(page.rect.height,297*72/25.4,places=3)
                self.assertIn('50 mm',page.get_text())
                pix=page.get_pixmap(matrix=fitz.Matrix(scale,scale),alpha=False)
                pixels=np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,pix.n)
                printed=pixels[sample_y,sample_x,0]<128
                with Image.open(ART/name) as share:expected=np.array(share)[:,:,3]==255
                self.assertTrue(np.array_equal(printed,expected),name)

    def test_decoder_rejects_misaligned_or_lossy_inputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            source=Path(tmp)/'bad.png';dest=Path(tmp)/'out.png'
            for image in (Image.new('RGB',(3,4),'black'),Image.new('RGB',(4,4),'white'),Image.new('RGB',(4,4),'#888888'),Image.new('RGBA',(4,4),(0,0,0,255))):
                image.save(source)
                with self.assertRaises(ValueError):gen.recover_file(source,dest)
            self.assertFalse(dest.exists())

    def test_zip_has_only_two_shares_and_local_interface_sources_are_pinned(self):
        with zipfile.ZipFile(ART/'bench.zip') as archive:
            self.assertEqual(set(archive.namelist()),{'bench.html','sheet-a.png','sheet-b.png'})
            for name in archive.namelist():
                self.assertEqual(archive.read(name),(ART/name).read_bytes())
                self.assertEqual(archive.getinfo(name).date_time,(2026,11,18,0,0,0))
        html=(ART/'bench.html').read_text()
        self.assertNotRegex(html,r'https?://|fetch\(|XMLHttpRequest|localStorage|setInterval|requestAnimationFrame|source\.png|recovered\.png|stack\.png')
        self.assertIn('aria-live="polite"',html)
        rows=json.loads((ROOT/'atlas/samples/veil/sources.json').read_text())
        good=[r for r in rows if r['status']=='README screening']
        self.assertEqual(len(good),7);self.assertEqual(len(rows)-len(good),1)
        self.assertEqual(sum('source_file' in r for r in good),3)
        for r in good:
            self.assertRegex(r['commit'],r'^[a-f0-9]{40}$')
            self.assertIn('/blob/'+r['commit']+'/',r['url'])
            if 'source_file' in r:self.assertIn('/blob/'+r['commit']+'/',r['source_url'])

    def test_reprint_is_byte_identical(self):
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run([sys.executable,str(GEN),'--output',tmp],check=True,capture_output=True)
            self.assertEqual({p.name for p in Path(tmp).iterdir()},{p.name for p in ART.iterdir()})
            for source in ART.iterdir():self.assertEqual(source.read_bytes(),(Path(tmp)/source.name).read_bytes(),source.name)
