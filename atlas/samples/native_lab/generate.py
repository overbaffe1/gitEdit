"""Generate actual native GitHub inputs and an insertable block; never edits README."""
from pathlib import Path
import math,json,hashlib,csv,io,importlib.util
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'assets/native-lab';HERE=Path(__file__).parent
START='<!-- native-lab:start -->';END='<!-- native-lab:end -->'
SCHEMES={
'flow':'''flowchart LR
    A[README] --> B{Что попробовать?}
    B --> C[Вращать STL]
    B --> D[Двигать карту]
    B --> E[Читать схему]
''',
'sequence':'''sequenceDiagram
    actor Reader as Читатель
    participant GH as GitHub
    participant File as Файл репозитория
    Reader->>GH: Открывает файл
    GH->>File: Читает поддерживаемый формат
    File-->>GH: Данные
    GH-->>Reader: Нативный просмотрщик
    Note over Reader,GH: Не запуск произвольного кода
''',
'states':'''stateDiagram-v2
    [*] --> Source
    Source --> Preview: открыть Preview
    Preview --> Source: открыть Code
    Preview --> Raw: открыть Raw
    Raw --> [*]
''',
'git':'''gitGraph
    commit id: "исходник"
    branch experiment
    checkout experiment
    commit id: "новый вид"
    checkout main
    merge experiment
    commit id: "готово"
''',
'pie':'''pie showData
    title Три способа изучать этот стенд — условные доли
    "В README" : 5
    "В просмотрщике файла" : 4
    "В истории Git" : 2
'''}
def mesh():
 n,m=12,6;vertices=[];faces=[]
 for i in range(n):
  u=i*math.tau/n
  for j in range(m):
   v=j*math.tau/m;vertices.append(((2+.45*math.cos(v))*math.cos(u),(2+.45*math.cos(v))*math.sin(u),.45*math.sin(v)))
 for i in range(n):
  for j in range(m):
   a=i*m+j;b=((i+1)%n)*m+j;c=((i+1)%n)*m+(j+1)%m;d=i*m+(j+1)%m
   faces.extend([(a,b,c),(a,c,d)])
 off=len(vertices);vertices.extend([(0,0,1.3),(0,0,-1.3),(.8,0,0),(0,.8,0),(-.8,0,0),(0,-.8,0)])
 for i in range(4):
  a=2+i;b=2+(i+1)%4
  faces.extend([(off,off+a,off+b),(off+1,off+b,off+a)])
 return vertices,faces
def normal(a,b,c):
 u=[b[i]-a[i] for i in range(3)];v=[c[i]-a[i] for i in range(3)]
 cross=(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]);length=math.sqrt(sum(x*x for x in cross));return tuple(x/length for x in cross)
def stl():
 vs,fs=mesh();lines=['solid native_orbit']
 for face in fs:
  pts=[vs[i] for i in face];norm=normal(*pts);lines.append('  facet normal '+' '.join(f'{x:.6f}' for x in norm));lines.append('    outer loop')
  lines.extend('      vertex '+' '.join(f'{x:.6f}' for x in p) for p in pts);lines.extend(['    endloop','  endfacet'])
 return '\n'.join(lines+['endsolid native_orbit'])+'\n'
