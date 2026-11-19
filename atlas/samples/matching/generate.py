#!/usr/bin/env python3
"""Deterministic 8x8 stable-matching gallery. Preferences are a committed fixture."""
import csv
import io
import json
from pathlib import Path
import zipfile
from PIL import Image,ImageDraw,ImageFont
from solve import deferred
from verify import enumerate_stable,audit,blocking
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'assets/matching'


def main():
    OUT.mkdir(parents=True,exist_ok=True);problem=json.loads(Path(__file__).with_name('problem.json').read_text());logs={side:deferred(problem,side) for side in ['A','B']}
    first=logs['A']['assignment'];second=logs['B']['assignment'];stable=enumerate_stable(problem);certificate={'A_assignment':first,'B_assignment':second,'all_stable':stable};report=audit(problem,first,second,stable)
    swapped=first.copy();swapped[0],swapped[1]=swapped[1],swapped[0];witness={'assignment':swapped,'blocking_pairs':blocking(problem,swapped)}
    for name,obj in [('problem.json',problem),('certificate.json',certificate),('audit.json',report),('events.json',logs),('broken.json',witness)]: (OUT/name).write_text(json.dumps(obj,indent=2)+'\n')
    text=io.StringIO();writer=csv.writer(text);writer.writerow(['A','partner_when_A_proposes','partner_when_B_proposes','A_rank_when_A_proposes','A_rank_when_B_proposes'])
    for a in range(8):writer.writerow([a+1,first[a]+1,second[a]+1,problem['A'][a].index(first[a])+1,problem['A'][a].index(second[a])+1])
    (OUT/'pairs.csv').write_text(text.getvalue())
    font=ImageFont.load_default(size=21);small=ImageFont.load_default(size=15);frames=[];length=max(len(x['events']) for x in logs.values())
    for step in range(length+1):
        im=Image.new('RGB',(920,620),'#201e30');d=ImageDraw.Draw(im);d.text((27,20),'SAME PREFERENCES / TWO STABLE ANSWERS',font=font,fill='#f4e7d2');d.text((27,56),'8 + 8 participants | 40,320 assignments | exactly 5 stable',font=small,fill='#d1bfd7')
        for panel,side in enumerate(['A','B']):
            ox=panel*460;events=logs[side]['events'];index=min(step,len(events));assignment=events[index-1]['assignment'] if index else [-1]*8;color='#a8dfc9' if side=='A' else '#f1b797'
            d.text((ox+28,98),f'{side} PROPOSES / {index} of {len(events)}',font=font,fill=color)
            for a,b in enumerate(assignment):
                if b>=0:d.line((ox+80,156+a*44,ox+377,156+b*44),fill=color,width=3)
            if index:
                e=events[index-1];a=e['proposer'] if side=='A' else e['receiver'];b=e['receiver'] if side=='A' else e['proposer'];d.line((ox+80,156+a*44,ox+377,156+b*44),fill='#ffd479' if e['accepted'] else '#ed92ad',width=5)
            for i in range(8):
                for x,label in [(ox+32,'A'),(ox+377,'B')]:
                    y=140+i*44;d.rounded_rectangle((x,y,x+47,y+32),6,fill='#514462');d.text((x+7,y+4),label+str(i+1),font=font,fill='#f4e7d2')
            if all(b>=0 for b in assignment):
                sa=sum(problem['A'][a].index(b)+1 for a,b in enumerate(assignment));sb=sum(problem['B'][b].index(a)+1 for a,b in enumerate(assignment));d.text((ox+28,514),'STABLE / 0 BLOCKING PAIRS',font=small,fill=color);d.text((ox+28,543),f'Rank sums: A = {sa}, B = {sb}',font=small,fill='#d1bfd7')
            else:d.text((ox+28,514),'PARTIAL / ACCEPTANCES ARE TENTATIVE',font=small,fill='#d1bfd7')
        d.text((27,588),'7 of 8 partners change. Proposer-optimal means: among stable assignments, for each proposer.',font=small,fill='#f4e7d2');frames.append(im)
    frames[-1].save(OUT/'proof.png');frames[0].save(OUT/'proposals.gif',save_all=True,append_images=frames[1:],duration=[900]+[600]*(len(frames)-2)+[2500],loop=0,optimize=False)
    data={'problem':problem,'logs':logs,'certificate':certificate};html=Path(__file__).with_name('bench-template.html').read_text().replace('__DATA__',json.dumps(data,separators=(',',':')));(OUT/'matching.html').write_text(html)
    with zipfile.ZipFile(OUT/'bench.zip','w',zipfile.ZIP_DEFLATED) as z:
        for name in ['matching.html','problem.json','certificate.json','audit.json','events.json','broken.json','pairs.csv','verify.py','solve.py']:
            contents=Path(__file__).with_name(name).read_bytes() if name.endswith('.py') else (OUT/name).read_bytes();info=zipfile.ZipInfo(name,date_time=(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,contents)
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
