#!/usr/bin/env python3
"""A static hidden-relief image and a blind correspondence check, made locally."""
import argparse
from bisect import bisect_left
import hashlib
import io
import json
from pathlib import Path
import zipfile

import numpy as np
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[3]
WIDTH=960
HEIGHT=480
EYE=160
MU=.4
SEED=0x6D6F6F6E
PALETTE=np.array([
    [16,49,60],[27,72,80],[43,99,104],[62,127,124],
    [94,154,140],[140,179,154],[190,202,170],[237,218,180],
    [183,122,78],[218,160,103],[99,95,85],[45,65,83],
    [29,86,90],[115,151,139],[163,191,161],[219,206,163],
],dtype=np.uint8)
MIN_LAG=60
MAX_LAG=80


def depthmap():
    """Analytic rounded ring and separate raised satellite, not a copied depth asset."""
    y,x=np.mgrid[:HEIGHT,:WIDTH]
    radius=np.sqrt((x-465.)**2+(y-245.)**2)
    ring=.9*np.sqrt(np.maximum(0,1-((radius-124)/34)**2))
    satellite=.75*np.sqrt(np.maximum(0,1-((x-688.)**2+(y-129.)**2)/37**2))
    return np.maximum(ring,satellite)


def separation(depth):
    return np.floor(EYE*(1-MU*np.asarray(depth))/(2-MU*np.asarray(depth))+.5).astype(np.int16)


def links_for_row(depth):
    """Greedy near-first, one-to-one, order-preserving correspondence matching.

    A pixel may have an incoming and outgoing edge; because all edges point right,
    they form chains. Shorter separation (nearer relief) gets priority. Duplicate
    projections and order inversions are rejected, not forced into one large union.
    This is a discrete matching approximation, not a full continuous ray tracer.
    """
    width=len(depth)
    lags=separation(depth)
    candidates=[]
    for x,s in enumerate(lags):
        s=int(s);left=x-s//2;right=left+s
        if 0<=left<right<width:
            candidates.append((s,x,left,right))
    candidates.sort()
    lefts=[];rights=[];edges=[];used_right=set()
    for s,x,left,right in candidates:
        i=bisect_left(lefts,left)
        if i<len(lefts) and lefts[i]==left:continue
        if right in used_right:continue
        if i>0 and rights[i-1]>=right:continue
        if i<len(rights) and rights[i]<=right:continue
        lefts.insert(i,left);rights.insert(i,right);used_right.add(right)
        edges.append((x,left,right,s))
    incoming=np.arange(width,dtype=np.int16)
    for _,left,right,_ in edges:incoming[right]=left
    roots=np.empty(width,dtype=np.int16)
    for x in range(width):roots[x]=x if incoming[x]==x else roots[int(incoming[x])]
    return roots,edges


def noise(y,x):
    """Explicit 32-bit integer mixer, stable across numpy/Python versions."""
    value=(SEED+y*0x9E3779B9+x*0x85EBCA6B)&0xFFFFFFFF
    value=((value^(value>>16))*0x7FEB352D)&0xFFFFFFFF
    value=((value^(value>>15))*0x846CA68B)&0xFFFFFFFF
    return (value^(value>>16))&0xFFFFFFFF


def encode(depth):
    height,width=depth.shape
    output=np.empty((height,width,3),dtype=np.uint8)
    counts=[];sample=[]
    for y,row in enumerate(depth):
        roots,edges=links_for_row(row)
        color=np.array([noise(y,x)%len(PALETTE) for x in range(width)])
        output[y]=PALETTE[color[roots]]
        counts.append(len(edges))
        if y==HEIGHT//2:sample=[list(edge) for edge in sorted(edges)]
    return output,counts,sample


def box_average(array,rx=5,ry=2):
    padded=np.pad(array,((ry,ry),(rx,rx)),mode='edge')
    integral=np.pad(padded,((1,0),(1,0))).cumsum(0).cumsum(1)
    h=2*ry+1;w=2*rx+1
    return (integral[h:,w:]-integral[:-h,w:]-integral[h:,:-w]+integral[:-h,:-w])/(w*h)


