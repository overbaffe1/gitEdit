"""Turn the 16 calendar weeks in snake-weeks.csv into a rotatable ASCII STL.

python atlas/samples/weekly-skyline.py
Updates the source STL, the visitor-facing STL and its static plate, never the README.
A unit of height is one commit. Every week is a separate closed solid;
streets are the spaces between buildings. No network or extra packages.
"""
import argparse
import csv
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent


def read_weeks():
    with (HERE / 'snake-weeks.csv').open() as file:
        rows = list(csv.DictReader(file))
    start = date.fromisoformat(rows[0]['date_utc'])
    if len(rows) != 112 or start.weekday() != 0:
        raise ValueError('Expected 16 complete weeks starting on Monday')
    for i, row in enumerate(rows):
        if row['date_utc'] != (start + timedelta(days=i)).isoformat() or int(row['commits']) < 0:
            raise ValueError(f'Invalid calendar row: {row}')
    return [sum(int(row['commits']) for row in rows[i:i+7]) for i in range(0, len(rows), 7)]


def build(heights):
    lines = ['solid weekly_skyline']
    for i, h in enumerate(heights):
        if h == 0:
            continue
        x, y = (i % 4)*14, (i // 4)*14
        square = [(x,y), (x+10,y), (x+10,y+10), (x,y+10)]
        vertices = [(u,v,z) for z in (0,h) for u,v in square]
        sides = [('0 0 -1',(0,3,2,1)), ('0 0 1',(4,5,6,7)),
                 ('0 -1 0',(0,1,5,4)), ('1 0 0',(1,2,6,5)),
                 ('0 1 0',(2,3,7,6)), ('-1 0 0',(3,0,4,7))]
        for normal, (a,b,c,d) in sides:
            for tri in ((a,b,c),(a,c,d)):
                lines.extend((f'  facet normal {normal}', '    outer loop'))
                lines.extend('      vertex %d %d %d' % vertices[j] for j in tri)
                lines.extend(('    endloop', '  endfacet'))
    return '\n'.join([*lines,'endsolid weekly_skyline',''])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--update-readme', action='store_true', help='Legacy spelling; updates linked files only.')
    parser.parse_args()
    (HERE / 'weekly-skyline.stl').write_text(build(read_weeks()), encoding='ascii')
    from file_plates import publish_skyline
    publish_skyline()
