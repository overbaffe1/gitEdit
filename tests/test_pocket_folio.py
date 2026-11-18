"""The portable edition, the folded sheet and its four QR/URL pairs tell the same story."""

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'atlas/samples/pocket_folio'
ART = Path('assets/pocket-folio')
BLOCK = Path('templates/blocks/pocket-folio.md')
PDF = ART / 'issue-a4.pdf'
PNG = ART / 'spread.png'
ISSUE = json.loads((SRC / 'issue.json').read_text(encoding='utf-8'))
PRESS = [sys.executable, SRC / 'press.py']
READER = importlib.util.find_spec('pymupdf') is not None
PRESS_READY = (READER and all(importlib.util.find_spec(k) for k in ('PIL', 'reportlab'))
               and Path('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf').is_file())
DECODER = READER and all(importlib.util.find_spec(k) for k in ('zxingcpp', 'PIL'))


class PocketFolio(unittest.TestCase):
    def test_every_margin_opens_its_evidence_even_outside_this_repo(self):
        block = (ROOT / BLOCK).read_text(encoding='utf-8')
        home = (ROOT / 'README.md').read_text(encoding='utf-8').split('### Карманное портфолио\n')[1].split('\n## ')[0]
        self.assertIn(block, home)
        self.assertNotIn('<details', home)
        self.assertEqual(subprocess.check_output([sys.executable, '-S', *PRESS[1:], '--markdown'], encoding='utf-8'), block)
        table = ET.fromstring(block.replace('<br>', '<br/>'))
        for i, (tr, w) in enumerate(zip(table.findall('tbody/tr'), ISSUE['works'], strict=True), 1):
            field, card = tr
            self.assertEqual(field.get('scope'), 'row')
            self.assertEqual(field.findtext('a/strong'), str(w['number']))
            self.assertEqual(field.findtext('a/sub'), w['unit'])
            self.assertEqual(card.findtext('sub'), f'{2 * i:02d}–{2 * i + 1:02d} · {w["project"]}')
            for link, kind in [(field.find('a'), 'proof'), (card.find('a'), 'also')]:
                self.assertTrue(link.get('href').startswith('https://github.com/'))
                self.assertEqual(link.get('href'), w[kind]['url'])
            self.assertEqual(field.find('a').get('title'), w['proof']['label'])
            self.assertIn(w['body'], ''.join(card.itertext()))

    def test_editable_issue_and_unprintable_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'custom.json'
            data = json.loads((SRC / 'issue.json').read_text(encoding='utf-8'))
            data['works'][0]['title'] = 'Волна & <луч>'
            path.write_text(json.dumps(data))
            cmd = [*PRESS, '--issue', path, '--markdown']
            self.assertIn('Волна &amp; &lt;луч&gt;', subprocess.check_output(cmd, encoding='utf-8'))
            data['works'][0]['number'] += 1
            path.write_text(json.dumps(data))
            bad = subprocess.run(cmd, check=False, capture_output=True, encoding='utf-8')
            self.assertNotEqual(bad.returncode, 0)
            self.assertIn('marks', bad.stderr)
            self.assertFalse(bad.stdout)

    @unittest.skipUnless(READER, 'install PyMuPDF to read back the imposed A4')
    def test_fold_order_orientation_margins_and_links(self):
        import pymupdf

        with pymupdf.open(ROOT / PDF) as doc:
            self.assertEqual(len(doc), 1)
            p = doc[0]
            w, h = p.rect.width, p.rect.height
            self.assertAlmostEqual(w * 25.4 / 72, 297, places=3)
            self.assertAlmostEqual(h * 25.4 / 72, 210, places=3)
            rows = [[5, 4, 3, 2], [6, 7, 8, 1]]
            for r, slots in enumerate(rows):
                for col, n in enumerate(slots):
                    clip = pymupdf.Rect(col * w / 4, r * h / 2, (col + 1) * w / 4, (r + 1) * h / 2)
                    detail = p.get_text('dict', clip=clip)
                    lines = [line for b in detail['blocks'] for line in b.get('lines', [])]
                    self.assertIn(f'{n:02d} / 08', [''.join(s['text'] for s in line['spans']) for line in lines])
                    self.assertEqual({line['dir'] for line in lines}, {(-1., 0.) if r == 0 else (1., 0.)})
                    for line in lines:
                        x0, y0, x1, y1 = line['bbox']
                        self.assertTrue(clip.x0 + 8 < x0 < x1 < clip.x1 - 8 and clip.y0 + 8 < y0 < y1 < clip.y1 - 8)
            found = {}
            for link in p.get_links():
                rect = link['from']
                n = rows[int(rect.y0 // (h / 2))][int(rect.x0 // (w / 4))]
                found[n] = link['uri']
            self.assertEqual(found, {**{3 + 2 * i: v['proof']['url'] for i, v in enumerate(ISSUE['works'])}, 8: ISSUE['profile']})

    @unittest.skipUnless(DECODER, 'optional: PyMuPDF, Pillow and zxing-cpp for an optical read of the paper QR codes')
    def test_qr_ink_decodes_on_the_finished_sheet(self):
        import pymupdf
        import zxingcpp
        from PIL import Image

        with pymupdf.open(ROOT / PDF) as doc:
            pix = doc[0].get_pixmap(dpi=144, colorspace=pymupdf.csGRAY, alpha=False)
            image = Image.frombytes('L', (pix.width, pix.height), pix.samples)
            self.assertCountEqual([x.text for x in zxingcpp.read_barcodes(image)],
                                  [ISSUE['profile'], *(w['proof']['url'] for w in ISSUE['works'])])
        # The screen proof is the *upright* CosmoH spread, not a thumbnail of the upside-down sheet.
        with Image.open(ROOT / PNG) as image:
            (code,) = zxingcpp.read_barcodes(image)
            self.assertEqual((code.text, code.orientation), (ISSUE['works'][1]['proof']['url'], 0))

    @unittest.skipUnless(PRESS_READY, 'install print requirements and the DejaVu fonts for a reprint')
    def test_clean_reprint(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp)
            (dest / 'README.md').write_text('untouched')
            subprocess.run([*PRESS, '--out', dest], check=True)
            files = {p.relative_to(dest) for p in dest.rglob('*') if p.is_file()}
            self.assertEqual(files, {Path('README.md'), BLOCK, PNG, PDF})
            self.assertEqual((dest / 'README.md').read_text(), 'untouched')
            for file in (BLOCK, PNG, PDF):
                self.assertEqual((dest / file).read_bytes(), (ROOT / file).read_bytes(), file)
