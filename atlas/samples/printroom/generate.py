#!/usr/bin/env python3
"""An original ray-marched torus, printed six ways. Python standard library only."""
import argparse
from html import escape
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
W,H = 128,80
BAYER = ((0,8,2,10),(12,4,14,6),(3,11,1,9),(15,7,13,5))
RAMP = '@%#*+=-:. '


def normalize(v):
    length=math.sqrt(sum(x*x for x in v))
    return tuple(x/length for x in v)


def sdf(p):
    x,y,z=p
    # Inverse rotation about x, then y. The hole faces the camera obliquely.
    y,z = y*math.cos(.65)-z*math.sin(.65), y*math.sin(.65)+z*math.cos(.65)
    x,z = x*math.cos(.3)+z*math.sin(.3), -x*math.sin(.3)+z*math.cos(.3)
    return math.hypot(math.hypot(x,y)-.88,z)-.30


def render():
    light=normalize((-3,5,6))
    image=[]
    for iy in range(H):
        row=[]
        for ix in range(W):
            x=(ix+.5-W/2)*3.6/W
            y=(H/2-iy-.5)*3.6/W
            z=3.0
            hit=False
            for _ in range(100):
                distance=sdf((x,y,z))
                if distance<.0005:
                    hit=True
                    break
                z-=max(distance,.0001)
                if z < -2:
                    break
            if not hit:
                row.append(255)
                continue
            epsilon=.001
            p=(x,y,z)
            gradient=[]
            for axis in range(3):
                a=list(p); b=list(p)
                a[axis]+=epsilon; b[axis]-=epsilon
                gradient.append(sdf(a)-sdf(b))
            n=normalize(gradient)
            diffuse=max(0,sum(a*b for a,b in zip(n,light)))
            half=normalize((light[0],light[1],light[2]+1))
            specular=max(0,sum(a*b for a,b in zip(n,half)))**32
            row.append(round(255*min(.94,.13+.68*diffuse+.17*specular)))
        image.append(row)
    return image


def dither(image):
    return [[v/255 < (BAYER[y%4][x%4]+.5)/16 for x,v in enumerate(row)] for y,row in enumerate(image)]


def ascii_art(image):
    rows=[]
    for y in range(0,H,4):
        row=''
        for x in range(0,W,2):
            average=sum(image[yy][xx] for yy in range(y,y+4) for xx in range(x,x+2))/8
            row+=RAMP[min(len(RAMP)-1,int(average/256*len(RAMP)))]
        rows.append(row)
    return '\n'.join(rows)+'\n'


def rle(image):
    """Runs of equal values, with rows preserved. Coordinates are sample indices."""
    for y,row in enumerate(image):
        x=0
        while x<len(row):
            end=x+1
            while end<len(row) and row[end]==row[x]:
                end+=1
            yield x,y,end-x,row[x]
            x=end


def contours(image,level):
    """Marching squares with linear interpolation and a fixed saddle pairing."""
    segments=[]
    for y in range(len(image)-1):
        for x in range(len(image[0])-1):
            corners=[(x,y,image[y][x]),(x+1,y,image[y][x+1]),
                     (x+1,y+1,image[y+1][x+1]),(x,y+1,image[y+1][x])]
            crossings=[]
            for a,b in zip(corners,corners[1:]+corners[:1]):
                if (a[2]<level)!=(b[2]<level):
                    t=(level-a[2])/(b[2]-a[2])
                    crossings.append((a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1])))
            if len(crossings)==2:
                segments.append(crossings)
            elif len(crossings)==4:
                # Fixed pairing: deterministic saddle convention, not topology inference.
                segments.extend([crossings[:2],crossings[2:]])
    return segments


def text(x,y,value,size=15,color='#254f60',attrs=''):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" {attrs}>{escape(value)}</text>'


def plate(title,subtitle,body,notes):
    labels=''.join(text(715,155+i*31,n,15) for i,n in enumerate(notes))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1040" height="560" viewBox="0 0 1040 560" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(subtitle)}</desc>
