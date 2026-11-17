"""A frieze and its overlay, from the same four lines of typesetting.

Change a digit to quarter-turn that square. In this edition A must still reach
one of the four right-edge exits. Run `python atlas/samples/tile-frieze.py`.
"""
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[2] / 'assets'
ROWS = ('101010111', '011110010', '000110000', '101010001')
# Ports in clockwise order N, E, S, W. Each tile pairs its four edge midpoints.
PAIRS = (((0, 1), (2, 3)), ((0, 3), (2, 1)))
OFFSETS = ((0, -1), (1, 0), (0, 1), (-1, 0))
SIDE, X, Y = 40, 47, 17
START_ROW = 1


def track():
    c, r, port = 0, START_ROW, 3
    chain = []
    while 0 <= c < len(ROWS[0]) and 0 <= r < len(ROWS):
        pairs = PAIRS[int(ROWS[r][c])]
        j = next(j for j, pair in enumerate(pairs) if port in pair)
        chain.append((c, r, j))
        a, b = pairs[j]
        end = a if port == b else b
        dx, dy = OFFSETS[end]
        c, r, port = c+dx, r+dy, (end+2)%4
    if c != len(ROWS[0]):
        raise ValueError('A no longer reaches the numbered edge; choose another setting')
    return chain, r


def arc(c, r, j):
    flip = int(ROWS[r][c])
    a, b = PAIRS[flip][j]
    h = SIDE//2
    cx, cy = X+c*SIDE+h, Y+r*SIDE+h
    ax, ay = OFFSETS[a]
    bx, by = OFFSETS[b]
    return f'M{cx+ax*h} {cy+ay*h}a{h} {h} 0 0 {flip} {(bx-ax)*h} {(by-ay)*h}'


def render(answer):
    ink, paper, signal = '#253c61', '#e6edd4', '#a13d25'
    chain, exit_row = track()
    across, down = len(ROWS[0])*SIDE, len(ROWS)*SIDE
    start_y = Y + SIDE*(START_ROW+.5)
    ends = []
    for r in range(len(ROWS)):
        x, y = X+across+22, Y+SIDE*(r+.5)
        lit = answer and r == exit_row
        ends.append(f'<circle cx="{x}" cy="{y}" r="13" stroke="{ink}" fill="{signal if lit else paper}"/><text x="{x}" y="{y+6}" fill="{paper if lit else ink}">{r+1}</text>')
    paths = ''.join(arc(c,r,j) for r,row in enumerate(ROWS) for c in range(len(row)) for j in range(2))
    trace = ''.join(arc(c,r,j) for c,r,j in chain)
    overlay = f'<path d="{trace}" stroke="{signal}" stroke-width="8"/><path d="{trace}" stroke="{paper}" stroke-width="2" stroke-dasharray="3 4"/>' if answer else ''
    w, h = X*2 + across, Y*2 + down
    desc = f'Дорожка от А выделена пунктиром до выхода {exit_row+1}.' if answer else 'Проследи дорожку от А слева до одного из четырёх номеров справа.'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d" xml:lang="ru">
  <title id="t">Модульный форзац</title><desc id="d">{desc}</desc>
  <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="8" fill="{paper}" stroke="{ink}"/>
  <defs><clipPath id="print"><rect x="{X}" y="{Y}" width="{across}" height="{down}"/></clipPath></defs>
  <g clip-path="url(#print)" fill="none"><path d="{paths}" stroke="{ink}" stroke-width="5"/>{overlay}</g>
  <rect x="{X}" y="{Y}" width="{across}" height="{down}" fill="none" stroke="{ink}"/>
  <g font-family="monospace" font-size="18" font-weight="bold" text-anchor="middle">{''.join(ends)}
    <path d="M8 {start_y-13}H31L44 {start_y}l-13 13H8Z" fill="{signal}"/><text x="22" y="{start_y+6}" fill="{paper}">А</text>
  </g>
</svg>\n'''


if __name__ == '__main__':
    for name, answer in [('tile-frieze', False), ('tile-route', True)]:
        (ASSETS/f'{name}.svg').write_text(render(answer), encoding='utf-8')
    chain, row = track()
    print(f'A → {row+1}, {len(chain)} arcs')
