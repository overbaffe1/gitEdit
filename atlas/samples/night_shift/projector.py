"""One interlaced moth print and a four-position opaque grille.

The mask, paper and README player share one coordinate system. No video, JS,
external assets or font downloads. Run with Python 3 (standard library only).
"""
from pathlib import Path

OUT = Path(__file__).resolve().parents[3] / 'assets/night-shift'
W, H, SLIT = 240, 144, 2  # One unit = 0.5 mm at the size specified on the print pair.
POSES = ((1., 0.), (.73, .15), (.26, .26), (.67, -.16))
PERIOD = SLIT * len(POSES)
DARK, LIGHT = '#173640', '#f7d59d'

WING = '''<path fill="#9bd6c0" d="M-4-3C-21-4-49-2-78 9c8 13 21 25 38 21-2 9-6 17-14 24 21-5 34-19 48-40Z"/>
<path fill="#527d74" d="M-9 6q-20 13-44 22 25-3 41-14zm-7 8q-12 19-26 29 19-9 28-25z"/>
<path fill="#f3cf8e" d="M-3-9c-19-14-52-43-97-49 3 22 13 39 32 51 17 10 38 12 62 17Z"/>
<path fill="#e6ac76" d="M-100-58q24 6 43 20l-12 11q-6-14-22-16z"/>
<path fill="#668780" d="M-96-53q24 23 73 49-53-22-73-49z"/>
<path d="M-5 5q-31-19-59-26m51 20q-18-7-35-7m18-1-12-11" stroke="#956b50" fill="none" stroke-width="1.2"/>
<ellipse cx="-51" cy="-23" rx="9.3" ry="7" fill="#344e50" transform="rotate(27 -51 -23)"/><ellipse cx="-50" cy="-23" rx="5" ry="3.6" fill="#fff1c0" transform="rotate(27 -50 -23)"/>
<path d="M-74-15l3 3m-10-9 3 3m-9-11 2 3" fill="none" stroke="#fff1ce" stroke-width="2.4"/>'''
BODY = '''<path d="M117 70q-7-20-17-22m23 22q7-20 17-22m-24 16-8-6m16 6 8-6" fill="none" stroke="#d9b381" stroke-width="2"/>
<path d="M115 75q5-12 10 0 3 14-5 36-8-23-5-36Z" fill="#d59c70"/><ellipse cx="120" cy="75" rx="5.7" ry="7.1" fill="#fff0c8"/>
<path d="M117 88h6m-5 5h4" stroke="#5d6860" stroke-width="2"/>'''


def defs():
    parts = [f'<g id="wing">{WING}</g>']
    slices = []
    for i,(span,tilt) in enumerate(POSES):
        parts.append(f'<g id="f{i}"><g transform="translate(120 79)"><use href="#wing" transform="matrix({span} {tilt} 0 1 0 0)"/><g transform="scale(-1 1)"><use href="#wing" transform="matrix({span} {tilt} 0 1 0 0)"/></g></g>{BODY}</g>')
        parts.append(f'<pattern id="p{i}" patternUnits="userSpaceOnUse" width="{PERIOD}" height="{H}"><rect x="{i*SLIT}" width="{SLIT}" height="{H}" fill="white" shape-rendering="crispEdges"/></pattern><mask id="m{i}" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="url(#p{i})"/></mask>')
        slices.append(f'<use href="#f{i}" mask="url(#m{i})"/>')
    parts.append(f'<g id="paper"><rect width="{W}" height="{H}" fill="{DARK}"/>{"".join(slices)}</g>')
    return '\n'.join(parts)


def grille(color):
    return f'<pattern id="bars" patternUnits="userSpaceOnUse" width="{PERIOD}" height="{H}"><rect x="{SLIT}" width="{PERIOD-SLIT}" height="{H}" fill="{color}" shape-rendering="crispEdges"/></pattern>'


def piece(paper):
    title = 'Бумага с четырьмя фазами' if paper else 'Решётка · шаг 1 мм'
    definition = defs() if paper else grille('#10252c')
    art = '<use href="#paper"/>' if paper else f'<rect width="{W}" height="{H}" fill="url(#bars)"/>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="120mm" height="72mm" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d" xml:lang="ru">
