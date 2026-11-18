"""Typeset local GIF timings as a GitHub Markdown block. Prints to stdout; edits no files.

Run from the repository root. No arguments: the three tracks in gitEdit.
For another reel: python3 atlas/samples/cue_sheet.py 'Сгиб=assets/night-shift/fold.gif'
Building needs Pillow; reading the score needs no images or scripts.
"""

import argparse
from dataclasses import dataclass
from html import escape
from itertools import accumulate
from pathlib import Path
from urllib.parse import quote

SLOTS = 16
BASE_MS = 400
INK = '·▁▂▃▄▅▆▇█'
DEMO = ('Набор=assets/facet-count.gif', 'Сгиб=assets/night-shift/fold.gif', 'Медуза=assets/aurelia/swim.gif')


@dataclass(frozen=True)
class Track:
    label: str
    href: str
    delays: tuple[int, ...]


def read_track(spec):
    from PIL import Image, ImageSequence

    label, sep, filename = spec.partition('=')
    path = Path(filename)
    if not sep or not label.strip() or not label.isprintable() or not filename or path.is_absolute() or '..' in path.parts:
        raise ValueError(f'ожидается Имя=путь/от/корня.gif: {spec!r}')
    with Image.open(path, formats=['GIF']) as im:
        delays = tuple(frame.info.get('duration', 0) for frame in ImageSequence.Iterator(im))
    if len(delays) < 2 or any(d <= 0 for d in delays):
        raise ValueError(f'{path}: нужны хотя бы два кадра с положительными задержками')
    return Track(label.strip(), '/' + quote(path.as_posix()), delays)


def endings(delays, step):
    """Count frame endings in (i * step, (i + 1) * step], including the last partial cell."""
    cells = [0] * ((sum(delays) + step - 1) // step)
    for end in accumulate(delays):
        cells[(end - 1) // step] += 1
    return cells


def ruler(step):
    axis = [' '] * (SLOTS + 1)  # room for a two-digit final tick above the right border
    rail = ['─'] * SLOTS
    for i in range(0, SLOTS, 5):
        number = str(i * step // 1000)  # five cells are always a whole number of seconds
        if len(number) <= min(5, len(axis) - i):
            axis[i:i + len(number)] = number
            rail[i] = '┬'
    return ' ' + ''.join(axis), '╭' + ''.join(rail) + '╮'


def typeset(tracks):
    totals = [sum(t.delays) for t in tracks]
    # One scale across all tracks. Never stretch a short reel across the full width.
    span = SLOTS * BASE_MS
    step = ((max(totals) + span - 1) // span) * BASE_MS
    rows = [endings(t.delays, step) for t in tracks]
    unit = (max(map(max, rows)) + 7) // 8
    times = [f'{ms // 1000},{ms % 1000 // 10:02}' for ms in totals]  # GIF precision: centiseconds
    time_label = 't, с'
    width = max(len(time_label), *(len(s) for s in times))
    axis, rail = ruler(step)
    lines = ['<pre>', f'{axis} <b>{time_label}</b>' + ' ' * (width - len(time_label) + 2) + '<b>ЛЕНТА</b>', rail]
    for track, cells, seconds in zip(tracks, rows, times, strict=True):
        strip = ''.join(INK[(n + unit - 1) // unit] for n in cells)
        link = f'<a href="{escape(track.href, quote=True)}">{escape(track.label)}</a>'
        lines.append(f'│{strip:<{SLOTS}}│ {seconds:>{width}}  {link}')
    lines += ['╰' + '─' * SLOTS + '╯', '</pre>']
    legend = ('`▁`…`█` — от 1 до 8.' if unit == 1 else
              f'`▁` — от 1 до {unit}, `▂` — от {unit + 1} до {2 * unit}, и так до `█`.')
    seconds_per_cell = f'{step // 1000},{step % 1000 // 100}'
    lines += ['', (f'Одна клетка — **{seconds_per_cell} с**. Высота — сколько кадров закончилось за это время: '
                   f'`·` — ни одного, {legend} Пробел — за концом петли.')]
    return '\n'.join(lines) + '\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('tracks', nargs='*', metavar='ИМЯ=ФАЙЛ.gif', help='GIF относительно корня репозитория')
    args = parser.parse_args()
    try:
        block = typeset([read_track(spec) for spec in args.tracks or DEMO])
    except ImportError:
        parser.exit(1, 'Для чтения GIF установи Pillow: python3 -m pip install Pillow\n')
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(block, end='')
