[← Полевой атлас](README.md) · [Нативные альтернативы](native.md)

# Как это сделано в других репозиториях

Сначала нажми на **результат**, потом на источник. Разница принципиальна: записанному GIF не нужен сервер при просмотре; карточка по URL зависит от сервиса; «живой» README часто просто переписывает бот. В этом атласе чужие демо открываются по ссылке; новые workflow и приложения не подключались. Ссылки сверены с проектами 17 ноября 2026 года.

## Линейка, набранная текстом

В [README spark](https://github.com/holman/spark/blob/ab88ac6f8f33698f39ece2f109b1117ef39a68eb/README.md) числовой ряд помещается в строку: каждый следующий уровень — чуть более высокий печатный знак. В [дереве каталогов Optimism](https://github.com/ethereum-optimism/optimism/blob/7047a367dc263a63828a297abd5a1302d9ea23c0/README.md#directory-structure) ветки тоже текстовые, а названия папок внутри `<pre>` остаются ссылками.

В [партитуре пауз](../templates/blocks/cue-sheet.md) эти два приёма встречаются: ссылка ведёт к GIF, а ритм записи можно прочитать, не открывая её. Дорожки не растянуты до одинаковой длины: после 3,71 с у терминала уже пусто, а у кристалла справа ещё видны сгибы. В основе — задержки из трёх готовых файлов; ни внешнего сервиса, ни картинки для шкалы нет.

## Краски, которые не нужно подбирать пипеткой

В [README Nord](https://github.com/nordtheme/nord/blob/1cef71605416a222e57225b544540ce0fcec18d4/README.md) цвета собраны в [карточки с подписями](https://github.com/nordtheme/assets/blob/5e00ff689823cb91dd5d013bd4ebae06e79279c5/static/images/artworks/coloring/cards.svg), а для редактора лежит [палитра `.gpl`](https://github.com/nordtheme/nord/blob/1cef71605416a222e57225b544540ce0fcec18d4/src/swatches/nord.gpl). У Rosé Pine интересен другой приём: [в CSS](https://github.com/rose-pine/palette/blob/92af52b465ab6e47437aca223c9b8d3009a2023b/dist/css/rose-pine-media.css) имя краски остаётся тем же, а её значение меняется по `prefers-color-scheme`.

В gitEdit [два оттиска одной пробы](../assets/inkbook/press.svg) видны одновременно: можно сравнить текст и акцент, не переключая тему. [Карточки, палитра и CSS](samples/inkbook/) берут краски из нашего [CSV](samples/palettes.csv). От Nord и Rosé Pine взяты приёмы подачи, не рисунки и не цвета.

## Виньетка вместо ещё одного баннера

В [README Catppuccin для Kitty](https://github.com/catppuccin/kitty/blob/177d447f0c3626959ef001b4605f5d844541fd63/README.md) в конце стоит [тонкая линия с силуэтом кота](https://github.com/catppuccin/catppuccin/blob/d09787dd98ca6fba08af5ef2ae94a7e09f17daca/assets/footers/gray0_ctp_on_line.svg). Это украшение страницы: ему не нужны ни надпись, ни кнопка. В gitEdit под триптихом и после печатного листа повторяется своя [виньетка с мотыльком](../assets/moth-rule.svg). Медный и мятный оттенки взяты из панорамы мастерской, а сквозь прорези в крыльях виден фон страницы.

## Первый экран без баннера: вид и код одного блока

В [Best-README-Template](https://github.com/othneildrew/Best-README-Template/blob/fc444eb7b04b2e4863f6080b1507a219e95103fa/README.md) под названием стоят ссылки на документацию, демо и шаблоны Issues. Полезный приём здесь не логотип, а подписи к ссылкам: ещё до прокрутки ясно, куда каждая ведёт. У [GitHub CLI](https://github.com/cli/cli/blob/e1219499a578b69e3437adaa31cd60614e23c802/README.md) сразу после названия коротко объяснено, для чего нужен `gh`.

В [каталоге gitEdit](../templates/) на один блок приходится один `.md`, а не картинка и отдельный листинг. Сравни [переключатель в вёрстке](../templates/blocks/quickstart.md) и [его исходные строки](../templates/blocks/quickstart.md?plain=1): в первом режиме можно выбрать способ, во втором — забрать обе инструкции вместе с переключателем. Параметр [`?plain=1` описан в документации GitHub](https://github.com/github/docs/blob/49a012fa50b42661a59bfcb80dad5910bced5e81/content/get-started/writing-on-github/working-with-advanced-formatting/creating-a-permanent-link-to-a-code-snippet.md). Это две страницы просмотра **одного файла**, а не вкладки, нарисованные внутри Markdown.

**Как связать раскрытия.** В [README node-core-utils](https://github.com/nodejs/node-core-utils/blob/27468f5b97caa9d415f9928bbe1bdf0c463df122/README.md) две инструкции объединены общим `name`. В [сравнении ARM64 и ARM32 у Samsung](https://github.com/Samsung/escargot/blob/6a2b740857f619e6d4c6f1330dfc8fa331b71926/README.md) так же переключаются результаты для архитектур. Это [свойство самого `<details>`](https://github.com/mdn/content/blob/5d53607e3645a456fce6564424823169157b74b1/files/en-us/web/html/reference/elements/details/index.md), а не скрипт. В [шаблоне инструкций](../templates/blocks/quickstart.md) при открытии «В терминале» раздел «В браузере» закроется. В просмотрщике без поддержки групп оба раздела всё равно можно прочесть.

## Терминал и рисунок вместо скриншота

| Посмотреть результат | Как повторить приём |
|---|---|
| [VHS · готовая запись терминала](https://github.com/charmbracelet/vhs/blob/main/examples/demo.gif) | Открой [сценарий этой записи](https://github.com/charmbracelet/vhs/blob/main/examples/demo.tape): ввод, паузы и размеры терминала описаны текстом. Генерируй GIF заново, когда меняются команды. |
| [Freeze · код в рамке с тенью](https://github.com/charmbracelet/freeze/blob/main/test/golden/svg/shadow.svg) | [Freeze](https://github.com/charmbracelet/freeze#examples) превращает код или цветной вывод терминала в картинку. Хороший формат для одного экрана. Команду для копирования оставь и текстом. |
| [agg · запись сеанса как GIF](https://github.com/asciinema/agg/blob/main/demo.gif) | В отличие от VHS, [agg](https://github.com/asciinema/agg) берёт уже записанный сеанс asciinema. Проверь запись перед публикацией: история команд попадает в кадр. |
| [D2 · результат компоновки схемы](https://github.com/d2lang/d2/blob/master/docs/assets/example.svg) | В [примере D2](https://github.com/d2lang/d2#what-does-d2-look-like) сравни текст и результат. В README вставляют экспортированный SVG; блок `d2` сам по себе не заменяет Mermaid. |
| [Excalidraw · доска с рисунками от руки](https://github.com/excalidraw/excalidraw#readme) | В [редакторе](https://excalidraw.com/) нарисуй схему, сохрани редактируемый `.excalidraw`, для читателей экспортируй SVG или PNG. |

## Показать активность, не вывешивая стену бейджей

| Посмотреть результат | Как повторить приём |
|---|---|
| [3D Contrib · ночной город](https://github.com/yoshi389111/github-profile-3d-contrib/blob/main/docs/demo/profile-night-view.svg) | [Action автора](https://github.com/yoshi389111/github-profile-3d-contrib) превращает календарь вкладов в изометрический SVG. Вращать его нельзя — это иллюстрация. |
| [GitHub Skyline · фото модели и вид в терминале](https://github.com/github/gh-skyline#readme) | [Расширение GitHub CLI](https://github.com/github/gh-skyline#usage) строит уже **геометрию STL** по истории вкладов. Чтобы понять разницу с SVG, [покрути наш маленький STL](../assets/crystal.stl). |
| [Metrics · год на изометрическом календаре](https://github.com/lowlighter/metrics/blob/examples/metrics.plugin.isocalendar.fullyear.svg) | В [библиотеке плагинов](https://github.com/lowlighter/metrics#readme) выбери один модуль, а не всю панель сразу. Генератор может сохранять результат в репозиторий. |
| [snk · змейка на настоящем поле вкладов](https://github.com/Platane/snk/blob/output/github-contribution-grid-snake.gif) | [Platane/snk](https://github.com/Platane/snk) генерирует картинку, это не управляемая игра внутри Markdown. В gitEdit уже есть [неактивный шаблон workflow](../templates/profile-snake-workflow.yml). |
| [Readme Stats · галерея карточек](https://github.com/anuraghazra/github-readme-stats#all-demos) | Статистика, языки и карточка репозитория. [Авторы прямо предупреждают о лимитах публичного сервиса](https://github.com/anuraghazra/github-readme-stats#important-notices-); для предсказуемой картинки можно генерировать файл через Actions. |
| [Star History · график звёзд во времени](https://github.com/star-history/star-history#readme) | Вместо одного числа видно, **когда** менялся интерес к проекту. Это внешний сервис; оставь читателю и текстовую ссылку на страницу графика. |

## README, который меняется между посещениями

| Посмотреть результат | Где на самом деле живёт интерактивность |
|---|---|
| [Tim Burgan · шахматная доска](https://github.com/timburgan/timburgan#tims-community-chess-tournament) | Клетки — картинки в таблице. Ссылки предлагают ход через Issue, а [workflow](https://github.com/timburgan/timburgan/tree/master/.github/workflows) обновляет позицию. Чтобы рассмотреть доску, отправлять ход не нужно. |
| [Simon Willison · свежие релизы, статьи и TIL](https://github.com/simonw/simonw#readme) | Три обычных списка ссылок, никаких счётчиков. Сравни профиль с его [сборкой README](https://github.com/simonw/simonw/blob/main/.github/workflows/build.yml). |
| [Blog Post Workflow · варианты ленты](https://github.com/gautamkrishnar/blog-post-workflow#advanced-usage-examples) | [Action](https://github.com/gautamkrishnar/blog-post-workflow) вставляет записи RSS в отмеченный участок Markdown; остальную страницу можно редактировать вручную. |
| [All Contributors · таблица участников](https://github.com/all-contributors/allcontributors.org/blob/main/src/assets/reference/contributors-table-small.png) | Под портретами отмечены разные виды вклада: документация, дизайн, ответы на вопросы. У [самого проекта](https://github.com/all-contributors/allcontributors.org#the-all-contributors-table) есть и таблица, и объяснение формата. |

## Лёгкая шапка или отдельный сайт

| Посмотреть результат | Граница возможностей |
|---|---|
| [Typing SVG · редактор с предпросмотром](https://readme-typing-svg.demolab.com/demo/) | Текст печатает [генерируемый SVG](https://github.com/DenverCoder1/readme-typing-svg), не JavaScript в Markdown. Важное имя или описание не прячь только в анимации. |
| [Cayman · опубликованная страница](https://pages-themes.github.io/cayman/) | Сравни с [репозиторием темы](https://github.com/pages-themes/cayman): свои стили и навигация работают на Pages, не в рамке README. |
| [giscus · обсуждения под страницей](https://giscus.app/) | [giscus](https://github.com/giscus/giscus#how-it-works) связывает комментарии **на сайте** с GitHub Discussions. В README поставь ссылку; установка приложения и подключение обсуждений — отдельное решение. |
| [Satori · редактор карточки ссылки](https://og-playground.vercel.app/) | Поменяй текст в редакторе и сравни вкладки SVG и PNG. [Satori](https://github.com/vercel/satori) преобразует разметку в SVG; для Social preview GitHub нужен уже экспортированный растр. |
| [reveal.js · листаемая презентация](https://revealjs.com/demo/) | Нажми пробел для следующего слайда, Esc для общего плана. [Исходный HTML демо](https://github.com/hakimel/reveal.js/blob/master/demo.html) размещают на сайте, а в README дают обложку-ссылку или PDF. |

## Как спрятать три буквы в одном предмете

В [модели ondras/3](https://github.com/ondras/3/blob/3749f6a674fc7fdc233ff7aea082af28939f5c2b/geb.scad) три буквы выдавливаются в глубину. Пересечение объёмов даёт предмет, который читается по-разному с разных сторон. У [Shadow Cube Generator](https://github.com/flurl/shadow_cube_generator/blob/d53eff7aa7536f51309e3fe3dd8c599db09acef1/README.md) другой способ задать форму: рисуешь три вида по клеткам.

Для README не нужен ни редактор, ни встроенная 3D-сцена. В [нашей кинопетле](../assets/shadow-type/git.gif) вращается одна сетка с проекциями **G / I / T**. [Неподвижный лист](../assets/shadow-type/proof.png) показывает все три сразу, а [STL](../assets/shadow-type/git.stl) можно повернуть отдельно. Буквы нарисованы по клеткам специально для gitEdit; ни шрифт, ни сетка из чужого проекта не копировались.

## Что рисуют два звуковых канала

В [демо osci-render](https://github.com/jameshball/osci-render/blob/25f5938e5983af8803b5b090176bde1b7e35180e/images/blender.gif) движение из Blender выводится на осциллограф. Хорошая точка входа — [фигура Лиссажу из oscli](https://github.com/ismael-joffroy-chandoutis/oscli/blob/6f01c704550d29fece609b4041f41f27602077f1/examples/lissajous.png). В [описании oscli](https://github.com/ismael-joffroy-chandoutis/oscli/blob/6f01c704550d29fece609b4041f41f27602077f1/README.md) есть ключ к рисунку: в режиме X/Y левый канал отклоняет луч по горизонтали, правый — по вертикали. Это не спектрограмма: частоты раскладывать не надо.

У [нашей аурелии](../assets/aurelia/swim.gif) нет команды «поднять перо». [Генератор сигнала](samples/aurelia/xy_signal.py) проводит луч до кончика каждого щупальца и возвращает к куполу. [Рендер](samples/aurelia/render.py) заново открывает [готовый WAV](../assets/aurelia/aurelia.wav) и строит кадр по 800 соседним стереопарам. Тот же файл можно открыть в стереоосциллографе: **X = L, Y = R**, один обход за 1/60 секунды. Или распаковать [наш осциллограф](../assets/aurelia/scope.zip?raw=true): в нём уже лежит запись. Контур, сигнал и оформление сделаны для gitEdit; чужие записи и кадры не использовались.

## Один PNG на светлой и тёмной бумаге

В [демо HideImageMaker](https://github.com/wuyr/HideImageMaker/blob/9fc2d095f4c7bd1119f1be35c4080cfe03472553/preview.gif) из двух исходных картинок собирают одну. Приём называют *mirage tank*: [пояснение со схемой смешивания](https://github.com/lilyco-42/mirage-tank/blob/4f0c5f3233f1c9868398de9c8c2619941417b8e0/README.md). Меняется фон под прозрачными пикселями, а не URL картинки. Для README достаточно одного обычного `<img>`.

У [нашего листа](../assets/twilight/glass.png) две печатные формы: [шерсть](samples/twilight/fox.png) и [перья](samples/twilight/owl.png). Это полутоновые маски: светлая точка означает больше краски. Портреты сгенерированы для gitEdit, переведены в маски и совмещены по глазам. В сам README маски не загружаются.

**Секрет пикселя.** Пусть лисице нужна доля `d` тёмной краски, сипухе — `n` белой. Непрозрачность равна `d + n` (не больше единицы), остальное просвечивает. На белой бумаге белая краска незаметна — остаётся только штрих лисицы. На графите исчезает тёмная краска. У [двойного оттиска](../assets/twilight/proof.png) подложки `#ffffff` и `#0d1117`; на промежуточном сером могут проступить оба портрета. [Сборщик](samples/twilight/print.py) сначала записывает прозрачный PNG, затем читает его обратно для оттиска. В [карманном столе](../assets/twilight/table.zip?raw=true) лежит тот же файл.

## Игра, набранная шрифтом

В [разборе Fontemon](https://github.com/mmulet/code-relay/blob/3a6b651445aac3b8dc6fad64b4234b6950828dbe/markdown/HowIDidIt.md) автор показывает, как превратить типографскую подстановку в переход между игровыми сценами. У него есть и [редактор таких игр](https://github.com/mmulet/font-game-engine/blob/56ca281abedeaf875e4fc871cf65674f79cd3e25/README.md). Другой пример — [крестики-нолики Mabi19](https://github.com/Mabi19/tic-tac-toe-font/blob/ec8761e0c3a992d57f546e9716fc13e3fff23d29/README.md): партия задаётся последовательностью набранных знаков.

Для [наборного склада](../assets/typecase/dock.ttf) мы сделали свою комнату и нарисовали робота, ящик и причал. [Сборщик](samples/typecase/build_font.py) обходит [план](samples/typecase/room.txt): с учётом стен, толчков и остановки после доставки достижимы **256 положений**. Все они записаны в обычном TTF. При наборе правило OpenType `calt` читает новую цифру в контексте предыдущей комнаты и выбирает следующий рисунок. Вторая подстановка заменяет пройденные комнаты пустыми знаками нулевой ширины. Текст не меняется: сотри цифру — шрифт наберёт оставшуюся строку заново.

[Запись](../assets/typecase/delivery.gif) отпечатана с готового TTF через HarfBuzz и FreeType. В [офлайн-пробнике](../assets/typecase/typecase.zip?raw=true) экранные кнопки только правят строку; с выключенным JavaScript можно по-прежнему набирать ходы в самом поле. Для игры в своём редакторе нужен набор с контекстными подстановками, а не вывод независимых символов по клеткам терминала. Чужие шрифты, уровни и спрайты не копировались.

## Рисунок, который читается в цилиндре

В [опыте FeichenFD](https://github.com/FeichenFD/cylindricalmirror/blob/e64bd8cf896f9e0e85fdb997b331ab9c9aae168e/README.md) показаны исходник, [деформированный лист A4](https://github.com/FeichenFD/cylindricalmirror/blob/e64bd8cf896f9e0e85fdb997b331ab9c9aae168e/images/test_1024_anamorph.png) и [расчётный вид в зеркале](https://github.com/FeichenFD/cylindricalmirror/blob/e64bd8cf896f9e0e85fdb997b331ab9c9aae168e/images/test_1024_anamorph_preview.png). Второй полезный разбор — [проекция в CylindricAnamorphosis](https://github.com/FDaCostaB/CylindricAnamorphosis/blob/c3d40ec9167dbd827e8f32cc9cad88e81af1cd0c/projection.c): найти пересечение с цилиндром, отразить направление относительно нормали, дойти до бумаги. Простая полярная развёртка — другой приём: сам [AnamorphMeIJ](https://github.com/phillipkent/AnamorphMeIJ/blob/cd5e6764432352d8980e496fd10fdbf44872dc65/README.md) называет её приближением.

В [нашем листе](../assets/catoptric/sheet-a4.pdf) учтена перспектива **одной заданной точки наблюдения**. Для каждой точки бумаги [печатник](samples/catoptric/print.py) ищет, куда на стенку зеркала попадёт луч. Для [проверки](../assets/catoptric/proof.png) расчёт идёт в обратную сторону: из глаза через цилиндр — к пикселю уже отпечатанного листа. [Оптический стол](../assets/catoptric/bench.zip?raw=true) знает только этот лист. Если сдвинуть глаз, конёк искривится, хотя краска не сдвинулась ни на миллиметр. [Гравюра](samples/catoptric/engraving.png) сгенерирована специально для этого опыта и оформлена как натурная карточка; ни чужие изображения, ни код проекции в репозиторий не переносились.

## Где искать дальше

- [Awesome README](https://github.com/matiassingers/awesome-readme#examples) — примеры **проектов**; особенно полезно сравнивать первый экран и объяснение архитектуры.
- [Awesome GitHub Profile README](https://github.com/abhisheknaiidu/awesome-github-profile-readme#categories) — подборка **профилей** по типу: игры, автоматизация, минимализм.
- [Beautify GitHub Profile](https://github.com/rzashakeri/beautify-github-profile) — большой каталог виджетов. Проверяй демо у оригинального автора: публичные инстансы и условия доступа меняются.

**Перед переносом:** смотри лицензию конкретного проекта и его иллюстраций. Для внешней картинки оставь `alt` и обычную ссылку. Для автоматизации начни с ручного запуска, проверь разрешения и фиксируй сторонние Actions на проверенной версии (лучше на полном SHA). Не вставляй токены в Markdown или параметры картинки.
