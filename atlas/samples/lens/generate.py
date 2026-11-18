#!/usr/bin/env python3
"""Original point-mass thin-lens scene. Not a black-hole/geodesic simulation."""
import argparse
import csv
import json
import math
from pathlib import Path
import random
import zipfile

import numpy as np
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[3]
SIZE=384
EXTENT=2.25
FRAMES=32
BENCH_SIZE=192


def stars():
    rng=random.Random(20261118)
    return [[rng.uniform(-3,3),rng.uniform(-3,3),rng.uniform(.006,.019),rng.uniform(.07,.5)] for _ in range(36)]


STARS=stars()


def coordinates(size):
    axis=np.linspace(-EXTENT,EXTENT,size)
    return np.meshgrid(axis,axis)


def lens_map(x,y,e=1.):
    x,y=np.broadcast_arrays(np.asarray(x,dtype=float),np.asarray(y,dtype=float))
    if e<0:raise ValueError('Einstein radius cannot be negative')
    if e==0:return x.copy(),y.copy()
    r2=x*x+y*y
    factor=np.full_like(r2,np.nan)
    np.divide(e*e,r2,out=factor,where=r2>0)
    return x*(1-factor),y*(1-factor)


def point_images(bx,by,e=1.):
    radius=math.hypot(bx,by)
    if radius==0 or e<=0:raise ValueError('use the Einstein ring at beta=0; e must be positive')
    root=math.sqrt(radius*radius+4*e*e)
    return [((radius+sign*root)/2*bx/radius,(radius+sign*root)/2*by/radius) for sign in (1,-1)]


def background(x,y):
    light=np.zeros((*np.broadcast_shapes(np.shape(x),np.shape(y)),3))+[.008,.014,.024]
    for sx,sy,width,brightness in STARS:
        amount=brightness*np.exp(-((x-sx)**2+(y-sy)**2)/(2*width*width))
        light+=amount[...,None]*[.68,.8,1.]
    return light


def galaxy(x,y,offset=0.):
    dx=x-offset;r=np.hypot(dx,y);angle=np.arctan2(y,dx)
    core=2.7*np.exp(-(r/.035)**2)
    disk=.36*np.exp(-r/.13)
    arms=.32*np.exp(-(r/.19)**2)*(.5+.5*np.cos(2*angle-24*r))**3
    return core[...,None]*[1.,.72,.4]+disk[...,None]*[.3,.52,1.]+arms[...,None]*[.28,.7,1.]


def encode_rgb(light):
    return np.uint8(np.clip(np.floor(255*(-np.expm1(-3*np.nan_to_num(light,nan=0)))+.5),0,255))


def render(size=SIZE,offset=0.,e=1.):
    x,y=coordinates(size);bx,by=lens_map(x,y,e)
    return encode_rgb(background(x,y)+galaxy(x,y,offset)),encode_rgb(background(bx,by)+galaxy(bx,by,offset))


def plate(source,lensed,offset):
    image=Image.new('RGB',(1000,600),'#122a38');d=ImageDraw.Draw(image)
    title=ImageFont.load_default(size=20);small=ImageFont.load_default(size=14)
    d.text((28,20),'ONE GALAXY / TWO IMAGES / ONE EINSTEIN RING',font=title,fill='#edd3a2')
    d.text((28,52),'POINT-MASS THIN LENS / DIMENSIONLESS ANGLES / NOT A BLACK-HOLE SHADOW',font=small,fill='#a9c8c8')
    for data,x,label in ((source,28,'SOURCE PLANE'),(lensed,520,'OBSERVED IMAGE')):
        d.text((x,86),label,font=small,fill='#edd3a2')
        image.paste(Image.fromarray(data).resize((448,448),Image.Resampling.BICUBIC),(x,109))
    d.text((28,572),f'source offset = {offset:+.3f} theta_E     /     beta = theta - theta / |theta|^2',font=small,fill='#a9c8c8')
    return image


