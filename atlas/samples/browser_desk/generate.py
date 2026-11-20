"""AST-backed native GitHub code tour; no code execution or network calls."""
from pathlib import Path
import ast,json,hashlib,csv,io
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).parent;OUT=ROOT/'assets/browser-desk'
START='<!-- browser-desk:start -->';END='<!-- browser-desk:end -->'
TARGETS=[('atlas/samples/native_lab/generate.py','mesh','Геометрия вращаемого STL'),('atlas/samples/contourpress/generate.py','contours','Как сшиваются линии рельефа'),('atlas/samples/github_controls/generate.py','links','Как устроены ссылки на форму')]
def collect():
 sha=json.loads((HERE/'config.json').read_text())['base_commit'];records=[]
 for path,symbol,label in TARGETS:
  data=(ROOT/path).read_bytes();tree=ast.parse(data);fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name==symbol)
  calls=sorted(n.lineno for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id==symbol)
  records.append({'path':path,'symbol':symbol,'label':label,'commit':sha,'sha256':hashlib.sha256(data).hexdigest(),'start':fn.lineno,'end':fn.end_lineno,'direct_calls_in_same_file':calls,'source':'https://github.com/overbaffe1/gitEdit/blob/main/'+path,'permalink':f'https://github.com/overbaffe1/gitEdit/blob/{sha}/{path}#L{fn.lineno}-L{fn.end_lineno}','blame':f'https://github.com/overbaffe1/gitEdit/blame/{sha}/{path}'})
 return records
def main():
 OUT.mkdir(parents=True,exist_ok=True);records=collect()
 (OUT/'tour.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
 s=io.StringIO(newline='');w=csv.writer(s,lineterminator='\n');w.writerow(['symbol','path','start','end','direct_calls_in_same_file','permalink'])
 for r in records:w.writerow([r['symbol'],r['path'],r['start'],r['end'],len(r['direct_calls_in_same_file']),r['permalink']])
 (OUT/'tour.csv').write_text(s.getvalue())
 b=START+'''
## Нажми точку — и GitHub станет редактором

**[Открыть этот репозиторий в VS Code для браузера](https://github.dev/overbaffe1/gitEdit)**. Или на странице репозитория GitHub, вне текстового поля, нажми <kbd>.</kbd>; <kbd>&gt;</kbd> открывает редактор в новой вкладке. **Нужен вход в GitHub.** Это официальный web-editor, не скриншот, не наше приложение и не iframe в README.

Вместо установки IDE и клонирования — дерево настоящих файлов, поиск, подсветка и панель Source Control. Для безопасного опыта достаточно читать код; **Commit & Push не нажимай**. Редактирование создаёт локальные изменения в хранилище браузера, а публикация через Source Control действительно меняет Git.

> [!NOTE]
> **github.dev — не Codespaces:** редактор бесплатный и работает в браузере, но не даёт вычислительной машины, обычного терминала и запуска наших Python-генераторов. Платный codespace здесь не создаётся; не выбирай переход в Codespaces ради этого опыта.

### Три остановки по настоящему коду

В web-editor найди нужный файл через **Go to File** или дерево. В обычном GitHub открой ссылку «Код», затем Symbols и имя функции: переходы к определениям/ссылкам зависят от доступности индексации. «Точные строки» работают как запасной путь без Symbols.

| Что исследовать | Код на активной ветке | Неизменяемый фрагмент | История строк |
|---|---|---|---|
'''
 for r in records:b+=f'| {r["label"]}: `{r["symbol"]}` | [Код]({r["source"]}) | [Точные строки {r["start"]}–{r["end"]}]({r["permalink"]}) | [Blame]({r["blame"]}) |\n'
 b+='''
**Ещё два встроенных приёма:** на странице кода нажми <kbd>y</kbd>, чтобы заменить ссылку на ветку постоянной ссылкой на коммит; <kbd>b</kbd> открывает Blame. Нажатие <kbd>?</kbd> показывает доступные горячие клавиши GitHub. Раскладка, фокус и настройки доступности могут влиять на сочетания.

Номера строк выше **получены из Python AST**, а не набраны вручную. [Маршрут JSON](assets/browser-desk/tour.json) · [Таблица CSV](assets/browser-desk/tour.csv) · [Подробности, приватность черновиков и границы проверки](atlas/browser-desk.md). Внутри README по-прежнему нет исполняемого редактора; ссылка открывает официальный сервис GitHub.

'''+END+'\n\n'
 (HERE/'readme-block.md').write_text(b)
 (OUT/'manifest.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.iterdir()) if p.name!='manifest.json'},indent=2)+'\n')
if __name__=='__main__':main()
