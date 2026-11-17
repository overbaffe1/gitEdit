"""Print the North cover in two compositions and a clean, STILL plate for a website.

Run `python atlas/samples/polar-press.py` (standard library only). Each export
is self-contained: the README never has to load a font, stylesheet or script.
"""
from html import escape
from math import cos, exp, sin
from pathlib import Path

OUT = Path(__file__).resolve().parents[2] / 'assets'
W, H = 1000, 280
NAME, STRAP = 'gitEdit', 'Мастерская README'  # Keep the cover name short.

# An opaque quiet colour under the type; the moon and horizon stay visible on the right.
PALETTES = """
    :root {
      --sky: #d9d9da; --haze: #ffdeb4; --ray: #3e9b8c; --shine: #ffedbe;
      --moon: #fff3c4; --moon-ink: #b76f5f; --distant: #bd8586;
      --middle: #6c8f89; --coast: #34595d; --edge: #edf1c5;
      --paper: #f4ecda; --ink: #1e3940; --rule: #546b68;
    }
    @media (prefers-color-scheme: dark) {
      :root {
        --sky: #171a33; --haze: #4e737a; --ray: #68d9ba; --shine: #c0f0bf;
        --moon: #ffd6a2; --moon-ink: #cf8167; --distant: #666480;
        --middle: #376765; --coast: #183f48; --edge: #93bfb1;
        --paper: #151e2d; --ink: #fff1d6; --rule: #b6cfc9;
      }
    }
"""
MOTION = """
    @media (prefers-reduced-motion: no-preference) {
      .curtain { animation: aurora 8s ease-in-out infinite alternate; }
      .middle { animation: drift 10s ease-in-out infinite alternate; }
      .near { animation: tide 10s ease-in-out infinite alternate; }
      @keyframes aurora { from { transform: translate(0, 0); } to { transform: translate(38px, -11px); } }
      @keyframes drift { from { transform: translateX(0); } to { transform: translateX(14px); } }
      @keyframes tide { from { transform: translateX(0); } to { transform: translateX(42px); } }
    }
"""


def silk():
    """One translucent ribbon with separate printed filaments along its lip."""
    upper, lower, threads = [], [], []
    for x in range(-60, W + 65, 8):
        y = 94 + 31*sin(x/105) + 18*sin(x/54 + .6) - 40*exp(-((x-636)/108)**2)
        length = 33 + 29*(1+cos(x/87)) + 12*sin(x/23)
        upper.append((x+21, y-length))
        lower.append((x, y))
        threads.append(f'M{x+21},{y-length:.1f} Q{x+4},{y-22:.1f} {x},{y:.1f}')
    points = lambda pts: ' '.join(f'{x:.0f},{y:.1f}' for x, y in pts)
    return f'''<g class="curtain">
      <polygon points="{points(upper + lower[::-1])}" fill="url(#silk)"/>
      <path d="{' '.join(threads)}" fill="none" stroke="url(#silk)" stroke-width="1.5"/>
      <polyline points="{points(lower)}" fill="none" stroke="var(--shine)" opacity=".65" stroke-width="1.6"/>
    </g>'''


FAR = 'M-50 202 43 178 102 187 161 168 217 187 287 157 322 170 397 146 457 169 496 152 532 161 590 128 620 147 688 101 713 121 735 108 786 151 815 137 861 166 914 127 948 150 990 130 1050 155V300H-50Z'
MID = 'M-50 223 28 207 92 219 152 194 209 207 256 180 322 204 398 176 455 187 509 155 535 166 569 151 609 177 655 153 707 194 749 178 800 190 868 151 896 163 929 147 1009 184 1050 168V300H-50Z'
NEAR = 'M-50 247 Q40 215 116 240T278 236Q368 201 437 219T574 224Q646 194 700 205T854 214Q920 188 1050 199V300H-50Z'


def landscape():
    # Contours are clipped to the nearest bank; translating the group keeps cuts aligned.
    cuts = '\n'.join(f'<use href="#bank-line" transform="translate(0 {dy})"/>' for dy in range(5,95,7))
    return f'''<rect width="1000" height="280" fill="url(#sky)"/>
    <rect width="1000" height="280" fill="url(#speck)"/>
    <g fill="none" stroke="var(--shine)" opacity=".72" stroke-width="1.3">
      <path d="M540 23v9m-4.5-4.5h9M936 70v11m-5.5-5.5h11M706 28v6m-3-3h6"/>
    </g>
    {silk()}
    <circle cx="796" cy="104" r="61" fill="var(--moon)"/>
    <circle cx="796" cy="104" r="61" fill="url(#disc-lines)"/>
    <ellipse cx="796" cy="104" rx="88" ry="24" transform="rotate(-21 796 104)" fill="none" stroke="var(--shine)" stroke-width="1.2"/>
    <path d="{FAR}" fill="var(--distant)"/>
    <g class="middle"><path d="{MID}" fill="var(--middle)"/>
      <path d="m509 155 26 11-15 2-5 13z m59-4 25 15-16-5-3 7z m300 0 28 12-20-3-6 7z" fill="var(--edge)" opacity=".6"/>
    </g>
    <g class="near"><path d="{NEAR}" fill="var(--coast)"/>
      <g clip-path="url(#bank)" fill="none" stroke="var(--edge)" stroke-width="1" opacity=".46">{cuts}</g>
    </g>'''


