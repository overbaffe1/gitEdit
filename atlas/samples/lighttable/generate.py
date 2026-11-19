"""Original slide mounts around read-only crops of the repository's own exhibits."""
from pathlib import Path
import hashlib,json,random
import pymupdf
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageOps
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'assets/lighttable';FONT=Path('/usr/share/fonts/truetype/dejavu')
ITEMS=[dict(id='engraving',title='Штриховая гравюра',label='ГРАВЮРА',subtitle='Один рисунок. Другой язык печати.',source='assets/printroom/hatch.svg',crop=[.03,.17,.61,.92],target='atlas/printroom.md',angle=-1.4),dict(id='rosette',title='Гильоширные розетки',label='РОЗЕТКИ',subtitle='Линия вместо готовой текстуры.',source='assets/afterlight/guilloche.svg',crop=[.06,.22,.94,.90],target='atlas/afterlight.md',angle=1.1),dict(id='moon',title='Нитяная луна',label='НИТЯНАЯ ЛУНА',subtitle='Изображение становится маршрутом.',source='assets/threadmoon/moon.png',crop=[.06,.10,.94,.94],target='atlas/threadmoon.md',angle=.8),dict(id='depth',title='Скрытая глубина',label='ГЛУБИНА',subtitle='Узор, в котором спрятан рельеф.',source='assets/stereogram/stereogram.png',crop=[0,0,1,1],target='atlas/stereogram.md',angle=-1),dict(id='fold',title='Бумажный кристалл',label='КРИСТАЛЛ',subtitle='Из плоского листа — восемь граней.',source='assets/night-shift/fold-still.png',crop=[.02,.15,.98,.96],target='atlas/relief.md',angle=-.7),dict(id='rolling',title='Пара Туси',label='КАЧЕНИЕ',subtitle='Два круга рисуют прямую.',source='assets/rolling/tusi-still.svg',crop=[.08,.22,.62,.90],target='atlas/rolling.md',angle=1.3)]
def font(size,bold=False,mono=False):return ImageFont.truetype(str(FONT/('DejaVuSansMono.ttf' if mono else 'DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')),size)
def raster(path):
 if path.suffix=='.svg':
  with pymupdf.open(path) as doc:
   pix=doc[0].get_pixmap(matrix=pymupdf.Matrix(1.5,1.5),alpha=False);return Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
 with Image.open(path) as src:
  src.seek(0);im=src.convert('RGBA');base=Image.new('RGBA',im.size,'white');base.alpha_composite(im);return base.convert('RGB')
def crop_image(item):
 im=raster(ROOT/item['source']);x,y,X,Y=item['crop'];box=(round(x*im.width),round(y*im.height),round(X*im.width),round(Y*im.height));return im.crop(box),list(box)
