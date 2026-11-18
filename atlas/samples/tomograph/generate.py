#!/usr/bin/env python3
"""Generate an original mechanical phantom and analytic line integrals, then forget it to reconstruct."""
import argparse
import csv
import json
import math
from pathlib import Path
import zipfile
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import reconstruct as inverse

ROOT=Path(__file__).resolve().parents[3]
DETECTORS=256
ANGLES=120
SIZE=192
COUNTS=(2,3,4,5,6,8,10,12,15,20,24,30,40,60,120)
# density, center x/y, semiaxes a/b, rotation radians. Own non-medical mechanical phantom.
ELLIPSES=((.85,0,0,.82,.82,0),(-.85,0,.32,.17,.17,0),
          (-.85,-.28,-.18,.20,.20,0),(-.85,.32,-.22,.12,.12,0),
          (.55,.35,.3,.13,.25,.4))


def phantom(size=SIZE):
    axis=np.linspace(-1,1,size);x,y=np.meshgrid(axis,axis);density=np.zeros_like(x)
    for value,cx,cy,a,b,phi in ELLIPSES:
        dx=x-cx;dy=y-cy;u=dx*np.cos(phi)+dy*np.sin(phi);v=-dx*np.sin(phi)+dy*np.cos(phi)
        density+=value*((u/a)**2+(v/b)**2<=1)
    return density


def analytic_projections(s,angles,ellipses=ELLIPSES):
    output=np.zeros((len(angles),len(s)))
    for i,theta in enumerate(angles):
        for value,cx,cy,a,b,phi in ellipses:
            width=math.hypot(a*math.cos(theta-phi),b*math.sin(theta-phi))
            t=(s-cx*math.cos(theta)-cy*math.sin(theta))/width
            output[i]+=2*value*a*b/width*np.sqrt(np.maximum(0,1-t*t))
    return output


def write_csv(path,s,angles,projections):
    with path.open('w',newline='') as f:
        writer=csv.writer(f,lineterminator='\n')
        writer.writerow(['detector_s']+[f'angle_{math.degrees(a):05.1f}' for a in angles])
        for t,column in zip(s,projections.T):writer.writerow([f'{t:.10f}']+[f'{v:.8f}' for v in column])


def sinogram(data):
    t=np.clip(data.T/np.max(data),0,1)
    cold=np.array([10,25,40]);mid=np.array([30,111,140]);hot=np.array([244,208,153])
    rgb=np.where((t<.5)[:,:,None],cold+(mid-cold)*(2*t[:,:,None]),mid+(hot-mid)*(2*t[:,:,None]-1))
    return Image.fromarray(np.uint8(np.clip(np.round(rgb),0,255)))


def plate(data,result,count):
    image=Image.new('RGB',(1000,560),'#152b38');d=ImageDraw.Draw(image)
    title=ImageFont.load_default(size=20);small=ImageFont.load_default(size=14)
    d.text((28,20),'A PART FROM ITS SHADOWS / COMPUTED TOMOGRAPHY',font=title,fill='#efd5a3')
    d.text((28,54),'SYNTHETIC LINE INTEGRALS / NOT X-RAY EXPOSURE / NO MEDICAL DATA',font=small,fill='#a8c7c7')
    indices=inverse.selected(len(data),count)
    shown=np.zeros_like(data);shown[indices]=data[indices]
    image.paste(sinogram(shown).resize((420,384),Image.Resampling.NEAREST),(28,110))
    image.paste(inverse.display(result).convert('RGB').resize((384,384),Image.Resampling.NEAREST),(550,110))
    d.text((28,86),'SINOGRAM / ANGLE ->, DETECTOR DOWN',font=small,fill='#efd5a3')
    d.text((550,86),f'RECONSTRUCTION / {count} PROJECTIONS',font=small,fill='#efd5a3')
    d.text((28,515),'THE RECONSTRUCTOR READS MEASUREMENTS ONLY, NEVER THE ORIGINAL DRAWING.',font=small,fill='#a8c7c7')
    d.text((28,540),'A RAMP FILTER REMOVES THE BLUR OF PLAIN BACKPROJECTION.',font=small,fill='#a8c7c7')
    return image