def decode(pixels):
    """Blind local matching: accepts only RGB pixels, never depth, links or seed."""
    height,width,_=pixels.shape
    costs=[]
    for lag in range(MIN_LAG,MAX_LAG+1):
        left_offset=lag//2;right_offset=lag-left_offset
        mismatch=np.ones((height,width),dtype=np.float64)
        mismatch[:,left_offset:width-right_offset]=np.any(
            pixels[:,:width-lag]!=pixels[:,lag:],axis=2)
        costs.append(box_average(mismatch))
    costs=np.array(costs)
    # On exact ties prefer the background lag rather than inventing a near surface.
    selected=MAX_LAG-np.argmin(costs[::-1],axis=0)
    minimum=np.min(costs,axis=0)
    return selected.astype(np.uint8),minimum


def lag_to_depth(lag):
    lag=np.asarray(lag,dtype=np.float64)
    return np.clip((EYE-2*lag)/(MU*(EYE-lag)),0,1)


def decode_file(source,dest):
    with Image.open(source) as image:pixels=np.array(image.convert('RGB'))
    lag,_=decode(pixels)
    Image.fromarray(np.uint8(np.round(lag_to_depth(lag)*255))).save(dest)
    return lag


def png_bytes(array):
    stream=io.BytesIO();Image.fromarray(array).save(stream,format='PNG');return stream.getvalue()


def proof(depth,lag):
    """Explain source vs recovered relief; do not label the target as a decode."""
    poster=Image.new('RGB',(1040,1160),'#f2e9d3');draw=ImageDraw.Draw(poster)
    draw.text((30,22),'HIDDEN RELIEF / SOURCE AND BLIND RECOVERY',fill='#1b4850')
    panels=[('SOURCE DEPTH / NOT A DECODE',np.uint8(np.round(depth*255))),
            ('DECODED FROM PNG ONLY / BLOCK MATCHING',np.uint8(np.round(lag_to_depth(lag)*255)))]
    for i,(label,data) in enumerate(panels):
        image=Image.fromarray(data).convert('RGB')
        yy=68+i*530
        draw.text((40,yy-22),label,fill='#1b4850');poster.paste(image,(40,yy))
    draw.text((40,1125),'BRIGHTER = NEARER. DEPTH SHAPE IS NOT A PERCEPTION GUARANTEE.',fill='#1b4850')
    return poster


