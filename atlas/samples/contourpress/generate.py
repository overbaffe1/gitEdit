"""Original contour poster. Marching triangles on a fixed synthetic scalar grid."""
from pathlib import Path
from functools import lru_cache
import math,json,hashlib,html,csv,io
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'assets/contourpress'
NX,NY=140,112
LEVELS=[i*.06 for i in range(1,19)]
BG='#152c32';INK='#f0edda';LINE='#c8efa3';MUTED='#a5b8b3'
def field(x,y):
 return 1.1*math.exp(-((x+.8)**2/1.1+(y-.35)**2/1.7))+.86*math.exp(-((x-1)**2/.8+(y+.25)**2/.7))+.25*math.exp(-((x-.1)**2/3+(y+1.2)**2/.25))
@lru_cache(maxsize=1)
def grid():
 return [(x,y,field(x,y)) for j in range(NY+1) for i in range(NX+1) for x,y in [(-3.5+i*7/NX,-2.8+j*5.6/NY)]]
def triangles():
 for j in range(NY):
  for i in range(NX):
   a=j*(NX+1)+i;b=a+1;c=a+NX+1;d=c+1
   yield a,b,d;yield a,d,c

def crossing(a,b,level):
 p,q=grid()[a],grid()[b]
 t=(level-p[2])/(q[2]-p[2])
 return p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])
@lru_cache(maxsize=32)
def contours(level):
 # Keys are original grid-edge vertex pairs: stitching never relies on rounded coordinates.
 points={};adj={}
 for tri in triangles():
  hits=[]
  for a,b in zip(tri,tri[1:]+tri[:1]):
   za,zb=grid()[a][2],grid()[b][2]
   if (za<level)==(zb<level):continue
   key=tuple(sorted((a,b)));points.setdefault(key,crossing(*key,level));hits.append(key)
  if len(hits)==2:
   a,b=hits;adj.setdefault(a,[]).append(b);adj.setdefault(b,[]).append(a)
  elif hits:raise ValueError('Unexpected contour degeneracy')
 if any(len(n)!=2 for n in adj.values()):raise ValueError('Expected closed non-branching contours')
 unseen=set(adj);chains=[]
 while unseen:
  start=min(unseen);cur=start;prev=None;keys=[]
  while True:
   keys.append(cur);unseen.remove(cur)
   nxt=next(n for n in adj[cur] if n!=prev)
   prev,cur=cur,nxt
   if cur==start:break
  chains.append([points[k] for k in keys]+[points[start]])
 return chains

def text(x,y,s,size=20,color=INK,extra=''):
 return f'<text x="{x}" y="{y}" fill="{color}" font-family="DejaVu Sans,Arial,sans-serif" font-size="{size}" {extra}>{html.escape(s)}</text>'
def begin(w,h,title,desc):
 return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',f'<title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(desc)}</desc>',f'<rect width="{w}" height="{h}" fill="{BG}"/>']
def map_art(x,y,w):
 h=w*.8;a=[]
 for i in range(8):
  xx=x+i*w/7;a.append(f'<path d="M{xx:.2f} {y}V{y+h:.2f}" stroke="#294248" stroke-width=".7"/>')
 for j in range(7):
  yy=y+j*h/6;a.append(f'<path d="M{x} {yy:.2f}H{x+w:.2f}" stroke="#294248" stroke-width=".7"/>')
 for k,level in enumerate(LEVELS):
  for chain in contours(level):
   d='M'+'L'.join(f'{x+(px+3.5)/7*w:.2f} {y+(2.8-py)/5.6*h:.2f}' for px,py in chain)+'Z'
   major=(k+1)%3==0
   a.append(f'<path data-level="{level:.2f}" d="{d}" fill="none" stroke="{LINE}" stroke-width="{1.8 if major else .85}" opacity="{1 if major else .68}"/>')
 yy=y+h/2
 a.append(f'<path d="M{x+20} {yy:.2f}H{x+w-20:.2f}" stroke="{INK}" stroke-width="1" stroke-dasharray="8 9"/>')
 a.append(text(x+4,yy-12,'A',18));a.append(text(x+w-24,yy-12,'A′',18))
 return ''.join(a)
