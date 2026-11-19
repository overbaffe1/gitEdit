"""Original three-plate poster. CSS lives in self-contained SVG images, never in README."""
from pathlib import Path
import importlib.util,json,hashlib,math
import pymupdf
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'assets/pressroom'
spec=importlib.util.spec_from_file_location('foyer_type',ROOT/'atlas/samples/foyer/generate.py');type_module=importlib.util.module_from_spec(spec);spec.loader.exec_module(type_module);SVG=type_module.SVG
P=dict(paper='#f1e7d3',ink='#17343f',blue='#06798d',orange='#e9653c',muted='#657771',rule='#b9b7a6',wash='#e7dcc4')
CSS='''
.plate-one{animation:register-one 16s ease-in-out infinite}
.plate-two{animation:register-two 16s ease-in-out infinite}
.plate-three{animation:register-three 16s ease-in-out infinite}
@keyframes register-one{0%,8%,100%{transform:translate(-28px,12px)}32%,85%{transform:translate(0,0)}}
@keyframes register-two{0%,8%,100%{transform:translate(24px,-18px)}32%,85%{transform:translate(0,0)}}
@keyframes register-three{0%,8%,100%{transform:translate(9px,19px)}32%,85%{transform:translate(0,0)}}
@media(prefers-reduced-motion:reduce){.plate-one,.plate-two,.plate-three{animation:none!important;transform:none!important}}
@media print{.plate-one,.plate-two,.plate-three{animation:none!important;transform:none!important}}
'''
def registration(s,color):
 for x,y in [(-15,75),(495,75),(-15,465),(495,465)]:
  s.circle(x,y,8,'none',color,1);s.line(x-13,y,x+13,y,color,1);s.line(x,y-13,x,y+13,color,1)
def scene(s,x,y,scale,animated,only=None):
 p=s.p;s.add(f'<g transform="translate({x},{y}) scale({scale})">')
 s.add(f'<path d="M0,540V240A240,240 0 0 1 480,240V540Z" fill="{p["wash"]}"/>')
 layers=[('one',p['orange']),('two',p['blue']),('three',p['ink'])]
 for number,color in layers:
  if only and only!=number:continue
  s.add(f'<g class="plate-{number}" data-plate="{number}">');registration(s,color);s.add('<g>')
  if number=='one':
   s.circle(324,164,101,color);s.circle(294,134,101,p['wash']);s.rect(0,435,480,105,color)
   for k in range(7):s.circle(47+k*65,470,18,p['paper'])
  elif number=='two':
   for k in range(21):
    yy=292+k*10;s.add(f'<path d="M0,{yy} C95,{yy-70} 230,{yy+90} 480,{yy-50}" fill="none" stroke="{color}" stroke-width="3"/>')
   for k in range(13):
    xx=14+k*15;top=max(58,240-math.sqrt(240**2-(xx-240)**2)+4);s.line(xx,top,xx,264,color,1.8)
   s.circle(104,185,43,p['paper'],color,4);s.circle(104,185,23,'none',color,1)
  else:
   s.add(f'<path d="M4,536V240A236,236 0 0 1 476,240V536Z" fill="none" stroke="{color}" stroke-width="8"/>')
   stair='M0,540V510H45V480H90V450H135V420H180V390H225V360H270V540Z';s.add(f'<path d="{stair}" fill="{color}"/>')
   for xx,yy in [(246,81),(187,189),(390,295),(68,329)]:s.line(xx-7,yy,xx+7,yy,color,2);s.line(xx,yy-7,xx,yy+7,color,2)
   s.rect(420,377,14,163,color);s.rect(390,407,74,7,color)
  s.add('</g></g>')
 s.add('</g>')
def poster(mobile=False,animated=True,only=None):
 w,h=(720,1000) if mobile else (1440,900);s=SVG(w,h,P,'Ночной тираж. Три цветовые формы сходятся в один абстрактный ночной пейзаж.');s.rect(0,0,w,h,P['paper']);s.text('gitEdit  /  ПЕЧАТНАЯ МАСТЕРСКАЯ',40,44,14,font='mono',tracking=1.2)
 if animated:s.add('<style>'+CSS+'</style>')
 s.line(40,65,w-40,65,P['ink'])
 if mobile:
  s.text('Ночной',34,155,78,font='serif',tracking=-2);s.text('тираж.',34,238,91,font='serif',tracking=-3);s.text('03 КРАСКИ / 01 ЛИСТ',41,279,15,font='mono',tracking=1.8);scene(s,144,345,.90,animated,only);s.line(40,885,680,885,P['ink']);s.text('Совпасть — и замереть.',40,927,29,font='serif');s.text('МЕДЛЕННАЯ ПРИВОДКА. НЕ СИМУЛЯЦИЯ СТАНКА.',40,966,12,font='mono')
 else:
  s.text('Ночной',48,258,138,font='serif',tracking=-5);s.text('тираж.',48,411,159,font='serif',tracking=-5);s.text('03 КРАСКИ',58,497,19,font='mono',tracking=2);s.text('01 ЛИСТ',58,532,19,font='mono',tracking=2);s.line(60,575,670,575,P['ink']);s.text('Совпасть —',58,636,44,font='serif');s.text('и замереть.',58,692,44,font='serif');scene(s,848,166,.99,animated,only);s.line(40,795,1400,795,P['ink']);s.text('ЦВЕТНЫЕ СЛОИ СХОДЯТСЯ. РИСУНОК ОСТАЁТСЯ.',42,840,17,font='mono',tracking=1);s.text('БЕЗ СЛУЧАЙНОСТИ. БЕЗ ВНЕШНИХ СЕРВИСОВ.',42,872,11,font='mono',tracking=1);s.text('NIGHT PRESS',1185,840,14,font='mono')
 # Explicit colour legend is static; no progress indicator or statistical value is implied.
 for i,color in enumerate([P['orange'],P['blue'],P['ink']]):
  xx=(592 if mobile else 1260)+i*28;s.circle(xx,39,7,color)
 suffix='-mobile' if mobile else '';name=f'plate-{only}.svg' if only else ('motion' if animated else 'still')+suffix+'.svg';s.save(OUT/name)
 return OUT/name

