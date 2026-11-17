// Sample the real player through its ordinary transport, independent of GPU/wall-clock speed.
import puppeteer from 'puppeteer-core';
import { mkdir } from 'node:fs/promises';
import { join } from 'node:path';
const [url, dir] = process.argv.slice(2);
if (!url || !dir || !process.env.CHROME_BIN)
  throw Error('CHROME_BIN=/path/to/chrome node capture.mjs <studio-url> <empty-frames-directory>');
await mkdir(dir, { recursive: true });
const browser = await puppeteer.launch({
  executablePath: process.env.CHROME_BIN,
  headless: true,
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
  const page = await browser.newPage();
  await page.setViewport({ width: 1160, height: 820, deviceScaleFactor: 1 });
  await page.emulateMediaFeatures([{ name: 'prefers-reduced-motion', value: 'reduce' }]);
  await page.goto(url);
  await page.waitForSelector('#stage[data-state=ready][data-scene=crystal]');
  await page.addStyleTag({
    content:
      '.desk{display:block}.player{width:706px}.stage{width:704px;height:400px;aspect-ratio:auto}.intro{display:none}',
  });
  const stage = await page.$('#stage');
  await page.$eval('#home', (b) => b.click());
  for (let i = 0; i < 100; i++) {
    await page.$eval(
      '#time',
      async (r, i) => {
        r.value = (i * 10 + 60) % 1000;
        r.dispatchEvent(new Event('input'));
        await new Promise((ok) => requestAnimationFrame(() => requestAnimationFrame(ok)));
      },
      i
    );
    await stage.screenshot({ path: join(dir, `frame-${String(i).padStart(3, '0')}.png`) });
  }
} finally {
  await browser.close();
}
