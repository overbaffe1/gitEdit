<!-- browser-desk:start -->
## Нажми точку — и GitHub станет редактором

**[Открыть этот репозиторий в VS Code для браузера](https://github.dev/overbaffe1/gitEdit)**. Или на странице репозитория GitHub, вне текстового поля, нажми <kbd>.</kbd>; <kbd>&gt;</kbd> открывает редактор в новой вкладке. **Нужен вход в GitHub.** Это официальный web-editor, не скриншот, не наше приложение и не iframe в README.

Вместо установки IDE и клонирования — дерево настоящих файлов, поиск, подсветка и панель Source Control. Для безопасного опыта достаточно читать код; **Commit & Push не нажимай**. Редактирование создаёт локальные изменения в хранилище браузера, а публикация через Source Control действительно меняет Git.

> [!NOTE]
> **github.dev — не Codespaces:** редактор бесплатный и работает в браузере, но не даёт вычислительной машины, обычного терминала и запуска наших Python-генераторов. Платный codespace здесь не создаётся; не выбирай переход в Codespaces ради этого опыта.

### Три остановки по настоящему коду

В web-editor найди нужный файл через **Go to File** или дерево. В обычном GitHub открой ссылку «Код», затем Symbols и имя функции: переходы к определениям/ссылкам зависят от доступности индексации. «Точные строки» работают как запасной путь без Symbols.

| Что исследовать | Код на активной ветке | Неизменяемый фрагмент | История строк |
|---|---|---|---|
| Геометрия вращаемого STL: `mesh` | [Код](https://github.com/overbaffe1/gitEdit/blob/main/atlas/samples/native_lab/generate.py) | [Точные строки 45–59](https://github.com/overbaffe1/gitEdit/blob/fa5c788fcb2acffe988eb821642a6e8033fd366d/atlas/samples/native_lab/generate.py#L45-L59) | [Blame](https://github.com/overbaffe1/gitEdit/blame/fa5c788fcb2acffe988eb821642a6e8033fd366d/atlas/samples/native_lab/generate.py) |
| Как сшиваются линии рельефа: `contours` | [Код](https://github.com/overbaffe1/gitEdit/blob/main/atlas/samples/contourpress/generate.py) | [Точные строки 25–47](https://github.com/overbaffe1/gitEdit/blob/fa5c788fcb2acffe988eb821642a6e8033fd366d/atlas/samples/contourpress/generate.py#L25-L47) | [Blame](https://github.com/overbaffe1/gitEdit/blame/fa5c788fcb2acffe988eb821642a6e8033fd366d/atlas/samples/contourpress/generate.py) |
| Как устроены ссылки на форму: `links` | [Код](https://github.com/overbaffe1/gitEdit/blob/main/atlas/samples/github_controls/generate.py) | [Точные строки 7–11](https://github.com/overbaffe1/gitEdit/blob/fa5c788fcb2acffe988eb821642a6e8033fd366d/atlas/samples/github_controls/generate.py#L7-L11) | [Blame](https://github.com/overbaffe1/gitEdit/blame/fa5c788fcb2acffe988eb821642a6e8033fd366d/atlas/samples/github_controls/generate.py) |

**Ещё два встроенных приёма:** на странице кода нажми <kbd>y</kbd>, чтобы заменить ссылку на ветку постоянной ссылкой на коммит; <kbd>b</kbd> открывает Blame. Нажатие <kbd>?</kbd> показывает доступные горячие клавиши GitHub. Раскладка, фокус и настройки доступности могут влиять на сочетания.

Номера строк выше **получены из Python AST**, а не набраны вручную. [Маршрут JSON](assets/browser-desk/tour.json) · [Таблица CSV](assets/browser-desk/tour.csv) · [Подробности, приватность черновиков и границы проверки](atlas/browser-desk.md). Внутри README по-прежнему нет исполняемого редактора; ссылка открывает официальный сервис GitHub.

<!-- browser-desk:end -->

