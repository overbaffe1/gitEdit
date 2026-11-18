# Склад крутого для README — копируй одну строку

> Склад — это не выставка. Тут одна строка = один эффект. Без сборки, без Python. Копируешь Markdown, меняешь `USER` и готово.
>
> Хочешь листать красивое? После склада загляни в [витрину в README](../README.md) — там орбита, неоновые пилюли и стеклянная панель.

**Как пользоваться:** каждый блок ниже — готовый Markdown. Открывай «Код» рядом с предпросмотром, меняй параметры в URL и вставляй в свой README. Всё рендерится как внешние картинки — GitHub просто показывает SVG.

## 1. Шапка-волна

```markdown
![Header](https://capsule-render.vercel.app/api?type=waving&color=0:111827,100:7c3aed&height=200&section=header&text=ПРИВЕТ&fontSize=52&fontColor=fff&animation=fadeIn)
```
Параметры: `text`, `color` (градиент `0:цвет1,100:цвет2`), `height`, `animation=fadeIn`. [capsule-render](https://github.com/kyechan99/capsule-render)

Шаблон целиком: [ANIMATED-HEADER-TEMPLATE.md](../templates/ANIMATED-HEADER-TEMPLATE.md)

## 2. Печаталка

```markdown
[![Typing](https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&pause=1000&color=A78BFA&center=true&width=500&lines=Hello+World;Я+делаю+крутые+штуки)](https://git.io/typing-svg)
```
Меняй `lines` через `;`, пробел как `+`. [readme-typing-svg](https://github.com/DenverCoder1/readme-typing-svg)

## 3. Стена скиллов

```markdown
<img src="https://skillicons.dev/icons?i=py,ts,react,nodejs,blender,docker,postgres,linux&theme=dark&perline=8" alt="stack" />
```
Список иконок: [skillicons.dev](https://skillicons.dev) — `i=` через запятую.

## 4. Бейдж на любой вкус

```markdown
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
```
Конструктор: [shields.io](https://shields.io/badges) — `style=flat|for-the-badge|social`, `logo=` из [simpleicons.org](https://simpleicons.org)

## 5. Карточка статистики

```markdown
<img src="https://github-readme-stats.vercel.app/api?username=overbaffe1&show_icons=true&theme=tokyonight" />
<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=overbaffe1&layout=compact&theme=tokyonight" />
```
[github-readme-stats](https://github.com/anuraghazra/github-readme-stats) — требует публичного API, кешируется.

## 6. Змейка — ест граф вкладов

1. Добавь workflow из [templates/profile-snake-workflow.yml](../templates/profile-snake-workflow.yml) в `.github/workflows/snake.yml`
2. Нажми **Run workflow** в Actions
3. Вставь в README:

```markdown
![snake](https://raw.githubusercontent.com/USER/USER/output/github-contribution-grid-snake.svg)
```

Генератор: [Platane/snk](https://github.com/Platane/snk) — рисует SVG по календарю, без JS.

## 7. Город вкладов 3D

```markdown
![city](https://raw.githubusercontent.com/yoshi389111/github-profile-3d-contrib/main/docs/demo/profile-night-view.svg)
```

[github-profile-3d-contrib](https://github.com/yoshi389111/github-profile-3d-contrib) — та же история, что у нас в [Профиле](../templates/PROFILE-README-TEMPLATE.md)

## 8. Трофеи

```markdown
![trophy](https://github-profile-trophy.vercel.app/?username=overbaffe1&theme=tokyonight&no-frame=true&margin-w=8)
```

[github-profile-trophy](https://github.com/ryo-ma/github-profile-trophy)

---

### Честно про внешние картинки

| Плюс | Минус |
| --- | --- |
| Одна строка, красиво | Зависишь от чужого сервера — если ляжет, картинка пропадёт |
| Не нужен Actions | GitHub кеширует через camo ~1 час |
| | Не печатается на бумагу как наш `crystal-net.svg` |

Хочешь без зависимостей — бери блоки из [templates/blocks/](../templates/blocks/) (чистый Markdown, без картинок). Хочешь вау за 30 секунд — бери отсюда.

Есть свой приём? [Предложить блок](https://github.com/overbaffe1/gitEdit/issues/new?template=readme-block.yml)
