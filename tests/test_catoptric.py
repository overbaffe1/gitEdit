"""A physically scaled print and its reflection, not a straight image pasted on a cylinder."""

import base64
import importlib.util
import re
import unittest
import zipfile
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'assets/catoptric'
SRC = ROOT / 'atlas/samples/catoptric'
OPTICS = all(importlib.util.find_spec(n) for n in ('numpy', 'PIL'))


class PrintKit(unittest.TestCase):
    def test_portable_reads_only_the_shipped_paper(self):
        with zipfile.ZipFile(ART / 'bench.zip') as z:
            self.assertEqual(z.namelist(), ['mirror.html', 'sheet-a4.pdf'])
            self.assertEqual(z.read('sheet-a4.pdf'), (ART / 'sheet-a4.pdf').read_bytes())
            page = z.read('mirror.html').decode()
        (data,) = re.findall(r'data:image/png;base64,([A-Za-z0-9+/=]+)', page)
        self.assertEqual(base64.b64decode(data, validate=True), (ART / 'sheet.png').read_bytes())
        self.assertEqual(page.replace(data, '@@SHEET@@'), (SRC / 'bench.html.in').read_text())
        self.assertNotRegex(page, r'https?://|engraving\.png')
        self.assertIn('href="sheet-a4.pdf"', page)
        home = (ROOT / 'README.md').read_text()
        for url in ('sheet-a4.pdf', 'sheet-a4.pdf?raw=true', 'proof.png', 'mirror.png', 'bench.zip?raw=true'):
            self.assertIn('assets/catoptric/' + url, home)

    @unittest.skipUnless(
        importlib.util.find_spec('pymupdf') and OPTICS, 'install PyMuPDF and Pillow for PDF checks'
    )
    def test_pdf_is_one_lossless_a4_at_actual_size(self):
        import pymupdf
        from PIL import Image, ImageChops

        with pymupdf.open(ART / 'sheet-a4.pdf') as doc, Image.open(ART / 'sheet.png') as sheet:
            self.assertEqual(len(doc), 1)
            page = doc[0]
            mm = 72 / 25.4
            for dim, length in zip((page.rect.width, page.rect.height), (297, 210), strict=True):
                self.assertAlmostEqual(dim / mm, length, places=3)
            (image,) = page.get_images()
            (rect,) = page.get_image_rects(image[0])
            self.assertEqual(rect, page.rect)
            with Image.open(BytesIO(doc.extract_image(image[0])['image'])) as embedded:
                self.assertEqual(embedded.size, (2376, 1680))
                self.assertIsNone(ImageChops.difference(sheet, embedded.convert('RGB')).getbbox())
            # Top ends of the two long ruler ticks: physical separation 50 mm and nothing drawn between them here.
            self.assertEqual(sheet.getpixel((10 * 8, 197 * 8)), sheet.getpixel((60 * 8, 197 * 8)))
            self.assertLess(max(sheet.getpixel((10 * 8, 197 * 8))), 150)
            self.assertEqual(sheet.getpixel((11 * 8, 197 * 8)), (255, 255, 255))


@unittest.skipUnless(OPTICS, 'install atlas/samples/catoptric/requirements.txt for optical checks')
class Reflection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import numpy as np
        from PIL import Image

        spec = importlib.util.spec_from_file_location('catoptric_optics', SRC / 'optics.py')
        cls.o = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.o)
        cls.np = np
        with Image.open(ART / 'sheet.png') as im:
            cls.sheet = np.array(im.convert('RGB'))
        with Image.open(SRC / 'engraving.png') as im:
            cls.master = np.array(im.convert('RGB'))

    def test_entire_field_is_visible_and_the_two_optical_paths_agree(self):
        np = self.np
        o = self.o
        u, v = np.meshgrid(np.linspace(-18.8, 18.8, 81), np.linspace(-23.5, 23.5, 77))
        q = o.sight(u, v)
        self.assertTrue(q['side'].all())
        self.assertFalse(q['cap'].any())
        self.assertGreater(q['z'].min(), 0)
        self.assertLess(q['z'].max(), 80)
        self.assertGreater((148.5 - np.abs(q['x'])).min(), 8)
        self.assertGreater((57 - q['y']).min(), 27)
        self.assertLess((57 - q['y']).max(), 195)
        pu, pv, visible = o.paper_to_card(q['x'], q['y'])
        self.assertTrue(visible.all())
        np.testing.assert_allclose(pu, u, atol=0.00001)
        np.testing.assert_allclose(pv, v, atol=0.00001)
        # On the symmetry axis this reduces independently to similar triangles.
        centre = o.sight(np.array(0.0), np.array(0.0))
        self.assertAlmostEqual(float(centre['y']), -25 - 44 * (280 - 25) / (240 - 44), places=8)

    def test_readme_views_show_the_observed_paper(self):
        from PIL import Image, ImageChops

        np = self.np
        with Image.open(ART / 'mirror.png') as mobile, Image.open(ART / 'proof.png') as wide:
            w, h = mobile.size
            # Same camera image in both responsive plates.
            inset = wide.crop((591, 81, 591 + w, 81 + h))
            self.assertIsNone(ImageChops.difference(inset, mobile).getbbox())
            u = -55.5 + (np.arange(w)[None, :] + 0.5) * 111 / w
            v = 61.4 - (np.arange(h)[:, None] + 0.5) * 109.4 / h
            rays = self.o.sight(u, v)
            raw = self.o.from_sheet(self.sheet, rays['x'], rays['y'])
            # Camera has mild reflective shading and antialiasing; compare the actual figure, not its frame.
            cut = (abs(u) < 17) & (abs(v) < 20)
            correlation = np.corrcoef(raw[cut].ravel(), np.asarray(mobile)[cut].ravel())[0, 1]
            self.assertGreater(correlation, 0.985)

    def test_published_ink_reconstructs_an_upright_engraving_only_on_axis(self):
        np = self.np
        o = self.o
        h, w = self.master.shape[:2]
        u = ((np.arange(w)[None, :] + 0.5) / w - 0.5) * 37.6
        v = (0.5 - (np.arange(h)[:, None] + 0.5) / h) * 47

        def reconstruct(yaw):
            q = o.sight(u, v, yaw=yaw)
            return o.from_sheet(self.sheet, q['x'], q['y'])

        straight = reconstruct(0)
        difference = np.abs(straight - self.master)
        self.assertLess(difference.mean(), 2.5)
        self.assertLess(np.percentile(difference, 95), 15)
        self.assertGreater(np.abs(straight - self.master[::-1]).mean(), 10 * difference.mean())
        self.assertGreater(np.abs(reconstruct(25) - self.master).mean(), 25)
        # Check the seahorse, not just the easily matched light paper around its silhouette.
        dark = self.master[:, :, 1] < 100
        self.assertGreater(dark.mean(), 0.10)
        self.assertLess(difference[dark].mean(), 6)
        mark = o.sight(np.array(14.77), np.array(20.48))
        self.assertAlmostEqual(148.5 + mark['x'], 256.36, places=2)
        self.assertAlmostEqual(57 - mark['y'], 105.89, places=2)
        np.testing.assert_array_equal(o.from_sheet(self.sheet, mark['x'], mark['y']), self.master[38, 428])