def make_bench(facts):
    """No runtime encoder: inspect the emitted image and one computed link row."""
    payload=json.dumps({'width':WIDTH,'height':HEIGHT,'row':HEIGHT//2,'pairs':facts['sample_row_edges']})
    return '''<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Скрытый рельеф — стол соответствий</title>
<style>body{font:18px system-ui;background:#f2e9d3;color:#1b4850;max-width:1000px;margin:25px auto;padding:0 16px}canvas{width:100%;height:auto}button,input{font:inherit}button{padding:10px}input{width:100%}:focus-visible{outline:3px solid #b77a4e}output{display:block;padding:14px 0}</style>
<h1>Скрытый рельеф</h1><p>Стереограмма неподвижна. Здесь можно проверить, какие точки связаны в средней строке: они имеют одинаковый RGB. Сдвиг ползунка не меняет исходный PNG.</p>
<canvas id="view" width="960" height="540" aria-label="Узор или карта глубины; под узором выделена пара точек средней строки"></canvas>
<p><button id="mode">Показать карту глубины</button> <button id="reset">В начало</button></p>
<label for="pair">Соответствие в строке 240</label><input id="pair" type="range" min="0" value="0"><output id="status" aria-live="polite"></output>
<p>Не нужно добиваться объёма силой. Если не видно — открой карту глубины; при дискомфорте прекрати просмотр. Это не проверка зрения. Карта — исходная цель, не результат декодирования. Ничего не сохраняется, сеть не нужна.</p>
<script>const data=PAYLOAD;const c=document.querySelector('#view'),ctx=c.getContext('2d'),slider=document.querySelector('#pair'),button=document.querySelector('#mode');slider.max=data.pairs.length-1;let showDepth=false;const pattern=new Image(),depth=new Image();let loaded=0;const ready=()=>{loaded++;if(loaded===2)draw()};pattern.onload=ready;depth.onload=ready;pattern.src='stereogram.png';depth.src='depth.png';
function draw(){if(loaded!==2)return;ctx.fillStyle='#f2e9d3';ctx.fillRect(0,0,c.width,c.height);ctx.drawImage(showDepth?depth:pattern,0,0);const [x,l,r,s]=data.pairs[Number(slider.value)];if(!showDepth){ctx.strokeStyle='#f7db99';ctx.lineWidth=2;ctx.beginPath();ctx.arc(l,data.row,6,0,7);ctx.moveTo(r+6,data.row);ctx.arc(r,data.row,6,0,7);ctx.stroke();ctx.beginPath();ctx.moveTo(l,490);ctx.lineTo(r,490);ctx.stroke();ctx.fillStyle='#1b4850';ctx.font='16px system-ui';ctx.fillText('l='+l+'   r='+r+'   separation='+s+' px',30,520)}document.querySelector('#status').textContent=showDepth?'Исходная карта: светлее — ближе.':'Строка '+data.row+', центр '+x+': пиксели '+l+' и '+r+', расстояние '+s+' px; RGB совпадает.';button.textContent=showDepth?'Вернуть узор':'Показать карту глубины';slider.disabled=showDepth}
slider.addEventListener('input',draw);button.onclick=()=>{showDepth=!showDepth;draw()};document.querySelector('#reset').onclick=()=>{showDepth=false;slider.value=0;draw()};</script></html>'''.replace('PAYLOAD',payload)


def deterministic_zip(path,files):
    with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED) as archive:
        for name,content in sorted(files.items()):
            item=zipfile.ZipInfo(name,date_time=(2026,11,18,0,0,0));item.compress_type=zipfile.ZIP_DEFLATED
            item.external_attr=0o644<<16;archive.writestr(item,content)


def generate(output):
    output.mkdir(parents=True,exist_ok=True)
    depth=depthmap();pixels,counts,sample=encode(depth)
    raw=png_bytes(pixels);(output/'stereogram.png').write_bytes(raw)
    depth_bytes=png_bytes(np.uint8(np.round(depth*255)));(output/'depth.png').write_bytes(depth_bytes)
    # Deliberately read the exported PNG back, not the encoder's working buffer.
    lag=decode_file(output/'stereogram.png',output/'recovered.png')
    expected=separation(depth)
    y,x=np.mgrid[:HEIGHT,:WIDTH];interior=(x>=100)&(x<WIDTH-100)&(y>=10)&(y<HEIGHT-10)
    foreground=(expected<77)&interior;predicted=(lag<77)&interior
    union=np.sum(foreground|predicted);iou=float(np.sum(foreground&predicted)/union)
    facts={'width':WIDTH,'height':HEIGHT,'eye_parameter_px':EYE,'mu':MU,'seed':SEED,
           'background_separation_px':int(separation(0)),'minimum_separation_px':int(np.min(expected)),
           'edges_per_row':counts,'sample_row':HEIGHT//2,'sample_row_edges':sample,
           'decode':{'algorithm':'RGB inequality, 11x5 mean mismatch, lags 60..80; ties prefer larger lag',
                     'interior_x':[100,WIDTH-100],'interior_y':[10,HEIGHT-10],'foreground_threshold_lag':77,
                     'mean_absolute_lag_error_px':float(np.mean(np.abs(lag.astype(float)-expected)[interior])),
                     'foreground_iou':iou},
           'sha256':hashlib.sha256(raw).hexdigest(),
           'limits':'Discrete ordered correspondence matching, not full optical ray tracing or a human-vision test.'}
    (output/'facts.json').write_text(json.dumps(facts,ensure_ascii=False,indent=2)+'\n')
    proof(depth,lag).save(output/'proof.png')
    html=make_bench(facts).encode();(output/'bench.html').write_bytes(html)
    deterministic_zip(output/'bench.zip',{'bench.html':html,'stereogram.png':raw,'depth.png':depth_bytes})
    print(json.dumps(facts['decode'],indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'assets/stereogram')
    parser.add_argument('--decode',type=Path,help='Decode a supplied PNG only; --output is destination PNG in this mode')
    args=parser.parse_args()
    if args.decode:decode_file(args.decode,args.output)
    else:generate(args.output)