def proof(source,full,plain,limited):
    image=Image.new('RGB',(1000,610),'#eee5d0');d=ImageDraw.Draw(image)
    font=ImageFont.load_default(size=16)
    for data,x,y,label,filtered in ((source,28,42,'SOURCE / CHECK ONLY',True),(full,520,42,'120 VIEWS + RAMP',True),
                                  (plain,28,340,'120 VIEWS / NO FILTER',False),(limited,520,340,'60 VIEWS / ONLY 0..90 DEG',True)):
        d.text((x,y-25),label,font=font,fill='#234553')
        image.paste(inverse.display(data,filtered).convert('RGB').resize((240,240),Image.Resampling.NEAREST),(x,y))
    return image


def bench_html(s,angles,data):
    payload=json.dumps({'s':s.tolist(),'angles':angles.tolist(),'data':data.tolist()},separators=(',',':'))
    return '''<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Предмет из теней</title>
<style>body{font:18px system-ui;background:#152b38;color:#d6e3dc;max-width:760px;margin:25px auto;padding:0 18px}canvas{width:100%;height:auto;image-rendering:pixelated;max-width:512px}button,select{font:inherit;padding:8px}:focus-visible{outline:3px solid #efd5a3}output{display:block;margin:16px 0}</style>
<h1>Предмет из одних теней</h1><p>Внутри только таблица синтетических проекций. Исходного рисунка и геометрии детали нет. FFT ramp-фильтр и обратная проекция вычисляются здесь, без сети.</p>
<canvas id="view" width="128" height="128" aria-label="Реконструкция сечения детали с тремя отверстиями из выбранного числа проекций"></canvas>
<p><label for="views">Проекций</label> <select id="views"><option>4</option><option>8</option><option>15</option><option>30</option><option>60</option><option selected>120</option></select></p>
<p><label><input id="filter" type="checkbox" checked> Ramp-фильтр</label> <button id="reset">120 + фильтр</button></p><output id="status" aria-live="polite"></output>
<p>Без фильтра получается размазанная обратная проекция. Масштаб показа явно различается: 1.5 для FBP, 4.5 для обычной BP; это не сравнение абсолютной яркости. Число проекций — разреженная выборка из полного углового диапазона, не ограничение диапазона до первых градусов.</p>
<p>Нет медицинских данных, реального сканирования, рентгеновского излучения, нейросети, автосохранения и автопроигрывания. Это идеальная 2D parallel-beam модель, не диагностический инструмент.</p>
<script>const cfg=PAYLOAD;
function fft(re,im,inverse){const n=re.length;for(let i=1,j=0;i<n;i++){let bit=n>>1;for(;j&bit;bit>>=1)j^=bit;j^=bit;if(i<j){[re[i],re[j]]=[re[j],re[i]];[im[i],im[j]]=[im[j],im[i]]}}for(let len=2;len<=n;len*=2){const angle=(inverse?2:-2)*Math.PI/len,cr=Math.cos(angle),ci=Math.sin(angle);for(let start=0;start<n;start+=len){let wr=1,wi=0;for(let j=0;j<len/2;j++){const a=start+j,b=a+len/2,vr=re[b]*wr-im[b]*wi,vi=re[b]*wi+im[b]*wr;re[b]=re[a]-vr;im[b]=im[a]-vi;re[a]+=vr;im[a]+=vi;const w=wr;wr=w*cr-wi*ci;wi=w*ci+wi*cr}}}if(inverse)for(let i=0;i<n;i++){re[i]/=n;im[i]/=n}}
const spacing=cfg.s[1]-cfg.s[0],width=cfg.s.length;let padded=1;while(padded<2*width)padded*=2;
const filtered=cfg.data.map(row=>{const re=new Float64Array(padded),im=new Float64Array(padded);re.set(row);fft(re,im,false);for(let i=0;i<padded;i++){const ramp=Math.min(i,padded-i)/(padded*spacing);re[i]*=ramp;im[i]*=ramp}fft(re,im,true);return re.slice(0,width)});
function draw(){const count=Number(document.querySelector('#views').value),useFilter=document.querySelector('#filter').checked,rows=useFilter?filtered:cfg.data,n=128,ctx=document.querySelector('#view').getContext('2d'),image=ctx.createImageData(n,n),out=new Float64Array(n*n);for(let k=0;k<count;k++){const index=Math.floor(k*rows.length/count),row=rows[index],angle=cfg.angles[index],co=Math.cos(angle),si=Math.sin(angle);for(let y=0;y<n;y++)for(let x=0;x<n;x++){const t=(2*x/(n-1)-1)*co+(2*y/(n-1)-1)*si,q=(t-cfg.s[0])/spacing,j=Math.floor(q);if(j>=0&&j<width-1)out[y*n+x]+=row[j]*(1-(q-j))+row[j+1]*(q-j)}}const scale=useFilter?1.5:4.5;for(let i=0;i<out.length;i++){const v=Math.floor(255*Math.max(0,Math.min(1,out[i]*Math.PI/count/scale))+.5),p=i*4;image.data[p]=v;image.data[p+1]=v;image.data[p+2]=v;image.data[p+3]=255}ctx.putImageData(image,0,0);document.querySelector('#status').textContent=count+' проекций; '+(useFilter?'FFT ramp + обратная проекция.':'без фильтра, масштаб показа 4.5.')}
document.querySelector('#views').addEventListener('change',draw);document.querySelector('#filter').addEventListener('change',draw);document.querySelector('#reset').onclick=()=>{document.querySelector('#views').value='120';document.querySelector('#filter').checked=true;draw()};draw();</script></html>'''.replace('PAYLOAD',payload)


