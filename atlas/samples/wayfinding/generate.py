"""Deterministic, dependency-free editorial route map. Never edits README."""
from pathlib import Path
import json, hashlib, html
ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'assets/wayfinding'
ROUTES = [
 ('A', 'Линия света', '#ec7654', [('01','Гравюра','printroom'),('02','Розетки','afterlight'),('03','Нитяная луна','threadmoon')]),
 ('B', 'Линия объёма', '#5689c4', [('04','Стереограмма','stereogram'),('05','Бумажный кристалл','relief'),('06','Материальная проба','materials')]),
 ('C', 'Линия движения', '#b49b56', [('07','Пара Туси','rolling'),('08','Ночной тираж','pressroom'),('09','Код Грея','gray')]),
]
def svg(mobile=False, dark=False):
 w,h = (720,1700) if mobile else (1440,1020)
 bg,ink,muted,grid = ('#101e2a','#f4e8ce','#b7c4c9','#263745') if dark else ('#f3eddf','#162c3b','#52626a','#dad5c8')
 a=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">', '<title id="title">Карта ночного бюро</title>', '<desc id="desc">Три независимых маршрута, девять экспонатов. A: гравюра, розетки, нитяная луна. B: стереограмма, бумажный кристалл, материальная проба. C: пара Туси, ночной тираж, код Грея. Ссылки находятся под картой.</desc>',f'<rect width="{w}" height="{h}" fill="{bg}"/>']
 def line(x1,y1,x2,y2,c=grid,sw=1): a.append(f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{c}" stroke-width="{sw}" fill="none"/>')
 def text(x,y,s,size=20,c=ink,weight=400): a.append(f'<text x="{x}" y="{y}" fill="{c}" font-family="DejaVu Sans,Arial,sans-serif" font-size="{size}" font-weight="{weight}">{html.escape(s)}</text>')
 for x in range(40,w,40): line(x,280,x,h-90)
 for y in range(280,h-89,40): line(40,y,w-40,y)
 text(40,56,'БЮРО / ПУТЕВОДИТЕЛЬ',18,muted)
 text(w-160,56,'ЛИСТ 04',18,muted)
 line(40,78,w-40,78,ink)
 text(40,157,'КАРТА',76 if mobile else 88,weight=700)
 text(40,237,'НОЧНОГО БЮРО',61 if mobile else 88,weight=700)
 if mobile:
  for ri,(code,name,color,stops) in enumerate(ROUTES):
   top=320+ri*420
   text(48,top,code+' / '+name.upper(),25,ink,700)
   a.append(f'<path d="M92 {top+56}V{top+312}" stroke="{color}" stroke-width="10" fill="none"/>')
   for j,(num,label,slug) in enumerate(stops):
    y=top+62+j*120
    a.append(f'<circle cx="92" cy="{y}" r="16" fill="{bg}" stroke="{ink}" stroke-width="3"/>')
    text(133,y-7,num,17,muted)
    text(133,y+28,label,29,ink,700)
 else:
  for ri,(code,name,color,stops) in enumerate(ROUTES):
   y=390+ri*200
   text(48,y-45,code,48,color,700)
   text(48,y-15,name,18,muted)
   a.append(f'<path d="M260 {y}H600L680 {y-80}H1330" stroke="{color}" stroke-width="12" stroke-linejoin="round" stroke-linecap="round" fill="none"/>')
   for j,(num,label,slug) in enumerate(stops):
    x,yy=[(340,y),(820,y-80),(1160,y-80)][j]
    a.append(f'<circle cx="{x}" cy="{yy}" r="17" fill="{bg}" stroke="{ink}" stroke-width="3"/>')
    text(x-15,yy+53,num,18,muted)
    text(x-95,yy+88,label,22,ink,700)
 line(40,h-104,w-40,h-104,ink)
 text(40,h-64,'03 МАРШРУТА / 09 ОСТАНОВОК',19,ink,700)
 text(40,h-30,'Не география. Порядок просмотра — на твой выбор.',16,muted)
 a.append('</svg>')
 return '\n'.join(a)+'\n'
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 for dark in (False,True):
  for mobile in (False,True):
   name='map-'+('dark' if dark else 'light')+('-mobile' if mobile else '')+'.svg'
   (OUT/name).write_text(svg(mobile,dark))
 block='''## Карта ночного бюро

<a href="atlas/wayfinding.md"><picture>
  <source media="(max-width: 640px) and (prefers-color-scheme: dark)" srcset="assets/wayfinding/map-dark-mobile.svg">
  <source media="(max-width: 640px)" srcset="assets/wayfinding/map-light-mobile.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/wayfinding/map-dark.svg">
  <img src="assets/wayfinding/map-light.svg" width="1440" alt="Карта ночного бюро: три линии и девять остановок. Текстовые ссылки на все экспонаты — сразу под картой.">
</picture></a>

Это **схема просмотра, не географическая карта**. Цвет дублируется буквами A/B/C и номерами; станции внутри картинки не кнопки. Открывай экспонаты по ссылкам:

'''
 for code,name,color,stops in ROUTES:
  block+='**'+code+' · '+name+':** '+ ' → '.join(f'[{num} {label}](atlas/{slug}.md)' for num,label,slug in stops)+'.\n\n'
 block+='На телефоне линии становятся вертикальными; для тёмной темы есть отдельная палитра. [Крупная схема](assets/wayfinding/map-light.svg) · [Дизайн, текстовый маршрут и исследование](atlas/wayfinding.md).\n\n'
 (Path(__file__).parent/'readme-block.md').write_text(block)
 (OUT/'routes.json').write_text(json.dumps(ROUTES,ensure_ascii=False,indent=2)+'\n')
 hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.iterdir()) if p.suffix in ('.svg','.json') and p.name!='manifest.json'}
 (OUT/'manifest.json').write_text(json.dumps(hashes,indent=2)+'\n')
 # Only the local proof adds CSS; README uses native GitHub picture and Markdown.
 picture=block[block.index('<a '):block.index('</a>')+4].replace('assets/wayfinding/','').replace('atlas/wayfinding.md','../../atlas/wayfinding.md')
 nav=''.join(f'<p>{code} · {html.escape(name)}: '+ ' → '.join(f'<a href="../../atlas/{slug}.md">{num} {html.escape(label)}</a>' for num,label,slug in stops)+'</p>' for code,name,c,stops in ROUTES)
 (OUT/'proof.html').write_text('<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Карта ночного бюро — проверка</title><style>body{margin:20px auto;max-width:1100px;padding:0 16px;font:18px/1.6 sans-serif;color:#162c3b;background:#fff}img{max-width:100%;height:auto}a{color:#2463a0}@media(prefers-color-scheme:dark){body{color:#f4e8ce;background:#101e2a}a{color:#9ecafa}}</style>'+picture+nav+'</html>')
if __name__=='__main__': main()
