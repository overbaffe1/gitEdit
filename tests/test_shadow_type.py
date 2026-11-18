"""Read the distributed STL back independently: the silhouettes must be in the mesh, not just the GIF."""

import struct
import sys
import unittest
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'atlas/samples'))
import shadow_type as typecase


class ShadowTypeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = (ROOT / 'assets/shadow-type/git.stl').read_bytes()
        cls.triangles = [
            (row[:3], (row[3:6], row[6:9], row[9:12])) for row in struct.iter_unpack('<12fH', cls.raw[84:])
        ]

    def test_print_is_one_closed_surface(self):
        self.assertEqual(len(self.triangles), struct.unpack_from('<I', self.raw, 80)[0])
        self.assertEqual(self.raw, typecase.stl(typecase.surface(typecase.cells())))
        # Opposite windings on every shared edge, with no loose pieces or interior faces.
        edges = defaultdict(list)
        for i, (_, tri) in enumerate(self.triangles):
            for a, b in zip(tri, tri[1:] + tri[:1]):
                edges[tuple(sorted((a, b)))].append((a, i))
        neighbors = defaultdict(set)
        for pair in edges.values():
            self.assertEqual(len(pair), 2)
            (a, i), (b, j) = pair
            self.assertNotEqual(a, b)
            neighbors[i].add(j)
            neighbors[j].add(i)
        stack, seen = [0], {0}
        while stack:
            unseen = neighbors[stack.pop()] - seen
            stack.extend(unseen)
            seen.update(unseen)
        self.assertEqual(len(seen), len(self.triangles))

    def test_front_side_top_read_git(self):
        projected = {char: set() for char in 'GIT'}
        for normal, tri in self.triangles:
            # Samples strictly inside each triangle; one grid cell is four STL units wide.
            x, y, z = (int(sum(p[i] for p in tri) / 12) for i in range(3))
            if normal == (0, -1, 0):
                projected['G'].add((x, 6 - z))
            elif normal == (1, 0, 0):
                projected['I'].add((y, 6 - z))
            elif normal == (0, 0, 1):
                projected['T'].add((y, x))
        for char, rows in typecase.GLYPHS.items():
            expected = {(x, y) for y, row in enumerate(rows) for x, bit in enumerate(row) if bit == '#'}
            self.assertEqual(projected[char], expected, char)

    def test_motion_and_print_links(self):
        art = ROOT / 'assets/shadow-type'
        gif = (art / 'git.gif').read_bytes()
        png = (art / 'proof.png').read_bytes()
        self.assertEqual(gif[:6], b'GIF89a')
        self.assertIn(b'NETSCAPE2.0', gif)
        self.assertEqual(png[:8], b'\x89PNG\r\n\x1a\n')
        self.assertEqual(struct.unpack_from('<HH', gif, 6), struct.unpack_from('>II', png, 16))
        text = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertIn('<a href="assets/shadow-type/git.stl"><picture>', text)
        self.assertIn('media="(prefers-reduced-motion: reduce)" srcset="assets/shadow-type/proof.png"', text)
        self.assertIn('<img src="assets/shadow-type/git.gif"', text)
        self.assertIn('](assets/shadow-type/git.stl)', text)
