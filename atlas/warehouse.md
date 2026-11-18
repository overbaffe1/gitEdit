# Склад gitEdit — полный каталог 85+ находок
> Этот файл — автопись склада: каждая находка = один self-hosted SVG + генератор `atlas/samples/*.py` + описание откуда идея.
> Всего SVG в `assets/`: **93** · vitrine в README: 55 блоков · генераторы: 127 Python-файлов.
> Все анимации — чистый SMIL/CSS, без JS, с `prefers-reduced-motion: reduce`.

## Как искать
- **Копируй Markdown**: каждый блок ниже — готовая строка вида `<p align="center"><a href="/assets/orbit-stack.svg"><img src="/assets/orbit-stack.svg">` — меняй `orbit-stack.svg` на нужный файл из таблиц
- **Пересобери**: `python3 atlas/samples/orbit-stack.py` — перепишет SVG из Python-источника
- **Тема**: меняй `&theme=dark|light|radical|tokyonight|dracula|catppuccin` в URL внешних виджетов, или палитру внутри SVG

## Stats suite (github-readme-stats, self-hosted)
| Файл | Что делает | Анимация | Откуда идея |
|---|---|---|---|
| `stats-overview.svg` | 5 tiles stars forks commits PRs issues + mini calendar fade  | 7984B | stats-overview |
| `streak-fire.svg` | current 34 longest 112 fire flicker 0.6s | 1598B | streak-fire |
| `langs-donut.svg` | donut animated dashoffset 1.2s 6 langs | 2257B | langs-donut |
| `activity-graph.svg` | area chart 31 days line+points fade 0.6s | 1653B | activity-graph |
| `waka-bar.svg` | Полоска языков по часам кодинга. | 1367B | waka-bar |
| `waka-donut.svg` | wakatime donut + 32h week | 1629B | waka-donut |
| `repo-pin-cards.svg` | 2 pinned repos | 1536B | repo-pin-cards |
| `calendar-themes.svg` | 3 theme calendars | 1727B | calendar-themes |
| `trophies-ranked.svg` | 4 ranks with glow | 2365B | trophies-ranked |
| `trophy-shelf.svg` | Трофеи по уровням, как в играх. | 2210B | trophy-shelf |
| `metrics-plaza.svg` | lines of code isocalendar | 1435B | metrics-plaza |

## Capsule / header (capsule-render)
| Файл | Что делает | Анимация | Откуда идея |
|---|---|---|---|
| `capsule-wave-header.svg` | waving gradient header type=waving color=gradient height=160 | 1264B | capsule-wave-header |
| `capsule-wave-footer.svg` | footer waving inverted | 1049B | capsule-wave-footer |
| `capsule-slice.svg` | two more capsule types | 1240B | capsule-slice |
| `header-suite.svg` | 4 header styles | 1251B | header-suite |
| `wave-divider.svg` | Волна с бегущей кометой. | 908B | wave-divider |
| `neon-pill.svg` |  | 3215B | neon-pill |
| `glass-panel.svg` |  | 2849B | glass-panel |
| `typing-banner.svg` | Текст печатается с мигающим курсором, как на профиле. | 1111B | typing-banner |
| `typing-themes.svg` | typing dots with 3 themes preview | 1197B | typing-themes |
| `figlet-banner.svg` | ascii art figlet | 1190B | figlet-banner |
| `quote-card.svg` | quote typing cursor 0.8s blink | 1155B | quote-card |
| `joke-card.svg` | joke setup punchline reveal 1s | 902B | joke-card |
| `presence-card.svg` | spotify + coding | 1824B | presence-card |
| `social-preview-card.svg` | OG image 1280x640 | 1070B | social-preview-card |
| `simple-icons-wall.svg` | 1856 icons → shields badges | 1333B | simple-icons-wall |
| `badge-wall.svg` | 12 badges fade | 1784B | badge-wall |
| `shields-dynamic.svg` | endpoint badge from json | 836B | shields-dynamic |
| `profile-views.svg` | eye blink 3s counter | 1326B | profile-views |
| `holopin-board.svg` | 6 badges shelf pop | 2594B | holopin-board |

## 3D city / skyline / city (yoshi389111, github-city, gh-skyline)
| Файл | Что делает | Анимация | Откуда идея |
|---|---|---|---|
| `city-skyline.svg` | isometric blocks breathe | 2095B | city-skyline |
| `skyline-stl.svg` | stencil for 3D print | 1455B | skyline-stl |
| `commit-pulse.svg` | Изометрический монолит вкладов, выше = больше коммитов.</d | 2444B | commit-pulse |
| `contrib-galaxy.svg` | Точки-коммиты как звёзды в галактике, закручиваются. | 2046B | contrib-galaxy |
| `neon-stadium.svg` | 3D стадион из календаря вкладов, неоновая обводка. | 2208B | neon-stadium |
| `heatmap-wave.svg` | 53 недели календарь, клетки проявляются по диагонали. | 2966B | heatmap-wave |
| `heatmap-iso.svg` | iso cubes height log count | 1379B | heatmap-iso |
| `weekly-skyline.svg` |  | 6808B | weekly-skyline |
| `contrib-flower.svg` | petals radial grow | 1445B | contrib-flower |

