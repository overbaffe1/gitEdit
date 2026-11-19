"""Editorial foyer: original vector compositions with outlined local type, no external assets."""
from pathlib import Path
import math,json,hashlib
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'assets/foyer';FONTS=Path('/usr/share/fonts/truetype/dejavu')
PALETTES={'light':dict(paper='#f1ecdf',ink='#222b2b',blue='#254ddb',orange='#dc542e',muted='#706f63',rule='#c9c5b7',wash='#dbdfb5'), 'dark':dict(paper='#182326',ink='#f1ecdf',blue='#a2b8ff',orange='#ff916d',muted='#b0b8aa',rule='#445151',wash='#354840')}
class SVG:
 def __init__(self,w,h,p,title):
  self.w=w;self.h=h;self.p=p;self.body=[];self.defs={};self.title=title
 def add(self,s):self.body.append(s)
 def rect(self,x,y,w,h,c,extra=''):self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" {extra}/>')
 def line(self,x,y,X,Y,c,width=1):self.add(f'<path d="M{x},{y}L{X},{Y}" fill="none" stroke="{c}" stroke-width="{width}"/>')
 def circle(self,x,y,r,c,stroke='none',width=1):self.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" stroke="{stroke}" stroke-width="{width}"/>')
 def text(self,text,x,y,size,color=None,font='bold',tracking=0):
  f=fontdata(font);scale=size/f['units'];parts=[];offset=0
  for ch in text:
   name=f['cmap'].get(ord(ch),'space');key=font+'_'+name
   if key not in self.defs:
    pen=SVGPathPen(f['glyphs']);f['glyphs'][name].draw(pen);self.defs[key]=pen.getCommands()
   parts.append(f'<use href="#{key}" transform="translate({offset:.4f},0)"/>');offset+=f['widths'][name][0]*scale+tracking
  self.add(f'<g fill="{color or self.p["ink"]}" aria-label="{text}" transform="translate({x},{y})">'+''.join(part.replace(')"/>',f') scale({scale:.6f},-{scale:.6f})"/>') for part in parts)+'</g>')
  return offset
 def save(self,path):
  defs=''.join(f'<path id="{k}" d="{v}"/>' for k,v in self.defs.items());s=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" role="img" aria-labelledby="title"><title id="title">{self.title}</title><defs>{defs}</defs>'+''.join(self.body)+'</svg>\n';path.write_text(s)
_CACHE={}
def fontdata(name):
 if name not in _CACHE:
  f=TTFont(FONTS/({'bold':'DejaVuSans-Bold.ttf','mono':'DejaVuSansMono.ttf','serif':'DejaVuSerif.ttf'}[name]));_CACHE[name]={'units':f['head'].unitsPerEm,'cmap':f.getBestCmap(),'glyphs':f.getGlyphSet(),'widths':f['hmtx'].metrics}
 return _CACHE[name]

def ticks(s,x,y,r):
 for i in range(72):
  a=math.tau*i/72;rr=r+(12 if i%6==0 else 5);s.line(x+math.cos(a)*r,y+math.sin(a)*r,x+math.cos(a)*rr,y+math.sin(a)*rr,s.p['muted'],1)

def iris(s,x,y,r):
 p=s.p;s.circle(x+8,y+8,r,p['wash']);s.circle(x,y,r,p['paper'],p['ink'],2)
 # Interleaved elliptical line fields: not a photograph or a reused illustration.
 for i in range(1,37):
  ry=r*i/38
  s.add(f'<ellipse cx="{x}" cy="{y}" rx="{r*.93:.3f}" ry="{ry:.3f}" fill="none" stroke="{p["ink"]}" stroke-width="1.4" transform="rotate(38 {x} {y})"/>')
 # Both ellipse radii are below r, so every rotated ellipse stays within the rim.
 s.circle(x,y,r*.37,p['blue']);s.circle(x-r*.05,y+r*.01,r*.14,p['paper']);s.circle(x+r*.13,y-r*.14,r*.035,p['orange']);ticks(s,x,y,r+17)
 s.line(x-r-42,y,x-r+4,y,p['orange'],2);s.line(x+r-4,y,x+r+42,y,p['orange'],2);s.line(x,y-r-42,x,y-r+4,p['orange'],2);s.line(x,y+r-4,x,y+r+42,p['orange'],2)

