"""Own balance-scale illustrations, printable plan and deterministic archive."""
import csv,io,json,zipfile
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from construct import construct
from verify import verify,thirteen_bound
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'assets/coins'
def main():
 OUT.mkdir(parents=True,exist_ok=True);plan=construct();audit=verify(plan);bound=thirteen_bound();assert not any(r['both_branches_fit'] for r in bound)
 for name,obj in [('plan.json',plan),('audit.json',audit),('thirteen.json',bound)]: (OUT/name).write_text(json.dumps(obj,indent=2)+'\n')
 text=io.StringIO();w=csv.writer(text);w.writerow(['coin','kind','weighing_1','weighing_2','weighing_3']);w.writerows([c['coin'],c['kind'],*c['outcomes']] for c in plan['cases']);(OUT/'cases.csv').write_text(text.getvalue())
 (OUT/'coins.html').write_text(Path(__file__).with_name('bench-template.html').read_text().replace('__PLAN__',json.dumps(plan,separators=(',',':'))))
 f=ImageFont.load_default(size=24);small=ImageFont.load_default(size=17);big=ImageFont.load_default(size=30);frames=[]
 for kind in ['heavy','light']:
  case=next(c for c in plan['cases'] if c['coin']==7 and c['kind']==kind)
  for step in range(4):
   row=plan['rows'][max(0,step-1)];outcome=case['outcomes'][step-1] if step else 0;tilt=outcome*25;trace=case['outcomes'][:step];possible=[c for c in plan['cases'] if c['outcomes'][:step]==trace];im=Image.new('RGB',(1000,660),'#263039');d=ImageDraw.Draw(im);d.text((28,20),'TWELVE COINS / THREE WEIGHINGS',font=f,fill='#f3e7ca');d.text((28,64),'Exactly one odd coin. It may be heavier OR lighter. No external reference.',font=small,fill='#c5cabb');d.text((28,111),f'Weighing {step} of 3 / compatible hypotheses: {len(possible)}',font=f,fill='#c2dbb0')
   d.line((500,220,500,475),fill='#c5cabb',width=7);d.line((430,480,570,480),fill='#c5cabb',width=7);d.line((170,220+tilt,830,220-tilt),fill='#c5cabb',width=7)
   for side,x,y in [(1,210,320+tilt),(-1,790,320-tilt)]:
    d.line((x-90,y,x+90,y),fill='#c5cabb',width=4);d.line((x-90,y,x-40,y-100),fill='#c5cabb',width=3);d.line((x+90,y,x+40,y-100),fill='#c5cabb',width=3)
    for i,coin in enumerate(j+1 for j,v in enumerate(row) if v==side):
     xx=x-63+i*42;d.ellipse((xx-18,y-43,xx+18,y-7),fill='#dbbd79');d.text((xx,y-25),str(coin),font=small,anchor='mm',fill='#263039')
   symbols={1:'L',-1:'R',0:'='};d.text((500,370),' '.join(symbols[t] for t in trace) or 'NO RESULTS YET',font=big,anchor='mm',fill='#e9b86c');d.text((500,415),'Off scale: '+', '.join(str(j+1) for j,v in enumerate(row) if not v),font=small,anchor='mm',fill='#c5cabb')
   d.text((28,516),f'Identified: coin 7, {kind}.' if len(possible)==1 else 'Do not guess: several cases still fit the observed prefix.',font=f,fill='#c2dbb0');d.text((28,567),'L = left heavier / R = right heavier / = balanced',font=small,fill='#f3e7ca');d.text((28,607),'24 cases independently checked. Each weighing: four coins against four.',font=small,fill='#c5cabb');d.text((28,635),'Thirteen coins: 26 hypotheses fit in 27 labels, but no legal first split works.',font=small,fill='#c5cabb');frames.append(im)
 frames[3].save(OUT/'proof.png');frames[0].save(OUT/'weigh.gif',save_all=True,append_images=frames[1:],duration=[1300,1400,1400,2400]*2,loop=0,optimize=False)
 svg=['<svg xmlns="http://www.w3.org/2000/svg" width="210mm" height="297mm" viewBox="0 0 210 297"><rect width="210" height="297" fill="white"/><g font-family="sans-serif" fill="#263039"><text x="18" y="20" font-size="6">TWELVE COINS / THREE WEIGHINGS</text><text x="18" y="32" font-size="3.6">A4, print 100%. Exactly one odd coin: heavy OR light.</text>']
 for i,row in enumerate(plan['rows']):
  left=', '.join(str(k+1) for k,v in enumerate(row) if v==1);right=', '.join(str(k+1) for k,v in enumerate(row) if v==-1);svg.append(f'<text x="18" y="{50+i*17}" font-size="4.5">{i+1}. LEFT: {left} / RIGHT: {right}</text>')
 svg.append('<text x="18" y="108" font-size="3.6">Record L (left heavier), R (right heavier), = (balanced).</text><text x="18" y="118" font-size="3.6">Then find the three-result trace below. Do not change the plan.</text>')
 for j,c in enumerate(plan['cases']):
  x=18+(j//12)*92;y=135+(j%12)*10;trace=' '.join({1:'L',-1:'R',0:'='}[v] for v in c['outcomes']);svg.append(f'<text x="{x}" y="{y}" font-size="4">{trace} : coin {c["coin"]}, {c["kind"]}</text>')
 svg.append('<text x="18" y="270" font-size="3.5">Other traces: incompatible with this exact one-odd-coin model.</text><text x="18" y="280" font-size="3.5">Paper labels are not weights. A physical trial needs suitable scales.</text></g></svg>');(OUT/'plan-a4.svg').write_text(''.join(svg)+'\n')
 with zipfile.ZipFile(OUT/'bench.zip','w',zipfile.ZIP_DEFLATED) as z:
  for name in ['coins.html','plan.json','audit.json','thirteen.json','cases.csv','plan-a4.svg','verify.py','construct.py']:
   data=Path(__file__).with_name(name).read_bytes() if name.endswith('.py') else (OUT/name).read_bytes();info=zipfile.ZipInfo(name,date_time=(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,data)
 print(json.dumps(audit,indent=2))
if __name__=='__main__':main()
