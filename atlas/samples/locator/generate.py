#!/usr/bin/env python3
"""Own maximal-sequence toroidal pattern and digitally simulated localization experiment."""
import argparse
import csv
import json
from pathlib import Path
import zipfile
from PIL import Image,ImageDraw,ImageFont
import audit
import codebook as c

ROOT=Path(__file__).resolve().parents[3]
SAMPLE=Path(__file__).resolve().parent


def pattern():
    state=1;seen=set();sequence=[]
    while state not in seen:
        seen.add(state);sequence.append(state&1)
        feedback=((state>>0)^(state>>1)^(state>>4)^(state>>6))&1
        state=(state>>1)|(feedback<<11)
    if len(sequence)!=4095 or state!=1:raise RuntimeError('LFSR period mismatch')
    # CRT: i mod 63 = x, i mod 65 = y.
    return [[sequence[(2080*x+2016*y)%4095] for x in range(63)] for y in range(65)]


def plate(grid,entries,x,y,observed,label):
    image=Image.new('RGB',(1000,690),'#152934');d=ImageDraw.Draw(image);large=ImageFont.load_default(size=23);small=ImageFont.load_default(size=16)
    d.text((24,18),'COORDINATES WITHOUT NUMBERS',font=large,fill='#efd09a')
    d.text((24,53),'4095 POSITIONS / 4x4 UNIQUE / 6x6 CORRECTS UP TO THREE BIT FLIPS',font=small,fill='#bdd1ce')
    d.text((24,95),'THE PATTERN / 63 x 65 / TOROIDAL',font=small,fill='#efd09a')
    for yy,row in enumerate(grid):
        for xx,bit in enumerate(row):d.rectangle((24+6*xx,130+6*yy,29+6*xx,135+6*yy),fill='#ffffff' if bit else '#000000')
    for dy in range(6):
        for dx in range(6):
            xx=(x+dx)%63;yy=(y+dy)%65;d.rectangle((24+6*xx,130+6*yy,29+6*xx,135+6*yy),outline='#e6a14a')
    original=c.signature(grid,x,y);difference=observed^original;result=c.locate(entries,observed)
    d.text((474,95),'OBSERVED 6 x 6 / '+label,font=small,fill='#efd09a')
    for i in range(36):
        bit=(observed>>(35-i))&1;xx=474+(i%6)*40;yy=140+(i//6)*40
        d.rectangle((xx,yy,xx+38,yy+38),fill='#ffffff' if bit else '#000000',outline='#ed785d' if difference>>(35-i)&1 else '#527787',width=3 if difference>>(35-i)&1 else 1)
    if result['accepted']:
        p=result['position'];d.text((474,415),f'DECODER: X={p["x"]}, Y={p["y"]}; DISTANCE={p["distance"]}',font=small,fill='#efd09a')
        correct=(p['x'],p['y'])==(x,y)
        d.text((474,452),'CORRECT' if correct else 'WRONG ANSWER / OUTSIDE GUARANTEE',font=small,fill='#bdd1ce' if correct else '#ed785d')
    else:d.text((474,415),'DECODER REFUSES / NO CANDIDATE <= 3',font=small,fill='#ed785d')
    d.text((474,493),f'SIMULATOR TRUTH: X={x}, Y={y}',font=small,fill='#bdd1ce')
    d.text((474,526),f'ACTUAL FLIPPED BITS: {difference.bit_count()}',font=small,fill='#bdd1ce')
    d.text((24,575),'DECODER INPUT: ONLY THE OBSERVED BITS + PUBLISHED MAP. NO TRUE X/Y.',font=small,fill='#bdd1ce')
    d.text((24,614),'RED CELL OUTLINE: A BIT FLIPPED BY THE SIMULATOR. ORIENTATION IS GIVEN.',font=small,fill='#bdd1ce')
    d.text((24,653),'DIGITAL MODEL ONLY / NO CAMERA, PRINT TEST, PERSPECTIVE OR ROTATION DETECTOR.',font=small,fill='#bdd1ce')
    return image


def generate(output):
    output.mkdir(parents=True,exist_ok=True)
    with (output/'pattern.csv').open('w',newline='') as f:csv.writer(f,lineterminator='\n').writerows(pattern())
    grid=c.load(output/'pattern.csv');entries=c.book(grid);report=audit.audit(grid)
    (output/'certificate.json').write_text(json.dumps(report,indent=2)+'\n')
    raw=Image.new('1',(63,65));raw.putdata([bit for row in grid for bit in row]);raw.resize((504,520),Image.Resampling.NEAREST).save(output/'pattern.png')
    with (output/'windows.csv').open('w',newline='') as f:
        writer=csv.writer(f,lineterminator='\n');writer.writerow(['x','y','window4_hex','window6_hex'])
        for x,y,code in entries:writer.writerow([x,y,f'{c.signature(grid,x,y,4):04x}',f'{code:09x}'])
    x,y=9,12;original=c.signature(grid,x,y);three=original^(1<<35)^(1<<19)^(1<<2);four,partner,flips=c.four_error_example(entries,x,y)
    cases={'clean':original,'three-flips':three,'four-flips-wrong':four,'zero-rejected':0}
    results={}
    for name,observed in cases.items():
        (output/(name+'.txt')).write_text(c.patch_text(observed));results[name]={'truth':{'x':x,'y':y},'observed_hex':f'{observed:09x}','actual_flips':(original^observed).bit_count(),'decoded':c.locate(entries,observed)}
    (output/'examples.json').write_text(json.dumps(results,indent=2)+'\n')
    plate(grid,entries,x,y,three,'THREE FLIPS').save(output/'poster.png')
    plate(grid,entries,x,y,four,'FOUR FLIPS').save(output/'outside-guarantee.png')
    stages=[]
    for i in range(16):
        xx=(i*3+9)%63;yy=(i*2+12)%65;stages.append((xx,yy,c.signature(grid,xx,yy),'CLEAN'))
    stages.extend([(x,y,original,'CLEAN'),(x,y,three,'THREE FLIPS'),(x,y,four,'FOUR FLIPS'),(x,y,0,'ZERO WINDOW'),(61,63,c.signature(grid,61,63),'TORUS WRAP')])
    frames=[plate(grid,entries,*stage) for stage in stages];sheet=Image.new('RGB',(1000,1380));sheet.paste(frames[0],(0,0));sheet.paste(frames[18],(0,690));palette=sheet.quantize(colors=128,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
    indexed=[frame.quantize(palette=palette,dither=Image.Dither.NONE) for frame in frames];durations=[160]*len(frames)
    for i in range(16,len(frames)):durations[i]=1800
    indexed[0].save(output/'locate.gif',save_all=True,append_images=indexed[1:],loop=0,duration=durations,disposal=2,optimize=False)
    live=(SAMPLE/'bench-template.html').read_text().replace('__GRID__',json.dumps(grid,separators=(',',':'))).encode();(output/'bench.html').write_bytes(live)
    with zipfile.ZipFile(output/'bench.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
        info=zipfile.ZipInfo('bench.html',(2026,11,18,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,live)
    facts={'construction':'12-bit maximal sequence, recurrence taps [0,1,4,6], initial state 1, period 4095; CRT index=(2080*x+2016*y) mod 4095',
           'width':63,'height':65,'window4_unique':report['window4_unique'],'window6_unique':report['window6_unique'],'minimum_pair_distance_6x6':report['certified_pair_distance'],
           'guaranteed_correctable_flips':report['guaranteed_correctable_flips'],'example_four_error_partner':partner,'example_four_error_bit_positions_lsb_first':flips,'frames':len(frames),
           'limits':'known scale, grid alignment and orientation; binary flips only; toroidal synthetic crop; no camera, physical print/read, homography or rotation handling'}
    (output/'facts.json').write_text(json.dumps(facts,indent=2)+'\n');print(json.dumps(facts,indent=2));print(json.dumps(report,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=ROOT/'assets/locator');generate(p.parse_args().output)
