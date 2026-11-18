#!/usr/bin/env python3
"""Compile a small hyperlink adventure into SVG rooms and ordinary Markdown states.

No JavaScript, server, issues, workflow, tracking, timestamps or README edits.
"""
import argparse
from collections import deque
from html import escape
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
ROOMS=(
    ('Док','Здесь прибывают письма, которых ещё никто не написал. На стене план станции.','dock'),
    ('Архив','В ящиках лежат маршруты других путешественников. Южная дверь ведёт в атриум.','archive'),
    ('Обсерватория','На подставке сияет линза. Ты берёшь её: без неё луч маяка не собрать.','lens'),
    ('Оранжерея','Корни держат свод, листья ловят свет. Путь вниз ведёт к мастерской.','garden'),
    ('Атриум','На полу пересекаются световые дорожки. Отсюда удобно вернуться к архиву.','atrium'),
    ('Резонатор','Пустые кольца отвечают на каждый шаг. На севере обсерватория, на юге маяк.','rings'),
    ('Мастерская','На верстаке ждёт латунный ключ. Ты берёшь его: он отпирает корпус маяка.','key'),
    ('Галерея','В рамах пока нет картин. Зато между мастерской и маяком есть проход.','gallery'),
    ('Маяк','Для запуска нужны латунный ключ и линза. Можно вернуться за недостающим.','beacon'),
)
EDGES=((0,1),(0,3),(1,4),(2,5),(3,6),(4,5),(5,8),(6,7),(7,8))
PICKUPS={2:2,6:1}
LABELS={(-1,0):'Север', (1,0):'Юг',(0,-1):'Запад',(0,1):'Восток'}


def normalize(room,inventory):
    return room,inventory|PICKUPS.get(room,0)


def won(state):
    return state==(8,3)


def state_id(state):
    return f'r{state[0]:02}-i{state[1]}'


def neighbors(state):
    if won(state):
        return []
    room,inventory=state
    result=[]
    for a,b in EDGES:
        target=b if a==room else a if b==room else None
        if target is not None:
            delta=(target//3-room//3,target%3-room%3)
            result.append((LABELS[delta],normalize(target,inventory)))
    return result


def reachable():
    start=normalize(0,0)
    queue=deque([start]);seen={start}
    while queue:
        state=queue.popleft()
        for _,target in neighbors(state):
            if target not in seen:
                seen.add(target);queue.append(target)
    return sorted(seen)


def iso(u,v,z=0):
    return 500+(u-v)*48,185+(u+v)*26-z


def polygon(points,fill,stroke='#668a96',width=1):
    coords=' '.join(f'{x:.2f},{y:.2f}' for x,y in points)
    return f'<polygon points="{coords}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'


def box(u,v,w,d,h,color):
    a,b,c,e=[iso(x,y) for x,y in ((u,v),(u+w,v),(u+w,v+d),(u,v+d))]
    A,B,C,E=[iso(x,y,h) for x,y in ((u,v),(u+w,v),(u+w,v+d),(u,v+d))]
    return polygon([b,c,C,B],'#244754')+polygon([c,e,E,C],'#1b3648')+polygon([A,B,C,E],color)


def text(x,y,value,size=16,fill='#e5eee7'):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}">{escape(value)}</text>'


