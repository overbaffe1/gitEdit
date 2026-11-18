# Полевой атлас GitHub

**Открыть экспонат:** [триптих целиком](../assets/night-shift/bench-master.jpg) · [механическая капсула](../assets/crystal-theatre.gif) · [маршрут на карте](../assets/survey.geojson) · [шахматный этюд](../assets/mate-in-one.svg). Здесь собраны исходные файлы и примеры из других проектов.

<a href="samples/atlas-plate.svg"><img src="samples/atlas-plate.svg" width="680" alt="Полевой атлас gitEdit. Образец № 1 — кристалл с шестью вершинами, двенадцатью рёбрами и восемью гранями."></a>

## Выбери маршрут

| Хочу… | Куда идти |
|---|---|
| Подобрать **фон, фактуру и марку проекта** | [Пейзаж](../assets/polar-cover.svg) · [печатная проба кольца](../assets/ring-screen.svg) · [марка](../assets/seal-crystal.svg) · [форзац](../assets/tile-frieze.svg) |
| Вставить модель, карту, формулу или диаграмму **прямо в Markdown** | [Карты и 3D](relief.md) · [диаграммы, формулы и типографика](native.md) — примеры, исходники и способ повторить |
| Посмотреть, как GitHub показывает **обычный файл** | [Фильтр в CSV](samples/palettes.csv) · [блокнот Jupyter](samples/crystal.ipynb) |
| Подсмотреть идею **в другом проекте** | [Разбор публичных репозиториев](inspiration.md) — готовые GIF, SVG, профили, игры и сайты; рядом указано, чем их сделали |
| Оформить **не только README** | [Профиль, карточка ссылки, формы, релизы, Wiki и Pages](surfaces.md) — где виден результат и что надо включить |
| Забрать готовую шапку, бейджи, змейку или целый шаблон | [Шаблон проекта](../templates/PROJECT-README-TEMPLATE.md) · [шаблон профиля](../templates/PROFILE-README-TEMPLATE.md) · [workflow змейки](../templates/profile-snake-workflow.yml) |

## Витрина файлов

Открывай **название**, не кнопку Raw: нам нужен просмотрщик GitHub. Все экспонаты в таблице хранятся в этом репозитории. Чтобы просто посмотреть, ничего устанавливать, запускать или авторизовывать не нужно.

| Экспонат | Что попробовать |
|---|---|
| [Синий 3D-просмотрщик GitHub · Кристалл (`.stl`)](../assets/crystal.stl) | Потяни за модель, приблизь колесом, переключи поверхность на каркас. Это настоящая замкнутая сетка, а не анимация вращения. |
| [Карта · Две точки и профиль (`.geojson`)](../assets/survey.geojson) | Приблизь ломаную между A и B. Это учебные координаты, не туристический трек. |
| [Карта · Соседние листы (`.topojson`)](../assets/sheets.topojson) | Найди общий край двух полигонов. В исходнике он записан один раз. |
| [Таблица · Краски gitEdit (`.csv`)](samples/palettes.csv) | Введи `Чертёж` в фильтр над таблицей: останутся светлый и тёмный наборы. Номер строки даёт ссылку на неё. TSV работает аналогично. |
| [Блокнот · Пересчёт граней (`.ipynb`)](samples/crystal.ipynb) | Под ячейкой Python уже сохранён результат `6 − 12 + 8 = 2`. На GitHub это просмотр, не работающий Jupyter-сервер. Для пересчёта нужны блокнот и STL рядом. |
| [Схема · Путь от эскиза до тиража (`.mmd`)](samples/edition.mmd) | Открой схему состояний отдельным файлом; [готовый PNG](../assets/mermaid/edition.png) открывается без движка Mermaid. |
| [Печатный лист (`.pdf`)](samples/field-sheet.pdf) | Одна страница, которую можно рассмотреть или скачать для печати. Важные ссылки оставляй рядом в Markdown: просмотрщик PDF их игнорирует. |
| [Карточка ссылки (`.png`)](samples/social-preview.png) · [мастер (`.svg`)](samples/atlas-plate.svg) | Готовый PNG 1280 × 640 для Social preview. Открой SVG как текст, чтобы заменить надписи и цвета, затем экспортируй новый PNG. [Как загрузить Social preview](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview) |

**Не только Markdown:** сравни [README проекта Asciidoctor в `.adoc`](https://github.com/asciidoctor/asciidoctor/blob/main/README.adoc) и [руководство Python в `.rst`](https://github.com/python/cpython/blob/main/Doc/howto/argparse.rst). Перечень распознаваемых форматов — в [github/markup](https://github.com/github/markup). Это не значит, что GitHub выполнит все директивы полноценной сборки документации.

**Если вместо экспоната виден код:** сначала открой файл на github.com. Для 3D проверь поддержку WebGL. Большие файлы могут не получить предпросмотр; например, для STL документация указывает предел 10 МБ. Для любого важного демо оставляй подпись и ссылку на исходник. Управление, лимиты и режимы просмотра: GitHub Docs [1](https://docs.github.com/en/repositories/working-with-files/using-files/working-with-non-code-files).

*Срез для github.com: 17 ноября 2026 года. Это атлас оформления и представления проектов, не перечень всех настроек платформы. Авторы, исходные проекты и условия переиспользования экспонатов указаны в таблице «Откуда взялись экспонаты» в [исходнике README](https://github.com/overbaffe1/gitEdit/blob/main/README.md?plain=1).*
