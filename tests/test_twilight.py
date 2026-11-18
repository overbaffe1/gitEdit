"""Read the one RGBA plate back on two stocks. The two ink cuts are independent references."""

import re
import struct
import unittest
from pathlib import Path
from zipfile import ZipFile

try:
    from PIL import Image, ImageChops
except ImportError:
    Image = None

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'assets/twilight'
SOURCE = ROOT / 'atlas/samples/twilight'


class TwilightTest(unittest.TestCase):
    def test_same_static_png_in_readme_and_portable_table(self):
        raw = (ART / 'glass.png').read_bytes()
        self.assertEqual(raw[:8], b'\x89PNG\r\n\x1a\n')
        self.assertEqual(struct.unpack_from('>IIBB', raw, 16), (720, 856, 8, 6))
        with ZipFile(ART / 'table.zip') as pocket:
            self.assertEqual(set(pocket.namelist()), {'table.html', 'glass.png'})
            self.assertEqual(pocket.read('glass.png'), raw)
            html = pocket.read('table.html').decode('utf-8')
            self.assertEqual(html, (SOURCE / 'table.html').read_text('utf-8'))
            self.assertEqual(re.findall(r'<img src="([^"]+)"', html), ['glass.png'])
        doc = (ROOT / 'README.md').read_text('utf-8').split('## Сумеречный лист\n')[1].split('\n## ')[0]
        before, inside = doc.split('<details>')
        self.assertNotRegex(before, r'<picture|<source|srcset=')
        self.assertIn('<a href="assets/twilight/proof.png"><img src="assets/twilight/glass.png"', before)
        self.assertIn('src="assets/twilight/proof.png"', inside)

    @unittest.skipUnless(Image, 'Pillow needed to check the ink separations')
    def test_both_papers_recover_their_own_engraving(self):
        with Image.open(ART / 'glass.png') as film, Image.open(ART / 'proof.png') as proof:
            self.assertEqual(film.n_frames, 1)
            w, h = film.size
            self.assertEqual(proof.size, (2 * w, h))
            # The portraits sit inside this window; it excludes the shared registration marks and type.
            cut_box = (96, 0, 550, 632)
            window = (136, 90, 590, 722)
            for i, (name, stock, ink) in enumerate(
                [('fox', (255, 255, 255), (13, 17, 23)), ('owl', (13, 17, 23), (255, 255, 255))]
            ):
                with self.subTest(name=name), Image.open(SOURCE / f'{name}.png') as cut:
                    paper = Image.new('RGB', film.size, stock)
                    paper.paste(film, (0, 0), film.getchannel('A'))
                    self.assertEqual(proof.crop((i * w, 0, (i + 1) * w, h)).tobytes(), paper.tobytes())
                    # Check the actual printed pixels against only this reading's ink mask.
                    self.assertGreater(cut.getextrema()[1], 150)
                    mask = cut.crop(cut_box)
                    expected = Image.composite(
                        Image.new('RGB', mask.size, ink), Image.new('RGB', mask.size, stock), mask
                    )
                    error = ImageChops.difference(paper.crop(window), expected)
                    self.assertLessEqual(max(hi for _, hi in error.getextrema()), 1)  # 8-bit RGBA rounding
