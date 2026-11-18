"""Пиксельная ночь — призрак над городом, чистые прямоугольники и SMIL."""
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[2] / "assets"

# 80x40 pixels, each 8px = 640x320 viewBox
# palette: dusk
PIXEL = 8
W, H = 80, 40

def rect(x, y, w=1, h=1, fill="#000"):
    return f'<rect x="{x*PIXEL}" y="{y*PIXEL}" width="{w*PIXEL}" height="{h*PIXEL}" fill="{fill}"/>'

# city skyline heights (in pixels)
city = [6,9,7,11,5,13,8,10,6,12,7,9,11,6,14,9,7,10,8,12,6,9,7,15,8,10,6,11,9,7,10,8,13,6,9,12,7,10,8,11]
stars = [(5,4),(12,6),(28,3),(33,7),(45,5),(58,2),(62,8),(71,4),(18,9),(50,8)]

ghost_w=7
ghost_data = [
    "  ███  ",
    " █████ ",
    "███████",
    "███████",
    "███████",
    "█ █ █ █",
    "       ",
]
ghost_colors = {"█": "#eef", " ": None}
blink_y = 2  # eye row

svg_parts = []
svg_parts.append('<svg xmlns="http://www.w3.org/2000/svg" width="640" height="320" viewBox="0 0 640 320" role="img">')
svg_parts.append('<title>Пиксельная ночь</title><desc>Пиксельный город ночью, над ним парит призрак и моргает.</desc>')
svg_parts.append('<rect width="640" height="320" fill="#0b0f1a"/>')
# sky gradient via horizontal bands
for i in range(22):
    alpha = 1 - i/22
    # from #1a1a2e to #16213e to #0f3460
    r = int(11 + i*1.2)
    g = int(15 + i*0.8)
    b = int(26 + i*6)
    svg_parts.append(f'<rect x="0" y="{i*PIXEL}" width="640" height="{PIXEL}" fill="rgb({r},{g},{b})" opacity="1"/>')
# stars with twinkle
for sx, sy in stars:
    svg_parts.append(f'<g><rect x="{sx*PIXEL}" y="{sy*PIXEL}" width="{PIXEL}" height="{PIXEL}" fill="#ffe9a0" opacity="0.95"><animate attributeName="opacity" values="1;0.3;1" dur="{2+ (sx%3)}s" repeatCount="indefinite"/></rect></g>')
# moon
svg_parts.append(rect(66,3,6,6,"#fff8dc"))
svg_parts.append(rect(67,4,4,4,"#fff3b0"))
svg_parts.append(rect(68,3,1,1,"#e8e0b0"))
# city
base_y = 28
for x, h in enumerate(city[:80]):
    # building
    svg_parts.append(rect(x, base_y - h, 1, h, "#0a1628"))
    svg_parts.append(rect(x, base_y - h, 1, 1, "#1a2a4a"))
    # windows random
    if h>8 and x%3==0:
        svg_parts.append(rect(x, base_y - h + 2, 1, 1, "#ffde59" if x%6==0 else "#ff8a5c"))
        svg_parts.append(f'<rect x="{x*PIXEL}" y="{(base_y - h +2)*PIXEL}" width="{PIXEL}" height="{PIXEL}" fill="#ffde59" opacity="0.9"><animate attributeName="opacity" values="0.9;0.2;0.9" dur="{1.5 + (x%4)*0.3}s" repeatCount="indefinite"/></rect>' if x%7==0 else "")
# ground
svg_parts.append(rect(0,28,80,12,"#0d1b2a"))
svg_parts.append(rect(0,28,80,1,"#1e3a5f"))
# road dots
for x in range(0,80,6):
    svg_parts.append(rect(x,33,2,1,"#2a4a7a"))
# ghost group with float
svg_parts.append('<g id="ghost">')
svg_parts.append('  <animateTransform attributeName="transform" type="translate" values="0,0; 0,-12; 0,0" dur="2.4s" repeatCount="indefinite" additive="sum"/>')
ghost_x, ghost_y = 36, 10
for dy, row in enumerate(ghost_data):
    for dx, ch in enumerate(row):
        if ch == "█":
            # body
            svg_parts.append(f'<rect x="{(ghost_x+dx)*PIXEL}" y="{(ghost_y+dy)*PIXEL}" width="{PIXEL}" height="{PIXEL}" fill="#f0f4ff" stroke="#cbd5e1" stroke-width="0.5"/>')
# eyes
svg_parts.append(f'<rect x="{(ghost_x+2)*PIXEL}" y="{(ghost_y+blink_y)*PIXEL+2}" width="{PIXEL-3}" height="{PIXEL-3}" fill="#0b0f1a"><animate attributeName="opacity" values="1;1;0;1" dur="4s" repeatCount="indefinite" keyTimes="0;0.9;0.92;1"/></rect>')
svg_parts.append(f'<rect x="{(ghost_x+4)*PIXEL}" y="{(ghost_y+blink_y)*PIXEL+2}" width="{PIXEL-3}" height="{PIXEL-3}" fill="#0b0f1a"><animate attributeName="opacity" values="1;1;0;1" dur="4s" repeatCount="indefinite" keyTimes="0;0.9;0.92;1"/></rect>')
svg_parts.append('</g>')
# text
svg_parts.append('<g font-family="monospace" font-size="10" fill="#94a3b8">')
svg_parts.append('<text x="12" y="312" letter-spacing="2">ПИКСЕЛЬНАЯ НОЧЬ · ПРИЗРАК ПАРИТ · ОКНА МЕРЦАЮТ</text>')
svg_parts.append('<text x="470" y="312" font-size="8" fill="#475569">PIXEL · SMIL · NO JS · 80×40</text>')
svg_parts.append('</g>')
svg_parts.append('<style>@media (prefers-reduced-motion: reduce) { animate, animateTransform { display:none; } }</style>')
svg_parts.append('</svg>')

if __name__ == "__main__":
    out = ASSETS / "pixel-night.svg"
    out.write_text("\n".join(svg_parts), encoding="utf-8")
    print(f"written {out} {out.stat().st_size} bytes")
