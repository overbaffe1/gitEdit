#!/usr/bin/env python3
"""Six original optical exhibits and six reveal files. Standard library only."""
import argparse
from html import escape
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
PAPER='#f4efe2'
INK='#243b53'
ORANGE='#ba4c30'
GUIDE='#177e89'
NAMES=('ebbinghaus','muller-lyer','cafe-wall','hering','contrast','kanizsa')


def text(x,y,value,size=15,color=INK):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{escape(value)}</text>'


def segment(x1,y1,x2,y2,color=INK,width=2,attrs=''):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" {attrs}/>'


def circle(x,y,r,fill,attrs=''):
    return f'<circle cx="{x:.5f}" cy="{y:.5f}" r="{r}" fill="{fill}" {attrs}/>'


def wrap(title,question,body,reveal,defs=''):
    style='text{font-family:ui-monospace,Consolas,monospace}'
    if reveal:
        style+='.context{opacity:.12}'
    note='ПРОВЕРКА / бирюзовая разметка объясняет геометрию' if reveal else 'Сначала посмотри; клик по картинке в README откроет проверку'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1040" height="520" viewBox="0 0 1040 520" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(question)}</desc>
<defs>{defs}</defs><style>{style}</style>
<rect width="1040" height="520" rx="16" fill="{PAPER}"/>
{text(30,37,title,22)}{text(30,67,question,14)}
<path d="M30 84H1010M30 477H1010" stroke="#c4c5b6"/>
{body}{text(30,504,note,12,GUIDE if reveal else INK)}
</svg>\n'''


def exhibit(name,reveal=False):
    body=''; defs=''
    if name=='ebbinghaus':
        title='01 / КРУГИ В РАЗНОМ ОКРУЖЕНИИ'
        question='Какой из двух оранжевых кругов кажется больше?'
        context=''
        for cx,count,distance,radius in ((260,8,70,15),(740,6,115,51)):
            for i in range(count):
                angle=math.tau*i/count
                context+=circle(cx+distance*math.cos(angle),285+distance*math.sin(angle),radius,INK)
        body+='<g class="context">'+context+'</g>'
        for cx in (260,740):
            body+=circle(cx,285,28,ORANGE,'data-target="equal-circle"')
        if reveal:
            for y in (257,313):
                body+=segment(225,y,775,y,GUIDE,1.5,'stroke-dasharray="5 5"')
            body+=text(410,220,'r₁ = r₂ = 28',20,GUIDE)
    elif name=='muller-lyer':
        title='02 / ДЛИНА МЕЖДУ НАКОНЕЧНИКАМИ'
        question='Сравни только горизонтальные оранжевые отрезки.'
        context=''
        for y,direction in ((205,1),(355,-1)):
            for x,sign in ((260,direction),(780,-direction)):
                context+=segment(x,y,x+sign*52,y-48,INK,3)+segment(x,y,x+sign*52,y+48,INK,3)
            body+=segment(260,y,780,y,ORANGE,5,'data-target="equal-segment"')
        body='<g class="context">'+context+'</g>'+body
        if reveal:
            for x in (260,780):
                body+=segment(x,130,x,430,GUIDE,1.5,'stroke-dasharray="5 5"')
            body+=text(365,285,'520 = 520 SVG-единиц',20,GUIDE)
    elif name=='cafe-wall':
        title='03 / СТЕНА КАФЕ'
        question='Кажутся ли горизонтальные швы наклонёнными?'
        defs='<clipPath id="wall"><rect x="100" y="128" width="840" height="294"/></clipPath>'
        context=''
        for row in range(7):
            offset=(0,22,44,22)[row%4]
            for col in range(-1,13):
                x=100+col*70+offset
                fill='#192c3e' if col%2 else '#fffcf0'
                context+=f'<rect x="{x}" y="{128+row*42}" width="70" height="39" fill="{fill}"/>'
        body+='<rect x="100" y="128" width="840" height="294" fill="#8c8c83"/>'
        body+='<g class="context" clip-path="url(#wall)">'+context+'</g>'
        if reveal:
            for row in range(7):
                y=128+row*42+40.5
                body+=segment(100,y,940,y,GUIDE,1.5,'data-target="horizontal-guide"')
            body+=text(310,454,'Все швы горизонтальны: y₁ = y₂',19,GUIDE)
    elif name=='hering':
        title='04 / ПРЯМЫЕ НА ВЕЕРНОМ ФОНЕ'
        question='Две оранжевые линии прямые или выгнутые?'
        defs='<clipPath id="fan"><rect x="105" y="120" width="830" height="330"/></clipPath>'
        context=''
        for i in range(32):
            a=math.pi*i/32
            dx,dy=700*math.cos(a),700*math.sin(a)
            context+=segment(520-dx,285-dy,520+dx,285+dy,INK,1)
        body+='<g class="context" clip-path="url(#fan)">'+context+'</g>'
        for x in (410,630):
            body+=segment(x,130,x,440,ORANGE,4,'data-target="vertical-line"')
        if reveal:
            for y in (130,440):
                body+=segment(390,y,650,y,GUIDE,1.5)
            body+=text(415,467,'x = const',18,GUIDE)
    elif name=='contrast':
        title='05 / ОДНА КРАСКА, ДВА ФОНА'
        question='Который из двух маленьких серых прямоугольников светлее?'
        body+='<g class="context"><rect x="140" y="140" width="310" height="290" fill="#243b53"/><rect x="590" y="140" width="310" height="290" fill="#d9d4bc"/></g>'
        for x in (250,700):
            body+=f'<rect x="{x}" y="235" width="90" height="100" fill="#888888" data-target="equal-gray"/>'
        if reveal:
            body+='<rect x="340" y="235" width="360" height="100" fill="#888888"/>'
            body+=text(360,200,'Оба fill = #888888',20,GUIDE)
            body+=segment(250,350,790,350,GUIDE,2)
    elif name=='kanizsa':
        title='06 / ТРЕУГОЛЬНИК БЕЗ КОНТУРА'
        question='Видишь ли ты светлый треугольник поверх трёх дисков?'
        vertices=((520,150),(350,400),(690,400))
        for x,y in vertices:
            body+=circle(x,y,58,INK,'data-target="disk"')
        # The paper-colored polygon only cuts the disks. It has no visible stroke
        # and uses exactly the same fill as the surrounding paper.
        body+=f'<polygon points="520,150 350,400 690,400" fill="{PAPER}" data-target="paper-cutout"/>'
        if reveal:
            body+=f'<polygon points="520,150 350,400 690,400" fill="none" stroke="{GUIDE}" stroke-width="2" stroke-dasharray="5 5"/>'
            body+=text(60,235,'Пунктир добавлен',17,GUIDE)+text(60,264,'только в проверке',17,GUIDE)
            body+=text(700,235,'Заливка треугольника',15,GUIDE)+text(700,264,'= фон '+PAPER,15,GUIDE)
    else:
        raise ValueError(name)
    return wrap(title,question,body,reveal,defs)


def generate(output):
    output.mkdir(parents=True,exist_ok=True)
    for name in NAMES:
        (output/f'{name}.svg').write_text(exhibit(name),encoding='utf-8')
        (output/f'{name}-proof.svg').write_text(exhibit(name,True),encoding='utf-8')
    facts={'scope':'Illustrations, not a clinical perception test',
           'ebbinghaus':{'target_radii':[28,28]},
           'muller-lyer':{'target_x':[260,780],'lengths':[520,520]},
           'cafe-wall':{'rows':7,'row_pitch':42,'mortar':3,'slope':0},
           'hering':{'target_x':[410,630],'target_y':[130,440]},
           'contrast':{'target_fill':['#888888','#888888']},
           'kanizsa':{'paper':PAPER,'triangle_fill':PAPER,'outline_in_original':False}}
    (output/'facts.json').write_text(json.dumps(facts,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'assets/perception')
    generate(parser.parse_args().output)