## ASCII / neofetch / portrait (neofetch, ascii-art)
| Файл | Что делает | Анимация | Откуда идея |
|---|---|---|---|
| `ascii-portrait.svg` | Монохромный ASCII-портрет печатается строка за строкой. | 2386B | ascii-portrait |
| `neofetch-card.svg` | Неофеч-стиль: иконка + строки ключ/значение, печатается. | 1948B | neofetch-card |
| `pixel-night.svg` | Пиксельный город ночью, над ним парит призрак и моргает. | 14414B | pixel-night |
| `hologram-card.svg` | Слева — проектор с голограммой глобуса, справа — имя и | 5075B | hologram-card |
| `liquid-blob.svg` | Одна капля морфит между четырьмя формами — чистый SMIL на pa | 4902B | liquid-blob |
| `orbit-stack.svg` |  | 5134B | orbit-stack |
| `skill-orbit.svg` | orbiting icons 6s 8s 10s | 1436B | skill-orbit |
| `radar-skills.svg` | Шестиугольный радар, заполнение анимируется. | 1807B | radar-skills |
| `timeline-journey.svg` | Линия прогресса зажигает вехи одну за другой. | 2568B | timeline-journey |
| `terminal-block.svg` | Окно терминала, команды печатаются одна за другой, курсор мо | 3832B | terminal-block |
| `terminal-tabs.svg` | tabs zsh + python + git | 1598B | terminal-tabs |
| `profile-generator-preview.svg` | generator preview | 1413B | profile-generator-preview |

## Games / interactive (chess, snake, pacman, tetris, gol)
| Файл | Что делает | Анимация | Откуда идея |
|---|---|---|---|
| `chess-puzzle.svg` | 8x8 board hover reveals arrow Qh7# | 5776B | chess-puzzle |
| `snake-mini.svg` | snake eats green squares 2s loop | 1937B | snake-mini |
| `snake-full.svg` | snake eats contribution path 3s loop | 1696B | snake-full |
| `pacman-board.svg` | pacman eats 10 dots across grid 1.8s loop | 1984B | pacman-board |
| `tetris-stack.svg` | tetrominoes drop 0.8s clear flash 0.3s | 1618B | tetris-stack |
| `game-of-life.svg` | conway updates on 10x10 2 frames blink | 1333B | game-of-life |
| `contrib-painter.svg` | paint your name with commits | 2070B | contrib-painter |

## Music / presence / misc
| Файл | Что делает | Анимация | Откуда идея |
|---|---|---|---|
| `spotify-card.svg` | Карточка трека с эквалайзером, обложка инлайн. | 1735B | spotify-card |
| `presence-card.svg` | spotify + coding | 1824B | presence-card |
| `drago-card.svg` | Дракон эволюционирует от активности, HUD уровня. | 1687B | drago-card |
| `equalizer.svg` | Восемь столбиков танцуют как аудио-метр, каждый со своим тем | 4112B | equalizer |
| `marquee-icons.svg` | Иконки едут влево бесшовно, на паузу при reduced-motion.</de | 3270B | marquee-icons |
| `octocat-wave.svg` | octocat waving | 1057B | octocat-wave |
| `git-log-graph.svg` | commit graph lines | 1306B | git-log-graph |
| `contrib-painter.svg` | paint your name with commits | 2070B | contrib-painter |
| `octocat-wave.svg` | octocat waving | 1057B | octocat-wave |
| `header-suite.svg` | 4 header styles | 1251B | header-suite |

## Workflow-шаблоны (копируй в `.github/workflows/`)
```yaml
# snake.yml — Platane/snk → output branch
name: Snake
on:
  schedule: [{cron: '0 0 * * *'}]
  workflow_dispatch:
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: Platane/snk@v3
        with:
          github_user_name: ${{ github.repository_owner }}
          outputs: dist/github-snake.svg
      - run: git config user.name 'bot' && git push origin HEAD:output
```
Смотри готовый шаблон: [profile-snake-workflow.yml](../templates/profile-snake-workflow.yml)

## Где копать дальше
- [Awesome GitHub Profile README](https://github.com/abhisheknaiidu/awesome-github-profile-readme) — 100+ профилей
- [awesome-github-profile-readme by abbhishek](https://github.com/EddyVinck/awesome-github-profile) — подборки
- [lowlighter/metrics](https://github.com/lowlighter/metrics) — 40+ плагинов для README
- [Platane/snk](https://github.com/Platane/snk) — змейка
- [yoshi389111/github-profile-3d-contrib](https://github.com/yoshi389111/github-profile-3d-contrib) — 3D контрибы
- [github/gh-skyline](https://github.com/github/gh-skyline) — STL скайлайн
- [kyechan99/capsule-render](https://github.com/kyechan99/capsule-render) — волны/заголовки
- [DenverCoder1/readme-typing-svg](https://github.com/DenverCoder1/readme-typing-svg) — печаталка
- [tandpfun/skill-icons](https://github.com/tandpfun/skill-icons) / [skillicons.dev](https://skillicons.dev) — иконки
- [ryo-ma/github-profile-trophy](https://github.com/ryo-ma/github-profile-trophy) — трофеи
- [ABSphreak/readme-jokes](https://github.com/ABSphreak/readme-jokes) — шутки
- [holopin.io](https://holopin.io) — бейджи