def art(room):
    title,_,kind=ROOMS[room]
    body=''
    body+=polygon([iso(0,0),iso(0,5),iso(0,5,90),iso(0,0,90)],'#1b3b4a')
    body+=polygon([iso(0,0),iso(5,0),iso(5,0,90),iso(0,0,90)],'#234756')
    for u in range(5):
        for v in range(5):
            body+=polygon([iso(u,v),iso(u+1,v),iso(u+1,v+1),iso(u,v+1)],'#2d5861' if (u+v)%2 else '#315f64','#416d73')
    # Small inset windows on the back wall are architectural marks, not controls.
    for v in (.6,2.0,3.4):
        body+=polygon([iso(0,v,25),iso(0,v+.6,25),iso(0,v+.6,65),iso(0,v,65)],'#f3c17d','#f3c17d')
    if kind=='archive':
        for v in (.4,1.8,3.2):
            body+=box(.35,v,.7,1.1,76,'#d69b65')
            for z in (19,38,57):
                p,q=iso(1.05,v,z),iso(1.05,v+1.1,z)
                body+=f'<path d="M{p[0]} {p[1]}L{q[0]} {q[1]}" stroke="#ddb27a" stroke-width="3"/>'
    elif kind=='garden':
        for u,v in ((1,1),(3,1),(1,3),(3,3)):
            body+=box(u,v,.7,.7,18,'#b68d68')
            x,y=iso(u+.35,v+.35,22)
            body+=f'<path d="M{x} {y}v-48m0 25q-35-30-30-40q30 0 30 25m0 15q35-30 30-40q-30 0-30 25" fill="none" stroke="#a8c693" stroke-width="7"/>'
    elif kind=='gallery':
        for u in (.5,2,3.5):
            body+=polygon([iso(u,0,20),iso(u+.9,0,20),iso(u+.9,0,70),iso(u,0,70)],'#35515b','#e0af75',3)
    elif kind=='rings':
        for i in range(4):
            x,y=iso(1+i*.7,2.5,55)
            body+=f'<ellipse cx="{x}" cy="{y}" rx="34" ry="57" fill="none" stroke="#dcbf87" stroke-width="4"/>'
    elif kind=='atrium':
        body+=box(2,2,1,1,18,'#d3b17d')
        x,y=iso(2.5,2.5,70)
        body+=f'<path d="M{x} {y-40}l30 40-30 40-30-40z" fill="none" stroke="#9fdfcc" stroke-width="3"/>'
    elif kind=='dock':
        for u,v in ((1,1),(3,2),(2,3)):
            body+=box(u,v,.9,.8,30,'#ce9c6b')
        x,y=iso(2.5,2.5,90)
        body+=f'<path d="M{x-35} {y}h70v36h-70zM{x-35} {y}l35 23 35-23" fill="#e4cf9c" stroke="#8b7866" stroke-width="2"/>'
    else:
        body+=box(2,2,1.2,1.2,45,'#bd9c75')
        x,y=iso(2.6,2.6,93)
        if kind=='lens':
            body+=f'<ellipse cx="{x}" cy="{y}" rx="34" ry="45" fill="#75cfc5" fill-opacity=".28" stroke="#bbe7d6" stroke-width="4"/><path d="M{x-18} {y-20}q15-20 30-12" fill="none" stroke="#f0f7db" stroke-width="3"/>'
        elif kind=='key':
            body+=f'<circle cx="{x-20}" cy="{y}" r="16" fill="none" stroke="#f4c680" stroke-width="8"/><path d="M{x-3} {y}h55m-8 0v15m-15-15v12" fill="none" stroke="#f4c680" stroke-width="8"/>'
        elif kind=='beacon':
            body+=polygon([(x,y-28),(x+100,y-50),(x+115,y+10),(x,y+5)],'#436e6a','#649d8b')
            body+=f'<circle cx="{x}" cy="{y}" r="26" fill="#f5cf91"/><circle cx="{x}" cy="{y}" r="12" fill="#fff0bd"/>'
    # Location map is deliberately textual/graphic only; real doors are Markdown links.
    for i in range(9):
        xx=70+(i%3)*25;yy=370+(i//3)*25
        body+=f'<rect x="{xx}" y="{yy}" width="17" height="17" rx="2" fill="{"#f4c680" if i==room else "#345765"}"/>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="540" viewBox="0 0 1000 540" role="img" aria-labelledby="title desc">
<title id="title">Станция Палимпсест / {escape(title)}</title><desc id="desc">Изометрическая иллюстрация комнаты; управление находится в Markdown под картинкой.</desc>
<style>text{{font-family:ui-monospace,Consolas,monospace}}</style><rect width="1000" height="540" rx="18" fill="#132c3a"/>
{text(35,38,'ПАЛИМПСЕСТ / '+title.upper(),22)}{text(35,66,'Гипертекстовый квест · обычные ссылки · без сервера и JavaScript',13,'#a6c7c6')}
{body}{text(35,496,'НАВИГАЦИЯ — ПОД РИСУНКОМ',12,'#f4c680')}{text(35,522,'Знаки предметов — символы комнат; текущий инвентарь указан текстом.',11,'#a6c7c6')}
</svg>\n'''


def inventory_label(mask):
    return ('ключ' if mask&1 else '—')+' / '+('линза' if mask&2 else '—')


def page(state):
    room,mask=state
    name,description,_=ROOMS[room]
    heading='Маяк зажжён' if won(state) else name
    body=f'# {heading}\n\n'
    body+=f'![Изометрическая комната: {name}. Управление обычными ссылками ниже.](../../assets/wayfinder/room{room:02}.svg)\n\n'
    body+=f'**Инвентарь: {inventory_label(mask)}.** Код состояния: `{state_id(state)}`.\n\n'
    if won(state):
        body+='Ты открыл корпус ключом, поставил линзу и направил луч к доку. Станция снова принимает письма. **Победа.**\n\n'
    else:
        body+=description+'\n\n'
        if room==8:
            missing=[label for bit,label in ((1,'ключ'),(2,'линза')) if not mask&bit]
            body+='Маяк пока закрыт. Не хватает: **'+', '.join(missing)+'**.\n\n'
        links={direction:f'[{direction}: {ROOMS[target[0]][0]}]({state_id(target)}.md)' for direction,target in neighbors(state)}
        body+='| | | |\n| :---: | :---: | :---: |\n'
        body+=f'| | {links.get("Север","Стена")} | |\n'
        body+=f'| {links.get("Запад","Стена")} | **Ты здесь** | {links.get("Восток","Стена")} |\n'
        body+=f'| | {links.get("Юг","Стена")} | |\n\n'
    body+='[Начать заново](r00-i0.md) · [Правила](README.md) · [Вернуться в галерею](../../README.md)\n\n'
    body+='Это переходы между готовыми файлами, не серверная игра. Инвентарь хранится в URL страницы; Back откатывает ход. Можно делиться ссылкой на состояние. Секретов и защиты от прямого открытия страниц нет.\n'
    return body


def generate(output):
    pages=output/'atlas/wayfinder';assets=output/'assets/wayfinder'
    pages.mkdir(parents=True,exist_ok=True);assets.mkdir(parents=True,exist_ok=True)
    states=reachable()
    for room in range(len(ROOMS)):
        (assets/f'room{room:02}.svg').write_text(art(room),encoding='utf-8')
    for state in states:
        (pages/f'{state_id(state)}.md').write_text(page(state),encoding='utf-8')
    rules='''# Станция «Палимпсест»

[Начать с дока](r00-i0.md) · [Вернуться в галерею](../../README.md) · [Исследование идеи](../expedition.md)

Собери **латунный ключ** в мастерской и **линзу** в обсерватории, затем доберись до маяка. Предметы подбираются автоматически при входе. Нажимай подписанные направления в таблице, а не дверь на рисунке.

Это маленький одиночный квест из заранее созданных Markdown-страниц. Нет JavaScript, сервера, Issues, токенов, Actions или общего состояния игроков. Ход ничего не публикует и не меняет в репозитории. Нужен только просмотрщик Markdown со ссылками; на публичном GitHub вход в аккаунт не требуется.

Имя страницы хранит комнату и инвентарь. Закладка сохраняет позицию, Back возвращает к прошлому состоянию. «Начать заново» сбрасывает инвентарь. Рисунки предметов — символы комнат, не оставшийся лут. Некоторые комнаты стоит пройти повторно.

Все состояния и финал лежат в открытых файлах. Можно открыть победу напрямую — защиты от спойлеров и читерства нет. Это демонстрация гипертекста, не соревнование. В галерее вход только через док.

**Доступность:** названия комнат, инвентарь и все действия написаны текстом. Картинка не обязательна для прохождения. Используй Tab/Enter для ссылок. Управление стрелками клавиатуры и ручное вращение сцены не реализованы.

Повторить из корня репозитория: `python3 atlas/samples/expedition/generate.py`. Генератор выпускает только свои страницы и рисунки, корневой README не редактирует. [Описание структуры и ограничений](../expedition.md).
'''
    (pages/'README.md').write_text(rules,encoding='utf-8')
    graph={'start':state_id((0,0)),'goal':state_id((8,3)),'rooms':len(ROOMS),
           'states':[{'id':state_id(s),'room':s[0],'inventory':s[1],'won':won(s),'moves':[{'label':label,'target':state_id(t)} for label,t in neighbors(s)]} for s in states]}
    (assets/'states.json').write_text(json.dumps(graph,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT,help='Destination root containing atlas/ and assets/')
    generate(parser.parse_args().output)