def fence(lang,s):return '```'+lang+'\n'+s.rstrip()+'\n```\n\n'
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 (OUT/'orbit.stl').write_text(stl())
 for name in ['survey.geojson','sheets.topojson']:(OUT/name).write_bytes((ROOT/'assets'/name).read_bytes())
 for name,s in SCHEMES.items():(OUT/(name+'.mmd')).write_text(s)
 diff=json.loads((HERE/'config.json').read_text())['image_diff_commit'];diffurl='https://github.com/overbaffe1/gitEdit/commit/'+diff
 b=START+'''\n## GitHub, который можно потрогать

**Здесь — возможности самого GitHub, а не нарисованные кнопки.** Первые блоки работают в README; дальше явно помечено, что откроется на отдельной странице. В стороннем Markdown-просмотрщике вместо них может быть только исходный код.

> [!TIP]
> Начни с модели и карт: тяни мышью, меняй масштаб. Это настоящие встроенные просмотрщики, не GIF. Если блок не загрузился, рядом есть ссылка на отдельный файл.

### 1. Поверни объект — настоящий STL

Перетаскивай модель, приближай колесом, попробуй режим **Wireframe** в панели просмотрщика. Кольцо и кристалл — две раздельные замкнутые компоненты: 78 вершин и 152 треугольника. Это демонстрационная геометрия, не готовое изделие для печати.

'''+fence('stl',stl())
 b+='[Открыть ту же модель отдельным STL](assets/native-lab/orbit.stl) · [Как устроен стенд и его ограничения](atlas/native-lab.md). Для 3D нужен работающий WebGL в браузере.\n\n### 2. Подвигай карту — GeoJSON прямо здесь\n\nПопробуй масштабирование и перетаскивание. Точки и ломаная **условные**, это не проверенный туристический маршрут. Подложка загружается картографическим просмотрщиком GitHub, не нашим кодом.\n\n'+fence('geojson',(OUT/'survey.geojson').read_text())
 b+='[Та же карта отдельным файлом](assets/native-lab/survey.geojson). Окно с properties по нажатию на объект зависит от интерфейса просмотрщика.\n\n### 3. Две области с общей границей — TopoJSON\n\nЭто другая запись геометрии: соседние учебные полигоны ссылаются на общую дугу. Перемещать карту и менять масштаб можно так же; редактировать вершины в этом окне нельзя.\n\n'+fence('topojson',(OUT/'sheets.topojson').read_text())
 b+='[Те же области отдельным TopoJSON](assets/native-lab/sheets.topojson).\n\n### 4. Схемы строит GitHub, а не экспортёр PNG\n\nНиже пять **живых блоков Mermaid**: схема выбора, последовательность, состояния, Git-граф и круговая диаграмма. Это отрисовка текста, не симулятор процесса. Кнопки панорамирования/масштаба зависят от текущего интерфейса GitHub; произвольные JavaScript-обработчики сюда не добавлены.\n\n'
 for name in SCHEMES:b+=fence('mermaid',SCHEMES[name])
 b+='[Исходная схема](assets/native-lab/flow.mmd) · [Последовательность](assets/native-lab/sequence.mmd) · [Состояния](assets/native-lab/states.mmd) · [Git-граф](assets/native-lab/git.mmd) · [Доли](assets/native-lab/pie.mmd). Числа в диаграмме долей учебные, не статистика посетителей.\n\n### 5. Настоящее «до / после» со слайдером\n\n**[Открыть сравнение двух версий PNG на GitHub]('+diffurl+')** — выбери **Swipe**, затем **Onion Skin**, если эти режимы доступны в твоём интерфейсе. В первой версии круг оранжевый и полоски короче, во второй круг зелёный и полоски длиннее. Это один и тот же файл в двух коммитах, не картинка с нарисованным ползунком. **Откроется история изменений, не виджет внутри README.**\n\n[Текущий PNG](assets/native-lab/revision.png) · [Код, создающий обе версии](atlas/samples/native_lab/diff_image.py). В мобильном интерфейсе набор средств сравнения может отличаться.\n\n### 6. Ещё четыре просмотрщика — открой и попробуй\n\n| Открыть на GitHub | Что делать | Где граница |\n|---|---|---|\n| [Каталог CSV](assets/native-lab/catalog.csv) · [тот же TSV](assets/native-lab/catalog.tsv) | Введи `map` или `3d` в поиск над таблицей, если он доступен; нажми номер строки для ссылки на неё | Поиск на странице файла, не в Markdown-таблице; набор элементов UI зависит от интерфейса GitHub |\n| [Notebook с сохранённым результатом](assets/native-lab/mesh.ipynb) | Посмотри код и готовый текстовый вывод | GitHub не запускает Python, JS-виджеты и ячейки notebook |\n| [PDF из существующей галереи](assets/pressroom/print-a4.pdf) | Открой документ в просмотрщике GitHub | PDF не встроен в README; ссылки внутри PDF GitHub может игнорировать |\n| [Исходник Mermaid отдельным файлом](assets/native-lab/flow.mmd) | Сравни Preview и Code, если переключатель доступен | Это нативный рендер файла, не отдельное приложение |\n\n### 7. Необычная разметка, которая действительно работает\n\nФормулу ниже набирает GitHub, а не генератор картинки:\n\n```math\nV-E+F = 78-228+152 = 2\n```\n\nЭто сумма характеристик двух компонент (тора и октаэдра), **не утверждение, что вся модель — одна сфера**.\n\n<details open>\n<summary>Нажми: это настоящий раскрывающийся блок, а не кнопка на картинке</summary>\n\nОн открыт изначально, чтобы ничего не прятать. Сверни и разверни его мышью или клавиатурой. Выбор состояния не сохраняется в Git.\n\n- [x] Отмеченный пункт списка.\n- [ ] Неотмеченный пункт списка.\n\nЭти галочки показывают состояние Markdown, а не форму для отправки ответов: в README не обещается изменение файла кликом.\n\nСноска делает переход к примечанию и обратно.[^native-lab-note]\n\n</details>\n\n[^native-lab-note]: Это обычная сноска GitHub Markdown. В длинном README примечание окажется внизу документа; GitHub добавляет обратную ссылку.\n\n> [!IMPORTANT]\n> Произвольный HTML/JS, iframe с сайтом, Three.js-сцена, запуск notebook и игра на canvas не становятся работающими виджетами от вставки в README. Не путай нативные просмотрщики со ссылками на Pages и анимациями-картинками.\n\n[Полный реестр возможностей, пять типов alerts, адаптация по теме, видео и честные ограничения](atlas/native-lab.md) · [Постоянные ссылки на изученную документацию](atlas/samples/native_lab/sources.json). Все старые разделы ниже сохранены.\n\n'+END+'\n\n'
 extra='''### 8. Автогруппировка точек и другие форматы документации

[Открыть карту с 800 учебными точками](assets/native-lab/clusters.geojson): отдаляй и приближай. GitHub документирует автоматическую кластеризацию больших наборов; появление групп зависит от масштаба и текущего просмотрщика. Точки созданы сеткой, не являются адресами людей или результатом наблюдений.

GitHub умеет показывать не только Markdown: [reStructuredText](assets/native-lab/notes.rst) · [AsciiDoc](assets/native-lab/notes.adoc) · [Org](assets/native-lab/notes.org). Это **другие разметки документа**, не три новых интерактивных движка. [Узнать версию Mermaid отдельным файлом](assets/native-lab/version.mmd).

'''
 b=b.replace(END,extra+END)
 (HERE/'readme-block.md').write_text(b)
 features=[{'type':'Feature','properties':{'id':j*40+i+1,'note':'synthetic grid; not a real address'},'geometry':{'type':'Point','coordinates':[4.8+i*.001,52.3+j*.001]}} for j in range(20) for i in range(40)]
 (OUT/'clusters.geojson').write_text(json.dumps({'type':'FeatureCollection','features':features},ensure_ascii=False,separators=(',',':'))+'\n')
 (OUT/'version.mmd').write_text('info\n')
 (OUT/'notes.rst').write_text('Native GitHub renderer: reStructuredText\n========================================\n\nThis page is rendered from **reStructuredText**, not Markdown.\n\n* The format is supported by GitHub Markup.\n* There is no Python execution or custom JavaScript.\n\nExample::\n\n    vertices - edges + faces = 2\n')
 (OUT/'notes.adoc').write_text('= Native GitHub renderer: AsciiDoc\n\nThis page is rendered from *AsciiDoc*, not Markdown.\n\n|===\n|Format |Execution\n|AsciiDoc |No custom JavaScript\n|===\n')
 (OUT/'notes.org').write_text('* Native GitHub renderer: Org\n\nThis page uses *Org* markup, not Markdown.\n\n- Headings and lists are rendered.\n- Code is not executed.\n\n| Format | Execution |\n| Org | None |\n')
 # Searchable catalog describes actual artifacts rather than inventing usage statistics.
 rows=[['id','category','format','try','path'],['01','3d','STL','rotate zoom wireframe','orbit.stl'],['02','map','GeoJSON','pan zoom','survey.geojson'],['03','map','TopoJSON','pan zoom','sheets.topojson'],['04','diagram','Mermaid','read generated diagram','flow.mmd'],['05','image-diff','PNG','open linked commit; swipe onion skin','revision.png'],['06','notebook','IPYNB','read saved output; no execution','mesh.ipynb']]
 for name,sep in [('catalog.csv',','),('catalog.tsv','\t')]:
  s=io.StringIO(newline='');csv.writer(s,delimiter=sep,lineterminator='\n').writerows(rows);(OUT/name).write_text(s.getvalue())
 code='vertices, edges, faces = 78, 228, 152\nprint(vertices - edges + faces)\n'
 nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3'}},'cells':[{'id':'intro','cell_type':'markdown','metadata':{},'source':['# Сохранённый вывод, не работающий Python-сервер\n','Тор: χ=0; октаэдр: χ=2. Две компоненты вместе: χ=2.']},{'id':'counts','cell_type':'code','metadata':{},'execution_count':1,'source':code.splitlines(True),'outputs':[{'name':'stdout','output_type':'stream','text':['2\n']}]}]}
 (OUT/'mesh.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
 spec=importlib.util.spec_from_file_location('diff_image',HERE/'diff_image.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);mod.render(2).save(OUT/'revision.png',optimize=True)
 manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.iterdir()) if p.name!='manifest.json'}
 (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
if __name__=='__main__':main()
