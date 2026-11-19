"""Two original raster revisions for GitHub's real image-diff controls."""
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[3]
def render(revision=2):
 im=Image.new('RGB',(800,480),'#142c36');d=ImageDraw.Draw(im)
 for x in range(0,801,40):d.line((x,0,x,480),fill='#213c45')
 for y in range(0,481,40):d.line((0,y,800,y),fill='#213c45')
 d.rounded_rectangle((80,80,720,400),32,fill='#ede6cd')
 d.ellipse((145,145,335,335),fill='#dd9257' if revision==1 else '#4d8c87')
 shift=0 if revision==1 else 48
 for i in range(4):d.rounded_rectangle((390,145+i*45,620+shift,160+i*45),6,fill='#294956')
 d.text((100,98),'REVISION '+str(revision),fill='#294956',font_size=21)
 return im
if __name__=='__main__':
 import sys
 p=ROOT/'assets/native-lab/revision.png';p.parent.mkdir(parents=True,exist_ok=True);render(int(sys.argv[1]) if len(sys.argv)>1 else 2).save(p,optimize=True)
