# Шпаргалка по бейджам (шильдам) для GitHub `README.md`

<p align="left">
  <a href="https://shields.io/"><img src="https://img.shields.io/badge/Powered%20by-Shields.io-000000?style=flat-square&logo=shieldsdotio&logoColor=white" alt="Shields.io"></a>
  <a href="https://simpleicons.org/"><img src="https://img.shields.io/badge/Icons-Simple%20Icons-111111?style=flat-square&logo=simpleicons&logoColor=white" alt="Simple Icons"></a>
  <img src="https://img.shields.io/github/last-commit/overbaffe1/gitEdit?style=flat-square&color=8A2BE2&label=Last%20Commit" alt="Last Commit">
  <img src="https://img.shields.io/github/repo-size/overbaffe1/gitEdit?style=flat-square&color=007EC6&label=Repo%20Size" alt="Repo Size">
</p>

Красивые цветные плашки в шапке репозиториев называются **бейджи (GitHub Badges)** или **шилды (Shields)**.

Никакие картинки скачивать и коммитить в репозиторий **не нужно** — это обычные ссылки на картинки, которые бесплатный сервис **[Shields.io](https://shields.io/)** генерирует на лету в чётком векторном формате `SVG`, а иконки брендов подтягивает из каталога **[Simple Icons](https://simpleicons.org/)** (3000+ логотипов).

---

## Содержание

1. [Базовый синтаксис за 10 секунд](#1-базовый-синтаксис-за-10-секунд)
2. [Правила спецсимволов и все параметры URL](#2-правила-спецсимволов-и-все-параметры-url)
3. [Сравнение всех 5 стилей оформления](#3-сравнение-всех-5-стилей-оформления)
4. [Как сделать бейдж кликабельной кнопкой](#4-как-сделать-бейдж-кликабельной-кнопкой)
5. [Готовая витрина технологий (Copy & Paste)](#5-готовая-витрина-технологий-copy--paste)
6. [«Живые» (динамические) бейджи GitHub и GitHub Actions](#6-живые-динамические-бейджи-github-и-github-actions)
7. [Красивое выравнивание в шапке README](#7-красивое-выравнивание-в-шапке-readme)

---

## 1. Базовый синтаксис за 10 секунд

Обычный статичный бейдж строится по одной формуле:

```text
https://img.shields.io/badge/<ЛЕВЫЙ_ТЕКСТ>-<ПРАВЫЙ_ТЕКСТ>-<HEX_ЦВЕТ>?style=flat-square&logo=<ИКОНКА>&logoColor=white
```

**Пример вживую:**

![Blender](https://img.shields.io/badge/Blender-bpy%205.x%20(headless)-EA7600?style=flat-square&logo=blender&logoColor=white)

**Код для `README.md`:**

```markdown
![Blender](https://img.shields.io/badge/Blender-bpy%205.x%20(headless)-EA7600?style=flat-square&logo=blender&logoColor=white)
```

Если поставить несколько таких строк подряд (через перенос строки или пробел, **без пустой строки между ними**), GitHub сам выстроит их в аккуратную горизонтальную линию.

### Бейдж из одной половинки (только цветная кнопка без серого ярлыка)

Если левая серая часть не нужна, просто опусти `<ЛЕВЫЙ_ТЕКСТ>-`:

![Telegram](https://img.shields.io/badge/Telegram-26A5E4?style=flat-square&logo=telegram&logoColor=white)

```markdown
![Telegram](https://img.shields.io/badge/Telegram-26A5E4?style=flat-square&logo=telegram&logoColor=white)
```

---

## 2. Правила спецсимволов и все параметры URL

Так как дефис `-` и подчёркивание `_` используются самим `shields.io` как разделители, внутри текста работают простые замены:

| Что нужно написать в тексте | Как писать в ссылке | Пример |
|---|---|---|
| Пробел ` ` | `_` или `%20` | `AI_Agent` или `AI%20Agent` → `AI Agent` |
| Дефис `-` | Два дефиса `--` | `UTF--8` → `UTF-8` |
| Подчёркивание `_` | Два подчёркивания `__` | `my__var` → `my_var` |
| Плюс `+` | `%2B` | `C%2B%2B` → `C++` |
| Процент `%` | `%25` | `100%25` → `100%` |
| Двоеточие `:` | `%3A` (или `:`) | `am3d%3Amodel3d` → `am3d:model3d` |

### Полезные параметры после знака `?` (соединяются через `&`)

| Параметр | Что меняет | Примеры значений |
|---|---|---|
| `style=` | Форма и размер плашки | `flat`, `flat-square`, `for-the-badge`, `plastic`, `social` |
| `logo=` | Иконка слева (slug с сайта [simpleicons.org](https://simpleicons.org/)) | `python`, `nodedotjs`, `docker`, `github`, `blender`, `telegram` |
| `logoColor=` | Цвет иконки | `white`, `black`, `FFD43B` (HEX без `#`) |
| `labelColor=` | Цвет фона левой половинки (по умолчанию тёмно-серый `#555`) | `1a1b27`, `000000`, `24292e` |
| `color=` | Цвет правой половинки (переопределяет цвет у динамических бейджей) | `brightgreen`, `8A2BE2`, `EA7600` |

> **Как узнать точное имя иконки и фирменный цвет?** Открой [simpleicons.org](https://simpleicons.org/), вбей название технологии (например, `Node.js`) — на карточке сразу написаны её HEX-цвет (`#5FA04E`) и slug для параметра `logo=` (`nodedotjs`).

---

## 3. Сравнение всех 5 стилей оформления

| Стиль (`?style=...`) | Живой вид | Когда лучше использовать |
|---|---|---|
| `flat` *(по умолчанию)* | ![flat](https://img.shields.io/badge/Style-flat-007EC6?style=flat&logo=github&logoColor=white) | Классический спокойный стиль для большинства библиотек |
| `flat-square` | ![flat-square](https://img.shields.io/badge/Style-flat--square-EA7600?style=flat-square&logo=blender&logoColor=white) | Строгие прямые углы, отлично смотрится в технических проектах |
| `for-the-badge` | ![for-the-badge](https://img.shields.io/badge/Style-for--the--badge-8A2BE2?style=for-the-badge&logo=rocket&logoColor=white) | Крупные акцентные кнопки (КАПСОМ) для главных ссылок: «Демо», «Документация», «Скачать» |
| `plastic` | ![plastic](https://img.shields.io/badge/Style-plastic-339933?style=plastic&logo=nodedotjs&logoColor=white) | Лёгкий ретро-глянец с объёмом |
| `social` | ![social](https://img.shields.io/github/stars/overbaffe1/gitEdit?style=social) | Нативный стиль счётчиков GitHub (звёзды, форки, подписчики) |

---

## 4. Как сделать бейдж кликабельной кнопкой

В Markdown картинка — это `![alt](картинка)`, а ссылка — `[текст](адрес)`. Просто оберни картинку в ссылку `[![alt](картинка)](адрес)`:

[![Открыть документацию](https://img.shields.io/badge/Открыть-Документацию-8A2BE2?style=for-the-badge&logo=readthedocs&logoColor=white)](#1-базовый-синтаксис-за-10-секунд)
[![Написать в Telegram](https://img.shields.io/badge/Telegram-Канал-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/)

```markdown
[![Открыть документацию](https://img.shields.io/badge/Открыть-Документацию-8A2BE2?style=for-the-badge&logo=readthedocs&logoColor=white)](docs/README.md)
[![Написать в Telegram](https://img.shields.io/badge/Telegram-Канал-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/username)
```

Ссылаться можно как на внешние сайты (`https://...`), так и на файлы внутри репозитория (`AGENTS.md`, `exports/`) или якоря заголовков (`#раздел`).

---

## 5. Готовая витрина технологий (Copy & Paste)

Подборка готовых бейджей с фирменными цветами в стиле `flat-square`:

| Превью | Код для копирования |
|---|---|
| ![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white) | `![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)` |
| ![JavaScript](https://img.shields.io/badge/JavaScript-ES2023-F7DF1E?style=flat-square&logo=javascript&logoColor=black) | `![JavaScript](https://img.shields.io/badge/JavaScript-ES2023-F7DF1E?style=flat-square&logo=javascript&logoColor=black)` |
| ![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=flat-square&logo=typescript&logoColor=white) | `![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=flat-square&logo=typescript&logoColor=white)` |
| ![Node.js](https://img.shields.io/badge/Node.js-20%20LTS-339933?style=flat-square&logo=nodedotjs&logoColor=white) | `![Node.js](https://img.shields.io/badge/Node.js-20%20LTS-339933?style=flat-square&logo=nodedotjs&logoColor=white)` |
| ![React](https://img.shields.io/badge/React-19-20232A?style=flat-square&logo=react&logoColor=61DAFB) | `![React](https://img.shields.io/badge/React-19-20232A?style=flat-square&logo=react&logoColor=61DAFB)` |
| ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white) | `![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)` |
| ![C++](https://img.shields.io/badge/C%2B%2B-20-00599C?style=flat-square&logo=cplusplus&logoColor=white) | `![C++](https://img.shields.io/badge/C%2B%2B-20-00599C?style=flat-square&logo=cplusplus&logoColor=white)` |
| ![Rust](https://img.shields.io/badge/Rust-000000?style=flat-square&logo=rust&logoColor=white) | `![Rust](https://img.shields.io/badge/Rust-000000?style=flat-square&logo=rust&logoColor=white)` |
| ![Go](https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white) | `![Go](https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white)` |
| ![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white) | `![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)` |
| ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white) | `![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)` |
| ![Blender](https://img.shields.io/badge/Blender-bpy-EA7600?style=flat-square&logo=blender&logoColor=white) | `![Blender](https://img.shields.io/badge/Blender-bpy-EA7600?style=flat-square&logo=blender&logoColor=white)` |
| ![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black) | `![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black)` |
| ![License MIT](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square) | `![License MIT](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)` |

---

## 6. «Живые» (динамические) бейджи GitHub и GitHub Actions

Эти бейджи сами обращаются к API GitHub и показывают актуальные метрики по публичному репозиторию `<USER>/<REPO>`:

| Что показывает | Живой пример | Шаблон ссылки |
|---|---|---|
| Дата последнего коммита | ![Last Commit](https://img.shields.io/github/last-commit/overbaffe1/MyWorkAiBrain?style=flat-square) | `https://img.shields.io/github/last-commit/<USER>/<REPO>?style=flat-square` |
| Размер репозитория | ![Repo Size](https://img.shields.io/github/repo-size/overbaffe1/MyWorkAiBrain?style=flat-square) | `https://img.shields.io/github/repo-size/<USER>/<REPO>?style=flat-square` |
| Звёзды репозитория | ![Stars](https://img.shields.io/github/stars/overbaffe1/MyWorkAiBrain?style=flat-square) | `https://img.shields.io/github/stars/<USER>/<REPO>?style=flat-square` |
| Главный язык кода | ![Top Lang](https://img.shields.io/github/languages/top/overbaffe1/MyWorkAiBrain?style=flat-square) | `https://img.shields.io/github/languages/top/<USER>/<REPO>?style=flat-square` |
| Открытые Issues | ![Issues](https://img.shields.io/github/issues/overbaffe1/MyWorkAiBrain?style=flat-square) | `https://img.shields.io/github/issues/<USER>/<REPO>?style=flat-square` |
| Открытые Pull Requests | ![PRs](https://img.shields.io/github/issues-pr/overbaffe1/MyWorkAiBrain?style=flat-square) | `https://img.shields.io/github/issues-pr/<USER>/<REPO>?style=flat-square` |

### Бейдж статуса тестов / сборки GitHub Actions

Когда в репозитории настроен воркфлоу `.github/workflows/ci.yml`, статус его последнего прогона (`passing` / `failing`) добавляется так:

```markdown
<!-- Вариант через Shields.io (единый стиль со всеми остальными бейджами) -->
[![CI](https://img.shields.io/github/actions/workflow/status/<USER>/<REPO>/ci.yml?branch=main&style=flat-square&logo=githubactions&logoColor=white&label=CI)](https://github.com/<USER>/<REPO>/actions)

<!-- Родной бейдж самого GitHub -->
[![CI](https://github.com/<USER>/<REPO>/actions/workflows/ci.yml/badge.svg)](https://github.com/<USER>/<REPO>/actions)
```

---

## 7. Красивое выравнивание в шапке README

Обычный Markdown всегда прижимает бейджи к левому краю. Если хочется поставить заголовок и ряд кнопок **ровно по центру страницы**, оберни их в `<div align="center">`:

```html
<div align="center">

# Название проекта

Короткое описание в одну строку

[![Docs](https://img.shields.io/badge/Docs-Read-8A2BE2?style=for-the-badge&logo=readthedocs&logoColor=white)](#)
[![Demo](https://img.shields.io/badge/Live-Demo-22C55E?style=for-the-badge&logo=vercel&logoColor=white)](#)

</div>
```

---

## Полезные ссылки

* **[shields.io](https://shields.io/)** — официальный визуальный конструктор любых статичных и динамических бейджей.
* **[simpleicons.org](https://simpleicons.org/)** — поиск по 3000+ иконкам брендов и их точным HEX-цветам.
* **[ileriayo/markdown-badges](https://github.com/Ileriayo/markdown-badges)** — огромная коллекция готовых бейджей под сотни языков, фреймворков и сервисов.
