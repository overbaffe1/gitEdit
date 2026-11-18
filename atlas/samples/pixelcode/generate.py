#!/usr/bin/env python3
"""Emit a real Piet source image; derive all previews from execution of that PNG."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import runner

ROOT=Path(__file__).resolve().parents[3]
# Area of the source block matters only for push. Other areas stay one codel.
PLAN=[('push',7),('push',10),('multiply',1),('push',1),('add',1),('outchar',1),
      ('push',8),('push',9),('multiply',1),('push',1),('add',1),('outchar',1),
      ('push',7),('push',12),('multiply',1),('outchar',1),('push',1),('pointer',1),
      ('pop',1),('pop',1)]


def build():
    image=Image.new('RGB',(22,14),'black');h=0;l=0
    for i,(command,area) in enumerate(PLAN):
        if i<19:x,y=i,0
        else:x,y=18,1
        for offset in range(area):image.putpixel((x,y+offset),tuple(bytes.fromhex(runner.COLORS[l][h][1:])))
        dh,dl=runner.DELTAS[command];h=(h+dh)%6;l=(l+dl)%3
    # The entrance touches the middle of the top edge, never a DP/CC exit corner.
    color=tuple(bytes.fromhex(runner.COLORS[l][h][1:]))
    for y in range(2,7):
        for x in range(16,21):image.putpixel((x,y),color)
    return image


def frame(program,event,index,total):
    plate=Image.new('RGB',(1000,620),'#152d38');draw=ImageDraw.Draw(plate)
    font=ImageFont.load_default(size=17);small=ImageFont.load_default(size=13);large=ImageFont.load_default(size=38)
    draw.text((32,24),'PIXELCODE / THIS PNG IS A PROGRAM',font=font,fill='#f1d7a6')
    draw.text((32,53),'PIET / 18 CODE COLORS + BLACK / EACH SOURCE PIXEL IS ONE CODEL',font=small,fill='#abc7c3')
    scale=25;ox=32;oy=106
    plate.paste(program.resize((22*scale,14*scale),Image.Resampling.NEAREST),(ox,oy))
    # The outline is annotation on the preview only, never in the executable PNG.
    for x,y in event['block']:
        draw.rectangle((ox+x*scale,oy+y*scale,ox+(x+1)*scale-1,oy+(y+1)*scale-1),outline='#ffffff',width=2)
    draw.text((630,108),f'STEP {index:02} / {total:02}',font=font,fill='#abc7c3')
    draw.text((630,148),event['operation'].upper(),font=large,fill='#f1d7a6')
    draw.text((630,210),f'SOURCE AREA: {event["area"]}',font=font,fill='#abc7c3')
    draw.text((630,242),'STACK AFTER:',font=font,fill='#abc7c3')
    draw.text((630,270),str(event['stack_after']),font=large,fill='#f5eee0')
    draw.text((630,330),'STDOUT:',font=font,fill='#abc7c3')
    draw.text((630,365),event['output'] or '(empty)',font=large,fill='#f1d7a6')
    draw.text((32,493),'7 x 10 + 1 = 71       8 x 9 + 1 = 73       7 x 12 = 84',font=font,fill='#f1d7a6')
    draw.text((32,529),'BLACK = WALL. BLOCK AREA = PUSH VALUE. COLOR CHANGE = INSTRUCTION.',font=small,fill='#abc7c3')
    draw.text((32,558),'PREVIEW ONLY: annotations are not executable code. Run program.png instead.',font=small,fill='#abc7c3')
    draw.text((32,587),'The final square halts naturally after eight blocked DP/CC exits.',font=small,fill='#abc7c3')
    return plate


def generate(output):
    output.mkdir(parents=True,exist_ok=True)
    program=build();program.save(output/'program.png')
    # Execution reads the file back; the runner never receives PLAN.
    result=runner.run(runner.load(output/'program.png'))
    if not result['halted'] or result['output']!='GIT':raise RuntimeError('program did not produce GIT and halt')
    trace=result['trace']
    (output/'trace.json').write_text(json.dumps(result,indent=2)+'\n')
    with (output/'trace.csv').open('w',newline='') as f:
        writer=csv.writer(f,lineterminator='\n');writer.writerow(['step','operation','source_area','stack_before','stack_after','stdout','blocked_attempts'])
        for row in trace:
            writer.writerow([row['step'],row['operation'],row['area'],str(row['stack_before']),str(row['stack_after']),row['output'],sum(a['blocked'] for a in row['attempts'])])
    facts={'format':'Piet source, 1 pixel = 1 codel','width':program.width,'height':program.height,
           'output':result['output'],'transitions':len(trace)-1,'halt_block_area':trace[-1]['area'],
           'halt_blocked_exits':len(trace[-1]['attempts']),'stack_at_halt':result['stack'],
           'sha256':hashlib.sha256((output/'program.png').read_bytes()).hexdigest(),
           'runner_scope':'Only six commands used by this program; colored blocks and black. No white, input, or general Piet conformance claim.'}
    (output/'facts.json').write_text(json.dumps(facts,indent=2)+'\n')
    program.resize((528,336),Image.Resampling.NEAREST).save(output/'program-24x.png')
    frames=[frame(program,row,i,len(trace)-1) for i,row in enumerate(trace)]
    frames[-1].save(output/'poster.png')
    # A shared explicit 256-color palette (20 program colors + panel colors + cube).
    palette=Image.new('P',(1,1));colors=[tuple(bytes.fromhex(v[1:])) for row in runner.COLORS for v in row]
    colors += [(0,0,0),(255,255,255),(21,45,56),(241,215,166),(171,199,195),(245,238,224)]
    for r in range(6):
        for g in range(6):
            for b in range(6):colors.append((r*51,g*51,b*51))
    colors=(colors+[(0,0,0)]*256)[:256];palette.putpalette([v for color in colors for v in color])
    indexed=[p.quantize(palette=palette,dither=Image.Dither.NONE) for p in frames]
    indexed[0].save(output/'execution.gif',save_all=True,append_images=indexed[1:],loop=0,
                    duration=[500]*(len(frames)-1)+[2200],disposal=2,optimize=False)
    print(f'{program.width}x{program.height}, {len(trace)-1} transitions, stdout={result["output"]!r}, blocked exits={len(trace[-1]["attempts"])}')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=ROOT/'assets/pixelcode')
    generate(p.parse_args().output)