def bench_html():
    config=json.dumps({'size':BENCH_SIZE,'extent':EXTENT,'stars':STARS})
    return '''<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Одна галактика — два изображения</title>
<style>body{font:18px system-ui;background:#122a38;color:#d5e2da;max-width:1000px;margin:25px auto;padding:0 18px}.views{display:grid;grid-template-columns:1fr 1fr;gap:20px}canvas{width:100%;height:auto}button,input{font:inherit}input{width:100%}button{padding:10px}:focus-visible{outline:3px solid #edd3a2}output{display:block;padding:12px 0}@media(max-width:540px){.views{grid-template-columns:1fr}}</style>
<h1>Одна галактика — два изображения</h1><div class="views"><div><p>Плоскость источника</p><canvas id="source" width="192" height="192" aria-label="Одна процедурная галактика и фоновые звёзды"></canvas></div><div><p>Наблюдаемое изображение</p><canvas id="lensed" width="192" height="192" aria-label="Результат обратного отображения тонкой точечной линзой"></canvas></div></div>
<label for="offset">Смещение галактики относительно оси, условные углы</label><input id="offset" type="range" min="-0.9" max="0.9" step="0.01" value="0">
<label for="radius">Радиус Эйнштейна, условные углы (0 = без линзы)</label><input id="radius" type="range" min="0" max="1.3" step="0.01" value="1"><button id="align">На ось, радиус 1</button><output id="status" aria-live="polite"></output>
<p>Это тонкая линза — точечная масса, а не симуляция чёрной дыры. Нет горизонта событий, аккреционного диска, временных задержек и измеренной массы. Палитра художественная. Тёмная середина не означает «тень» чёрной дыры. Сеть не используется; меняется живой расчёт, не готовые кадры.</p>
<script>const cfg=CONFIG;const offset=document.querySelector('#offset'),radius=document.querySelector('#radius');
function sample(x,y,u){let R=.008,G=.014,B=.024;for(const [sx,sy,w,a] of cfg.stars){const q=a*Math.exp(-((x-sx)**2+(y-sy)**2)/(2*w*w));R+=q*.68;G+=q*.8;B+=q}const dx=x-u,r=Math.hypot(dx,y),angle=Math.atan2(y,dx),core=2.7*Math.exp(-((r/.035)**2)),disk=.36*Math.exp(-r/.13),arms=.32*Math.exp(-((r/.19)**2))*(.5+.5*Math.cos(2*angle-24*r))**3;return [R+core+disk*.3+arms*.28,G+core*.72+disk*.52+arms*.7,B+core*.4+disk+arms]}
function draw(){const n=cfg.size,u=Number(offset.value),e=Number(radius.value);for(const id of ['source','lensed']){const ctx=document.querySelector('#'+id).getContext('2d'),im=ctx.createImageData(n,n);for(let iy=0;iy<n;iy++)for(let ix=0;ix<n;ix++){let x=(ix/(n-1)*2-1)*cfg.extent,y=(iy/(n-1)*2-1)*cfg.extent;if(id==='lensed'&&e!==0){const f=1-e*e/(x*x+y*y);x*=f;y*=f}const rgb=sample(x,y,u),p=(iy*n+ix)*4;for(let k=0;k<3;k++)im.data[p+k]=Math.floor(255*(-Math.expm1(-3*rgb[k]))+.5);im.data[p+3]=255}ctx.putImageData(im,0,0)}document.querySelector('#status').textContent='Смещение '+u.toFixed(2)+'; радиус '+e.toFixed(2)+(e===0?' — линза выключена.':u===0?' — центр источника на оси.':' — два изображения одного источника.')}
offset.addEventListener('input',draw);radius.addEventListener('input',draw);document.querySelector('#align').onclick=()=>{offset.value=0;radius.value=1;draw()};draw();</script></html>'''.replace('CONFIG',config)


def generate(output):
    output.mkdir(parents=True,exist_ok=True)
    source,lensed=render()
    Image.fromarray(source).save(output/'source.png');Image.fromarray(lensed).save(output/'ring.png')
    # Preserve circles in the still poster: the plate layout uses square image panels.
    plate(source,lensed,0).save(output/'poster.png')
    frames=[];offsets=[]
    # Cache the static mapped backgrounds; only the galaxy moves in the sequence.
    x,y=coordinates(SIZE);bx,by=lens_map(x,y);bg=background(x,y);lbg=background(bx,by)
    for i in range(FRAMES):
        u=.85*math.sin(2*math.pi*i/FRAMES);offsets.append(u)
        frames.append(plate(encode_rgb(bg+galaxy(x,y,u)),encode_rgb(lbg+galaxy(bx,by,u)),u))
    # One deterministic palette learned from four actual frames, shared by all frames.
    training=Image.new('RGB',(1000,600*4))
    for j,i in enumerate((0,4,8,12)):training.paste(frames[i],(0,j*600))
    palette=training.quantize(colors=256,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
    indexed=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
    indexed[0].save(output/'crossing.gif',save_all=True,append_images=indexed[1:],loop=0,duration=140,disposal=2,optimize=False)
    rows=[]
    for beta in (.1,.25,.55,.85):
        for sign,(tx,ty) in zip(('outer','inner'),point_images(beta,0)):
            sx,sy=lens_map(tx,ty)
            rows.append([beta,sign,tx,ty,float(sx),float(sy),float(1-1/(tx*tx+ty*ty)**2)])
    with (output/'images.csv').open('w',newline='') as f:
        writer=csv.writer(f,lineterminator='\n');writer.writerow(['source_beta_x','image','theta_x','theta_y','mapped_beta_x','mapped_beta_y','jacobian_determinant']);writer.writerows(rows)
    bench_source,bench_lensed=render(BENCH_SIZE)
    Image.fromarray(bench_source).save(output/'bench-source.png');Image.fromarray(bench_lensed).save(output/'bench-ring.png')
    facts={'model':'single point-mass thin lens; no black-hole shadow or GR geodesic integration',
           'size':SIZE,'extent':EXTENT,'einstein_radius':1.,'frames':FRAMES,'frame_duration_ms':140,
           'source_offsets':offsets,'stars':STARS,'sample_source':[.55,0.],
           'sample_images':[list(p) for p in point_images(.55,0)],
           'limitations':['synthetic galaxy and star positions; not telescope data','dimensionless angles; no inferred mass or distances','geometric optics, one lens plane, point mass','fixed exposure and artistic RGB; not observed spectra','no time delay, diffraction, PSF or relativistic event horizon']}
    (output/'facts.json').write_text(json.dumps(facts,indent=2)+'\n')
    html=bench_html().encode();(output/'bench.html').write_bytes(html)
    with zipfile.ZipFile(output/'bench.zip','w',compression=zipfile.ZIP_DEFLATED) as archive:
        info=zipfile.ZipInfo('bench.html',(2026,11,18,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
        archive.writestr(info,html)
    print('Point-mass thin lens; 32 frames; images for beta=.55:',point_images(.55,0))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=ROOT/'assets/lens')
    generate(parser.parse_args().output)
