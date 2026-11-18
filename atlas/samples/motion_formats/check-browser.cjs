#!/usr/bin/env node
// Optional: NODE_PATH points to playwright-core; CHROMIUM_PATH to installed Chrome.
const { chromium } = require('playwright-core');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const root = path.resolve(__dirname, '../../..');
const url = (name) => pathToFileURL(path.join(root, 'assets/motion-formats', name)).href;

(async () => {
  if (!process.env.CHROMIUM_PATH) throw new Error('Set CHROMIUM_PATH to an installed Chromium executable');
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH, headless: true,
    args: process.env.MOTION_NO_SANDBOX === '1' ? ['--no-sandbox'] : [] });
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'motion-format-check-'));
  try {
    const names = ['cube.gif', 'cube-apng.png', 'cube.webp'];
    const pictures = names.map((name, i) => `<picture><source media="(prefers-reduced-motion: reduce)" srcset="${url(i === 0 ? 'poster-matte.png' : 'poster.png')}"><img id="img${i}" src="${url(name)}" width="256" height="192" alt="One authored cube loop"></picture>`).join('');
    const adaptive = `<picture><source media="(prefers-reduced-motion: reduce)" srcset="${url('poster.png')}"><source type="image/webp" srcset="${url('cube.webp')}"><img id="adaptive" src="${url('cube.gif')}" width="256" height="192" alt="Adaptive loop"></picture>`;
    const html = path.join(temp, 'index.html');
    fs.writeFileSync(html, '<!doctype html><style>body{margin:0;background:#f4efe2}img{vertical-align:top}</style>' + pictures + adaptive);
    const page = await browser.newPage({ viewport: { width: 1040, height: 400 }, reducedMotion: 'no-preference' });
    await page.goto(pathToFileURL(html).href);
    await page.locator('img').evaluateAll((images) => Promise.all(images.map((image) => image.decode())));
    for (let i = 0; i < names.length; i++) {
      const image = page.locator(`#img${i}`);
      const before = await image.screenshot();
      await page.waitForTimeout(270);
      const after = await image.screenshot();
      if (before.equals(after)) throw new Error(`${names[i]} did not visibly animate`);
      console.log(`${names[i]}: decoded and visibly animated in Chromium`);
    }
    if (await page.locator('#adaptive').evaluate((image) => image.currentSrc) !== url('cube.webp')) {
      throw new Error('Adaptive picture did not select WebP');
    }
    await page.screenshot({ path: path.join(temp, 'motion.png') });
    await page.emulateMedia({ reducedMotion: 'reduce' });
    await page.locator('img').evaluateAll((images) => Promise.all(images.map((image) => image.decode())));
    for (const id of ['img0', 'img1', 'img2', 'adaptive']) {
      const image = page.locator(`#${id}`);
      const expected = id === 'img0' ? 'poster-matte.png' : 'poster.png';
      if (await image.evaluate((im) => im.currentSrc) !== url(expected)) throw new Error(`${id} did not choose still`);
      const before = await image.screenshot();
      await page.waitForTimeout(200);
      if (!before.equals(await image.screenshot())) throw new Error(`${id}: still image changed`);
    }
    console.log('Reduced-motion: all four pictures selected PNG posters and remained still');
    console.log('This tests local Chromium, not GitHub cache/mobile client behavior.');
  } finally {
    await browser.close();
    fs.rmSync(temp, { recursive: true, force: true });
  }
})().catch((error) => { console.error(error); process.exitCode = 1; });
