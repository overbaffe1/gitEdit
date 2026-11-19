#!/usr/bin/env python3
"""Deterministic transport gallery assets. Run from any directory."""
import csv
import io
import json
import math
from pathlib import Path
import zipfile
from PIL import Image, ImageDraw, ImageFont
from solve import costs,greedy,hungarian
from verify import verify

ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'assets/transport'

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    # Two distinct lattice silhouettes: an open spiral and a five-point star outline.
    source=[[round(125+(20+1.8*k)*math.cos(k*.30)),round(125+(20+1.8*k)*math.sin(k*.30))] for k in range(64)]
    vertices=[[125+108*math.cos(-math.pi/2+k*math.pi/5)*(1 if k%2==0 else .43),125+108*math.sin(-math.pi/2+k*math.pi/5)*(1 if k%2==0 else .43)] for k in range(10)]
    target=[]
    for k in range(64):
        edge=k*10/64;i=int(edge);t=edge-i;a=vertices[i];b=vertices[(i+1)%10]
        target.append([round(a[d]*(1-t)+b[d]*t) for d in (0,1)])
    problem={'cost':'squared_euclidean','source':source,'target':target};matrix=costs(source,target);certificate=hungarian(matrix);g=greedy(matrix);report=verify(problem,certificate)
    report['greedy_cost']=sum(matrix[i][j] for i,j in enumerate(g));report['greedy_excess_percent']=round(100*(report['greedy_cost']/report['primal_cost']-1),2)
    def save(name,obj):(OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    save('problem.json',problem);save('certificate.json',certificate);save('audit.json',report)
    text=io.StringIO();writer=csv.writer(text);writer.writerow(['source','greedy_target','optimal_target','greedy_cost','optimal_cost'])
    for i,j in enumerate(g):writer.writerow([i,j,certificate['assignment'][i],matrix[i][j],matrix[i][certificate['assignment'][i]]])
    (OUT/'assignments.csv').write_text(text.getvalue())
    frames=[]
    font=ImageFont.load_default(size=17);small=ImageFont.load_default(size=13)
    for frame in range(41):
        t=(1-math.cos(math.pi*frame/40))/2;im=Image.new('RGB',(840,420),'#101d2b');d=ImageDraw.Draw(im)
        d.text((26,18),'MIGRATION / 64 PARTICLES',font=font,fill='#e8e0cb')
        for panel,(assignment,title,color,total) in enumerate([(g,'NEAREST FREE','#f5ae76',report['greedy_cost']),(certificate['assignment'],'GLOBAL + CERTIFICATE','#7be0ce',report['primal_cost'])]):
            offset=40+panel*410;d.text((offset,56),title,font=font,fill=color);d.text((offset,82),f'Sum squared distance: {total}',font=small,fill='#bac9d5')
            for i,j in enumerate(assignment):
                a=source[i];b=target[j];ax=offset+int(a[0]*1.2);ay=110+int(a[1]*1.05);bx=offset+int(b[0]*1.2);by=110+int(b[1]*1.05)
                d.line((ax,ay,bx,by),fill='#283c4e');x=round(ax*(1-t)+bx*t);y=round(ay*(1-t)+by*t);d.ellipse((x-3,y-3,x+3,y+3),fill=color)
        d.text((26,394),f'Exact dual lower bound = {report["dual_lower_bound"]} | 4096 inequalities checked | gap 0',font=small,fill='#bac9d5');frames.append(im)
    frames[20].save(OUT/'proof.png');frames[0].save(OUT/'migration.gif',save_all=True,append_images=frames[1:]+frames[-2:0:-1],duration=60,loop=0,optimize=False)
    template=(Path(__file__).with_name('bench-template.html')).read_text();html=template.replace('__DATA__',json.dumps({'problem':problem,'certificate':certificate,'greedy':g},separators=(',',':')))
    (OUT/'transport.html').write_text(html)
    with zipfile.ZipFile(OUT/'bench.zip','w',zipfile.ZIP_DEFLATED) as z:
        for name in ['transport.html','problem.json','certificate.json','audit.json','assignments.csv']:
            info=zipfile.ZipInfo(name,date_time=(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,(OUT/name).read_bytes())
        for name in ['verify.py','solve.py']:z.writestr(zipfile.ZipInfo(name,date_time=(2026,1,1,0,0,0)),Path(__file__).with_name(name).read_bytes())
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
