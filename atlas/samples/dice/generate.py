#!/usr/bin/env python3
"""Render a deterministic Efron dice exhibit; no random trials."""
import csv
import io
import json
import math
from pathlib import Path
import zipfile
from PIL import Image,ImageDraw,ImageFont
from exact import DICE,audit
from verify import verify
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'assets/dice'
COLORS=['#eeae77','#8ed0bd','#a9bde9','#d7a1c7'];BG='#10252b'


def main():
    OUT.mkdir(parents=True,exist_ok=True);report=audit(DICE);assert verify(DICE,report)
    for name,value in [('dice.json',DICE),('audit.json',report)]: (OUT/name).write_text(json.dumps(value,indent=2)+'\n')
    table=io.StringIO();w=csv.writer(table);w.writerow(['rolls','first','second','wins','ties','losses','total','probability'])
    for n in ['1','2']:
        for a in 'ABCD':
            for b in 'ABCD':
                r=report['modes'][n]['pairs'][a+b];w.writerow([n,a,b]+[r[k] for k in ['wins','ties','losses','total','probability']])
    (OUT/'pairs.csv').write_text(table.getvalue())
    f=ImageFont.load_default(size=23);small=ImageFont.load_default(size=16);big=ImageFont.load_default(size=42);frames=[]
    positions=[(235,150),(390,305),(235,460),(80,305)]
    for active in range(4):
        for step in range(12):
            im=Image.new('RGB',(920,600),BG);d=ImageDraw.Draw(im)
            d.text((30,20),'NO CHAMPION / EFRON DICE',font=f,fill='#edf0db');d.text((30,55),'A > B > C > D > A     |     P = 2/3 on every arrow',font=small,fill='#bfd2c7')
            for i in range(4):
                x,y=positions[i];xx,yy=positions[(i+1)%4];dx=xx-x;dy=yy-y;length=math.hypot(dx,dy);ux=dx/length;uy=dy/length;sx=x+ux*68;sy=y+uy*68;ex=xx-ux*68;ey=yy-uy*68;color=COLORS[i] if i==active else '#3c5b5e'
                d.line((sx,sy,ex,ey),fill=color,width=5 if i==active else 2);d.polygon([(ex,ey),(ex-ux*15-uy*6,ey-uy*15+ux*6),(ex-ux*15+uy*6,ey-uy*15-ux*6)],fill=color)
            for i,(x,y) in enumerate(positions):
                name='ABCD'[i];color=COLORS[i];d.rounded_rectangle((x-58,y-55,x+58,y+55),12,fill='#1d383f',outline=color,width=3 if i==active else 1);d.text((x-45,y-46),name,font=f,fill=color)
                for k,face in enumerate(DICE[name]):d.text((x-42+(k%3)*32,y-8+(k//3)*27),str(face),font=f,fill='#edf0db')
            a='ABCD'[active];b='ABCD'[(active+1)%4];d.text((180,286),'24 / 36',font=f,fill=COLORS[active]);d.text((184,318),'EXACT WINS',font=small,fill='#bfd2c7')
            d.text((545,116),f'{a} versus {b}',font=big,fill=COLORS[active]);d.text((546,176),'Every face pair, not a simulation',font=small,fill='#bfd2c7')
            for j,val in enumerate(DICE[b]):d.text((575+j*45,211),str(val),font=small,fill=COLORS[(active+1)%4])
            for i,val in enumerate(DICE[a]):
                d.text((540,247+i*45),str(val),font=small,fill=COLORS[active])
                for j,other in enumerate(DICE[b]):
                    x=568+j*45;y=240+i*45;shown=i*6+j<(step+1)*3;fill=('#397e68' if val>other else '#b86d55') if shown else '#1d383f';d.rounded_rectangle((x,y,x+38,y+38),5,fill=fill)
                    if shown:d.text((x+12,y+9),'+' if val>other else '-',font=small,fill='#edf0db')
            d.text((545,527),'24 wins / 12 losses / 0 ties',font=small,fill='#edf0db');d.text((30,566),'Independent fair faces. A stronger chance is not a guaranteed win.',font=small,fill='#bfd2c7');frames.append(im)
    frames[11].save(OUT/'proof.png');frames[0].save(OUT/'cycle.gif',save_all=True,append_images=frames[1:],duration=140,loop=0,optimize=False)
    # A4 SVG with four cross nets. Tabs are deliberately omitted: educational fold model.
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="210mm" height="297mm" viewBox="0 0 210 297"><rect width="210" height="297" fill="white"/><g font-family="sans-serif" fill="#162f34"><text x="12" y="16" font-size="6">NO CHAMPION / FOUR LABELLED DICE</text><text x="12" y="25" font-size="3.4">A > B > C > D > A : 24/36 = 2/3 on each arrow</text>']
    cells=[(1,0),(0,1),(1,1),(2,1),(3,1),(1,2)]
    for i,name in enumerate('ABCD'):
        ox=14+(i%2)*98;oy=48+(i//2)*100;svg.append(f'<text x="{ox}" y="{oy-7}" font-size="6">{name} : '+','.join(map(str,DICE[name]))+'</text>')
        for (x,y),face in zip(cells,DICE[name]):
            xx=ox+x*19;yy=oy+y*19;svg.append(f'<rect x="{xx}" y="{yy}" width="19" height="19" fill="none" stroke="#426365" stroke-width=".3"/><text x="{xx+9.5}" y="{yy+12}" text-anchor="middle" font-size="8">{face}</text>')
    svg.append('<text x="12" y="258" font-size="3.4">Print at 100%. Face edge: 19 mm. Cut outline, score shared edges.</text><text x="12" y="266" font-size="3.4">No glue tabs: tape inside. Repeated labels are separate faces.</text><text x="12" y="274" font-size="3.4">Teaching model only: paper dice are not calibrated fair randomizers.</text></g></svg>');(OUT/'nets-a4.svg').write_text(''.join(svg)+'\n')
    html=Path(__file__).with_name('bench-template.html').read_text().replace('__DICE__',json.dumps(DICE)).replace('__REPORT__',json.dumps(report));(OUT/'table.html').write_text(html)
    with zipfile.ZipFile(OUT/'table.zip','w',zipfile.ZIP_DEFLATED) as z:
        for name in ['table.html','dice.json','audit.json','pairs.csv','nets-a4.svg','exact.py','verify.py']:
            data=Path(__file__).with_name(name).read_bytes() if name.endswith('.py') else (OUT/name).read_bytes();info=zipfile.ZipInfo(name,date_time=(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,data)
    print('Verified 32 pair/mode entries: 21,312 elementary outcomes; cycle 24/36 on all four edges.')

if __name__=='__main__':main()
