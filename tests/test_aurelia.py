"""Read the published stereo specimen, not an exporter's private drawing instructions."""

import base64
import re
import struct
import tempfile
import unittest
import wave
from itertools import pairwise
from pathlib import Path
from zipfile import ZipFile

from atlas.samples.aurelia.xy_signal import write_wav

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'assets/aurelia'
SOURCE = ROOT / 'atlas/samples/aurelia'

try:
    from PIL import Image
except ImportError:
    Image = None  # The signal and package tests need only the standard library.


class AureliaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.wav = (ART / 'aurelia.wav').read_bytes()
        with wave.open(str(ART / 'aurelia.wav'), 'rb') as wav:
            cls.params = wav.getparams()
            cls.pairs = list(struct.iter_unpack('<hh', wav.readframes(wav.getnframes())))

    def test_stereo_signal_and_loop_seam(self):
        self.assertEqual(self.params[:5], (2, 2, 48_000, 192_000, 'NONE'))
        self.assertEqual(len(self.pairs), 800 * 240)
        # No image payload, and no blanking jumps between strokes, scans, or at the loop seam.
        self.assertEqual(len(self.wav), 44 + len(self.pairs) * 4)
        for k in (0, 1):
            channel = [p[k] for p in self.pairs]
            self.assertLess(min(channel), -2500)
            self.assertGreater(max(channel), 2500)
            self.assertLess(max(map(abs, channel)), 8192)  # headroom on the sound output
            jumps = (abs(a - b) for a, b in pairwise([channel[-1], *channel]))
            self.assertLess(max(jumps), 256)
            self.assertLess(max(abs(sum(channel[i : i + 800])) / 800 for i in range(0, len(channel), 800)), 0.5)
        with tempfile.TemporaryDirectory() as tmp:
            fresh = Path(tmp) / 'new.wav'
            write_wav(fresh)
            self.assertEqual(fresh.read_bytes(), self.wav)

    def test_pocket_scope_packs_the_same_recording(self):
        with ZipFile(ART / 'scope.zip') as pocket:
            self.assertEqual(pocket.namelist(), ['aurelia.html'])
            html = pocket.read('aurelia.html').decode('utf-8')
        (blob,) = re.findall(r'<script type="application/octet-stream" id="recording">([^<]+)</script>', html)
        self.assertEqual(base64.b64decode(blob, validate=True), self.wav)
        self.assertEqual(html.replace(blob, '@@STEREO_WAV@@'), (SOURCE / 'scope.html.in').read_text('utf-8'))

    def test_motion_fallback_and_downloads(self):
        text = (ROOT / 'README.md').read_text('utf-8')
        self.assertRegex(
            text,
            r'<picture>\s*<source media="\(prefers-reduced-motion: reduce\)" srcset="assets/aurelia/trace.png">\s*<img src="assets/aurelia/swim.gif"[^>]+alt="[^"]+">',
        )
        for name in ('aurelia.wav', 'scope.zip'):
            self.assertIn(f'](assets/aurelia/{name}?raw=true)', text)

    @unittest.skipUnless(Image, 'Pillow needed to read the phosphor prints')
    def test_printed_trace_follows_the_pcm(self):
        def check(frame, scan):
            # Published calibration: screen origin and the same deflection gain on both axes.
            points = {
                (round(207 + 0.0306 * left), round(174 - 0.0306 * right))
                for left, right in self.pairs[800 * scan : 800 * (scan + 1)]
            }
            pixels = frame.convert('RGB').load()
            # A real trace must hit the expected points and not fill the rest of the screen with light.
            hit = sum(
                any(pixels[x + dx, y + dy][1] > 145 for dx in (-1, 0, 1) for dy in (-1, 0, 1))
                for x, y in points
            )
            self.assertGreater(hit / len(points), 0.98, scan)
            lit = sum(pixels[x, y][1] > 145 for x in range(62, 352) for y in range(60, 312))
            self.assertLess(lit, 0.12 * 290 * 252, scan)

        with Image.open(ART / 'trace.png') as still, Image.open(ART / 'swim.gif') as film:
            self.assertEqual(still.size, film.size)
            self.assertEqual(film.n_frames, 80)
            self.assertEqual(film.info['loop'], 0)
            check(still, 0)
            duration = 0
            for i in range(film.n_frames):
                film.seek(i)
                duration += film.info['duration']
                if i in (0, 19, 39, 62, 79):
                    check(film, i * 3)
            self.assertEqual(duration, 4000)
