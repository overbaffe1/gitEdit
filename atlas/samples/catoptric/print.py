"""Print a physical anamorphosis, then reconstruct it by looking at the saved sheet.

Python 3.11+, numpy, Pillow, ReportLab, DejaVu fonts. All outputs are deterministic.
"""

import argparse
import base64
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

import numpy as np
from optics import AIM, AXIS, CARD, DIST, PAGE, SCALE, TOP, R, from_sheet, paper_to_card, sample, sight
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

HERE = Path(__file__).resolve().parent
OUTPUT = HERE.parents[2] / 'assets/catoptric'
INK, RUST, RULE, STOCK = '#244b50', '#98462b', '#9ba79d', '#fffdf6'


def font(face, size):
    return ImageFont.truetype(f'DejaVu{face}.ttf', size)


def form():
    """Full-size furniture: one labelled, non-reflecting sheet on the bench."""
    s = SCALE
    w, h = PAGE
    cx, cy = AXIS
    im = Image.new('RGB', (w * s, h * s), 'white')
    d = ImageDraw.Draw(im)

    def coord(seq):
        return tuple(round(x * s) for x in seq)

    def line(pts, ink=RULE, th=0.20):
        d.line(coord(pts), fill=ink, width=max(1, round(th * s)))

    def text(x, y, txt, face, size, ink=INK, anc='lm'):
        d.text(coord((x, y)), txt, font=font(face, round(s * size)), anchor=anc, fill=ink)

    def ring(x, y, r, ink, th):
        d.ellipse(coord((x - r, y - r, x + r, y + r)), outline=ink, width=round(th * s))

    line((9, 25.7, 288, 25.7))
    text(9, 8.4, 'КАБИНЕТ ОТРАЖЕНИЙ  /  I', 'SansMono-Bold', 2.9, RUST)
    text(8.5, 18, 'Морской конёк', 'Serif', 8.1)
    text(288, 9, 'ЗЕРКАЛЬНЫЙ ЦИЛИНДР   Ø 50 мм   /   от 80 мм высотой', 'SansMono-Bold', 3.0, INK, 'rm')
    text(288, 17, 'Глаз: 280 мм от оси по столу, 240 мм над листом.', 'Sans', 3.4, INK, 'rm')
    ring(cx, cy, R, INK, 0.25)
    ring(cx, cy, R - 2.1, RULE, 0.13)
    for sx, sy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        line((cx + sx * (R - 3), cy + sy * (R - 3), cx + sx * (R + 1), cy + sy * (R + 1)), RUST, 0.22)
    line((cx - 2, cy, cx + 2, cy), RUST, 0.25)
    line((cx, cy - 2, cx, cy + 2), RUST, 0.25)
    text(cx, cy + 9, 'МЕСТО ЗЕРКАЛА', 'SansMono-Bold', 2.7, INK, 'mm')
    text(cx, cy + 13, 'Ø 50 мм', 'SansMono', 2.6, INK, 'mm')
    # Verification scale and viewing direction are outside the fan, not part of the subject.
    line((10, 200, 60, 200), INK, 0.3)
    for k in range(11):
        line((10 + 5 * k, 200, 10 + 5 * k, 196.5 if k % 2 == 0 else 198.4), INK, 0.23)
    text(10, 195, '50 мм   /   проверка масштаба', 'SansMono', 2.7)
    line((cx, 204, cx, 196.5), RUST, 0.38)
    line((cx - 1.5, 198.6, cx, 196.5, cx + 1.5, 198.6), RUST, 0.38)
    text(cx + 4, 201, 'ЛИНИЯ ВЗГЛЯДА', 'SansMono-Bold', 2.7, RUST)
    text(288, 201, 'A4  /  АЛЬБОМ  /  100 %', 'SansMono-Bold', 2.8, INK, 'rm')
    return im


def expose(path):
    sheet = np.array(form())
    h, w = sheet.shape[:2]
    with Image.open(HERE / 'engraving.png') as art:
        source = np.array(art.convert('RGB'))
        sh, sw = source.shape[:2]
    x = (np.arange(w)[None, :] + 0.5) / SCALE - AXIS[0]
    # Tiles keep temporary arrays small at print resolution. The two margins remain untouched.
    for y0 in range(27 * SCALE, 195 * SCALE, 48):
        y1 = min(y0 + 48, 195 * SCALE, h)
        y = AXIS[1] - (np.arange(y0, y1)[:, None] + 0.5) / SCALE
        u, v, valid = paper_to_card(x, y)
        on = valid & (np.abs(u) <= CARD[0] / 2) & (np.abs(v) <= CARD[1] / 2)
        sheet[y0:y1][on] = np.rint(
            sample(source, (0.5 + u[on] / CARD[0]) * sw - 0.5, (0.5 - v[on] / CARD[1]) * sh - 0.5)
        ).astype('uint8')
    Image.fromarray(sheet).save(path, optimize=True, dpi=(SCALE * 25.4, SCALE * 25.4))


def table_color(x, y):
    grain = (np.sin(y * 0.57 + x * 0.052) * 1.9 + np.sin(y * 1.7 + x * 0.02) + np.cos(x * 0.03) * 1.3)[
        ..., None
    ]
    return np.array((57, 78, 78)) + grain


def on_paper(x, y):
    return (np.abs(x) <= PAGE[0] / 2) & (y <= AXIS[1]) & (y >= AXIS[1] - PAGE[1])


