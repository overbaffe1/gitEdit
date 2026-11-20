"""Publish native UI entry points; no issue submission, network or README editing."""
from pathlib import Path
from urllib.parse import urlencode
import json,hashlib
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).parent;OUT=ROOT/'assets/github-controls'
START='<!-- github-controls:start -->';END='<!-- github-controls:end -->'
def links():
 cfg=json.loads((HERE/'config.json').read_text());base='https://github.com/overbaffe1/gitEdit/'
 form=base+'issues/new?'+urlencode({'template':'native-playground.yml'})
 prefilled=base+'issues/new?'+urlencode({'template':'native-playground.yml','callsign':'Лунный архивариус'})
 return form,prefilled,base+'commit/'+cfg['rich_diff_commit']
def main():
 form,prefilled,diff=links()
 b=START+f'''
## Пульт GitHub: настоящие поля и визуальный diff

**Ещё две механики платформы, не картинки и не сторонний сайт.** Обе открываются на отдельных страницах GitHub — внутри README произвольную форму или diff-виджет не вставить.

### Покрути не модель, а сам интерфейс

**[Открыть нативную форму-песочницу]({form})** · [Та же форма с заполненным позывным]({prefilled}). Может понадобиться вход в GitHub. Это переход на страницу создания Issue, **не отправка**.

Там можно реально менять одиночный и множественный выбор, вводить текст и переключать флажки. GitHub строит форму из [этого YAML](.github/ISSUE_TEMPLATE/native-playground.yml), без нашего JavaScript.

1. Выбери поверхность: README, файл или история.
2. Отметь несколько интересных механик и измени текстовое поле.
3. Посмотри на обязательные поля и отдельное подтверждение публикации.
4. **Просто закрой страницу. Для демонстрации отправлять Issue не нужно.**

> [!WARNING]
> Кнопка Create/Submit issue создаст настоящую публичную запись, если проверки пройдены. Не вводи секреты и личные данные, не прикрепляй приватные файлы: вложение может начать загружаться ещё до отправки формы. На сохранение черновика или отсутствие сетевых запросов не рассчитывай.

### Посмотри изменения не в коде, а в готовом документе

**[Открыть настоящий rich diff Markdown]({diff})**. В коммите меняется только одна короткая карточка: жирный текст, таблица и нумерованный список. Выбери **Display the rich diff / Rendered**, если этот режим доступен в твоём интерфейсе. Сравни с Source: это те же изменения, но в отформатированном документе, а не в строках Markdown.

[Текущая карточка](assets/github-controls/revision.md) · [Её исходник](assets/github-controls/revision.md?plain=1) · [Что здесь умеет и чего не умеет GitHub](atlas/github-controls.md).

Ни форма, ни rich diff не встроены в эту страницу. Здесь настоящие входы в интерфейсы GitHub; ниже остаются вращаемый STL, карты и Mermaid прямо в README. Старое содержимое не удалено.

'''+END+'\n\n'
 (HERE/'readme-block.md').write_text(b)
 data=[{'id':'issue-form','entry':form,'context':'GitHub new issue page; may require sign-in','mutates_on_open':False,'note':'Submit creates a real issue; uploads can happen earlier. No claim of zero network traffic.'},{'id':'prefill','entry':prefilled,'context':'Same native form; callsign is a documented field-id query parameter','mutates_on_open':False},{'id':'rich-diff','entry':diff,'context':'Commit view, choose rendered diff if available','mutates_on_open':False}]
 (OUT/'mechanics.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 paths=[ROOT/'.github/ISSUE_TEMPLATE/native-playground.yml',OUT/'revision.md',OUT/'mechanics.json']
 (OUT/'manifest.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},indent=2)+'\n')
if __name__=='__main__':main()
