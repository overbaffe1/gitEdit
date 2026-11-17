[← Полевой атлас](README.md) · [Что работает прямо в README](native.md) · [Разборы чужих проектов](inspiration.md)

# Оформление за пределами README

Иногда правильное место для элемента — не шапка репозитория. Ниже у каждого приёма есть пример или экран из документации и место, в котором его настраивают. Это обзор: настройки gitEdit не менялись.

## Профиль, организация, репозиторий

- **Личный профиль.** [Страница Саймона](https://github.com/simonw) и [исходник её центрального блока](https://github.com/simonw/simonw) — разные страницы. Для своего профиля нужен публичный репозиторий с именем аккаунта и непустым корневым `README.md`. [Инструкция](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme).
- **Закрепления.** В **Customize your pins** можно вместе выбрать до шести репозиториев и gist. Это аккуратная замена шести однотипным карточкам в README. [Посмотреть элементы управления](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/pinning-items-to-your-profile).
- **Страница команды.** Сравни [профиль организации GitHub](https://github.com/github) и [его исходник](https://github.com/github/.github/blob/main/profile/README.md). Для публичной версии путь — `profile/README.md` в репозитории организации `.github`, а не `.github/README.md` рабочего проекта. GitHub Docs [3](https://docs.github.com/en/organizations/collaborating-with-groups-in-organizations/customizing-your-organizations-profile).
- **Первый экран репозитория.** Если GitHub показывает «не тот» README, проверь, нет ли нескольких: приоритет у `.github/README`, затем у корневого README, затем у `docs/README` (в том числе `.md`). Относительные ссылки внутри файла считаются от его расположения. GitHub Docs [2](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes).
- **Боковая колонка About.** Одна фраза, адрес рабочего демо, несколько точных topics. Нажатие на тему ведёт в каталог: [например, подборка профилей](https://github.com/topics/profile-readme). [Как добавить темы](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics).

## Карточка ссылки

[Посмотреть готовый PNG gitEdit](samples/social-preview.png) · [Редактируемый вектор](samples/atlas-plate.svg) · [Печатный PDF того же листа](samples/field-sheet.pdf).

**Social preview** — картинка при отправке ссылки на репозиторий, а не баннер внутри README. Владелец может загрузить файл в **Settings → Social preview → Edit**. Наш PNG уже 1280 × 640; в документации рекомендован этот размер и файл меньше 1 МБ. Само наличие PNG в Git **не применяет** настройку. GitHub Docs [1](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview).

## Дать посетителю следующее действие

| Хочется… | Куда посмотреть и как устроено |
|---|---|
| **Показать, что нового** | [Релизы GitHub CLI](https://github.com/cli/cli/releases/latest): отдельная страница для описания версии и файлов. Положи в README ссылку на последний релиз вместо копии всего changelog. [О релизах](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases). |
| **Собрать баг-репорт** | [Реальная форма GitHub Docs в YAML](https://github.com/github/docs/blob/main/.github/ISSUE_TEMPLATE/improve-existing-docs.yaml). В `.github/ISSUE_TEMPLATE/` форма задаёт поля для **нового Issue**; в Markdown достаточно ссылки. [Скриншоты и схема настройки](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository). |
| **Дать правильную цитату** | Открой [проект Citation File Format](https://github.com/citation-file-format/citation-file-format), затем [его `CITATION.cff`](https://github.com/citation-file-format/citation-file-format/blob/main/CITATION.cff). Метаданные в корне включают **Cite this repository** с вариантами APA и BibTeX. [Инструкция](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files). |
| **Вынести справочник** | [Wiki проекта Jupyter](https://github.com/jupyter/jupyter/wiki) — отдельные страницы и навигация. Из README оставь вход в справочник. [Про Wiki и доступность](https://docs.github.com/en/communities/documenting-your-project-with-wikis/about-wikis). |
| **Обсудить идею** | [GitHub Community Discussions](https://github.com/orgs/community/discussions) — разговоры и категории, а не форма внутри README. Для комментариев на собственном сайте есть [пример giscus](https://giscus.app/). |
| **Сделать полноценный сайт** | [Тема Cayman вживую](https://pages-themes.github.io/cayman/) и [её исходники](https://github.com/pages-themes/cayman). **Pages** публикует статический сайт с HTML/CSS/JS; кнопка-ссылка в README только ведёт на него. [Как устроены Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages). |

**Фон во весь экран:** у [обложки README](../README.md#мастерская-оформления) пейзаж заканчивается по краю картинки. В [нашем HTML-примере](north.html) он лежит и за выделяемым текстом, и за панелью управления. Чтобы попробовать галочку паузы, открой страницу из распакованного архива в браузере; в списке файлов GitHub это исходный код. [Кадры и рецепт](../README.md#повторить-мастерскую-оформления).

## Ещё четыре поверхности, которые легко спутать с README

- **Roadmap.** Открой [публичную дорожную карту GitHub](https://github.com/orgs/github/projects/4247) и [пояснение к её полям](https://github.com/github/roadmap). Это представление **Projects**: можно показывать тот же набор задач в нескольких видах, а в README оставить вход в нужный.
- **Голосование.** Для выбора следующей темы используй опрос в **Discussions**, а не чекбоксы в `.md`: голоса должны где-то сохраняться. [Посмотреть, как создаётся poll](https://docs.github.com/en/discussions/collaborating-with-your-community-using-discussions/participating-in-a-discussion#creating-a-poll).
- **Спонсорство.** У [проекта Mermaid](https://github.com/mermaid-js/mermaid/blob/develop/.github/FUNDING.yml) видны реальные поля файла. Кнопка **Sponsor** настраивается через Sponsorships и `.github/FUNDING.yml` в основной ветке, а не через розовый бейдж. GitHub Docs [1](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/displaying-a-sponsor-button-in-your-repository).
- **Итог сборки.** В **Actions** можно показать Markdown-отчёт прямо в сводке запуска. Например, шаг с `printf '### Готово\nПроверены три палитры.\n' >> "$GITHUB_STEP_SUMMARY"` добавит заголовок и строку текста. [Пример и вид сводки](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands#adding-a-job-summary). Запускать workflow для просмотра документации не нужно.

## Три фокуса для ревью

1. **Дизайнерский diff.** В изменении изображения попробуй **2-up** (рядом), **Swipe** (ползунок) и **Onion skin** (наложение). [Реальные скриншоты всех режимов](https://docs.github.com/en/repositories/working-with-files/using-files/working-with-non-code-files#viewing-differences). Это сравнение *двух версий одного файла*, не эффект для двух картинок в README.
2. **Вёрстка до и после.** В PR с изменённым `.md` переключись с исходника на rendered diff — станет видно, как поменялся сам абзац. [Скриншот результата](https://docs.github.com/en/repositories/working-with-files/using-files/working-with-non-code-files#rendering-differences-in-prose-documents).
3. **Ссылка, которая не съедет.** [Первые строки workflow на фиксированном коммите](https://github.com/overbaffe1/gitEdit/blob/31388d6c1c6bfc52cb1c8d93dc8f46ab69425fb5/templates/profile-snake-workflow.yml#L1-L8). Именно SHA, а не имя ветки, фиксирует версию. Автоматическая вставка такого фрагмента кода — возможность комментариев в том же репозитории; в `.md` оставь ссылку или обычный блок кода. [Как получить permalink](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-a-permanent-link-to-a-code-snippet).

**Правило выбора:** вращать [кристалл](../README.md#покрути-кристалл) и приближать [карты](../README.md#две-карты) можно прямо в README. Для фильтра по строкам CSV или предпросмотра PDF нужен [просмотрщик файла](README.md#витрина-файлов), а для интерфейса со своим JavaScript — отдельный сайт.
