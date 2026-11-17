[← Полевой атлас](README.md) · [Диаграммы и набор текста](native.md)

# Карты и третье измерение

Три нативных экспоната: [кристалл](../assets/crystal.stl) · [профиль местности](../assets/survey.geojson) · [общая граница](../assets/sheets.topojson). Здесь нет скриптов, ключей карт или внешнего генератора изображений. Просмотрщики предоставляет сам GitHub. Синтаксис и ограничения: GitHub Docs [2](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams).

## Кристалл

Потяни за модель: верхняя и нижняя вершины чуть смещены относительно пояса. В режиме каркаса удобно пересчитать треугольники. Если встроенное окно не загрузилось, [открой отдельный STL](../assets/crystal.stl) или [посмотри статичный рисунок](samples/atlas-plate.svg).

```stl
solid field_crystal
  facet normal 0.5906538 0.7269586 0.3502274
    outer loop
      vertex 3 -1 36
      vertex 16 0 12
      vertex 0 13 12
    endloop
  endfacet
  facet normal 0.4731097 0.5822889 -0.6611405
    outer loop
      vertex -2 1 0
      vertex 0 13 12
      vertex 16 0 12
    endloop
  endfacet
  facet normal -0.5568154 0.6853112 0.4693668
    outer loop
      vertex 3 -1 36
      vertex 0 13 12
      vertex -16 0 12
    endloop
  endfacet
  facet normal -0.5236315 0.6444695 -0.5571976
    outer loop
      vertex -2 1 0
      vertex -16 0 12
      vertex 0 13 12
    endloop
  endfacet
  facet normal -0.5713854 -0.7032436 0.4230450
    outer loop
      vertex 3 -1 36
      vertex -16 0 12
      vertex 0 -13 12
    endloop
  endfacet
  facet normal -0.4923218 -0.6059346 -0.6248700
    outer loop
      vertex -2 1 0
      vertex 0 -13 12
      vertex -16 0 12
    endloop
  endfacet
  facet normal 0.6024457 -0.7414717 0.2954301
    outer loop
      vertex 3 -1 36
      vertex 0 -13 12
      vertex 16 0 12
    endloop
  endfacet
  facet normal 0.4435471 -0.5459041 -0.7108127
    outer loop
      vertex -2 1 0
      vertex 16 0 12
      vertex 0 -13 12
    endloop
  endfacet
endsolid field_crystal
```

**Как забрать:** в режиме **Code** скопируй блок вместе с ограждением `stl`. Другой вариант — вставь полный текст [ASCII STL](../assets/crystal.stl) между строками ` ```stl ` и ` ``` `. Там должен быть текст `solid … endsolid`, а не имя файла. Для бинарного STL используй ссылку на файл, а не блок с двоичными данными.

У выпуклого кристалла 6 вершин, 12 рёбер и 8 граней. [Блокнот с подсчётом](samples/crystal.ipynb) проверяет это по файлу, а не по рисунку.

## Две точки и линия

Приблизь ломаную, соединяющую A и B. `Point` задаёт одну отметку, `LineString` — профиль через несколько отсчётов. Координаты учебные; порядок чисел — **долгота, широта**, не наоборот.

```geojson
{
  "type": "FeatureCollection",
  "features": [
    {"type": "Feature", "properties": {"title": "Условная точка A"}, "geometry": {"type": "Point", "coordinates": [-19.10, 64.20]}},
    {"type": "Feature", "properties": {"title": "Условная точка B"}, "geometry": {"type": "Point", "coordinates": [-18.86, 64.28]}},
    {"type": "Feature", "properties": {"title": "Учебный профиль A–B", "stroke": "#7156a0"}, "geometry": {"type": "LineString", "coordinates": [[-19.10, 64.20], [-19.02, 64.26], [-18.94, 64.24], [-18.86, 64.28]]}}
  ]
}
```

[Открыть карту отдельно или скопировать данные](../assets/survey.geojson). Чтобы перенести её в свой README, вставь содержимое файла в блок с меткой `geojson`.

## Два листа, одна граница

Здесь интересен стык: два соседних полигона используют одну и ту же дугу. `0` — первая дуга в прямом направлении, `-1` — она же в обратном. Попробуй в копии файла вставить `[-18.98, 64.24]` между концами первой дуги: у обоих полигонов появится один и тот же излом, а остальные дуги менять не придётся.

```topojson
{
  "type": "Topology",
  "objects": {
    "sheets": {"type": "GeometryCollection", "geometries": [
      {"type": "Polygon", "properties": {"title": "Западный лист", "fill": "#9469bd"}, "arcs": [[0, 1]]},
      {"type": "Polygon", "properties": {"title": "Восточный лист", "fill": "#38806e"}, "arcs": [[-1, 2]]}
    ]}
  },
  "arcs": [
    [[-19.0, 64.18], [-19.0, 64.30]],
    [[-19.0, 64.30], [-19.14, 64.30], [-19.14, 64.18], [-19.0, 64.18]],
    [[-19.0, 64.18], [-18.82, 64.18], [-18.82, 64.30], [-19.0, 64.30]]
  ]
}
```

[Открыть TopoJSON отдельно или скопировать топологию](../assets/sheets.topojson). Это пример **без** `transform`: координаты дуг абсолютные. В README используй блок `topojson`.
