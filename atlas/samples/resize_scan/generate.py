"""Viewport-controlled finite flipbook using native picture media selection."""
from pathlib import Path
import hashlib
import json
import math
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).parent;ART=ROOT/'assets/resize-scan'
COUNT=13;FIRST=599;STEP=80;RADIUS=2.2;ORBIT=.9;BORE=.55

def upper(i):return FIRST+STEP*i

def selected(width):
 for i in range(COUNT-1):
  if width<=upper(i):return i
 return COUNT-1

def frame(i):
 if not isinstance(i,int) or not 0<=i<COUNT:raise ValueError('Frame index must be 0..12')
 z=i/(COUNT-1);angle=2*math.pi*z
 return {'index':i,'z':z,'angle':angle,'cx':ORBIT*math.cos(angle),'cy':ORBIT*math.sin(angle),'max_width':upper(i) if i<COUNT-1 else None,'file':f'slice-{i:02}.svg'}

def drawing(i,ox=0,oy=0,scale=1):
 p=frame(i);x=270+76*p['cx'];y=245-76*p['cy'];track=[]
 for j in range(COUNT):
  theta=2*math.pi*j/(COUNT-1);track.append(f'<circle cx="{270+76*ORBIT*math.cos(theta):.3f}" cy="{245-76*ORBIT*math.sin(theta):.3f}" r="2" fill="#88aeb6"/>')
 return f'''<g transform="translate({ox} {oy}) scale({scale})">
<rect width="840" height="440" rx="20" fill="#101f2a"/>
<text x="32" y="40" font-family="sans-serif" font-size="18" fill="#a6c0c4">RESIZE SCAN / NATIVE PICTURE</text>
<circle cx="270" cy="245" r="{76*RADIUS}" fill="#dca65d"/>
<circle cx="270" cy="245" r="{76*ORBIT}" fill="none" stroke="#755e43" stroke-dasharray="3 9"/>
{''.join(track)}
<circle cx="{x:.6f}" cy="{y:.6f}" r="{76*BORE}" fill="#101f2a" stroke="#ecdbbb" stroke-width="2"/>
<path d="M250 245h40M270 225v40" stroke="#f6dfb5" opacity=".7"/>
<text x="515" y="125" font-family="monospace" font-size="24" fill="#a6c0c4">SLICE {i+1:02} / {COUNT}</text>
<text x="515" y="195" font-family="monospace" font-size="46" fill="#f6dfb5">z = {p['z']:.2f}</text>
<text x="515" y="255" font-family="sans-serif" font-size="18" fill="#a6c0c4">SYNTHETIC SOLID</text>
<text x="515" y="288" font-family="sans-serif" font-size="18" fill="#a6c0c4">NO PATIENT / NO SENSOR</text>
<rect x="515" y="330" width="270" height="8" fill="#344d58"/>
<rect x="515" y="330" width="{270*p['z']:.3f}" height="8" fill="#dca65d"/>
<text x="515" y="385" font-family="monospace" font-size="16" fill="#a6c0c4">NARROW &lt;---&gt; WIDE</text>
</g>'''

def svg(i):return '<svg xmlns="http://www.w3.org/2000/svg" width="840" height="440" viewBox="0 0 840 440" role="img" aria-labelledby="title desc">\n'+f'<title id="title">Срез {i+1} из 13</title><desc id="desc">Схематическое сечение цилиндра с каналом; кадр выбирается по ширине окна, не по времени.</desc>\n'+drawing(i)+'\n</svg>\n'

def picture(prefix=''):
 out=['<picture>']
 for i in range(COUNT-1):out.append(f'  <source media="(max-width: {upper(i)}px)" srcset="{prefix}assets/resize-scan/slice-{i:02}.svg">')
 out.extend([f'  <img src="{prefix}assets/resize-scan/slice-12.svg" width="840" alt="Синтетическое сечение цилиндра с движущимся по глубине отверстием. Ширина окна выбирает один из 13 кадров; все кадры доступны отдельно в инструкции.">','</picture>'])
 return '\n'.join(out)+'\n'

def block():return '''<!-- resize-scan:start -->
## Ширина окна вместо ручки сканера

**На компьютере медленно сузь и расширь окно браузера.** Картинка ниже будет менять не только размер, но и **срез синтетической детали** — прямо здесь, без JS, перезагрузки и открытия другого сайта.

'''+picture()+'''
Это **13 заранее вычисленных кадров**, а не настоящий range-ползунок, медицинский сканер или расчёт на лету. Выбор делает браузер через `picture` → `source media`; ширина — всего окна в CSS-пикселях, не самой картинки. До 599 px показывается первый кадр, от 1480 px — последний, между ними шаг 80 px. Изменения происходят только при пересечении порогов.

На телефоне и маленьком экране все положения могут быть недоступны. **[Все кадры и таблица порогов без изменения окна](atlas/resize-scan.md)** · [Исходник для переноса TXT](assets/resize-scan/picture.txt). Это необычное применение уже знакомого responsive `picture`, не новая скрытая функция GitHub. Самопроизвольной анимации, звука и backend нет; все прежние разделы ниже сохранены.

<!-- resize-scan:end -->

'''

def main():
 ART.mkdir(parents=True,exist_ok=True)
 for i in range(COUNT):(ART/frame(i)['file']).write_text(svg(i))
 (ART/'frames.json').write_text(json.dumps({'count':COUNT,'geometry':{'outer_radius':RADIUS,'orbit':ORBIT,'bore_radius':BORE},'frames':[frame(i) for i in range(COUNT)]},ensure_ascii=False,indent=2)+'\n')
 # Five rows at half-scale, including the final single frame.
 sheet='<svg xmlns="http://www.w3.org/2000/svg" width="1260" height="1100" viewBox="0 0 1260 1100" role="img" aria-labelledby="title"><title id="title">Все тринадцать срезов синтетической детали</title>\n'+''.join(drawing(i,(i%3)*420,(i//3)*220,.5) for i in range(COUNT))+'</svg>\n'
 (ART/'all-slices.svg').write_text(sheet);(ART/'picture.txt').write_text(picture());(HERE/'readme-block.md').write_text(block())
 files=[*sorted(ART.glob('slice-*.svg')),ART/'all-slices.svg',ART/'frames.json',ART/'picture.txt',HERE/'readme-block.md'];(ART/'manifest.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2)+'\n')
if __name__=='__main__':main()
