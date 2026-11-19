#!/usr/bin/env python3
"""Generate exact eight-puzzle table, optimal route and gallery."""
import base64
import csv
import io
import json
from pathlib import Path
import zipfile
from PIL import Image,ImageDraw,ImageFont
from core import HARD,build,path,parity
from verify import check
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'assets/puzzle'


def main():
    OUT.mkdir(parents=True,exist_ok=True);table=build();report=check(table);route=path(HARD,table);assert len(route)==32
    impossible=tuple(2 if x==1 else 1 if x==2 else x for x in HARD)
    report['witness']={'start':list(HARD),'distance':31,'swapped':list(impossible),'swapped_parity':parity(impossible)}
    (OUT/'distances.bin').write_bytes(table);(OUT/'certificate.json').write_text(json.dumps(report,indent=2)+'\n');(OUT/'route.json').write_text(json.dumps(route,indent=2)+'\n')
    text=io.StringIO();w=csv.writer(text);w.writerow(['step','remaining','board'])
    for i,board in enumerate(route):w.writerow([i,31-i,''.join(map(str,board))])
    (OUT/'route.csv').write_text(text.getvalue())
    font=ImageFont.load_default(size=22);small=ImageFont.load_default(size=16);big=ImageFont.load_default(size=44);frames=[]
    colors=['','#ecc693','#e3b77f','#d5a573','#b9c8b2','#a4c3b5','#8cb8ae','#9eb6ce','#b1bdd4']
    def draw_board(d,board,ox,oy,next_board=None,t=0,forbidden=False):
        d.rounded_rectangle((ox-7,oy-7,ox+311,oy+311),12,fill='#0e1720')
        for i,value in enumerate(board):
            if not value:continue
            target=next_board.index(value) if next_board else i;x=ox+((i%3)*(1-t)+(target%3)*t)*104;y=oy+((i//3)*(1-t)+(target//3)*t)*104
            d.rounded_rectangle((x,y,x+96,y+96),9,fill=colors[value],outline='#e9d9b9',width=1)
            # Small inset and corner mark evoke a physical numbered tile.
            d.rounded_rectangle((x+7,y+7,x+89,y+89),7,outline='#766d63',width=1);d.text((x+34,y+24),str(value),font=big,fill='#20303b')
            if forbidden and value in (1,2):d.rectangle((x+3,y+3,x+93,y+93),outline='#c95069',width=5)
    for move in range(31):
        for sub in range(3):
            im=Image.new('RGB',(920,560),'#16212d');d=ImageDraw.Draw(im);d.text((30,22),'ONE SWAP / NO WAY HOME',font=font,fill='#f4e6cf');d.text((30,61),'Same tiles. Same rules. Different connected components.',font=small,fill='#bdd0d6')
            d.text((56,111),f'REACHABLE / {31-move} moves left',font=font,fill='#9ce3cf');d.text((518,111),'SWAP 1 AND 2 / IMPOSSIBLE',font=font,fill='#efa2af')
            draw_board(d,route[move],56,162,route[move+1],sub/3);draw_board(d,impossible,518,162,forbidden=True)
            d.text((56,493),f'Optimal route: move {move} / 31',font=small,fill='#bdd0d6');d.text((518,493),'Odd inversion parity stays odd forever.',font=small,fill='#bdd0d6');d.text((30,533),'181,440 reachable states | maximum distance 31 | all reachable edges checked',font=small,fill='#f4e6cf');frames.append(im)
    frames[0].save(OUT/'proof.png')
    final=frames[-1].copy();d=ImageDraw.Draw(final);d.rectangle((45,100,460,520),fill='#16212d');d.text((56,111),'HOME / 0 moves left',font=font,fill='#9ce3cf');draw_board(d,route[-1],56,162);d.text((56,493),'Exactly 31 legal moves. No shortcut.',font=small,fill='#bdd0d6');frames.append(final)
    frames[0].save(OUT/'route.gif',save_all=True,append_images=frames[1:],duration=[1000]+[80]*(len(frames)-2)+[1800],loop=0,optimize=False)
    bars=[]
    for key,value in report['histogram'].items():
        k=int(key);height=value/25000*180;bars.append(f'<rect x="{30+k*22}" y="{220-height:.2f}" width="17" height="{height:.2f}" fill="#9ce3cf"/><text x="{38+k*22}" y="238" text-anchor="middle">{k}</text>')
    (OUT/'histogram.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 270" role="img" aria-label="Number of reachable states by exact distance"><rect width="780" height="270" fill="#16212d"/><g font-family="sans-serif" font-size="11" fill="#f4e6cf"><text x="30" y="25" font-size="17">181,440 states / exact distance to 123456780</text>'+''.join(bars)+'<text x="30" y="260">Two states at distance 31. Unreachable permutations are not included.</text></g></svg>\n')
    html=Path(__file__).with_name('bench-template.html').read_text().replace('__TABLE__',base64.b64encode(table).decode());(OUT/'puzzle.html').write_text(html)
    with zipfile.ZipFile(OUT/'bench.zip','w',zipfile.ZIP_DEFLATED) as z:
        for name in ['puzzle.html','distances.bin','certificate.json','route.json','route.csv','verify.py','core.py']:
            data=Path(__file__).with_name(name).read_bytes() if name.endswith('.py') else (OUT/name).read_bytes();info=zipfile.ZipInfo(name,date_time=(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,data)
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
