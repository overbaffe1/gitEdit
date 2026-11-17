"""Draw the gallery's short calendar animation from snake-weeks.csv.
Requires Pillow 10+ and DejaVu Sans fonts; no API token, network or workflow.
"""
import csv
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parents[1] / 'assets'
with (HERE/'snake-weeks.csv').open() as f:
    counts = [int(r['commits']) for r in csv.DictReader(f)]
assert len(counts) == 16*7
bg, ink, quiet = '#1c2836', '#f9ecda', '#bfcfce'
levels = ('#344451','#577c83','#78a996','#abd69e','#ffd194')
canvas = Image.new('RGB',(552,216),bg); d = ImageDraw.Draw(canvas)
font = lambda sz: ImageFont.truetype('DejaVuSansMono.ttf',sz)
def text(x,y,s,sz,c=ink): d.text((x,y),s,font=font(sz),fill=c,anchor='lt')
text(20,15,'LAZYGIT   /   16 НЕДЕЛЬ',16); d.line((20,42,531,42),fill='#586777')
text(393,62,'КОММИТЫ',14,quiet);text(389,84,str(sum(counts)),38);text(393,151,'ЯНВ—АПР',14,quiet);text(393,173,'2025',20)
# Seven rows, Monday first. Week 0 is at the left. Keep darker tracks on eaten cells.
side=18
def box(week,day):
    x=22+week*21; y=55+day*21; return (x,y,x+side-1,y+side-1)
for i,n in enumerate(counts):
    level = sum(n>=cut for cut in (1,3,7,15))
    d.rounded_rectangle(box(i//7,i%7),radius=4,fill=levels[level]);
path=[(x,y) for x in range(16) for y in (range(7) if not x%2 else reversed(range(7)))]
frames=[]; durations=[]
for i, square in enumerate(path):
    d.rounded_rectangle(box(*square),radius=4,fill='#2b3946')
    frame=canvas.copy(); pen=ImageDraw.Draw(frame)
    for j in range(max(0,i-4),i+1):
        pos=box(*path[j]); pen.rounded_rectangle(pos,radius=6,fill=('#d29da6' if j<i else '#ffb494'))
    x,y,_,_=box(*square);pen.rectangle((x+4,y+5,x+6,y+7),fill=bg);pen.rectangle((x+11,y+5,x+13,y+7),fill=bg)
    if i==4: frame.save(ASSETS/'snake-weeks.png',optimize=True)
    if i>=4: frames.append(frame);durations.append(880 if i==4 else 65 if i<len(path)-1 else 460)
frames[0].save(ASSETS/'snake-weeks.gif',save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=1,optimize=True)