def hero(mobile=False):
 w,h=(720,1100) if mobile else (1440,1180)
 a=begin(w,h,'Тишина в линиях','Топографический плакат: светло-зелёные линии равных значений на тёмном фоне, два холма и небольшая гряда. Синтетическая поверхность, не реальные географические данные.')
 a.append(text(36 if mobile else 60,57,'БЮРО / АТЛАС НЕСУЩЕСТВУЮЩЕГО',16 if mobile else 19))
 a.append(text(w-145,57,'ЛИСТ 07',16 if mobile else 19))
 a.append(text(36 if mobile else 60,155,'ТИШИНА',80 if mobile else 114,extra='font-weight="700"'))
 a.append(text(36 if mobile else 60,242 if mobile else 274,'В ЛИНИЯХ',78 if mobile else 114,extra='font-weight="700"'))
 if mobile:
  a.append(map_art(24,300,672))
  a.append(text(36,886,'Вымышленный рельеф.',29,extra='font-weight="700"'))
  a.append(text(36,934,'18 уровней / шаг 0,06 / без единиц высоты',22,MUTED))
  a.append(text(36,978,'A — A′: разрез по горизонтали y = 0',22,MUTED))
  a.append(text(36,1052,'НЕ КАРТА МЕСТНОСТИ / СОБСТВЕННОЕ ПОЛЕ',17))
 else:
  a.append(map_art(340,304,1040))
  a.append(text(60,478,'ВЫМЫШЛЕННЫЙ',21,extra='font-weight="700"'));a.append(text(60,512,'РЕЛЬЕФ',21,extra='font-weight="700"'))
  a.append(text(60,608,'18 уровней',23));a.append(text(60,650,'Шаг 0,06',23));a.append(text(60,692,'Высоты без единиц',20,MUTED))
  a.append(text(60,862,'A — A′',27));a.append(text(60,902,'Разрез: y = 0',20,MUTED))
  a.append(text(60,1136,'НЕ КАРТА МЕСТНОСТИ / НЕ ДАННЫЕ СЪЁМКИ',19))
 a.append('</svg>');return '\n'.join(a)+'\n'
