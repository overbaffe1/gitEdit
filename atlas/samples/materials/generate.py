"""Own geometry and CPU-rendered editorial material study. No downloaded models/HDRIs."""
from pathlib import Path
from collections import Counter
import hashlib,json,struct
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from render import mesh,buffers,shading,wire_overlay,ground
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'assets/materials';FONT=Path('/usr/share/fonts/truetype/dejavu')
BG='#eeebe4';INK='#263749';MUTED='#6d797c'
def font(size,bold=False,mono=False):return ImageFont.truetype(str(FONT/('DejaVuSansMono.ttf' if mono else 'DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')),size)
def title(d,text,xy,size=22,color=INK,bold=False,mono=False):d.text(xy,text,font=font(size,bold,mono),fill=color)
def export(vertices,normals,faces):
    text=['# gitEdit material study; arbitrary units; same mesh for all three images']+['v '+' '.join(f'{x:.9f}' for x in v) for v in vertices]+['vn '+' '.join(f'{x:.9f}' for x in n) for n in normals]+['f '+' '.join(f'{i+1}//{i+1}' for i in f) for f in faces];(OUT/'form.obj').write_text('\n'.join(text)+'\n')
    out=bytearray(b'gitEdit original parametric form; arbitrary units'.ljust(80,b' '));out.extend(struct.pack('<I',len(faces)))
    for f in faces:
        triangle=vertices[f];n=np.cross(triangle[1]-triangle[0],triangle[2]-triangle[0]);n/=np.linalg.norm(n);out.extend(struct.pack('<12fH',*n,*triangle.ravel(),0))
    (OUT/'form.stl').write_bytes(out)
def compose_object(surface):
    base=Image.new('RGBA',surface.size,BG);base.alpha_composite(ground(*surface.size));base.alpha_composite(surface);return base.convert('RGB')
