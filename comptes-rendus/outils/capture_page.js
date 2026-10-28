// Capture d'une page Web avec son URL affichée au-dessus.
// Usage : node capture_page.js https://site sortie.png
const { chromium } = require('playwright');
const [url, out] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1100, height: 650 } });
  await p.goto(url + (url.includes('?') ? '&' : '?') + 't=' + Date.now(), { waitUntil: 'networkidle' });
  await p.evaluate(u => {
    const bar = document.createElement('div');
    bar.textContent = '🔒 ' + u;
    bar.style.cssText = 'position:fixed;top:0;left:0;right:0;z-index:99999;background:#e8e8e8;color:#222;font:14px Arial;padding:8px 12px;border-bottom:1px solid #bbb';
    document.body.style.paddingTop = '40px';
    document.body.appendChild(bar);
  }, url);
  await p.screenshot({ path: out });
  await b.close();
})();
