# Сигнал потерян — квест в одном Markdown

[← Галерея](../../README.md) · [Как это работает](../fragment-quest.md)

**Выбирай текстовые действия внутри открытой сцены.** Ссылка ведёт к скрытому содержимому другой секции: браузер раскрывает её, а общий `details name` закрывает предыдущую. Документ не перезагружается, меняется фрагмент адреса.

Это небольшой гипертекстовый квест, не новый движок GitHub. Все сцены публичны; можно раскрывать заголовки вручную. Нет секретного состояния, счёта, инвентаря или записи выбора в Git.

**Совместимость:** проверен ответ GitHub Markdown API в локальном Chromium, не production-интерфейс github.com со всеми его скриптами. Если ссылка только прокрутила страницу или ничего не раскрыла, открой нужный пронумерованный заголовок вручную. Названия целевых сцен указаны у каждого действия.

<details name="gitedit-fragment-quest-v1" open>
<summary><strong>00 / Приёмная</strong></summary>

<p id="fq-scene-dock"><strong>SIGNAL / LOST</strong></p>

Ночная станция потеряла маяк. На столе лежат линза и наушники. Нужно найти позывной и выбрать правильный канал.

- [Взять линзу](#user-content-fq-scene-lens) → 01 / Оптика
- [Надеть наушники](#user-content-fq-scene-radio) → 02 / Приёмник

</details>

<details name="gitedit-fragment-quest-v1">
<summary><strong>01 / Оптика</strong></summary>

<p id="fq-scene-lens"><strong>LENS / THREE DOTS</strong></p>

Под линзой видны три короткие царапины: · · ·. На обороте записано: «Сначала слушай, потом передавай». Это подсказка, не найденный предмет в инвентаре.

- [Послушать эфир](#user-content-fq-scene-radio) → 02 / Приёмник
- [Сразу нажать передачу](#user-content-fq-scene-echo) → 05 / Эхо

</details>

<details name="gitedit-fragment-quest-v1">
<summary><strong>02 / Приёмник</strong></summary>

<p id="fq-scene-radio"><strong>RX / SILENCE / RX</strong></p>

Сквозь треск слышен позывной «ИРИС». Голос просит перейти на тихий канал. Передатчик имеет два режима.

- [Выбрать тихий канал](#user-content-fq-scene-quiet) → 03 / Тихий канал
- [Включить усилитель](#user-content-fq-scene-loud) → 04 / Усилитель

</details>

<details name="gitedit-fragment-quest-v1">
<summary><strong>03 / Тихий канал</strong></summary>

<p id="fq-scene-quiet"><strong>CHANNEL / LOW</strong></p>

В эфире почти тихо. Нужно произнести услышанный позывной. Все варианты находятся в этом документе: игра не проверяет память и не запрещает заглядывать в другие сцены.

- [Передать «ИРИС»](#user-content-fq-scene-rescue) → 06 / Маяк найден
- [Передать «АТЛАС»](#user-content-fq-scene-echo) → 05 / Эхо

</details>

<details name="gitedit-fragment-quest-v1">
<summary><strong>04 / Усилитель</strong></summary>

<p id="fq-scene-loud"><strong>GAIN / OVERLOAD</strong></p>

Усилитель поднял шум вместе с сигналом. Станция не сломалась: можно вернуться к приёмнику и попробовать другой канал.

- [Вернуться к приёмнику](#user-content-fq-scene-radio) → 02 / Приёмник
- [Начать заново](#user-content-fq-scene-dock) → 00 / Приёмная

</details>

<details name="gitedit-fragment-quest-v1">
<summary><strong>05 / Эхо</strong></summary>

<p id="fq-scene-echo"><strong>TX / NO REPLY</strong></p>

Станция вернула только эхо. Это один из двух исходов истории, не штраф и не реальная отправка радиосигнала.

- [Сбросить маршрут](#user-content-fq-scene-dock) → 00 / Приёмная
- [Вернуться к приёмнику](#user-content-fq-scene-radio) → 02 / Приёмник

</details>

<details name="gitedit-fragment-quest-v1">
<summary><strong>06 / Маяк найден</strong></summary>

<p id="fq-scene-rescue"><strong>IRIS / LINK RESTORED</strong></p>

Маяк ответил тремя короткими вспышками. Связь восстановлена. Ты дошёл до второго исхода истории — без Issue, Actions, стороннего сервера и JavaScript.

- [Сыграть ещё раз](#user-content-fq-scene-dock) → 00 / Приёмная
- [Посмотреть первую подсказку](#user-content-fq-scene-lens) → 01 / Оптика

</details>

---

Если закрыл всё вручную, раскрой **00 / Приёмная**. Ссылки на уже выбранную сцену не используются в графе: повторная навигация к тому же hash после ручного закрытия может не повторить раскрытие. Для прямой ссылки на сцену копируй адрес после перехода, но учитывай зависимость от префикса санитайзера GitHub.
