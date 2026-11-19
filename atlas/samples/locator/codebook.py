"""Read a binary pattern, form oriented toroidal windows, decode bounded Hamming errors."""
import csv
from pathlib import Path


def load(path):
    with Path(path).open(newline='') as f:rows=list(csv.reader(f))
    if len(rows)!=65 or any(len(row)!=63 or any(v not in ('0','1') for v in row) for row in rows):raise ValueError('65 rows x 63 binary CSV columns required')
    return [[int(v) for v in row] for row in rows]


def signature(grid,x,y,size=6):
    value=0
    for dy in range(size):
        for dx in range(size):value=(value<<1)|grid[(y+dy)%65][(x+dx)%63]
    return value


def book(grid,size=6):return [(x,y,signature(grid,x,y,size)) for y in range(65) for x in range(63)]


def locate(entries,observed,radius=3):
    if type(observed)!=int or not 0<=observed<1<<36 or radius!=3:raise ValueError('36-bit observation and fixed radius 3 required')
    candidates=[{'x':x,'y':y,'distance':(code^observed).bit_count()} for x,y,code in entries if (code^observed).bit_count()<=radius]
    return {'accepted':len(candidates)==1,'position':candidates[0] if len(candidates)==1 else None,'candidate_count':len(candidates)}


def patch_text(value):return '\n'.join(f'{value:036b}'[i:i+6] for i in range(0,36,6))+'\n'


def parse_patch(text):
    lines=text.splitlines()
    if len(lines)!=6 or any(len(row)!=6 or set(row)-{'0','1'} for row in lines):raise ValueError('six lines of six bits required, known orientation')
    return int(''.join(lines),2)


def four_error_example(entries,x,y):
    original=next(code for xx,yy,code in entries if (xx,yy)==(x,y))
    for xx,yy,code in entries:
        difference=code^original
        if difference.bit_count()==7:
            bits=[i for i in range(36) if difference>>i&1][:4]
            observed=original
            for bit in bits:observed^=1<<bit
            return observed,{'x':xx,'y':yy},bits
    raise ValueError('no distance-seven partner')