<style>text{{font-family:ui-monospace,Consolas,monospace}}</style>
<rect width="1040" height="560" rx="16" fill="#f6f2e8"/>
{text(30,36,title,22)}{text(30,65,subtitle,13)}
<path d="M30 82H1010M30 520H1010" stroke="#c5d0c5"/>
<rect x="30" y="100" width="640" height="400" fill="#fffdf6"/>
{body}{labels}{text(30,545,'gitEdit / ПЕЧАТНАЯ КОМНАТА    ·    одна сцена / шесть методов / без JavaScript',12)}
</svg>\n'''


def prints(image):
    out={}
    quantized=[[min(15,v//16) for v in row] for row in image]
    body=''
    for x,y,length,v in rle(quantized):
        if v==15:
            continue
        # Palette interpolates dark indigo → warm paper.
        t=v/15
        rgb=tuple(round(a+(b-a)*t) for a,b in zip((23,64,89),(255,253,246)))
        fill='#'+''.join(f'{c:02x}' for c in rgb)
        body+=f'<rect x="{30+x*5}" y="{100+y*5}" width="{length*5}" height="5" fill="{fill}"/>'
    out['indigo']=plate('01 / ИНДИГОВЫЙ ОТТИСК','Тор, вычисленный трассировкой SDF · 128 × 80 отсчётов · 16 уровней.',body,
        ['Одна процедурная сцена','Никаких внешних фото','Освещение + блик','16 тонов → одна краска'])
    body=''
    for y in range(0,H,2):
        for x in range(0,W,2):
            darkness=1-sum(image[yy][xx] for yy in (y,y+1) for xx in (x,x+1))/(4*255)
            radius=4.8*math.sqrt(darkness)
            if radius>.08:
                body+=f'<circle cx="{35+x*5}" cy="{105+y*5}" r="{radius:.4f}" fill="#254f60"/>'
    out['halftone']=plate('02 / ГАЗЕТНАЯ ПОЛУТОНОВАЯ ПЕЧАТЬ','Меняется площадь точки, а не её цвет; радиус пропорционален корню из темноты.',body,
        ['64 × 40 ячеек','Одна краска','Радиус ∝ √темноты','Все точки — векторы'])
    body=''
    for x,y,length,on in rle(dither(image)):
        if on:
            body+=f'<rect x="{30+x*5}" y="{100+y*5}" width="{length*5}" height="5" fill="#254f60"/>'
    out['bayer']=plate('03 / ПИКСЕЛЬНЫЙ РАСТР BAYER','Пороговая матрица 4 × 4 превращает тона в два состояния: краска или бумага.',body,
        ['128 × 80 пикселей','Всего два цвета','Не blur и не шум','Повторяемая матрица'])
    body=''
    for y,row in enumerate(ascii_art(image).splitlines()):
        body+=text(42,117+y*19,row,16,'#254f60','xml:space="preserve" textLength="616" lengthAdjust="spacingAndGlyphs"')
    out['ascii']=plate('04 / РИСУНОК ИЗ ПЕЧАТНЫХ ЗНАКОВ','64 колонки × 20 строк · яркость блока выбирает символ из десяти уровней.',body,
        ['@ % # * + = - : .','Можно скачать .txt','SVG сохраняет пробелы','Форма зависит от шрифта'])
    body=''
    for y in range(0,H,2):
        for x in range(0,W,2):
            darkness=1-sum(image[yy][xx] for yy in (y,y+1) for xx in (x,x+1))/(4*255)
            if darkness>.08:
                length=8.5*darkness
                cx=35+x*5; cy=105+y*5
                body+=f'<path d="M{cx-length/2:.3f} {cy+length/2:.3f}l{length:.3f} {-length:.3f}" stroke="#254f60" stroke-width="1.3"/>'
                if darkness>.55:
                    body+=f'<path d="M{cx-length/2:.3f} {cy-length/2:.3f}l{length:.3f} {length:.3f}" stroke="#254f60" stroke-width="1"/>'
    out['hatch']=plate('05 / ШТРИХОВАЯ ГРАВЮРА','Темнота управляет длиной штриха; в густой тени появляется второй наклон.',body,
        ['Диагональная штриховка','В тени — перекрёстная','Не случайная текстура','Рисунок без заливок'])
    body=''
    for level in (50,75,100,125,150,175,200,225,245):
        d=''
        for a,b in contours(image,level):
            d+=f'M{32.5+a[0]*5:.2f},{102.5+a[1]*5:.2f}L{32.5+b[0]*5:.2f},{102.5+b[1]*5:.2f}'
        body+=f'<path d="{d}" fill="none" stroke="#254f60" stroke-width=".8"/>'
    out['isolines']=plate('06 / КОНТУРЫ ЯРКОСТИ','Marching squares строит девять изолиний по тому же исходному изображению.',body,
        ['9 порогов яркости','Линия = одинаковый тон','Не высота поверхности','Не географическая карта'])
    return out


def generate(output):
    image=render()
    output.mkdir(parents=True,exist_ok=True)
    # P2 is an ASCII portable graymap; every sample can be inspected without Pillow.
    pgm=f'P2\n# gitEdit original SDF torus\n{W} {H}\n255\n'
    pgm+='\n'.join(' '.join(map(str,row)) for row in image)+'\n'
    (output/'source.pgm').write_text(pgm,encoding='ascii')
    (output/'torus.txt').write_text(ascii_art(image),encoding='ascii')
    for name,svg in prints(image).items():
        (output/f'{name}.svg').write_text(svg,encoding='utf-8')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'assets/printroom')
    generate(parser.parse_args().output)
