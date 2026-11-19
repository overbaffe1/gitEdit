#!/usr/bin/env python3
"""Classic cospectral graph pair, own drawings and independent integer certificates."""
import argparse
import csv
import json
import math
from pathlib import Path
import zipfile
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import certify
import heat

ROOT=Path(__file__).resolve().parents[3]
SAMPLE=Path(__file__).resolve().parent


def graphs():
    rook=[[0]*16 for _ in range(16)];shrikhande=[[0]*16 for _ in range(16)]
    generators={(1,0),(3,0),(0,1),(0,3),(1,1),(3,3)}
    for i in range(16):
        x,y=divmod(i,4)
        for j in range(16):
            u,v=divmod(j,4)
            rook[i][j]=int(i!=j and (x==u or y==v))
            shrikhande[i][j]=int(((u-x)%4,(v-y)%4) in generators)
    return rook,shrikhande


def positions():
    centers=[(130,100),(350,100),(130,300),(350,300)];left=[]
    for i in range(16):
        cx,cy=centers[i//4];angle=2*math.pi*(i%4)/4-math.pi/4
        left.append([round(cx+57*math.cos(angle),6),round(cy+57*math.sin(angle),6)])
    right=[[round(240+170*math.cos(2*math.pi*i/16-math.pi/2),6),round(200+170*math.sin(2*math.pi*i/16-math.pi/2),6)] for i in range(16)]
    return [left,right]


def write_matrix(path,a):
    with path.open('w',newline='') as f:
        writer=csv.writer(f,lineterminator='\n');writer.writerow(['vertex',*range(len(a))])
        for i,row in enumerate(a):writer.writerow([i,*row])


def graph_image(a,pos,distribution,source=0,highlight=False):
    image=Image.new('RGB',(480,400),'#10232e');d=ImageDraw.Draw(image);font=ImageFont.load_default(size=12)
    for i in range(16):
        for j in range(i+1,16):
            if a[i][j]:d.line([tuple(pos[i]),tuple(pos[j])],fill='#efd09a' if highlight and i<4 and j<4 else '#426675',width=3 if highlight and i<4 and j<4 else 1)
    cold=np.array([29,66,82]);hot=np.array([245,209,154])
    for i,(x,y) in enumerate(pos):
        value=math.sqrt(max(0,min(1,float(distribution[i]))));color=tuple(np.floor(cold+(hot-cold)*value+.5).astype(int))
        d.ellipse((x-13,y-13,x+13,y+13),fill=color,outline='#ffffff' if i==source else '#efd09a' if highlight and i<4 else '#527888',width=3 if i==source else 2)
        d.text((x,y),str(i+1),font=font,fill='#ffffff',anchor='mm')
    return image


def plate(pair,t,broken=False,highlight=False):
    pair=[[row[:] for row in a] for a in pair]
    if broken:pair[1][0][1]=pair[1][1][0]=0
    image=Image.new('RGB',(1000,730),'#152934');d=ImageDraw.Draw(image);large=ImageFont.load_default(size=23);small=ImageFont.load_default(size=16)
    d.text((24,16),'SAME SPECTRUM / DIFFERENT NETWORKS',font=large,fill='#efd09a')
    subtitle='CONTROL: ONE EDGE REMOVED ON THE RIGHT' if broken else 'EXACT INTEGER CERTIFICATE / NOT JUST ROUNDED EIGENVALUES'
    d.text((24,53),subtitle,font=small,fill='#bdd1ce')
    traces=[]
    for i,(a,pos,name) in enumerate(zip(pair,positions(),['ROOK 4x4','SHRIKHANDE'])):
        kernel=heat.kernel(a,t);traces.append(float(np.trace(kernel)))
        image.paste(graph_image(a,pos,kernel[:,0],highlight=highlight and i==0),(10+500*i,112))
        d.text((24+500*i,88),name+(' / 47 EDGES' if broken and i==1 else ' / 16 NODES, 48 EDGES'),font=small,fill='#efd09a')
        d.text((24+500*i,530),f'HEAT TRACE AT t={t:.2f}: {traces[-1]:.8f}',font=small,fill='#efd09a')
        d.text((24+500*i,565),'COMPLETE FOUR-NODE CLIQUES: '+('8' if i==0 else '0'),font=small,fill='#bdd1ce')
    if not broken:d.text((24,612),'SHARED LAPLACIAN SPECTRUM: 0 x 1, 4 x 6, 8 x 9. YET NOT ISOMORPHIC.',font=small,fill='#efd09a')
    else:d.text((24,612),f'EDGE 1-2 DELETED: HEAT-TRACE DIFFERENCE = {abs(traces[0]-traces[1]):.8f}',font=small,fill='#efd09a')
    d.text((24,650),'COLOUR: sqrt(HEAT) ON ONE FIXED SCALE. WHITE OUTLINE: SINGLE SOURCE.',font=small,fill='#bdd1ce')
    d.text((24,689),'LAYOUT IS DECORATIVE. EDGES HAVE UNIT CONDUCTANCE. THIS IS NOT A PHYSICAL DRUM.',font=small,fill='#bdd1ce')
    return image


def generate(output):
    output.mkdir(parents=True,exist_ok=True);pair=graphs()
    for name,a in zip(('rook','shrikhande'),pair):write_matrix(output/(name+'.csv'),a)
    # Independent path: reload published CSV matrices before all certification and rendering.
    pair=[certify.load(output/(name+'.csv')) for name in ('rook','shrikhande')]
    reports=[certify.certify(a) for a in pair]
    (output/'certificates.json').write_text(json.dumps(dict(zip(('rook','shrikhande'),reports)),indent=2)+'\n')
    with (output/'edges.csv').open('w',newline='') as f:
        writer=csv.writer(f,lineterminator='\n');writer.writerow(['graph','from_zero_based','to_zero_based'])
        for name,a in zip(('rook','shrikhande'),pair):
            for i in range(16):
                for j in range(i+1,16):
                    if a[i][j]:writer.writerow([name,i,j])
    broken=[row[:] for row in pair[1]];broken[0][1]=broken[1][0]=0;broken_report=certify.certify(broken)
    with (output/'heat-trace.csv').open('w',newline='') as f:
        writer=csv.writer(f,lineterminator='\n');writer.writerow(['time','rook_trace','shrikhande_trace','deleted_edge_trace','shared_exact_formula','rook_mass','shrikhande_mass'])
        for t in np.linspace(0,2,101):
            kernels=[heat.kernel(a,float(t)) for a in [*pair,broken]]
            writer.writerow([f'{t:.2f}',*[f'{np.trace(k):.15f}' for k in kernels],f'{1+6*math.exp(-4*t)+9*math.exp(-8*t):.15f}',float(kernels[0][:,0].sum()),float(kernels[1][:,0].sum())])
    plate(pair,.25,highlight=True).save(output/'poster.png');plate(pair,.25,broken=True,highlight=True).save(output/'broken.png')
    stages=[(float(t),False,False) for t in np.linspace(0,1,21)]+[(.25,False,True),(.25,True,True)]+[(float(t),True,True) for t in np.linspace(.3,1,8)]+[(.25,False,True)]
    frames=[plate(pair,*stage) for stage in stages]
    sheet=Image.new('RGB',(1000,1460));sheet.paste(frames[0],(0,0));sheet.paste(frames[22],(0,730))
    palette=sheet.quantize(colors=256,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
    indexed=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
    durations=[150]*len(frames);durations[0]=700;durations[21]=1800;durations[22]=1800;durations[-1]=1600
    indexed[0].save(output/'twins.gif',save_all=True,append_images=indexed[1:],loop=0,duration=durations,disposal=2,optimize=False)
    config={'adjacencies':pair,'positions':positions()};live=(SAMPLE/'bench-template.html').read_text().replace('__CONFIG__',json.dumps(config,separators=(',',':'))).encode();(output/'bench.html').write_bytes(live)
    with zipfile.ZipFile(output/'bench.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
        info=zipfile.ZipInfo('bench.html',(2026,11,18,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,live)
    t=.25;trace=[float(np.trace(heat.kernel(a,t))) for a in [*pair,broken]]
    facts={'pair':'classic 4x4 rook and Shrikhande graphs; independently constructed from definitions, not a new discovery',
           'vertices_each':16,'edges_each':48,'adjacency_spectrum':{'6':1,'2':6,'-2':9},'laplacian_spectrum':{'0':1,'4':6,'8':9},
           'exact_common_identity':'A^2 = 4I + 2J','four_cliques':[r['four_clique_count'] for r in reports],
           'same_exact_adjacency_polynomial':reports[0]['adjacency_characteristic_descending']==reports[1]['adjacency_characteristic_descending'],
           'same_exact_laplacian_polynomial':reports[0]['laplacian_characteristic_descending']==reports[1]['laplacian_characteristic_descending'],
           'trace_at_0_25':trace,'deleted_edge':[0,1],'deleted_edge_identity':broken_report['A_squared_equals_4I_plus_2J'],
           'frames':len(frames),'heat_solver':'uniformization, 97 terms (k=0..96), max time 2, max degree 6',
           'limits':'finite simple unit-weight graphs, not geometric drums; same spectrum does not imply same labelled heat kernel'}
    (output/'facts.json').write_text(json.dumps(facts,indent=2)+'\n');print(json.dumps(facts,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=ROOT/'assets/twins');generate(p.parse_args().output)
