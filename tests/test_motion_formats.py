"""Decode the actual animation containers, not just their file extensions."""
import csv
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

try:
    from PIL import Image, ImageChops, features
except ImportError:
    Image=None

ROOT=Path(__file__).resolve().parents[1]
GEN=ROOT/'atlas/samples/motion_formats/generate.py'
ART=ROOT/'assets/motion-formats'
if Image:
    spec=importlib.util.spec_from_file_location('motion_formats',GEN)
    gen=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gen)
else:
    gen=None


@unittest.skipUnless(Image,'Pillow needed to decode motion containers')
class MotionFormatsTest(unittest.TestCase):
    def test_magic_frames_timing_and_loop(self):
        expected={'cube.gif':b'GIF89a','cube-apng.png':b'\x89PNG\r\n\x1a\n','cube.webp':b'RIFF'}
        for name,magic in expected.items():
            self.assertTrue((ART/name).read_bytes().startswith(magic))
            with Image.open(ART/name) as im:
                self.assertEqual(im.n_frames,32)
                self.assertEqual(im.size,(256,192))
                self.assertEqual(im.info.get('loop'),0)
                total=0
                for i in range(im.n_frames):
                    im.seek(i);im.load()
                    self.assertEqual(im.info['duration'],80)
                    total+=im.info['duration']
                self.assertEqual(total,2560)
        self.assertIn(b'acTL',(ART/'cube-apng.png').read_bytes())
        self.assertIn(b'ANIM',(ART/'cube.webp').read_bytes())

    def test_lossless_frames_match_source_on_black_and_white(self):
        if not features.check('webp'):
            self.skipTest('Pillow WebP support needed')
        expected=[gen.frame(i) for i in range(gen.COUNT)]
        for name in ('cube-apng.png','cube.webp'):
            with Image.open(ART/name) as im:
                for i in range(gen.COUNT):
                    im.seek(i)
                    got=im.convert('RGBA')
                    # Hidden RGB under zero alpha is codec-dependent; compare the
                    # visible image on two independent opaque backgrounds instead.
                    for bg in ((0,0,0,255),(255,255,255,255)):
                        paper=Image.new('RGBA',gen.SIZE,bg)
                        a=Image.alpha_composite(paper,got).convert('RGB')
                        b=Image.alpha_composite(paper,expected[i]).convert('RGB')
                        self.assertIsNone(ImageChops.difference(a,b).getbbox(),(name,i,bg))

    def test_real_alpha_and_deliberately_opaque_gif(self):
        for name in ('cube-apng.png','cube.webp'):
            with Image.open(ART/name) as im:
                for i in (0,8,16,24):
                    im.seek(i)
                    alpha=im.convert('RGBA').getchannel('A')
                    self.assertEqual(alpha.getextrema(),(0,255))
                    hist=alpha.histogram()
                    self.assertGreater(sum(hist[1:255]),0)
        with Image.open(ART/'cube.gif') as im:
            for i in range(32):
                im.seek(i)
                self.assertEqual(im.convert('RGBA').getchannel('A').getextrema(),(255,255))

    def test_static_posters_and_storyboard(self):
        for name in ('poster.png','poster-matte.png','storyboard.png'):
            with Image.open(ART/name) as im:
                self.assertEqual(getattr(im,'n_frames',1),1)
                size=(1024,384) if name=='storyboard.png' else gen.SIZE
                self.assertEqual(im.size,size)
        with Image.open(ART/'poster.png') as im:
            self.assertEqual(im.convert('RGBA').tobytes(),gen.frame(0).tobytes())
        with Image.open(ART/'poster-matte.png') as im:
            self.assertEqual(im.convert('RGB').tobytes(),gen.flatten(gen.frame(0)).tobytes())
        with Image.open(ART/'storyboard.png') as im:
            for j,i in enumerate(range(0,32,4)):
                x=(j%4)*256;y=(j//4)*192
                tile=im.crop((x,y,x+256,y+192)).convert('RGB')
                self.assertEqual(tile.tobytes(),gen.flatten(gen.frame(i)).tobytes())

    def test_measurements_are_real_and_present_in_readme(self):
        data=json.loads((ART/'formats.json').read_text())
        rows=list(csv.DictReader(io.StringIO((ART/'formats.csv').read_text())))
        self.assertEqual(len(rows),3)
        self.assertEqual(data['size'],[256,192])
        self.assertEqual(data['loop_ms'],2560)
        readme=(ROOT/'README.md').read_text()
        for a,b in zip(rows,data['files']):
            for key,value in a.items():
                self.assertEqual(value,str(b[key]))
            self.assertEqual(int(a['bytes']),(ART/a['file']).stat().st_size)
            self.assertIn(f'| {a["bytes"]} | 32 | 2560 мс |',readme)
        self.assertEqual(readme.count('src="assets/motion-formats/cube-apng.png"'),1)
        self.assertIn('<source type="image/webp" srcset="assets/motion-formats/cube.webp">',readme)
        # The named accordion reuses this demo with its own reduced-motion source.
        panel=(ROOT/'atlas/samples/exclusive_panel/readme-block.md').read_text()
        self.assertEqual(readme.count(panel),1)
        original=readme.replace(panel,'',1)
        self.assertEqual(original.count('media="(prefers-reduced-motion: reduce)" srcset="assets/motion-formats/'),4)

    def test_clean_reprint_preserves_readme(self):
        before=(ROOT/'README.md').read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run([sys.executable,str(GEN),'--output',tmp],cwd=tmp,check=True)
            self.assertEqual({p.name for p in ART.iterdir()},{p.name for p in Path(tmp).iterdir()})
            for file in ART.iterdir():
                self.assertEqual(file.read_bytes(),(Path(tmp)/file.name).read_bytes(),file.name)
        self.assertEqual(before,(ROOT/'README.md').read_bytes())
