"""Deterministic synthetic Simpson exhibit and finite-grid audit."""
import csv,io,json,zipfile
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from model import construct
from verify import verify
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'assets/simpson'
def main():
 OUT.mkdir(exist_ok=True,parents=True);reversed_count=0;rows=[]
 for a in range(1,10):
  for b in range(1,10):
   c=construct(a,b);r=verify(c);reversed_count+=r['reversal'];rows.append([a,b,*r['aggregate_A'],*r['aggregate_B'],r['total_cross'],int(r['reversal'])])
 assert reversed_count==28
 audit={'compositions':81,'reversed':28,'not_reversed':53,'common_weights_checked':891};(OUT/'audit.json').write_text(json.dumps(audit,indent=2)+'\n')
 for name,a,b in [('reversal',1,9),('equal-mix',5,5),('near',4,5)]: (OUT/(name+'.json')).write_text(json.dumps(construct(a,b),indent=2)+'\n')
 text=io.StringIO();w=csv.writer(text);w.writerow(['A_easy_tenths','B_easy_tenths','A_success','A_total','B_success','B_total','total_cross','reversal']);w.writerows(rows);(OUT/'grid.csv').write_text(text.getvalue())
 (OUT/'simpson.html').write_text(Path(__file__).with_name('bench-template.html').read_text())
 font=ImageFont.load_default(size=24);small=ImageFont.load_default(size=17);big=ImageFont.load_default(size=32);frames=[]
 for a,b in [(5,5),(4,6),(3,7),(2,8),(1,9),(2,8),(3,7),(4,6)]:
  im=Image.new('RGB',(1000,660),'#203238');d=ImageDraw.Draw(im);d.text((28,20),'BETTER IN BOTH GROUPS / WORSE OVERALL',font=font,fill='#f5e9d4');d.text((28,66),'Synthetic tasks. Fixed success rates, changing group composition.',font=small,fill='#c9d5c7')
  for i,(label,e,rate) in enumerate([('A',a,30+6*a),('B',b,20+6*b)]):
   y=140+i*166;easy=e*10;hard=100-easy;d.text((28,y+17),label,font=big,fill='#edcf8d' if not i else '#deb58e');d.rectangle((85,y,85+easy*7,y+45),fill='#a9c8b6');d.rectangle((85+easy*7,y,785,y+45),fill='#8b9fb8');d.text((85,y-27),f'{easy} easy / {hard} hard',font=small,fill='#c9d5c7');d.text((818,y+6),'90% / 30%' if not i else '80% / 20%',font=small,fill='#f5e9d4');d.rectangle((85,y+68,85+rate*7,y+98),fill='#edcf8d' if not i else '#deb58e');d.text((818,y+68),f'{rate}% total',font=small,fill='#f5e9d4')
  A=30+6*a;B=20+6*b;d.text((28,479),f'Overall: A {A}% '+('<' if A<B else '>')+f' B {B}%',font=big,fill='#edcf8d');d.text((28,536),'Equal weights (50% easy / 50% hard): A 60% > B 50%, always.',font=font,fill='#c5dfbd');d.text((28,595),'28 reversals in 81 compositions. Exact counts, no statistical or causal claim.',font=small,fill='#c9d5c7');d.text((28,625),'Group A rates: 90% / 30%. Group B rates: 80% / 20%. Each frame is a synthetic batch.',font=small,fill='#c9d5c7');frames.append(im)
 frames[4].save(OUT/'proof.png');frames[0].save(OUT/'mix.gif',save_all=True,append_images=frames[1:],duration=[1800]+[600]*3+[2400]+[600]*3,loop=0,optimize=False)
 # Exact grid, axes and reversal boundary, readable without colour.
 svg=['<svg xmlns="http://www.w3.org/2000/svg" width="760" height="650" viewBox="0 0 760 650"><rect width="760" height="650" fill="#203238"/><g font-family="sans-serif" fill="#f5e9d4"><text x="28" y="35" font-size="22">81 MIXES / 28 REVERSALS</text><text x="28" y="65" font-size="15">Rows: easy tasks in A. Columns: easy tasks in B. R: aggregate A &lt; B.</text>']
 for a in range(1,10):
  svg.append(f'<text x="45" y="{127+(a-1)*48}" font-size="16">{a*10}</text>')
  for b in range(1,10):
   rev=b-a>=2;x=90+(b-1)*64;y=100+(a-1)*48;svg.append(f'<rect x="{x}" y="{y}" width="59" height="43" fill="'+('#deb58e' if rev else '#a9c8b6')+f'"/><text x="{x+30}" y="{y+28}" text-anchor="middle" fill="#203238" font-size="19">'+('R' if rev else 'A')+'</text>')
 for b in range(1,10):svg.append(f'<text x="{120+(b-1)*64}" y="90" text-anchor="middle" font-size="16">{b*10}</text>')
 svg.append('<text x="28" y="568" font-size="17">Reversal iff B has at least 20 more easy tasks than A.</text><text x="28" y="601" font-size="16">A wins in each group for all 81 mixes. No ties in this grid.</text><text x="28" y="630" font-size="15">Synthetic data. Composition is not a causal conclusion.</text></g></svg>');(OUT/'grid.svg').write_text(''.join(svg)+'\n')
 # Printable paper table, not a causal decision aid.
 paper=['<svg xmlns="http://www.w3.org/2000/svg" width="210mm" height="297mm" viewBox="0 0 210 297"><rect width="210" height="297" fill="white"/><g font-family="sans-serif" fill="#203238"><text x="20" y="22" font-size="6">SAME GROUP RATES / DIFFERENT MIX</text>']
 lines=['Synthetic task outcomes. A4 / print at 100%.','Method A: easy 9 / 10 = 90%; hard 27 / 90 = 30%.','Method B: easy 72 / 90 = 80%; hard 2 / 10 = 20%.','A wins in BOTH groups.','Totals: A 36 / 100 = 36%; B 74 / 100 = 74%.','Why? A gets 90 hard tasks; B gets only 10.','A total = 0.1 x 90% + 0.9 x 30% = 36%.','B total = 0.9 x 80% + 0.1 x 20% = 74%.','Now use equal weights: half easy, half hard.','A standardized = 0.5 x 90% + 0.5 x 30% = 60%.','B standardized = 0.5 x 80% + 0.5 x 20% = 50%.','Standardized rates are NOT new observations.','Neither table alone proves a causal effect.','Try a common easy-task weight w between 0 and 1:','A = 30% + 60w percentage points.','B = 20% + 60w percentage points.','The common-weight gap is always 10 percentage points.']
 for k,line in enumerate(lines):paper.append(f'<text x="20" y="{40+12*k}" font-size="3.7">{line}</text>')
 paper.append('</g></svg>');(OUT/'mix-a4.svg').write_text(''.join(paper)+'\n')
 with zipfile.ZipFile(OUT/'bench.zip','w',zipfile.ZIP_DEFLATED) as z:
  for name in ['simpson.html','reversal.json','equal-mix.json','near.json','audit.json','grid.csv','grid.svg','mix-a4.svg','verify.py','model.py']:
   data=Path(__file__).with_name(name).read_bytes() if name.endswith('.py') else (OUT/name).read_bytes();info=zipfile.ZipInfo(name,date_time=(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,data)
 print(json.dumps(audit,indent=2))
if __name__=='__main__':main()
