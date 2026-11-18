"""Print one RGBA field plate for two backgrounds. Python 3.10+, Pillow and DejaVu fonts.

Run python3 atlas/samples/twilight/print.py [--out DIRECTORY]. The registered L-mode
vignettes are press-ready ink coverages, 0 = clear. Their sum is at most 255. No network or theme detection.
"""

import argparse
from math import cos, sin, tau
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile, ZipInfo

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[2] / 'assets/twilight'
S = 2
SIZE = 360 * S, 428 * S
WHITE = (255, 255, 255)
NIGHT = (13, 17, 23)
COPPER = (165, 100, 53, 255)


def scale(*coords):
    return tuple(round(v * S) for v in coords)


def font(name, size):
    return ImageFont.truetype(f'DejaVu{name}.ttf', round(size * S))


def masks():
    for name, title, species, evening in [
        ('fox', 'Лисица', 'Vulpes vulpes', False),
        ('owl', 'Сипуха', 'Tyto alba', True),
    ]:
        plate = Image.new('L', SIZE)
        with Image.open(HERE / f'{name}.png') as cut:
            if cut.mode != 'L' or cut.size != (640, 640):
                raise ValueError(f'{name}: expected the registered 640 × 640 ink mask')
            plate.paste(cut, scale(20, 45))
        d = ImageDraw.Draw(plate)
        x, anchor = (344, 'rm') if evening else (16, 'lm')
        d.text(scale(x, 386), title, fill=222, font=font('Serif', 34), anchor=anchor)
        d.text(scale(x, 414), species, fill=210, font=font('SansMono', 13), anchor=anchor)
        cx, cy = (316 if evening else 44), 74
        if evening:
            d.ellipse(scale(cx - 12, cy - 12, cx + 12, cy + 12), fill=197)
            d.ellipse(scale(cx - 5, cy - 16, cx + 19, cy + 8), fill=0)
            for x, y, r in [(cx + 14, cy - 11, 3), (cx + 22, cy, 1.6)]:
                d.polygon(
                    [scale(x, y - r), scale(x + r * 0.55, y), scale(x, y + r), scale(x - r * 0.55, y)], fill=197
                )
        else:
            d.ellipse(scale(cx - 8, cy - 8, cx + 8, cy + 8), outline=197, width=2 * S)
            for j in range(12):
                a = tau * j / 12
                d.line(
                    [scale(cx + 11 * cos(a), cy + 11 * sin(a)), scale(cx + 16 * cos(a), cy + 16 * sin(a))],
                    fill=197,
                    width=S,
                )
        yield plate


def glass(day, night):
    # Straight (not premultiplied) PNG color. d units of dark paper + n units of white
    # paper are opaque; the rest is clear. On white n disappears, on dark d disappears.
    ds, ns = day.tobytes(), night.tobytes()
    rgba = bytearray()
    for d, n in zip(ds, ns, strict=True):
        a = d + n
        if a > 255:
            raise ValueError('Overinked pixel: dark and light ink coverages sum to more than 255')
        if not a:
            rgba.extend(b'\0\0\0\0')
        else:
            rgba.extend((d * k + n * 255 + a // 2) // a for k in NIGHT)
            rgba.append(a)
    sheet = Image.frombytes('RGBA', SIZE, bytes(rgba))
    # A common spot-color pass, outside both portraits. These registration marks never change.
    marks = Image.new('RGBA', SIZE)
    pen = ImageDraw.Draw(marks)
    pen.text(scale(16, 19), 'Б Е С Т И А Р И Й', font=font('SansMono-Bold', 11), fill=COPPER, anchor='lm')
    pen.text(scale(344, 19), 'ЛИСТ  /  01', font=font('SansMono', 11), fill=COPPER, anchor='rm')
    for y in (35, 363):
        pen.line([scale(16, y), scale(344, y)], fill=(*COPPER[:3], 165), width=S)
    for x, sign in [(8, 1), (352, -1)]:
        pen.line([scale(x, 185), scale(x + 10 * sign, 185)], fill=COPPER, width=S)
        pen.line([scale(x, 182), scale(x, 188)], fill=COPPER, width=S)
    return Image.alpha_composite(sheet, marks)


def proof(sheet):
    w, h = sheet.size
    spread = Image.new('RGB', (2 * w, h))
    for i, color in enumerate((WHITE, NIGHT)):
        backing = Image.new('RGBA', sheet.size, (*color, 255))
        spread.paste(Image.alpha_composite(backing, sheet).convert('RGB'), (i * w, 0))
    return spread


def export(out):
    out.mkdir(exist_ok=True, parents=True)
    png = out / 'glass.png'
    glass(*masks()).save(png, optimize=True)
    # Both proofs and the portable table use the actual finished PNG, not the original vignettes.
    with Image.open(png) as sheet:
        proof(sheet).save(out / 'proof.png', optimize=True)
    with ZipFile(out / 'table.zip', 'w') as archive:
        archive.writestr(ZipInfo('table.html'), (HERE / 'table.html').read_bytes(), compress_type=ZIP_DEFLATED)
        archive.writestr(ZipInfo('glass.png'), png.read_bytes(), compress_type=ZIP_STORED)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=OUT)
    export(parser.parse_args().out)
