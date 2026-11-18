[← Полевой атлас](README.md) · [Картография и 3D](relief.md) · [Кристалл отдельным STL](../assets/crystal.stl)

# Что умеет сам README

Формулы и разметку показывает сам GitHub. Схемы уже отрисованы, поэтому при чтении Mermaid не загружается. Рядом с рисунками есть отдельные `.mmd`: в режиме **Code** можно скопировать их текст.

## Схема состояний

В цветопробе два исхода: отправить лист в печать или вернуть его к эскизу. Стрелка назад передаёт эту разницу лучше линейного списка.

<p><a href="../assets/mermaid/edition.png"><img src="../assets/mermaid/edition.png" width="210" alt="Из цветопробы можно вернуться к эскизу или отправить лист в тираж."></a></p>

[Скопировать чистый `.mmd`](samples/edition.mmd). Внутри Markdown добавь вокруг него ограждение `mermaid`; в самом `.mmd` обратные кавычки не нужны.

## Доли и длительности

**Круговая диаграмма** отвечает на вопрос «сколько от целого?». Здесь числа учебные: шесть частей бумаги, три части чернил и одна часть акцента.

<p><a href="../assets/mermaid/ink-share.png"><img src="../assets/mermaid/ink-share.png" width="510" alt="Шесть частей бумаги, три части чернил, одна часть акцента."></a></p>

[Исходник круговой диаграммы](samples/ink-share.mmd).

**Диаграмма Ганта** отвечает на другой вопрос — «что после чего и сколько длится?». Вторая работа начинается после первой, а не в произвольную дату.

<p><a href="../assets/mermaid/schedule.png"><img src="../assets/mermaid/schedule.png" width="650" alt="Последовательно: два дня эскиза, один день цветопробы, два дня печати."></a></p>

[Исходник диаграммы Ганта](samples/schedule.mmd). Другие рисунки: [архитектура](../assets/mermaid/presentation.png), [диалог сервисов](../assets/mermaid/task-sequence.png), [граф коммитов](../assets/mermaid/commits.png). Если свежий синтаксис из редактора не работает в твоём README, блок `mermaid` с единственной строкой `info` покажет версию движка GitHub. Документация [2](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams).

## Формула вместо картинки

У нашего [кристалла](../assets/crystal.stl) число граней $F=8$. Характеристику Эйлера удобно показать отдельной строкой:

```math
V-E+F = 6-12+8 = 2
```

<details>
<summary>Скопировать обе формы записи</summary>

````markdown
Число граней $F=8$.

```math
V-E+F = 6-12+8 = 2
```
````

</details>

В GitHub Markdown формулы набираются в синтаксисе LaTeX, их отображает MathJax. Для блочной записи также подходят `$$`. GitHub Docs [1](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions).

## Редакторский стол

**Правка с первого взгляда.** Блок `diff` подсвечивает добавленные и удалённые строки. Это иллюстрация в документе, а не настоящий diff коммита:

```diff
- Название проекта и двенадцать бейджей.
+ Покрути модель. Затем скачай исходник и измени одну вершину.
```

**Лист приёмки.** В исходнике используй `- [x]` или `- [ ]`. Это состояние документа, не голосование: отметки меняют в самом Markdown.

- [x] У модели есть ссылка на файл.
- [x] Смысл схемы понятен без цвета.[^shape]
- [ ] Подставить данные собственного проекта перед публикацией.

<details>
<summary><b>Почему на полях нет цветных кружков рядом с HEX?</b></summary>

В README `#EF6747` в обратных кавычках — текст. Автоматические образцы HEX, RGB и HSL задокументированы для Issues, PR и Discussions, не для README. Для читателя покажи отдельную [цветопробу](../assets/relief-riso.svg), а значение оставь доступным для копирования. В [картотеке](samples/inkbook/) есть те же краски для GIMP и пример строки для ревью палитры. GitHub Docs [1](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

</details>

> [!TIP]
> Спрячь длинный исходник под `<details>`, но не саму ссылку на результат. Проверь раскрытие с клавиатуры: <kbd>Tab</kbd> до заголовка, затем <kbd>Enter</kbd>.

**Ещё из набора:** [шаблон с бейджами](../templates/PROJECT-README-TEMPLATE.md), [ризограф](../assets/relief-riso.svg), [фосфор](../assets/relief-phosphor.svg), [ролик LazyGit](https://github.com/user-attachments/assets/031799d1-740d-4cda-90cf-689513fa9860) и [обложка «Чертёж»](../assets/cover-project.svg). Для внешнего видео достаточно картинки-ссылки; не рассчитывай на YouTube-iframe внутри README.

[^shape]: Это живая сноска. В исходнике у текста стоит `[^shape]`, а определение начинается с `[^shape]:`. На схеме полезно подписывать линии и узлы, а не различать их только оттенком.