def render(kind, motion=False):
    compact, plate = kind == 'compact', kind == 'plate'
    w, h = (420, 197) if compact else (W, H)
    x = 20 if compact else 43
    title_y, title_px = (105, 62) if compact else (156, 106)
    strap_y, strap_px = (138, 18) if compact else (208, 25)
    text = '' if plate else f'''
    <rect width="{w}" height="{h}" fill="url(#quiet)"/>
    <g fill="var(--ink)">
      <rect x="{x}" y="22" width="10" height="10" fill="var(--rule)"/>
      <text x="{x+20}" y="32" font-family="monospace" font-size="{13 if compact else 16}" letter-spacing="1.7">ПОЛЕВОЕ БЮРО / 01</text>
      <text x="{x-3}" y="{title_y}" font-family="Georgia, 'DejaVu Serif', serif" font-size="{title_px}" font-weight="bold" letter-spacing="-5">{escape(NAME)}</text>
      <text x="{x}" y="{strap_y}" font-family="system-ui, sans-serif" font-size="{strap_px}" font-weight="600">{escape(STRAP)}</text>
      <path d="M{x} {h-29}h32" stroke="var(--rule)" stroke-width="2"/>
      <text x="{x+43}" y="{h-24}" font-family="monospace" font-size="{12 if compact else 14}" letter-spacing="1.5">СЕВЕР / АТЛАС ДВИЖЕНИЯ</text>
    </g>'''
    desc = ('Панорама без текста: полярное небо, луна и три плана побережья.' if plate else
            f'{escape(NAME)} — {escape(STRAP)}. Полярное сияние, луна и три плана побережья.')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d" xml:lang="ru">
  <title id="t">Север · {escape(NAME)}</title><desc id="d">{desc}</desc>
  <style>{PALETTES}{MOTION if motion else ''}  </style>
  <defs>
    <linearGradient id="sky" x2="0" y2="1" gradientUnits="objectBoundingBox"><stop stop-color="var(--sky)"/><stop offset="1" stop-color="var(--haze)"/></linearGradient>
    <linearGradient id="silk" x2=".2" y2="1" gradientUnits="objectBoundingBox"><stop stop-color="var(--ray)" stop-opacity="0"/><stop offset=".65" stop-color="var(--ray)" stop-opacity=".44"/><stop offset="1" stop-color="var(--shine)" stop-opacity=".84"/></linearGradient>
    <linearGradient id="quiet"><stop stop-color="var(--paper)" stop-opacity=".97"/><stop offset=".4" stop-color="var(--paper)" stop-opacity=".93"/><stop offset=".74" stop-color="var(--paper)" stop-opacity="0"/></linearGradient>
    <pattern id="speck" width="13" height="13" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r=".78" fill="var(--shine)" opacity=".34"/></pattern>
    <pattern id="disc-lines" patternUnits="userSpaceOnUse" width="7" height="7" patternTransform="rotate(-10)"><path d="M0 6h7" stroke="var(--moon-ink)" opacity=".34"/></pattern>
    <clipPath id="bank"><path d="{NEAR}"/></clipPath>
    <path id="bank-line" d="M-60 243Q28 207 117 230T280 228Q367 198 439 209T575 216Q648 183 713 199T865 203Q940 172 1060 193"/>
    <clipPath id="frame"><rect width="{w}" height="{h}" rx="{0 if plate else 12}"/></clipPath>
  </defs>
  <g clip-path="url(#frame)">
    <svg width="{w}" height="{h}" viewBox="{'320 0 597 280' if compact else '0 0 1000 280'}" preserveAspectRatio="xMaxYMid slice">{landscape()}</svg>{text}
  </g>
</svg>\n'''


if __name__ == '__main__':
    for kind, name in [('wide', 'polar-cover'), ('compact', 'polar-cover-compact')]:
        (OUT / f'{name}.svg').write_text(render(kind, motion=True), encoding='utf-8')
        (OUT / f'{name}-still.svg').write_text(render(kind), encoding='utf-8')
    (OUT / 'polar-plate.svg').write_text(render('plate'), encoding='utf-8')
