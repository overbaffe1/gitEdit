"""Impose eight upright folios on one A4; take the screen proof from the saved sheet."""

from itertools import groupby

import pymupdf
from PIL import Image
from reportlab.graphics.barcode import qrencoder
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# Sheet as seen on the printed side, in landscape. Rotate the entire upper row.
ORDER = ((5, 4, 3, 2), (6, 7, 8, 1))
W, H = 297 / 4, 210 / 2  # one panel, mm
INK, MUTED, RULE = '#232630', '#4c5359', '#b8b6aa'
PALETTES = [('#913d29', '#f9eee3'), ('#155f58', '#e7f2eb'), ('#593d71', '#f1eaf5')]
SANS, BOLD, SERIF, MONO = 'DejaVuSans', 'DejaVuSans-Bold', 'DejaVuSerif', 'DejaVuSansMono'


def text(c, x, top, value, face=SANS, size=3.1, ink=INK, right=False, width=None):
    available = width if width is not None else (x - 5 if right else W - 5 - x)
    advance = pdfmetrics.stringWidth(value, face, size)
    if advance > available:
        size *= available / advance
        if size < 2.35:
            raise ValueError(f'Укороти подпись для печати: {value}')
    c.setFillColor(ink)
    c.setFont(face, size)
    (c.drawRightString if right else c.drawString)(x, H - top, value)


def box(c, x, top, width, height, fill):
    c.setFillColor(fill)
    c.rect(x, H - top - height, width, height, stroke=0, fill=1)


def line(c, x1, y1, x2, y2, ink=RULE, width=.22):
    c.setStrokeColor(ink)
    c.setLineWidth(width)
    c.line(x1, H - y1, x2, H - y2)


def paragraph(c, value, x, top, width, face, size, leading, bottom, ink=INK):
    """Wrap by embedded font metrics. Fail instead of printing over the next panel or QR."""
    buf = ''
    for word in value.split():
        if pdfmetrics.stringWidth(word, face, size) > width:
            raise ValueError(f'Слово не помещается на полосе: {word}')
        candidate = (buf + ' ' + word).strip()
        if pdfmetrics.stringWidth(candidate, face, size) > width:
            text(c, x, top, buf, face, size, ink)
            top += leading
            buf = word
        else:
            buf = candidate
    if top > bottom:
        raise ValueError(f'Текст не помещается на полосе: {value}')
    text(c, x, top, buf, face, size, ink)
    return top


def qr(c, url, x, top, size):
    code = qrencoder.QRCode(None, qrencoder.QRErrorCorrectLevel.M)
    code.addData(url)
    code.make()
    pitch = size / (code.getModuleCount() + 8)  # four white modules on every side
    box(c, x, top, size, size, '#ffffff')
    c.linkURL(url, (x, H - top - size, x + size, H - top), relative=1, thickness=0)
    c.setFillColor('#151922')
    # One filled path, so adjacent modules do not acquire pale hairlines during rasterisation.
    path = c.beginPath()
    for row, modules in enumerate(code.modules):
        col = 0
        for dark, run in groupby(modules):
            count = sum(1 for _ in run)
            if dark:
                path.rect(x + (col + 4) * pitch, H - top - (row + 5) * pitch, count * pitch, pitch)
            col += count
    c.drawPath(path, stroke=0, fill=1)


def furniture(c, issue, n):
    text(c, 6, 9, 'ЛИЧНЫЙ ТИРАЖ  /  ' + issue['issue'], MONO, 2.45, MUTED)
    text(c, W - 6, 9, f'{n:02} / 08', MONO, 2.45, MUTED, right=True)
    line(c, 6, 11.5, W - 6, 11.5)


def cover(c, issue):
    text(c, 6, 23, issue['author'], MONO, 3.6)
    paragraph(c, issue['title'], 5, 42, W - 10, SERIF, 12.4, 12, 60)
    line(c, 6, 64, W - 6, 64, INK, .7)
    # A small index printed in the three inks of this edition.
    for i, (work, (ink, tint)) in enumerate(zip(issue['works'], PALETTES, strict=True)):
        x = 6 + i * 21
        box(c, x, 68, 19.4, 20, tint)
        box(c, x, 68, 19.4, .9, ink)
        text(c, x + 2, 78.5, str(work['number']), SERIF, 6.9, ink, width=16)
        text(c, x + 2, 85.2, work['unit'], SANS, 2.7, ink, width=16)
    text(c, 6, 97, 'ИЗБРАННЫЕ РАБОТЫ  /  3 РАЗВОРОТА', MONO, 2.4, MUTED)


