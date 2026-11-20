"""Finite Markdown configurator: states are files, transitions are normal links."""
from pathlib import Path
import itertools,json,hashlib,html
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).parent;ART=ROOT/'assets/switchboard';PAGES=ROOT/'atlas/switchboard/states'
START='<!-- switchboard:start -->';END='<!-- switchboard:end -->'
OPTIONS={'layout':{'wide':'Лента','stack':'Плакат'},'palette':{'ink':'Чернила','coral':'Коралл','forest':'Лес'},'detail':{'brief':'Коротко','full':'Подробно'}}
COLORS={'ink':'#263e66','coral':'#ac4b3a','forest':'#25594d'}
def states():return [dict(zip(OPTIONS,values)) for values in itertools.product(*(v.keys() for v in OPTIONS.values()))]
def key(s):return '-'.join(s[k] for k in OPTIONS)
def image_name(s):return s['layout']+'-'+s['palette']+'.svg'
def transitions(s):
 return [{'axis':axis,'value':value,'target':key({**s,axis:value})} for axis,values in OPTIONS.items() for value in values if value!=s[axis]]
def image(layout,palette):
 w,h=(1200,260) if layout=='wide' else (720,480);ink=COLORS[palette]
 title='НАЗВАНИЕ ПРОЕКТА' if layout=='wide' else 'НАЗВАНИЕ'
 a=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">','<title id="title">Шаблон обложки проекта</title><desc id="desc">Собственный SVG: название проекта и простая геометрия. Цвет и раскладка выбраны на Markdown-странице.</desc>',f'<rect width="{w}" height="{h}" rx="16" fill="#f1e9d9"/>',f'<path d="M32 40H{w-32}" stroke="{ink}"/>',f'<text x="40" y="84" fill="{ink}" font-family="DejaVu Sans,Arial,sans-serif" font-size="18">BUILD / SHARE / EXPLAIN</text>',f'<text x="40" y="168" fill="{ink}" font-family="DejaVu Sans,Arial,sans-serif" font-size="{56 if layout=="wide" else 60}" font-weight="700">{title}</text>']
 if layout=='stack':a.append(f'<text x="40" y="235" fill="{ink}" font-family="DejaVu Sans,Arial,sans-serif" font-size="60" font-weight="700">ПРОЕКТА</text>')
 x,y=(1050,130) if layout=='wide' else (530,360)
 a.extend([f'<circle cx="{x}" cy="{y}" r="47" fill="none" stroke="{ink}" stroke-width="3"/>',f'<path d="M{x-70} {y+55}L{x} {y-65}L{x+70} {y+55}Z" fill="none" stroke="{ink}" stroke-width="3"/>','</svg>']);return '\n'.join(a)+'\n'
def snippet(s,src='assets/readme-card.svg'):
 width='100%' if s['layout']=='wide' else '520'
 b=f'<img src="{src}" width="{width}" alt="Обложка проекта: название и геометрический знак.">\n\n## Название проекта\n\nОдно предложение: что делает проект и кому помогает. Замени этот пример своим текстом.\n'
 if s['detail']=='full':b+='\n### С чего начать\n\n1. Объясни первый шаг.\n2. Укажи, где искать примеры.\n3. Опиши ожидаемый результат.\n\n| Раздел | Что написать |\n|---|---|\n| Возможности | Главные задачи проекта |\n| Ограничения | Чего проект не обещает |\n| Участие | Как предложить улучшение |\n'
 return b

