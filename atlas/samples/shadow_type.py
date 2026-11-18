"""G/I/T: one solid, three orthographic silhouettes. Run with Python 3.10+, Pillow and DejaVu fonts.

The STL, film and still are different exports of the same surface. No network access.
"""

import struct
from collections import defaultdict
from itertools import pairwise, product
from math import cos, pi, radians, sin
from pathlib import Path

OUT = Path(__file__).resolve().parents[2] / 'assets' / 'shadow-type'
GLYPHS = {
    'G': ('.#####.', '##...##', '##.....', '##.####', '##...##', '##...##', '.#####.'),
    'I': ('#######', '#######', '..###..', '..###..', '..###..', '#######', '#######'),
    'T': ('#######', '#######', '..###..', '..###..', '..###..', '..###..', '..###..'),
}
N = len(GLYPHS['G'])
# Azimuth/elevation in degrees. The top view has screen-right +Y, screen-up -X.
VIEWS = {'G': (0, 0), 'I': (90, 0), 'T': (90, 90)}
OBLIQUE = (35, 26)
W, H, SS = 672, 316, 2


def cells():
    return {
        (x, y, z)
        for x, y, z in product(range(N), repeat=3)
        if GLYPHS['G'][N - 1 - z][x] == '#' and GLYPHS['I'][N - 1 - z][y] == '#' and GLYPHS['T'][x][y] == '#'
    }


def surface(solid):
    """Only exposed quads, counterclockwise as seen from outside."""
    faces = []
    for cell in sorted(solid):
        for axis, side in product(range(3), (-1, 1)):
            neighbor = list(cell)
            neighbor[axis] += side
            if tuple(neighbor) in solid:
                continue
            normal = [0, 0, 0]
            normal[axis] = side
            quad = []
            for a, b in ((0, 0), (1, 0), (1, 1), (0, 1)):
                p = list(cell)
                p[axis] += int(side > 0)
                p[(axis + 1) % 3] += a
                p[(axis + 2) % 3] += b
                quad.append(tuple(p))
            faces.append((tuple(normal), tuple(quad if side > 0 else reversed(quad))))
    return faces


def stl(faces):
    data = bytearray(b'gitEdit / G I T / orthographic specimen'.ljust(80, b'\0'))
    data.extend(struct.pack('<I', 2 * len(faces)))
    for normal, (a, b, c, d) in faces:
        for tri in ((a, b, c), (a, c, d)):
            data.extend(struct.pack('<12fH', *normal, *(4 * v for p in tri for v in p), 0))
    return bytes(data)


def basis(azimuth, elevation):
    a, e = radians(azimuth), radians(elevation)
    return (
        (cos(a), sin(a), 0),
        (-sin(a) * sin(e), cos(a) * sin(e), cos(e)),
        (sin(a) * cos(e), -cos(a) * cos(e), sin(e)),
    )


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def edges(quad):
    return zip(quad, quad[1:] + quad[:1])


def poses(steps=16):
    """Hold each exact reading; the last transition meets the first frame without a cut."""
    stops = [OBLIQUE, *VIEWS.values(), OBLIQUE]
    for j, (a, b) in enumerate(pairwise(stops)):
        for k in range(steps):
            t = (1 - cos(pi * k / steps)) / 2
            yield tuple(x + (y - x) * t for x, y in zip(a, b)), (1050 if j == 0 else 1250) if k == 0 else 70


