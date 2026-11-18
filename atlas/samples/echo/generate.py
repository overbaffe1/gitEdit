#!/usr/bin/env python3
"""Original lossless lattice wave experiment. Return frames are freshly integrated, not reversed."""
import argparse
import csv
import json
from pathlib import Path
import zipfile
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from wave_local import step,energy,modified_energy

ROOT=Path(__file__).resolve().parents[3]
N=112
DT=.45
STEPS=240
STRIDE=8


def initial(n=N):
    y,x=np.mgrid[:n,:n]/(n-1)
    fixed=(x==0)|(x==1)|(y==0)|(y==1)
    fixed|=((x-.52)**2+(y-.43)**2<.085**2)
    fixed|=((x-.72)**2+(y-.70)**2<.12**2)
    fixed|=(abs(x-.32)<.025)&(y>.64)&(y<.86)
    u=np.exp(-((x-.24)**2+(y-.34)**2)/(2*.033**2));u[fixed]=0
    return u,np.zeros_like(u),fixed


def field(u,fixed):
    # Fixed, signed nonlinear display map. No per-frame normalization.
    t=np.tanh(5*u)[:,:,None];neutral=np.array([21,40,55]);positive=np.array([255,207,134]);negative=np.array([43,194,207])
    rgb=neutral+np.maximum(t,0)*(positive-neutral)+np.maximum(-t,0)*(negative-neutral)
    rgb[fixed]=[114,132,136]
    return Image.fromarray(np.uint8(np.floor(np.clip(rgb,0,255)+.5)))


def plate(u,fixed,stage,k,control=None):
    image=Image.new('RGB',(1000,610),'#152837');d=ImageDraw.Draw(image)
    large=ImageFont.load_default(size=23);small=ImageFont.load_default(size=15)
    d.text((28,18),'ECHO / A WAVE THAT FINDS ITS WAY BACK',font=large,fill='#efcf96')
    d.text((28,52),'LOSSLESS LATTICE / FIXED WALLS / NEWLY COMPUTED FRAMES, NOT REVERSED GIF',font=small,fill='#b2cdd0')
    image.paste(field(u,fixed).resize((448,448),Image.Resampling.NEAREST),(28,105))
    if control is not None:image.paste(field(control,fixed).resize((448,448),Image.Resampling.NEAREST),(524,105))
    else:
        d.text((540,190),'A pulse scatters off obstacles.',font=small,fill='#b2cdd0')
        d.text((540,226),'At step 240, KEEP displacement u.',font=small,fill='#b2cdd0')
        d.text((540,262),'Change EVERY velocity v to -v.',font=small,fill='#efcf96')
        d.text((540,298),'Then integrate FORWARD again.',font=small,fill='#b2cdd0')
    d.text((28,82),f'{stage} / STEP {k}',font=small,fill='#efcf96')
    if control is not None:d.text((524,82),'CONTROL / KEEP v, DO NOT REVERSE',font=small,fill='#efcf96')
    d.text((28,572),'SIGNED DISPLACEMENT: CYAN < 0 / DARK = 0 / AMBER > 0. SAME SCALE IN EVERY FRAME.',font=small,fill='#b2cdd0')
    return image


