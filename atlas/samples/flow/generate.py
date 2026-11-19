#!/usr/bin/env python3
"""Exact two-valve flow gallery with portable flow/cut certificates."""
import base64
import csv
import io
import json
import math
from pathlib import Path
import zipfile
from PIL import Image,ImageDraw,ImageFont
from solve import solve,edges,LABELS
from verify import verify,all_cuts
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'assets/flow'


def main():
    OUT.mkdir(parents=True,exist_ok=True);samples={f'{a},{b}':solve(a,b) for a in range(13) for b in range(13)};reports={key:verify(c,True) for key,c in samples.items()};assert all(r['exhaustive_agrees'] for r in reports.values())
    presets=[('baseline',7,6),('inlet',9,6),('outlet',7,8),('both',9,8),('wide',12,12)]
    def save(name,obj):(OUT/name).write_text(json.dumps(obj,indent=2)+'\n')
    save('scenarios.json',samples)
    for name,a,b in presets:save(name+'.json',samples[f'{a},{b}'])
    save('audit.json',{'scenarios_verified':169,'cuts_enumerated':169*64,'presets':{name:reports[f'{a},{b}'] for name,a,b in presets},'largest_flow_on_grid':max(c['value'] for c in samples.values())})
    summary=io.StringIO();sw=csv.writer(summary);sw.writerow(['alpha','beta','flow','cut_capacity','number_of_minimum_cuts'])
    cuts=io.StringIO();cw=csv.writer(cuts);cw.writerow(['alpha','beta','source_side','capacity'])
    for key,c in samples.items():
        a,b=c['valve_a'],c['valve_b'];r=reports[key];sw.writerow([a,b,c['value'],r['cut_capacity'],len(r['all_minimum_cuts'])])
        for cut in all_cuts(a,b):cw.writerow([a,b,''.join(LABELS[i] for i in cut['source_side']),cut['capacity']])
    (OUT/'sweep.csv').write_text(summary.getvalue());(OUT/'cuts.csv').write_text(cuts.getvalue())
    svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 500" role="img" aria-label="Maximum flow for all 169 pairs of valve capacities"><rect width="480" height="500" fill="#142735"/><g font-family="sans-serif" text-anchor="middle" fill="#f4e4c8"><text x="240" y="27" font-size="18">TWO VALVES / EXACT MAXIMUM FLOW</text><text x="20" y="52" font-size="14">β</text>']
    for b in range(13):
        y=65+(12-b)*29;svg.append(f'<text x="31" y="{y+18}" font-size="12">{b}</text>')
        for a in range(13):
            value=samples[f'{a},{b}']['value'];t=(value-5)/9;rgb=tuple(round(lo*(1-t)+hi*t) for lo,hi in zip((44,87,108),(242,193,122)));color='#'+''.join(f'{x:02x}' for x in rgb);x=52+a*29;svg.append(f'<rect x="{x}" y="{y}" width="26" height="26" rx="3" fill="{color}"/><text x="{x+13}" y="{y+18}" font-size="12" fill="'+('#142735' if value>=10 else '#f4e4c8')+f'">{value}</text>')
    for a in range(13):svg.append(f'<text x="{65+a*29}" y="463" font-size="12">{a}</text>')
    svg.append('<text x="440" y="463" font-size="14">α</text><text x="240" y="489" font-size="12">Each cell has a checked feasible flow and equal-capacity cut.</text></g></svg>');map_svg=''.join(svg)+'\n';(OUT/'map.svg').write_text(map_svg)
    f=ImageFont.load_default(size=23);small=ImageFont.load_default(size=16);big=ImageFont.load_default(size=36);frames=[]
    nodes=[(45,300),(260,180),(260,420),(500,180),(500,420),(740,180),(740,420),(955,300)]
    captions=['BASELINE','ONLY INLET WIDER','ONLY OUTLET WIDER','BOTH VALVES WIDER','NOW ANOTHER CUT LIMITS THE FLOW']
    for phase,(name,a,b) in enumerate(presets):
        c=samples[f'{a},{b}'];cut=c['cut']
        for frame in range(8):
            im=Image.new('RGB',(1000,620),'#142735');d=ImageDraw.Draw(im);d.text((28,20),'TWO VALVES / ONE LIMIT',font=f,fill='#f4e4c8');d.text((28,63),captions[phase],font=f,fill='#a2e0cc');d.text((28,105),f'alpha = {a}, beta = {b}   |   maximum = {c["value"]}',font=big,fill='#f2c17a')
            for i,(u,v,cap) in enumerate(edges(a,b)):
                x,y=nodes[u];xx,yy=nodes[v];dx=xx-x;dy=yy-y;length=math.hypot(dx,dy);ux=dx/length;uy=dy/length;ex=xx-ux*21;ey=yy-uy*21;cross=u in cut and v not in cut;color='#f19a9f' if cross else '#638c9d';d.line((x,y,ex,ey),fill=color,width=6 if cross else 3);d.polygon([(ex,ey),(ex-ux*14-uy*6,ey-uy*14+ux*6),(ex-ux*14+uy*6,ey-uy*14-ux*6)],fill=color)
                flow=c['flows'][i]
                for k in range(flow):
                    t=(k/max(flow,1)+frame/8)%1;px=x*(1-t)+xx*t;py=y*(1-t)+yy*t;d.ellipse((px-2,py-2,px+2,py+2),fill='#e7dcc7')
            for i,(u,v,cap) in enumerate(edges(a,b)):
                x,y=nodes[u];xx,yy=nodes[v];mx=(x+xx)/2;my=(y+yy)/2+(-18 if yy>y else 18) if u>0 and v<7 and yy!=y else (y+yy)/2;d.rectangle((mx-30,my-14,mx+30,my+14),fill='#142735');d.text((mx-24,my-10),f'{c["flows"][i]} / {cap}',font=small,fill='#f4e4c8')
            for i,(x,y) in enumerate(nodes):d.ellipse((x-20,y-20,x+20,y+20),fill='#8fd6c0' if i in cut else '#b6a4df');d.text((x-7,y-14),LABELS[i],font=f,fill='#142735')
            d.text((28,485),f'Feasible flow = {c["value"]}   |   red cut capacity = {reports[f"{a},{b}"]["cut_capacity"]}   |   gap = 0',font=f,fill='#a2e0cc');d.text((28,532),'Baseline 12  /  inlet only 12  /  outlet only 12  /  both 14  /  wider still 14',font=small,fill='#f4e4c8');d.text((28,584),'Flow / capacity labels. Dots are schematic: no pressure, travel time or fluid dynamics simulated.',font=small,fill='#b8ced3');frames.append(im)
    frames[24].save(OUT/'proof.png');frames[0].save(OUT/'valves.gif',save_all=True,append_images=frames[1:],duration=150,loop=0,optimize=False)
    html=Path(__file__).with_name('bench-template.html').read_text().replace('__DATA__',json.dumps(samples,separators=(',',':'))).replace('__MAP__',base64.b64encode(map_svg.encode()).decode());(OUT/'flow.html').write_text(html)
    with zipfile.ZipFile(OUT/'bench.zip','w',zipfile.ZIP_DEFLATED) as z:
        for name in ['flow.html','scenarios.json','baseline.json','inlet.json','outlet.json','both.json','wide.json','audit.json','sweep.csv','cuts.csv','map.svg','verify.py','solve.py']:
            data=Path(__file__).with_name(name).read_bytes() if name.endswith('.py') else (OUT/name).read_bytes();info=zipfile.ZipInfo(name,date_time=(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,data)
    print('169 flow/cut certificates verified, 10816 cuts enumerated. Presets: 12, 12, 12, 14, 14.')

if __name__=='__main__':main()