def generate(output):
    output.mkdir(parents=True,exist_ok=True)
    s=np.linspace(-1.25,1.25,DETECTORS);angles=np.arange(ANGLES)*math.pi/ANGLES
    write_csv(output/'projections.csv',s,angles,analytic_projections(s,angles))
    # From this point, the reconstruction sees only the rounded published CSV.
    s,angles,data=inverse.load(output/'projections.csv')
    full=inverse.reconstruct(s,angles,data);plain=inverse.reconstruct(s,angles,data,filtered=False)
    indices=np.arange(ANGLES//2);filtered=inverse.ramp_filter(data,s[1]-s[0])
    limited=inverse.backproject(s,angles[indices],filtered[indices],span=math.pi/2)
    source=phantom()
    for name,array,filt in [('source.png',source,True),('reconstruction.png',full,True),('plain.png',plain,False),('limited.png',limited,True)]:
        inverse.display(array,filt).save(output/name)
    sinogram(data).save(output/'sinogram.png');plate(data,full,120).save(output/'poster.png');proof(source,full,plain,limited).save(output/'proof.png')
    frames=[plate(data,inverse.reconstruct(s,angles,data,count),count) for count in COUNTS]
    training=Image.new('RGB',(1000,560*3))
    for j,i in enumerate((0,7,len(frames)-1)):training.paste(frames[i],(0,j*560))
    palette=training.quantize(colors=256,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
    indexed=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
    indexed[0].save(output/'recover.gif',save_all=True,append_images=indexed[1:],loop=0,duration=[350]*(len(frames)-1)+[2200],disposal=2,optimize=False)
    small=inverse.reconstruct(s,angles,data,size=128);inverse.display(small).save(output/'bench-reference.png')
    nrmse=lambda a:float(np.linalg.norm(a-source)/np.linalg.norm(source))
    facts={'geometry':'synthetic 2D parallel beam; line integrals, not raw transmitted intensity',
           'angles':ANGLES,'detectors':DETECTORS,'detector_range':[-1.25,1.25],'output_extent':[-1,1],
           'csv_bytes':(output/'projections.csv').stat().st_size,'source':'original mechanical ellipse phantom, not medical data',
           'filtered_nrmse':nrmse(full),'eight_views_nrmse':nrmse(inverse.reconstruct(s,angles,data,8)),
           'limited_90deg_nrmse':nrmse(limited),'animation_views':list(COUNTS),
           'error_definition':'L2(reconstruction-source)/L2(source) over all 192x192 pixels before clipping/display',
           'display_scales':{'filtered':1.5,'plain':4.5},'limits':'no noise, scatter, beam hardening, PSF, real scanner or diagnostic use'}
    (output/'facts.json').write_text(json.dumps(facts,indent=2)+'\n')
    html=bench_html(s,angles,data).encode();(output/'bench.html').write_bytes(html)
    with zipfile.ZipFile(output/'bench.zip','w',compression=zipfile.ZIP_DEFLATED) as archive:
        info=zipfile.ZipInfo('bench.html',(2026,11,18,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
        archive.writestr(info,html)
    print(json.dumps(facts,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=ROOT/'assets/tomograph')
    generate(parser.parse_args().output)