def main():
 OUT.mkdir(exist_ok=True,parents=True)
 for mobile in [False,True]:
  poster(mobile,True);still=poster(mobile,False)
  with pymupdf.open(still) as doc:
   pix=doc[0].get_pixmap(alpha=False);pix.save(OUT/('still-mobile.png' if mobile else 'still.png'))
 for ink in ['one','two','three']:poster(False,False,ink)
 # Portrait A4 static print. No moving content or fake printer calibration marks.
 with pymupdf.open(OUT/'still-mobile.svg') as svg:
  raw=svg.convert_to_pdf()
 with pymupdf.open(stream=raw,filetype='pdf') as source:
  pdf=pymupdf.open();page=pdf.new_page(width=595.2756,height=841.8898);page.show_pdf_page(pymupdf.Rect(28.35,28.35,566.9256,813.5398),source,0,keep_proportion=True);pdf.set_metadata({'title':'Ночной тираж — неподвижный плакат','author':'gitEdit','creationDate':'D:20260101000000Z','modDate':'D:20260101000000Z'});(OUT/'print-a4.pdf').write_bytes(pdf.tobytes(garbage=4,deflate=True,no_new_id=True));pdf.close()
 block='''## Ночной тираж

<a href="atlas/pressroom.md"><picture>
  <source media="(max-width: 640px) and (prefers-reduced-motion: reduce)" srcset="assets/pressroom/still-mobile.svg">
  <source media="(prefers-reduced-motion: reduce)" srcset="assets/pressroom/still.svg">
  <source media="(max-width: 640px)" srcset="assets/pressroom/motion-mobile.svg">
  <img src="assets/pressroom/motion.svg" width="1440" alt="Ночной тираж: оранжевый месяц, синие линии и тёмная архитектура медленно совмещаются в один печатный плакат. Есть неподвижная версия.">
</picture></a>

Три цветовые формы медленно сходятся, затем рисунок надолго замирает. Это **графическая метафора приводки**, не симуляция печатного станка. Заголовок и подписи не двигаются.

[Неподвижный плакат PNG](assets/pressroom/still.png) · [Плакат A4 PDF](assets/pressroom/print-a4.pdf) · [Три слоя отдельно и устройство анимации](atlas/pressroom.md). При reduced-motion показывается статичная композиция; внутри SVG движение тоже отключается. Всё остальное в галерее сохранено.

''';Path(__file__).with_name('readme-block.md').write_text(block)
 html='<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Ночной тираж — цветопроба</title><style>body{margin:0;background:#1c2d34;color:#eee;font:18px system-ui;padding:20px}main{max-width:1000px;margin:auto}img{width:100%;height:auto;display:block}a{color:#ffd0a3}p{line-height:1.5}@media(max-width:640px){body{padding:10px}}</style><main>'+block[block.index('<a '):block.index('</picture></a>')+len('</picture></a>')].replace('href="atlas/','href="../../atlas/').replace('srcset="assets/','srcset="../../assets/').replace('src="assets/','src="../../assets/')+'<p>Локальная цветопроба изображения. <a href="still.svg">Открыть неподвижный SVG</a>.</p></main></html>';(OUT/'proof.html').write_text(html)
 specdata={'duration_seconds':16,'separated_until_percent':8,'aligned_from_percent':32,'aligned_through_percent':85,'aligned_hold_seconds':8.48,'initial_offsets':{'one':[-28,12],'two':[24,-18],'three':[9,19]},'motion':'translation only; no opacity or flashing; captions fixed','print':'A4 portrait, static','compositions':{'desktop':[1440,900],'mobile':[720,1000]}};(OUT/'timing.json').write_text(json.dumps(specdata,indent=2)+'\n')
 manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.iterdir()) if p.suffix in ['.svg','.png','.pdf']};(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('7 self-contained SVGs, 2 PNGs, static A4 PDF; README unchanged.')
if __name__=='__main__':main()
