#!/usr/bin/env python3
"""Two transparent noise sheets reveal an original paper boat by ordinary stacking.

PUBLIC DETERMINISTIC DEMO, NOT A SECRET-SHARING TOOL. No input secrets accepted.
"""
import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path
import zipfile

import numpy as np
from PIL import Image,ImageDraw,ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

ROOT=Path(__file__).resolve().parents[3]
WIDTH,HEIGHT=128,96
SEED='gitEdit / two sheets / public demonstration / 2026-11-18'
PATTERNS=tuple(tuple(int(i in pair) for i in range(4)) for pair in combinations(range(4),2))


def boat():
    image=Image.new('1',(WIDTH,HEIGHT),0);d=ImageDraw.Draw(image)
    d.polygon([(19,59),(111,59),(89,80),(43,80)],fill=1)
    d.polygon([(60,14),(60,55),(22,55)],fill=1)
    d.polygon([(65,23),(105,55),(65,55)],fill=1)
    d.line([(37,86),(92,86)],fill=1,width=2)
    return np.array(image,dtype=bool)


def choice(x,y,seed):
    """Public deterministic texture; rejection avoids a modulo-6 bucket imbalance."""
    counter=0
    while True:
        digest=hashlib.sha256(f'{seed}:{x}:{y}:{counter}'.encode()).digest()
        for value in digest:
            if value<252:return value%6
        counter+=1


def split(secret,seed=SEED):
    h,w=secret.shape;a=np.zeros((h*2,w*2),dtype=bool);b=a.copy()
    for y in range(h):
        for x in range(w):
            pattern=np.array(PATTERNS[choice(x,y,seed)],dtype=bool).reshape(2,2)
            a[2*y:2*y+2,2*x:2*x+2]=pattern
            b[2*y:2*y+2,2*x:2*x+2]=~pattern if secret[y,x] else pattern
    return a,b


def rgba(bits):
    pixels=np.zeros((*bits.shape,4),dtype=np.uint8)
    pixels[:,:,3]=bits.astype(np.uint8)*255
    return Image.fromarray(pixels)