def html():
    return '''<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Волна задом наперёд</title>
<style>body{font:18px system-ui;background:#152837;color:#b2cdd0;max-width:760px;margin:24px auto;padding:0 18px}h1{color:#efcf96}canvas{width:100%;max-width:448px;image-rendering:pixelated}button,select{font:inherit;padding:8px;margin:4px}:focus-visible{outline:3px solid #efcf96}output{display:block;margin:12px 0}</style>
<h1>Волна задом наперёд</h1><p>Не проигрыватель кадров: здесь заново решается uₜₜ = Δu. На шаге 240 сохраняем форму волны и выбираем, что сделать со скоростями во всех узлах. После этого считаем ещё 240 шагов вперёд.</p>
<canvas id="view" width="112" height="112" aria-label="Поле знакового смещения волны между закреплёнными препятствиями"></canvas>
<p><label for="mode">На развороте:</label><select id="mode"><option value="reverse">v → −v</option><option value="zero">v → 0 (потерять скорости)</option><option value="keep">Оставить v</option></select></p>
<p><button id="step">+12 шагов</button><button id="end">До конца фазы</button><button id="reset">Сначала</button></p><output id="status" aria-live="polite"></output>
<p>Бирюзовый — отрицательное смещение, янтарный — положительное. Цветовая шкала одна на весь опыт. Серые узлы закреплены (u = v = 0), это отражающие края мембраны, не поглощающий слой и не акустические жёсткие стенки.</p>
<p>Сброс скоростей не уничтожает всю фокусировку: в обратимой линейной модели остаётся смесь прямой и обратной волн. Время не обращается физически: идеализированное полное управление всем полем, без шума и потерь. Не boundary-only time-reversal mirror и не звук. Сети, файлов кадров и автопроигрывания нет.</p>
<script>
const n=112,dt=.45,turn=240,total=n*n;let u,v,fixed,target,t,mode;
function init(){u=new Float64Array(total);v=new Float64Array(total);fixed=new Uint8Array(total);for(let y=0;y<n;y++)for(let x=0;x<n;x++){const X=x/(n-1),Y=y/(n-1),i=y*n+x;fixed[i]=(x===0||y===0||x===n-1||y===n-1||((X-.52)**2+(Y-.43)**2<.085**2)||((X-.72)**2+(Y-.70)**2<.12**2)||(Math.abs(X-.32)<.025&&Y>.64&&Y<.86))?1:0;u[i]=fixed[i]?0:Math.exp(-((X-.24)**2+(Y-.34)**2)/(2*.033**2))}target=u.slice();t=0;mode=null;document.querySelector('#mode').disabled=false;draw()}
function lap(a){const b=new Float64Array(total);for(let y=1;y<n-1;y++)for(let x=1;x<n-1;x++){const i=y*n+x;if(!fixed[i])b[i]=a[i-n]+a[i+n]+a[i-1]+a[i+1]-4*a[i]}return b}
function advance(count){for(let k=0;k<count&&t<2*turn;k++){if(t===turn){mode=document.querySelector('#mode').value;for(let i=0;i<total;i++)if(mode==='reverse')v[i]=-v[i];else if(mode==='zero')v[i]=0;document.querySelector('#mode').disabled=true}let force=lap(u);for(let i=0;i<total;i++){v[i]+=.5*dt*force[i];u[i]+=dt*v[i]}force=lap(u);for(let i=0;i<total;i++)v[i]+=.5*dt*force[i];t++}draw()}
function error(){let numerator=0,denominator=0;for(let i=0;i<total;i++){numerator+=(u[i]-target[i])**2;denominator+=target[i]**2}return Math.sqrt(numerator/denominator)}
function draw(){const ctx=document.querySelector('#view').getContext('2d'),image=ctx.createImageData(n,n),neutral=[21,40,55],pos=[255,207,134],neg=[43,194,207];for(let i=0;i<total;i++){const a=Math.tanh(5*u[i]);for(let c=0;c<3;c++)image.data[i*4+c]=fixed[i]?[114,132,136][c]:Math.floor(neutral[c]+Math.max(a,0)*(pos[c]-neutral[c])+Math.max(-a,0)*(neg[c]-neutral[c])+.5);image.data[i*4+3]=255}ctx.putImageData(image,0,0);document.querySelector('#status').textContent='Шаг '+t+'/480. '+(t<=turn?'Распространение; на границе фаз выберите режим.':'После операции '+mode+'.')+' Относительная L2-ошибка смещения: '+error().toExponential(5);document.querySelector('#step').disabled=t===2*turn;document.querySelector('#end').disabled=t===2*turn}
document.querySelector('#step').onclick=()=>advance(12);document.querySelector('#end').onclick=()=>advance(t<turn?turn-t:2*turn-t);document.querySelector('#reset').onclick=init;init();
</script></html>'''


