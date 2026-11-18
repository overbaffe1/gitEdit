"""Read the shipped TTF as a typesetter, not the compiler's move() function."""

import base64
import importlib.util
import re
import unittest
import zipfile
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'assets/typecase'
SRC = ROOT / 'atlas/samples/typecase'
FONT = ART / 'dock.ttf'
SHAPING = all(importlib.util.find_spec(m) for m in ('uharfbuzz', 'fontTools'))
PRESS = all(importlib.util.find_spec(m) for m in ('freetype', 'PIL'))
SOLUTION = '08686622488'


class Cartridge(unittest.TestCase):
    def test_portable_contains_the_released_font(self):
        ttf = FONT.read_bytes()
        self.assertEqual(ttf[:4], b'\x00\x01\x00\x00')
        with zipfile.ZipFile(ART / 'typecase.zip') as z:
            self.assertEqual(z.namelist(), ['dock.html'])
            html = z.read('dock.html').decode()
        (match,) = re.findall(r'data:font/ttf;base64,([A-Za-z0-9+/=]+)', html)
        self.assertEqual(base64.b64decode(match, validate=True), ttf)
        template = (SRC / 'dock.html.in').read_text()
        self.assertEqual(html, template.replace('@@DOCK_TTF@@', match).replace('@@SOLUTION@@', SOLUTION))
        self.assertIn('type="text"', html)
        self.assertNotRegex(html, r'(?i)https?://|<canvas\b')
        home = (ROOT / 'README.md').read_text()
        for url in ('delivery.gif', 'proof.png', 'typecase.zip?raw=true', 'dock.ttf?raw=true'):
            self.assertIn(f'assets/typecase/{url}', home)


