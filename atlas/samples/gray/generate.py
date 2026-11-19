"""Own illustrations, exact transition audit and printable reflected Gray disk."""
import csv,io,json,math,zipfile
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from model import construct,gray,decode
from verify import verify
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'assets/gray'
def sample(a,b,mask):return (a&(~mask&63))|(b&mask)
def main():
 OUT.mkdir(parents=True,exist_ok=True);c=construct();audit=verify(c)
 for name,obj in [('certificate.json',c),('audit.json',audit)]: (OUT/name).write_text(json.dumps(obj,indent=2)+'\n')
 text=io.StringIO();w=csv.writer(text);w.writerow(['from','to','binary_changed_bits','gray_changed_bits','binary_readings','gray_readings']);w.writerows([r['from'],r['to'],(r['from']^r['to']).bit_count(),1,len(r['binary_reads']),len(r['gray_reads'])] for r in c['transitions']);(OUT/'transitions.csv').write_text(text.getvalue());(OUT/'gray.html').write_text(Path(__file__).with_name('bench-template.html').read_text())
 f=ImageFont.load_default(size=24);small=ImageFont.load_default(size=17);big=ImageFont.load_default(size=28);frames=[]
 for k in [0,1,2,3,4,5,6,6]:
  mask=(1<<k)-1;b=sample(31,32,mask);g=sample(gray(31),gray(32),mask);im=Image.new('RGB',(1000,660),'#202b3a');d=ImageDraw.Draw(im);d.text((28,20),'ONE STEP / ONE CHANGING BIT',font=f,fill='#f4e9d2');d.text((28,63),'Position 31 -> 32. Each track reads its own old or new bit.',font=small,fill='#bbcbbc')
  for row,(name,values,decoded) in enumerate([('BINARY',[31,b,32],b),('GRAY',[gray(31),g,gray(32)],decode(g))]):
   y=139+row*183;d.text((28,y+26),name,font=f,fill='#f4e9d2')
   for col,value in enumerate(values):
    x=180+col*267;word=f'{value:06b}'
    for bit,ch in enumerate(word):
     xx=x+bit*37;d.rounded_rectangle((xx,y,xx+31,y+48),4,fill='#dfc48a' if ch=='1' else '#3a4b60');d.text((xx+15,y+24),ch,font=small,anchor='mm',fill='#202b3a' if ch=='1' else '#f4e9d2')
    d.text((x,y+63),['OLD','SAMPLED','NEW'][col],font=small,fill='#bbcbbc')
   d.text((180,y+102),f'Sampled position: {decoded}'+(' / NOT an endpoint' if decoded not in [31,32] else ' / endpoint'),font=big,fill='#e9ad9c' if decoded not in [31,32] else '#c2dcb4')
  d.text((28,510),f'{k} of 6 sensors switched to the new side (low bits first).',font=f,fill='#dfc48a');d.text((28,561),'Possible mixed positions for this edge: binary 64 / Gray 2.',font=f,fill='#c2dcb4');d.text((28,606),'64 cyclic edges checked, including 63 -> 0. One adjacent transition only.',font=small,fill='#bbcbbc');d.text((28,635),'Not error correction. Arbitrary bit errors or skipped positions violate the model.',font=small,fill='#bbcbbc');frames.append(im)
 frames[5].save(OUT/'proof.png');frames[0].save(OUT/'scan.gif',save_all=True,append_images=frames[1:-1],duration=[1700]+[650]*5+[2200],loop=0,optimize=False)
 svg=['<svg xmlns="http://www.w3.org/2000/svg" width="210mm" height="297mm" viewBox="0 0 210 297"><rect width="210" height="297" fill="white"/><g font-family="sans-serif" fill="#202b3a"><text x="17" y="17" font-size="6">64 POSITIONS / GRAY DISK</text><text x="17" y="28" font-size="3.7">A4, print 100%. Clockwise. Outside to inside: MSB to LSB.</text>']
 cx,cy=105,130
 for i,word in enumerate(c['words']):
  start=2*math.pi*(i-.5)/64-math.pi/2;end=2*math.pi*(i+.5)/64-math.pi/2
  for bit,ch in enumerate(word):
   outer=88-bit*10;inner=outer-10
   def pt(r,a):return f'{cx+r*math.cos(a):.5f},{cy+r*math.sin(a):.5f}'
   path=f'M {pt(outer,start)} A {outer},{outer} 0 0 1 {pt(outer,end)} L {pt(inner,end)} A {inner},{inner} 0 0 0 {pt(inner,start)} Z';svg.append(f'<path data-position="{i}" data-bit="{bit}" data-value="{ch}" d="{path}" fill="'+('#202b3a' if ch=='1' else 'white')+'"/>')
 for i in range(0,64,8):
  a=2*math.pi*i/64-math.pi/2;svg.append(f'<text x="{cx+94*math.cos(a):.4f}" y="{cy+94*math.sin(a)+1.5:.4f}" text-anchor="middle" font-size="4">{i}</text>')
 svg.append('<circle cx="105" cy="130" r="2" fill="none" stroke="#202b3a" stroke-width=".3"/><text x="105" y="128" text-anchor="middle" font-size="4">6 TRACKS</text><text x="105" y="136" text-anchor="middle" font-size="3.5">black = 1</text><text x="17" y="240" font-size="3.7">Read on a sector centre, not on a boundary. Position 0: top.</text><text x="17" y="251" font-size="3.7">Track radii: 28..88 mm, 10 mm per track. Disk diameter: 176 mm.</text><text x="17" y="262" font-size="3.7">Bits are Gray symbols; decode them, do not read as binary position.</text><text x="17" y="274" font-size="3.7">Teaching diagram only. Not a calibrated physical encoder.</text></g></svg>');(OUT/'disk-a4.svg').write_text(''.join(svg)+'\n')
 with zipfile.ZipFile(OUT/'bench.zip','w',zipfile.ZIP_DEFLATED) as z:
  for name in ['gray.html','certificate.json','audit.json','transitions.csv','disk-a4.svg','verify.py','model.py']:
   data=Path(__file__).with_name(name).read_bytes() if name.endswith('.py') else (OUT/name).read_bytes();info=zipfile.ZipInfo(name,date_time=(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,data)
 print(json.dumps(audit,indent=2))
if __name__=='__main__':main()
