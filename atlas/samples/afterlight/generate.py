#!/usr/bin/env python3
"""Reprint the Afterlight room using only Python's standard library.

No network, random seed, fonts or README edits. --output supports clean-room tests.
"""
import argparse
import csv
import colorsys
import io
import json
import math
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[3]
TAU = math.tau
INK = '#dce7f4'
CYAN = '#65e3dc'
CORAL = '#ff957d'


def hsl(hue, saturation, lightness):
    rgb = colorsys.hls_to_rgb((hue % 360)/360, lightness/100, saturation/100)
    return '#' + ''.join(f'{round(v*255):02x}' for v in rgb)


def path(points):
    return 'M' + ' L'.join(f'{x:.2f},{y:.2f}' for x, y in points)


def text(x, y, value, size=14, fill=INK, extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" {extra}>{escape(value)}</text>'


def plate(title, subtitle, body, css='', defs=''):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="360" viewBox="0 0 960 360" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(subtitle)}</desc>
<defs>{defs}</defs><style>
text{{font-family:ui-monospace,Consolas,monospace}} .moving{{transform-box:view-box}}
{css}
@media(prefers-reduced-motion:reduce){{.moving{{animation:none!important}}}}
</style><rect width="960" height="360" rx="20" fill="#111c2b"/>
{text(30,38,title,20)}{text(30,64,subtitle,12,'#a2b5cd')}
{body}<path d="M30 320H930" stroke="#31445b"/>{text(30,343,'gitEdit / AFTERLIGHT     ·     SVG + CSS     ·     no scripts / no requests',11,'#a2b5cd')}
</svg>'''


def exhibits():
    out = {}
    # Two superposed fine gratings create large-scale interference bands.
    grating = ''.join(f'<path d="M{x} -200V600"/>' for x in range(-250,1200,7))
    out['moire'] = plate('01 / МУАРОВЫЙ ИНТЕРФЕРОМЕТР','Две частые решётки → большие полосы биений.',
        f'<g clip-path="url(#window)" stroke="{CYAN}" stroke-width="2">{grating}<g transform="rotate(7 480 195)"><g class="moving" style="transform-origin:480px 195px;animation:sway 14s ease-in-out infinite" stroke="{CORAL}">{grating}</g></g></g>',
        '@keyframes sway{0%,100%{transform:rotate(3deg)}50%{transform:rotate(13deg)}}',
        '<clipPath id="window"><rect x="30" y="88" width="900" height="218" rx="8"/></clipPath>')
    # Every oscillator completes an integer number of turns in 60 seconds.
    body = ''
    for i in range(16):
        x = 65 + i*55
        period = 60/(18+i)
        body += f'<g class="moving" style="transform-origin:{x}px 102px;animation:pend {period:.9f}s ease-in-out infinite"><path d="M{x} 102V260" stroke="#58718e"/><circle cx="{x}" cy="260" r="10" fill="{CYAN if i%2 else CORAL}"/></g>'
    out['pendulum'] = plate('02 / МАЯТНИКОВАЯ ВОЛНА','16 осцилляторов · 18…33 периода за минуту · стилизация, не симулятор.',body,
        '@keyframes pend{0%,100%{transform:rotate(-12deg)}50%{transform:rotate(12deg)}}')
    # Static paths reveal themselves once, leaving a useful motion-free drawing.
    body = ''
    for j, color in enumerate([CYAN,CORAL,'#a997ff']):
        pts = [(480+370*math.sin(3*t+.18*j)*math.exp(-.045*t),190+100*math.sin(4*t)*math.exp(-.045*t)) for t in [i*TAU/1500 for i in range(1501)]]
        body += f'<path d="{path(pts)}" fill="none" stroke="{color}" stroke-width="1.2" pathLength="1" class="moving" style="animation:draw 9s ease-out both;animation-delay:{j*.5}s"/>'
    out['harmonograph'] = plate('03 / ГАРМОНОГРАФ','Затухающие колебания 3:4 · траектория рисуется один раз.',body,
        '@keyframes draw{from{stroke-dasharray:1;stroke-dashoffset:1}to{stroke-dasharray:1;stroke-dashoffset:0}}')
    body = ''
    for i in range(420):
        a = i*math.pi*(3-math.sqrt(5)); r = 5*math.sqrt(i)
        body += f'<circle cx="{240+r*math.cos(a):.2f}" cy="{193+r*math.sin(a):.2f}" r="2.8" fill="{hsl(155+i*.17,65,70)}"/>'
    body = '<g class="moving" style="transform-origin:240px 193px;animation:turn 90s linear infinite">'+body+'</g>'
    body += text(430,156,'137.507764°',36,CYAN)+text(430,192,'Золотой угол → порядок без сетки',18)+text(430,226,'r = 5√n   /   θ = nπ(3 − √5)',16,'#a2b5cd')
    out['phyllotaxis'] = plate('04 / ФИЛЛОТАКСИС','420 семян подсолнуха · один и тот же угол на каждом шаге.',body,'@keyframes turn{to{transform:rotate(360deg)}}')
    body = ''
    for j in range(27):
        pts=[]
        for i in range(241):
            x=40+i*880/240; y=105+j*7-40*math.exp(-((x-360)/120)**2)*math.sin(j*.16)-28*math.exp(-((x-690)/100)**2)*math.cos(j*.14)
            pts.append((x,y))
        body += f'<path d="{path(pts)}" fill="none" stroke="{hsl(170+j*2,60,45+j)}" stroke-width="1.2"/>'
    out['contours'] = plate('05 / ТОПОГРАФИЧЕСКИЙ ШЁЛК','Линии рельефа вместо тяжёлого фонового изображения.',body)
    # Thresholded alpha merges blurred circles into a single liquid silhouette.
    body='<g filter="url(#goo)">'
    for i in range(7):
        body+=f'<circle cx="{270+i*65}" cy="195" r="43" fill="{CYAN}" class="moving" style="animation:float {4+i*.3}s ease-in-out {-i*.6}s infinite"/>'
    body+='</g>'
    out['metaballs'] = plate('06 / МЕТАСФЕРЫ','Размытие + порог альфа-канала: отдельные капли слипаются.',body,
        '@keyframes float{0%,100%{transform:translateY(-28px)}50%{transform:translateY(28px)}}',
        '<filter id="goo" x="-30%" y="-80%" width="160%" height="260%" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="10"/><feColorMatrix values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 24 -10"/></filter>')
    body=''
    for side, color in [(0,CYAN),(1,CORAL)]:
        pts=[]
        for i in range(2401):
            t=i*TAU/2400; r=87+21*math.cos(17*t+side*.5)
            pts.append((280+side*400+r*math.cos(t),195+r*math.sin(t)))
        body+=f'<path d="{path(pts)}" fill="none" stroke="{color}" stroke-width="1.1"/>'
        for j in range(1,5):
            body+=f'<circle cx="{280+side*400}" cy="195" r="{j*22}" fill="none" stroke="{color}" stroke-width=".5"/>'
    out['guilloche'] = plate('07 / ГИЛЬОШИРНАЯ РОЗЕТКА','Банкнотная графика: точная линия, а не текстура из фотобанка.',body)
    body=''
    for i in range(36):
        x=65+(i%12)*75; y=124+(i//12)*69
        body+=f'<g class="moving" style="transform-origin:{x}px {y}px;animation:tile 8s ease-in-out {-i*.12}s infinite"><path d="M{x-26} {y+26}A52 52 0 0 1 {x+26} {y-26}" fill="none" stroke="{CYAN if i%2 else CORAL}" stroke-width="7"/></g>'
    out['truchet'] = plate('08 / ПОВОРОТ ПЛИТКИ','Одна четверть окружности → целый лабиринт; медленная смена ориентаций.',body,
        '@keyframes tile{0%,30%,100%{transform:rotate(0deg)}50%,80%{transform:rotate(90deg)}}')
    # Text follows two authored paths; SVG text is not a downloadable custom font.
    defs='<path id="upper" d="M50 204Q260 50 480 204T910 204"/><path id="lower" d="M50 225Q260 71 480 225T910 225"/>'
    body=f'<use href="#upper" fill="none" stroke="#31445b"/><text fill="{CYAN}" font-size="27" letter-spacing="4"><textPath href="#upper">ТЕКСТ МОЖЕТ ИДТИ НЕ ПО ПРЯМОЙ</textPath></text><text fill="{CORAL}" font-size="13" letter-spacing="5"><textPath href="#lower">TYPE / ALONG / A / PATH / TYPE / ALONG / A / PATH</textPath></text>'
    out['textpath'] = plate('09 / ТИПОГРАФИЧЕСКАЯ ВОЛНА','textPath: заголовок на собственной кривой Безье.',body,defs=defs)
    body=''
    for i in range(14):
        a=i*math.pi/7
        pts=[(480+390*math.cos(t)*math.cos(a)-88*math.sin(t)*math.sin(a),195+90*math.cos(t)*math.sin(a)+38*math.sin(t)*math.cos(a)) for t in [j*TAU/240 for j in range(241)]]
        body+=f'<path d="{path(pts)}" fill="none" stroke="{CYAN if i%2 else CORAL}" stroke-width=".8" opacity=".7"/>'
    out['spirograph'] = plate('10 / ПРОВОЛОЧНЫЙ ОБЪЁМ','14 проекций эллипса создают глубину без WebGL и STL.',body)
    body=''
    for i in range(9):
        pts=[(60+j*840/300,195+85*math.sin(j*TAU/300*2+i*.22)) for j in range(301)]
        body+=f'<path d="{path(pts)}" fill="none" stroke="{hsl(165+i*9,70,72)}" stroke-width="2" pathLength="100" stroke-dasharray="2 2" class="moving" style="animation:flow {6+i*.3}s linear infinite"/>'
    out['phase'] = plate('11 / ФАЗОВЫЕ ДОРОЖКИ','Пунктир течёт по неподвижной кривой: движение без кадрового GIF.',body,
        '@keyframes flow{to{stroke-dashoffset:-100}}')
    defs='<filter id="paper"><feTurbulence type="fractalNoise" baseFrequency=".7" numOctaves="3" seed="12"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncA type="linear" slope=".18"/></feComponentTransfer><feBlend in="SourceGraphic" mode="soft-light"/></filter>'
    body='<g filter="url(#paper)"><rect x="40" y="90" width="880" height="214" rx="3" fill="#e7d7b4"/>'
    for i in range(36):
        x=90+i*22
        body+=f'<path d="M{x} 276Q{x-70} 130 {x+20} 110" fill="none" stroke="{("#164b74" if i%2 else "#bd553d")}" stroke-width="2"/>'
    body+=text(490,204,'PAPER / 012',30,'#163d57')+'</g>'
    out['paper'] = plate('12 / ЦИФРОВАЯ БУМАГА','feTurbulence: зерно генерируется внутри SVG; seed фиксирован.',body,defs=defs)
    return out


def generate(output):
    output.mkdir(parents=True,exist_ok=True)
    works=exhibits()
    for name, svg in works.items():
        (output/f'{name}.svg').write_text(svg+'\n',encoding='utf-8')
    rows=[['exhibit','format','motion','bytes']]
    for name in works:
        rows.append([name,'SVG','CSS' if '@keyframes' in works[name] else 'static',len((works[name]+'\n').encode())])
    for ext, sep in [('csv',','),('tsv','\t')]:
        stream=io.StringIO(newline='')
        csv.writer(stream,delimiter=sep,lineterminator='\n').writerows(rows)
        (output/f'catalog.{ext}').write_text(stream.getvalue(),encoding='utf-8')
    notebook={
        'cells':[
            {'cell_type':'markdown','metadata':{},'source':['# Филлотаксис: рисунок из формулы\n','Это сохранённый результат, не запущенный в GitHub Python.\n']},
            {'cell_type':'code','execution_count':1,'metadata':{},'source':[
                'import math\n','from IPython.display import SVG, display\n',
                'dots = []\n','for n in range(420):\n','    a = n * math.pi * (3 - math.sqrt(5))\n','    r = 5 * math.sqrt(n)\n',
                '    dots.append(f\'<circle cx="{240+r*math.cos(a):.2f}" cy="{193+r*math.sin(a):.2f}" r="2.8" fill="#65e3dc"/>\')\n',
                'display(SVG(\'<svg xmlns="http://www.w3.org/2000/svg" viewBox="100 75 280 240">\' + "".join(dots) + "</svg>"))\n'],
             'outputs':[{'output_type':'display_data','metadata':{},'data':{'image/svg+xml':['<svg xmlns="http://www.w3.org/2000/svg" viewBox="100 75 280 240">'+''.join(f'<circle cx="{240+5*math.sqrt(n)*math.cos(n*math.pi*(3-math.sqrt(5))):.2f}" cy="{193+5*math.sqrt(n)*math.sin(n*math.pi*(3-math.sqrt(5))):.2f}" r="2.8" fill="#65e3dc"/>' for n in range(420))+'</svg>'],'text/plain':['<SVG: 420 seeds>']}}]}
        ],'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3.11'}},'nbformat':4,'nbformat_minor':5}
    for i, cell in enumerate(notebook['cells']):
        cell['id']=f'afterlight-{i}'
    (output/'phyllotaxis.ipynb').write_text(json.dumps(notebook,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'assets/afterlight')
    generate(parser.parse_args().output)
