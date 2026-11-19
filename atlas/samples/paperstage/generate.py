"""Deterministic 2.5D paper-theatre illustration; no physical renderer."""
from pathlib import Path
import html,json,hashlib
ROOT=Path(__file__).resolve().parents[3]; OUT=ROOT/'assets/paperstage'
BG='#eee7e2'; INK='#263b49'; COLORS=['#f7e7bb','#e8af8a','#ce7665','#6a929a','#3d657e']; BACK='#213f59'
OUTER='M-240 620V240A240 240 0 0 1 240 240V620Z'
HOLE='M-170 620V240A170 170 0 0 1 170 240V620Z'
FRAME=OUTER+HOLE

def text(x,y,s,size=20,color=INK,extra=''):
 return f'<text x="{x}" y="{y}" fill="{color}" font-family="DejaVu Sans,Arial,sans-serif" font-size="{size}" {extra}>{html.escape(s)}</text>'
def poly(points,color,extra=''):
 return f'<polygon points="{points}" fill="{color}" {extra}/>'
def frame(i,edge=True):
 color=COLORS[i]
 # Offset flat silhouettes suggest a cut edge, not a real extruded mesh.
 return (f'<path d="{FRAME}" transform="translate(7 5)" fill="{INK}" fill-opacity=".26" fill-rule="evenodd"/>' if edge else '')+f'<path d="{FRAME}" fill="{color}" fill-rule="evenodd"/>'
def back():
 return f'<path d="{OUTER}" fill="{BACK}"/><circle cx="-70" cy="330" r="73" fill="#ed9a56"/><circle cx="-93" cy="309" r="6" fill="#f7c58a"/>'
def scene():
 a=[]
 a.append('<ellipse cx="661" cy="928" rx="520" ry="70" fill="#263b49" opacity=".10"/>')
 a.append(poly('140,940 900,940 1160,812 400,812','#d18c7a'))
 a.append(poly('140,940 900,940 900,962 140,962','#bd7367'))
 a.append(poly('900,940 1160,812 1160,834 900,962','#ac695f'))
 a.append('<g transform="translate(610 180)">'+back()+'</g>')
 # Painter order is deliberately explicit: rear to front.
 for i in reversed(range(5)):
  a.append(f'<g data-layer="{i+1}" transform="translate({450+i*32} {300-i*24})">'+frame(i)+'</g>')
 # Steps are drawn front-to-back as a stylised raised path, not a collision-tested construction.
 for i in reversed(range(7)):
  x=410+i*19;y=945-i*26
  a.append(poly(f'{x},{y} {x+116},{y} {x+135},{y-10} {x+19},{y-10}','#f5d59c'))
  a.append(poly(f'{x},{y} {x+116},{y} {x+116},{y+14} {x},{y+14}','#d49b71'))
  a.append(poly(f'{x+116},{y} {x+135},{y-10} {x+135},{y+4} {x+116},{y+14}','#b97c63'))
 return ''.join(a)
def begin(w,h,title,desc):
 return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',f'<title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(desc)}</desc>',f'<rect width="{w}" height="{h}" fill="{BG}"/>']
def hero(mobile=False):
 w,h=(720,1040) if mobile else (1440,1120)
 a=begin(w,h,'Бумажная сцена','Пять цветных арок перед тёмным задником с оранжевым диском. Небольшая лестница ведёт внутрь. Собственная плоская векторная иллюстрация с условной глубиной, не фотография макета.')
 a.append(text(36 if mobile else 60,55,'БЮРО / МАЛЫЙ ТЕАТР',18))
 a.append(text(w-160,55,'ЛИСТ 06',18))
 if mobile:
  a.append(text(36,126,'БУМАЖНАЯ',60,extra='font-weight="700"'))
  a.append(text(36,193,'СЦЕНА',60,extra='font-weight="700"'))
  a.append('<g transform="translate(-30 235) scale(.60)">'+scene()+'</g>')
  a.append(text(36,902,'Пять рам. Один просвет.',29,extra='font-weight="700"'))
  a.append(text(36,945,'Глубина из цвета, сдвига и перекрытий.',21))
  a.append(text(36,994,'ВЕКТОРНАЯ ИЛЛЮСТРАЦИЯ / НЕ ФОТОГРАФИЯ',17))
 else:
  a.append(text(60,165,'БУМАЖНАЯ СЦЕНА',88,extra='font-weight="700"'))
  a.append(scene())
  a.append(text(1030,398,'01—05',34,extra='font-weight="700"'))
  a.append(text(1030,438,'Цветные рамы',22))
  a.append(text(1030,527,'06',34,extra='font-weight="700"'))
  a.append(text(1030,567,'Ночной задник',22))
  a.append(text(1030,679,'Один просвет.',22))
  a.append(text(1030,714,'Пять планов.',22))
  a.append(text(60,1056,'ГЛУБИНА ИЗ ЦВЕТА, СДВИГА И ПЕРЕКРЫТИЙ',19))
  a.append(text(900,1056,'НЕ ФОТОГРАФИЯ / НЕ 3D-МОДЕЛЬ',18))
 a.append('</svg>');return '\n'.join(a)+'\n'
