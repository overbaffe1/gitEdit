#!/usr/bin/env python3
"""Generate certified Lights Out 5x5 exhibit, deterministic and offline."""
import json
from pathlib import Path
import zipfile
from PIL import Image,ImageDraw,ImageFont
from core import certificate,apply,solve,moves
from verify import check
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'assets/lights'


def main():
    OUT.mkdir(parents=True,exist_ok=True);cert=certificate();start=apply((1<<25)-1);solution=solve(start,cert);impossible=solve(start^1,cert);audit=check(cert,solution);check(cert,impossible)
    assert solution['minimum']==9 and [x.bit_count() for x in solution['candidates']]==[9,13,13,25]
    for name,data in [('certificate.json',cert),('solution.json',solution),('impossible.json',impossible),('audit.json',audit)]: (OUT/name).write_text(json.dumps(data,indent=2)+'\n')
    press=[i for i in range(25) if solution['chosen']>>i&1];board=start;route=[{'board':board,'pressed':None}]
    for i in press:board^=moves()[i];route.append({'board':board,'pressed':i})
    assert board==0;(OUT/'route.json').write_text(json.dumps(route,indent=2)+'\n')
    f=ImageFont.load_default(size=22);small=ImageFont.load_default(size=15);frames=[]
    for step,state in enumerate(route):
        im=Image.new('RGB',(920,620),'#10262d');d=ImageDraw.Draw(im);d.text((28,20),'LIGHTS OUT / TWO INVISIBLE SEALS',font=f,fill='#f0e7cf');d.text((28,57),'A legal press changes a cross. A single edited lamp changes the solvability class.',font=small,fill='#b6d1cd')
        for panel,b in enumerate([state['board'],start^1]):
            ox=55+panel*460;d.text((ox-14,103),f'SOLVABLE / move {step} of 9' if not panel else 'ONE LAMP EDITED / IMPOSSIBLE',font=f,fill='#c9ead6' if not panel else '#ee9fb8')
            for i in range(25):
                x=ox+i%5*61;y=150+i//5*61;on=b>>i&1;d.rounded_rectangle((x,y,x+53,y+53),9,fill='#f2c267' if on else '#19363e',outline='#ffe7a3' if on else '#40606a',width=1)
                if panel and i==0:d.rounded_rectangle((x-3,y-3,x+56,y+56),10,outline='#ee9fb8',width=3)
                if not panel and state['pressed']==i:d.ellipse((x+18,y+18,x+36,y+36),fill='#b5476a')
            syndrome=[(b&m).bit_count()%2 for m in cert['checks']];d.text((ox,475),'Conserved parities: '+' / '.join(map(str,syndrome)),font=small,fill='#c9ead6' if not panel else '#ee9fb8')
        for index,seal in enumerate(cert['checks']):
            ox=55+index*190
            for i in range(25):
                x=ox+(i%5)*12;y=516+(i//5)*12;d.rectangle((x,y,x+9,y+9),fill='#ac9eeb' if seal>>i&1 else '#284650')
            d.text((ox+68,532),f'SEAL {index+1}',font=small,fill='#ac9eeb')
        d.text((515,523),'Initial solution weights: 9, 13, 13, 25',font=small,fill='#f0e7cf');d.text((515,549),'Both parities must be zero.',font=small,fill='#b6d1cd');d.text((28,590),'Rank 23 / 25 | 202 reversible row operations checked | exactly 1/4 of all boards solvable',font=small,fill='#b6d1cd');frames.append(im)
    frames[0].save(OUT/'proof.png');frames[0].save(OUT/'switches.gif',save_all=True,append_images=frames[1:],duration=[1000]+[650]*(len(frames)-2)+[2200],loop=0,optimize=False)
    svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 330" role="img" aria-label="Two conserved parity patterns for bounded 5x5 Lights Out"><rect width="620" height="330" fill="#10262d"/><g font-family="sans-serif" fill="#f0e7cf"><text x="25" y="30" font-size="20">TWO CONSERVED PARITIES / GF(2)</text>']
    for k,m in enumerate(cert['checks']):
        ox=35+k*310;svg.append(f'<text x="{ox}" y="64" font-size="16">Seal {k+1}</text>')
        for i in range(25):svg.append(f'<rect x="{ox+(i%5)*40}" y="{80+(i//5)*40}" width="34" height="34" rx="5" fill="'+('#ac9eeb' if m>>i&1 else '#284650')+'"/>')
    svg.append('<text x="25" y="312" font-size="14">Parity of lit marked cells is unchanged by every legal cross press.</text></g></svg>');(OUT/'seals.svg').write_text(''.join(svg)+'\n')
    data={'certificate':cert,'start':start};html=Path(__file__).with_name('bench-template.html').read_text().replace('__DATA__',json.dumps(data,separators=(',',':')));(OUT/'lights.html').write_text(html)
    with zipfile.ZipFile(OUT/'bench.zip','w',zipfile.ZIP_DEFLATED) as z:
        for name in ['lights.html','certificate.json','solution.json','impossible.json','audit.json','route.json','seals.svg','verify.py','core.py']:
            data=Path(__file__).with_name(name).read_bytes() if name.endswith('.py') else (OUT/name).read_bytes();info=zipfile.ZipInfo(name,date_time=(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,data)
    print(json.dumps(audit,indent=2))

if __name__=='__main__':main()
