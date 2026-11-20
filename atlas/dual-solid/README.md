# Одна скульптура — две надписи

[← Галерея](../../README.md) · [Геометрия и ограничения](../dual-solid.md) · [Открыть сам STL](../../assets/dual-solid/ai-3d.stl) · [Точные проекции без WebGL](../../assets/dual-solid/projections.svg)

**Зажми и поверни модель.** Найди **AI** в одном боковом силуэте, затем поверни вокруг вертикали примерно на 90° и найди **3D**. Если надпись зеркальная, посмотри с противоположной стороны; если спуталась срезами — выровняй наклон. Начальный ракурс GitHub не задаётся нашим генератором.

Это не GIF: ориентацию выбираешь ты. Сервер расчётов и JS приложения отсутствуют; WebGL и код самого просмотрщика принадлежат GitHub. Снизу вставлен полный ASCII STL, а не имя файла. Доступность viewer зависит от клиента и WebGL.

**83 вокселя, 632 треугольников.** В модели нет плоских надписей-текстур: читаются пустоты и объём. Не обещаем печатную связность или идеально фронтальный текст в перспективном рендерере.

```stl
solid ai_3d_dual_solid
 facet normal 1 0 0
  outer loop
   vertex -5 -5 -7
   vertex -5 -3 -7
   vertex -5 -3 -5
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -5 -5 -7
   vertex -5 -3 -5
   vertex -5 -5 -5
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -7 -5 -7
   vertex -7 -5 -5
   vertex -7 -3 -5
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -7 -5 -7
   vertex -7 -3 -5
   vertex -7 -3 -7
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -7 -3 -7
   vertex -7 -3 -5
   vertex -5 -3 -5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -7 -3 -7
   vertex -5 -3 -5
   vertex -5 -3 -7
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -7 -5 -7
   vertex -5 -5 -7
   vertex -5 -5 -5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -7 -5 -7
   vertex -5 -5 -5
   vertex -7 -5 -5
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -7 -5 -7
   vertex -7 -3 -7
   vertex -5 -3 -7
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -7 -5 -7
   vertex -5 -3 -7
   vertex -5 -5 -7
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -5 -5 -5
   vertex -5 -3 -5
   vertex -5 -3 -3
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -5 -5 -5
   vertex -5 -3 -3
   vertex -5 -5 -3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -7 -5 -5
   vertex -7 -5 -3
   vertex -7 -3 -3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -7 -5 -5
   vertex -7 -3 -3
   vertex -7 -3 -5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -7 -3 -5
   vertex -7 -3 -3
   vertex -5 -3 -3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -7 -3 -5
   vertex -5 -3 -3
   vertex -5 -3 -5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -7 -5 -5
   vertex -5 -5 -5
   vertex -5 -5 -3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -7 -5 -5
   vertex -5 -5 -3
   vertex -7 -5 -3
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -5 -5 -3
   vertex -5 -3 -3
   vertex -5 -3 -1
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -5 -5 -3
   vertex -5 -3 -1
   vertex -5 -5 -1
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -7 -5 -3
   vertex -7 -5 -1
   vertex -7 -3 -1
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -7 -5 -3
   vertex -7 -3 -1
   vertex -7 -3 -3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -7 -5 -3
   vertex -5 -5 -3
   vertex -5 -5 -1
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -7 -5 -3
   vertex -5 -5 -1
   vertex -7 -5 -1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -7 -5 -1
   vertex -5 -5 -1
   vertex -5 -3 -1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -7 -5 -1
   vertex -5 -3 -1
   vertex -7 -3 -1
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -5 -5 1
   vertex -5 -3 1
   vertex -5 -3 3
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -5 -5 1
   vertex -5 -3 3
   vertex -5 -5 3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -7 -5 1
   vertex -7 -5 3
   vertex -7 -3 3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -7 -5 1
   vertex -7 -3 3
   vertex -7 -3 1
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -7 -5 1
   vertex -5 -5 1
   vertex -5 -5 3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -7 -5 1
   vertex -5 -5 3
   vertex -7 -5 3
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -7 -5 1
   vertex -7 -3 1
   vertex -5 -3 1
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -7 -5 1
   vertex -5 -3 1
   vertex -5 -5 1
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -5 -5 3
   vertex -5 -3 3
   vertex -5 -3 5
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -5 -5 3
   vertex -5 -3 5
   vertex -5 -5 5
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -7 -5 3
   vertex -7 -5 5
   vertex -7 -3 5
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -7 -5 3
   vertex -7 -3 5
   vertex -7 -3 3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -7 -3 3
   vertex -7 -3 5
   vertex -5 -3 5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -7 -3 3
   vertex -5 -3 5
   vertex -5 -3 3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -7 -5 3
   vertex -5 -5 3
   vertex -5 -5 5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -7 -5 3
   vertex -5 -5 5
   vertex -7 -5 5
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -7 -5 5
   vertex -5 -5 5
   vertex -5 -3 5
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -7 -5 5
   vertex -5 -3 5
   vertex -7 -3 5
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -5 -3 -3
   vertex -5 -1 -3
   vertex -5 -1 -1
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -5 -3 -3
   vertex -5 -1 -1
   vertex -5 -3 -1
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -7 -3 -3
   vertex -7 -3 -1
   vertex -7 -1 -1
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -7 -3 -3
   vertex -7 -1 -1
   vertex -7 -1 -3
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -7 -3 -1
   vertex -5 -3 -1
   vertex -5 -1 -1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -7 -3 -1
   vertex -5 -1 -1
   vertex -7 -1 -1
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -7 -3 -3
   vertex -7 -1 -3
   vertex -5 -1 -3
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -7 -3 -3
   vertex -5 -1 -3
   vertex -5 -3 -3
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -5 -3 1
   vertex -5 -1 1
   vertex -5 -1 3
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -5 -3 1
   vertex -5 -1 3
   vertex -5 -3 3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -7 -3 1
   vertex -7 -3 3
   vertex -7 -1 3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -7 -3 1
   vertex -7 -1 3
   vertex -7 -1 1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -7 -3 3
   vertex -5 -3 3
   vertex -5 -1 3
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -7 -3 3
   vertex -5 -1 3
   vertex -7 -1 3
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -7 -3 1
   vertex -7 -1 1
   vertex -5 -1 1
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -7 -3 1
   vertex -5 -1 1
   vertex -5 -3 1
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -5 -3 5
   vertex -5 -1 5
   vertex -5 -1 7
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -5 -3 5
   vertex -5 -1 7
   vertex -5 -3 7
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -7 -3 5
   vertex -7 -3 7
   vertex -7 -1 7
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -7 -3 5
   vertex -7 -1 7
   vertex -7 -1 5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -7 -3 5
   vertex -5 -3 5
   vertex -5 -3 7
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -7 -3 5
   vertex -5 -3 7
   vertex -7 -3 7
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -7 -3 7
   vertex -5 -3 7
   vertex -5 -1 7
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -7 -3 7
   vertex -5 -1 7
   vertex -7 -1 7
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -7 -3 5
   vertex -7 -1 5
   vertex -5 -1 5
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -7 -3 5
   vertex -5 -1 5
   vertex -5 -3 5
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -7 -1 -7
   vertex -7 -1 -5
   vertex -7 1 -5
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -7 -1 -7
   vertex -7 1 -5
   vertex -7 1 -7
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -7 1 -7
   vertex -7 1 -5
   vertex -5 1 -5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -7 1 -7
   vertex -5 1 -5
   vertex -5 1 -7
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -7 -1 -7
   vertex -5 -1 -7
   vertex -5 -1 -5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -7 -1 -7
   vertex -5 -1 -5
   vertex -7 -1 -5
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -7 -1 -7
   vertex -7 1 -7
   vertex -5 1 -7
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -7 -1 -7
   vertex -5 1 -7
   vertex -5 -1 -7
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -7 -1 -5
   vertex -7 -1 -3
   vertex -7 1 -3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -7 -1 -5
   vertex -7 1 -3
   vertex -7 1 -5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -7 1 -5
   vertex -7 1 -3
   vertex -5 1 -3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -7 1 -5
   vertex -5 1 -3
   vertex -5 1 -5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -7 -1 -5
   vertex -5 -1 -5
   vertex -5 -1 -3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -7 -1 -5
   vertex -5 -1 -3
   vertex -7 -1 -3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -7 -1 -3
   vertex -7 -1 -1
   vertex -7 1 -1
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -7 -1 -3
   vertex -7 1 -1
   vertex -7 1 -3
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -7 -1 -1
   vertex -5 -1 -1
   vertex -5 1 -1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -7 -1 -1
   vertex -5 1 -1
   vertex -7 1 -1
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -7 -1 1
   vertex -7 -1 3
   vertex -7 1 3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -7 -1 1
   vertex -7 1 3
   vertex -7 1 1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -7 -1 3
   vertex -5 -1 3
   vertex -5 1 3
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -7 -1 3
   vertex -5 1 3
   vertex -7 1 3
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -7 -1 1
   vertex -7 1 1
   vertex -5 1 1
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -7 -1 1
   vertex -5 1 1
   vertex -5 -1 1
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -7 -1 5
   vertex -7 -1 7
   vertex -7 1 7
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -7 -1 5
   vertex -7 1 7
   vertex -7 1 5
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -7 -1 7
   vertex -5 -1 7
   vertex -5 1 7
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -7 -1 7
   vertex -5 1 7
   vertex -7 1 7
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -7 -1 5
   vertex -7 1 5
   vertex -5 1 5
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -7 -1 5
   vertex -5 1 5
   vertex -5 -1 5
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -5 1 -3
   vertex -5 3 -3
   vertex -5 3 -1
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -5 1 -3
   vertex -5 3 -1
   vertex -5 1 -1
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -7 1 -3
   vertex -7 1 -1
   vertex -7 3 -1
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -7 1 -3
   vertex -7 3 -1
   vertex -7 3 -3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -7 3 -3
   vertex -7 3 -1
   vertex -5 3 -1
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -7 3 -3
   vertex -5 3 -1
   vertex -5 3 -3
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -7 1 -1
   vertex -5 1 -1
   vertex -5 3 -1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -7 1 -1
   vertex -5 3 -1
   vertex -7 3 -1
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -7 1 -3
   vertex -7 3 -3
   vertex -5 3 -3
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -7 1 -3
   vertex -5 3 -3
   vertex -5 1 -3
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -5 1 1
   vertex -5 3 1
   vertex -5 3 3
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -5 1 1
   vertex -5 3 3
   vertex -5 1 3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -7 1 1
   vertex -7 1 3
   vertex -7 3 3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -7 1 1
   vertex -7 3 3
   vertex -7 3 1
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -7 3 1
   vertex -7 3 3
   vertex -5 3 3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -7 3 1
   vertex -5 3 3
   vertex -5 3 1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -7 1 3
   vertex -5 1 3
   vertex -5 3 3
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -7 1 3
   vertex -5 3 3
   vertex -7 3 3
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -7 1 1
   vertex -7 3 1
   vertex -5 3 1
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -7 1 1
   vertex -5 3 1
   vertex -5 1 1
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -5 1 5
   vertex -5 3 5
   vertex -5 3 7
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -5 1 5
   vertex -5 3 7
   vertex -5 1 7
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -7 1 5
   vertex -7 1 7
   vertex -7 3 7
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -7 1 5
   vertex -7 3 7
   vertex -7 3 5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -7 3 5
   vertex -7 3 7
   vertex -5 3 7
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -7 3 5
   vertex -5 3 7
   vertex -5 3 5
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -7 1 7
   vertex -5 1 7
   vertex -5 3 7
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -7 1 7
   vertex -5 3 7
   vertex -7 3 7
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -7 1 5
   vertex -7 3 5
   vertex -5 3 5
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -7 1 5
   vertex -5 3 5
   vertex -5 1 5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -5 1 -7
   vertex -5 1 -5
   vertex -3 1 -5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -5 1 -7
   vertex -3 1 -5
   vertex -3 1 -7
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -5 -1 -7
   vertex -3 -1 -7
   vertex -3 -1 -5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -5 -1 -7
   vertex -3 -1 -5
   vertex -5 -1 -5
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -5 -1 -7
   vertex -5 1 -7
   vertex -3 1 -7
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -5 -1 -7
   vertex -3 1 -7
   vertex -3 -1 -7
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -5 1 -5
   vertex -5 1 -3
   vertex -3 1 -3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -5 1 -5
   vertex -3 1 -3
   vertex -3 1 -5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -5 -1 -5
   vertex -3 -1 -5
   vertex -3 -1 -3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -5 -1 -5
   vertex -3 -1 -3
   vertex -5 -1 -3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -5 1 -3
   vertex -5 1 -1
   vertex -3 1 -1
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -5 1 -3
   vertex -3 1 -1
   vertex -3 1 -3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -5 -1 -3
   vertex -3 -1 -3
   vertex -3 -1 -1
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -5 -1 -3
   vertex -3 -1 -1
   vertex -5 -1 -1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -5 -1 -1
   vertex -3 -1 -1
   vertex -3 1 -1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -5 -1 -1
   vertex -3 1 -1
   vertex -5 1 -1
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -5 1 1
   vertex -5 1 3
   vertex -3 1 3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -5 1 1
   vertex -3 1 3
   vertex -3 1 1
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -5 -1 1
   vertex -3 -1 1
   vertex -3 -1 3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -5 -1 1
   vertex -3 -1 3
   vertex -5 -1 3
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -5 -1 3
   vertex -3 -1 3
   vertex -3 1 3
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -5 -1 3
   vertex -3 1 3
   vertex -5 1 3
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -5 -1 1
   vertex -5 1 1
   vertex -3 1 1
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -5 -1 1
   vertex -3 1 1
   vertex -3 -1 1
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -5 1 5
   vertex -5 1 7
   vertex -3 1 7
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -5 1 5
   vertex -3 1 7
   vertex -3 1 5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -5 -1 5
   vertex -3 -1 5
   vertex -3 -1 7
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -5 -1 5
   vertex -3 -1 7
   vertex -5 -1 7
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -5 -1 7
   vertex -3 -1 7
   vertex -3 1 7
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -5 -1 7
   vertex -3 1 7
   vertex -5 1 7
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -5 -1 5
   vertex -5 1 5
   vertex -3 1 5
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -5 -1 5
   vertex -3 1 5
   vertex -3 -1 5
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -3 3 -7
   vertex -3 5 -7
   vertex -3 5 -5
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -3 3 -7
   vertex -3 5 -5
   vertex -3 3 -5
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -5 3 -7
   vertex -5 3 -5
   vertex -5 5 -5
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -5 3 -7
   vertex -5 5 -5
   vertex -5 5 -7
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -5 5 -7
   vertex -5 5 -5
   vertex -3 5 -5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -5 5 -7
   vertex -3 5 -5
   vertex -3 5 -7
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -5 3 -7
   vertex -3 3 -7
   vertex -3 3 -5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -5 3 -7
   vertex -3 3 -5
   vertex -5 3 -5
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -5 3 -7
   vertex -5 5 -7
   vertex -3 5 -7
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -5 3 -7
   vertex -3 5 -7
   vertex -3 3 -7
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -3 3 -5
   vertex -3 5 -5
   vertex -3 5 -3
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -3 3 -5
   vertex -3 5 -3
   vertex -3 3 -3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -5 3 -5
   vertex -5 3 -3
   vertex -5 5 -3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -5 3 -5
   vertex -5 5 -3
   vertex -5 5 -5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -5 5 -5
   vertex -5 5 -3
   vertex -3 5 -3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -5 5 -5
   vertex -3 5 -3
   vertex -3 5 -5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -5 3 -5
   vertex -3 3 -5
   vertex -3 3 -3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -5 3 -5
   vertex -3 3 -3
   vertex -5 3 -3
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -3 3 -3
   vertex -3 5 -3
   vertex -3 5 -1
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -3 3 -3
   vertex -3 5 -1
   vertex -3 3 -1
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -5 3 -3
   vertex -5 3 -1
   vertex -5 5 -1
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -5 3 -3
   vertex -5 5 -1
   vertex -5 5 -3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -5 5 -3
   vertex -5 5 -1
   vertex -3 5 -1
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -5 5 -3
   vertex -3 5 -1
   vertex -3 5 -3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -5 3 -3
   vertex -3 3 -3
   vertex -3 3 -1
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -5 3 -3
   vertex -3 3 -1
   vertex -5 3 -1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -5 3 -1
   vertex -3 3 -1
   vertex -3 5 -1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -5 3 -1
   vertex -3 5 -1
   vertex -5 5 -1
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -3 3 1
   vertex -3 5 1
   vertex -3 5 3
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -3 3 1
   vertex -3 5 3
   vertex -3 3 3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -5 3 1
   vertex -5 3 3
   vertex -5 5 3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -5 3 1
   vertex -5 5 3
   vertex -5 5 1
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -5 5 1
   vertex -5 5 3
   vertex -3 5 3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -5 5 1
   vertex -3 5 3
   vertex -3 5 1
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -5 3 1
   vertex -3 3 1
   vertex -3 3 3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -5 3 1
   vertex -3 3 3
   vertex -5 3 3
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -5 3 1
   vertex -5 5 1
   vertex -3 5 1
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -5 3 1
   vertex -3 5 1
   vertex -3 3 1
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -3 3 3
   vertex -3 5 3
   vertex -3 5 5
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -3 3 3
   vertex -3 5 5
   vertex -3 3 5
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -5 3 3
   vertex -5 3 5
   vertex -5 5 5
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -5 3 3
   vertex -5 5 5
   vertex -5 5 3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -5 5 3
   vertex -5 5 5
   vertex -3 5 5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -5 5 3
   vertex -3 5 5
   vertex -3 5 3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -5 3 3
   vertex -3 3 3
   vertex -3 3 5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -5 3 3
   vertex -3 3 5
   vertex -5 3 5
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -5 3 5
   vertex -3 3 5
   vertex -3 5 5
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -5 3 5
   vertex -3 5 5
   vertex -5 5 5
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -1 -5 -7
   vertex -1 -3 -7
   vertex -1 -3 -5
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -1 -5 -7
   vertex -1 -3 -5
   vertex -1 -5 -5
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -3 -5 -7
   vertex -3 -5 -5
   vertex -3 -3 -5
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -3 -5 -7
   vertex -3 -3 -5
   vertex -3 -3 -7
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -3 -3 -7
   vertex -3 -3 -5
   vertex -1 -3 -5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -3 -3 -7
   vertex -1 -3 -5
   vertex -1 -3 -7
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -3 -5 -7
   vertex -1 -5 -7
   vertex -1 -5 -5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -3 -5 -7
   vertex -1 -5 -5
   vertex -3 -5 -5
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -3 -5 -7
   vertex -3 -3 -7
   vertex -1 -3 -7
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -3 -5 -7
   vertex -1 -3 -7
   vertex -1 -5 -7
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -1 -5 -5
   vertex -1 -3 -5
   vertex -1 -3 -3
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -1 -5 -5
   vertex -1 -3 -3
   vertex -1 -5 -3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -3 -5 -5
   vertex -3 -5 -3
   vertex -3 -3 -3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -3 -5 -5
   vertex -3 -3 -3
   vertex -3 -3 -5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -3 -3 -5
   vertex -3 -3 -3
   vertex -1 -3 -3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -3 -3 -5
   vertex -1 -3 -3
   vertex -1 -3 -5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -3 -5 -5
   vertex -1 -5 -5
   vertex -1 -5 -3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -3 -5 -5
   vertex -1 -5 -3
   vertex -3 -5 -3
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -1 -5 -3
   vertex -1 -3 -3
   vertex -1 -3 -1
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -1 -5 -3
   vertex -1 -3 -1
   vertex -1 -5 -1
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -3 -5 -3
   vertex -3 -5 -1
   vertex -3 -3 -1
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -3 -5 -3
   vertex -3 -3 -1
   vertex -3 -3 -3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -3 -5 -3
   vertex -1 -5 -3
   vertex -1 -5 -1
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -3 -5 -3
   vertex -1 -5 -1
   vertex -3 -5 -1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -3 -5 -1
   vertex -1 -5 -1
   vertex -1 -3 -1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -3 -5 -1
   vertex -1 -3 -1
   vertex -3 -3 -1
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -1 -5 1
   vertex -1 -3 1
   vertex -1 -3 3
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -1 -5 1
   vertex -1 -3 3
   vertex -1 -5 3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -3 -5 1
   vertex -3 -5 3
   vertex -3 -3 3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -3 -5 1
   vertex -3 -3 3
   vertex -3 -3 1
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -3 -5 1
   vertex -1 -5 1
   vertex -1 -5 3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -3 -5 1
   vertex -1 -5 3
   vertex -3 -5 3
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -3 -5 1
   vertex -3 -3 1
   vertex -1 -3 1
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -3 -5 1
   vertex -1 -3 1
   vertex -1 -5 1
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -1 -5 3
   vertex -1 -3 3
   vertex -1 -3 5
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -1 -5 3
   vertex -1 -3 5
   vertex -1 -5 5
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -3 -5 3
   vertex -3 -5 5
   vertex -3 -3 5
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -3 -5 3
   vertex -3 -3 5
   vertex -3 -3 3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -3 -3 3
   vertex -3 -3 5
   vertex -1 -3 5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -3 -3 3
   vertex -1 -3 5
   vertex -1 -3 3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -3 -5 3
   vertex -1 -5 3
   vertex -1 -5 5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -3 -5 3
   vertex -1 -5 5
   vertex -3 -5 5
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -3 -5 5
   vertex -1 -5 5
   vertex -1 -3 5
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -3 -5 5
   vertex -1 -3 5
   vertex -3 -3 5
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -1 -3 -3
   vertex -1 -1 -3
   vertex -1 -1 -1
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -1 -3 -3
   vertex -1 -1 -1
   vertex -1 -3 -1
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -3 -3 -3
   vertex -3 -3 -1
   vertex -3 -1 -1
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -3 -3 -3
   vertex -3 -1 -1
   vertex -3 -1 -3
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -3 -3 -1
   vertex -1 -3 -1
   vertex -1 -1 -1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -3 -3 -1
   vertex -1 -1 -1
   vertex -3 -1 -1
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -3 -3 -3
   vertex -3 -1 -3
   vertex -1 -1 -3
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -3 -3 -3
   vertex -1 -1 -3
   vertex -1 -3 -3
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -1 -3 1
   vertex -1 -1 1
   vertex -1 -1 3
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -1 -3 1
   vertex -1 -1 3
   vertex -1 -3 3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -3 -3 1
   vertex -3 -3 3
   vertex -3 -1 3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -3 -3 1
   vertex -3 -1 3
   vertex -3 -1 1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -3 -3 3
   vertex -1 -3 3
   vertex -1 -1 3
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -3 -3 3
   vertex -1 -1 3
   vertex -3 -1 3
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -3 -3 1
   vertex -3 -1 1
   vertex -1 -1 1
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -3 -3 1
   vertex -1 -1 1
   vertex -1 -3 1
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -1 -3 5
   vertex -1 -1 5
   vertex -1 -1 7
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -1 -3 5
   vertex -1 -1 7
   vertex -1 -3 7
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -3 -3 5
   vertex -3 -3 7
   vertex -3 -1 7
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -3 -3 5
   vertex -3 -1 7
   vertex -3 -1 5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -3 -3 5
   vertex -1 -3 5
   vertex -1 -3 7
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -3 -3 5
   vertex -1 -3 7
   vertex -3 -3 7
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -3 -3 7
   vertex -1 -3 7
   vertex -1 -1 7
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -3 -3 7
   vertex -1 -1 7
   vertex -3 -1 7
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -3 -3 5
   vertex -3 -1 5
   vertex -1 -1 5
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -3 -3 5
   vertex -1 -1 5
   vertex -1 -3 5
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -1 -1 -7
   vertex -1 1 -7
   vertex -1 1 -5
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -1 -1 -7
   vertex -1 1 -5
   vertex -1 -1 -5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -3 1 -7
   vertex -3 1 -5
   vertex -1 1 -5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -3 1 -7
   vertex -1 1 -5
   vertex -1 1 -7
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -3 -1 -7
   vertex -1 -1 -7
   vertex -1 -1 -5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -3 -1 -7
   vertex -1 -1 -5
   vertex -3 -1 -5
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -3 -1 -7
   vertex -3 1 -7
   vertex -1 1 -7
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -3 -1 -7
   vertex -1 1 -7
   vertex -1 -1 -7
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -1 -1 -5
   vertex -1 1 -5
   vertex -1 1 -3
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -1 -1 -5
   vertex -1 1 -3
   vertex -1 -1 -3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -3 1 -5
   vertex -3 1 -3
   vertex -1 1 -3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -3 1 -5
   vertex -1 1 -3
   vertex -1 1 -5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -3 -1 -5
   vertex -1 -1 -5
   vertex -1 -1 -3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex -3 -1 -5
   vertex -1 -1 -3
   vertex -3 -1 -3
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -1 -1 -3
   vertex -1 1 -3
   vertex -1 1 -1
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -1 -1 -3
   vertex -1 1 -1
   vertex -1 -1 -1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -3 -1 -1
   vertex -1 -1 -1
   vertex -1 1 -1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -3 -1 -1
   vertex -1 1 -1
   vertex -3 1 -1
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -1 -1 1
   vertex -1 1 1
   vertex -1 1 3
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -1 -1 1
   vertex -1 1 3
   vertex -1 -1 3
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -3 -1 3
   vertex -1 -1 3
   vertex -1 1 3
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -3 -1 3
   vertex -1 1 3
   vertex -3 1 3
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -3 -1 1
   vertex -3 1 1
   vertex -1 1 1
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -3 -1 1
   vertex -1 1 1
   vertex -1 -1 1
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -1 -1 5
   vertex -1 1 5
   vertex -1 1 7
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -1 -1 5
   vertex -1 1 7
   vertex -1 -1 7
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -3 -1 7
   vertex -1 -1 7
   vertex -1 1 7
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -3 -1 7
   vertex -1 1 7
   vertex -3 1 7
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -3 -1 5
   vertex -3 1 5
   vertex -1 1 5
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -3 -1 5
   vertex -1 1 5
   vertex -1 -1 5
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -1 1 -3
   vertex -1 3 -3
   vertex -1 3 -1
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -1 1 -3
   vertex -1 3 -1
   vertex -1 1 -1
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -3 1 -3
   vertex -3 1 -1
   vertex -3 3 -1
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -3 1 -3
   vertex -3 3 -1
   vertex -3 3 -3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -3 3 -3
   vertex -3 3 -1
   vertex -1 3 -1
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -3 3 -3
   vertex -1 3 -1
   vertex -1 3 -3
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -3 1 -1
   vertex -1 1 -1
   vertex -1 3 -1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -3 1 -1
   vertex -1 3 -1
   vertex -3 3 -1
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -3 1 -3
   vertex -3 3 -3
   vertex -1 3 -3
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -3 1 -3
   vertex -1 3 -3
   vertex -1 1 -3
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -1 1 1
   vertex -1 3 1
   vertex -1 3 3
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -1 1 1
   vertex -1 3 3
   vertex -1 1 3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -3 1 1
   vertex -3 1 3
   vertex -3 3 3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -3 1 1
   vertex -3 3 3
   vertex -3 3 1
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -3 3 1
   vertex -3 3 3
   vertex -1 3 3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -3 3 1
   vertex -1 3 3
   vertex -1 3 1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -3 1 3
   vertex -1 1 3
   vertex -1 3 3
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -3 1 3
   vertex -1 3 3
   vertex -3 3 3
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -3 1 1
   vertex -3 3 1
   vertex -1 3 1
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -3 1 1
   vertex -1 3 1
   vertex -1 1 1
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -1 1 5
   vertex -1 3 5
   vertex -1 3 7
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex -1 1 5
   vertex -1 3 7
   vertex -1 1 7
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -3 1 5
   vertex -3 1 7
   vertex -3 3 7
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex -3 1 5
   vertex -3 3 7
   vertex -3 3 5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -3 3 5
   vertex -3 3 7
   vertex -1 3 7
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex -3 3 5
   vertex -1 3 7
   vertex -1 3 5
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -3 1 7
   vertex -1 1 7
   vertex -1 3 7
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex -3 1 7
   vertex -1 3 7
   vertex -3 3 7
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -3 1 5
   vertex -3 3 5
   vertex -1 3 5
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex -3 1 5
   vertex -1 3 5
   vertex -1 1 5
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 1 -5 -7
   vertex 1 -5 -5
   vertex 1 -3 -5
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 1 -5 -7
   vertex 1 -3 -5
   vertex 1 -3 -7
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 1 -3 -7
   vertex 1 -3 -5
   vertex 3 -3 -5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 1 -3 -7
   vertex 3 -3 -5
   vertex 3 -3 -7
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 1 -5 -7
   vertex 3 -5 -7
   vertex 3 -5 -5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 1 -5 -7
   vertex 3 -5 -5
   vertex 1 -5 -5
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 1 -5 -7
   vertex 1 -3 -7
   vertex 3 -3 -7
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 1 -5 -7
   vertex 3 -3 -7
   vertex 3 -5 -7
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 1 -5 -5
   vertex 1 -5 -3
   vertex 1 -3 -3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 1 -5 -5
   vertex 1 -3 -3
   vertex 1 -3 -5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 1 -3 -5
   vertex 1 -3 -3
   vertex 3 -3 -3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 1 -3 -5
   vertex 3 -3 -3
   vertex 3 -3 -5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 1 -5 -5
   vertex 3 -5 -5
   vertex 3 -5 -3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 1 -5 -5
   vertex 3 -5 -3
   vertex 1 -5 -3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 1 -5 -3
   vertex 1 -5 -1
   vertex 1 -3 -1
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 1 -5 -3
   vertex 1 -3 -1
   vertex 1 -3 -3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 1 -3 -3
   vertex 1 -3 -1
   vertex 3 -3 -1
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 1 -3 -3
   vertex 3 -3 -1
   vertex 3 -3 -3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 1 -5 -3
   vertex 3 -5 -3
   vertex 3 -5 -1
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 1 -5 -3
   vertex 3 -5 -1
   vertex 1 -5 -1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 1 -5 -1
   vertex 3 -5 -1
   vertex 3 -3 -1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 1 -5 -1
   vertex 3 -3 -1
   vertex 1 -3 -1
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 1 -5 1
   vertex 1 -5 3
   vertex 1 -3 3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 1 -5 1
   vertex 1 -3 3
   vertex 1 -3 1
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 1 -3 1
   vertex 1 -3 3
   vertex 3 -3 3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 1 -3 1
   vertex 3 -3 3
   vertex 3 -3 1
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 1 -5 1
   vertex 3 -5 1
   vertex 3 -5 3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 1 -5 1
   vertex 3 -5 3
   vertex 1 -5 3
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 1 -5 1
   vertex 1 -3 1
   vertex 3 -3 1
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 1 -5 1
   vertex 3 -3 1
   vertex 3 -5 1
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 1 -5 3
   vertex 1 -5 5
   vertex 1 -3 5
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 1 -5 3
   vertex 1 -3 5
   vertex 1 -3 3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 1 -3 3
   vertex 1 -3 5
   vertex 3 -3 5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 1 -3 3
   vertex 3 -3 5
   vertex 3 -3 3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 1 -5 3
   vertex 3 -5 3
   vertex 3 -5 5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 1 -5 3
   vertex 3 -5 5
   vertex 1 -5 5
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 1 -5 5
   vertex 3 -5 5
   vertex 3 -3 5
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 1 -5 5
   vertex 3 -3 5
   vertex 1 -3 5
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 1 3 -7
   vertex 1 3 -5
   vertex 1 5 -5
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 1 3 -7
   vertex 1 5 -5
   vertex 1 5 -7
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 1 5 -7
   vertex 1 5 -5
   vertex 3 5 -5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 1 5 -7
   vertex 3 5 -5
   vertex 3 5 -7
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 1 3 -7
   vertex 3 3 -7
   vertex 3 3 -5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 1 3 -7
   vertex 3 3 -5
   vertex 1 3 -5
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 1 3 -7
   vertex 1 5 -7
   vertex 3 5 -7
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 1 3 -7
   vertex 3 5 -7
   vertex 3 3 -7
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 1 3 -5
   vertex 1 3 -3
   vertex 1 5 -3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 1 3 -5
   vertex 1 5 -3
   vertex 1 5 -5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 1 5 -5
   vertex 1 5 -3
   vertex 3 5 -3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 1 5 -5
   vertex 3 5 -3
   vertex 3 5 -5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 1 3 -5
   vertex 3 3 -5
   vertex 3 3 -3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 1 3 -5
   vertex 3 3 -3
   vertex 1 3 -3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 1 3 -3
   vertex 1 3 -1
   vertex 1 5 -1
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 1 3 -3
   vertex 1 5 -1
   vertex 1 5 -3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 1 5 -3
   vertex 1 5 -1
   vertex 3 5 -1
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 1 5 -3
   vertex 3 5 -1
   vertex 3 5 -3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 1 3 -3
   vertex 3 3 -3
   vertex 3 3 -1
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 1 3 -3
   vertex 3 3 -1
   vertex 1 3 -1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 1 3 -1
   vertex 3 3 -1
   vertex 3 5 -1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 1 3 -1
   vertex 3 5 -1
   vertex 1 5 -1
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 1 3 1
   vertex 1 3 3
   vertex 1 5 3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 1 3 1
   vertex 1 5 3
   vertex 1 5 1
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 1 5 1
   vertex 1 5 3
   vertex 3 5 3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 1 5 1
   vertex 3 5 3
   vertex 3 5 1
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 1 3 1
   vertex 3 3 1
   vertex 3 3 3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 1 3 1
   vertex 3 3 3
   vertex 1 3 3
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 1 3 1
   vertex 1 5 1
   vertex 3 5 1
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 1 3 1
   vertex 3 5 1
   vertex 3 3 1
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 1 3 3
   vertex 1 3 5
   vertex 1 5 5
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 1 3 3
   vertex 1 5 5
   vertex 1 5 3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 1 5 3
   vertex 1 5 5
   vertex 3 5 5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 1 5 3
   vertex 3 5 5
   vertex 3 5 3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 1 3 3
   vertex 3 3 3
   vertex 3 3 5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 1 3 3
   vertex 3 3 5
   vertex 1 3 5
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 1 3 5
   vertex 3 3 5
   vertex 3 5 5
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 1 3 5
   vertex 3 5 5
   vertex 1 5 5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 3 -3 -7
   vertex 3 -3 -5
   vertex 5 -3 -5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 3 -3 -7
   vertex 5 -3 -5
   vertex 5 -3 -7
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 3 -5 -7
   vertex 5 -5 -7
   vertex 5 -5 -5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 3 -5 -7
   vertex 5 -5 -5
   vertex 3 -5 -5
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 3 -5 -7
   vertex 3 -3 -7
   vertex 5 -3 -7
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 3 -5 -7
   vertex 5 -3 -7
   vertex 5 -5 -7
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 3 -3 -5
   vertex 3 -3 -3
   vertex 5 -3 -3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 3 -3 -5
   vertex 5 -3 -3
   vertex 5 -3 -5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 3 -5 -5
   vertex 5 -5 -5
   vertex 5 -5 -3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 3 -5 -5
   vertex 5 -5 -3
   vertex 3 -5 -3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 3 -5 -3
   vertex 5 -5 -3
   vertex 5 -5 -1
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 3 -5 -3
   vertex 5 -5 -1
   vertex 3 -5 -1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 3 -5 -1
   vertex 5 -5 -1
   vertex 5 -3 -1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 3 -5 -1
   vertex 5 -3 -1
   vertex 3 -3 -1
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 3 -5 1
   vertex 5 -5 1
   vertex 5 -5 3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 3 -5 1
   vertex 5 -5 3
   vertex 3 -5 3
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 3 -5 1
   vertex 3 -3 1
   vertex 5 -3 1
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 3 -5 1
   vertex 5 -3 1
   vertex 5 -5 1
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 3 -3 3
   vertex 3 -3 5
   vertex 5 -3 5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 3 -3 3
   vertex 5 -3 5
   vertex 5 -3 3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 3 -5 3
   vertex 5 -5 3
   vertex 5 -5 5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 3 -5 3
   vertex 5 -5 5
   vertex 3 -5 5
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 3 -5 5
   vertex 5 -5 5
   vertex 5 -3 5
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 3 -5 5
   vertex 5 -3 5
   vertex 3 -3 5
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 5 -3 -3
   vertex 5 -1 -3
   vertex 5 -1 -1
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 5 -3 -3
   vertex 5 -1 -1
   vertex 5 -3 -1
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 3 -3 -3
   vertex 3 -3 -1
   vertex 3 -1 -1
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 3 -3 -3
   vertex 3 -1 -1
   vertex 3 -1 -3
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 3 -3 -1
   vertex 5 -3 -1
   vertex 5 -1 -1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 3 -3 -1
   vertex 5 -1 -1
   vertex 3 -1 -1
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 3 -3 -3
   vertex 3 -1 -3
   vertex 5 -1 -3
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 3 -3 -3
   vertex 5 -1 -3
   vertex 5 -3 -3
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 5 -3 1
   vertex 5 -1 1
   vertex 5 -1 3
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 5 -3 1
   vertex 5 -1 3
   vertex 5 -3 3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 3 -3 1
   vertex 3 -3 3
   vertex 3 -1 3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 3 -3 1
   vertex 3 -1 3
   vertex 3 -1 1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 3 -3 3
   vertex 5 -3 3
   vertex 5 -1 3
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 3 -3 3
   vertex 5 -1 3
   vertex 3 -1 3
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 3 -3 1
   vertex 3 -1 1
   vertex 5 -1 1
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 3 -3 1
   vertex 5 -1 1
   vertex 5 -3 1
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 5 -3 5
   vertex 5 -1 5
   vertex 5 -1 7
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 5 -3 5
   vertex 5 -1 7
   vertex 5 -3 7
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 3 -3 5
   vertex 3 -3 7
   vertex 3 -1 7
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 3 -3 5
   vertex 3 -1 7
   vertex 3 -1 5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 3 -3 5
   vertex 5 -3 5
   vertex 5 -3 7
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 3 -3 5
   vertex 5 -3 7
   vertex 3 -3 7
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 3 -3 7
   vertex 5 -3 7
   vertex 5 -1 7
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 3 -3 7
   vertex 5 -1 7
   vertex 3 -1 7
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 3 -3 5
   vertex 3 -1 5
   vertex 5 -1 5
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 3 -3 5
   vertex 5 -1 5
   vertex 5 -3 5
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 5 -1 -7
   vertex 5 1 -7
   vertex 5 1 -5
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 5 -1 -7
   vertex 5 1 -5
   vertex 5 -1 -5
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 3 -1 -7
   vertex 3 -1 -5
   vertex 3 1 -5
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 3 -1 -7
   vertex 3 1 -5
   vertex 3 1 -7
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 3 1 -7
   vertex 3 1 -5
   vertex 5 1 -5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 3 1 -7
   vertex 5 1 -5
   vertex 5 1 -7
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 3 -1 -7
   vertex 5 -1 -7
   vertex 5 -1 -5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 3 -1 -7
   vertex 5 -1 -5
   vertex 3 -1 -5
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 3 -1 -7
   vertex 3 1 -7
   vertex 5 1 -7
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 3 -1 -7
   vertex 5 1 -7
   vertex 5 -1 -7
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 5 -1 -5
   vertex 5 1 -5
   vertex 5 1 -3
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 5 -1 -5
   vertex 5 1 -3
   vertex 5 -1 -3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 3 -1 -5
   vertex 3 -1 -3
   vertex 3 1 -3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 3 -1 -5
   vertex 3 1 -3
   vertex 3 1 -5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 3 1 -5
   vertex 3 1 -3
   vertex 5 1 -3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 3 1 -5
   vertex 5 1 -3
   vertex 5 1 -5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 3 -1 -5
   vertex 5 -1 -5
   vertex 5 -1 -3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 3 -1 -5
   vertex 5 -1 -3
   vertex 3 -1 -3
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 5 -1 -3
   vertex 5 1 -3
   vertex 5 1 -1
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 5 -1 -3
   vertex 5 1 -1
   vertex 5 -1 -1
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 3 -1 -3
   vertex 3 -1 -1
   vertex 3 1 -1
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 3 -1 -3
   vertex 3 1 -1
   vertex 3 1 -3
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 3 -1 -1
   vertex 5 -1 -1
   vertex 5 1 -1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 3 -1 -1
   vertex 5 1 -1
   vertex 3 1 -1
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 5 -1 1
   vertex 5 1 1
   vertex 5 1 3
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 5 -1 1
   vertex 5 1 3
   vertex 5 -1 3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 3 -1 1
   vertex 3 -1 3
   vertex 3 1 3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 3 -1 1
   vertex 3 1 3
   vertex 3 1 1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 3 -1 3
   vertex 5 -1 3
   vertex 5 1 3
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 3 -1 3
   vertex 5 1 3
   vertex 3 1 3
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 3 -1 1
   vertex 3 1 1
   vertex 5 1 1
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 3 -1 1
   vertex 5 1 1
   vertex 5 -1 1
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 5 -1 5
   vertex 5 1 5
   vertex 5 1 7
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 5 -1 5
   vertex 5 1 7
   vertex 5 -1 7
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 3 -1 5
   vertex 3 -1 7
   vertex 3 1 7
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 3 -1 5
   vertex 3 1 7
   vertex 3 1 5
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 3 -1 7
   vertex 5 -1 7
   vertex 5 1 7
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 3 -1 7
   vertex 5 1 7
   vertex 3 1 7
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 3 -1 5
   vertex 3 1 5
   vertex 5 1 5
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 3 -1 5
   vertex 5 1 5
   vertex 5 -1 5
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 5 1 -3
   vertex 5 3 -3
   vertex 5 3 -1
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 5 1 -3
   vertex 5 3 -1
   vertex 5 1 -1
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 3 1 -3
   vertex 3 1 -1
   vertex 3 3 -1
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 3 1 -3
   vertex 3 3 -1
   vertex 3 3 -3
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 3 1 -1
   vertex 5 1 -1
   vertex 5 3 -1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 3 1 -1
   vertex 5 3 -1
   vertex 3 3 -1
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 3 1 -3
   vertex 3 3 -3
   vertex 5 3 -3
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 3 1 -3
   vertex 5 3 -3
   vertex 5 1 -3
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 5 1 1
   vertex 5 3 1
   vertex 5 3 3
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 5 1 1
   vertex 5 3 3
   vertex 5 1 3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 3 1 1
   vertex 3 1 3
   vertex 3 3 3
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 3 1 1
   vertex 3 3 3
   vertex 3 3 1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 3 1 3
   vertex 5 1 3
   vertex 5 3 3
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 3 1 3
   vertex 5 3 3
   vertex 3 3 3
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 3 1 1
   vertex 3 3 1
   vertex 5 3 1
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 3 1 1
   vertex 5 3 1
   vertex 5 1 1
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 5 1 5
   vertex 5 3 5
   vertex 5 3 7
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 5 1 5
   vertex 5 3 7
   vertex 5 1 7
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 3 1 5
   vertex 3 1 7
   vertex 3 3 7
  endloop
 endfacet
 facet normal -1 0 0
  outer loop
   vertex 3 1 5
   vertex 3 3 7
   vertex 3 3 5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 3 3 5
   vertex 3 3 7
   vertex 5 3 7
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 3 3 5
   vertex 5 3 7
   vertex 5 3 5
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 3 1 7
   vertex 5 1 7
   vertex 5 3 7
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 3 1 7
   vertex 5 3 7
   vertex 3 3 7
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 3 1 5
   vertex 3 3 5
   vertex 5 3 5
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 3 1 5
   vertex 5 3 5
   vertex 5 1 5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 3 5 -7
   vertex 3 5 -5
   vertex 5 5 -5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 3 5 -7
   vertex 5 5 -5
   vertex 5 5 -7
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 3 3 -7
   vertex 5 3 -7
   vertex 5 3 -5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 3 3 -7
   vertex 5 3 -5
   vertex 3 3 -5
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 3 3 -7
   vertex 3 5 -7
   vertex 5 5 -7
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 3 3 -7
   vertex 5 5 -7
   vertex 5 3 -7
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 3 5 -5
   vertex 3 5 -3
   vertex 5 5 -3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 3 5 -5
   vertex 5 5 -3
   vertex 5 5 -5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 3 3 -5
   vertex 5 3 -5
   vertex 5 3 -3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 3 3 -5
   vertex 5 3 -3
   vertex 3 3 -3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 3 5 -3
   vertex 3 5 -1
   vertex 5 5 -1
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 3 5 -3
   vertex 5 5 -1
   vertex 5 5 -3
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 3 3 -1
   vertex 5 3 -1
   vertex 5 5 -1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 3 3 -1
   vertex 5 5 -1
   vertex 3 5 -1
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 3 5 1
   vertex 3 5 3
   vertex 5 5 3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 3 5 1
   vertex 5 5 3
   vertex 5 5 1
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 3 3 1
   vertex 3 5 1
   vertex 5 5 1
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 3 3 1
   vertex 5 5 1
   vertex 5 3 1
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 3 5 3
   vertex 3 5 5
   vertex 5 5 5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 3 5 3
   vertex 5 5 5
   vertex 5 5 3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 3 3 3
   vertex 5 3 3
   vertex 5 3 5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 3 3 3
   vertex 5 3 5
   vertex 3 3 5
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 3 3 5
   vertex 5 3 5
   vertex 5 5 5
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 3 3 5
   vertex 5 5 5
   vertex 3 5 5
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 7 -5 -7
   vertex 7 -3 -7
   vertex 7 -3 -5
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 7 -5 -7
   vertex 7 -3 -5
   vertex 7 -5 -5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 5 -3 -7
   vertex 5 -3 -5
   vertex 7 -3 -5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 5 -3 -7
   vertex 7 -3 -5
   vertex 7 -3 -7
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 5 -5 -7
   vertex 7 -5 -7
   vertex 7 -5 -5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 5 -5 -7
   vertex 7 -5 -5
   vertex 5 -5 -5
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 5 -5 -7
   vertex 5 -3 -7
   vertex 7 -3 -7
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 5 -5 -7
   vertex 7 -3 -7
   vertex 7 -5 -7
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 7 -5 -5
   vertex 7 -3 -5
   vertex 7 -3 -3
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 7 -5 -5
   vertex 7 -3 -3
   vertex 7 -5 -3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 5 -3 -5
   vertex 5 -3 -3
   vertex 7 -3 -3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 5 -3 -5
   vertex 7 -3 -3
   vertex 7 -3 -5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 5 -5 -5
   vertex 7 -5 -5
   vertex 7 -5 -3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 5 -5 -5
   vertex 7 -5 -3
   vertex 5 -5 -3
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 7 -5 -3
   vertex 7 -3 -3
   vertex 7 -3 -1
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 7 -5 -3
   vertex 7 -3 -1
   vertex 7 -5 -1
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 5 -3 -3
   vertex 5 -3 -1
   vertex 7 -3 -1
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 5 -3 -3
   vertex 7 -3 -1
   vertex 7 -3 -3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 5 -5 -3
   vertex 7 -5 -3
   vertex 7 -5 -1
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 5 -5 -3
   vertex 7 -5 -1
   vertex 5 -5 -1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 5 -5 -1
   vertex 7 -5 -1
   vertex 7 -3 -1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 5 -5 -1
   vertex 7 -3 -1
   vertex 5 -3 -1
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 7 -5 1
   vertex 7 -3 1
   vertex 7 -3 3
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 7 -5 1
   vertex 7 -3 3
   vertex 7 -5 3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 5 -3 1
   vertex 5 -3 3
   vertex 7 -3 3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 5 -3 1
   vertex 7 -3 3
   vertex 7 -3 1
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 5 -5 1
   vertex 7 -5 1
   vertex 7 -5 3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 5 -5 1
   vertex 7 -5 3
   vertex 5 -5 3
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 5 -5 1
   vertex 5 -3 1
   vertex 7 -3 1
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 5 -5 1
   vertex 7 -3 1
   vertex 7 -5 1
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 7 -5 3
   vertex 7 -3 3
   vertex 7 -3 5
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 7 -5 3
   vertex 7 -3 5
   vertex 7 -5 5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 5 -3 3
   vertex 5 -3 5
   vertex 7 -3 5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 5 -3 3
   vertex 7 -3 5
   vertex 7 -3 3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 5 -5 3
   vertex 7 -5 3
   vertex 7 -5 5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 5 -5 3
   vertex 7 -5 5
   vertex 5 -5 5
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 5 -5 5
   vertex 7 -5 5
   vertex 7 -3 5
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 5 -5 5
   vertex 7 -3 5
   vertex 5 -3 5
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 7 3 -7
   vertex 7 5 -7
   vertex 7 5 -5
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 7 3 -7
   vertex 7 5 -5
   vertex 7 3 -5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 5 5 -7
   vertex 5 5 -5
   vertex 7 5 -5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 5 5 -7
   vertex 7 5 -5
   vertex 7 5 -7
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 5 3 -7
   vertex 7 3 -7
   vertex 7 3 -5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 5 3 -7
   vertex 7 3 -5
   vertex 5 3 -5
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 5 3 -7
   vertex 5 5 -7
   vertex 7 5 -7
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 5 3 -7
   vertex 7 5 -7
   vertex 7 3 -7
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 7 3 -5
   vertex 7 5 -5
   vertex 7 5 -3
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 7 3 -5
   vertex 7 5 -3
   vertex 7 3 -3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 5 5 -5
   vertex 5 5 -3
   vertex 7 5 -3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 5 5 -5
   vertex 7 5 -3
   vertex 7 5 -5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 5 3 -5
   vertex 7 3 -5
   vertex 7 3 -3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 5 3 -5
   vertex 7 3 -3
   vertex 5 3 -3
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 7 3 -3
   vertex 7 5 -3
   vertex 7 5 -1
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 7 3 -3
   vertex 7 5 -1
   vertex 7 3 -1
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 5 5 -3
   vertex 5 5 -1
   vertex 7 5 -1
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 5 5 -3
   vertex 7 5 -1
   vertex 7 5 -3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 5 3 -3
   vertex 7 3 -3
   vertex 7 3 -1
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 5 3 -3
   vertex 7 3 -1
   vertex 5 3 -1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 5 3 -1
   vertex 7 3 -1
   vertex 7 5 -1
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 5 3 -1
   vertex 7 5 -1
   vertex 5 5 -1
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 7 3 1
   vertex 7 5 1
   vertex 7 5 3
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 7 3 1
   vertex 7 5 3
   vertex 7 3 3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 5 5 1
   vertex 5 5 3
   vertex 7 5 3
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 5 5 1
   vertex 7 5 3
   vertex 7 5 1
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 5 3 1
   vertex 7 3 1
   vertex 7 3 3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 5 3 1
   vertex 7 3 3
   vertex 5 3 3
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 5 3 1
   vertex 5 5 1
   vertex 7 5 1
  endloop
 endfacet
 facet normal 0 0 -1
  outer loop
   vertex 5 3 1
   vertex 7 5 1
   vertex 7 3 1
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 7 3 3
   vertex 7 5 3
   vertex 7 5 5
  endloop
 endfacet
 facet normal 1 0 0
  outer loop
   vertex 7 3 3
   vertex 7 5 5
   vertex 7 3 5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 5 5 3
   vertex 5 5 5
   vertex 7 5 5
  endloop
 endfacet
 facet normal 0 1 0
  outer loop
   vertex 5 5 3
   vertex 7 5 5
   vertex 7 5 3
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 5 3 3
   vertex 7 3 3
   vertex 7 3 5
  endloop
 endfacet
 facet normal 0 -1 0
  outer loop
   vertex 5 3 3
   vertex 7 3 5
   vertex 5 3 5
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 5 3 5
   vertex 7 3 5
   vertex 7 5 5
  endloop
 endfacet
 facet normal 0 0 1
  outer loop
   vertex 5 3 5
   vertex 7 5 5
   vertex 5 5 5
  endloop
 endfacet
endsolid ai_3d_dual_solid
```

Текстовая альтернатива: математическая проекция на XY — «AI», на ZY — «3D». [Проверяемые маски и статистика](../../assets/dual-solid/geometry.json).
