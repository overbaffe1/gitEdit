"""Naborny Sklad: compile a one-crate room into a real OpenType state machine.

Python 3.11+ and fonttools. Each digit is substituted in the context of the preceding
board glyph; a second lookup blanks earlier boards. The underlying text stays intact.
"""

import argparse
from collections import deque
from itertools import groupby
from pathlib import Path

from fontTools.colorLib.builder import buildCOLR, buildCPAL
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[2] / 'assets/typecase'
ROOM = (HERE / 'room.txt').read_text('ascii').splitlines()
ROWS, COLS = len(ROOM), len(ROOM[0])
PLAN = ''.join(ROOM)
START = (PLAN.index('@'), PLAN.index('$'))
DOCK = PLAN.index('.')
# The solid perimeter lets a single flattened index describe a position.
DIRECTIONS = {'8': -COLS, '6': 1, '2': COLS, '4': -1}
U, TILE, EM = 8, 16, 1024
WIDTH, HEIGHT = COLS * TILE * U, ROWS * TILE * U
PAPER, WALL, DOT, TARGET, PORTER, CRATE, SEAL = range(7)
INKS = ('f5ebcd', '364d54', 'b9bea3', '16716a', '29373e', 'b0512c', '126952')


def move(state, delta):
    player, box = state
    if box == DOCK or PLAN[player + delta] == '#':
        return state
    player += delta
    if player == box:
        if PLAN[box + delta] == '#':
            return state
        box += delta
    return player, box


def graph():
    """Reachable positions only; histories leading to the same room share one glyph."""
    if (
        any(len(row) != COLS or row[0] != '#' or row[-1] != '#' for row in ROOM)
        or any(c != '#' for c in ROOM[0] + ROOM[-1])
        or any(PLAN.count(c) != 1 for c in '@$.')
    ):
        raise ValueError('Need a rectangular walled room with one player, crate and dock')
    queue = deque([START])
    paths = {START: '0'}
    while queue:
        here = queue.popleft()
        for digit, delta in DIRECTIONS.items():
            there = move(here, delta)
            if there not in paths:
                paths[there] = paths[here] + digit
                queue.append(there)
    return paths


def tag(state):
    return f'room.p{state[0]:02}.b{state[1]:02}'


def bitmap(rows):
    """Turn the horizontal runs of a little ink cut into clockwise TrueType contours."""
    pen = TTGlyphPen(None)
    h = len(rows)
    for y, row in enumerate(rows):
        x = 0
        for bit, run in groupby(row):
            end = x + sum(1 for _ in run)
            if bit == '#':
                left, right = x * U, end * U
                bottom, top = (h - y - 1) * U, (h - y) * U
                pen.moveTo((left, bottom))
                pen.lineTo((left, top))
                pen.lineTo((right, top))
                pen.lineTo((right, bottom))
                pen.closePath()
            x = end
    return pen.glyph()


def tile(fn, w=TILE, h=TILE):
    return bitmap([''.join('#' if fn(x, y) else '.' for x in range(w)) for y in range(h)])


DIGITS = {
    '0': ('111', '101', '101', '101', '111'),
    '1': ('010', '110', '010', '010', '111'),
    '2': ('111', '001', '111', '100', '111'),
    '4': ('101', '101', '111', '001', '001'),
    '6': ('111', '100', '111', '101', '111'),
    '8': ('111', '101', '111', '101', '111'),
    'O': ('111', '101', '101', '101', '111'),
    'K': ('101', '110', '100', '110', '101'),
}


