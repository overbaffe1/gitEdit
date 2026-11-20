"""One Markdown document, native fragment reveal + exclusive details. No JS."""
from pathlib import Path
import hashlib
import json
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).parent;ART=ROOT/'assets/fragment-quest';PLAY=ROOT/'atlas/fragment-quest/README.md'
GROUP='gitedit-fragment-quest-v1';PREFIX='fq-scene-'
# Independent original story. State is public and finite, not a saved inventory.
SCENES=[
 ('dock','00 / Приёмная','SIGNAL / LOST',
  'Ночная станция потеряла маяк. На столе лежат линза и наушники. Нужно найти позывной и выбрать правильный канал.',
  [('lens','Взять линзу'),('radio','Надеть наушники')]),
 ('lens','01 / Оптика','LENS / THREE DOTS',
  'Под линзой видны три короткие царапины: · · ·. На обороте записано: «Сначала слушай, потом передавай». Это подсказка, не найденный предмет в инвентаре.',
  [('radio','Послушать эфир'),('echo','Сразу нажать передачу')]),
 ('radio','02 / Приёмник','RX / SILENCE / RX',
  'Сквозь треск слышен позывной «ИРИС». Голос просит перейти на тихий канал. Передатчик имеет два режима.',
  [('quiet','Выбрать тихий канал'),('loud','Включить усилитель')]),
 ('quiet','03 / Тихий канал','CHANNEL / LOW',
  'В эфире почти тихо. Нужно произнести услышанный позывной. Все варианты находятся в этом документе: игра не проверяет память и не запрещает заглядывать в другие сцены.',
  [('rescue','Передать «ИРИС»'),('echo','Передать «АТЛАС»')]),
 ('loud','04 / Усилитель','GAIN / OVERLOAD',
  'Усилитель поднял шум вместе с сигналом. Станция не сломалась: можно вернуться к приёмнику и попробовать другой канал.',
  [('radio','Вернуться к приёмнику'),('dock','Начать заново')]),
 ('echo','05 / Эхо','TX / NO REPLY',
  'Станция вернула только эхо. Это один из двух исходов истории, не штраф и не реальная отправка радиосигнала.',
  [('dock','Сбросить маршрут'),('radio','Вернуться к приёмнику')]),
 ('rescue','06 / Маяк найден','IRIS / LINK RESTORED',
  'Маяк ответил тремя короткими вспышками. Связь восстановлена. Ты дошёл до второго исхода истории — без Issue, Actions, стороннего сервера и JavaScript.',
  [('dock','Сыграть ещё раз'),('lens','Посмотреть первую подсказку')]),
]
def anchor(scene):return 'user-content-'+PREFIX+scene

def play():
 out=['# Сигнал потерян — квест в одном Markdown','',
 '[← Галерея](../../README.md) · [Как это работает](../fragment-quest.md)','',
 '**Выбирай текстовые действия внутри открытой сцены.** Ссылка ведёт к скрытому содержимому другой секции: браузер раскрывает её, а общий `details name` закрывает предыдущую. Документ не перезагружается, меняется фрагмент адреса.','',
 'Это небольшой гипертекстовый квест, не новый движок GitHub. Все сцены публичны; можно раскрывать заголовки вручную. Нет секретного состояния, счёта, инвентаря или записи выбора в Git.','',
 '**Совместимость:** проверен ответ GitHub Markdown API в локальном Chromium, не production-интерфейс github.com со всеми его скриптами. Если ссылка только прокрутила страницу или ничего не раскрыла, открой нужный пронумерованный заголовок вручную. Названия целевых сцен указаны у каждого действия.','']
 titles={s[0]:s[1] for s in SCENES}
 for key,title,display,text,edges in SCENES:
  out.extend([f'<details name="{GROUP}"'+(' open>' if key=='dock' else '>'),f'<summary><strong>{title}</strong></summary>','',f'<p id="{PREFIX+key}"><strong>{display}</strong></p>','',text,''])
  for target,label in edges:out.append(f'- [{label}](#{anchor(target)}) → {titles[target]}')
  out.extend(['','</details>',''])
 out.extend(['---','', 'Если закрыл всё вручную, раскрой **00 / Приёмная**. Ссылки на уже выбранную сцену не используются в графе: повторная навигация к тому же hash после ручного закрытия может не повторить раскрытие. Для прямой ссылки на сцену копируй адрес после перехода, но учитывай зависимость от префикса санитайзера GitHub.',''])
 return '\n'.join(out)

def block():return '''<!-- fragment-quest:start -->
## Квест в одном Markdown: ссылки открывают скрытые сцены

**[Играть: «Сигнал потерян»](atlas/fragment-quest/README.md)** — семь сцен, два исхода, без JavaScript и бота. Выбери действие в открытой сцене: обычная ссылка меняет фрагмент адреса и в проверенном браузере раскрывает нужный закрытый `details`; прежнюю сцену закрывает общий `name`.

В отличие от конструктора из отдельных файлов, весь маршрут находится **в одном документе**. Это не инвентарь и не тайный сервер: все сцены можно раскрыть вручную. [Механизм и границы проверки](atlas/fragment-quest.md) · [Граф маршрутов JSON](assets/fragment-quest/graph.json).

Проверено на HTML из GitHub Markdown API в локальном Chromium; интерфейс github.com со своими скриптами может влиять на переходы. Поэтому у каждого действия указан номер сцены и есть ручной запасной путь. Корневой README здесь содержит вход, сама игра открывается отдельным Markdown-документом — не выдаём ссылку за встроенный игровой виджет.

<!-- fragment-quest:end -->

'''

def main():
 ART.mkdir(parents=True,exist_ok=True);PLAY.parent.mkdir(parents=True,exist_ok=True)
 PLAY.write_text(play());(ART/'play.txt').write_text(play());(HERE/'readme-block.md').write_text(block())
 graph=[{'id':s[0],'title':s[1],'target_id':anchor(s[0]),'transitions':[{'target':t,'label':l} for t,l in s[4]]} for s in SCENES]
 (ART/'graph.json').write_text(json.dumps(graph,ensure_ascii=False,indent=2)+'\n')
 paths=[PLAY,ART/'play.txt',ART/'graph.json',HERE/'readme-block.md']
 (ART/'manifest.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},indent=2)+'\n')
if __name__=='__main__':main()
