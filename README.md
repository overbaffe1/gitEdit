<picture>
  <source media="(max-width: 600px)" srcset="assets/banner-compact.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/banner-light.svg">
  <img alt="gitEdit — Конструктор вау-оформления GitHub" src="assets/banner-dark.svg" width="100%">
</picture>

# Витрина шаблонов

Выбери обложку и скопируй Markdown из открывшегося шаблона.

<p align="center">
  <a href="templates/PROJECT-README-TEMPLATE.md"><img src="assets/cover-project.svg" width="360" alt="Открыть шаблон проекта: демо, стек и запуск"></a>
  <a href="templates/PROFILE-README-TEMPLATE.md"><img src="assets/cover-profile.svg" width="360" alt="Открыть шаблон профиля: работы, стек и контакты"></a>
</p>

[Кинолаборатория](#кинолаборатория) · [Оглавление](#оглавление) · [Код витрины](#5-витрина-из-двух-обложек) · [Змейка для профиля](templates/profile-snake-workflow.yml)

## Кинолаборатория

На плёнке — короткая история двух веток. Проследи линии назад от кадра `M`: какие два коммита стали его родителями?

<p align="center">
  <img src="assets/commit-reel.svg" width="560" alt="От A расходятся линии к B в main и C в edit. Из B и C линии сходятся в M.">
</p>

<details>
<summary><b>Монтажный лист</b> · проверить ответ и забрать киноленту</summary>

Родители `M` — **`B` и `C`**. Коммит `A` есть в истории обеих веток, но он их общий предок, а не родитель `M`.

Скопируй [киноленту](assets/commit-reel.svg) в папку `assets/` своего репозитория и вставь строку ниже. Это иллюстрация, а не статистика репозитория: она проигрывается один раз, а при включённом уменьшении движения сразу показывает всю схему.

```markdown
![История веток: A → B и A → C, затем слияние B и C в M](assets/commit-reel.svg)
```

Хочешь изобразить свои ветки? Вот [та же история на Mermaid](#граф-коммитов): вместо координат SVG редактируются имена веток и коммитов.

</details>

<details>
<summary><b>Проявочная</b> · сравнить «Ризограф» и «Фосфор»</summary>

Один хребет, два оттиска. У «Ризографа» видны точки типографского растра и чуть смещённая краска. У «Фосфора» те же вершины проступают на сетке экрана.

<p align="center">
  <img src="assets/relief-riso.svg" width="340" alt="Ризограф: тёмный горный хребет и коралловое солнце на кремовой бумаге">
  <img src="assets/relief-phosphor.svg" width="340" alt="Фосфор: тот же хребет мятными линиями, над ним янтарный диск">
</p>

| Оттиск | Фон `--paper` | Контур `--ink` | Акцент `--spot` |
|---|---|---|---|
| [Ризограф](assets/relief-riso.svg) | `#FFF1D9` | `#292948` | `#EF6747` |
| [Фосфор](assets/relief-phosphor.svg) | `#102622` | `#ADF2CB` | `#FFD182` |

Чтобы превратить пару в одну заставку, скопируй оба SVG в `assets/` и вставь этот блок. На светлой теме появится бумажный оттиск, на тёмной — экранный. Цвета меняются в `:root` каждого SVG.

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/relief-phosphor.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/relief-riso.svg">
  <img src="assets/relief-riso.svg" width="480" alt="Рельеф: горный хребет под низким солнцем">
</picture>
```

</details>

## Оглавление

Нужен один элемент, а не целый шаблон? Выбери раздел ниже: рядом с примерами есть код для копирования.

1. [Бейджи и шилды (`Shields.io` + `Simple Icons`)](#1-бейджи-и-шилды-shieldsio--simple-icons)
2. [Квадратные иконки стека одной строкой (`Skill Icons`)](#2-квадратные-иконки-стека-одной-строкой-skill-icons)
3. [Живые SVG-анимации: печатная машинка, волны и свои баннеры](#3-живые-svg-анимации-печатная-машинка-волны-и-свои-баннеры)
4. [Цветные инфо-блоки GitHub Alerts](#4-цветные-инфо-блоки-github-alerts)
5. [Интерактивные векторные схемы `Mermaid`](#5-интерактивные-векторные-схемы-mermaid)
6. [Продвинутая вёрстка портфолио (сплит, темы `<picture>`, видео, `<kbd>`)](#6-продвинутая-вёрстка-портфолио-сплит-темы-picture-видео-kbd)
7. [Секретный репозиторий профиля (`overbaffe1/overbaffe1`) + змейка коммитов](#7-секретный-репозиторий-профиля-overbaffe1overbaffe1--змейка-коммитов)

<img src="assets/divider.svg" width="100%" alt="">

## 1. Бейджи и шилды (`Shields.io` + `Simple Icons`)

Цветные кнопки-плашки рисует на лету бесплатный сервис **[Shields.io](https://shields.io/)** в векторном формате `SVG` (скачивать файлы в репо не нужно), а логотипы брендов берутся из каталога **[Simple Icons](https://simpleicons.org/)** (более 3000 иконок).

### Формула статичного бейджа за 10 секунд

```text
https://img.shields.io/badge/<ЛЕВЫЙ_ТЕКСТ>-<ПРАВЫЙ_ТЕКСТ>-<HEX_ЦВЕТ>?style=flat-square&logo=<ИКОНКА>&logoColor=white
```

* **Двухчастный бейдж:** ![Blender](https://img.shields.io/badge/Blender-bpy%205.x%20(headless)-EA7600?style=flat-square&logo=blender&logoColor=white)
  ```markdown
  ![Blender](https://img.shields.io/badge/Blender-bpy%205.x%20(headless)-EA7600?style=flat-square&logo=blender&logoColor=white)
  ```
* **Одночастная цветная плашка (без серой левой части):** ![Telegram](https://img.shields.io/badge/Telegram-26A5E4?style=flat-square&logo=telegram&logoColor=white)
  ```markdown
  ![Telegram](https://img.shields.io/badge/Telegram-26A5E4?style=flat-square&logo=telegram&logoColor=white)
  ```

### Таблица спецсимволов и параметров URL

| Символ в тексте | Замена в ссылке | Пример | Параметр `?` | За что отвечает |
|---|---|---|---|---|
| Пробел ` ` | `_` или `%20` | `AI%20Agent` → `AI Agent` | `style=` | `flat`, `flat-square`, `for-the-badge`, `plastic`, `social` |
| Дефис `-` | `--` | `UTF--8` → `UTF-8` | `logo=` | Slug иконки с [simpleicons.org](https://simpleicons.org/) (`python`, `docker`) |
| Подчёркивание `_` | `__` | `my__var` → `my_var` | `logoColor=` | Цвет иконки (`white`, `black`, `FFD43B`) |
| Плюс `+` | `%2B` | `C%2B%2B` → `C++` | `labelColor=` | Цвет левой части (`1E293B`, `000000`) |
| Процент `%` | `%25` | `100%25` → `100%` | `color=` | Переопределение цвета правой части |

### Все 5 стилей лицом к лицу

| Стиль | Живой рендер | Где смотрится лучше всего |
|---|---|---|
| `flat` | ![flat](https://img.shields.io/badge/Style-flat-007EC6?style=flat&logo=github&logoColor=white) | Универсальная классика по умолчанию |
| `flat-square` | ![flat-square](https://img.shields.io/badge/Style-flat--square-EA7600?style=flat-square&logo=blender&logoColor=white) | Строгие инженерные проекты и компактные шапки |
| `for-the-badge` | ![for-the-badge](https://img.shields.io/badge/Style-for--the--badge-8B5CF6?style=for-the-badge&logo=rocket&logoColor=white) | Крупные акцентные кнопки навигации («Демо», «Доки», «Скачать») |
| `plastic` | ![plastic](https://img.shields.io/badge/Style-plastic-16A34A?style=plastic&logo=nodedotjs&logoColor=white) | Глянцевый объёмный стиль |
| `social` | ![social](https://img.shields.io/github/stars/overbaffe1/MyWorkAiBrain?style=social) | Нативные счётчики звёзд и форков |

### Кликабельные кнопки-ссылки

Чтобы плашка работала как настоящая кнопка, оберни картинку в Markdown-ссылку `[![alt](картинка)](адрес)`:

[![Посмотреть MyWorkAiBrain](https://img.shields.io/badge/Проект-MyWorkAiBrain-E3B663?style=for-the-badge&logo=blender&logoColor=black)](https://github.com/overbaffe1/MyWorkAiBrain)
[![Открыть шаблон](https://img.shields.io/badge/Шаблон-Project%20README-8B5CF6?style=for-the-badge&logo=markdown&logoColor=white)](templates/PROJECT-README-TEMPLATE.md)

```markdown
[![Посмотреть MyWorkAiBrain](https://img.shields.io/badge/Проект-MyWorkAiBrain-E3B663?style=for-the-badge&logo=blender&logoColor=black)](https://github.com/overbaffe1/MyWorkAiBrain)
```

### Витрина готовых бейджей технологий (Copy & Paste)

| Превью | Готовый Markdown-код |
|---|---|
| ![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white) | `![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)` |
| ![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=flat-square&logo=typescript&logoColor=white) | `![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=flat-square&logo=typescript&logoColor=white)` |
| ![JavaScript](https://img.shields.io/badge/JavaScript-ES2023-F7DF1E?style=flat-square&logo=javascript&logoColor=black) | `![JavaScript](https://img.shields.io/badge/JavaScript-ES2023-F7DF1E?style=flat-square&logo=javascript&logoColor=black)` |
| ![Node.js](https://img.shields.io/badge/Node.js-20%20LTS-339933?style=flat-square&logo=nodedotjs&logoColor=white) | `![Node.js](https://img.shields.io/badge/Node.js-20%20LTS-339933?style=flat-square&logo=nodedotjs&logoColor=white)` |
| ![React](https://img.shields.io/badge/React-19-20232A?style=flat-square&logo=react&logoColor=61DAFB) | `![React](https://img.shields.io/badge/React-19-20232A?style=flat-square&logo=react&logoColor=61DAFB)` |
| ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white) | `![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)` |
| ![C++](https://img.shields.io/badge/C%2B%2B-20-00599C?style=flat-square&logo=cplusplus&logoColor=white) | `![C++](https://img.shields.io/badge/C%2B%2B-20-00599C?style=flat-square&logo=cplusplus&logoColor=white)` |
| ![Rust](https://img.shields.io/badge/Rust-000000?style=flat-square&logo=rust&logoColor=white) | `![Rust](https://img.shields.io/badge/Rust-000000?style=flat-square&logo=rust&logoColor=white)` |
| ![Go](https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white) | `![Go](https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white)` |
| ![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white) | `![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)` |
| ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white) | `![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)` |
| ![Blender](https://img.shields.io/badge/Blender-bpy-EA7600?style=flat-square&logo=blender&logoColor=white) | `![Blender](https://img.shields.io/badge/Blender-bpy-EA7600?style=flat-square&logo=blender&logoColor=white)` |
| ![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white) | `![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)` |
| ![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black) | `![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black)` |
| ![License MIT](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square) | `![License MIT](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)` |

### Динамические бейджи GitHub API и GitHub Actions

Строка показателей для этого репозитория:

![Последнее обновление](https://img.shields.io/github/last-commit/overbaffe1/gitEdit?style=flat-square&color=8B5CF6&label=Updated)
![Размер репозитория](https://img.shields.io/github/repo-size/overbaffe1/gitEdit?style=flat-square&color=0284C7&label=Size)
![Звёзды](https://img.shields.io/github/stars/overbaffe1/gitEdit?style=flat-square&color=EAB308)

| Метрика | Живой пример | Шаблон |
|---|---|---|
| Последний коммит | ![Last Commit](https://img.shields.io/github/last-commit/overbaffe1/MyWorkAiBrain?style=flat-square) | `https://img.shields.io/github/last-commit/<USER>/<REPO>?style=flat-square` |
| Размер репо | ![Size](https://img.shields.io/github/repo-size/overbaffe1/MyWorkAiBrain?style=flat-square) | `https://img.shields.io/github/repo-size/<USER>/<REPO>?style=flat-square` |
| Главный язык | ![Top Lang](https://img.shields.io/github/languages/top/overbaffe1/MyWorkAiBrain?style=flat-square) | `https://img.shields.io/github/languages/top/<USER>/<REPO>?style=flat-square` |
| Звёзды | ![Stars](https://img.shields.io/github/stars/overbaffe1/MyWorkAiBrain?style=flat-square) | `https://img.shields.io/github/stars/<USER>/<REPO>?style=flat-square` |
| Статус GitHub Actions | `build \| passing` | `https://img.shields.io/github/actions/workflow/status/<USER>/<REPO>/ci.yml?style=flat-square&logo=githubactions&logoColor=white` |

<img src="assets/divider.svg" width="100%" alt="">

## 2. Квадратные иконки стека одной строкой (`Skill Icons`)

Сервис **[skillicons.dev](https://skillicons.dev/)** собирает квадратные иконки приложений в единую плитку по списку через запятую (`&theme=dark` или `light`, `&perline=8`):

**Python / AI / 3D:**

![AI Stack](https://skillicons.dev/icons?i=py,pytorch,tensorflow,opencv,blender,fastapi,docker,linux&theme=dark)

```markdown
![AI Stack](https://skillicons.dev/icons?i=py,pytorch,tensorflow,opencv,blender,fastapi,docker,linux&theme=dark)
```

**Fullstack Web & DevOps:**

![Web Stack](https://skillicons.dev/icons?i=ts,js,nodejs,react,nextjs,tailwind,postgres,redis,nginx,git,github,githubactions&theme=dark&perline=12)

```markdown
![Web Stack](https://skillicons.dev/icons?i=ts,js,nodejs,react,nextjs,tailwind,postgres,redis,nginx,git,github,githubactions&theme=dark&perline=12)
```

<img src="assets/divider.svg" width="100%" alt="">

## 3. Живые SVG-анимации: печатная машинка, волны и свои баннеры

GitHub режет JavaScript, но **полностью разрешает SMIL `<animate>` / `<animateTransform>` внутри `.svg`-картинок**.

### А) Самопечатающийся текст — [Readme Typing SVG](https://readme-typing-svg.demolab.com/demo/)

![Typing Demo](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=21&pause=1000&color=38BDF8&vCenter=true&width=640&lines=Fullstack+%26+AI+Engineer;Procedural+3D+%26+Automation;Open+Source+Portfolio)

```markdown
![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=21&pause=1000&color=38BDF8&vCenter=true&width=640&lines=Первая+строка;Вторая+строка;Третья+строка)
```

### Б) Плывущая градиентная волна — [Capsule Render](https://github.com/kyechan99/capsule-render)

![Wave Demo](https://capsule-render.vercel.app/api?type=waving&color=0:0F172A,50:6D28D9,100:0284C7&height=150&section=header&text=Portfolio%20Project&fontSize=42&fontColor=FFFFFF&animation=fadeIn)

```markdown
![Header](https://capsule-render.vercel.app/api?type=waving&color=0:0F172A,50:6D28D9,100:0284C7&height=150&section=header&text=Portfolio%20Project&fontSize=42&fontColor=FFFFFF&animation=fadeIn)
```

### В) Профи-уровень: собственные локальные `.svg` в папке `assets/`

Внешние сервисы иногда уходят в офлайн, а **локальный `.svg` внутри самого репозитория** грузится мгновенно, никогда не падает и позволяет верстать любую анимацию (посмотри исходники [`assets/banner-dark.svg`](assets/banner-dark.svg) и [`assets/banner-light.svg`](assets/banner-light.svg) в этом репо!).

> [!WARNING]
> **Важная тонкость SVG в браузерах:** если двигаешь группу `<g transform="translate(860, 50)">`, не вешай на этот же `<g>` CSS `@keyframes { transform: translateY(...) }` — CSS перетрёт координаты `860, 50` в `0, 0`. Вкладывай внутрь дочерний `<g>` с нативным `<animateTransform attributeName="transform" type="translate" .../>`.

<img src="assets/divider.svg" width="100%" alt="">

## 4. Цветные инфо-блоки GitHub Alerts

Нативная замена обычным серым цитатам `>` — 5 системных плашек с иконками и цветной рамкой:

> [!NOTE]
> **Заметка (`[!NOTE]`):** Полезный контекст или справочная деталь, на которую стоит обратить внимание.

> [!TIP]
> **Совет (`[!TIP]`):** Лайфхак, ускоряющий работу — например, запуск в быстром режиме `FAST=1`.

> [!IMPORTANT]
> **Важно (`[!IMPORTANT]`):** Ключевое требование, без которого проект не запустится как задумано.

> [!WARNING]
> **Внимание (`[!WARNING]`):** Потенциальный подводный камень или ограничение совместимости.

> [!CAUTION]
> **Опасно (`[!CAUTION]`):** Действие может удалить данные или сломать сборку.

```markdown
> [!TIP]
> Текст зелёного блока с лампочкой.
```

<img src="assets/divider.svg" width="100%" alt="">

## 5. Интерактивные векторные схемы `Mermaid`

Блок кода с языком `mermaid` превращается на GitHub в масштабируемую векторную диаграмму без единого графического файла:

### Архитектурный пайплайн с кастомными цветами

```mermaid
flowchart LR
    U(["👤 Запрос пользователя"]) ==> A["🤖 AI Agent"]
    A --> B["🐍 Python / Blender bpy"]
    A --> C["⚡ Node.js / pptxgenjs"]
    B -->|".glb + PNG"| D["📦 JSZip / OpenXML"]
    C -->|"Черновой .pptx"| D
    D ==> E(["🎬 Живая 3D-презентация"])

    classDef accent fill:#1e1b4b,stroke:#8b5cf6,stroke-width:2px,color:#f5f3ff;
    classDef pipe fill:#0f172a,stroke:#38bdf8,stroke-width:1.5px,color:#e0f2fe;
    classDef done fill:#052e16,stroke:#22c55e,stroke-width:2px,color:#dcfce7;
    class U,A accent;
    class B,C,D pipe;
    class E done;
```

### Sequence-диаграмма взаимодействия сервисов

```mermaid
sequenceDiagram
    autonumber
    actor Client as Клиент
    participant API as FastAPI Backend
    participant DB as PostgreSQL
    Client->>API: POST /api/v1/tasks
    activate API
    API->>DB: INSERT task
    DB-->>API: task_id
    API-->>Client: 201 Created (JSON)
    deactivate API
```

````markdown
```mermaid
flowchart LR
    A[Старт] --> B{Проверка}
    B -->|OK| C[Деплой]
    B -->|Ошибка| D[Фикс]
```
````

### Граф коммитов

Та же склейка, что в [кинолаборатории](#кинолаборатория), но без рисунка: `branch` создаёт ветку, `checkout` переключает текущую, а `merge` сливает указанную ветку в текущую.

```mermaid
gitGraph
    commit id: "A"
    branch edit
    checkout main
    commit id: "B"
    checkout edit
    commit id: "C"
    checkout main
    merge edit id: "M"
```

<details>
<summary>Скопировать Markdown для своей истории</summary>

````markdown
```mermaid
gitGraph
    commit id: "A"
    branch edit
    checkout main
    commit id: "B"
    checkout edit
    commit id: "C"
    checkout main
    merge edit id: "M"
```
````

</details>

<img src="assets/divider.svg" width="100%" alt="">

## 6. Продвинутая вёрстка портфолио (сплит, темы `<picture>`, видео, `<kbd>`)

### 1) Автоматическая смена баннера под тёмную и светлую тему GitHub (`<picture>`)

Браузер берёт первый подходящий `<source>`. В шапке этой страницы на экранах до 600 пикселей показывается [короткая обложка](assets/banner-compact.svg) с крупным названием. На широких экранах остаётся полный баннер под цвет темы:

```html
<picture>
  <source media="(max-width: 600px)" srcset="assets/banner-compact.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/banner-light.svg">
  <img alt="Banner" src="assets/banner-dark.svg" width="100%">
</picture>
```

### 2) Сплит-вёрстка: текст слева + живая гифка справа

```html
<img align="right" width="44%" src="assets/demo.gif" alt="Live Demo">

### Главные возможности
* Пункт описания слева от анимации
* Второй пункт описания
* Третий пункт описания

<br clear="right"/>
```

### 3) Спойлеры `<details>` и физические клавиши `<kbd>`

Сочетания вроде <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> или <kbd>⌘ Cmd</kbd> + <kbd>K</kbd> пишутся через тег `<kbd>Ctrl</kbd>`, а большие скриншоты и логи удобно прятать под кат:

<details>
<summary><b>Нажми, чтобы развернуть пример спойлера</b></summary>
<br>
Сюда отлично прячутся длинные таблицы, переменные окружения <code>.env</code> или большие контакт-листы слайдов, чтобы не перегружать первый экран.
</details>

```html
<details>
<summary><b>Заголовок спойлера</b></summary>
<br>
Скрытый контент или большая картинка.
</details>
```

### 4) Настоящий `.mp4`-видеоплеер без утяжеления git-репозитория

Открой редактирование `README.md` прямо в веб-интерфейсе GitHub и **перетащи файл `.mp4` или `.mov` мышкой в текстовое поле**. GitHub загрузит ролик на свой внутренний CDN (`github.com/user-attachments/assets/...`) и вставит нативный видеоплеер со звуком и перемоткой, а сам репозиторий останется лёгким!

### 5) Витрина из двух обложек

В [витрине в начале страницы](#витрина-шаблонов) каждая обложка — обычная ссылка с локальным SVG внутри. Скопируй [«Чертёж»](assets/cover-project.svg) и [«Созвездие»](assets/cover-profile.svg) в папку `assets/` рядом со своим `README.md`. В `href` подставь пути к своим страницам:

```html
<p align="center">
  <a href="templates/PROJECT-README-TEMPLATE.md"><img src="assets/cover-project.svg" width="360" alt="Открыть шаблон проекта: демо, стек и запуск"></a>
  <a href="templates/PROFILE-README-TEMPLATE.md"><img src="assets/cover-profile.svg" width="360" alt="Открыть шаблон профиля: работы, стек и контакты"></a>
</p>
```

Не склеивай теги `</a>` и `<a>`: пробел или перенос строки между ними позволяет обложкам встать друг под другом на узком экране. Чтобы перекрасить карточку, поменяй `--paper` (фон) и `--accent` (акцент) в её SVG. Рядом в `@media (prefers-color-scheme: dark)` лежит тёмная палитра. Если включено уменьшение движения, обе иллюстрации сразу показываются в финальном виде.

<img src="assets/divider.svg" width="100%" alt="">

## 7. Секретный репозиторий профиля (`overbaffe1/overbaffe1`) + змейка коммитов

Если создать публичный репозиторий с именем **один в один как твой логин** (`overbaffe1/overbaffe1`), его `README.md` станет витриной прямо на главной странице твоего профиля **[github.com/overbaffe1](https://github.com/overbaffe1)**.

Что заготовлено в папке [`templates/`](templates/):
1. **[`templates/PROFILE-README-TEMPLATE.md`](templates/PROFILE-README-TEMPLATE.md)** — полностью собранный шаблон главной страницы профиля (волна, печатающийся подзаголовок, кнопки соцсетей, плитка стека, витрина лучших репозиториев и адаптивный блок со змейкой).
2. **[`templates/profile-snake-workflow.yml`](templates/profile-snake-workflow.yml)** — готовый воркфлоу GitHub Actions (`Platane/snk`), который раз в сутки сам рисует анимацию змейки, поедающей твои зелёные квадратики коммитов, сразу в двух версиях (для светлой и тёмной темы GitHub) в отдельную ветку `output`!
3. **[`templates/PROJECT-README-TEMPLATE.md`](templates/PROJECT-README-TEMPLATE.md)** — универсальный каркас вау-ридмика для любого нового проекта в портфолио.

---

## Полезные конструкторы в закладки

* **[shields.io](https://shields.io/)** — генератор любых статичных и динамических бейджей.
* **[simpleicons.org](https://simpleicons.org/)** — 3000+ логотипов брендов и их фирменные HEX-цвета.
* **[skillicons.dev](https://skillicons.dev/)** — плитки квадратных иконок стека.
* **[readme-typing-svg.demolab.com/demo](https://readme-typing-svg.demolab.com/demo/)** — визуальный редактор печатающегося SVG-текста.
* **[mermaid.live](https://mermaid.live/)** — песочница с предпросмотром диаграмм `Mermaid`.
* **[ileriayo/markdown-badges](https://github.com/Ileriayo/markdown-badges)** — огромная коллекция готовых бейджей.

[↑ К витрине шаблонов](#витрина-шаблонов)