def lettering(text, x, y, scale=1):
    if x < 0 or y < 0 or y >= 5 * scale:
        return False
    letter, col = divmod(x // scale, 4)
    return letter < len(text) and col < 3 and DIGITS[text[letter]][y // scale][col] == '1'


def composition(glyphs, pieces):
    pen = TTGlyphPen(glyphs)
    for name, x, y in pieces:
        pen.addComponent(name, (1, 0, 0, 1, x, y))
    return pen.glyph()


def build(path):
    paths = graph()
    gs = {'.notdef': tile(lambda x, y: x in (1, 14) or y in (1, 14)), 'blank': bitmap([])}
    for digit in DIRECTIONS:
        gs['key' + digit] = tile(lambda x, y, c=digit: lettering(c, x - 5, y - 3, 2))
    gs['paper'] = tile(lambda x, y: True, COLS * TILE, ROWS * TILE)
    gs['brick'] = tile(
        lambda x, y: (
            y % 8 != 0
            and (x + 8 * (y // 8)) % 16 != 0
            and not (y % 8 == 2 and (x + 8 * (y // 8)) % 16 in (2, 3))
        )
    )
    gs['floor'] = tile(lambda x, y: (x, y) in ((1, 1), (2, 1), (1, 2)))
    gs['target'] = tile(lambda x, y: abs(x - 7.5) + abs(y - 7.5) in (4, 5) or (x in (1, 14) and y in (5, 10)))
    gs['porter'] = bitmap(
        [
            '.......##.......',
            '.......##.......',
            '.....######.....',
            '...##########...',
            '..############..',
            '..##........##..',
            '..##.##..##.##..',
            '..##........##..',
            '...##########...',
            '.....######.....',
            '..############..',
            '..##.######.##..',
            '.....######.....',
            '.....##..##.....',
            '....###..###....',
            '................',
        ]
    )
    gs['crate'] = tile(
        lambda x, y: (
            1 <= x <= 14
            and 1 <= y <= 14
            and (
                x in (1, 14)
                or y in (1, 14)
                or (3 <= x <= 12 and 3 <= y <= 12 and (abs(x - y) <= 1 or abs(x + y - 15) <= 1))
            )
        )
    )
    gs['sealed'] = bitmap(
        [
            '................',
            '.##############.',
            '.##############.',
            '.##############.',
            '.##########..##.',
            '.#########..###.',
            '.########..####.',
            '.###..##..#####.',
            '.####....######.',
            '.#####..#######.',
            '.##############.',
            '.##############.',
            '.##############.',
            '.##############.',
            '.##############.',
            '................',
        ]
    )
    # A cast panel in the lintel reads 01 until the actual crate reaches its socket.
    for name, text in [('idle', '01'), ('done', 'OK')]:
        gs[name] = tile(
            lambda x, y, t=text: (
                (1 <= x <= 46 and y in (1, 14))
                or (1 < y < 14 and x in (1, 46))
                or (y in (7, 8) and x in (5, 6, 41, 42))
                or lettering(t, x - 17, y - 3, 2)
            ),
            48,
            16,
        )

    def origin(pos):
        y, x = divmod(pos, COLS)
        return x * TILE * U, (ROWS - 1 - y) * TILE * U

    lintel = COLS // 2 - 1
    gs['masonry'] = composition(
        gs, [('brick', *origin(i)) for i, c in enumerate(PLAN) if c == '#' and not lintel <= i < lintel + 3]
    )
    gs['dots'] = composition(gs, [('floor', *origin(i)) for i, c in enumerate(PLAN) if c != '#'])

    def placed(name, pos):
        key = f'{name}.at{pos:02}'
        if key not in gs:
            gs[key] = composition(gs, [(name, *origin(pos))])
        return key

    layers = {}
    for state in paths:
        p, b = state
        won = b == DOCK
        paints = [
            ('paper', PAPER),
            ('masonry', WALL),
            ('dots', DOT),
            (placed('done' if won else 'idle', lintel), SEAL if won else WALL),
        ]
        if DOCK not in (b, p):
            paints.append((placed('target', DOCK), TARGET))
        paints.extend(
            [(placed('sealed' if won else 'crate', b), SEAL if won else CRATE), (placed('porter', p), PORTER)]
        )
        layers[tag(state)] = paints
        # Monochrome readers get the same contours, minus the opaque paper background.
        gs[tag(state)] = composition(gs, [(name, 0, 0) for name, _ in paints[1:]])

    fb = FontBuilder(EM, isTTF=True)
    fb.setupGlyphOrder(list(gs))
    fb.setupCharacterMap({ord('0'): tag(START), **{ord(c): 'key' + c for c in DIRECTIONS}})
    fb.setupGlyf(gs)
    fb.setupHorizontalMetrics(
        {
            name: (
                0 if name == 'blank' else TILE * U if name.startswith('key') else WIDTH,
                getattr(shape, 'xMin', 0),
            )
            for name, shape in gs.items()
        }
    )
    fb.setupHorizontalHeader(ascent=HEIGHT, descent=0, lineGap=0)
    fb.setupNameTable(
        {
            'familyName': 'Typecase Dock',
            'styleName': 'Regular',
            'uniqueFontIdentifier': 'gitEdit:TypecaseDock:1',
            'fullName': 'Typecase Dock Regular',
            'psName': 'TypecaseDock-Regular',
            'version': 'Version 1.000',
        }
    )
    fb.setupOS2(
        sTypoAscender=HEIGHT, sTypoDescender=0, sTypoLineGap=0, usWinAscent=HEIGHT, usWinDescent=0, fsType=0
    )
    fb.setupPost()
    font = fb.font
    font['CPAL'] = buildCPAL([[tuple(v / 255 for v in bytes.fromhex(c + 'ff')) for c in INKS]])
    font['COLR'] = buildCOLR(layers, version=0, glyphMap=font.getReverseGlyphMap())
    # One left-to-right contextual lookup. The result is already the previous board
    # when the next digit is visited. No fixed maximum number of moves in the font.
    turns = [
        f"sub {tag(s)} key{c}' by {tag(move(s, delta))};" for s in paths for c, delta in DIRECTIONS.items()
    ]
    # If the field is empty (or its initial 0 was selected), the first move starts at the entrance.
    turns += [f"sub key{c}' by {tag(move(START, delta))};" for c, delta in DIRECTIONS.items()]
    features = [
        'languagesystem DFLT dflt;',
        'languagesystem latn dflt;',
        '@boards = [' + ' '.join(map(tag, paths)) + '];',
        'feature calt {',
        'lookup Walk {',
        *turns,
        '} Walk;',
        "lookup Clear { sub @boards' @boards by blank; } Clear;",
        '} calt;',
    ]
    addOpenTypeFeaturesFromString(font, '\n'.join(features))
    # Fixed specimen date (2026-11-17, seconds since the OpenType epoch) makes builds reproducible.
    font['head'].created = font['head'].modified = 3_877_718_400
    font.recalcTimestamp = False
    path.parent.mkdir(exist_ok=True, parents=True)
    font.save(path)
    return paths


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=OUT / 'dock.ttf')
    args = parser.parse_args()
    states = build(args.out)
    print(
        f'{args.out}: {len(states)} boards; shortest delivery: {next(p for (_, b), p in states.items() if b == DOCK)}'
    )
