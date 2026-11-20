"""Original voxel intersection, native ASCII STL. Standard library only."""
from pathlib import Path
from collections import Counter
import hashlib
import json
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).parent;ART=ROOT/'assets/dual-solid';PLAY=ROOT/'atlas/dual-solid/README.md'
FONT={'A':['010','101','111','101','101'],'I':['111','010','010','010','111'],'3':['111','001','111','001','111'],'D':['110','101','101','101','110']}
def mask(word):return ['0'.join(FONT[c][y] for c in word) for y in range(5)]
def voxels():
 a,b=mask('AI'),mask('3D')
 return {(x,4-row,z) for row in range(5) for x in range(7) for z in range(7) if a[row][x]=='1' and b[row][z]=='1'}
# Counterclockwise vertices viewed from outside. Two triangles per exposed quad.
FACES=[((1,0,0),((1,0,0),(1,1,0),(1,1,1),(1,0,1))),((-1,0,0),((0,0,0),(0,0,1),(0,1,1),(0,1,0))),((0,1,0),((0,1,0),(0,1,1),(1,1,1),(1,1,0))),((0,-1,0),((0,0,0),(1,0,0),(1,0,1),(0,0,1))),((0,0,1),((0,0,1),(1,0,1),(1,1,1),(0,1,1))),((0,0,-1),((0,0,0),(0,1,0),(1,1,0),(1,0,0)))]
def mesh():
 cells=voxels();out=[]
 for x,y,z in sorted(cells):
  for normal,corners in FACES:
   if (x+normal[0],y+normal[1],z+normal[2]) in cells:continue
   points=[(2*(x+dx)-7,2*(y+dy)-5,2*(z+dz)-7) for dx,dy,dz in corners]
   for ids in [(0,1,2),(0,2,3)]:out.append((normal,tuple(points[i] for i in ids)))
 return out

def stl():
 out=['solid ai_3d_dual_solid']
 for n,tri in mesh():
  out+=[' facet normal '+' '.join(map(str,n)),'  outer loop']
  out+=['   vertex '+' '.join(map(str,v)) for v in tri]
  out+=['  endloop',' endfacet']
 return '\n'.join(out+['endsolid ai_3d_dual_solid',''])
def projection(axis):
 cells=voxels()
 return [''.join('1' if any((x,4-row,z) in cells for x,z in ([(col,k) for k in range(7)] if axis=='xy' else [(k,col) for k in range(7)])) else '0' for col in range(7)) for row in range(5)]
def stats():
 edges=Counter(tuple(sorted((a,b))) for _,tri in mesh() for a,b in zip(tri,tri[1:]+tri[:1]));cells=voxels();remaining=set(cells);components=[]
 while remaining:
  todo=[min(remaining)];seen=set(todo)
  while todo:
   x,y,z=todo.pop()
   for (dx,dy,dz),_ in FACES:
    v=(x+dx,y+dy,z+dz)
    if v in remaining and v not in seen:seen.add(v);todo.append(v)
  remaining-=seen;components.append(len(seen))
 return {'voxels':len(cells),'voxel_edge':2,'volume':8*len(cells),'triangles':len(mesh()),'edge_incidence_histogram':{str(k):v for k,v in sorted(Counter(edges.values()).items())},'face_connected_components':sorted(components),'targets':{'xy':mask('AI'),'zy':mask('3D')},'recovered_projections':{'xy':projection('xy'),'zy':projection('zy')}}
def proof():
 out=['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="420" viewBox="0 0 900 420" role="img" aria-labelledby="title desc">','<title id="title">Две проекции одной voxel-скульптуры</title><desc id="desc">Слева AI, справа 3D. Обе маски вычислены из общей трёхмерной геометрии, не являются отдельными сторонами текстуры.</desc>','<rect width="900" height="420" fill="#f3eddf"/>']
 for left,axis,title in [(45,'xy','XY / AI'),(495,'zy','ZY / 3D')]:
  out.append(f'<text x="{left}" y="48" font-family="sans-serif" font-size="24" fill="#213e55">{title}</text>')
  for y,row in enumerate(projection(axis)):
   for x,bit in enumerate(row):
    if bit=='1':out.append(f'<rect x="{left+x*48}" y="{80+y*48}" width="48" height="48" fill="#213e55"/>')
 out+=['<text x="45" y="385" font-family="sans-serif" font-size="18" fill="#213e55">ORTHOGRAPHIC PROJECTIONS / SAME SOLID / NO TEXTURES</text>','</svg>',''];return '\n'.join(out)

def block():return '''<!-- dual-solid:start -->
## Поверни фигуру: AI с одной стороны, 3D с другой

**[Открыть настоящую вращаемую 3D-амбиграмму](atlas/dual-solid/README.md)**. Это одна геометрия, а не две картинки: с одного направления её силуэт читается как **AI**, после поворота примерно на четверть оборота — как **3D**.

Используется уже знакомый нативный STL-viewer GitHub; **новое здесь — сама двухликая конструкция, не ещё один движок**. Внутри нет текстур, анимации, JavaScript и сервера. Скачивание приложения не требуется. [STL-файл](assets/dual-solid/ai-3d.stl) · [Две точные проекции](assets/dual-solid/projections.svg) · [Как это вычислено и проверено](atlas/dual-solid.md).

Крутить нужно вручную; читаемость точных проекций не гарантирует такой же результат с любого перспективного ракурса. Это экранная скульптура, **не готовая модель для 3D-печати**. Все прежние разделы ниже сохранены.

<!-- dual-solid:end -->

'''
def main():
 ART.mkdir(parents=True,exist_ok=True);PLAY.parent.mkdir(parents=True,exist_ok=True)
 model=stl();d=stats();(ART/'ai-3d.stl').write_text(model);(ART/'geometry.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');(ART/'projections.svg').write_text(proof());(HERE/'readme-block.md').write_text(block())
 scene='''# Одна скульптура — две надписи

[← Галерея](../../README.md) · [Геометрия и ограничения](../dual-solid.md) · [Открыть сам STL](../../assets/dual-solid/ai-3d.stl) · [Точные проекции без WebGL](../../assets/dual-solid/projections.svg)

**Зажми и поверни модель.** Найди **AI** в одном боковом силуэте, затем поверни вокруг вертикали примерно на 90° и найди **3D**. Если надпись зеркальная, посмотри с противоположной стороны; если спуталась срезами — выровняй наклон. Начальный ракурс GitHub не задаётся нашим генератором.

Это не GIF: ориентацию выбираешь ты. Сервер расчётов и JS приложения отсутствуют; WebGL и код самого просмотрщика принадлежат GitHub. Снизу вставлен полный ASCII STL, а не имя файла. Доступность viewer зависит от клиента и WebGL.

'''+f"**{d['voxels']} вокселя, {d['triangles']} треугольников.** В модели нет плоских надписей-текстур: читаются пустоты и объём. Не обещаем печатную связность или идеально фронтальный текст в перспективном рендерере.\n\n"+'```stl\n'+model+'```\n\nТекстовая альтернатива: математическая проекция на XY — «AI», на ZY — «3D». [Проверяемые маски и статистика](../../assets/dual-solid/geometry.json).\n'
 PLAY.write_text(scene)
 paths=[ART/'ai-3d.stl',ART/'geometry.json',ART/'projections.svg',PLAY,HERE/'readme-block.md'];(ART/'manifest.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},indent=2)+'\n')
if __name__=='__main__':main()