@unittest.skipUnless(SHAPING, 'install atlas/samples/typecase/requirements.txt for HarfBuzz checks')
class Typesetting(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import uharfbuzz as hb
        from fontTools.ttLib import TTFont

        cls.tt = TTFont(FONT)
        cls.addClassCleanup(cls.tt.close)
        cls.hb = hb
        cls.shaper = hb.Font(hb.Face(FONT.read_bytes()))
        cls.names = cls.tt.getGlyphOrder()
        cls.rows = (SRC / 'room.txt').read_text().splitlines()
        cls.floor = {(x, y) for y, row in enumerate(cls.rows) for x, ch in enumerate(row) if ch != '#'}
        marks = {ch: (x, y) for x, y in cls.floor if (ch := cls.rows[y][x]) in '@$.'}
        cls.start = (marks['@'], marks['$'])
        cls.dock = marks['.']
        cls.directions = {'8': (0, -1), '4': (-1, 0), '6': (1, 0), '2': (0, 1)}

    def shape(self, text):
        buf = self.hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        self.hb.shape(self.shaper, buf)  # calt must be on by default in a normal text run
        ids = [item.codepoint for item in buf.glyph_infos]
        self.assertEqual([self.names[i] for i in ids[:-1]], ['blank'] * (len(text) - 1))
        self.assertEqual([pos.x_advance for pos in buf.glyph_positions], [0] * (len(text) - 1) + [896])
        return ids[-1]

    def ink(self, glyph):
        # Decode the physical positions of the colored components, not a claimed board ID in a name.
        colors = self.tt['COLR'].ColorLayers[self.names[glyph]]
        tiles = {}
        for layer in colors:
            if '.at' not in layer.name:
                continue
            ((piece, matrix),) = [c.getComponentInfo() for c in self.tt['glyf'][layer.name].components]
            x, y = matrix[-2:]
            self.assertEqual((x % 128, y % 128), (0, 0))
            tiles[piece] = x // 128, len(self.rows) - 1 - y // 128
        won = 'sealed' in tiles
        self.assertIn('done' if won else 'idle', tiles)
        player = tiles['porter']
        box = tiles['sealed' if won else 'crate']
        self.assertEqual(won, box == self.dock)
        self.assertEqual(tiles.get('target'), None if self.dock in (player, box) else self.dock)
        return player, box

    def step(self, state, velocity):
        (x, y), box = state
        dx, dy = velocity
        adj = x + dx, y + dy
        if box == self.dock or adj not in self.floor:
            return state
        if adj != box:
            return adj, box
        front = adj[0] + dx, adj[1] + dy
        return (adj, front) if front in self.floor else state

    def test_all_reachable_transitions_change_the_actual_print(self):
        seen = {self.start: '0'}
        q = deque([self.start])
        gids = set()
        count = 0
        self.assertEqual(self.ink(self.shape('0')), self.start)
        while q:
            here = q.popleft()
            prefix = seen[here]
            for key, direction in self.directions.items():
                route = prefix + key
                want = self.step(here, direction)
                glyph = self.shape(route)
                self.assertEqual(self.shape(route[1:]), glyph, route)  # no leading zero
                self.assertEqual(self.ink(glyph), want, route)
                gids.add(glyph)
                count += 1
                if want not in seen:
                    seen[want] = route
                    q.append(want)
        self.assertEqual(count, 1024)
        self.assertEqual(len(gids), 256)
        self.assertEqual(len(seen), len(self.tt['COLR'].ColorLayers))
        shortest = min(len(s) - 1 for (_, box), s in seen.items() if box == self.dock)
        self.assertEqual(shortest, 10)
        self.assertEqual(self.ink(self.shape(SOLUTION))[1], self.dock)

    def test_undo_blocked_push_win_and_reset(self):
        route = '0866'
        wall = self.shape(route)
        self.assertEqual(self.ink(wall), ((4, 3), (5, 3)))
        self.assertEqual(self.shape(route + '6'), wall)  # crate against the right wall
        self.assertEqual(self.ink(self.shape(route[:-1])), ((3, 3), (4, 3)))
        self.assertNotEqual(self.shape(SOLUTION[:-1]), self.shape(SOLUTION))
        self.assertEqual(self.shape(SOLUTION + '8624'), self.shape(SOLUTION))
        self.assertEqual(self.shape(SOLUTION + '0'), self.shape('0'))
        self.assertEqual(self.shape('0' + '84' * 70 + '0' + SOLUTION[1:]), self.shape(SOLUTION))

    @unittest.skipUnless(PRESS, 'install FreeType/Pillow for the print proofs')
    def test_published_impressions_come_from_the_shaped_ttf(self):
        import freetype
        from PIL import Image, ImageChops

        ft = freetype.Face(str(FONT))
        ft.set_pixel_sizes(0, 384)

        def print_route(s):
            ft.load_glyph(
                self.shape(s), freetype.FT_LOAD_RENDER | freetype.FT_LOAD_COLOR | freetype.FT_LOAD_NO_HINTING
            )
            b = ft.glyph.bitmap
            self.assertEqual(b.pixel_mode, freetype.FT_PIXEL_MODE_BGRA)
            return Image.frombytes('RGBA', (b.width, b.rows), bytes(b.buffer), 'raw', 'BGRA', b.pitch).convert(
                'RGB'
            )

        with Image.open(ART / 'proof.png') as panel:
            for x, s in [(16, '0866'), (368, '086')]:
                ink = print_route(s)
                sample = panel.crop((x, 57, x + ink.width, 57 + ink.height))
                self.assertIsNone(ImageChops.difference(ink, sample).getbbox())
        routes = (
            [SOLUTION[:i] for i in range(1, 4)]
            + ['0866', '086']
            + [SOLUTION[:i] for i in range(4, len(SOLUTION) + 1)]
        )
        with Image.open(ART / 'delivery.gif') as anim:
            self.assertEqual(anim.n_frames, len(routes))
            self.assertEqual(anim.info['loop'], 0)
            for i, s in enumerate(routes):
                anim.seek(i)
                ink = print_route(s)
                crop = anim.convert('RGB').crop((16, 57, 16 + ink.width, 57 + ink.height))
                error = ImageChops.difference(ink, crop)
                self.assertLess(max(hi for _, hi in error.getextrema()), 12, (i, s))
