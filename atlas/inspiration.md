[← Полевой атлас](README.md) · [Нативные альтернативы](native.md)

# Как это сделано в других репозиториях

Сначала нажми на **результат**, потом на источник. Разница принципиальна: записанному GIF не нужен сервер при просмотре; карточка по URL зависит от сервиса; «живой» README часто просто переписывает бот. В этом атласе чужие демо открываются по ссылке; новые workflow и приложения не подключались. Ссылки сверены с проектами 17 ноября 2026 года.

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

## Где искать дальше

- [Awesome README](https://github.com/matiassingers/awesome-readme#examples) — примеры **проектов**; особенно полезно сравнивать первый экран и объяснение архитектуры.
- [Awesome GitHub Profile README](https://github.com/abhisheknaiidu/awesome-github-profile-readme#categories) — подборка **профилей** по типу: игры, автоматизация, минимализм.
- [Beautify GitHub Profile](https://github.com/rzashakeri/beautify-github-profile) — большой каталог виджетов. Проверяй демо у оригинального автора: публичные инстансы и условия доступа меняются.

**Перед переносом:** смотри лицензию конкретного проекта и его иллюстраций. Для внешней картинки оставь `alt` и обычную ссылку. Для автоматизации начни с ручного запуска, проверь разрешения и фиксируй сторонние Actions на проверенной версии (лучше на полном SHA). Не вставляй токены в Markdown или параметры картинки.
