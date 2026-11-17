"""Typeset the same 16 repo weeks as a six-channel paper tape (SVG only)."""
import csv
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[2] / 'assets/night-shift'
TRACKS = (32,16,8,None,4,2,1)  # None is a small feed hole, never a data bit.
PAPER,INK,CASE,PALE,ACCENT = '#f5d89f','#1f3640','#172f37','#b2d5c3','#f6b47e'


def weeks():
    with (HERE.parent/'snake-weeks.csv').open() as f: rows=list(csv.DictReader(f))
    dates=[date.fromisoformat(r['date_utc']) for r in rows]; counts=[int(r['commits']) for r in rows]
    if len(dates)!=112 or dates[0].weekday()!=0 or any(d!=dates[0]+timedelta(days=i) for i,d in enumerate(dates)) or min(counts)<0:
        raise ValueError('Expected 16 complete Monday–Sunday weeks')
    result=[sum(counts[i:i+7]) for i in range(0,len(rows),7)]
    if max(result)>=64: raise ValueError('A weekly count no longer fits six channels')
    return result


def text(x,y,body,size,color=INK,anchor='start',bold=False):
    return f'<text x="{x}" y="{y}" fill="{color}" text-anchor="{anchor}" font-family="monospace" font-size="{size}" font-weight="{"bold" if bold else "normal"}">{body}</text>'


def svg(w,h,body,title,desc):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d" xml:lang="ru"><title id="t">{title}</title><desc id="d">{desc}</desc>\n{body}\n</svg>\n'


def strip(values, compact=False):
    # Narrow layout aligns week 7 directly above week 15 for comparison.
    cols=8 if compact else 16; w=62+cols*36;h=396 if compact else 232
    body=[f'<rect width="{w}" height="{h}" rx="10" fill="{CASE}"/>',text(15,28,'02 / СЧИТЫВАТЕЛЬ',15,PALE,bold=True),text(w-15,28,'6 БИТ',14,PAPER,'end')]
    for r in range(len(values)//cols):
        y=43+164*r
        body.extend([f'<rect x="9" y="{y}" width="{w-18}" height="155" rx="5" fill="{PAPER}"/>',f'<path d="M44 {y+3}v149" stroke="#ba9a6f"/>'])
        for j,weight in enumerate(TRACKS):
            cy=y+34+j*17;body.append(text(27,cy+4,'·' if weight is None else weight,13,INK,'middle',True))
        for c,n in enumerate(values[r*cols:(r+1)*cols]):
            ix=r*cols+c+1; x=65+c*36
            if ix in (7,15):
                body.append(f'<rect x="{x-14}" y="{y+4}" width="28" height="147" rx="10" fill="{"#acd0bf" if ix==7 else "#ecb18b"}" stroke="{INK}"/>')
            body.append(text(x,y+17,f'{ix:02}',13,INK,'middle',True))
            for j,weight in enumerate(TRACKS):
                cy=y+34+j*17
                if weight is None or n & weight:
                    rad=2 if weight is None else 5.7
                    body.append(f'<circle data-week="{ix}" data-track="{weight or 0}" cx="{x}" cy="{cy}" r="{rad}" fill="{INK}"/>')
                else:
                    body.append(f'<circle cx="{x}" cy="{cy}" r="5.6" fill="none" stroke="#bc9e73" stroke-width=".8"/>')
    body += [text(14,h-12,'LAZYGIT / 16 НЕДЕЛЬ',13,PALE),text(w-14,h-12,'07 ↔ 15',13,ACCENT,'end',True)]
    return svg(w,h,'\n'.join(body),'Перфолента · 16 недель LazyGit','Тёмное отверстие задаёт единицу. Дорожки сверху: 32, 16, 8, подача, 4, 2, 1. Выделены недели 7 и 15.')


def compare(values):
    w,h=476,154; parts=[f'<rect width="{w}" height="{h}" rx="8" fill="{CASE}"/>',text(16,25,'КЛЮЧ / ДВЕ КОЛОНКИ',14,PALE, bold=True)]
    for j,wt in enumerate(x for x in TRACKS if x): parts.append(text(116+j*45,51,wt,14,PAPER,'middle'))
    for i,ix in enumerate((7,15)):
        y=74+i*43;val=values[ix-1];parts.extend([text(15,y+6,f'№ {ix:02}',18,PAPER),text(459,y+7,f'= {val}',19,ACCENT,'end',True)])
        for j,wt in enumerate(x for x in TRACKS if x):
            x=116+j*45;col=ACCENT if j==5 else PALE
            parts.append(f'<circle cx="{x}" cy="{y}" r="10" fill="{col if val&wt else CASE}" stroke="{col}" stroke-width="2"/>')
    return svg(w,h,'\n'.join(parts),'Ключ · 44 и 45','В обеих строках есть 32, 8 и 4. Только в строке 15 есть ещё единица.')


if __name__=='__main__':
    vals=weeks()
    for name,s in [('weeks-tape',strip(vals)),('weeks-tape-compact',strip(vals,True)),('weeks-key',compare(vals))]:
        (OUT/(name+'.svg')).write_text(s,encoding='utf-8')
