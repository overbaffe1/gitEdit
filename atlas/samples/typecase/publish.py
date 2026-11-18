"""Build the TTF, print two specimens from its shaped output and pack the offline type tester.

Python 3.11+, requirements.txt and system DejaVu fonts. No browser or network needed at build time.
"""

import argparse
import base64
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

import freetype
import uharfbuzz as hb
from build_font import DOCK, HERE, OUT, build
from PIL import Image, ImageDraw, ImageFont

W, H = 720, 394
STOCK, INK, RUST, GREEN = '#f8f1df', '#253e44', '#a2462b', '#176459'
MUTED, RULE = '#566566', '#b4b7a4'
REPAIR = '086'
WRONG = REPAIR + '6'


class Press:
    def __init__(self, path):
        self.shaper = hb.Font(hb.Face(path.read_bytes()))
        self.printer = freetype.Face(str(path))

    def impression(self, text):
        """Only the released font gets to decide what these digits look like."""
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.shaper, buf, {'calt': True})
        advances = [p.x_advance for p in buf.glyph_positions]
        if not advances[-1] or any(advances[:-1]):
            raise ValueError(f'Expected one visible room for {text!r}')
        self.printer.set_pixel_sizes(0, 384)
        self.printer.load_glyph(
            buf.glyph_infos[-1].codepoint,
            freetype.FT_LOAD_RENDER | freetype.FT_LOAD_COLOR | freetype.FT_LOAD_NO_HINTING,
        )
        bm = self.printer.glyph.bitmap
        if bm.pixel_mode != freetype.FT_PIXEL_MODE_BGRA:
            raise ValueError('Use a FreeType build with COLR v0 support')
        # The first color layer is opaque paper, so premultiplied BGRA here has A=255.
        return Image.frombytes('RGBA', (bm.width, bm.rows), bytes(bm.buffer), 'raw', 'BGRA', bm.pitch).convert(
            'RGB'
        )


def face(name, size):
    return ImageFont.truetype(f'DejaVu{name}.ttf', size)


class Slip:
    def __init__(self, press):
        self.press = press
        self.serif = face('Serif', 28)
        self.key = face('SansMono-Bold', 47)
        self.mono = face('SansMono', 14)
        self.bold = face('SansMono-Bold', 16)
        self.digits = face('SansMono', 24)
        self.caption = face('Sans', 20)

    def paper(self, subtitle):
        im = Image.new('RGB', (W, H), STOCK)
        d = ImageDraw.Draw(im)
        d.rectangle((0, 0, W, 43), fill=INK)
        d.text((15, 20), 'Наборный склад', font=self.serif, fill=STOCK, anchor='lm')
        d.text((W - 16, 22), subtitle, font=self.mono, fill='#efcc9f', anchor='rm')
        return im, d

    def mount(self, im, d, text, x):
        board = self.press.impression(text)
        d.rectangle((x - 1, 56, x + board.width, 57 + board.height), outline=INK)
        im.paste(board, (x, 57))

    def frame(self, text, key, word):
        im, d = self.paper('ШРИФТОВАЯ ПРОБА   /   01')
        self.mount(im, d, text, 16)
        d.line((368, 57, 368, 345), fill=RULE, width=1)
        d.text((388, 72), 'КЛАВИША', font=self.bold, fill=MUTED, anchor='lm')
        tone = GREEN if word == 'Доставлено' else RUST
        d.rounded_rectangle((389, 95, 472, 173), radius=7, fill='#c3b79d')
        d.rounded_rectangle((387, 91, 470, 169), radius=7, fill='#fff9ea', outline=tone, width=2)
        d.text((429, 128), key, font=self.key, fill=tone, anchor='mm')
        d.text((485, 128), word, font=self.caption, fill=INK, anchor='lm')
        d.text((388, 218), 'А ПОД ШРИФТОМ — ТЕКСТ:', font=self.bold, fill=MUTED, anchor='lm')
        d.rectangle((386, 236, 703, 282), fill='#e6ddc6')
        d.text((398, 259), text, font=self.digits, fill=INK, anchor='lm')
        cursor = round(401 + self.digits.getlength(text))
        d.line((cursor, 247, cursor, 272), fill=tone, width=2)
        d.text((388, 319), '8 ↑    4 ←    2 ↓    6 →', font=self.bold, fill=GREEN, anchor='lm')
        d.line((16, 358, 704, 358), fill=RULE)
        d.text((16, 375), 'TYPECASE DOCK   /   TTF', font=self.mono, fill=MUTED, anchor='lm')
        d.text((704, 375), 'ОДИН ВИДИМЫЙ ГЛИФ', font=self.mono, fill=INK, anchor='rm')
        return im

    def proof(self):
        im, d = self.paper('ДВА ОТТИСКА   /   BACKSPACE')
        for x, text, label in [(16, WRONG, 'Лишний толчок'), (368, REPAIR, 'Стереть одну цифру')]:
            self.mount(im, d, text, x)
            d.text((x, 368), text, font=self.digits, fill=INK, anchor='lm')
            d.text((x + 336, 369), label, font=self.bold, fill=RUST if x == 16 else GREEN, anchor='rm')
        return im


def tape(solution):
    if not solution.startswith(REPAIR):
        raise ValueError('This specimen is written for the room with a right-wall trap')
    words = {'8': 'Вверх', '4': 'Влево', '2': 'Вниз', '6': 'Вправо'}
    for end, key in enumerate(solution, 1):
        text = solution[:end]
        if text == REPAIR:
            yield text, key, 'Толчок', 800
            yield WRONG, '6', 'У стены', 1250
            yield REPAIR, '⌫', 'Отмена толчка', 1150
        elif end == 1:
            yield text, key, 'Вход', 1300
        elif end == len(solution):
            yield text, key, 'Доставлено', 1800
        else:
            yield text, key, words[key], 480


def publish(out):
    ttf = out / 'dock.ttf'
    states = build(ttf)
    solution = next(path for (_, box), path in states.items() if box == DOCK)  # breadth-first order
    slip = Slip(Press(ttf))
    slip.proof().save(out / 'proof.png', optimize=True)
    shots = []
    durations = []
    for text, key, word, ms in tape(solution):
        shots.append(slip.frame(text, key, word))
        durations.append(ms)
    swatches = Image.new('RGB', (W, H * 4))
    for i, k in enumerate((0, 3, 4, -1)):
        swatches.paste(shots[k], (0, i * H))
    palette = swatches.quantize(colors=128)
    frames = [im.quantize(palette=palette, dither=Image.Dither.NONE) for im in shots]
    frames[0].save(
        out / 'delivery.gif',
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        disposal=1,
        optimize=True,
    )

    html = (HERE / 'dock.html.in').read_text('utf-8')
    if html.count('@@DOCK_TTF@@') != 1 or html.count('@@SOLUTION@@') != 1:
        raise ValueError('Missing specimen slot')
    html = html.replace('@@DOCK_TTF@@', base64.b64encode(ttf.read_bytes()).decode('ascii')).replace(
        '@@SOLUTION@@', solution
    )
    with ZipFile(out / 'typecase.zip', 'w') as archive:
        archive.writestr(ZipInfo('dock.html'), html.encode('utf-8'), compress_type=ZIP_DEFLATED)
    print(f'{len(states)} reachable rooms; {len(frames)} prints; {solution}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=OUT)
    publish(parser.parse_args().out)
