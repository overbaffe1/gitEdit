import { CanvasTexture, SRGBColorSpace } from 'three';
import { Theatre, glb, stl, release } from './scene.js';

const $ = (id) => document.getElementById(id),
  reduced = matchMedia('(prefers-reduced-motion: reduce)');
const SHIP =
  'https://api.github.com/repos/overbaffe1/MyWorkAiBrain/git/blobs/44eca970cdabbb5c8d2fcf34a7ea16c50d54eda7';
const MAX = 32 * 1024 * 1024;
let theatre,
  active = '',
  run = 0,
  controller,
  wire = false,
  shipBytes;
const labels = {
  crystal: ['01', 'Малахитовая капсула', 'МИНЕРАЛ · МАЛАХИТ / ЛАТУНЬ'],
  ship: ['02', 'Парусник Кантильона', 'CANTILLON · 23 КОСТИ'],
};
const fmt = (t) => `${Math.floor(t / 60)}:${String(Math.floor(t % 60)).padStart(2, '0')}`;
function transport(t, d) {
  $('time').value = String(Math.round((t / d) * 1000));
  $('time').setAttribute('aria-valuetext', `${t.toFixed(1)} из ${d.toFixed(1)} с`);
  $('counter').value = fmt(t) + ' / ' + fmt(d);
}
function play(on) {
  theatre.play(on);
  $('play').textContent = on ? 'Пауза' : 'Пуск';
  $('play').setAttribute('aria-label', on ? 'Приостановить движение' : 'Воспроизвести движение');
}
function message(text) {
  $('status').textContent = text;
}
function paintWire(on) {
  wire = on;
  theatre.wire(on);
  $('wire').setAttribute('aria-pressed', String(on));
}
function unavailable(reason) {
  $('poster').hidden = false;
  $('stage').dataset.state = 'unavailable';
  message(reason);
  for (const id of ['play', 'time', 'clip', 'file', 'wire', 'home', 'crystal', 'ship', 'paint'])
    $(id).disabled = true;
}
function bytes64(s) {
  return Uint8Array.from(atob(s), (c) => c.charCodeAt(0)).buffer;
}
async function bytes(url, options) {
  const response = await fetch(url, options);
  if (!response.ok) throw Error('HTTP ' + response.status);
  return response.arrayBuffer();
}

async function show(key, file) {
  if (!theatre || $('stage').dataset.state === 'unavailable') return;
  const ticket = ++run;
  controller?.abort();
  controller = new AbortController();
  const signal = controller.signal;
  const local = key === 'local',
    ext = local ? file.name.split('.').pop().toLowerCase() : 'glb';
  message(key === 'ship' ? 'Загружаю оригинальный GLB из MyWorkAiBrain…' : 'Открываю модель…');
  let model;
  try {
    let data;
    if (local) {
      if (!['glb', 'stl'].includes(ext)) throw Error('Выбери STL или упакованный GLB.');
      if (file.size > MAX) throw Error('Максимум 32 МиБ.');
      data = await file.arrayBuffer();
    } else if (key === 'ship') {
      data =
        shipBytes || (await bytes(SHIP, { signal, headers: { Accept: 'application/vnd.github.raw+json' } }));
    } else {
      const baked = $('embedded-glb');
      data = baked ? bytes64(baked.textContent) : await bytes('./malachite.glb', { signal });
    }
    if (ticket !== run) return;
    model = ext === 'stl' ? stl(data) : await glb(data);
    if (ticket !== run) {
      release(model.object);
      return;
    }
    if (key === 'ship') shipBytes = data;
    model.capsule = key === 'crystal';
    theatre.mount(model);
    active = key;
    const [num, name, kicker] = labels[key] || ['03', file.name, 'ЛОКАЛЬНЫЙ ФАЙЛ · ' + ext.toUpperCase()];
    $('number').textContent = num;
    $('badge').textContent = ext.toUpperCase();
    $('plate-kicker').textContent = kicker;
    $('plate-name').textContent = name;
    $('poster').hidden = true;
    $('stage').dataset.scene = key;
    $('stage').dataset.state = 'ready';
    for (const id of ['play', 'time', 'clip', 'wire', 'home', 'file']) $(id).disabled = false;
    $('paint-label').hidden = !model.paint;
    const clips = model.clips.map(
      (a, i) =>
        new Option(key === 'ship' && i === 0 ? 'Паруса и волны' : a.name || `Клип ${i + 1}`, String(i))
    );
    $('clip').replaceChildren(...clips, new Option('Поворотный стол', '-1'));
    $('clip').selectedIndex = 0;
    for (const id of ['crystal', 'ship']) $(id).setAttribute('aria-pressed', String(id === key));
    theatre.clip(Number($('clip').value));
    paintWire(false);
    play(!reduced.matches);
    message(
      key === 'ship'
        ? 'Оригинальный клип: паруса, волны и крылья чайки.'
        : key === 'crystal'
          ? 'Створки расходятся и открывают две латунные орбиты.'
          : ext === 'stl'
            ? 'STL: добавлен поворотный стол. Можно наложить свою текстуру.'
            : `Модель открыта. Встроенных клипов: ${model.clips.length}.`
    );
  } catch (err) {
    if (ticket !== run || signal.aborted) return;
    if (model && theatre.model !== model) release(model.object);
    const text =
      key === 'ship'
        ? 'Парусник не загрузился. Для него нужен доступ к GitHub; можно открыть скачанный ship.glb.'
        : `Не удалось открыть модель. ${err.message || ''}`;
    if (!active && key === 'ship') {
      await show('crystal');
      if (active === 'crystal') message(text + ' Показана капсула.');
    } else {
      if (!active) $('poster').hidden = false;
      message(text);
    }
  }
}

