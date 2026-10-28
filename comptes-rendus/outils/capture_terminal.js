// Capture d'écran "terminal" : exécute une commande et enregistre le résultat en PNG.
// Usage : node capture_terminal.js "commande" sortie.png
const { chromium } = require('playwright');
const { execSync } = require('child_process');
const [cmd, out] = process.argv.slice(2);
let res;
try { res = execSync(cmd, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }); }
catch (e) { res = (e.stdout || '') + (e.stderr || ''); }
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 900, height: 100 } });
  await p.setContent(`<body style="margin:0;background:#1e1e1e"><pre style="color:#ddd;font:14px monospace;padding:12px;margin:0;display:inline-block">${esc('$ ' + cmd + '\n' + res)}</pre></body>`);
  await p.locator('pre').screenshot({ path: out });
  await b.close();
})();
