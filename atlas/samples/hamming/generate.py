"""Generate own Hamming demo, exhaustive certificates and offline archive."""
from pathlib import Path
from itertools import product
import csv,io,json,zipfile
from PIL import Image,ImageDraw,ImageFont
from codec import encode,decode,certificate
from verify import verify,codebook,distance
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'assets/hamming'
def flip(s,positions):return ''.join(('1' if b=='0' else '0') if i in positions else b for i,b in enumerate(s,1))
def main():
 OUT.mkdir(parents=True,exist_ok=True);book=codebook();assert len(book)==16;mind=min(distance(a,b) for i,a in enumerate(book) for b in book[i+1:]);assert mind==3
 rows=[];counts=[dict(weight=i,cases=0,recovered=0,zero_syndrome=0) for i in range(8)];certs=[]
 for data in map(''.join,product('01',repeat=4)):
  sent=encode(data)
  for mask in range(128):
   positions=[p for p in range(1,8) if mask&(1<<(p-1))];received=flip(sent,positions);c=certificate(data,received);r=verify(c);row=counts[len(positions)];row['cases']+=1;row['recovered']+=r['candidate_equals_sent'];row['zero_syndrome']+=not r['syndrome'];rows.append([data,sent,mask,received,len(positions),c['syndrome'],c['candidate'],int(r['candidate_equals_sent'])])
 examples={name:certificate('1011',flip(encode('1011'),positions)) for name,positions in [('clean',[]),('single',[5]),('double',[3,5]),('undetected',[3,5,6])]}
 for name,c in examples.items():(OUT/(name+'.json')).write_text(json.dumps(c,indent=2)+'\n')
 audit={'checked':len(rows),'codewords':16,'minimum_distance':mind,'recovered':sum(x['recovered'] for x in counts),'single_errors_corrected':counts[1]['recovered'],'double_errors_detected_but_miscorrected':counts[2]['cases'],'byWeight':counts};assert audit['single_errors_corrected']==112;assert counts[2]['zero_syndrome']==counts[2]['recovered']==0
 (OUT/'audit.json').write_text(json.dumps(audit,indent=2)+'\n');text=io.StringIO();w=csv.writer(text);w.writerow(['data','sent','mask','received','errors','syndrome','candidate','recovered']);w.writerows(rows);(OUT/'sweep.csv').write_text(text.getvalue());(OUT/'codebook.json').write_text(json.dumps(book,indent=2)+'\n')
 (OUT/'hamming.html').write_text(Path(__file__).with_name('bench-template.html').read_text())
 f=ImageFont.load_default(size=24);small=ImageFont.load_default(size=17);big=ImageFont.load_default(size=28);frames=[];sent=encode('1011');colours=['#e6ab97','#9dcbbc','#b3afe2'];groups=[[1,3,5,7],[2,3,6,7],[4,5,6,7]]
 stages=[([],False,'CLEAN / 0 ERRORS')]+[([i],False,f'SINGLE ERROR / POSITION {i}') for i in range(1,8)]+[([3,5],False,'TWO ERRORS / POSITIONS 3 AND 5'),([3,5],True,'BLIND CORRECTION / WRONG CODEWORD'),([3,5,6],False,'THREE ERRORS / ZERO SYNDROME')]
 for positions,corrected,title in stages:
  received=flip(sent,positions);out=decode(received);shown=out['candidate'] if corrected else received;checks=[sum(int(shown[p-1]) for p in g)%2 for g in groups];syndrome=checks[0]+2*checks[1]+4*checks[2];im=Image.new('RGB',(1000,660),'#202638');d=ImageDraw.Draw(im);d.text((28,20),'SEVEN LIGHTS / THREE PARITY CHECKS',font=f,fill='#f3e8ce');d.text((28,65),title,font=big,fill='#edbc72');d.text((28,113),f'Data 1011 / sent {sent} / displayed {shown}',font=small,fill='#c7cfcd')
  for i in range(1,8):
   x=185+(i-1)*110;d.text((x,166),str(i),anchor='mm',font=f,fill='#f3e8ce');d.rounded_rectangle((x-29,194,x+29,251),9,fill='#eec98d' if shown[i-1]=='1' else '#35415b',outline='#e6ab97' if shown[i-1]!=sent[i-1] else '#b1b9c1',width=3);d.text((x,222),shown[i-1],anchor='mm',font=big,fill='#202638' if shown[i-1]=='1' else '#f3e8ce')
   for k,g in enumerate(groups):
    y=310+k*66;d.ellipse((x-13,y-13,x+13,y+13),fill=colours[k] if i in g else '#35415b')
  for k in range(3):d.text((28,297+k*66),f'S{1<<k}',font=f,fill=colours[k]);d.text((920,297+k*66),str(checks[k]),font=f,fill=colours[k])
  d.text((28,496),f'Syndrome S4 S2 S1 = {checks[2]}{checks[1]}{checks[0]} = {syndrome}',font=f,fill='#edbc72')
  message='No change suggested.' if not syndrome else f'Decoder would flip position {syndrome}.';d.text((28,540),message,font=f,fill='#f3e8ce');d.text((28,586),'Guarantee: at most ONE error. A valid candidate does not prove recovery.',font=small,fill='#c7cfcd');d.text((28,623),'2048 transmissions checked / 112 single errors corrected / 336 double errors miscorrected',font=small,fill='#c7cfcd');frames.append(im)
 frames[5].save(OUT/'proof.png');frames[0].save(OUT/'checks.gif',save_all=True,append_images=frames[1:],duration=[1400]*8+[2200]*3,loop=0,optimize=False)
 svg=['<svg xmlns="http://www.w3.org/2000/svg" width="210mm" height="297mm" viewBox="0 0 210 297"><rect width="210" height="297" fill="white"/><g font-family="sans-serif" fill="#202638"><text x="20" y="20" font-size="6">HAMMING (7,4) / PARITY CARD</text><text x="20" y="32" font-size="4">Positions go left to right. Even parity. Print A4 at 100%.</text>']
 for i in range(1,8):
  x=40+(i-1)*22;svg.append(f'<text x="{x+8}" y="53" text-anchor="middle" font-size="5">{i}</text><rect x="{x}" y="60" width="16" height="16" fill="none" stroke="#202638" stroke-width=".3"/>')
  for k,g in enumerate(groups):
   if i in g:svg.append(f'<circle cx="{x+8}" cy="{100+k*22}" r="4" fill="{colours[k]}" stroke="#202638" stroke-width=".3"/>')
 for k in range(3):svg.append(f'<text x="20" y="{102+k*22}" font-size="5">S{1<<k}</text>')
 lines=['Data goes into positions 3, 5, 6, 7.','Choose parity bits 1, 2, 4 to make each row even.','Receiver: count the 1 bits in each coloured row.','Odd row: S = 1. Even row: S = 0.','Read syndrome as binary S4 S2 S1.','If at most one error occurred: flip that position.','Syndrome 0: do not flip anything.','Warning: two errors can cause a wrong correction.','This is (7,4), NOT extended (8,4) SECDED.']
 for k,line in enumerate(lines):svg.append(f'<text x="20" y="{177+k*10}" font-size="3.8">{line}</text>')
 svg.append('</g></svg>');(OUT/'parity-a4.svg').write_text(''.join(svg)+'\n')
 with zipfile.ZipFile(OUT/'bench.zip','w',zipfile.ZIP_DEFLATED) as z:
  for name in ['hamming.html','clean.json','single.json','double.json','undetected.json','audit.json','codebook.json','sweep.csv','parity-a4.svg','verify.py','codec.py']:
   data=Path(__file__).with_name(name).read_bytes() if name.endswith('.py') else (OUT/name).read_bytes();info=zipfile.ZipInfo(name,date_time=(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,data)
 print(json.dumps(audit,indent=2))
if __name__=='__main__':main()
