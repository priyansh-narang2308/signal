// Renders screenshot-ready states of the SIGNAL prototype.
// Usage: node shoot.js [outDir] [--full]
const { chromium } = require("playwright");
const path = require("path");
const fs = require("fs");

const BASE = "http://127.0.0.1:8765/prototype/index.html";
const CHROME = process.env.HOME + "/Library/Caches/ms-playwright/chromium-1243/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing";
const out = path.resolve(process.argv[2] || path.join(__dirname, "../../screenshots"));
const full = process.argv.includes("--full");
fs.mkdirSync(out, { recursive: true }); fs.mkdirSync(path.join(__dirname, "..", "crops"), { recursive: true });

const SHOTS = [
  ["01-home", "research"],
  ["02-research", "run"],
  ["03-discovery", "discovery"],
  ["04-evidence", "evidence"],
  ["05-falsification", "falsification"],
  ["06-generalization", "generalization"],
  ["07-methodology", "methodology"],
];
// element crops used by the PDF
const CROPS = [
  ["crop-expectations", "discovery", "#expectWrap"],
  ["crop-timeline", "discovery", "#timeline"],
  ["crop-funnel", "run", ".run-grid"],
  ["crop-chain", "evidence", ".ev-grid"],
  ["crop-tests", "falsification", "#testsTable"],
  ["crop-disc-head", "discovery", ".disc-head"],
  ["crop-strength", "falsification", "#strengthRules"],
];

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME });
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
  const page = await ctx.newPage();
  const errors = [];
  page.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });
  page.on("pageerror", (e) => errors.push(String(e)));
  await page.goto(BASE + "?static=1#/research");
  await page.evaluate(() => window.SIGNAL.ready);
  for (const [name, route] of SHOTS) {
    await page.evaluate((r) => { location.hash = "#/" + r; }, route);
    await page.waitForTimeout(250);
    await page.screenshot({ path: path.join(out, name + ".png"), fullPage: full });
  }
  for (const [name, route, sel] of CROPS) {
    await page.evaluate((r) => { location.hash = "#/" + r; }, route);
    await page.waitForTimeout(200);
    await page.locator(sel).first().screenshot({ path: path.join(__dirname, "..", "crops", name + ".png") }).catch(async () => {
      
      await page.locator(sel).first().screenshot({ path: path.join(__dirname, "..", "crops", name + ".png") });
    });
  }
  console.log("errors:", errors.length ? errors : "none");
  await browser.close();
})();
