<!-- resize-scan:start -->
## Ширина окна вместо ручки сканера

**На компьютере медленно сузь и расширь окно браузера.** Картинка ниже будет менять не только размер, но и **срез синтетической детали** — прямо здесь, без JS, перезагрузки и открытия другого сайта.

<picture>
  <source media="(max-width: 599px)" srcset="assets/resize-scan/slice-00.svg">
  <source media="(max-width: 679px)" srcset="assets/resize-scan/slice-01.svg">
  <source media="(max-width: 759px)" srcset="assets/resize-scan/slice-02.svg">
  <source media="(max-width: 839px)" srcset="assets/resize-scan/slice-03.svg">
  <source media="(max-width: 919px)" srcset="assets/resize-scan/slice-04.svg">
  <source media="(max-width: 999px)" srcset="assets/resize-scan/slice-05.svg">
  <source media="(max-width: 1079px)" srcset="assets/resize-scan/slice-06.svg">
  <source media="(max-width: 1159px)" srcset="assets/resize-scan/slice-07.svg">
  <source media="(max-width: 1239px)" srcset="assets/resize-scan/slice-08.svg">
  <source media="(max-width: 1319px)" srcset="assets/resize-scan/slice-09.svg">
  <source media="(max-width: 1399px)" srcset="assets/resize-scan/slice-10.svg">
  <source media="(max-width: 1479px)" srcset="assets/resize-scan/slice-11.svg">
  <img src="assets/resize-scan/slice-12.svg" width="840" alt="Синтетическое сечение цилиндра с движущимся по глубине отверстием. Ширина окна выбирает один из 13 кадров; все кадры доступны отдельно в инструкции.">
</picture>

Это **13 заранее вычисленных кадров**, а не настоящий range-ползунок, медицинский сканер или расчёт на лету. Выбор делает браузер через `picture` → `source media`; ширина — всего окна в CSS-пикселях, не самой картинки. До 599 px показывается первый кадр, от 1480 px — последний, между ними шаг 80 px. Изменения происходят только при пересечении порогов.

На телефоне и маленьком экране все положения могут быть недоступны. **[Все кадры и таблица порогов без изменения окна](atlas/resize-scan.md)** · [Исходник для переноса TXT](assets/resize-scan/picture.txt). Это необычное применение уже знакомого responsive `picture`, не новая скрытая функция GitHub. Самопроизвольной анимации, звука и backend нет; все прежние разделы ниже сохранены.

<!-- resize-scan:end -->