def slide(item,index,theme,art):
 dark=theme=='dark';bg='#1e2b31' if dark else '#e8e6dd';im=Image.new('RGB',(1000,800),bg);d=ImageDraw.Draw(im);rng=random.Random(801+index)
 # Light-table grid remains outside the mount. All grain is our fixed procedural texture.
 for x in range(0,1000,50):d.line((x,0,x,800),fill='#293940' if dark else '#dddbd2',width=1)
 for y in range(0,800,50):d.line((0,y,1000,y),fill='#293940' if dark else '#dddbd2',width=1)
 for _ in range(1200):
  x=rng.randrange(1000);y=rng.randrange(800);d.point((x,y),fill='#344047' if dark else '#d7d6cd')
 mount=Image.new('RGBA',(910,704),(0,0,0,0));m=ImageDraw.Draw(mount);m.rounded_rectangle((3,3,905,697),radius=22,fill='#deddd0',outline='#a8a99e',width=2);m.rounded_rectangle((9,9,899,691),radius=18,outline='#f9f7e9',width=3)
 # A shallow acetate bevel. The image stays unfiltered; only surrounding material has grain.
 m.rounded_rectangle((37,107,873,568),radius=10,fill='#7b817c');m.rounded_rectangle((44,114,866,561),radius=8,fill='#121c24');contained=ImageOps.contain(art,(810,435),Image.Resampling.LANCZOS);mount.alpha_composite(contained.convert('RGBA'),((910-contained.width)//2,119+(435-contained.height)//2))
 for y in [32,65,612,645]:
  for x in [28,864]:m.rounded_rectangle((x,y,x+15,y+24),radius=4,fill=bg,outline='#969e99',width=1)
 m.text((64,35),f'{index:02d}',font=font(52,True),fill='#b33e28');m.text((172,40),'GITEDIT  /  DIAPOSITIVE',font=font(22,mono=True),fill='#465755');m.text((172,72),'СВЕТОВОЙ СТОЛ  ·  ВЫБОРКА ИЗ ГАЛЕРЕИ',font=font(14,mono=True),fill='#66716b')
 for x in range(64,846,8):m.line((x,587,x,591 if x%32 else 596),fill='#8e958a',width=1)
 m.text((63,613),item['label'],font=font(39,True),fill='#23383c');m.text((64,667),'ОТКРЫТЬ ЭКСПОНАТ',font=font(16,mono=True),fill='#66716b',anchor='ls');m.line((812,636,843,605),fill='#b33e28',width=4);m.line((813,605,843,605,843,635),fill='#b33e28',width=4)
 # Sparse material speckles only on the border, not across the artwork.
 for _ in range(550):
  x=rng.randrange(15,892);y=rng.randrange(17,685)
  if not 35<x<875 or not 103<y<570:m.point((x,y),fill=(150,152,139,60))
 rot=mount.rotate(item['angle'],resample=Image.Resampling.BICUBIC,expand=True);alpha=rot.getchannel('A');shadow=Image.new('RGBA',rot.size,(0,0,0,0));shadow.putalpha(alpha.point(lambda x:x//3).filter(ImageFilter.GaussianBlur(12)));stage=im.convert('RGBA');xy=((1000-rot.width)//2,(800-rot.height)//2);stage.alpha_composite(shadow,(xy[0]+8,xy[1]+13));stage.alpha_composite(rot,xy);return stage.convert('RGB')
def picture(item,index,prefix=''):
 return f'<a href="{prefix}{item["target"]}"><picture><source media="(prefers-color-scheme: dark)" srcset="{prefix}assets/lighttable/{item["id"]}-dark.png"><img src="{prefix}assets/lighttable/{item["id"]}-light.png" width="100%" alt="{index:02d}. {item["title"]}: статичная миниатюра, открыть разбор экспоната"></picture></a>'
def table(prefix=''):
 rows=['<table width="100%">']
 for start in range(0,6,2):
  rows.append('<tr>')
  for i in range(start,start+2):
   item=ITEMS[i];rows.append('<td width="50%" valign="top">'+picture(item,i+1,prefix)+f'<br><a href="{prefix}{item["target"]}"><strong>{i+1:02d} · {item["title"]}</strong></a><br><sub>{item["subtitle"]}</sub></td>')
  rows.append('</tr>')
 rows.append('</table>');return '\n'.join(rows)
def main():
 OUT.mkdir(parents=True,exist_ok=True);catalog=[];images=[]
 for i,item in enumerate(ITEMS,1):
  art,box=crop_image(item)
  for theme in ['light','dark']:
   im=slide(item,i,theme,art);im.quantize(colors=256,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).save(OUT/f'{item["id"]}-{theme}.png',optimize=True)
   if theme=='light':images.append(im)
  catalog.append({**item,'number':i,'source_sha256':hashlib.sha256((ROOT/item['source']).read_bytes()).hexdigest(),'raster_crop_px':box,'preview_size':[1000,800],'modification':'read-only crop, uniformly resized to fit; PNG palette quantized to 256 colours without dithering; no artwork grain or colour grading'})
 (OUT/'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
 # Standalone full sheet is not the README's interactive surface. Each thumbnail is separate there.
 sheet=Image.new('RGB',(1600,2200),'#e8e6dd');d=ImageDraw.Draw(sheet);d.text((70,52),'СВЕТОВОЙ СТОЛ',font=font(63,True),fill='#23383c');d.text((74,142),'ШЕСТЬ ВХОДОВ В СУЩЕСТВУЮЩУЮ ГАЛЕРЕЮ',font=font(23,mono=True),fill='#64726d');d.line((70,198,1530,198),fill='#aab0a2',width=2)
 for i,im in enumerate(images):
  x=55+(i%2)*750;y=228+(i//2)*610;sheet.paste(im.resize((740,592),Image.Resampling.LANCZOS),(x,y))
 d.text((73,2125),'Это миниатюры. Оптические эффекты смотри в оригиналах.',font=font(22),fill='#465755');sheet.save(OUT/'contact-sheet.jpg',quality=94,subsampling=0,optimize=True)
 block='## Световой стол\n\nШесть диапозитивов из уже существующей галереи. **Нажми на изображение или подпись**, чтобы открыть экспонат: рамки декоративные, ссылки настоящие.\n\n'+table()+'\n\n[Контактный лист крупно](assets/lighttable/contact-sheet.jpg) · [Текстовый каталог и устройство оформления](atlas/lighttable.md). Миниатюры кадрированы для навигации: стереограмму и точные рисунки рассматривай в оригиналах.\n\n';Path(__file__).with_name('readme-block.md').write_text(block)
 html='<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Световой стол — цветопроба</title><style>body{background:#fff;color:#222;font:16px system-ui;margin:0;padding:24px}main{max-width:980px;margin:auto}table{border-collapse:collapse;table-layout:fixed;width:100%}td{border:1px solid #d1d9e0;padding:10px;overflow-wrap:anywhere}img{display:block;width:100%;height:auto}a{color:#0969da;text-decoration:none}a:focus-visible{outline:3px solid #bf4930}sub{vertical-align:baseline;font-size:12px}p{line-height:1.5}@media(prefers-color-scheme:dark){body{background:#0d1117;color:#eee}td{border-color:#3d444d}a{color:#79c0ff}}@media(max-width:480px){body{padding:8px}td{padding:5px}strong{font-size:13px}}</style><main><h1>Световой стол</h1><p>Цветопроба, не эмулятор всех стилей GitHub.</p>'+table('../../')+'<p>Статичная навигация, без JS и сети. Ссылки работают внутри полного репозитория.</p></main></html>';(OUT/'proof.html').write_text(html)
 manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.glob('*.png'))};(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('12 slide images + contact sheet. Existing artwork and README not modified.')
if __name__=='__main__':main()
