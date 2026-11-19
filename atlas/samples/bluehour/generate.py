"""Own botanical-inspired geometry. Static SVG, no external assets or libraries."""
from pathlib import Path
import math,random,html,json,hashlib
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'assets/bluehour'
PAPER='#f2edda'; BLUE='#123e73'; WHITE='#e5eddc'
LABELS=[('01','Перистый ритм','fern'),('02','Веер света','fan'),('03','Созвездие зонтика','umbel')]
def n(v):return f'{v:.2f}'
def pt(p):return ' '.join(n(v) for v in p)
def path(d,fill='none',stroke=WHITE,width=2,extra=''):
 return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'
def leaf(x,y,dx,dy,width):
 length=math.hypot(dx,dy); nx,ny=-dy/length*width,dx/length*width
 return path(f'M{pt((x,y))} Q{pt((x+dx*.42+nx,y+dy*.42+ny))} {pt((x+dx,y+dy))} Q{pt((x+dx*.5-nx,y+dy*.5-ny))} {pt((x,y))}Z',WHITE,'none',0)
def fern():
 a=[path('M-18 560 Q26 280 24 12',width=4)]
 for i in range(1,21):
  t=i/22; x=15+12*math.sin(t*3); y=535-535*t
  length=175*math.sin(math.pi*t)**.8*(1-.30*t)
  for side in [-1,1]:
   dx=side*length;dy=-length*.48
   a.append(path(f'M{pt((x,y))} Q{pt((x+dx*.6,y+dy*.3))} {pt((x+dx,y+dy))}',width=1.6))
   for j in range(1,11):
    u=j/11;px=x+dx*u;py=y+dy*u*u
    ll=length*.27*(1-u)**.65+2
    for s in [-1,1]:a.append(leaf(px,py,side*ll*.6,-ll*s,ll*.14))
 return ''.join(a)
def fan():
 a=[path('M-12 555 Q42 451 0 350',width=4)]
 points=[]
 for i in range(161):
  angle=math.radians(-170+i); r=238+5*math.sin(i*1.6)-43*math.exp(-((i-80)/9)**2)
  points.append((math.cos(angle)*r,350+math.sin(angle)*r))
 a.append(path('M0 350L'+'L'.join(pt(p) for p in points)+'Z',WHITE,'none',0))
 for i in range(3,159,5):
  p=points[i];a.append(path(f'M0 350 Q{pt((p[0]*.6,350+(p[1]-350)*.35))} {pt(p)}',stroke=BLUE,width=1,extra='opacity=".3"'))
 return ''.join(a)
def umbel():
 a=[path('M-28 555 Q-38 400 0 282',width=4)]
 for i in range(15):
  theta=math.radians(-174+i*12);x=math.cos(theta)*156;y=250+math.sin(theta)*170
  a.append(path(f'M0 282 Q{pt((x*.45,y+55))} {pt((x,y))}',width=1.8))
  for j in range(7):
   ang=j*math.tau/7;xx=x+math.cos(ang)*18;yy=y+math.sin(ang)*15
   a.append(path(f'M{pt((x,y))}L{pt((xx,yy))}',width=1))
   a.append(f'<circle cx="{n(xx)}" cy="{n(yy)}" r="4.5" fill="{WHITE}"/>')
 a.append(leaf(-25,440,-83,-57,20));a.append(leaf(-24,410,84,-82,16))
 return ''.join(a)
FORMS={'fern':fern,'fan':fan,'umbel':umbel}
def text(x,y,s,size=20,color=BLUE,family='sans-serif',extra=''):
 return f'<text x="{x}" y="{y}" font-family="DejaVu Sans,{family}" font-size="{size}" fill="{color}" {extra}>{html.escape(s)}</text>'
def begin(w,h,title,desc):
 return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',f'<title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(desc)}</desc>',f'<rect width="{w}" height="{h}" fill="{PAPER}"/>']
def grain(w,h):
 # Seeded sparse flecks, not physical paper/chemical simulation. No filters.
 rng=random.Random(814)
 return ''.join(f'<circle cx="{n(rng.uniform(36,w-36))}" cy="{n(rng.uniform(36,h-36))}" r="{n(rng.uniform(.3,1.3))}" fill="{WHITE}" opacity=".12"/>' for _ in range(950))
