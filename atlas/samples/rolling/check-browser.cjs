#!/usr/bin/env node
// Optional integration check: playwright-core + an installed Chromium.
// No dependencies are needed by the Python generator or the unit tests.
const { chromium } = require('playwright-core');
const path = require('node:path');
const fs = require('node:fs');
const os = require('node:os');
const { pathToFileURL } = require('node:url');
const root = path.resolve(__dirname, '../../..');
const specs = {
  tusi: [150, 75, 'inside'], deltoid: [150, 50, 'inside'],
  astroid: [150, 37.5, 'inside'], cardioid: [65, 65, 'outside'],
  cycloid: [65, 65, 'line'],
};
const url = (name) => pathToFileURL(path.join(root, 'assets/rolling', name)).href;

(async () => {
  if (!process.env.CHROMIUM_PATH) throw new Error('Set CHROMIUM_PATH to an installed Chromium executable');
  const browser = await chromium.launch({
    executablePath: process.env.CHROMIUM_PATH, headless: true,
    args: process.env.ROLLING_NO_SANDBOX === '1' ? ['--no-sandbox'] : [],
  });
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'rolling-check-'));
  try {
    const page = await browser.newPage({ viewport: { width: 1040, height: 540 }, reducedMotion: 'no-preference' });
    for (const [name, [R, r, kind]] of Object.entries(specs)) {
      await page.goto(url(`${name}.svg`));
      for (const fraction of [0, .125, .25, .55, .875]) {
        await page.evaluate((ms) => {
          for (const animation of document.getAnimations()) {
            animation.pause(); animation.currentTime = ms;
          }
        }, fraction * 14000);
        const observed = await page.evaluate(() => {
          const marker = document.querySelector('.spin circle:last-child');
          const point = new DOMPoint(+(marker.getAttribute('cx') || 0), +(marker.getAttribute('cy') || 0))
            .matrixTransform(marker.getCTM());
          return { x: point.x, y: point.y, animations: document.getAnimations().length };
        });
        const t = (kind === 'line' ? 0 : .7) + fraction * 2 * Math.PI;
        let x, y;
        if (kind === 'line') {
          x = 100 + r * (t - Math.sin(t)); y = 425 - r + r * Math.cos(t);
        } else {
          const distance = kind === 'inside' ? R - r : R + r;
          const angle = (kind === 'inside' ? -1 : 1) * distance / r * t;
          const sign = kind === 'inside' ? 1 : -1;
          x = 315 + distance * Math.cos(t) + sign * r * Math.cos(angle);
          y = 290 + distance * Math.sin(t) + sign * r * Math.sin(angle);
        }
        if (observed.animations !== 2 || Math.hypot(observed.x - x, observed.y - y) > .02) {
          throw new Error(`${name} at ${fraction}: ${JSON.stringify({ observed, x, y })}`);
        }
      }
      await page.emulateMedia({ reducedMotion: 'reduce' });
      if (await page.evaluate(() => document.getAnimations().length) !== 0) {
        throw new Error(`${name}: reduced-motion did not stop standalone animations`);
      }
      const html = path.join(temp, 'picture.html');
      fs.writeFileSync(html, `<!doctype html><picture><source media="(prefers-reduced-motion: reduce)" srcset="${url(`${name}-still.svg`)}"><img src="${url(`${name}.svg`)}" alt="Rolling mechanism"></picture>`);
      await page.goto(pathToFileURL(html).href);
      await page.locator('img').evaluate((img) => img.decode());
      if (await page.locator('img').evaluate((img) => img.currentSrc) !== url(`${name}-still.svg`)) {
        throw new Error(`${name}: picture did not select still`);
      }
      await page.emulateMedia({ reducedMotion: 'no-preference' });
      await page.locator('img').evaluate((img) => img.decode());
      if (await page.locator('img').evaluate((img) => img.currentSrc) !== url(`${name}.svg`)) {
        throw new Error(`${name}: picture did not select motion`);
      }
      console.log(`${name}: five phases, reduced-motion and picture source selection OK`);
    }
  } finally {
    await browser.close();
    fs.rmSync(temp, { recursive: true, force: true });
  }
})().catch((error) => { console.error(error); process.exitCode = 1; });
