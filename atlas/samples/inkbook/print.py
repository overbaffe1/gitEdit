"""Print three paired colour specimens and their GIMP/CSS swatches from palettes.csv."""

import argparse
import csv
from dataclasses import dataclass
from itertools import pairwise
from math import cos, radians, sin
from pathlib import Path
from string import Template
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
CSV = HERE.parent / 'palettes.csv'
OUT = HERE.parents[2] / 'assets/inkbook'


def rgb(code):
    return tuple(bytes.fromhex(code.removeprefix('#')))


def luminance(code):
    def linear(byte):
        s = byte / 255
        return s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4

    r, g, b = map(linear, rgb(code))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    low, high = sorted((luminance(a), luminance(b)))
    return (high + 0.05) / (low + 0.05)


@dataclass(frozen=True)
class Sample:
    name: str
    theme: str
    paper: str
    ink: str
    accent: str

    def legend(self, side):
        return {f'{side}_name': escape(self.name), f'{side}_paper': self.paper,
                f'{side}_ink': self.ink, f'{side}_accent': self.accent,
                f'{side}_ratio': f'{contrast(self.ink, self.paper):.2f}'.replace('.', ',')}


def etching():
    # Offset solid disc and a separate circular impression of the wave plate.
    lines = '\n'.join(f'<use href="#wave" transform="translate(0 {y})"/>' for y in range(48, 227, 7))
    return f'''<defs>
        <clipPath id="disc"><circle cx="103" cy="139" r="50"/></clipPath>
        <path id="wave" d="M42 0C69-19 81-20 106-2s38 19 61-2"/>
        <g id="ruling" clip-path="url(#disc)" fill="none">{lines}</g>
        <mask id="knockout" maskUnits="userSpaceOnUse" x="45" y="78" width="132" height="116">
          <rect x="45" y="78" width="132" height="116" fill="white"/>
          <use href="#ruling" stroke="black" stroke-width="3.8"/>
        </mask>
      </defs>
      <circle cx="120" cy="133" r="50" mask="url(#knockout)"/>
      <use href="#ruling" stroke="currentColor" stroke-width="1.7"/>
      <circle cx="103" cy="139" r="50" fill="none" stroke="currentColor"/>
      <path d="M170 95h11m-5.5-5.5v11M44 173h7m-3.5-3.5v7" fill="none" stroke="currentColor"/>'''


def pleat():
    # Leave a cut of paper between adjacent facets (no extra shade of ink).
    x, y = 113, 186
    points = []
    for i in range(15):
        angle = radians(203 + 9.5 * i)
        radius = 96 if i % 2 == 0 else 81
        points.append((x + radius * cos(angle), y + radius * sin(angle)))
    faces = []
    for i, (a, b) in enumerate(pairwise(points)):
        cx, cy = (x + a[0] + b[0]) / 3, (y + a[1] + b[1]) / 3
        coords = ' '.join(f'{cx + .95 * (px - cx):.2f},{cy + .95 * (py - cy):.2f}'
                          for px, py in [(x, y), a, b])
        ink = ' fill="currentColor"' if i % 2 else ''
        faces.append(f'<polygon points="{coords}"{ink}/>')
    return ('\n'.join(faces) + '\n<g fill="none" stroke="currentColor">'
            '<path d="M37 123a100 100 0 0 1 143-11" stroke-dasharray="1 4"/>'
            '<circle cx="113" cy="189" r="3"/><path d="M134 189h38m-3-3 3 3-3 3"/></g>')


def orbit():
    ticks = ''.join(f'<path d="M112 82v{5 if a % 90 == 0 else 2}" transform="rotate({a} 112 136)"/>'
                    for a in range(0, 360, 15))
    return f'''<g fill="none" stroke="currentColor">
        <circle cx="112" cy="136" r="48" stroke-dasharray="1 3"/>{ticks}
        <ellipse cx="112" cy="136" rx="76" ry="23" transform="rotate(-28 112 136)"/>
        <ellipse cx="112" cy="136" rx="33" ry="53" transform="rotate(-28 112 136)"/>
      </g>
      <path d="M112 101C115 125 121 132 145 136C121 140 116 148 112 172C108 148 102 140 79 136C102 132 109 124 112 101Z"/>
      <circle cx="112" cy="136" r="4.3" fill="currentColor"/>
      <path d="m164 98 2.5 6.5 6.5 2.5-6.5 2.5-2.5 6.5-2.5-6.5-6.5-2.5 6.5-2.5Z" fill="currentColor"/>
      <circle cx="53" cy="174" r="4"/><circle cx="65" cy="96" r="1.6" fill="currentColor"/>'''


# Pair by name *and* mode, not by CSV row position. All colour values live in the CSV.
PAIRS = (
    ('press', 'Ризограф', 'Фосфор', 'Линии оттиска', etching),
    ('blueprint', 'Чертёж', 'Чертёж', 'Складки веера', pleat),
    ('orbit', 'Созвездие', 'Созвездие', 'Звезда и две орбиты', orbit),
)


def css_rule(key, sample):
    # Decide using the unrounded ratio. Accent is always available as a decorative ink.
    link = sample.accent if contrast(sample.paper, sample.accent) >= 4.5 else sample.ink
    return (f'[data-inkbook="{key}"] {{\n  --ge-paper: {sample.paper};\n  --ge-ink: {sample.ink};\n'
            f'  --ge-accent: {sample.accent};\n  --ge-link: {link};\n}}')


def print_book(output):
    with CSV.open(encoding='utf-8', newline='') as source:
        rows = (Sample(r['Палитра'], r['Тема'], r['Фон'], r['Текст'], r['Акцент']) for r in csv.DictReader(source))
        samples = {(s.name, s.theme): s for s in rows}
    master = Template((HERE / 'card.svg.in').read_text(encoding='utf-8'))
    output.mkdir(parents=True, exist_ok=True)
    gpl = ['GIMP Palette', 'Name: gitEdit — Картотека красок', 'Columns: 3', '#']
    light, dark = [], []
    for n, (key, day_name, night_name, mark, draw) in enumerate(PAIRS, 1):
        day, night = samples[day_name, 'светлая'], samples[night_name, 'тёмная']
        art = master.substitute(number=f'{n:02}', mark_name=mark, engraving=draw(),
                                **day.legend('day'), **night.legend('night'))
        (output / f'{key}.svg').write_text(art, encoding='utf-8')
        for s in (day, night):
            for label, code in [('фон', s.paper), ('текст', s.ink), ('акцент', s.accent)]:
                r, g, b = rgb(code)
                gpl.append(f'{r:3} {g:3} {b:3}\t{s.name} / {s.theme} / {label}')
        light.append(css_rule(key, day))
        dark.append(css_rule(key, night))
    (output / 'inkbook.gpl').write_text('\n'.join(gpl) + '\n', encoding='utf-8')
    css = ('/* gitEdit | Choose a pair with data-inkbook="press", "blueprint" or "orbit". */\n'
           + '\n'.join(light) + '\n\n@media (prefers-color-scheme: dark) {\n'
           + '\n'.join('  ' + line for rule in dark for line in rule.splitlines()) + '\n}\n')
    (output / 'inkbook.css').write_text(css, encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=OUT, help='directory for the five printed files')
    print_book(parser.parse_args().out)
