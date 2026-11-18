"""Cut three edge-to-edge panels from one panorama. Keep the exhibit tickets separate."""
from pathlib import Path
from PIL import Image

OUT = Path(__file__).resolve().parents[3] / 'assets/night-shift'

STOPS = [('fold', 'К перфоленте', '#f1c694'), ('tape', 'В театр теней', '#edb197'), ('moth', 'К рабочему столу', '#b8d9c3')]


def ticket(index, destination, paper):
    inks = ['#1c3740' if i <= index else 'none' for i in range(3)]
    punches = ''.join(f'<circle cx="{24+i*18}" cy="43" r="5" fill="{fill}" stroke="#1c3740"/>' for i, fill in enumerate(inks))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="338" height="64" viewBox="0 0 338 64" role="img" aria-labelledby="t d" xml:lang="ru">
<title id="t">{destination}</title><desc id="d">Билет ночной смены, остановка {index+1} из трёх.</desc>
<path d="M3 3H335v21a8 8 0 0 0 0 16v21H3V40a8 8 0 0 0 0-16Z" fill="{paper}" stroke="#213c43" stroke-width="2"/>
<path d="M80 4v56" stroke="#576359" stroke-dasharray="3 3"/>
<g font-family="monospace" fill="#193944"><text x="16" y="24" font-size="14" font-weight="bold">0{index+1}/03</text>{punches}<text x="95" y="22" font-size="11" letter-spacing="1.4">НОЧНАЯ СМЕНА</text></g>
<text x="94" y="46" font-family="system-ui,sans-serif" font-weight="bold" font-size="22" fill="#193944">{destination}</text><path d="M303 33h16m-7-7 7 7-7 7" fill="none" stroke="#193944" stroke-width="2.4"/>
</svg>\n'''


if __name__ == '__main__':
    with Image.open(OUT / 'bench-master.jpg') as image:
        width = image.width // 3
        left = (image.width - 3*width) // 2
        for i, name in enumerate(('glass', 'tape', 'film')):
            x = left + i * width
            panel = image.crop((x, 0, x + width, image.height))
            panel.save(OUT / f'bench-{name}.jpg', quality=86, optimize=True, subsampling=2)
    for i,(name,dest,color) in enumerate(STOPS):
        (OUT / f'ticket-{name}.svg').write_text(ticket(i,dest,color),encoding='utf-8')
