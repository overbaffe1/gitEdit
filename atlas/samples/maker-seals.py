"""Make project marks from names; no service, JS or third-party artwork.

python atlas/samples/maker-seals.py                            # gallery set
python atlas/samples/maker-seals.py my-project mark.svg --label «Проект» --orbit
"""
import argparse
import hashlib
import math
from html import escape
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[2] / 'assets'
PALETTES = [('#f5e4bd', '#244c4e', '#3b6c66'), ('#f8dbca', '#633449', '#a94e51'),
            ('#dfddf1', '#43345c', '#776298'), ('#d9e8d9', '#28483e', '#517059')]


def ornament(key):
    digest = hashlib.sha256(key.encode('utf-8')).digest()
    lobes = 3 + digest[3] % 7
    rotation = digest[1] * math.tau / 256
    depth = 0.19 + digest[2] / 1500
    pts = []
    for i in range(160):
        a = math.tau * i / 160
        r = 32 * (1 + depth * math.cos(a*lobes) + .055*math.cos(2*a*lobes))
        pts.append(f'{82+r*math.cos(a+rotation):.1f},{75+r*math.sin(a+rotation):.1f}')
    return 'M'+' '.join(pts)+'Z', PALETTES[digest[5] % len(PALETTES)]


def render(key, label, orbit=False):
    shape, (paper, ink, accent) = ornament(key)
    label = escape(label)
    motion = '''
  <style>
    @media (prefers-reduced-motion: no-preference) {
      .rim { transform-origin: 82px 75px; animation: orbit 32s linear infinite; }
      @keyframes orbit { to { transform: rotate(360deg); } }
    }
  </style>''' if orbit else ''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="164" height="165" viewBox="0 0 164 165" role="img" aria-labelledby="t d" xml:lang="ru">
  <title id="t">Марка · {label}</title><desc id="d">Форма розетки получена из имени {escape(key)}. Под ней постоянная подпись: {label}.</desc>{motion}
  <defs>
    <path id="type" d="M82 21a54 54 0 1 1 0 108a54 54 0 1 1 0-108Z"/>
    <path id="flower" d="{shape}"/>
  </defs>
  <rect x="1" y="1" width="162" height="163" rx="8" fill="{paper}" stroke="{accent}"/>
  <circle cx="82" cy="75" r="64" fill="none" stroke="{ink}" stroke-width="2"/>
  <circle cx="82" cy="75" r="47" fill="none" stroke="{accent}"/>
  <g class="rim"><text font-family="monospace" font-size="10" font-weight="bold" fill="{ink}"><textPath href="#type" textLength="334" lengthAdjust="spacing">GITEDIT · БЮРО ФОРМЫ · СЕРИЯ ЗНАКОВ · </textPath></text></g>
  <use href="#flower" fill="{accent}" stroke="{ink}" stroke-width="1.3"/>
  <g fill="none" stroke="{paper}" stroke-width="2">
    <use href="#flower" transform="translate(82 75) scale(.78) translate(-82 -75)"/>
    <use href="#flower" transform="translate(82 75) scale(.51) translate(-82 -75)"/>
  </g>
  <circle cx="82" cy="75" r="6.5" fill="{paper}" stroke="{ink}"/>
  <text x="82" y="155" text-anchor="middle" fill="{ink}" font-size="15" font-family="system-ui, sans-serif" font-weight="700">{label}</text>
</svg>\n'''


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('seed', nargs='?')
    parser.add_argument('output', nargs='?', type=Path)
    parser.add_argument('--label')
    parser.add_argument('--orbit', action='store_true')
    args = parser.parse_args()
    if args.seed is None and args.output is None and not args.label and not args.orbit:
        for key, label in [('crystal','Кристалл'), ('skyline','Квартал'), ('reel','Кинолента')]:
            (ASSETS / f'seal-{key}.svg').write_text(render(key, label, key=='crystal'), encoding='utf-8')
    elif args.seed and args.output:
        args.output.write_text(render(args.seed, args.label or args.seed, args.orbit), encoding='utf-8')
    else:
        parser.error('supply both a seed and an output path, or neither for the gallery set')