def arrow(s,x,y,size,c):
 s.line(x,y+size,x+size,y,c,3);s.line(x,y,x+size,y,c,3);s.line(x+size,y,x+size,y+size,c,3)

def cover(theme,mobile=False):
 p=PALETTES[theme];w,h=(720,920) if mobile else (1440,760);s=SVG(w,h,p,'Бюро странных вещей. Смотреть. Собирать. Проверять.');s.rect(0,0,w,h,p['paper']);margin=38 if mobile else 60
 s.text('gitEdit',margin,53,23,font='mono');s.text('НЕЗАВИСИМЫЙ КАБИНЕТ',margin,85,12,font='mono',tracking=2);s.line(margin,108,w-margin,108,p['ink'])
 if mobile:
  for text,y in [('БЮРО',209),('СТРАННЫХ',294),('ВЕЩЕЙ',379)]:s.text(text,margin,y,76,tracking=-3)
  iris(s,360,611,153);s.text('Смотри. Собирай. Проверяй.',margin,851,27,font='serif');s.line(margin,872,w-margin,872,p['ink']);s.text('НЕ ВСЁ ТАК, КАК ВИДНО.',margin,899,12,font='mono',tracking=1.2);arrow(s,650,885,15,p['orange'])
 else:
  s.text('БЮРО',53,252,144,tracking=-6);s.text('СТРАННЫХ',53,394,119,tracking=-6);s.text('ВЕЩЕЙ',53,536,144,tracking=-6);iris(s,1115,348,205);s.text('НЕ ВСЁ ТАК,',1040,631,14,font='mono',tracking=1.4);s.text('КАК ВИДНО.',1040,657,14,font='mono',tracking=1.4)
  s.line(60,596,793,596,p['ink']);s.text('Смотри. Собирай. Проверяй.',60,642,29,font='serif');s.text('ОПТИКА  /  БУМАГА  /  ПРОВЕРЯЕМЫЕ ФОКУСЫ',60,689,13,font='mono',tracking=1);s.line(60,718,1380,718,p['ink']);s.text('ТРИ МАРШРУТА. НИ ОДНОЙ ОБЯЗАТЕЛЬНОЙ ТОЧКИ ВХОДА.',60,742,11,font='mono',tracking=.9);arrow(s,1349,737,15,p['orange'])
 s.save(OUT/f'cover-{theme}{"-mobile" if mobile else ""}.svg')

def motif(s,kind,x,y,scale=1):
 p=s.p;s.add(f'<g transform="translate({x},{y}) scale({scale})">')
 if kind=='look':
  for i in range(22):
   r=20+i*3.4;s.add(f'<ellipse cx="120" cy="105" rx="{r}" ry="{r*.7}" fill="none" stroke="{p["blue"]}" stroke-width="1.8" transform="rotate({i*3} 120 105)"/>')
  s.circle(120,105,17,p['orange'])
 elif kind=='make':
  points=[(20,140),(75,37),(130,118),(175,23),(222,140),(165,175),(108,155),(68,185)]
  s.add('<path d="M'+'L'.join(f'{x},{y}' for x,y in points)+f'Z" fill="{p["wash"]}" stroke="{p["ink"]}" stroke-width="2"/>')
  for a,b in [(0,2),(1,2),(2,3),(2,4),(2,5),(2,6),(2,7)]:s.line(*points[a],*points[b],p['blue'],2)
  s.circle(130,118,6,p['orange'])
 else:
  for i in range(7):
   x=25+i*31;s.circle(x,72,10,p['orange'] if i in [1,2,5,6] else p['wash'],p['ink'],1)
   for j,g in enumerate([[0,2,4,6],[1,2,5,6],[3,4,5,6]]):
    if i in g:s.circle(x,112+j*25,4,p['blue'])
  s.line(20,177,220,177,p['ink']);s.text('101 = 5',68,209,17,p['ink'],'mono')
 s.add('</g>')