<title id="t">{title}</title><desc id="d">Деталь оптической пары «Мотылёк» для печати в масштабе 100 %.</desc><defs>{definition}</defs>{art}</svg>\n'''


def svg_text(x,y,body,size,fill=LIGHT,bold=False):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-family="monospace" font-size="{size}" font-weight="{"bold" if bold else "normal"}">{body}</text>'


def player(animated, compact=False):
    if compact:
        w,h=300,422
        left,right=(12,47,276,149),(12,237,276,149)
        bottom_label=(18,402); stage_label=(19,225)
    else:
        w,h=636,260
        left,right=(14,55,339,167),(375,55,247,167)
        bottom_label=(383,237); stage_label=(382,41)
    def window(box,art):
        x,y,width,height=box
        return f'<svg x="{x}" y="{y}" width="{width}" height="{height}" viewBox="0 0 {W} {H}" overflow="hidden"><g clip-path="url(#cell)">{art}</g></svg>'
    holes=''.join(f'<rect x="{x}" y="{y}" width="13" height="5" rx="1"/>' for x in range(13,w-13,25) for y in (5,h-10))
    master='<use href="#paper"/><g class="slide"><rect x="-16" width="272" height="144" fill="url(#bars)"/></g>'
    filmstrip=''.join(f'<use href="#f{i}" x="{W*i}"/>' for i in range(len(POSES)))
    def keyframes(name, step):
        positions=' '.join(f'{25*i}% {{ transform: translateX({step*i}px); }}' for i in range(4))
        return f'@keyframes {name} {{ {positions} 100% {{ transform:translateX(0); }} }}'
    style = f'''<style>@media (prefers-reduced-motion: no-preference) {{
.slide {{ animation: slide 5.6s step-end infinite; }} .reel {{ animation: next 5.6s step-end infinite; }}
{keyframes('slide',SLIT)} {keyframes('next',-W)} }}</style>''' if animated else ''
    caption = '' if compact else svg_text(22,237,'ОКНО / 1 ММ',12,'#c3d4bc')
    wells=''.join(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="4" fill="{DARK}" stroke="#a78f70"/>' for x,y,width,height in (left,right))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d" xml:lang="ru">
<title id="t">Проекционная · Мотылёк</title><desc id="d">В первом окне бумага за решёткой, во втором та же фаза взмаха целиком. Четыре положения решётки открывают четыре позы.</desc>
{style}<defs>{defs()}\n{grille(DARK)}<clipPath id="cell"><rect width="240" height="144"/></clipPath></defs>
<rect width="{w}" height="{h}" rx="7" fill="#663d36"/><g fill="#d3a077">{holes}</g>
<rect x="9" y="15" width="{w-18}" height="{h-31}" rx="4" fill="#213c42"/>
{svg_text(20,42,'03  /  МОТЫЛЁК',20,bold=True)}{svg_text(*stage_label,'ФАЗА БЕЗ РЕШЁТКИ',14)}
{wells}
{window(left,master)}{window(right,'<g class="reel">'+filmstrip+'</g>')}
{caption}{svg_text(*bottom_label,'4 ФАЗЫ · 1 ЛИСТ',12,'#c3d4bc')}
</svg>\n'''


def poses():
    frames=''.join(f'<svg x="{(i%2)*236+4}" y="{(i//2)*146+4}" width="232" height="138" viewBox="0 0 {W} {H}"><use href="#f{i}"/></svg>'+svg_text((i%2)*236+12,(i//2)*146+24,f'0{i+1}',14) for i in range(4))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="476" height="294" viewBox="0 0 476 294" role="img" aria-labelledby="t d" xml:lang="ru"><title id="t">Контактный лист · четыре фазы</title><desc id="d">Крылья раскрыты, поднимаются, смыкаются и снова опускаются.</desc><defs>{defs()}</defs><rect width="476" height="294" rx="6" fill="{DARK}"/><path d="M238 6v282M6 147h464" stroke="#86968c"/>{frames}</svg>\n'''


if __name__=='__main__':
    for name,art in [('moth-projector',player(True)),('moth-still',player(False)),('moth-projector-compact',player(True,True)),('moth-still-compact',player(False,True)),('moth-poses',poses()),('moth-paper',piece(True)),('moth-grille',piece(False))]:
        (OUT/(name+'.svg')).write_text(art,encoding='utf-8')
