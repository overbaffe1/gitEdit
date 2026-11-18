"""Rebuild the four-second stereo specimen, its README prints and the pocket scope.

python3 atlas/samples/aurelia/render.py [--out DIRECTORY]
Requires Pillow 10+ and DejaVu Sans/Serif/Mono fonts. Nothing is fetched at build or viewing time.
"""

import argparse
import base64
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from PIL import Image, ImageColor, ImageDraw, ImageFilter, ImageFont
from xy_signal import GAIN, RATE, SCAN, SCANS, read_wav, write_wav

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[2] / 'assets/aurelia'
W, H, S = 704, 348, 2
AQUA, AMBER, IRIS = '#9ff6d9', '#ffbc80', '#c2adff'
INK, MUTED = '#f7edda', '#adc1c3'


def scaled(p):
    return tuple(round(v * S) for v in p)


class Plate:
    def __init__(self, pcm):
        self.pcm = pcm
        self.paper = Image.new('RGB', scaled((W, H)), '#14232d')
        self.draw = ImageDraw.Draw(self.paper)
        self.serif = ImageFont.truetype('DejaVuSerif.ttf', 30 * S)
        self.mono = ImageFont.truetype('DejaVuSansMono.ttf', 12 * S)
        self.bold = ImageFont.truetype('DejaVuSansMono-Bold.ttf', 15 * S)
        self.text((18, 22), 'Аурелия', self.serif, INK)
        self.text((687, 26), 'АТЛАС СИГНАЛА   /   01', self.mono, '#d6cbb5', 'rm')
        self.line([(17, 47), (687, 47)], '#58696e')
        # The glass is deliberately low-contrast behind the actual PCM trace.
        glass = Image.new('RGB', (96, 68))
        px = glass.load()
        for y in range(68):
            for x in range(96):
                light = max(0.0, 1 - ((x - 50) / 60) ** 2 - ((y - 31) / 48) ** 2)
                px[x, y] = (round(6 + 3 * light), round(21 + 12 * light), round(29 + 12 * light))
        self.paper.paste(glass.resize(scaled((381, 261)), Image.Resampling.BICUBIC), scaled((16, 56)))
        for x in range(27, 392, 22):
            for y in range(66, 310, 22):
                self.draw.ellipse(scaled((x, y, x + 0.7, y + 0.7)), fill='#345052')
        self.draw.rounded_rectangle(scaled((16, 56, 397, 317)), radius=7 * S, outline='#4a6164', width=S)
        self.text((28, 74), 'X/Y', self.bold, '#97c3b8')
        self.text((383, 301), '60 Гц', self.mono, '#7c9d9a', 'rm')
        for cy, label, paint in [(123, 'L  /  ГОРИЗОНТАЛЬ', AMBER), (238, 'R  /  ВЕРТИКАЛЬ', IRIS)]:
            self.text((419, cy - 48), label, self.bold, paint)
            self.draw.rounded_rectangle(
                scaled((418, cy - 32, 686, cy + 32)), radius=4 * S, fill='#101c26', outline='#3b4d58', width=S
            )
            self.line([(426, cy), (678, cy)], '#364850')
            for x in range(426, 679, 42):
                self.line([(x, cy - 24), (x, cy + 24)], '#293a43')
        self.text((419, 298), 'Один обход луча', self.mono, MUTED)
        self.text((685, 298), '16,7 мс', self.mono, INK, 'rm')
        self.text((17, 332), 'СТЕРЕО   /   48 кГц', self.mono, '#d6cbb5')
        self.text((687, 332), '800 ПАР ОТСЧЁТОВ НА ОБХОД', self.mono, '#d6cbb5', 'rm')

    def text(self, p, s, font, fill, anchor='lm'):
        self.draw.text(scaled(p), s, fill=fill, font=font, anchor=anchor)

    def line(self, points, fill):
        self.draw.line([scaled(p) for p in points], fill=fill, width=S)

    def samples(self, scan):
        start = (scan % SCANS) * 2 * SCAN
        segment = self.pcm[start : start + 2 * SCAN]
        return list(zip(segment[::2], segment[1::2], strict=True))

    @staticmethod
    def xy(pairs):
        return [scaled((207 + 0.0306 * x, 174 - 0.0306 * y)) for x, y in pairs]

    def frame(self, scan, mark):
        im = self.paper.copy()
        samples = self.samples(scan)
        trace = self.xy(samples)
        # A short phosphor afterglow uses the preceding two scans of the *decoded* recording.
        beam = Image.new('L', im.size)
        d = ImageDraw.Draw(beam)
        for delta, level in [(2, 45), (1, 85), (0, 240)]:
            pts = self.xy(self.samples(scan - delta)) if delta else trace
            d.line(pts, fill=level, width=2 * S, joint='curve')
        im.paste('#348c81', (0, 0, *im.size), beam.filter(ImageFilter.GaussianBlur(3.8 * S)))
        im.paste('#5fc6a7', (0, 0, *im.size), beam.filter(ImageFilter.GaussianBlur(1.35 * S)))
        im.paste(AQUA, (0, 0, *im.size), beam)
        d = ImageDraw.Draw(im)
        for k, cy, color in ((0, 123, AMBER), (1, 238, IRIS)):
            pts = [scaled((426 + 252 * i / (SCAN - 1), cy - 26 * p[k] / GAIN)) for i, p in enumerate(samples)]
            x, y = pts[mark]
            d.line((x, (cy - 30) * S, x, (cy + 30) * S), fill='#5b7079', width=S)
            d.line(pts, fill=color, width=2 * S, joint='curve')
            d.ellipse((x - 3 * S, y - 3 * S, x + 3 * S, y + 3 * S), fill=INK)
        x, y = trace[mark]
        d.ellipse((x - 4 * S, y - 4 * S, x + 4 * S, y + 4 * S), fill='#ffe1a7', outline='#493e37', width=S)
        return im.resize((W, H), Image.Resampling.LANCZOS)


