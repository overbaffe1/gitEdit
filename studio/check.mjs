// Browser smoke test. Same CHROME_BIN / CI_CHROME options as capture.mjs.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { mkdtemp, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { setTimeout as delay } from 'node:timers/promises';
import puppeteer from 'puppeteer-core';
const root = dirname(dirname(fileURLToPath(import.meta.url))),
  url = process.argv[2];
if (!url || !process.env.CHROME_BIN)
  throw Error('CHROME_BIN=/path/to/chrome node check.mjs <studio-url> [--ship]');
const tmp = await mkdtemp(join(tmpdir(), 'facet-check-'));
const b = await puppeteer.launch({
  executablePath: process.env.CHROME_BIN,
  headless: true,
  acceptInsecureCerts: !!process.env.CI_CHROME,
  args: process.env.CI_CHROME
    ? [
        '--no-sandbox',
        '--no-zygote',
        '--use-gl=angle',
        '--use-angle=swiftshader',
        '--enable-unsafe-swiftshader',
      ]
    : [],
});
try {
  const p = await b.newPage(),
    errors = [],
    requests = [];
  p.on('pageerror', (e) => errors.push(e.message));
  p.on('request', (r) => requests.push([r.method(), r.url()]));
  const waitScene = (s) => p.waitForSelector(`#stage[data-state=ready][data-scene=${s}]`);
  const read = (id) => p.$eval('#' + id, (e) => e.textContent);
  const stage = async () => {
    await p.evaluate(() => new Promise((ok) => requestAnimationFrame(() => requestAnimationFrame(ok))));
    return createHash('sha256')
      .update(await (await p.$('#stage')).screenshot())
      .digest('hex');
  };
  const scrub = async (f) =>
    p.$eval(
      '#time',
      (e, v) => {
        e.value = v;
        e.dispatchEvent(new Event('input'));
      },
      f
    );
  const reduced = (value) =>
    p.emulateMediaFeatures([{ name: 'prefers-reduced-motion', value: value ? 'reduce' : 'no-preference' }]);
  await p.setViewport({ width: 1100, height: 860 });
  await reduced(false);
  await p.goto(url);
  await waitScene('crystal');
  await p.waitForFunction(() => document.querySelector('#time').valueAsNumber > 3);
  await p.click('#play');
  await scrub(140);
  const closed = await stage();
  await scrub(430);
  const opened = await stage();
  assert.notEqual(closed, opened);
  await delay(1050);
  assert.equal(await stage(), opened, 'paused pose drifted');
  await p.focus('canvas');
  await p.keyboard.press('ArrowLeft');
  assert.notEqual(await stage(), opened);
  await p.click('#home');
  assert.equal(await stage(), opened);
  await p.click('#wire');
  assert.notEqual(await stage(), opened);
  await p.click('#wire');
  await reduced(true);
  assert.ok(!requests.some(([, u]) => u.startsWith('https://api.github.com/')));
  if (process.argv.includes('--ship')) {
    await p.click('#ship');
    await waitScene('ship');
    assert.equal(await read('play'), 'Пуск');
    assert.match(await read('counter'), /0:04/);
    const rig = await stage();
    await scrub(380);
    assert.notEqual(await stage(), rig, 'authored clip is static');
    assert.equal(await p.$eval('#clip', (e) => e.selectedOptions[0].text), 'Паруса и волны');
  }
  const open = async (path) => {
    await (await p.$('#file')).uploadFile(path);
    await p.waitForFunction(
      (n) => document.querySelector('#plate-name').textContent === n,
      {},
      path.split('/').pop()
    );
  };
  await open(join(root, 'docs/malachite.glb'));
  assert.match(await read('clip'), /Размыкание/);
  await open(join(root, 'atlas/samples/crystal.stl'));
  assert.equal(await p.$eval('#paint-label', (e) => e.hidden), false);
  assert.equal(await p.$eval('#clip', (e) => e.value), '-1');
  const bare = await stage();
  await (await p.$('#paint')).uploadFile(join(root, 'assets/crystal-light.png'));
  await p.waitForFunction(() => document.querySelector('#status').textContent.includes('наложена'));
  assert.notEqual(await stage(), bare);
  const binary = Buffer.alloc(84 + 50);
  binary.writeUInt32LE(1, 80);
  [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0].forEach((v, i) => binary.writeFloatLE(v, 84 + 4 * i));
  const bin = join(tmp, 'triangle.stl');
  await writeFile(bin, binary);
  await open(bin);
  const bad = join(tmp, 'empty.glb');
  await writeFile(bad, 'not a GLB');
  await (await p.$('#file')).uploadFile(bad);
  await p.waitForFunction(() => document.querySelector('#status').textContent.startsWith('Не удалось'));
  assert.equal(await read('plate-name'), 'triangle.stl');
  // Disconnect, then open the actual ZIP's HTML via file://. The built-in model and textures still work.
  execFileSync('python3', ['-m', 'zipfile', '-e', join(root, 'assets/crystal-view.zip'), tmp]);
  await p.setViewport({ width: 320, height: 740, isMobile: true, hasTouch: true });
  await p.setOfflineMode(true);
  const from = requests.length;
  await p.goto(pathToFileURL(join(tmp, 'crystal.html')).href);
  await waitScene('crystal');
  assert.equal(await read('play'), 'Пуск');
  assert.ok(await p.evaluate(() => document.documentElement.scrollWidth === innerWidth));
  const rect = await p.$eval('canvas', (el) => {
    const r = el.getBoundingClientRect();
    return { x: r.left + r.width / 2, y: r.top + r.height / 2 };
  });
  const first = await stage();
  const cdp = await p.createCDPSession();
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [rect] });
  await cdp.send('Input.dispatchTouchEvent', {
    type: 'touchMove',
    touchPoints: [{ x: rect.x + 45, y: rect.y + 13 }],
  });
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
  assert.notEqual(await stage(), first);
  assert.ok(!requests.slice(from).some(([, u]) => /^https?:/.test(u)), 'offline HTML used network');
  assert.deepEqual(errors, []);
  assert.ok(requests.every(([method]) => method === 'GET'));
  const fail = await b.newPage();
  await fail.evaluateOnNewDocument(() => {
    const get = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function (type, ...args) {
      return type.includes('webgl') ? null : get.call(this, type, ...args);
    };
  });
  await fail.goto(url);
  await fail.waitForSelector('#stage[data-state=unavailable]');
  assert.ok(await fail.$eval('#poster', (im) => !im.hidden && im.complete && im.naturalWidth > 0));
  console.log(
    'OK: autoplay, pause/seek, camera, wireframe, local GLB, ASCII/binary STL, image map, invalid input, small-screen touch, offline ZIP, WebGL fallback' +
      (process.argv.includes('--ship') ? ', original 4 s ship rig.' : '.')
  );
} finally {
  await b.close();
  await rm(tmp, { recursive: true, force: true });
}