def scene(sheet, size=(690, 680), window=(-55.5, 55.5, -48, 61.4), yaw=0.0, height=240.0, mirror=True):
    """Render a model, not a photo. Only `sheet` is a picture input to this function."""
    w, h = size
    left, right, low, high = window
    u = left + (np.arange(w)[None, :] + 0.5) * (right - left) / w
    v = high - (np.arange(h)[:, None] + 0.5) * (high - low) / h
    q = sight(u, v, yaw, height)
    fx, fy = q['floor_x'], q['floor_y']
    floor = np.where(on_paper(fx, fy)[..., None], from_sheet(sheet, fx, fy), table_color(fx, fy))
    if mirror:
        # A soft contact shadow and a turned metal rim make the two surfaces readable.
        floor *= (1 - 0.18 * np.exp(-np.maximum(0, np.hypot(fx, fy) - R) / 6))[..., None]
        x, y = q['x'], q['y']
        nx = q['nx']
        z = q['z']
        silver = np.exp(-(((nx + 0.87) / 0.12) ** 2)) + 0.65 * np.exp(-(((nx - 0.94) / 0.05) ** 2))
        wall = np.where(on_paper(x, y)[..., None], from_sheet(sheet, x, y), table_color(x, y))
        wall = wall * (0.98 - 0.12 * np.minimum(1, np.abs(nx) ** 4))[..., None] + silver[..., None] * 36
        rim = (z > TOP - 1.0) | (z < 0.55)
        metal = 93 + 95 * silver + 26 * np.cos(nx * 14)
        wall = np.where(rim[..., None], np.stack((metal, metal + 8, metal + 8), axis=-1), wall)
        floor = np.where(q['side'][..., None], wall, floor)
        # Top cap is not a second picture: a spun-metal finish in eye-relative coordinates.
        focal = np.hypot(DIST - R, height - AIM)
        tc = (TOP - height) / (AIM - height + v * (DIST - R) / focal)
        capx = tc * u
        capy = -DIST + tc * (DIST - R + v * (height - AIM) / focal)
        cr = np.hypot(capx, capy)
        phi = np.arctan2(capy, capx)
        value = 147 + 30 * np.sin(2 * phi + 0.6) + 12 * np.cos(4 * phi) + 4 * np.cos(cr * 8)
        value = np.where(cr > R - 0.45, 198, value)
        value = np.where((cr > R - 1.25) & (cr <= R - 0.8), 112, value)
        floor = np.where(q['cap'][..., None], np.stack((value - 8, value + 3, value + 3), axis=-1), floor)
    return Image.fromarray(np.uint8(np.rint(np.clip(floor, 0, 255))))


def proof(sheet_path, out):
    with Image.open(sheet_path) as src:
        sheet = np.array(src.convert('RGB'))
    view = scene(sheet)
    # Two honest views: the flat fan at left and a pinhole view of exactly those inks at right.
    cover = Image.new('RGB', (1056, 564), STOCK)
    d = ImageDraw.Draw(cover)
    d.rectangle((0, 0, 1055, 66), fill=INK)
    d.text((26, 32), 'Зеркальный конёк', font=font('Serif', 38), anchor='lm', fill=STOCK)
    d.text((1030, 34), 'ОПТИЧЕСКИЙ КАБИНЕТ  /  I', font=font('SansMono', 18), anchor='rm', fill='#eac697')
    left = Image.fromarray(sheet).crop((18 * SCALE, 28 * SCALE, 279 * SCALE, 193 * SCALE))
    left.thumbnail((523, 360), Image.Resampling.LANCZOS)
    d.rectangle((16, 80, 552, 514), fill='white', outline=RULE)
    cover.paste(left, (22 + (523 - left.width) // 2, 81 + (433 - left.height) // 2))
    # A tighter blackline around the computed camera image separates it from the paper view.
    view = view.resize((439, 433), Image.Resampling.LANCZOS)
    cover.paste(view, (591, 81))
    d.rectangle((590, 80, 1030, 514), outline=INK)
    d.text((21, 539), '01   Чернила на листе', font=font('Serif', 23), anchor='lm', fill=INK)
    d.text((591, 539), '02   Те же чернила в отражении', font=font('Serif', 23), anchor='lm', fill=INK)
    d.text((33, 106), 'А4   /   ВИД СВЕРХУ', font=font('SansMono', 16), anchor='lm', fill=RUST)
    cover.save(out / 'proof.png', optimize=True)
    # The narrow README shows the actual mirror at usable size, not unreadably small panels.
    view.save(out / 'mirror.png', optimize=True)


def publish(out):
    out.mkdir(parents=True, exist_ok=True)
    sheet = out / 'sheet.png'
    expose(sheet)
    pdf = canvas.Canvas(
        str(out / 'sheet-a4.pdf'), pagesize=tuple(n * mm for n in PAGE), invariant=1, pageCompression=1
    )
    pdf.setTitle('Морской конёк — зеркальная анаморфоза')
    pdf.setAuthor('gitEdit')
    # Let ReportLab name the image object by its pixels, not the output directory name.
    with Image.open(sheet) as raster:
        pdf.drawImage(ImageReader(raster), 0, 0, PAGE[0] * mm, PAGE[1] * mm)
    pdf.showPage()
    pdf.save()
    proof(sheet, out)
    template = (HERE / 'bench.html.in').read_text(encoding='utf-8')
    if template.count('@@SHEET@@') != 1:
        raise ValueError('Missing sheet slot in viewer')
    html = template.replace('@@SHEET@@', base64.b64encode(sheet.read_bytes()).decode('ascii'))
    with ZipFile(out / 'bench.zip', 'w') as archive:
        archive.writestr(ZipInfo('mirror.html'), html.encode(), compress_type=ZIP_DEFLATED)
        archive.writestr(
            ZipInfo('sheet-a4.pdf'), (out / 'sheet-a4.pdf').read_bytes(), compress_type=ZIP_DEFLATED
        )


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out', type=Path, default=OUTPUT)
    publish(p.parse_args().out)