def block_counts(bits):
    h,w=bits.shape
    if h%2 or w%2:raise ValueError('even-sized aligned raster required')
    return bits.reshape(h//2,2,w//2,2).sum(axis=(1,3))


def recover_file(source,destination):
    """Read only the flattened aligned stack PNG, not shares, seed or target."""
    with Image.open(source) as image:
        if image.mode!='RGB':raise ValueError('opaque RGB stack required')
        data=np.array(image)
    if not np.all((data==0)|(data==255)) or not np.all(data==data[:,:,:1]):
        raise ValueError('lossless black/white stack required; no interpolation or JPEG')
    counts=block_counts(data[:,:,0]==0)
    if not np.all(np.isin(counts,[2,4])):raise ValueError('not an aligned two-sheet stack')
    recovered=counts==4
    Image.fromarray(np.uint8(~recovered)*255).save(destination)
    return recovered


def overlay(a,b,dx=0,dy=0):
    surface=Image.new('RGBA',a.size,'white')
    surface.alpha_composite(a)
    surface.alpha_composite(b,dest=(dx,dy))
    return surface.convert('RGB')


def poster(a,b):
    paper='#f4ecda';image=Image.new('RGB',(1000,750),paper);d=ImageDraw.Draw(image)
    font=ImageFont.load_default(size=18);small=ImageFont.load_default(size=14)
    d.text((32,22),'TWO SHEETS / ONE PAPER BOAT',font=font,fill='#234653')
    for source,x,label in ((a,32,'SHEET A'),(b,520,'SHEET B')):
        white=Image.new('RGBA',source.size,'white');white.alpha_composite(source)
        image.paste(white.convert('RGB').resize((448,336),Image.Resampling.NEAREST),(x,78))
        d.text((x,53),label+' / 50% BLACK IN EVERY 2x2 BLOCK',font=small,fill='#234653')
    stacked=overlay(a,b)
    image.paste(stacked.resize((384,288),Image.Resampling.NEAREST),(32,448))
    d.text((448,470),'ALIGNED = ORDINARY BLACK-INK OVERLAY',font=small,fill='#234653')
    d.text((448,510),'BACKGROUND: 2 BLACK SUBPIXELS OF 4',font=small,fill='#234653')
    d.text((448,543),'BOAT:       4 BLACK SUBPIXELS OF 4',font=small,fill='#234653')
    d.text((448,588),'NO XOR. NO ORIGINAL DRAWING ON TOP.',font=small,fill='#234653')
    d.text((448,639),'PUBLIC SEED + BOTH SHEETS = NO SECRECY.',font=small,fill='#a15e3b')
    return image


def pdf_sheets(path,a,b):
    c=canvas.Canvas(str(path),pagesize=(210*mm,297*mm),invariant=1)
    c.setTitle('Two sheets - public paper boat demo')
    x0,y0=41*mm,115*mm;sub=.5*mm
    for label,bits in [('A',a),('B',b)]:
        c.setFont('Helvetica-Bold',16);c.drawString(20*mm,277*mm,f'TWO SHEETS / SHEET {label}')
        c.setFont('Helvetica',10)
        for i,text in enumerate(['Public reproducible demo, NOT for confidential information.',
                                  'Print at 100%, no fit-to-page; check the 50 mm scale.',
                                  'Use only clear film suitable for your printer; do not mirror.',
                                  'Align both sheets on white backing using the four crosses.',
                                  'Pattern area: 128 x 96 mm. Black subpixel: 0.5 x 0.5 mm.']):
            c.drawString(20*mm,(265-i*6)*mm,text)
        c.setFillColorRGB(0,0,0)
        for y,x in zip(*np.where(bits)):
            c.rect(x0+x*sub,y0+(bits.shape[0]-1-y)*sub,sub,sub,stroke=0,fill=1)
        c.setLineWidth(.3)
        for xx,yy in ((38,112),(172,112),(38,214),(172,214)):
            c.line((xx-2)*mm,yy*mm,(xx+2)*mm,yy*mm);c.line(xx*mm,(yy-2)*mm,xx*mm,(yy+2)*mm)
        c.setFont('Helvetica',9);c.drawString(20*mm,70*mm,'Physical printing/alignment has not been tested for this exhibit.')
        c.setLineWidth(.8);c.line(20*mm,42*mm,70*mm,42*mm)
        for xx in (20,70):c.line(xx*mm,40*mm,xx*mm,44*mm)
        c.drawString(20*mm,34*mm,'50 mm - measure before using the sheets')
        c.showPage()
    c.save()


def bench():
    return '''<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Два листа — один кораблик</title>
<style>body{font:18px system-ui;background:#f4ecda;color:#234653;max-width:800px;margin:25px auto;padding:0 18px}canvas{width:100%;height:auto;image-rendering:pixelated}button,select,input{font:inherit}button,select{padding:8px}input{width:100%}:focus-visible{outline:3px solid #ab704b}output{display:block;padding:12px 0}</style>
<h1>Два листа — один кораблик</h1><p>Рисунок появляется при совмещении прозрачных листов. Обычное наложение чёрных пикселей, без XOR и без подрисовки оригинала.</p>
<canvas id="view" width="288" height="224" aria-label="Совмещаемые шумовые листы: при точном совпадении появляется бумажный кораблик"></canvas>
<p><label for="mode">Слои</label> <select id="mode"><option value="stack">A + B</option><option value="a">Только A</option><option value="b">Только B</option></select> <button id="align">Совместить точно</button></p>
<label for="shift">Горизонтальный сдвиг B, в субпикселях</label><input id="shift" type="range" min="-12" max="12" step="1" value="9"><output id="status" aria-live="polite"></output>
<p>Это публичная воспроизводимая демонстрация, не инструмент хранения секретов: оба листа и seed опубликованы. Прогресс не сохраняется, сети нет. Здесь моделируется только целочисленный горизонтальный сдвиг, не деформация печатной плёнки.</p>
<script>const a=new Image(),b=new Image();let loaded=0;const c=document.querySelector('#view'),ctx=c.getContext('2d'),mode=document.querySelector('#mode'),shift=document.querySelector('#shift');const ready=()=>{loaded++;if(loaded===2)draw()};a.onload=ready;b.onload=ready;a.src='sheet-a.png';b.src='sheet-b.png';
function draw(){if(loaded!==2)return;ctx.fillStyle='#ffffff';ctx.fillRect(0,0,c.width,c.height);ctx.imageSmoothingEnabled=false;const m=mode.value,dx=Number(shift.value);if(m!=='b')ctx.drawImage(a,16,16);if(m!=='a')ctx.drawImage(b,16+(m==='stack'?dx:0),16);shift.disabled=m!=='stack';document.querySelector('#status').textContent=m==='stack'?'A + B: сдвиг '+dx+' px'+(dx===0?' — точное совмещение.':' — попробуй 0.'):'Один лист: в каждом блоке 2×2 ровно два чёрных субпикселя.'}
mode.addEventListener('change',draw);shift.addEventListener('input',draw);document.querySelector('#align').onclick=()=>{mode.value='stack';shift.value=0;draw()};</script></html>'''


def generate(output):
    output.mkdir(parents=True,exist_ok=True)
    secret=boat();abits,bbits=split(secret);a=rgba(abits);b=rgba(bbits)
    a.save(output/'sheet-a.png');b.save(output/'sheet-b.png')
    # Reload emitted RGBA shares and composite them like any image viewer would.
    with Image.open(output/'sheet-a.png') as aa,Image.open(output/'sheet-b.png') as bb:
        stack=overlay(aa,bb);stack.save(output/'stack.png')
        proof=poster(aa,bb);proof.save(output/'proof.png')
        proof.crop((0,0,1000,430)).save(output/'separated.png')
    Image.fromarray(np.uint8(~secret)*255).save(output/'source.png')
    recovered=recover_file(output/'stack.png',output/'recovered.png')
    if not np.array_equal(secret,recovered):raise RuntimeError('PNG-only recovery mismatch')
    pdf_sheets(output/'sheets-a4.pdf',abits,bbits)
    facts={'scheme':'2-out-of-2, 2x2 pixel expansion, ordinary black-ink OR overlay',
           'source_size':[WIDTH,HEIGHT],'sheet_size':[WIDTH*2,HEIGHT*2],
           'public_seed':SEED,'security':'PUBLIC DETERMINISTIC DEMO. No confidentiality. Do not submit secrets.',
           'patterns':[list(p) for p in PATTERNS],'a_black_subpixels':int(abits.sum()),'b_black_subpixels':int(bbits.sum()),
           'secret_black_pixels':int(secret.sum()),'recovered_errors':int(np.count_nonzero(secret!=recovered)),
           'background_black_subpixels_per_block':2,'foreground_black_subpixels_per_block':4,
           'printed_pattern_mm':[128,96],'printed_subpixel_mm':.5,
           'sha256':{name:hashlib.sha256((output/name).read_bytes()).hexdigest() for name in ['sheet-a.png','sheet-b.png','stack.png','recovered.png']}}
    (output/'facts.json').write_text(json.dumps(facts,indent=2)+'\n')
    html=bench().encode();(output/'bench.html').write_bytes(html)
    with zipfile.ZipFile(output/'bench.zip','w',compression=zipfile.ZIP_DEFLATED) as archive:
        for name,content in sorted({'bench.html':html,'sheet-a.png':(output/'sheet-a.png').read_bytes(),'sheet-b.png':(output/'sheet-b.png').read_bytes()}.items()):
            info=zipfile.ZipInfo(name,(2026,11,18,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
            archive.writestr(info,content)
    print(f'{WIDTH*HEIGHT} source pixels; {abits.sum()} black subpixels per sheet; recovered errors: {facts["recovered_errors"]}')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--decode',type=Path,help='Read only an aligned flattened RGB stack PNG; --output must be a destination PNG')
    args=parser.parse_args()
    if args.decode:
        if args.output is None:parser.error('--decode requires --output FILE.png')
        recover_file(args.decode,args.output)
    else:generate(args.output or ROOT/'assets/veil')
