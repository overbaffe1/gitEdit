"""Native exclusive details. No scripts, dependencies, dispatch or README writes."""
from pathlib import Path
import hashlib
import json
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).parent
ART=ROOT/'assets/exclusive-panel'
GROUP='gitedit-motion-desk-v1'
START='<!-- exclusive-panel:start -->'
END='<!-- exclusive-panel:end -->'

def panel(prefix=''):
 return f'''<details name="{GROUP}" open>
<summary><strong>01 · Статика — рассмотреть кадр</strong></summary>

<img src="{prefix}assets/motion-formats/poster.png" width="384" alt="Неподвижный бирюзовый куб и оранжевая точка со следом на прозрачном фоне.">

**Кадр без автодвижения.** Теперь открой второй режим: этот должен закрыться сам, а страница останется той же.

</details>
<details name="{GROUP}">
<summary><strong>02 · Движение — открыть петлю</strong></summary>

<picture>
  <source media="(prefers-reduced-motion: reduce)" srcset="{prefix}assets/motion-formats/poster.png">
  <img src="{prefix}assets/motion-formats/cube.gif" width="384" alt="Записанная петля вращения куба, 32 кадра; это не управляемая 3D-модель.">
</picture>

**Тот же сюжет в движении.** При системном предпочтении уменьшенного движения показывается неподвижный кадр. Чтобы убрать петлю с экрана, открой другой режим или сверни этот. Это не точная пауза/перемотка GIF; декодирование и загрузка закрытого содержимого зависят от браузера.

</details>
<details name="{GROUP}">
<summary><strong>03 · Исходник — повторить аккордеон</strong></summary>

Одинаковый **`name`** объединяет секции. Открытие одной закрывает другую. `open` задаёт только начальное раскрытие. Можно закрыть и последнюю — это аккордеон, не radio-tabs с обязательным выбранным пунктом.

```html
<details name="my-project-demo" open>
  <summary>Первый режим</summary>
  <p>Начальный экран.</p>
</details>
<details name="my-project-demo">
  <summary>Второй режим</summary>
  <p>Первый закроется при открытии второго.</p>
</details>
```

Для второй независимой группы выбери другое имя. Все секции с тем же именем в одном документе связаны, даже если стоят далеко друг от друга. Пустые строки после `summary` и перед закрытием `details` нужны, если внутри используется Markdown.

</details>
'''

def block():
 return START+'''
## Один экран — три режима, без JavaScript

**Нажми «02 · Движение» — «01 · Статика» закроется автоматически.** Затем открой исходник. Это настоящий переключаемый аккордеон **на этой же странице**, не переход в другой Markdown-файл и не скриншот интерфейса.

'''+panel()+'''
Управление: нажми заголовок мышью либо перейди к нему клавишей **Tab** и нажми **Enter / Пробел**. Без отправки данных, сохранения в Git и запуска Actions. Картинки взяты из уже существующей демонстрации форматов — новая возможность здесь именно взаимоисключающее раскрытие `details name`.

В старом браузере секции могут раскрываться независимо; содержимое останется доступным. Поддержка GitHub-санитайзера и браузера важна: [что проверено](atlas/exclusive-panel.md) · [готовый фрагмент TXT](assets/exclusive-panel/panel.txt). Для переноса картинок нужны также два локальных файла, перечисленные в инструкции. Это аккордеон, не настоящий видеоплеер и не скрытая возможность запускать JS.

'''+END+'\n\n'

def main():
 ART.mkdir(parents=True,exist_ok=True)
 for asset in ['poster.png','cube.gif']:
  if not (ROOT/'assets/motion-formats'/asset).is_file():raise FileNotFoundError(asset)
 (HERE/'readme-block.md').write_text(block())
 (ART/'panel.txt').write_text(panel())
 files=[HERE/'readme-block.md',ART/'panel.txt',ROOT/'assets/motion-formats/poster.png',ROOT/'assets/motion-formats/cube.gif']
 (ART/'manifest.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2)+'\n')
if __name__=='__main__':main()