ROUTES=[dict(id='look',number='01',title='СМОТРЕТЬ',subtitle='Свет врёт. Глаз достраивает.',description='Стереограммы, скрытые слои и смена точки зрения.',target='atlas/foyer-look.md'),dict(id='make',number='02',title='СОБИРАТЬ',subtitle='С экрана — на стол.',description='Бумага, сгибы, вырезы и настоящие детали.',target='atlas/foyer-make.md'),dict(id='prove',number='03',title='ПРОВЕРЯТЬ',subtitle='Красиво — ещё не значит верно.',description='Монеты, коды и фокусы с проверяемым ответом.',target='atlas/foyer-prove.md')]
def ribbon(route,theme,mobile=False):
 p=PALETTES[theme];w,h=(720,354) if mobile else (1440,238);s=SVG(w,h,p,route['title']+'. '+route['subtitle']);s.rect(0,0,w,h,p['paper']);s.line(0,1,w,1,p['ink'],2);s.line(0,h-1,w,h-1,p['rule']);
 if mobile:
  s.text(route['number'],28,51,18,p['orange'],'mono');s.text(route['title'],28,113,52,tracking=-2);s.text(route['subtitle'],28,154,22,font='serif');motif(s,route['id'],452,149,.9);s.text('ОТКРЫТЬ',28,308,13,font='mono',tracking=2);arrow(s,177,293,17,p['orange'])
 else:
  motif(s,route['id'],10,0,1);s.line(277,28,277,208,p['rule']);s.text(route['number'],311,57,16,p['orange'],'mono');s.text(route['title'],365,104,64,tracking=-2.5);s.text(route['subtitle'],365,152,25,font='serif');s.text(route['description'],365,191,15,font='mono');arrow(s,1338,98,28,p['orange'])
 s.save(OUT/f'{route["id"]}-{theme}{"-mobile" if mobile else ""}.svg')

def picture(name,alt,target,prefix=''):
 return f'''<a href="{prefix}{target}"><picture>
  <source media="(max-width: 640px) and (prefers-color-scheme: dark)" srcset="{prefix}assets/foyer/{name}-dark-mobile.svg">
  <source media="(max-width: 640px)" srcset="{prefix}assets/foyer/{name}-light-mobile.svg">
  <source media="(prefers-color-scheme: dark)" srcset="{prefix}assets/foyer/{name}-dark.svg">
  <img src="{prefix}assets/foyer/{name}-light.svg" width="1440" alt="{alt}">
</picture></a>'''

def main():
 OUT.mkdir(exist_ok=True,parents=True)
 for theme in PALETTES:
  for mobile in [False,True]:
   cover(theme,mobile)
   for route in ROUTES:ribbon(route,theme,mobile)
 (OUT/'routes.json').write_text(json.dumps(ROUTES,ensure_ascii=False,indent=2)+'\n')
 block='## Бюро странных вещей\n\n'+picture('cover','Бюро странных вещей. Смотри. Собирай. Проверяй.','atlas/foyer.md')+'\n\n'
 for route in ROUTES:block+=picture(route['id'],route['title']+'. '+route['subtitle'],route['target'])+'\n\n'
 block+='**Три входа, без правильного порядка:** [смотреть](atlas/foyer-look.md) · [собирать](atlas/foyer-make.md) · [проверять](atlas/foyer-prove.md). Это короткие маршруты по уже существующим экспонатам, а не новая обязательная инструкция.\n\n[Как устроено оформление и что подсмотрено в других README](atlas/foyer.md). Все старые экспонаты — дальше, без сокращений.\n\n'
 Path(__file__).with_name('readme-block.md').write_text(block)
 # Offline design proof. Does not pretend that arbitrary CSS is available on GitHub.
 html='<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Бюро странных вещей — цветопроба</title><style>body{margin:0;padding:24px;background:#ffffff;color:#222;font:18px system-ui}main{max-width:1000px;margin:auto}img{display:block;width:100%;height:auto}a{display:block;margin-bottom:18px}a:focus-visible{outline:4px solid #df542f}p{line-height:1.5}a.text{display:inline}@media(prefers-color-scheme:dark){body{background:#0d1117;color:#eee}}@media(max-width:640px){body{padding:12px}}</style><main>'
 for name,alt,target in [('cover','Бюро странных вещей','atlas/foyer.md')]+[(r['id'],r['title'],r['target']) for r in ROUTES]:html+=picture(name,alt,target,'../../')
 html+='<p>Цветопроба: оригинальные SVG, светлая/тёмная тема, отдельная мобильная композиция. Без анимации и сети. Полная навигация работает в репозитории.</p></main></html>';(OUT/'proof.html').write_text(html)
 manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.glob('*.svg'))};(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(f'{len(manifest)} static SVG compositions generated; README not modified.')
if __name__=='__main__':main()