def section_points():return [(x,z) for x,y,z in grid() if abs(y)<1e-12]
def profile(mobile=False):
 w,h=(720,620) if mobile else (1440,520)
 a=begin(w,h,'Разрез A — A′','График высоты той же сетки вдоль y=0, слева направо. Горизонтальный и вертикальный масштабы выбраны отдельно для чтения; единицы условные.')
 a.append(text(36,64,'ЧЕРЕЗ ДВА ХОЛМА',32 if mobile else 46,extra='font-weight="700"'))
 a.append(text(36,110,'A — A′ / тот же рельеф при y = 0',21 if mobile else 24,MUTED))
 x0=56;ww=w-112;ybase=h-116;hh=h-280
 for i in range(4):
  yy=ybase-i*.4/1.2*hh;a.append(f'<path d="M{x0} {yy:.2f}H{w-56}" stroke="#365056"/>');a.append(text(12,yy+5,f'{i*.4:.1f}',14,MUTED))
 points=[(x0+(x+3.5)/7*ww,ybase-z/1.2*hh) for x,z in section_points()]
 d='M'+'L'.join(f'{x:.2f} {y:.2f}' for x,y in points)
 a.append(f'<path d="{d}L{w-56} {ybase}H{x0}Z" fill="{LINE}" opacity=".12"/>')
 a.append(f'<path d="{d}" fill="none" stroke="{LINE}" stroke-width="3"/>')
 a.append(text(56,ybase+34,'A / x = −3,5',18));a.append(text(w-202,ybase+34,'A′ / x = 3,5',18))
 a.append(text(36,h-30,'Масштабы по x и z различаются. Значения условные.',18 if mobile else 22,MUTED))
 a.append('</svg>');return '\n'.join(a)+'\n'
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 for name,data in [('hero.svg',hero()),('hero-mobile.svg',hero(True)),('profile.svg',profile()),('profile-mobile.svg',profile(True))]: (OUT/name).write_text(data)
 a=begin(1400,1120,'Синтетическое поле — контуры','Те же 18 уровней и линия разреза, без плакатной типографики.');a.append(map_art(20,16,1360));a.append('</svg>');(OUT/'contours.svg').write_text('\n'.join(a)+'\n')
 rows=io.StringIO(newline='');writer=csv.writer(rows,lineterminator='\n');writer.writerow(['x','y','z'])
 for x,z in section_points():writer.writerow([f'{x:.8f}','0',f'{z:.12f}'])
 (OUT/'profile.csv').write_text(rows.getvalue())
 audit={'grid':[NX+1,NY+1],'triangles':NX*NY*2,'domain':[-3.5,3.5,-2.8,2.8],'section_y':0,'section_samples':len(section_points()),'units':'arbitrary; no CRS or real-world location','algorithm':'marching triangles; fixed diagonal a-d; linear interpolation on edges','levels':[{'value':round(level,2),'closed_chains':len(contours(level)),'vertices':sum(len(c)-1 for c in contours(level))} for level in LEVELS],'section_note':'Samples of the same grid row. Separate screen scales along x and z.'}
 (OUT/'audit.json').write_text(json.dumps(audit,indent=2)+'\n')
 m={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.iterdir()) if p.suffix in ['.svg','.json','.csv'] and p.name!='manifest.json'}
 (OUT/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 block='''## Тишина в линиях

<a href="atlas/contourpress.md"><picture>
  <source media="(max-width: 640px)" srcset="assets/contourpress/hero-mobile.svg">
  <img src="assets/contourpress/hero.svg" width="1440" alt="Тишина в линиях: тёмный топографический плакат со светло-зелёными контурами двух холмов и небольшой гряды. Собственная синтетическая поверхность, не реальные геоданные.">
</picture></a>

<picture>
  <source media="(max-width: 640px)" srcset="assets/contourpress/profile-mobile.svg">
  <img src="assets/contourpress/profile.svg" width="1440" alt="Разрез A — A′ вдоль y=0 той же сетки: линия проходит через два холма. Масштабы по горизонтали и вертикали различаются; высоты в условных единицах.">
</picture>

**Рельеф, которого нет на карте.** Восемнадцать уровней одного собственного поля; каждая третья линия толще. Пунктир A — A′ на плакате соответствует разрезу ниже. Это не местность, не результаты съёмки и не навигационная карта.

[Контуры крупно, без заголовка](assets/contourpress/contours.svg) · [Разрез CSV](assets/contourpress/profile.csv) · [Параметры и число контуров](assets/contourpress/audit.json) · [Алгоритм, оформление и исследованные README](atlas/contourpress.md). Для телефона подготовлены отдельные композиции; никакие картографические сервисы не вызываются.

'''
 (Path(__file__).parent/'readme-block.md').write_text(block)
 pictures=block[block.index('<a '):block.index('\n**')].replace('assets/contourpress/','').replace('atlas/contourpress.md','../../atlas/contourpress.md')
 (OUT/'proof.html').write_text('<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Тишина в линиях — проверка</title><style>body{max-width:1100px;margin:16px auto;padding:0 16px;font:18px/1.6 sans-serif}img{max-width:100%;height:auto}a{color:#265f88}@media(prefers-color-scheme:dark){body{background:#101e2a;color:#f0edda}a{color:#9ecafa}}</style>'+pictures+'<p><a href="contours.svg">Контуры</a> · <a href="profile.csv">Разрез CSV</a></p></html>')
if __name__=='__main__':main()
