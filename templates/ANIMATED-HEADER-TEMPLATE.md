# Анимированная шапка — волна + печаталка

Копируешь два внешних SVG и получаешь живую шапку без Actions.

> [!TIP]
> Это шаблон для **профиля** `overbaffe1/overbaffe1`, не для `templates/blocks/`. Он держит внешние картинки, поэтому лежит отдельно — тест `test_portable_blocks_have_no_image_dependency` специально пропускает такие шаблоны.

## Код

```markdown
<div align="center">

![Header](https://capsule-render.vercel.app/api?type=waving&color=0:111827,100:7c3aed&height=180&section=header&text=ПРИВЕТ%20Я%20АЛЕКСЕЙ&fontSize=44&fontColor=FFFFFF&animation=fadeIn&desc=Собираю%20инструменты%20которыми%20сам%20пользуюсь&descAlignY=76&descSize=18)

[![Typing](https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=500&size=20&pause=1200&color=A78BFA&center=true&vCenter=true&width=560&lines=Python+%E2%80%A2+FastAPI+%E2%80%A2+Blender;Делаю+3D+в+PowerPoint+кодом;Люблю+когда+README+можно+потрогать)](https://github.com/overbaffe1/gitEdit)

<sub>Python · FastAPI · Blender · PowerPoint 3D · GitHub Actions</sub>

</div>

<div align="center">

![Footer](https://capsule-render.vercel.app/api?type=waving&color=0:111827,100:7c3aed&height=90&section=footer)

</div>
```

## Как менять

- `text=` — заголовок волны (кодируй пробел как `%20`)
- `desc=` — подзаголовок
- `color=0:111827,100:7c3aed` — градиент от тёмного к фиолетовому
- `lines=` в typing-svg — строки через `;`, пауза `pause=1200`

Источники: [capsule-render](https://github.com/kyechan99/capsule-render) · [readme-typing-svg](https://github.com/DenverCoder1/readme-typing-svg) — оба рендерят статический SVG, без JS в README.

## Превью

![Header](https://capsule-render.vercel.app/api?type=waving&color=0:111827,100:7c3aed&height=180&section=header&text=ПРИВЕТ%20Я%20АЛЕКСЕЙ&fontSize=44&fontColor=FFFFFF&animation=fadeIn&desc=Собираю%20инструменты%20которыми%20сам%20пользуюсь&descAlignY=76&descSize=18)

[![Typing](https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=500&size=20&pause=1200&color=A78BFA&center=true&vCenter=true&width=560&lines=Python+%E2%80%A2+FastAPI+%E2%80%A2+Blender;Делаю+3D+в+PowerPoint+кодом;Люблю+когда+README+можно+потрогать)](https://github.com/overbaffe1/gitEdit)

<sub>Python · FastAPI · Blender · PowerPoint 3D · GitHub Actions</sub>

![Footer](https://capsule-render.vercel.app/api?type=waving&color=0:111827,100:7c3aed&height=90&section=footer)
