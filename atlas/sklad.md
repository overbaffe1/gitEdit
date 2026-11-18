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

## 9. Счётчик просмотров

```markdown
![views](https://komarev.com/ghpvc/?username=overbaffe1&label=Profile%20views&color=0e75b6&style=flat)
```
[komarev.com/ghpvc](https://github.com/antonkomarev/github-profile-views-counter) — хитс-каунтер, без Actions

## 10. Holopin — полка бейджей

```markdown
[![@you Holopin](https://holopin.me/overbaffe1)](https://holopin.io/@overbaffe1)
```
Собери на [holopin.io](https://holopin.io) → embed автоматически

## 11. Цитата / шутка

```markdown
![quote](https://github-readme-quotes-bay.vercel.app/api?theme=tokyonight)
![joke](https://readme-jokes.vercel.app/api?theme=dark)
```
[quotes](https://github.com/shravan20/github-readme-quotes) + [jokes](https://github.com/ABSphreak/readme-jokes)

## 12. LeetCode / Codewars

```markdown
![leetcode](https://leetcode-stats.vercel.app/api?username=overbaffe1)
![codewars](https://github.r2v.ch/codewars?user=overbaffe1)
```
[leetcode-stats](https://github.com/jeremyxu2010/leetcode-stats) / [codewars readme stats](https://github.com/CoderCoyAstro/CodWars-readme-stats)

## 13. Spotify Now Playing

```markdown
![spotify](https://spotify-readme-card.vercel.app/api/spotify?scan=true)
```
Нужен OAuth → [spotify-github-profile](https://spotify-github-profile.kittinanx.com) или селф-хост [spotify-card](/assets/spotify-card.svg)

## 14. Шахматы — игра прямо в README

```markdown
| Шахматы — White to move |
|---|
| ![board](https://raw.githubusercontent.com/marcizhu/readme-chess/master/board.svg) |
| [Сделать ход](https://github.com/USER/USER/issues/new?title=chess%7Cmove%20e2e4&labels=chess) |
```
Workflow: [templates/workflows/chess.yml](../templates/workflows/chess.yml) · [marcizhu/readme-chess](https://github.com/marcizhu/readme-chess)

## 15. 3 режима капсул

```markdown
![waving](https://capsule-render.vercel.app/api?type=waving&color=gradient&height=180)
![slice](https://capsule-render.vercel.app/api?type=slice&color=gradient&height=140&text=SUP)
![cylinder](https://capsule-render.vercel.app/api?type=cylinder&color=gradient&height=120)
```
Все типы: `waving / slice / cylinder / transparent / rect / soft / shark` — [capsule-render](https://github.com/kyechan99/capsule-render)

---

_Склад вырос с 8 до 15 строк. Хочешь сразу 100? Листай полный [warehouse.md](warehouse.md) или [витрину в README](../README.md) — там уже 70+ селф-хостед SVG._
