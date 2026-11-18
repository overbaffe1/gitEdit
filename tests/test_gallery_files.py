"""The gallery links to exhibit files. Rendering a diagram/model is an explicit choice."""
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / 'atlas/samples'
ART = ROOT / 'assets'
README = ROOT / 'README.md'
TEMPLATE = ROOT / 'templates/EXHIBITION-README-TEMPLATE.md'
DOCS = [README, *(ROOT / 'atlas').glob('*.md'), *(ROOT / 'templates').glob('*.md'), ROOT / 'studio/README.md']


def fence_languages(markdown):
    # A triple-backtick Mermaid example INSIDE ````markdown is plain text.
    delimiter = ''
    for line in markdown.splitlines():
        fence = re.fullmatch(r' {0,3}(`{3,}|~{3,})(.*)', line)
        if fence:
            mark, info = fence.groups()
            if not delimiter:
                delimiter = mark
                yield info.strip().lower()
            elif mark.startswith(delimiter) and not info.strip():
                delimiter = ''


class GalleryFilesTest(unittest.TestCase):
    def test_triptych_and_tickets_open_the_right_files(self):
        stops = ['fold.gif', 'weeks-tape.svg', 'moth-projector.svg']
        pictures = dict(zip(['bench-glass.jpg', 'bench-tape.jpg', 'bench-film.jpg'], stops))
        pictures.update({'ticket-fold.svg': stops[1], 'ticket-tape.svg': stops[2], 'ticket-moth.svg': 'bench-master.jpg'})
        for path in (README, TEMPLATE):
            text = path.read_text(encoding='utf-8')
            cards = {Path(src).name: href for href, src in re.findall(r'<a href="([^"]+)"><img src="([^"]+)"', text)}
            for name, dest in pictures.items():
                with self.subTest(path=path, picture=name):
                    self.assertEqual((path.parent / cards[name]).resolve(), ART / 'night-shift' / dest)
            top = text.split('\n## ', 1)[0]
            # A single unbroken row, not three numbered calls to action.
            row, = re.findall(r'<p align="center">([^\n]+)</p>', top)
            self.assertEqual(row.count('</a><a '), 2)
            self.assertEqual(row.count('width="33%"'), 3)
            self.assertEqual(re.findall(r'bench-(glass|tape|film)\.jpg', row), ['glass', 'tape', 'film'])
            self.assertNotRegex(top, r'Выбери прибор|# Ночная смена|\[0[123] ·')
            self.assertIn('bench-master.jpg)', top)

    def test_no_authored_exhibit_links_to_readme_fragments(self):
        # Scan our authored links, including copyable snippets, not GitHub-generated
        # heading/footnote controls, SVG paint IDs or references to third-party docs.
        for path in [*DOCS, ROOT / 'docs/index.html', ROOT / 'atlas/north.html']:
            text = path.read_text(encoding='utf-8')
            for href in re.findall(r'(?:href="|\]\()([^"\s)]+)', text):
                u = urlsplit(href)
                with self.subTest(page=path.name, href=href):
                    if not u.netloc and not u.scheme:
                        self.assertFalse(u.fragment)
                        if 'assets' in Path(u.path).parts:
                            self.assertTrue((path.parent / unquote(u.path)).is_file())
                    elif u.netloc == 'github.com' and u.path.startswith('/overbaffe1/gitEdit') and (
                        u.path.rstrip('/') == '/overbaffe1/gitEdit' or u.path.lower().endswith('.md')
                    ):
                        self.assertFalse(u.fragment)

    def test_diagrams_are_images_not_enrichments(self):
        for path in DOCS:
            self.assertNotIn('mermaid', set(fence_languages(path.read_text(encoding='utf-8'))), path)
        main = README.read_text(encoding='utf-8')
        self.assertFalse({'stl', 'geojson', 'topojson'} & set(fence_languages(main)))
        diagrams = re.findall(r'<a href="(assets/mermaid/[^\"]+)"><img src="([^\"]+)"[^>]+alt="([^\"]+)"', main)
        self.assertEqual(len({href for href, _, _ in diagrams}), 8)
        for href, src, alt in diagrams:
            self.assertEqual(src, href)
            self.assertTrue(alt.strip())
            self.assertEqual((ROOT / src).read_bytes()[:8], b'\x89PNG\r\n\x1a\n')
            self.assertIn(f'](atlas/samples/{Path(src).stem}.mmd)', main)
        self.assertEqual({p.stem for p in (ART / 'mermaid').glob('*.png')}, {p.stem for p in SAMPLES.glob('*.mmd')})

    def test_native_files_and_plates_regenerate_away_from_readme(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp)
            samples, assets = copy / 'atlas/samples', copy / 'assets'
            samples.mkdir(parents=True)
            assets.mkdir()
            (copy / 'README.md').write_text('untouched')
            for name in ('file_plates.py', 'weekly-skyline.py', 'snake-weeks.csv', 'crystal.stl', 'survey.geojson', 'sheets.topojson'):
                shutil.copy(SAMPLES / name, samples)
            subprocess.run([sys.executable, samples / 'weekly-skyline.py', '--update-readme'], check=True)
            subprocess.run([sys.executable, samples / 'file_plates.py'], check=True)
            self.assertEqual((copy / 'README.md').read_text(), 'untouched')
            for name in ('weekly-skyline.stl', 'crystal.stl', 'survey.geojson', 'sheets.topojson'):
                self.assertEqual((assets / name).read_bytes(), (SAMPLES / name).read_bytes())
            for plate in ('weekly-skyline', 'survey', 'sheets'):
                self.assertTrue((assets / f'{plate}.svg').is_file())
            for f in assets.iterdir():
                self.assertEqual(f.read_bytes(), (ART / f.name).read_bytes(), f.name)
