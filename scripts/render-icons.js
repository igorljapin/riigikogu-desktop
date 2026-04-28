#!/usr/bin/env node
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');
const fs = require('fs');

const ROOT = path.resolve(__dirname, '..');
const SVG_PATH = path.join(ROOT, 'icon.svg');

const SIZES = [
  { name: 'icon-512.png', px: 512 },
  { name: 'icon-192.png', px: 192 },
  { name: 'icon-32.png',  px: 32  },
  { name: 'icon-16.png',  px: 16  },
];

async function render() {
  const svgB64 = Buffer.from(fs.readFileSync(SVG_PATH)).toString('base64');
  const dataUrl = `data:image/svg+xml;base64,${svgB64}`;
  const browser = await chromium.launch();

  for (const { name, px } of SIZES) {
    const page = await browser.newPage();
    await page.setViewportSize({ width: px, height: px });
    const html = `<!DOCTYPE html><html><body style="margin:0;padding:0">
      <img src="${dataUrl}" width="${px}" height="${px}" style="display:block">
    </body></html>`;
    await page.setContent(html);
    await page.waitForTimeout(200);
    const out = path.join(ROOT, name);
    await page.screenshot({ path: out, clip: { x: 0, y: 0, width: px, height: px } });
    await page.close();
    console.log(`Wrote ${out} (${px}x${px})`);
  }

  await browser.close();
}

render().catch(err => { console.error(err); process.exit(1); });
