#!/usr/bin/env python3
"""Two-hole domino exhibit, exhaustive certificates and printable A4 materials."""
import csv
import io
import json
from itertools import combinations
from pathlib import Path
import zipfile
from PIL import Image,ImageDraw,ImageFont
from construct import cycle,construct,color,paths
from verify import verify,check_cycle
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'assets/domino'


def main():
    OUT.mkdir(parents=True,exist_ok=True);route=cycle();check_cycle(route);possible=construct([0,62]);impossible=construct([0,63]);rows=[];yes=no=0
    for a,b in combinations(range(64),2):
        c=construct([a,b]);verify(c);yes+=c['tileable'];no+=not c['tileable'];rows.append([a,b,c['remaining_colors'][0],c['remaining_colors'][1],int(c['tileable'])])
    assert (yes,no)==(1024,992)
    report={'pairs_checked':2016,'tileable':yes,'impossible':no,'domino_placements_checked':yes*31,'cycle':check_cycle(route),'possible':verify(possible),'impossible_example':verify(impossible),'chain_lengths_example':[len(x) for x in paths([0,62],route)]}
    for name,obj in [('cycle.json',route),('possible.json',possible),('impossible.json',impossible),('audit.json',report)]: (OUT/name).write_text(json.dumps(obj,indent=2)+'\n')
    text=io.StringIO();writer=csv.writer(text);writer.writerow(['hole_a','hole_b','dark_remaining','light_remaining','tileable']);writer.writerows(rows);(OUT/'pairs.csv').write_text(text.getvalue())
    f=ImageFont.load_default(size=22);small=ImageFont.load_default(size=15);frames=[];palette=['#9ac7b1','#b2bfdc','#d7b28c','#d3afc9']
    for step in range(32):
        im=Image.new('RGB',(1000,660),'#202b31');d=ImageDraw.Draw(im);d.text((28,20),'TWO HOLES / ONE COLOUR ARGUMENT',font=f,fill='#f3e6cd');d.text((28,56),'Every domino covers exactly one dark and one light square.',font=small,fill='#c5c9bc')
        for panel,holes in enumerate([[0,62],[0,63]]):
            ox=55+panel*500;oy=142;cell=47;d.text((ox-10,100),f'TILEABLE / {step} of 31 dominoes' if not panel else 'IMPOSSIBLE / TWO DARK HOLES',font=f,fill='#b8dec3' if not panel else '#eea3b5')
            for i in range(64):
                x=ox+i%8*cell;y=oy+i//8*cell;d.rectangle((x,y,x+cell-1,y+cell-1),fill='#e7d5af' if color(i) else '#445b63')
            if not panel:
                for k,(a,b) in enumerate(possible['dominoes'][:step]):
                    x=ox+min(a%8,b%8)*cell+3;y=oy+min(a//8,b//8)*cell+3;w=cell-6 if a%8==b%8 else 2*cell-6;h=2*cell-6 if a%8==b%8 else cell-6;d.rounded_rectangle((x,y,x+w,y+h),5,fill=palette[k%4],outline='#202b31',width=2)
                    for i in [a,b]:
                        xx=ox+i%8*cell+cell//2;yy=oy+i//8*cell+cell//2;d.ellipse((xx-3,yy-3,xx+3,yy+3),fill='#3b5157')
            for i in holes:
                x=ox+i%8*cell;y=oy+i//8*cell;d.rectangle((x+1,y+1,x+cell-2,y+cell-2),fill='#202b31',outline='#ed9baf',width=2);d.line((x+13,y+13,x+cell-13,y+cell-13),fill='#ed9baf',width=2);d.line((x+cell-13,y+13,x+13,y+cell-13),fill='#ed9baf',width=2)
            d.text((ox,541),'31 dark / 31 light' if not panel else '30 dark / 32 light',font=f,fill='#b8dec3' if not panel else '#eea3b5')
        d.text((28,591),'One 64-cell cycle constructs a tiling for every opposite-colour pair of holes.',font=small,fill='#f3e6cd');d.text((28,625),'2016 pairs checked: 1024 tileable / 992 impossible. Exactly two removed cells on a full 8x8 board.',font=small,fill='#c5c9bc');frames.append(im)
    frames[-1].save(OUT/'proof.png');frames[0].save(OUT/'tiling.gif',save_all=True,append_images=frames[1:],duration=[900]+[120]*30+[2200],loop=0,optimize=False)
    for kind in ['board','pieces']:
        svg=['<svg xmlns="http://www.w3.org/2000/svg" width="210mm" height="297mm" viewBox="0 0 210 297"><rect width="210" height="297" fill="white"/><g font-family="sans-serif" fill="#202b31">',f'<text x="25" y="19" font-size="6">TWO HOLES / {kind.upper()}</text>']
        if kind=='board':
            for i in range(64):
                x=25+i%8*20;y=40+i//8*20;svg.append(f'<rect x="{x}" y="{y}" width="20" height="20" fill="'+('#e7d5af' if color(i) else '#6d858a')+'" stroke="#202b31" stroke-width=".25"/>')
            for i in range(8):svg.append(f'<text x="{35+i*20}" y="35" text-anchor="middle" font-size="4">'+ 'ABCDEFGH'[i]+f'</text><text x="19" y="{52+i*20}" font-size="4">{i+1}</text>')
            svg.append('<text x="25" y="219" font-size="4">Choose exactly two cells to remove.</text><text x="25" y="229" font-size="4">Different colours: tileable. Same colour: impossible.</text>')
        else:
            for i in range(31):
                x=25+i%4*40;y=40+i//4*20;svg.append(f'<rect x="{x}" y="{y}" width="40" height="20" fill="#f6eddc" stroke="#202b31" stroke-width=".25"/><path d="M{x+20} {y+1}v18" stroke="#7d9290" stroke-width=".2" stroke-dasharray="1 1"/>')
            svg.append('<text x="25" y="219" font-size="4">31 dominoes, each 20 x 40 mm.</text><text x="25" y="229" font-size="4">Cut outer borders only. Do not cut dashed middle lines.</text>')
        svg.append('<text x="25" y="254" font-size="4">A4 / print at 100%. Board cell: 20 x 20 mm.</text><text x="25" y="264" font-size="4">Top-left is A1. Rotation allowed. No overlaps or gaps.</text></g></svg>')
        # Rotation is allowed: clarify that rotating a piece does not alter the colour argument.
        (OUT/(kind+'-a4.svg')).write_text(''.join(svg)+'\n')
    html=Path(__file__).with_name('bench-template.html').read_text().replace('__CYCLE__',json.dumps(route,separators=(',',':')));(OUT/'domino.html').write_text(html)
    with zipfile.ZipFile(OUT/'bench.zip','w',zipfile.ZIP_DEFLATED) as z:
        for name in ['domino.html','cycle.json','possible.json','impossible.json','audit.json','pairs.csv','board-a4.svg','pieces-a4.svg','verify.py','construct.py']:
            data=Path(__file__).with_name(name).read_bytes() if name.endswith('.py') else (OUT/name).read_bytes();info=zipfile.ZipInfo(name,date_time=(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,data)
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
