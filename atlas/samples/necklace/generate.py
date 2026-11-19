"""Own deterministic illustrations and offline package for B(2,5)."""
import csv,io,json,zipfile,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from construct import construct
from verify import verify
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'assets/necklace'
def main():
 OUT.mkdir(exist_ok=True,parents=True);s=construct();cert={'format':'binary-necklace-v1','order':5,'bits':s};result=verify(cert)
 for name,obj in [('certificate.json',cert),('audit.json',result)]: (OUT/name).write_text(json.dumps(obj,indent=2)+'\n')
 text=io.StringIO();w=csv.writer(text);w.writerow(['word','position']);w.writerows(result['positions'].items());(OUT/'words.csv').write_text(text.getvalue())
 (OUT/'necklace.html').write_text(Path(__file__).with_name('bench-template.html').read_text().replace('__BITS__',json.dumps(s)))
 font=ImageFont.load_default(size=23);small=ImageFont.load_default(size=16);big=ImageFont.load_default(size=42);frames=[]
 for pos in range(32):
  im=Image.new('RGB',(1000,660),'#172b34');d=ImageDraw.Draw(im);d.text((25,20),'32 LIGHTS / EVERY FIVE-BIT WORD',font=font,fill='#f7ead3');d.text((25,58),'Read clockwise. Neighbouring words share four bits.',font=small,fill='#c0d1c9')
  for i,bit in enumerate(s):
   a=2*math.pi*i/32-math.pi/2;x=300+204*math.cos(a);y=354+204*math.sin(a);selected=(i-pos)%32<5;d.ellipse((x-16,y-16,x+16,y+16),fill='#f4d2a1' if bit=='1' else '#35525e',outline='#f1a451' if selected else '#95afb2',width=4 if selected else 1);d.text((x,y),bit,font=small,anchor='mm',fill='#172b34' if bit=='1' else '#f7ead3')
  word=''.join(s[(pos+j)%32] for j in range(5));d.text((300,342),word,font=big,anchor='mm',fill='#f1b573');d.text((300,390),f'start {pos:02d} / clockwise',anchor='mm',font=small,fill='#c0d1c9');d.text((605,112),'32 words / 32 windows',font=font,fill='#b7dec0')
  for i in range(32):
   text=f'{i:05b}';x=610+(i%4)*90;y=165+(i//4)*45
   if text==word:d.rounded_rectangle((x-5,y-6,x+79,y+28),5,fill='#eeb36d')
   d.text((x,y),text,font=small,fill='#172b34' if text==word else '#c0d1c9')
  d.text((605,550),'Across the seam: wrap to bit 0.',font=small,fill='#f7ead3');d.text((25,620),'Optimal cyclic length: 32. Linear version: 36 bits, including the repeated 4-bit seam.',font=small,fill='#c0d1c9');frames.append(im)
 frames[29].save(OUT/'proof.png');frames[0].save(OUT/'scan.gif',save_all=True,append_images=frames[1:],duration=350,loop=0,optimize=False)
 # Four rows of eight 10 mm cells; assemble in numbered order into one strip, then join ends.
 svg=['<svg xmlns="http://www.w3.org/2000/svg" width="210mm" height="297mm" viewBox="0 0 210 297"><rect width="210" height="297" fill="white"/><g font-family="sans-serif"><text x="20" y="20" font-size="6">32 LIGHTS / PAPER LOOP</text><text x="20" y="32" font-size="3.7">A4, print 100%. Cells: 10 mm. Read in arrow direction.</text>']
 for row in range(4):
  y=50+row*35;svg.append(f'<text x="20" y="{y-4}" font-size="4">Strip {row+1} / positions {row*8}..{row*8+7} / read right</text>')
  for j in range(8):
   i=row*8+j;x=20+j*10;svg.append(f'<rect x="{x}" y="{y}" width="10" height="10" fill="'+('#ead6b3' if s[i]=='1' else '#36535f')+f'" stroke="black" stroke-width=".2"/><text x="{x+5}" y="{y+7}" text-anchor="middle" font-size="5" fill="'+('black' if s[i]=='1' else 'white')+f'">{s[i]}</text>')
  svg.append(f'<rect x="100" y="{y}" width="10" height="10" fill="none" stroke="black" stroke-dasharray="1 1" stroke-width=".2"/><text x="101" y="{y+6}" font-size="2.7">TAPE</text>')
 svg.append('<text x="20" y="210" font-size="4">Cut the 4 strips including their tape tabs.</text><text x="20" y="220" font-size="4">Join 1 to 2 to 3 to 4 to 1. Tabs go UNDER the next strip.</text><text x="20" y="230" font-size="4">Do not count a tape tab as a bit. Read 5 consecutive cells.</text><text x="20" y="247" font-size="4">A 50 mm window selects exactly five cells.</text><rect x="20" y="255" width="50" height="10" fill="none" stroke="black" stroke-width=".2"/><text x="20" y="278" font-size="3.5">Optional: cut a matching window in separate scrap paper.</text></g></svg>');(OUT/'loop-a4.svg').write_text(''.join(svg)+'\n')
 with zipfile.ZipFile(OUT/'bench.zip','w',zipfile.ZIP_DEFLATED) as z:
  for name in ['necklace.html','certificate.json','audit.json','words.csv','loop-a4.svg','verify.py','construct.py']:
   data=Path(__file__).with_name(name).read_bytes() if name.endswith('.py') else (OUT/name).read_bytes();info=zipfile.ZipInfo(name,date_time=(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,data)
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
