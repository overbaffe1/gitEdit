#!/usr/bin/env python3
"""Five rolling-circle exhibits, with exact CSS rotation relationships and stills."""
import argparse
from html import escape
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TAU = math.tau
PHASE = .7
SPECS = {
    'tusi': ('01 / ПАРА ТУСИ', 150, 75, 'inside',
             ['R : r = 2 : 1', 'Точка идёт по диаметру', 'Круг → прямая']),
    'deltoid': ('02 / ДЕЛЬТОИДА', 150, 50, 'inside',
                ['R : r = 3 : 1', 'Три острых вершины', 'Внутреннее качение']),
    'astroid': ('03 / АСТРОИДА', 150, 37.5, 'inside',
                ['R : r = 4 : 1', 'Четыре острых вершины', 'x = R cos³(t)', 'y = R sin³(t)']),
    'cardioid': ('04 / КАРДИОИДА', 65, 65, 'outside',
                 ['R : r = 1 : 1', 'Внешнее качение', 'Одна острая вершина']),
    'cycloid': ('05 / ЦИКЛОИДА', 65, 65, 'line',
                ['Качение по прямой', 'x = r(t − sin t)', 'y = r(1 − cos t)', 'Петля: один оборот']),
}


def geometry(kind,R,r,t):
    """Return center x/y, absolute wheel angle and marker x/y in local diagram units."""
    if kind=='line':
        center=(r*t,-r)
        angle=t
        point=(r*t-r*math.sin(t),-r+r*math.cos(t))
    else:
        distance=R-r if kind=='inside' else R+r
        angle=-(R-r)/r*t if kind=='inside' else (R+r)/r*t
        center=(distance*math.cos(t),distance*math.sin(t))
        sign=1 if kind=='inside' else -1
        point=(center[0]+sign*r*math.cos(angle),center[1]+sign*r*math.sin(angle))
    return (*center,angle,*point)


def text(x,y,value,size=15,color='#d8e6f0'):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}">{escape(value)}</text>'


def curve(kind,R,r,ox,oy):
    points=[]
    for i in range(721):
        *_,x,y=geometry(kind,R,r,i*TAU/720)
        points.append((ox+x,oy+y))
    return 'M'+' L'.join(f'{x:.4f},{y:.4f}' for x,y in points)


def draw(name,still=False):
    title,R,r,kind,notes=SPECS[name]
    ox,oy=(100,425) if kind=='line' else (315,290)
    t=PHASE if kind!='line' else 1.2
    degrees=math.degrees(t)
    speed=-(R/r) if kind=='inside' else R/r
    body=''
    if kind=='line':
        body+=f'<path d="M35 {oy}H650" stroke="#7994ab" stroke-width="2"/>'
        # Exact linear translation plus exact rotation; reset after one arch.
        start=0 if not still else t
        wheel_x=ox+r*start
        angle=math.degrees(start)
        wheel=f'<g class="travel" style="transform:translate({wheel_x:.6f}px,{oy-r:.6f}px)"><g class="spin" style="transform:rotate({angle:.6f}deg)">'
        wheel+=f'<circle r="{r}" fill="#55d6d0" fill-opacity=".06" stroke="#55d6d0" stroke-width="2"/><path d="M0 0V{r}" stroke="#55d6d0"/><circle r="4" fill="#55d6d0"/><circle cy="{r}" r="6" fill="#ffb879"/></g></g>'
        motion=f'@keyframes travel{{from{{transform:translate({ox}px,{oy-r}px)}}to{{transform:translate({ox+TAU*r:.9f}px,{oy-r}px)}}}}@keyframes spin{{from{{transform:rotate(0deg)}}to{{transform:rotate(360deg)}}}}.travel{{animation:travel 14s linear infinite}}.spin{{animation:spin 14s linear infinite}}'
    else:
        body+=f'<circle cx="{ox}" cy="{oy}" r="{R}" fill="none" stroke="#7994ab" stroke-width="2"/>'
        distance=R-r if kind=='inside' else R+r
        localangle=speed*degrees
        marker=r if kind=='inside' else -r
        wheel=f'<g transform="translate({ox} {oy})"><g class="carrier" style="transform:rotate({degrees:.9f}deg)"><g transform="translate({distance} 0)"><g class="spin" style="transform:rotate({localangle:.9f}deg)">'
        wheel+=f'<circle r="{r}" fill="#55d6d0" fill-opacity=".06" stroke="#55d6d0" stroke-width="2"/><path d="M0 0H{marker}" stroke="#55d6d0"/><circle r="4" fill="#55d6d0"/><circle cx="{marker}" r="6" fill="#ffb879"/></g></g></g></g>'
        motion=f'@keyframes carrier{{from{{transform:rotate({degrees:.9f}deg)}}to{{transform:rotate({degrees+360:.9f}deg)}}}}@keyframes spin{{from{{transform:rotate({localangle:.9f}deg)}}to{{transform:rotate({localangle+speed*360:.9f}deg)}}}}.carrier{{animation:carrier 14s linear infinite}}.spin{{animation:spin 14s linear infinite}}'
    body+=f'<path d="{curve(kind,R,r,ox,oy)}" fill="none" stroke="#ffb879" stroke-width="2.5"/>'+wheel
    for i,note in enumerate(notes):
        body+=text(705,165+i*32,note,16)
    body+=text(705,340,'синий / неподвижная опора',12,'#a7bbd0')
    body+=text(705,367,'бирюзовый / колесо',12,'#55d6d0')
    body+=text(705,394,'оранжевый / след точки',12,'#ffb879')
    subtitle='Качение без проскальзывания · траектория вычислена заранее · не интерактивная модель.'
    if still:
        style='text{font-family:ui-monospace,Consolas,monospace}'
    else:
        # The source picture switches to a true still. This is also a standalone fallback.
        style='text{font-family:ui-monospace,Consolas,monospace}'+motion+'@media(prefers-reduced-motion:reduce){.carrier,.spin,.travel{animation:none!important}}'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1040" height="540" viewBox="0 0 1040 540" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{subtitle}</desc><style>{style}</style>
<rect width="1040" height="540" rx="16" fill="#11263a"/>
{text(30,37,title,24)}{text(30,66,subtitle,12,'#a7bbd0')}
<path d="M30 83H1010M30 498H1010" stroke="#37536d"/>
{body}{text(30,524,'gitEdit / КАЧЕНИЕ БЕЗ GIF    ·    SVG + CSS / статичная версия по prefers-reduced-motion',12,'#a7bbd0')}
</svg>\n'''


def generate(output):
    output.mkdir(parents=True,exist_ok=True)
    for name in SPECS:
        (output/f'{name}.svg').write_text(draw(name),encoding='utf-8')
        (output/f'{name}-still.svg').write_text(draw(name,True),encoding='utf-8')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'assets/rolling')
    generate(parser.parse_args().output)