def generate(output):
    output.mkdir(parents=True,exist_ok=True)
    u,v,fixed=initial();source=u.copy();frames=[plate(u,fixed,'OUTWARD',0)];trace=[]
    e0=energy(u,v,fixed);m0=modified_energy(u,v,fixed)
    def record(phase,k,u,v):
        trace.append([phase,k,energy(u,v,fixed),modified_energy(u,v,fixed),float(np.linalg.norm(u-source)/np.linalg.norm(source))])
    record('out',0,u,v)
    for k in range(1,STEPS+1):
        u,v=step(u,v,fixed);record('out',k,u,v)
        if k%STRIDE==0:frames.append(plate(u,fixed,'OUTWARD',k))
    checkpoint_u=u.copy();checkpoint_v=v.copy()
    field(source,fixed).save(output/'source.png');field(u,fixed).save(output/'turn.png')
    # Construct the three .npy entries with fixed ZIP metadata for reproducibility.
    import io
    with zipfile.ZipFile(output/'checkpoint.npz','w',compression=zipfile.ZIP_DEFLATED) as archive:
        for name,arr in [('u',u),('v',v),('fixed',fixed)]:
            stream=io.BytesIO();np.save(stream,arr,allow_pickle=False);info=zipfile.ZipInfo(name+'.npy',(2026,11,18,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;archive.writestr(info,stream.getvalue())
    branches={}
    for mode in ('reverse','zero','keep'):
        bu=checkpoint_u.copy();bv=checkpoint_v.copy()
        if mode=='reverse':bv=-bv
        if mode=='zero':bv[:]=0
        control_u=checkpoint_u.copy();control_v=checkpoint_v.copy()
        for k in range(1,STEPS+1):
            bu,bv=step(bu,bv,fixed)
            if mode=='reverse':
                control_u,control_v=step(control_u,control_v,fixed);record('return',k,bu,bv)
                if k%STRIDE==0:frames.append(plate(bu,fixed,'AFTER v -> -v',k,control_u))
        branches[mode]={'u':bu,'v':bv,'relative_displacement_error':float(np.linalg.norm(bu-source)/np.linalg.norm(source)),'relative_velocity_residual':float(np.linalg.norm(bv)/np.linalg.norm(source))}
        field(bu,fixed).save(output/(mode+'.png'))
    frames[-1].save(output/'poster.png')
    # A fixed palette trained on actual computed frames.
    sample=Image.new('RGB',(1000,610*3))
    for j,i in enumerate((0,len(frames)//2,len(frames)-1)):sample.paste(frames[i],(0,610*j))
    palette=sample.quantize(colors=192,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
    indexed=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
    indexed[0].save(output/'return.gif',save_all=True,append_images=indexed[1:],loop=0,duration=[90]*(len(frames)-1)+[2000],disposal=2,optimize=False)
    image=Image.new('RGB',(1000,620),'#152837');d=ImageDraw.Draw(image);font=ImageFont.load_default(size=17)
    for title,arr,x,y in [('INITIAL',source,20,40),('SCATTERED / STEP 240',checkpoint_u,520,40),('AFTER v -> -v / 240 MORE',branches['reverse']['u'],20,350),('AFTER v -> 0 / 240 MORE',branches['zero']['u'],520,350)]:
        d.text((x,y-25),title,fill='#efcf96',font=font);image.paste(field(arr,fixed).resize((240,240),Image.Resampling.NEAREST),(x,y))
    image.save(output/'proof.png')
    with (output/'trace.csv').open('w',newline='') as f:
        writer=csv.writer(f,lineterminator='\n');writer.writerow(['phase','step','energy','modified_energy','relative_displacement_error']);writer.writerows(trace)
    facts={'grid':N,'dt':DT,'speed_cells_per_time':1,'steps_each_way':STEPS,'CFL_2D_limit':float(1/np.sqrt(2)),
           'boundary':'fixed nodes, u=v=0 (Dirichlet); not acoustic rigid-wall Neumann',
           'return_uses':'only checkpoint u,v,fixed; same forward stepper, no trajectory replay',
           'branches':{mode:{k:v for k,v in branch.items() if k not in ('u','v')} for mode,branch in branches.items()},
           'initial_energy':e0,'max_relative_energy_drift':max(abs(row[2]-e0)/e0 for row in trace),
           'max_relative_modified_energy_drift':max(abs(row[3]-m0)/m0 for row in trace),
           'frames':len(frames),'display':'same signed tanh(5u) map in every image; no frame normalization',
           'limits':'ideal full-state reversal, no damping or noise; not boundary-only time reversal, water or sound simulation'}
    (output/'facts.json').write_text(json.dumps(facts,indent=2)+'\n')
    live=html().encode();(output/'bench.html').write_bytes(live)
    with zipfile.ZipFile(output/'bench.zip','w',compression=zipfile.ZIP_DEFLATED) as archive:
        info=zipfile.ZipInfo('bench.html',(2026,11,18,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;archive.writestr(info,live)
    print(json.dumps(facts,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=ROOT/'assets/echo');generate(p.parse_args().output)
