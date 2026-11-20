"""Package a labelled local example and README entry; never dispatch a workflow."""
from pathlib import Path
import importlib.util,json,hashlib
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).parent;OUT=ROOT/'assets/actions-lab'
START='<!-- actions-lab:start -->';END='<!-- actions-lab:end -->'
def main():
 spec=importlib.util.spec_from_file_location('actions_payload',HERE/'run.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 sample=OUT/'example';sample.mkdir(parents=True,exist_ok=True)
 for name,data in mod.build(mod.parse_inputs({})).items():(sample/name).write_bytes(data)
 b=START+'''
## GitHub Actions как пульт эксперимента

**[Открыть ручной стенд в Actions](https://github.com/overbaffe1/gitEdit/actions/workflows/native-lab.yml)**. Это нативная страница GitHub с формой **Run workflow**, не нарисованная кнопка в README. Для запуска нужны вход, права записи и разрешённые Actions; workflow должен находиться в default branch.

Выбери расположение точек (`orbit` / `spiral`), число от 12 до 96, палитру и флажок CSV. После **явного запуска** GitHub выделяет runner, создаёт файлы, показывает отчёт в **Summary** и сохраняет скачиваемый **artifact**. Результаты не записываются в Git и не меняют README.

> [!WARNING]
> Второе нажатие **Run workflow** действительно запускает облачные вычисления. Это не бесплатный предпросмотр по определению: действуют политика Actions, квоты и условия оплаты репозитория. Для простого осмотра формы запуск не нужен. В этой работе workflow **не запускался**.

Что здесь можно увидеть нового:

- **Типизированные inputs** — choice, number и boolean в форме GitHub; скрипт повторно проверяет значения.
- **Job Summary** — собственный Markdown-отчёт на странице запуска, не только консольный лог.
- **Artifacts** — SVG, JSON, отчёт и необязательный CSV в скачиваемом архиве. Хранение запрошено на 3 дня; для загрузки нужен вход и доступ, могут действовать ограничения политики.
- **Настоящая ссылка на artifact** появляется из результата upload-action, а не угадывается заранее.

[Локальный образец отчёта — не облачный запуск](assets/actions-lab/example/summary.md) · [Образец SVG](assets/actions-lab/example/drawing.svg) · [Workflow YAML](.github/workflows/native-lab.yml) · [Как работает и какие есть ограничения](atlas/actions-lab.md).

Этот опыт открывается в Actions, не исполняется внутри README. Автотриггеров push/PR/schedule нет. Никакие Actions или настройки оплаты за читателя не включаются; все прежние стенды ниже сохранены.

'''+END+'\n\n'
 (HERE/'readme-block.md').write_text(b)
 paths=[ROOT/'.github/workflows/native-lab.yml',HERE/'run.py',*sorted(sample.iterdir())]
 (OUT/'manifest.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},indent=2)+'\n')
if __name__=='__main__':main()