def exploded(mobile=False):
 w,h=(720,1680) if mobile else (1440,800)
 a=begin(w,h,'Сцена по слоям','Те же пять арочных рам и шестой сплошной задник показаны отдельно. Это объяснение композиции, не выкройка и не инструкция по изготовлению.')
 a.append(text(36,64,'СЦЕНА ПО СЛОЯМ',36 if mobile else 46,extra='font-weight="700"'))
 a.append(text(36,108,'Один контур. Пять цветов. Шестой лист — задник.',18 if mobile else 24))
 for i in range(6):
  if mobile:
   x=190+(i%2)*330;y=160+(i//2)*480;scale=.52;labely=y+365
  else:
   x=160+i*222;y=245-i*15;scale=.39;labely=585-i*15
  a.append(f'<g data-layer="{i+1}" transform="translate({x} {y}) scale({scale})">'+(frame(i,False) if i<5 else back())+'</g>')
  a.append(text(x-110 if mobile else x-90,labely,f'{i+1:02} / '+('Задник' if i==5 else 'Рама'),23))
 a.append(text(36,h-46,'Разбор иллюстрации, не шаблон для резки.',18 if mobile else 22))
 a.append('</svg>');return '\n'.join(a)+'\n'
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 for name,data in [('hero.svg',hero()),('hero-mobile.svg',hero(True)),('layers.svg',exploded()),('layers-mobile.svg',exploded(True))]: (OUT/name).write_text(data)
 data={'frames':[{'id':i+1,'color':c,'dx':i*32,'dy':-i*24} for i,c in enumerate(COLORS)],'back':{'id':6,'color':BACK},'outer_path':OUTER,'hole_path':HOLE,'scope':'Screen-space illustration only; not a 3D mesh, physical shadow model or cutting template.'}
 (OUT/'scene.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 m={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.iterdir()) if p.suffix in ['.svg','.json'] and p.name!='manifest.json'}
 (OUT/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 block='''## Бумажная сцена

<a href="atlas/paperstage.md"><picture>
  <source media="(max-width: 640px)" srcset="assets/paperstage/hero-mobile.svg">
  <img src="assets/paperstage/hero.svg" width="1440" alt="Бумажная сцена: пять цветных арочных рам, тёмный задник с оранжевым диском и лестница. Собственная векторная иллюстрация с условной глубиной, не фотография макета.">
</picture></a>

<picture>
  <source media="(max-width: 640px)" srcset="assets/paperstage/layers-mobile.svg">
  <img src="assets/paperstage/layers.svg" width="1440" alt="Сцена разобрана на шесть листов: пять одинаковых арочных рам разных цветов и сплошной задник. На телефоне — сетка из двух колонок и трёх рядов.">
</picture>

**Пять рам. Один просвет.** Глубина возникает из сдвига, цвета и перекрытий — без WebGL, фотографии и настоящей 3D-модели. Нижний рисунок показывает те же контуры отдельно: это разбор иллюстрации, **не выкройка для резки**.

[Сцена крупно](assets/paperstage/hero.svg) · [Разбор по слоям](assets/paperstage/layers.svg) · [Параметры сцены JSON](assets/paperstage/scene.json) · [Как нарисовано и какие README исследованы](atlas/paperstage.md). На телефоне — отдельные композиции; цвет бумаги одинаков в обеих темах.

'''
 (Path(__file__).parent/'readme-block.md').write_text(block)
 pictures=block[block.index('<a '):block.index('\n**')].replace('assets/paperstage/','').replace('atlas/paperstage.md','../../atlas/paperstage.md')
 (OUT/'proof.html').write_text('<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Бумажная сцена — проверка</title><style>body{max-width:1100px;margin:16px auto;padding:0 16px;font:18px/1.6 sans-serif}img{max-width:100%;height:auto}a{color:#265f88}@media(prefers-color-scheme:dark){body{background:#14212e;color:#eee7e2}a{color:#9ecafa}}</style>'+pictures+'<p><a href="scene.json">Параметры сцены</a> · <a href="layers.svg">Слои крупно</a></p></html>')
if __name__=='__main__':main()
