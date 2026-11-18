#!/usr/bin/env python3
"""An original crescent reconstructed as a single continuous nail-to-nail thread."""
import argparse
import csv
import io
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

ROOT=Path(__file__).resolve().parents[3]
SIZE=192
COUNT=144
RADIUS=88
STRENGTH=.065
MIN_GAP=7
MAX_STEPS=1800
DIAMETER_MM=160


def nails():
    return [(round((SIZE-1)/2+RADIUS*math.sin(2*math.pi*i/COUNT)),
             round((SIZE-1)/2-RADIUS*math.cos(2*math.pi*i/COUNT))) for i in range(COUNT)]


def target():
    y,x=np.mgrid[:SIZE,:SIZE]
    # Self-authored analytic crescent, not a downloaded portrait or logo.
    outer=(x-91)**2+(y-94)**2<59**2
    cutout=(x-116)**2+(y-76)**2<53**2
    return (outer & ~cutout).astype(np.float64)*.78


def chord(a,b):
    """Integer Bresenham, unique pixels, independent of traversal direction."""
    if a>b:a,b=b,a
    x,y=a;tx,ty=b
    dx=abs(tx-x);dy=-abs(ty-y);sx=1 if x<tx else -1;sy=1 if y<ty else -1
    error=dx+dy;out=[]
    while True:
        out.append(y*SIZE+x)
        if (x,y)==(tx,ty):break
        e2=2*error
        if e2>=dy:error+=dy;x+=sx
        if e2<=dx:error+=dx;y+=sy
    return np.array(out,dtype=np.int32)


def valid(a,b):
    gap=abs(a-b)
    return min(gap,COUNT-gap)>=MIN_GAP


def solve(limit=MAX_STEPS):
    positions=nails();reference=target().ravel();density=np.zeros(SIZE*SIZE)
    cache={(a,b):chord(positions[a],positions[b]) for a in range(COUNT) for b in range(a+1,COUNT) if valid(a,b)}
    route=[0];errors=[float(np.sum(reference**2))]
    for _ in range(limit):
        a=route[-1];best_gain=1e-12;best=None
        for b in range(COUNT):
            if not valid(a,b):continue
            ix=cache[tuple(sorted((a,b)))];old=density[ix];new=np.minimum(1,old+STRENGTH)
            gain=float(np.sum((reference[ix]-old)**2-(reference[ix]-new)**2))
            if gain>best_gain:
                best_gain=gain;best=(b,ix,new)
        if best is None:break
        b,ix,new=best;density[ix]=new;route.append(b)
        errors.append(float(np.sum((reference-density)**2)))
    return route,errors


def reconstruct(route):
    density=np.zeros(SIZE*SIZE);points=nails()
    for a,b in zip(route,route[1:]):
        ix=chord(points[a],points[b]);density[ix]=np.minimum(1,density[ix]+STRENGTH)
    return density.reshape(SIZE,SIZE)


def field_image(density):
    paper=np.array([244,235,212]);ink=np.array([34,57,66])
    rgb=paper[None,None,:]*(1-density[:,:,None])+ink[None,None,:]*density[:,:,None]
    return Image.fromarray(np.uint8(np.round(rgb)))


def plate(density,step,total,side=768):
    image=Image.new('RGB',(side,side),(244,235,212))
    border=64
    field=field_image(density).resize((side-2*border,side-2*border),Image.Resampling.BILINEAR)
    image.paste(field,(border,border));d=ImageDraw.Draw(image)
    def p(x,y):return border+x*(side-2*border)/SIZE,border+y*(side-2*border)/SIZE
    for i,(x,y) in enumerate(nails()):
        xx,yy=p(x,y);d.ellipse((xx-1.8,yy-1.8,xx+1.8,yy+1.8),fill='#ac714b' if i else '#225360')
    d.text((30,24),'THREAD MOON / 144 PINS / ONE UNBROKEN ROUTE',fill='#223942')
    d.text((30,side-34),f'{step:04} / {total:04} CHORDS   -   NOT A PHOTO OF A PHYSICAL OBJECT',fill='#223942')
    return image


def print_template(path):
    c=canvas.Canvas(str(path),pagesize=(210*mm,297*mm),invariant=1)
    c.setTitle('Thread Moon - 160 mm pin template')
    cx,cy,r=105*mm,160*mm,DIAMETER_MM/2*mm
    c.setFont('Helvetica-Bold',15);c.drawString(18*mm,278*mm,'THREAD MOON / PIN TEMPLATE')
    c.setFont('Helvetica',9)
    for i,line in enumerate(['Print A4 at 100%; disable fit-to-page. Check the 50 mm scale.',
                             '144 pins, clockwise; 000 at top. Pin-circle diameter: 160 mm.',
                             'Tie at pin 000, then follow route.csv. Do not cut between rows.',
                             'Ideal centreline model: allow extra thread for wraps and knots.']):
        c.drawString(18*mm,(269-i*5)*mm,line)
    c.setLineWidth(.3);c.circle(cx,cy,r)
    for i in range(COUNT):
        angle=2*math.pi*i/COUNT
        x=cx+r*math.sin(angle);y=cy+r*math.cos(angle)
        c.circle(x,y,.4*mm,stroke=1,fill=0)
        c.setFont('Helvetica',5.5)
        c.drawCentredString(cx+(r+5*mm)*math.sin(angle),cy+(r+5*mm)*math.cos(angle)-1.6,f'{i:03}')
    c.setLineWidth(.8);c.line(20*mm,35*mm,70*mm,35*mm)
    for x in (20,70):c.line(x*mm,33*mm,x*mm,37*mm)
    c.setFont('Helvetica',9);c.drawString(20*mm,28*mm,'50 mm / calibration - measure before use')
    c.showPage();c.save()