def plate(c, w, ink, tint):
    box(c, 5, 15, W - 10, 64, tint)
    text(c, 8, 22, w['project'], MONO, 3.0, ink)
    text(c, 7, 43.5, str(w['number']), SERIF, 23, ink)
    text(c, 9, 50, w['unit'], BOLD, 4.2, ink)
    marks = w['marks']
    nx, ny = len(marks[0]), len(marks)
    dx, dy = (W - 20) / nx, 20 / ny
    c.setLineWidth(.38)
    c.setStrokeColor(ink)
    c.setFillColor(ink)
    for row, values in enumerate(marks):
        for col, mark in enumerate(values):
            x, y = 10 + (col + .5) * dx, H - 54 - (row + .5) * dy
            if mark == '|':
                # A count of strings, not a reconstruction of the rig or an audio waveform.
                c.line(x, y - 9, x, y + 2 + 7 * (col + 1) / nx)
                c.circle(x, y - 9, .58, fill=1, stroke=0)
            else:
                c.circle(x, y, .31 * min(dx, dy), fill=int(mark), stroke=1)
    paragraph(c, w['key'], 6, 86, W - 12, SANS, 2.95, 4.1, 99, MUTED)


def story(c, w, ink):
    text(c, 6, 20, w['project'], MONO, 3.0, ink)
    last = paragraph(c, w['title'], 6, 31, W - 12, SERIF, 6.35, 6.9, 39)
    paragraph(c, w['body'], 6, last + 8, W - 12, SANS, 3.18, 4.45, 65)
    line(c, 6, 69, W - 6, 69, ink, .5)
    qr(c, w['proof']['url'], 4.5, 71.5, 29)
    text(c, 37, 79, 'ИСТОЧНИК', MONO, 2.7, ink)
    paragraph(c, w['proof']['label'], 37, 86, W - 43, BOLD, 3.25, 4.2, 98)


def back(c, issue):
    text(c, 6, 27, 'Колофон', SERIF, 8.7)
    paragraph(c, 'Три работы, у каждой — число и файл, в котором его можно проверить.',
              6, 39, W - 12, SANS, 3.5, 5, 56)
    line(c, 6, 60, W - 6, 60, INK, .6)
    qr(c, issue['profile'], 4.5, 62.5, 28)
    text(c, 37, 76, 'ВЕСЬ', MONO, 3.0, MUTED)
    text(c, 37, 81, 'ПРОФИЛЬ', MONO, 3.0, MUTED)
    text(c, 6, 97, issue['profile'].removeprefix('https://'), MONO, 3, INK)


def compose(issue, file):
    c = canvas.Canvas(str(file), pagesize=(4 * W * mm, 2 * H * mm), invariant=1, pageCompression=1)
    c.setTitle(issue['title'] + ' — карманное портфолио')
    c.setAuthor(issue['author'])
    c.scale(mm, mm)
    for row, numbers in enumerate(ORDER):
        for col, n in enumerate(numbers):
            c.saveState()
            if row == 0:
                c.translate((col + 1) * W, 2 * H)
                c.rotate(180)
            else:
                c.translate(col * W, 0)
            furniture(c, issue, n)
            if n == 1:
                cover(c, issue)
            elif n == 8:
                back(c, issue)
            else:
                i = (n - 2) // 2
                if n % 2 == 0:
                    plate(c, issue['works'][i], *PALETTES[i])
                else:
                    story(c, issue['works'][i], PALETTES[i][0])
            c.restoreState()
    # Dashed creases; one continuous slit along the middle two panels. Outer margins are printer-safe.
    c.setStrokeColor(RULE)
    c.setLineWidth(.19)
    c.setDash(1.2, 1.2)
    for col in (1, 2, 3):
        c.line(col * W, 5, col * W, 2 * H - 5)
    c.line(5, H, W, H)
    c.line(3 * W, H, 4 * W - 5, H)
    c.setDash()
    c.setStrokeColor(INK)
    c.setLineWidth(.32)
    c.line(W, H, 3 * W, H)
    c.showPage()
    c.save()


def proof(pdf, png):
    # Folios 4 and 5 are adjacent but upside down in the upper left quarter-pair of the sheet.
    with pymupdf.open(pdf) as doc:
        page = doc[0]
        clip = pymupdf.Rect(0, 0, page.rect.width / 2, page.rect.height / 2)
        pix = page.get_pixmap(matrix=pymupdf.Matrix(2, 2), clip=clip, alpha=False)
        Image.frombytes('RGB', (pix.width, pix.height), pix.samples).transpose(Image.Transpose.ROTATE_180).save(png)


def print_edition(issue, out, fonts):
    for face in (SANS, BOLD, SERIF, MONO):
        file = fonts / (face + '.ttf')
        if not file.is_file():
            raise ValueError(f'Не найден {file}. Укажи каталог шрифтов DejaVu через --fonts.')
        pdfmetrics.registerFont(TTFont(face, str(file)))
    pdf = out / 'issue-a4.pdf'
    compose(issue, pdf)
    proof(pdf, out / 'spread.png')
