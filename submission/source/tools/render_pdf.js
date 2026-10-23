// Renders the Round 1 brief to A4 PDF and PNG previews; checks for page overflow.
// Usage: node render_pdf.js ["Team Name"]
const { chromium } = require("playwright");
const path = require("path");
const CHROME = process.env.HOME + "/Library/Caches/ms-playwright/chromium-1243/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing";
const team = process.argv[2] || "Team Name";
(async () => {
  const b = await chromium.launch({ executablePath: CHROME });
  const p = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2 });
  await p.goto("http://127.0.0.1:8765/source/pdf/round1.html?team=" + encodeURIComponent(team));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(300);
  const report = await p.evaluate(() => [...document.querySelectorAll(".page")].map((pg, i) => {
    const r = pg.getBoundingClientRect(); const foot = pg.querySelector(".foot").getBoundingClientRect();
    let maxBottom = 0; pg.querySelectorAll("*").forEach((el) => { if (!el.closest(".foot")) maxBottom = Math.max(maxBottom, el.getBoundingClientRect().bottom); });
    return { page: i + 1, height: Math.round(r.height), contentBottom: Math.round(maxBottom - r.top), footTop: Math.round(foot.top - r.top), overflow: maxBottom > foot.top + 0.5 };
  }));
  console.log(JSON.stringify(report));
  const pages = await p.$$(".page");
  for (let i = 0; i < pages.length; i++) await pages[i].screenshot({ path: path.join(__dirname, "..", "review", `pdf-p${i + 1}.png`) });
  await p.pdf({ path: path.join(__dirname, "..", "..", "pdf", team.replace(/[^A-Za-z0-9]/g, "") + "_TrackA_Round1.pdf"), format: "A4", printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 }, preferCSSPageSize: true });
  await b.close();
})();
