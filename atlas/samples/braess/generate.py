#!/usr/bin/env python3
"""Braess gallery: exact certificates, demand sweep, own illustrations."""
import base64
import csv
from fractions import Fraction as F
import io
import json
import math
from pathlib import Path
import zipfile
from PIL import Image,ImageDraw,ImageFont
from model import equilibrium
from verify import verify
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'assets/braess'


def main():
    OUT.mkdir(parents=True,exist_ok=True);samples={str(q):[equilibrium(q,False),equilibrium(q,True)] for q in range(1000,10001,100)}
    assert all(verify(c)['equilibrium_verified'] for pair in samples.values() for c in pair)
    for name,data in [('sweep.json',samples),('closed.json',samples['4000'][0]),('open.json',samples['4000'][1]),('audit.json',{'model':'nonatomic Wardrop; fixed directed network','scenarios_verified':182,'closed':verify(samples['4000'][0]),'open':verify(samples['4000'][1]),'delay_minutes':'15','time_ratio':'16/13','harmful_demand_interval':'3000 < Q < 9000'})]:
        (OUT/name).write_text(json.dumps(data,indent=2)+'\n')
    text=io.StringIO();w=csv.writer(text);w.writerow(['demand','closed_time','open_time','difference','open_SAT','open_SBT','open_SABT'])
    for q,pair in samples.items():
        a,b=pair;w.writerow([q,a['time'],b['time'],str(F(b['time'])-F(a['time']))]+[b['flows'][r] for r in ['SAT','SBT','SABT']])
    (OUT/'sweep.csv').write_text(text.getvalue())
    def coords(q,t):return (70+(q-1000)/9000*740,300-float(t)*2.5)
    lines=[]
    for index,color in [(0,'#9ad7c4'),(1,'#f2b58b')]:
        points=' '.join(f'{x:.2f},{y:.2f}' for q,pair in samples.items() for x,y in [coords(int(q),F(pair[index]['time']))]);lines.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="4"/>')
    chart='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 360" role="img" aria-label="Wardrop travel time by demand"><rect width="900" height="360" fill="#112b30"/><g font-family="sans-serif" fill="#f0e7d4"><text x="30" y="25" font-size="18">SAME DEMAND / DIFFERENT EQUILIBRIUM</text><text x="65" y="55" font-size="13">Minutes</text>'
    for t in [20,40,60,80,100]:
        y=300-t*2.5;chart+=f'<path d="M70 {y}H810" stroke="#355258"/><text x="35" y="{y+5}" font-size="13">{t}</text>'
    for q in [1000,3000,4500,6000,9000,10000]:
        x,_=coords(q,0);chart+=f'<text x="{x}" y="322" text-anchor="middle" font-size="12">{q}</text>'
    chart+=''.join(lines)+'<text x="70" y="348" fill="#9ad7c4" font-size="14">Closed</text><text x="180" y="348" fill="#f2b58b" font-size="14">Open A → B</text><text x="650" y="348" font-size="13">Demand Q</text></g></svg>\n';(OUT/'demand.svg').write_text(chart)
    frames=[];font=ImageFont.load_default(size=21);small=ImageFont.load_default(size=15);big=ImageFont.load_default(size=35)
    for frame in range(60):
        im=Image.new('RGB',(920,560),'#112b30');d=ImageDraw.Draw(im);d.text((28,20),'THE EXTRA ROAD / 4000 UNITS OF FLOW',font=font,fill='#f0e7d4')
        for panel in [0,1]:
            ox=panel*460;color='#f2b58b' if panel else '#9ad7c4';nodes={'S':(ox+35,286),'A':(ox+230,162),'B':(ox+230,410),'T':(ox+425,286)}
            d.text((ox+30,68),'OPEN: FREE A > B' if panel else 'CLOSED: TWO ROUTES',font=font,fill=color);d.text((ox+30,104),'80 minutes' if panel else '65 minutes',font=big,fill=color)
            edges=[('S','A','4000 / 40 min' if panel else '2000 / 20 min'),('A','T','0 / 45 min' if panel else '2000 / 45 min'),('S','B','0 / 45 min' if panel else '2000 / 45 min'),('B','T','4000 / 40 min' if panel else '2000 / 20 min')]
            if panel:edges.append(('A','B','4000 / 0 min'))
            for a,b,label in edges:
                x,y=nodes[a];xx,yy=nodes[b];dx=xx-x;dy=yy-y;length=math.hypot(dx,dy);ux=dx/length;uy=dy/length;ex=xx-ux*20;ey=yy-uy*20;d.line((x,y,ex,ey),fill='#527b7b',width=5);d.polygon([(ex,ey),(ex-ux*13-uy*5,ey-uy*13+ux*5),(ex-ux*13+uy*5,ey-uy*13-ux*5)],fill='#91b7ac')
            routes=[('SABT',18)] if panel else [('SAT',9),('SBT',9)]
            for route,count in routes:
                for k in range(count):
                    p=(k/count+frame/60)%1*(len(route)-1);i=int(p);t=p-i;a=nodes[route[i]];b=nodes[route[i+1]];x=a[0]*(1-t)+b[0]*t;y=a[1]*(1-t)+b[1]*t;d.ellipse((x-3,y-3,x+3,y+3),fill=color)
            for a,b,label in edges:
                x=(nodes[a][0]+nodes[b][0])/2;y=(nodes[a][1]+nodes[b][1])/2;d.rectangle((x-62,y-12,x+62,y+12),fill='#112b30');d.text((x-57,y-9),label,font=small,fill='#f0e7d4')
            for name,(x,y) in nodes.items():d.ellipse((x-17,y-17,x+17,y+17),fill='#2a4f55');d.text((x-6,y-12),name,font=font,fill='#f0e7d4')
            d.text((ox+30,457),'Used route costs: 80' if panel else 'Used route costs: 65 and 65',font=small,fill=color);d.text((ox+30,483),'Unused old routes: 85 and 85' if panel else 'No unilateral infinitesimal improvement',font=small,fill='#bdd3cb')
        d.text((28,529),'Exact Wardrop equilibrium. Moving dots are schematic, not a traffic microsimulation.',font=small,fill='#bdd3cb');frames.append(im)
    frames[0].save(OUT/'proof.png');frames[0].save(OUT/'roads.gif',save_all=True,append_images=frames[1:],duration=80,loop=0,optimize=False)
    html=Path(__file__).with_name('bench-template.html').read_text().replace('__DATA__',json.dumps(samples,separators=(',',':'))).replace('__CHART__',base64.b64encode(chart.encode()).decode());(OUT/'roads.html').write_text(html)
    with zipfile.ZipFile(OUT/'bench.zip','w',zipfile.ZIP_DEFLATED) as z:
        for name in ['roads.html','closed.json','open.json','sweep.json','sweep.csv','audit.json','demand.svg','verify.py','model.py']:
            data=Path(__file__).with_name(name).read_bytes() if name.endswith('.py') else (OUT/name).read_bytes();info=zipfile.ZipInfo(name,date_time=(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,data)
    print('182 exact certificates verified. Q=4000: 65 -> 80 minutes; harmful iff 3000 < Q < 9000.')

if __name__=='__main__':main()