def draw_media(pcm, out):
    plate = Plate(pcm)
    still = plate.frame(0, SCAN // 5)
    still.save(out / 'trace.png', optimize=True)
    # Pure median-cut loses the thin orange and violet signals among all the glass pixels.
    # Reserve six short ink ramps in one shared palette so the channels keep their identities.
    palette = still.quantize(colors=56)
    colors = palette.getpalette()[: 56 * 3]
    for ink in (AQUA, AMBER, IRIS, INK, MUTED, '#ffe1a7'):
        ramp = list(zip(ImageColor.getrgb('#101c26'), ImageColor.getrgb(ink), strict=True))
        colors.extend(round(lo + (hi - lo) * step / 12) for step in range(1, 13) for lo, hi in ramp)
    palette.putpalette(colors)
    frames = []
    # 20 fps; the pale reading mark moves slowly so its matching points on L and R can be followed.
    for scan in range(0, SCANS, 3):
        mark = (SCAN // 5 + 2 * SCAN * scan // SCANS) % SCAN
        frames.append(plate.frame(scan, mark).quantize(palette=palette, dither=Image.Dither.NONE))
    frames[0].save(
        out / 'swim.gif',
        save_all=True,
        append_images=frames[1:],
        duration=1000 * 3 * SCAN // RATE,
        loop=0,
        optimize=True,
        disposal=1,
    )


def pack_scope(wav_path, out):
    template = (HERE / 'scope.html.in').read_text(encoding='utf-8')
    assert template.count('@@STEREO_WAV@@') == 1
    html = template.replace('@@STEREO_WAV@@', base64.b64encode(wav_path.read_bytes()).decode('ascii'))
    with ZipFile(out / 'scope.zip', 'w') as archive:
        archive.writestr(ZipInfo('aurelia.html'), html.encode('utf-8'), compress_type=ZIP_DEFLATED)


def export(out):
    out.mkdir(parents=True, exist_ok=True)
    wav = out / 'aurelia.wav'
    write_wav(wav)
    draw_media(read_wav(wav), out)
    pack_scope(wav, out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=OUT)
    export(parser.parse_args().out)