def hero(mobile=False):
 w,h=(720,1220) if mobile else (1440,1080)
 a=begin(w,h,'Гербарий синего часа','Светлый перистый силуэт на глубоком синем поле. Авторская векторная стилизация цианотипии, не фотография и не ботанический образец.')
 a+=[f'<rect x="28" y="28" width="{w-56}" height="{h-56}" fill="{BLUE}"/>',grain(w,h)]
 a.append(text(60,78,'БЮРО / АРХИВ СВЕТА',17,WHITE));a.append(text(w-165,78,'ЛИСТ 05',17,WHITE))
 if mobile:
  a.append(text(60,163,'ГЕРБАРИЙ',70,WHITE,extra='font-weight="700"'))
  a.append(text(60,209,'синего часа',40,WHITE,family='serif',extra='font-style="italic"'))
  a.append('<g transform="translate(338 310) rotate(10) scale(1.25)">'+fern()+'</g>')
  a.append(text(60,1090,'01 / ПЕРИСТЫЙ РИТМ',24,WHITE))
  a.append(text(60,1135,'Силуэт, которого не было в природе.',20,WHITE))
  a.append(text(60,1167,'Собственная геометрия / цифровой отпечаток',17,WHITE))
 else:
  a.append('<g transform="translate(396 190) rotate(16) scale(1.24)">'+fern()+'</g>')
  a.append(text(745,295,'ГЕРБАРИЙ',88,WHITE,extra='font-weight="700"'))
  a.append(text(750,366,'синего часа',61,WHITE,family='serif',extra='font-style="italic"'))
  a.append(path('M752 424H1320',stroke=WHITE,width=1))
  a.append(text(752,478,'Сохранить не растение,',27,WHITE));a.append(text(752,518,'а паузу между светом и тенью.',27,WHITE))
  a.append(text(752,680,'01 / ПЕРИСТЫЙ РИТМ',23,WHITE));a.append(text(752,722,'Ритм ветвей. Никакой фотографии.',20,WHITE))
  a.append(text(60,985,'СОБСТВЕННАЯ ГЕОМЕТРИЯ',18,WHITE));a.append(text(880,985,'ЦИФРОВОЙ ОТПЕЧАТОК / НЕ ЦИАНОТИПИЯ',16,WHITE))
 a.append('</svg>');return '\n'.join(a)+'\n'
def contact(mobile=False):
 w,h=(720,2140) if mobile else (1440,880)
 a=begin(w,h,'Три силуэта — один синий','Перистая ветвь, веерный лист и зонтичное соцветие. Условные графические формы, не определитель растений.')
 a.append(text(40,64,'ТРИ СИЛУЭТА / ОДИН СИНИЙ',26,extra='font-weight="700"'))
 for i,(num,label,slug) in enumerate(LABELS):
  x,y,cw,ch=(40,100+i*660,640,560) if mobile else (40+i*465,110,430,610)
  a.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" fill="{BLUE}"/>')
  scale=.82 if mobile else .86
  a.append(f'<g transform="translate({x+cw/2} {y+25}) scale({scale})">'+FORMS[slug]()+'</g>')
  a.append(text(x,y+ch+40,num+' / '+label,25 if mobile else 22))
 a.append(text(40,h-30,'Условные формы. Не ботанический атлас и не химический процесс.',15))
 a.append('</svg>');return '\n'.join(a)+'\n'
def plate(slug):
 a=begin(620,800,dict((s,l) for n,l,s in LABELS)[slug],'Светлая условная растительная форма на синем поле; собственный векторный рисунок.')
 a.append(f'<rect x="24" y="24" width="572" height="692" fill="{BLUE}"/>')
 a.append('<g transform="translate(310 95)">'+FORMS[slug]()+'</g>')
 num,label,_=next(l for l in LABELS if l[2]==slug)
 a.append(text(24,762,num+' / '+label,24));a.append('</svg>');return '\n'.join(a)+'\n'
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 for name,data in [('hero.svg',hero()),('hero-mobile.svg',hero(True)),('contact.svg',contact()),('contact-mobile.svg',contact(True))]+[(s+'.svg',plate(s)) for _,_,s in LABELS]: (OUT/name).write_text(data)
 block='''## Гербарий синего часа

<a href="atlas/bluehour.md"><picture>
  <source media="(max-width: 640px)" srcset="assets/bluehour/hero-mobile.svg">
  <img src="assets/bluehour/hero.svg" width="1440" alt="Гербарий синего часа: светлая перистая ветвь на глубоком синем поле, бумажные поля и крупная музейная типографика. Собственный векторный рисунок, не фотография растения.">
</picture></a>

<a href="assets/bluehour/contact.svg"><picture>
  <source media="(max-width: 640px)" srcset="assets/bluehour/contact-mobile.svg">
  <img src="assets/bluehour/contact.svg" width="1440" alt="Три условных силуэта: 01 — перистая ветвь, 02 — веерный лист, 03 — зонтичное соцветие. На телефоне отпечатки расположены вертикально.">
</picture></a>

**Не растение, а ритм его силуэта.** Собственная геометрия, стилизованная под цианотипный отпечаток: без фотографии, химической симуляции и претензии на ботаническую точность. Синее поле одинаково в обеих темах — как лист бумаги, а не интерфейс.

[01 · Перистый ритм](assets/bluehour/fern.svg) · [02 · Веер света](assets/bluehour/fan.svg) · [03 · Созвездие зонтика](assets/bluehour/umbel.svg) · [Как нарисовано и какие README исследованы](atlas/bluehour.md). Векторные оригиналы можно открыть крупно; скрипты и внешние сервисы для просмотра не нужны.

'''
 (Path(__file__).parent/'readme-block.md').write_text(block)
 manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.glob('*.svg'))}
 (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 body=block[block.index('<a '):block.index('\n**')].replace('assets/bluehour/','').replace('atlas/bluehour.md','../../atlas/bluehour.md')
 nav=' · '.join(f'<a href="{s}.svg">{n} {html.escape(l)}</a>' for n,l,s in LABELS)
 (OUT/'proof.html').write_text('<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Гербарий — проверка</title><style>body{max-width:1100px;margin:16px auto;padding:0 16px;font:18px/1.6 sans-serif}img{max-width:100%;height:auto}a{color:#235e9b}@media(prefers-color-scheme:dark){body{background:#101e2a;color:#f2edda}a{color:#9ecafa}}</style>'+body+'<p>'+nav+'</p></html>')
if __name__=='__main__':main()