async function texture(file) {
  const model = theatre.model,
    ticket = run;
  let bitmap;
  try {
    if (!model?.paint) return;
    if (file.size > 16 * 1024 * 1024) throw Error('Изображение должно быть меньше 16 МиБ.');
    bitmap = await createImageBitmap(file);
    if (ticket !== run || theatre.model !== model) return;
    const k = Math.min(1, 2048 / Math.max(bitmap.width, bitmap.height)),
      c = document.createElement('canvas');
    c.width = Math.max(1, Math.round(bitmap.width * k));
    c.height = Math.max(1, Math.round(bitmap.height * k));
    c.getContext('2d').drawImage(bitmap, 0, 0, c.width, c.height);
    const tex = new CanvasTexture(c);
    tex.colorSpace = SRGBColorSpace;
    model.paint.map?.dispose();
    model.paint.map = tex;
    model.paint.color.set(0xffffff);
    model.paint.vertexColors = false;
    model.paint.needsUpdate = true;
    theatre.request();
    message('Текстура наложена на STL: ' + file.name);
  } catch (e) {
    if (ticket === run) message('Текстура не открылась. ' + e.message);
  } finally {
    bitmap?.close();
  }
}

try {
  theatre = new Theatre($('mount'), transport);
  $('file').disabled = false;
  $('mount').firstElementChild.addEventListener('webglcontextlost', () => {
    ++run;
    controller?.abort();
    play(false);
    unavailable('Графический контекст потерян. Остался постер; чтобы вернуть 3D, открой страницу заново.');
  });
  for (const key of ['crystal', 'ship']) $(key).onclick = () => show(key);
  $('file').onchange = (e) => {
    const f = e.target.files[0];
    e.target.value = '';
    if (f) show('local', f);
  };
  $('paint').onchange = (e) => {
    const f = e.target.files[0];
    e.target.value = '';
    if (f) texture(f);
  };
  $('play').onclick = () => play(!theatre.playing);
  $('home').onclick = () => theatre.home();
  $('wire').onclick = () => paintWire(!wire);
  $('time').oninput = () => {
    play(false);
    theatre.seek((theatre.duration * Number($('time').value)) / 1000);
  };
  $('clip').onchange = () => theatre.clip(Number($('clip').value));
  reduced.addEventListener('change', (e) => {
    if (e.matches) play(false);
  });
  show(new URLSearchParams(location.search).get('scene') === 'ship' ? 'ship' : 'crystal');
} catch {
  unavailable('Здесь недоступен WebGL 2. Показан кадр сцены; кинопетлю без WebGL можно посмотреть в README.');
}