class Proof:
    """A two-ink specimen card. The dark print is drawn from the mesh, never from font text."""

    def __init__(self, faces, count):
        from PIL import Image, ImageDraw, ImageFilter, ImageFont

        self.Image, self.Draw = Image, ImageDraw.Draw
        self.faces = faces
        self.vertices = {v for _, quad in faces for v in quad}
        incident = defaultdict(set)
        for normal, quad in faces:
            for a, b in edges(quad):
                incident[tuple(sorted((a, b)))].add(normal)
        self.creases = {edge for edge, normals in incident.items() if len(normals) > 1}
        self.mono = ImageFont.truetype('DejaVuSansMono.ttf', 14 * SS)
        self.bold = ImageFont.truetype('DejaVuSansMono-Bold.ttf', 15 * SS)
        self.small = ImageFont.truetype('DejaVuSansMono.ttf', 12 * SS)
        self.paper = Image.new('RGB', (W * SS, H * SS), '#153c39')
        d = self.Draw(self.paper)
        d.rectangle(self.box(404, 0, W, H), fill='#f6ecd7')
        # A fine register, not perspective decoration that could be mistaken for part of a letter.
        for x in range(19, 400, 14):
            for y in range(55, 259, 14):
                d.ellipse(self.box(x, y, x + 0.7, y + 0.7), fill='#345450')
        self.rule(d, (19, 43), (383, 43), '#55756c')
        self.rule(d, (19, 273), (383, 273), '#55756c')
        self.rule(d, (424, 43), (652, 43), '#baa990')
        self.rule(d, (424, 273), (652, 273), '#baa990')
        self.text(d, (19, 22), 'ЛИТЕРА  /  GIT', self.bold, '#f6e8c9')
        self.text(d, (383, 22), 'ТИП  03', self.small, '#b8c9b9', 'rm')
        self.text(d, (425, 22), 'ПРОЕКЦИЯ', self.bold, '#3a423d')
        self.text(d, (20, 294), 'ОДНА ФОРМА', self.small, '#c5d4c4')
        self.text(d, (383, 294), f'{count} ЯЧЕЕК', self.small, '#c5d4c4', 'rm')
        for x, sx in [(438, 1), (638, -1)]:
            for y, sy in [(67, 1), (250, -1)]:
                self.rule(d, (x, y), (x + sx * 8, y), '#bfa989')
                self.rule(d, (x, y), (x, y + sy * 8), '#bfa989')
        shade = Image.new('L', self.paper.size)
        self.Draw(shade).ellipse(self.box(115, 235, 278, 253), fill=120)
        self.paper.paste('#071f21', (0, 0, *self.paper.size), shade.filter(ImageFilter.GaussianBlur(6 * SS)))

    @staticmethod
    def box(x, y, xx, yy):
        return tuple(round(v * SS) for v in (x, y, xx, yy))

    @staticmethod
    def text(d, xy, text, font, color, anchor='lm'):
        d.text(tuple(v * SS for v in xy), text, font=font, fill=color, anchor=anchor)

    @staticmethod
    def rule(d, a, b, color):
        d.line([tuple(round(v * SS) for v in p) for p in (a, b)], fill=color, width=SS)

    def draw_form(self, d, pose, center, scale, ink=None):
        right, up, front = basis(*pose)
        projected, depths = {}, {}
        for v in self.vertices:
            p = tuple(i - N / 2 for i in v)
            projected[v] = (
                round(SS * (center[0] + scale * dot(p, right))),
                round(SS * (center[1] - scale * dot(p, up))),
            )
            depths[v] = dot(p, front)
        visible = [(sum(depths[v] for v in q) / 4, n, q) for n, q in self.faces if dot(n, front) > 1e-8]
        for depth, n, q in sorted(visible):
            if ink:
                color = ink
            else:
                # All poses use the same patinated brass; recessed surfaces carry less light.
                metal = (250, 197, 119) if n[2] else (158, 99, 67) if n[0] else (224, 153, 90)
                level = sum(v[2] for v in q) / (4 * N)
                shine = 0.85 + 0.05 * depth + 0.16 * level + 0.10 * dot(n, front) ** 6
                color = tuple(min(255, round(c * shine)) for c in metal)
            d.polygon([projected[v] for v in q], fill=color)
            if not ink:
                # Brushed tooling follows the material through every turn, not the screen.
                start = projected[q[0]]
                ux, uy = (b - a for a, b in zip(start, projected[q[1]]))
                vx, vy = (b - a for a, b in zip(start, projected[q[3]]))
                for mark in (1, 3, 6):
                    offset = (3 * q[0][0] + 5 * q[0][1] + 7 * q[0][2] + mark) % 11 / 48
                    pt = (start[0] + offset * ux + mark / 8 * vx, start[1] + offset * uy + mark / 8 * vy)
                    d.line(
                        (pt, (pt[0] + (0.67 - offset) * ux, pt[1] + (0.67 - offset) * uy)),
                        fill=tuple(max(0, c - 8) for c in color),
                        width=1,
                    )
                for a, b in edges(q):
                    if tuple(sorted((a, b))) in self.creases:
                        d.line(
                            (projected[a], projected[b]),
                            fill=tuple(min(255, c + 38) for c in color),
                            width=SS,
                        )

    def frame(self, pose, *, proof=False):
        im = self.paper.copy()
        d = self.Draw(im)
        self.draw_form(d, pose, (201, 158), 20.8)
        labels = ('СПЕРЕДИ', 'СБОКУ', 'СВЕРХУ')
        reading = 'ТРИ ВИДА' if proof else 'ПОВОРОТ'
        for i, key in enumerate(VIEWS.values()):
            if proof:
                y = 88 + i * 70
                self.draw_form(d, key, (479, y), 6.6, ink='#293d36')
                self.text(d, (536, y), labels[i], self.mono, '#465448')
            else:
                self.draw_form(d, key, (454 + i * 83, 294), 3.1, ink='#3c4b43')
                if all(abs(a - b) < 1e-8 for a, b in zip(pose, key)):
                    reading = labels[i]
                    self.rule(d, (437 + i * 83, 309), (471 + i * 83, 309), '#b35332')
        if proof:
            self.text(d, (425, 294), 'ОРТОГОНАЛЬНЫЕ ВИДЫ', self.small, '#665b4c')
        else:
            self.draw_form(d, pose, (538, 159), 15.0, ink='#293d36')
        self.text(d, (651, 22), reading, self.small, '#665b4c', 'rm')
        return im.resize((W, H), self.Image.Resampling.LANCZOS)


def export(out=OUT):
    from PIL import Image

    out.mkdir(parents=True, exist_ok=True)
    solid = cells()
    faces = surface(solid)
    (out / 'git.stl').write_bytes(stl(faces))
    card = Proof(faces, len(solid))
    card.frame(OBLIQUE, proof=True).save(out / 'proof.png', optimize=True)
    # One palette for every frame, otherwise the field and the type shimmer between angles.
    sample = Image.new('RGB', (W, H * 4))
    for i, pose in enumerate([OBLIQUE, *VIEWS.values()]):
        sample.paste(card.frame(pose), (0, i * H))
    palette = sample.quantize(colors=160)
    frames, durations = [], []
    for pose, duration in poses():
        frames.append(card.frame(pose).quantize(palette=palette, dither=Image.Dither.NONE))
        durations.append(duration)
    frames[0].save(
        out / 'git.gif',
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        disposal=1,
        optimize=True,
    )


if __name__ == '__main__':
    export()