def generate(output):
    output.mkdir(parents=True,exist_ok=True)
    route,errors=solve();steps=len(route)-1;points=nails()
    records=[];length=0
    for step,(a,b) in enumerate(zip(route,route[1:]),1):
        # Physical points are exact points on the ideal circle, not rounded raster points.
        distance=DIAMETER_MM*abs(math.sin(math.pi*(a-b)/COUNT))
        length+=distance/1000
        records.append([step,f'{a:03}',f'{b:03}',f'{distance:.6f}',f'{length:.6f}'])
    with (output/'route.csv').open('w',newline='') as f:
        writer=csv.writer(f,lineterminator='\n');writer.writerow(['step','from_pin','to_pin','chord_mm','cumulative_m']);writer.writerows(records)
    facts={'pins':COUNT,'steps':steps,'start_pin':0,'route':route,'diameter_mm':DIAMETER_MM,
           'minimum_pin_gap':MIN_GAP,'density_per_chord':STRENGTH,'grid':SIZE,
           'ideal_chord_length_m':length,'initial_sse':errors[0],'final_sse':errors[-1],
           'sse_by_step':errors,'stop':'no positive local gain' if steps<MAX_STEPS else 'step budget',
           'model':'Saturating additive darkness on unique Bresenham pixels; not physical thread reflectance.'}
    (output/'facts.json').write_text(json.dumps(facts,indent=2)+'\n')
    final=reconstruct(route)
    plate(final,steps,steps).save(output/'moon.png')
    plate(target(),0,steps).save(output/'target.png')
    indexes=sorted(set([0,steps]+[round(steps*i/35) for i in range(36)]))
    frames=[plate(reconstruct(route[:i+1]),i,steps,512) for i in indexes]
    # Fixed explicit palette: deterministic quantization shared by every frame.
    palette=Image.new('P',(1,1));colors=[]
    for i in range(256):
        t=i/255;colors.extend([round(244*(1-t)+34*t),round(235*(1-t)+57*t),round(212*(1-t)+66*t)])
    palette.putpalette(colors)
    indexed=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
    indexed[0].save(output/'winding.gif',save_all=True,append_images=indexed[1:],loop=0,
                    duration=[140]*(len(indexed)-1)+[2400],disposal=2,optimize=False)
    print_template(output/'pins-a4.pdf')
    # A browser can open this standalone aid offline; it does not run inside README.
    payload=json.dumps({'route':route,'pins':points,'size':SIZE})
    html='''<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Нитяная луна — счётчик</title>
<style>body{font:18px system-ui;max-width:760px;margin:30px auto;padding:0 20px;background:#f4ebd4;color:#223942}canvas{width:100%;height:auto}button,input{font:inherit}button{padding:10px}input{width:100%}:focus-visible{outline:3px solid #ab704b}output{display:block;margin:15px 0}</style>
<h1>Нитяная луна</h1><p>Один маршрут, без разрывов. Закрепи нить на гвоздике 000. Нажимай «Дальше» после каждого законченного перехода. Нумерация по часовой стрелке, 000 сверху.</p>
<canvas id="view" width="768" height="768" aria-label="Схема намотанных хорд и выделенный текущий переход"></canvas>
<output id="status" aria-live="polite"></output><button id="prev">Назад</button> <button id="next">Дальше</button> <button id="reset">Сначала</button>
<p><label for="step">Перейти к шагу</label><input id="step" type="range" min="0" value="0"></p>
<p>Прогресс не сохраняется автоматически. Запиши номер шага перед закрытием. Рисунок — схематические линии, не фотометрическая модель PNG. Здесь нет сети и автопроигрывания; на GitHub HTML показывается как исходник. Скачай файл и открой локально.</p>
<script>const data=PAYLOAD;const slider=document.querySelector('#step'),status=document.querySelector('#status'),ctx=document.querySelector('#view').getContext('2d');slider.max=data.route.length-1;
function point(i){const p=data.pins[i];return [64+p[0]*640/data.size,64+p[1]*640/data.size]}
function draw(){const n=Number(slider.value);ctx.fillStyle='#f4ebd4';ctx.fillRect(0,0,768,768);for(let k=1;k<=n;k++){const a=point(data.route[k-1]),b=point(data.route[k]);ctx.strokeStyle=k===n?'#b05e32':'rgba(34,57,66,.11)';ctx.lineWidth=k===n?2:1;ctx.beginPath();ctx.moveTo(...a);ctx.lineTo(...b);ctx.stroke()}data.pins.forEach((_,i)=>{const [x,y]=point(i);ctx.fillStyle='#223942';ctx.beginPath();ctx.arc(x,y,2,0,7);ctx.fill()});const pin=i=>String(i).padStart(3,'0');status.textContent=n===0?'Начало: закрепи нить на 000. Всего переходов: '+slider.max:'Шаг '+n+' / '+slider.max+': '+pin(data.route[n-1])+' → '+pin(data.route[n])+(n===Number(slider.max)?' — маршрут закончен.':'');document.querySelector('#prev').disabled=n===0;document.querySelector('#next').disabled=n===Number(slider.max)}
slider.addEventListener('input',draw);document.querySelector('#prev').onclick=()=>{slider.value=Number(slider.value)-1;draw()};document.querySelector('#next').onclick=()=>{slider.value=Number(slider.value)+1;draw()};document.querySelector('#reset').onclick=()=>{slider.value=0;draw()};draw();</script></html>'''.replace('PAYLOAD',payload)
    (output/'counter.html').write_text(html,encoding='utf-8')
    print(f'{steps} chords; ideal length {length:.2f} m; SSE {errors[0]:.2f} -> {errors[-1]:.2f}')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'assets/threadmoon')
    generate(parser.parse_args().output)
