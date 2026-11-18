"""Read the typeset strips back against the durations encoded in the finished GIFs."""

import importlib.util
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from itertools import accumulate
from pathlib import Path
from urllib.parse import unquote

from atlas.samples import cue_sheet

ROOT = Path(__file__).resolve().parents[1]
BLOCK = ROOT / 'templates/blocks/cue-sheet.md'
PRINTER = ROOT / 'atlas/samples/cue_sheet.py'
PILLOW = importlib.util.find_spec('PIL') is not None
ROW = re.compile(r'^│([^│]+)│ +([0-9]+,[0-9]{2}) +<a href="(/[^"\n]+)">([^\n]+)</a>$', re.MULTILINE)


class CueSheetTest(unittest.TestCase):
    def test_frame_ending_on_boundary_and_in_partial_last_cell(self):
        self.assertEqual(cue_sheet.endings([400, 800, 20, 30], 400), [1, 0, 1, 2])
        self.assertEqual(cue_sheet.endings([50] * 80, 400), [8] * 10)

    def test_one_scale_even_when_both_axes_change(self):
        tracks = [cue_sheet.Track('Быстро', '/fast.gif', (50,) * 130), cue_sheet.Track('Редко', '/slow.gif', (400, 400))]
        sheet = cue_sheet.typeset(tracks)
        self.assertIn('**0,8 с**', sheet)  # 6.50 s does not fit in 16 cells of 0.4 s
        self.assertIn('`▁` — от 1 до 2', sheet)  # 16 frame endings per full cell, two per level
        self.assertEqual([r[0] for r in ROW.findall(sheet)], ['█' * 8 + '▁' + ' ' * 7, '▁' + ' ' * 15])

    def test_portable_block_is_the_score_on_display(self):
        block = BLOCK.read_text(encoding='utf-8')
        section = (ROOT / 'README.md').read_text(encoding='utf-8').split('#### Партитура пауз\n')[1].split('\n#### ')[0]
        self.assertIn(block, section)
        self.assertNotRegex(section, r'<(?:img|picture|details|script)\b|!\[')
        rows = ROW.findall(block)
        self.assertEqual([r[3] for r in rows], ['Набор', 'Сгиб', 'Медуза'])
        for cells, _, href, _ in rows:
            self.assertEqual(len(cells), 16)
            self.assertTrue((ROOT / unquote(href[1:])).is_file())

    @unittest.skipUnless(PILLOW, 'install Pillow to read the finished GIFs')
    def test_every_printed_cell_against_the_finished_frames(self):
        from PIL import Image, ImageSequence

        sheet = BLOCK.read_text(encoding='utf-8')
        for cells, seconds, href, label in ROW.findall(sheet):
            with self.subTest(label=label), Image.open(ROOT / unquote(href[1:])) as im:
                ends = list(accumulate(frame.info['duration'] for frame in ImageSequence.Iterator(im)))
                self.assertEqual(ends[-1], int(seconds.replace(',', '')) * 10)
                for i, glyph in enumerate(cells):
                    if 400 * i >= ends[-1]:
                        self.assertEqual(glyph, ' ')  # past the loop end, not a held frame
                    else:
                        count = sum(400 * i < end <= 400 * (i + 1) for end in ends)
                        self.assertEqual(glyph, '·▁▂▃▄▅▆▇█'[count])
        self.assertEqual(subprocess.check_output([sys.executable, PRINTER], cwd=ROOT, encoding='utf-8'), sheet)

    @unittest.skipUnless(PILLOW, 'install Pillow for the printer CLI')
    def test_external_reel_quotes_links_and_rejects_untimed_input(self):
        from PIL import Image

        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp)
            name = 'пауза #1.gif'
            shutil.copy(ROOT / 'assets/facet-count.gif', dest / name)
            cmd = [sys.executable, PRINTER, f'Перо & <лист>={name}']
            result = subprocess.check_output(cmd, cwd=dest, encoding='utf-8')
            (_, seconds, href, label), = ROW.findall(result)
            self.assertEqual((seconds, label), ('3,71', 'Перо &amp; &lt;лист&gt;'))
            self.assertEqual(unquote(href), '/' + name)
            self.assertNotRegex(href, r'[ #]')
            self.assertEqual(list(dest.iterdir()), [dest / name])
            Image.new('RGB', (2, 2)).save(dest / name, save_all=True, append_images=[Image.new('RGB', (2, 2), 'red')])
            bad = subprocess.run(cmd, cwd=dest, capture_output=True, encoding='utf-8', check=False)
            self.assertNotEqual(bad.returncode, 0)
            self.assertFalse(bad.stdout)
            self.assertIn('положительными задержками', bad.stderr)
