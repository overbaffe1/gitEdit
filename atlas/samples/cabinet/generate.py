#!/usr/bin/env python3
"""Six data posters from a fixed, explicit sample of twelve repository files.

Standard library only; no network, git commands, timestamps or README writes.
"""
import argparse
from collections import Counter
import csv
import hashlib
from html import escape
import io
import json
import math
from pathlib import Path
import zlib

ROOT = Path(__file__).resolve().parents[3]
SAMPLE = (
    'assets/cover-profile.svg', 'assets/crystal-light.png',
    'assets/crystal-wipe.gif', 'assets/crystal.stl',
    'assets/survey.geojson', 'assets/sheets.topojson',
    'assets/typecase/dock.ttf', 'assets/aurelia/aurelia.wav',
    'assets/pocket-folio/issue-a4.pdf', 'assets/afterlight/phyllotaxis.ipynb',
    'assets/afterlight/catalog.csv', 'assets/twilight/table.zip',
)
COLORS = ('#f4b183','#86cec3','#c3ace5','#f0d078','#98b8e3','#d9a1ac',
          '#a3c47e','#b9b6e5','#dfab80','#81bcc0','#c8c39a','#dcaedb')
TEXT = '#f6e9d8'
MUTED = '#c7b6af'


def text(x,y,value,size=14,color=TEXT,attrs=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" {attrs}>{escape(str(value))}</text>'


def line(points,color=MUTED,width=1.5):
    points=' '.join(f'{x:.3f},{y:.3f}' for x,y in points)
    return f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="{width}"/>'


def plate(title,subtitle,body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1040" height="520" viewBox="0 0 1040 520" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(subtitle)}</desc>
<style>text{{font-family:ui-monospace,Consolas,monospace}}</style>
<rect width="1040" height="520" rx="18" fill="#2c212b"/>
{text(30,37,title,23)}{text(30,66,subtitle,13,MUTED)}
<path d="M30 82H1010M30 481H1010" stroke="#68505c"/>
{body}{text(30,507,'gitEdit / КАБИНЕТ ДАННЫХ    ·    12 выбранных файлов, НЕ весь репозиторий',12,MUTED)}
</svg>\n'''


def collect(root=ROOT):
    records=[]
    for i,path in enumerate(SAMPLE):
        data=(root/path).read_bytes()
        counts=Counter(data)
        records.append({'id':f'{i+1:02}', 'path':path, 'format':Path(path).suffix[1:],
                        'bytes':len(data), 'zlib_bytes':len(zlib.compress(data,9)),
                        'sha256':hashlib.sha256(data).hexdigest(),
                        'first16_hex':data[:16].hex(),
                        'histogram16':[sum(n for byte,n in counts.items() if byte//16==b) for b in range(16)]})
    return records


def rectangles(items,x,y,w,h):
    """Weighted binary partition. Each leaf area is exactly proportional to bytes."""
    if len(items)==1:
        return [(items[0],x,y,w,h)]
    total=sum(r['bytes'] for r in items)
    cumulative=0
    cuts=[]
    for i,r in enumerate(items[:-1],1):
        cumulative+=r['bytes']
        cuts.append((abs(total/2-cumulative),i,cumulative))
    _,k,left=min(cuts)
    ratio=left/total
    if w>=h:
        return rectangles(items[:k],x,y,w*ratio,h)+rectangles(items[k:],x+w*ratio,y,w*(1-ratio),h)
    return rectangles(items[:k],x,y,w,h*ratio)+rectangles(items[k:],x,y+h*ratio,w,h*(1-ratio))


def posters(rows):
    out={}
    total=sum(r['bytes'] for r in rows)
    by_size=sorted(rows,key=lambda r:(-r['bytes'],r['id']))
    color={r['id']:COLORS[i] for i,r in enumerate(rows)}
    body=''
    for r,x,y,w,h in rectangles(by_size,30,100,650,360):
        body+=f'<rect x="{x:.4f}" y="{y:.4f}" width="{w:.4f}" height="{h:.4f}" fill="{color[r["id"]]}" stroke="#2c212b" stroke-width="1"><title>{escape(r["path"])}: {r["bytes"]} B</title></rect>'
        if w>55 and h>34:
            caption=f'{r["id"]} / {r["format"]}'
            if w < len(caption)*8+16:
                caption=r['id']
            body+=text(round(x+8,2),round(y+23,2),caption,13,'#2c212b')
    for i,r in enumerate(rows):
        body+=text(708,114+i*29,f'{r["id"]} {r["format"]:7} {r["bytes"]:>8} B',13,color[r['id']])
    out['treemap']=plate('01 / ПЛОЩАДЬ ИМЕЕТ ЗНАЧЕНИЕ',f'Площадь прямоугольника ∝ байтам файла · всего в выборке {total:,} B.',body)
    body=''
    circumference=2*math.pi*135
    offset=0
    for r in by_size:
        length=circumference*r['bytes']/total
        body+=f'<circle cx="240" cy="280" r="135" fill="none" stroke="{color[r["id"]]}" stroke-width="42" stroke-dasharray="{length:.6f} {circumference-length:.6f}" stroke-dashoffset="{-offset:.6f}" transform="rotate(-90 240 280)"/>'
        offset+=length
    body+=text(240,277,'12 ФОРМАТОВ',24,attrs='text-anchor="middle"')+text(240,308,f'{total/1024/1024:.2f} MiB',18,MUTED,'text-anchor="middle"')
    for i,r in enumerate(by_size):
        body+=text(455,120+i*29,f'{r["id"]} .{r["format"]:7} {100*r["bytes"]/total:6.2f}%   {r["bytes"]:>8} B',14,color[r['id']])
    out['donut']=plate('02 / КОЛЬЦЕВОЙ АТЛАС ФОРМАТОВ','Один выбранный файл на формат · сектор ∝ байтам, не числу файлов.',body)
    body=line([(65,115),(65,422),(960,422)],'#806778')
    cumulative=0
    points=[]
    for i,r in enumerate(by_size):
        x=90+i*75
        h=270*r['bytes']/by_size[0]['bytes']
        body+=f'<rect x="{x}" y="{422-h:.3f}" width="42" height="{h:.3f}" fill="{color[r["id"]]}"/>'
        body+=text(x+21,445,r['id'],13,attrs='text-anchor="middle"')
        cumulative+=r['bytes']
        points.append((x+21,422-290*cumulative/total))
    body+=line(points,TEXT,2)
    for x,y in points:
        body+=f'<circle cx="{x}" cy="{y:.3f}" r="3" fill="{TEXT}"/>'
    body+=text(970,137,'100%',12)+text(970,426,'0%',12)
    body+=text(85,113,'столбики: байты / максимум',13,MUTED)+text(530,113,'линия: накопленная доля (правая шкала)',12,MUTED)
    out['pareto']=plate('03 / КТО ЗАНИМАЕТ МЕСТО','Файлы упорядочены по размеру; коды 01…12 раскрыты в CSV.',body)
    body=''
    for i,r in enumerate(rows):
        y=118+i*28
        ratio=r['zlib_bytes']/r['bytes']
        body+=text(32,y+5,f'{r["id"]} {r["format"]:7}',13,color[r['id']])
        body+=f'<rect x="175" y="{y-11}" width="600" height="17" rx="3" fill="#58414e"/>'
        body+=f'<rect x="175" y="{y-11}" width="{600*ratio:.3f}" height="17" rx="3" fill="{color[r["id"]]}"/>'
        body+=text(815,y+4,f'{100*ratio:6.1f}% / {r["zlib_bytes"]:>7} B',13)
    out['compression']=plate('04 / НАСКОЛЬКО СЖИМАЕТСЯ РИСУНОК','zlib level 9 / исходные байты · это опыт, НЕ HTTP-размер загрузки GitHub.',body)
    body=''
    for col in range(16):
        body+=text(205+col*34,112,f'{col:02X}',12,MUTED)
    for i,r in enumerate(rows):
        y=128+i*27
        body+=text(32,y+15,f'{r["id"]} {r["format"]:7}',13,color[r['id']])
        for j,byte in enumerate(bytes.fromhex(r['first16_hex'])):
            # Sixteen discrete luminance levels, actual hex printed on each cell.
            value=byte//16
            shade=70+value*10
            fill=f'#{shade:02x}{int(shade*.86):02x}{int(shade*.7):02x}'
            body+=f'<rect x="{198+j*34}" y="{y}" width="31" height="22" rx="2" fill="{fill}"/>'
            body+=text(202+j*34,y+15,f'{byte:02X}',11,'#241c26' if value>7 else '#fff3de')
        body+=text(765,y+15,r['first16_hex'][:8],12,MUTED)
    out['headers']=plate('05 / ПАСПОРТ ПЕРВЫХ БАЙТОВ','16 реальных байтов каждого файла · яркость = старшая hex-цифра · текст = весь байт.',body)
    body=''
    selected=[rows[i] for i in (0,1,6,7)]
    for i,r in enumerate(selected):
        x0=40+(i%2)*500; y0=120+(i//2)*176
        body+=text(x0,y0,f'{r["id"]} / {r["format"]} / {r["bytes"]} B',15,color[r['id']])
        peak=max(r['histogram16'])/r['bytes']
        for j,count in enumerate(r['histogram16']):
            height=110*count/r['bytes']
            body+=f'<rect x="{x0+j*27}" y="{y0+125-height:.4f}" width="22" height="{height:.4f}" fill="{color[r["id"]]}"/>'
            body+=text(x0+j*27+7,y0+143,f'{j:X}',10,MUTED)
        body+=text(x0+265,y0+20,f'пик {100*peak:.1f}%',12,MUTED)
        body+=line([(x0,y0+15),(x0,y0+125),(x0+432,y0+125)],'#806778',1)
    out['spectrum']=plate('06 / СПЕКТР СЫРЫХ БАЙТОВ','16 диапазонов 00–0F … F0–FF · общая шкала высоты 0…100% байтов файла.',body)
    return out


def generate(output,root=ROOT):
    rows=collect(root)
    output.mkdir(parents=True,exist_ok=True)
    for name,svg in posters(rows).items():
        (output/f'{name}.svg').write_text(svg,encoding='utf-8')
    stream=io.StringIO(newline='')
    fields=['id','path','format','bytes','zlib_bytes','sha256','first16_hex']
    writer=csv.DictWriter(stream,fieldnames=fields,extrasaction='ignore',lineterminator='\n')
    writer.writeheader(); writer.writerows(rows)
    (output/'files.csv').write_text(stream.getvalue(),encoding='utf-8')
    data={'scope':'Explicit sample, NOT whole repository', 'zlib_version':zlib.ZLIB_RUNTIME_VERSION,
          'files':rows,'total_bytes':sum(r['bytes'] for r in rows)}
    (output/'measurements.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'assets/cabinet')
    args=parser.parse_args()
    generate(args.output)
