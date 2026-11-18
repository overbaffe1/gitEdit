#!/usr/bin/env python3
"""Print eight original algorithm plates. Python standard library, no network."""
import argparse
import csv
from html import escape
import io
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BLUE = '#245b81'
RED = '#b84f38'


def label(x, y, value, size=16, color=BLUE):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{escape(value)}</text>'


def line(points, color=BLUE, width=1.5, attrs=''):
    d = 'M' + ' L'.join(f'{x:.3f},{y:.3f}' for x, y in points)
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" {attrs}/>'


def plate(title, subtitle, body, css=''):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="420" viewBox="0 0 960 420" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(subtitle)}</desc>
<style>text{{font-family:ui-monospace,Consolas,monospace}}{css}
@media(prefers-reduced-motion:reduce){{.motion{{animation:none!important}}}}</style>
<rect width="960" height="420" rx="16" fill="#f5f0e5"/>
<path d="M30 82H930M30 380H930" stroke="#c5c5b6"/>
{label(30,36,title,22)}{label(30,64,subtitle,13)}
{body}
{label(30,404,'gitEdit / АЛГОРИТМАРИЙ     ·     вычислено заранее / без JavaScript',12)}
</svg>\n'''


def rule90(width=111, generations=55):
    row = [0]*width
    row[width//2] = 1
    rows = [row]
    for _ in range(generations-1):
        row = [(row[x-1] if x else 0) ^ (row[x+1] if x+1 < width else 0) for x in range(width)]
        rows.append(row)
    return rows


def hilbert(order):
    """Integer Hilbert coordinates, lower-left orientation; consecutive cells touch."""
    size = 2**order
    points = []
    for distance in range(size*size):
        x = y = 0
        t, scale = distance, 1
        while scale < size:
            rx = 1 & (t//2)
            ry = 1 & (t ^ rx)
            if ry == 0:
                if rx == 1:
                    x, y = scale-1-x, scale-1-y
                x, y = y, x
            x += scale*rx
            y += scale*ry
            t //= 4
            scale *= 2
        points.append((x,y))
    return points


def sorting_states(values):
    values = list(values)
    states = [values.copy()]
    for end in range(len(values)-1, 0, -1):
        for i in range(end):
            if values[i] > values[i+1]:
                values[i], values[i+1] = values[i+1], values[i]
                states.append(values.copy())
    return states


def bezier(points, t):
    level = list(points)
    while len(level)>1:
        level = [((1-t)*a[0]+t*b[0],(1-t)*a[1]+t*b[1]) for a,b in zip(level, level[1:])]
    return level[0]


def clip_cell(poly, p, q):
    """Clip to the half-plane closer to p than q."""
    a, b = 2*(q[0]-p[0]), 2*(q[1]-p[1])
    c = q[0]**2+q[1]**2-p[0]**2-p[1]**2
    result = []
    for u,v in zip(poly, poly[1:]+poly[:1]):
        fu, fv = a*u[0]+b*u[1]-c, a*v[0]+b*v[1]-c
        if fu <= 1e-9:
            result.append(u)
        if (fu<0) != (fv<0):
            t = fu/(fu-fv)
            result.append((u[0]+t*(v[0]-u[0]),u[1]+t*(v[1]-u[1])))
    return result


def voronoi(seeds):
    cells=[]
    for p in seeds:
        poly=[(40,100),(920,100),(920,360),(40,360)]
        for q in seeds:
            if q != p:
                poly=clip_cell(poly,p,q)
        cells.append(poly)
    return cells


def tree_segments(depth=7):
    result=[]
    def grow(x,y,angle,length,n):
        end=(x+length*math.cos(angle), y+length*math.sin(angle))
        result.append(((x,y),end,n))
        if n:
            grow(*end,angle-.45,length*.72,n-1)
            grow(*end,angle+.45,length*.72,n-1)
    grow(290,355,-math.pi/2,75,depth)
    return result


def exhibits():
    out={}
    body=''
    for y,row in enumerate(rule90()):
        for x,on in enumerate(row):
            if on:
                body+=f'<rect x="{55+x*5}" y="{95+y*5}" width="4.5" height="4.5" fill="{BLUE}"/>'
    body+=label(650,174,'RULE 90',28)+label(650,211,'left XOR right',18)+label(650,251,'Одна клетка →',16)+label(650,278,'треугольный мир',16)
    out['rule90']=plate('01 / КЛЕТОЧНЫЙ ГОБЕЛЕН','Правило 90 · 111 клеток × 55 поколений · границы заполнены нулями.',body)
    body=''
    for i,order in enumerate((1,2,3,4)):
        points=hilbert(order); scale=185/(2**order-1)
        body+=line([(35+i*235+x*scale,118+y*scale) for x,y in points],BLUE if i%2==0 else RED,2,'pathLength="1" class="motion" style="animation:ink 7s ease-out both"')
        body+=label(45+i*235,346,f'n={order} / {len(points)} точек',13)
    out['hilbert']=plate('02 / ОДНА ЛИНИЯ, ВЕСЬ КВАДРАТ','Первые четыре порядка кривой Гильберта; соседние точки всегда рядом.',body,'@keyframes ink{from{stroke-dasharray:1;stroke-dashoffset:1}to{stroke-dasharray:1;stroke-dashoffset:0}}')
    values=[8,3,10,1,7,4,9,2,6,5]
    states=sorting_states(values)
    body=''
    for value in range(1,11):
        pts=[(50+i*860/(len(states)-1),112+state.index(value)*25) for i,state in enumerate(states)]
        color=BLUE if value%2 else RED
        body+=line(pts,color,2.2)
        body+=label(24,pts[0][1]+5,str(value),12,color)+label(922,pts[-1][1]+5,str(value),12,color)
    out['sorting']=plate('03 / КОСЫ СОРТИРОВКИ',f'Bubble sort · 10 чисел · {len(states)-1} обменов · слева вход, справа порядок.',body)
    controls=[(70,320),(200,100),(690,100),(880,320)]
    body=line(controls,'#a2aaa3',1)
    body+=line([bezier(controls,i/240) for i in range(241)],BLUE,3)
    for t in (.2,.5,.8):
        level=[((1-t)*a[0]+t*b[0],(1-t)*a[1]+t*b[1]) for a,b in zip(controls,controls[1:])]
        body+=line(level,RED,1)
        level2=[((1-t)*a[0]+t*b[0],(1-t)*a[1]+t*b[1]) for a,b in zip(level,level[1:])]
        body+=line(level2,RED,1.5)
        x,y=bezier(controls,t)
        body+=f'<circle cx="{x}" cy="{y}" r="5" fill="{RED}"/>'
        body+=label(x-18,y-13,f'{t:.1f}',12,RED)
    for x,y in controls:
        body+=f'<circle cx="{x}" cy="{y}" r="5" fill="{BLUE}"/>'
    out['bezier']=plate('04 / ЗАКУЛИСЬЕ КРИВОЙ БЕЗЬЕ','Алгоритм де Кастельжо · линейная интерполяция на трёх уровнях.',body)
    body=''
    for j,terms in enumerate((1,3,9)):
        x0=45+j*305
        body+=line([(x0,230),(x0+270,230)],'#b9bcb3',1)
        points=[]
        for i in range(401):
            t=i*math.tau/400
            y=sum(math.sin(k*t)/k for k in range(1,terms*2,2))*4/math.pi
            points.append((x0+i*270/400,230-70*y))
        body+=line(points,BLUE if j!=1 else RED,2)
        body+=label(x0+30,346,f'{terms} нечётных гармоник',13)
    out['fourier']=plate('05 / ИЗ СИНУСА В ПРЯМОУГОЛЬНИК','Частичные суммы ряда Фурье; выбросы у скачка — эффект Гиббса.',body)
    seeds=[(75+(i*197)%830,122+(i*83)%210) for i in range(23)]
    body=''
    colors=['#bbd7d4','#e7bfaa','#d5d6b7','#acc6da','#e5cfaa']
    for i,(seed,poly) in enumerate(zip(seeds,voronoi(seeds))):
        points=' '.join(f'{x:.3f},{y:.3f}' for x,y in poly)
        body+=f'<polygon points="{points}" fill="{colors[i%len(colors)]}" stroke="#f5f0e5" stroke-width="3"/>'
        body+=f'<circle cx="{seed[0]}" cy="{seed[1]}" r="3" fill="{BLUE}"/>'
    out['voronoi']=plate('06 / ВИТРАЖ БЛИЖАЙШИХ СОСЕДЕЙ','23 зерна · каждая точка ячейки ближе к своему зерну, чем к остальным.',body)
    body=''
    for a,b,depth in tree_segments():
        body+=line([a,b],BLUE if depth>2 else '#56764a',max(.7,depth*.65))
    body+=label(550,176,'ветвь → две ветви',24)+label(550,219,'угол ±0.45 рад',17)+label(550,250,'масштаб ×0.72',17)+label(550,281,'8 уровней / 255 сегментов',15)
    out['tree']=plate('07 / РЕКУРСИВНЫЙ ГЕРБАРИЙ','Двоичное дерево: одна функция растит весь рисунок.',body)
    body=''
    # Static dot density samples a two-source interference intensity field.
    for iy in range(40):
        for ix in range(130):
            x,y=45+ix*4,110+iy*6
            d1=math.hypot(x-170,y-205); d2=math.hypot(x-170,y-255)
            intensity=((math.cos((d1-d2)*.22)+1)/2)**2
            r=.35+1.45*intensity
            body+=f'<circle cx="{x}" cy="{y}" r="{r:.3f}" fill="{BLUE}"/>'
    body+=label(625,178,'ДВА ИСТОЧНИКА',23)+label(625,220,'разность хода →',17)+label(625,248,'светлые и тёмные',17)+label(625,276,'полосы',17)
    out['interference']=plate('08 / ПОЛОСЫ ИНТЕРФЕРЕНЦИИ','Учебное поле двух синфазных источников; интенсивность закодирована размером точек.',body)
    return out


def generate(output):
    output.mkdir(parents=True,exist_ok=True)
    stream=io.StringIO(newline='')
    writer=csv.writer(stream,lineterminator='\n')
    writer.writerow(['exhibit','bytes','animation'])
    for name,svg in exhibits().items():
        (output/f'{name}.svg').write_text(svg,encoding='utf-8')
        writer.writerow([name,len(svg.encode()),'once' if '@keyframes' in svg else 'none'])
    (output/'catalog.csv').write_text(stream.getvalue(),encoding='utf-8')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'assets/algorithmarium')
    generate(parser.parse_args().output)
