// HTML -> PDF mit Playwright/Chromium: node pdf.js
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + path.join(__dirname, 'silben-arbeitsblaetter.html'), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: path.join(__dirname, 'silben-arbeitsblaetter.pdf'), format: 'A4', printBackground: true, preferCSSPageSize: true });
  if (process.argv[2]) { // Vorschau-PNGs
    await p.setViewportSize({ width: 794, height: 1123 });
    const n = await p.locator('.page').count();
    for (let i = 0; i < n; i++) await p.locator('.page').nth(i).screenshot({ path: `${process.argv[2]}/s${i + 1}.png` });
  }
  await b.close();
})();