def main():
 OUT.mkdir(parents=True,exist_ok=True);vertices,normals,faces=mesh();depth,normal,xy,z=buffers(vertices,normals,faces);mask=np.isfinite(depth);surfaces={};renders={}
 for name in ['matte','metal','wire']:
  surface=shading(depth,normal,name)
  if name=='wire':surface=wire_overlay(surface,xy,z,depth)
  surfaces[name]=surface;renders[name]=compose_object(surface);renders[name].save(OUT/(name+'.jpg'),quality=94,subsampling=0,optimize=True)
 export(vertices,normals,faces)
 # The large product shot floats in front of restrained typesetting, not a framed exhibit card.
 hero=Image.new('RGBA',(1440,1020),BG);d=ImageDraw.Draw(hero);title(d,'gitEdit / MATERIAL STUDY', (52,35),19,mono=True);title(d,'001', (1312,35),19,mono=True);d.line((52,80,1388,80),fill='#aeb6b3',width=1);title(d,'ОДНА', (42,164),109,bold=True);title(d,'ФОРМА.', (42,282),109,bold=True);title(d,'Три поверхности.',(52,440),28);title(d,'Один ракурс.',(52,480),28);title(d,'Никакой подмены геометрии.',(52,547),16,mono=True)
 floating=surfaces['metal'].resize((930,845),Image.Resampling.LANCZOS);shadow=ground(930,845);hero.alpha_composite(shadow,(503,91));hero.alpha_composite(floating,(503,91));d=ImageDraw.Draw(hero);d.line((52,932,1388,932),fill='#aeb6b3',width=1);title(d,'МАТОВЫЙ СВЕТ / МЕТАЛЛИЧЕСКИЙ БЛИК / ВИДИМЫЕ РЁБРА',(52,958),17,mono=True);hero.convert('RGB').save(OUT/'hero.jpg',quality=94,subsampling=0,optimize=True)
 mobile=Image.new('RGBA',(720,1120),BG);d=ImageDraw.Draw(mobile);title(d,'gitEdit / MATERIAL STUDY',(30,28),17,mono=True);d.line((30,67,690,67),fill='#aeb6b3');title(d,'ОДНА ФОРМА.',(26,105),70,bold=True);title(d,'Три поверхности. Один ракурс.',(30,201),25);mobile.alpha_composite(ground(720,655),(0,280));mobile.alpha_composite(surfaces['metal'].resize((720,655),Image.Resampling.LANCZOS),(0,280));d=ImageDraw.Draw(mobile);d.line((30,992,690,992),fill='#aeb6b3');title(d,'НИКАКОЙ ПОДМЕНЫ ГЕОМЕТРИИ.',(30,1028),20,mono=True);title(d,'Не фото. Собственный CPU-рендер.',(30,1072),18,color=MUTED);mobile.convert('RGB').save(OUT/'hero-mobile.jpg',quality=94,subsampling=0,optimize=True)
 names=[('matte','01 / МАТОВАЯ'),('metal','02 / БЛИК'),('wire','03 / РЁБРА')];sheet=Image.new('RGB',(1440,586),BG);d=ImageDraw.Draw(sheet)
 for i,(name,label) in enumerate(names):sheet.paste(renders[name].resize((480,436),Image.Resampling.LANCZOS),(i*480,38));title(d,label,(i*480+34,502),24,bold=True);title(d,'Та же сетка и камера.',(i*480+34,545),15,mono=True)
 sheet.save(OUT/'comparison.jpg',quality=94,subsampling=0,optimize=True)
 strip=Image.new('RGB',(720,2160),BG);d=ImageDraw.Draw(strip)
 for i,(name,label) in enumerate(names):
  strip.paste(renders[name].resize((720,655),Image.Resampling.LANCZOS),(0,i*720));title(d,label,(32,i*720+658),25,bold=True)
 strip.save(OUT/'comparison-mobile.jpg',quality=93,subsampling=0,optimize=True)
 edges=Counter(tuple(sorted((int(f[i]),int(f[(i+1)%3])))) for f in faces for i in range(3));audit={'vertices':len(vertices),'faces':len(faces),'edges':len(edges),'edge_incidence_values':sorted(set(edges.values())),'euler_characteristic':len(vertices)-len(edges)+len(faces),'finite_coordinates':bool(np.isfinite(vertices).all()),'max_unit_normal_error':round(float(np.abs(np.linalg.norm(normals,axis=1)-1).max()),12),'mask_pixels':int(mask.sum()),'geometry_mask_sha256':hashlib.sha256(mask.tobytes()).hexdigest(),'image_size':[1100,1000],'shared_camera':True,'shared_visibility_buffer':True,'mesh_units':'arbitrary; not a print scale','shading':'illustrative analytic studio, not measured/physical BRDF'};(OUT/'audit.json').write_text(json.dumps(audit,indent=2)+'\n')
 block='''## Материальная проба

<a href="atlas/materials.md"><picture>
  <source media="(max-width: 640px)" srcset="assets/materials/hero-mobile.jpg">
  <img src="assets/materials/hero.jpg" width="1440" alt="Одна объёмная форма с металлическими бликами на светлом студийном фоне. Собственная геометрия и CPU-рендер, не фотография.">
</picture></a>

<picture>
  <source media="(max-width: 640px)" srcset="assets/materials/comparison-mobile.jpg">
  <img src="assets/materials/comparison.jpg" width="1440" alt="Одна и та же сетка с одного ракурса: матовая фиолетовая стилизация, металлический блик и видимые рёбра. На телефоне варианты расположены вертикально.">
</picture>

**Одна геометрия, камера и видимость — три способа показать поверхность.** Это собственные иллюстративные шейдеры, не фотографии материалов и не физически точная модель отражения.

[Матовая крупно](assets/materials/matte.jpg) · [Металлический блик](assets/materials/metal.jpg) · [Рёбра крупно](assets/materials/wire.jpg) · [Модель STL](assets/materials/form.stl) · [Устройство и исследованные README](atlas/materials.md). В самом README — готовые статичные изображения: WebGL, GPU и внешние сервисы не требуются.

''';Path(__file__).with_name('readme-block.md').write_text(block)
 html='<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Материальная проба</title><style>body{margin:0;padding:20px;background:#192737;color:#eee;font:18px system-ui}main{max-width:1000px;margin:auto}img{width:100%;height:auto;display:block}a{color:#b7c9ff}a:focus-visible{outline:3px solid orange}p{line-height:1.5}@media(max-width:640px){body{padding:8px}}</style><main>'+block[block.index('<a '):block.index('**Одна геометрия')].replace('href="atlas/','href="../../atlas/').replace('srcset="assets/','srcset="../../assets/').replace('src="assets/','src="../../assets/')+'<p>Статичная цветопроба. Веб-рендерера внутри нет.</p></main></html>';(OUT/'proof.html').write_text(html)
 manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.iterdir()) if p.suffix in ['.jpg','.obj','.stl']};(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(audit,indent=2))
if __name__=='__main__':main()