def page(s):
 b='# Конструктор README без скрипта\n\n[В галерею](../../../README.md) · [Как устроено](../../switchboard.md)\n\nСсылки ниже **открывают другую Markdown-страницу**. Меняется один параметр, остальные сохраняются в имени файла. Это не форма, не JS и не запись в Git.\n\n'
 for axis,values in OPTIONS.items():
  b+='**'+{'layout':'Форма','palette':'Цвет SVG','detail':'Текст'}[axis]+':** '+ ' · '.join('**'+label+' ✓**' if s[axis]==value else f'[{label}]({key({**s,axis:value})}.md)' for value,label in values.items())+'\n\n'
 b+=f'Состояние: `{key(s)}`. Всего 12 готовых вариантов. [Сбросить](wide-ink-brief.md). Кнопка браузера «Назад» возвращает предыдущий вариант.\n\n---\n\n### Предпросмотр\n\n'+snippet(s,'../../../assets/switchboard/'+image_name(s))
 b+='\n---\n\n### Забрать вариант в свой репозиторий\n\n1. Сохрани [этот SVG](../../../assets/switchboard/'+image_name(s)+') в своём проекте как `assets/readme-card.svg`. Для исходных байтов используй Raw/Download, а не HTML-страницу файла.\n2. Скопируй Markdown ниже в свой корневой README и замени демонстрационный текст.\n\n```markdown\n'+snippet(s)+'```\n\n[Тот же фрагмент отдельным TXT](../../../assets/switchboard/snippets/'+key(s)+'.txt). Это текст для ручного копирования, не автоматическое изменение файла и не команда в буфер обмена.\n\nЦвет выбран в самом SVG и не переключается автоматически с темой GitHub. Размеры — подсказки для рендера; узкий экран ограничивает картинку шириной контейнера. SVG не содержит скриптов и внешних ресурсов.\n'
 return b

def main():
 PAGES.mkdir(parents=True,exist_ok=True);(ART/'snippets').mkdir(parents=True,exist_ok=True)
 for layout in OPTIONS['layout']:
  for palette in OPTIONS['palette']:(ART/f'{layout}-{palette}.svg').write_text(image(layout,palette))
 records=[]
 for s in states():
  ident=key(s);(PAGES/(ident+'.md')).write_text(page(s));(ART/'snippets'/(ident+'.txt')).write_text(snippet(s));records.append({'id':ident,'state':s,'page':'atlas/switchboard/states/'+ident+'.md','image':'assets/switchboard/'+image_name(s),'snippet':'assets/switchboard/snippets/'+ident+'.txt','transitions':transitions(s)})
 (ART/'states.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
 b=START+'''
## Конструктор README без JavaScript

**[Открыть переключаемый конструктор](atlas/switchboard/states/wide-ink-brief.md)** — выбери форму, цвет и объём текста, затем забери готовый Markdown и SVG.

| Начать с чернил | Начать с коралла | Начать с леса |
|---|---|---|
| [Лента](atlas/switchboard/states/wide-ink-brief.md) | [Лента](atlas/switchboard/states/wide-coral-brief.md) | [Лента](atlas/switchboard/states/wide-forest-brief.md) |
| [Плакат](atlas/switchboard/states/stack-ink-brief.md) | [Плакат](atlas/switchboard/states/stack-coral-brief.md) | [Плакат](atlas/switchboard/states/stack-forest-brief.md) |

Это **12 связанных Markdown-страниц**, а не скрытый движок GitHub: каждый выбор открывает другую страницу, сохраняя остальные параметры в её имени. Работают обычные ссылки и «Назад» браузера; ничего не отправляется в Issue, Actions не запускаются, чужой сайт не открывается.

На каждой странице есть настоящий предпросмотр и исходник выбранного фрагмента. Для переноса нужны **два файла**: текст в корневой README и локальная SVG-обложка. Данные не записываются в репозиторий при переключении; приватные поля не собираются.

[Как устроены переходы, что исследовано и где ограничения](atlas/switchboard.md) · [Граф всех состояний JSON](assets/switchboard/states.json). Это гипертекстовый приём поверх GitHub Markdown, не встроенная форма внутри текущего README. Все прежние разделы ниже сохранены.

'''+END+'\n\n'
 (HERE/'readme-block.md').write_text(b)
 paths=[*sorted(PAGES.glob('*.md')),*sorted(ART.glob('*.svg')),*sorted((ART/'snippets').glob('*.txt')),ART/'states.json']
 (ART/'manifest.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},indent=2)+'\n')
if __name__=='__main__':main()
