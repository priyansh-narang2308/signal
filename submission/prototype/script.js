/* SIGNAL — Autonomous Financial Research
   Prototype controller. Replays a simulated research run on a synthetic panel.
   All values are illustrative and are not findings about any real company.

   URL modes:
     ?static=1  render every state fully revealed (screenshots)
     ?video=1   expose window.SIGNAL control API (demo film)            */

(function () {
  "use strict";

  const params = new URLSearchParams(location.search);
  const STATIC = params.has("static");
  const VIDEO = params.has("video");
  if (STATIC) document.body.classList.add("static");
  if (VIDEO) document.body.classList.add("video");

  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const h = (tag, cls, html) => {
    const el = document.createElement(tag);
    if (cls) el.className = cls;
    if (html != null) el.innerHTML = html;
    return el;
  };

  /* =====================================================================
     DATA (synthetic panel)
     ===================================================================== */

  const STAGES = [
    { n: "01", t: "INGEST", d: "Exchange filings, call transcripts, regulator series, rating rationales", kind: "code", st: "248 filings" },
    { n: "02", t: "NORMALIZE", d: "XBRL and tables → typed facts; arithmetic reconciliation", kind: "code + llm", st: "1,904 facts" },
    { n: "03", t: "BUILD EXPECTATIONS", d: "Self, peer and narrative baselines on every driver", kind: "code + llm", st: "74 nodes" },
    { n: "04", t: "FIND BREACHES", d: "Robust surprise vs all three expectations; persistence", kind: "code", st: "143 breaches" },
    { n: "05", t: "TRIANGULATE", d: "Corroboration counted by independent source family", kind: "code", st: "11 corroborated" },
    { n: "06", t: "FALSIFY", d: "Nine pre-registered tests + testable consequences", kind: "code", st: "2 survived" },
    { n: "07", t: "RANK", d: "Gates, weighted geometric score, deterministic strength", kind: "code", st: "1 discovery" },
    { n: "08", t: "REPORT", d: "Digit-free prose bound to evidence IDs", kind: "llm", st: "41 links" },
  ];

  const LOG = [
    ["01 INGEST", ["248 filings · 5 years · NSE + BSE archives", "Transcripts for 21 calls · investor decks · annual reports", "8-peer panel loaded · refreshed to Q1 FY27", "RBI sector series · rating rationales from 3 agencies"]],
    ["02 NORMALIZE", ["1,904 typed facts · XBRL first, tables with page anchors", "NPA movement identity reconciles 21 / 21 quarters", "Regime split at merger quarter · post-merger series only"]],
    ["03 BUILD EXPECTATIONS", ["74 driver nodes · self and peer baselines", "Claim ledger · 412 typed claims from 21 calls"]],
    ["04 FIND BREACHES", ["143 candidate breaches across 38 nodes", "31 structurally valid (reconciled, ≥2Q, no discontinuity)"]],
    ["05 TRIANGULATE", ["Families · company · peers · regulator · rating · press", "11 candidates with ≥2 independent families"]],
    ["06 FALSIFY", ["Peer residualisation · 4 company-specific", "Registered 9 tests × 4 hypotheses before execution", "2 survive · every rejection logged with its reason"]],
    ["07 RANK", ["Gates + weighted geometric score", "Strength rule → H-01 STRONG · H-02 MODERATE"]],
    ["08 REPORT", ["Prose bound to 41 evidence IDs · 0 LLM-typed digits", "Dossier rendered · 8 / 8 required elements"]],
  ];

  const FUNNEL = [
    { c: 143, l: "Candidate breaches", g: "≥1 expectation breached on a driver node", w: 100, stage: 3 },
    { c: 31, l: "Structurally valid", g: "reconciled · ≥2Q persistence · no discontinuity", w: 46, stage: 3 },
    { c: 11, l: "Independently corroborated", g: "≥2 independent source families", w: 28, stage: 4 },
    { c: 4, l: "Peer-specific", g: "survive peer residualisation", w: 17, stage: 5 },
    { c: 2, l: "Survived falsification", g: "9 pre-registered tests", w: 12, stage: 5 },
    { c: 1, l: "High-confidence discovery", g: "highest score · strength rule: Strong", w: 8, stage: 6, final: true },
  ];

  const REJECTS = [
    { name: "Other income spike, Q3 FY26", why: "<b>One-off accounting event</b> — single-quarter treasury gain, not persistent", at: "at: Structural validity", stage: 3 },
    { name: "Cost-to-income drift", why: "<b>Insufficient independent evidence</b> — company documents only", at: "at: Corroboration", stage: 4 },
    { name: "NIM compression, 31 bps", why: "<b>Sector-wide effect</b> — 7 of 8 peers moved together through the rate cycle", at: "at: Peer residualisation", stage: 5 },
    { name: "CASA ratio decline", why: "<b>Management already disclosed</b> — stated in 6 consecutive calls", at: "at: Novelty check · AE6", stage: 5 },
    { name: "Advances growth jump, Q2 FY26", why: "<b>Accounting artefact</b> — portfolio acquisition reclassified into advances", at: "at: Falsification · AE3", stage: 5 },
    { name: "Provision coverage rise", why: "<b>Denominator effect</b> — GNPA written down; no new provisioning", at: "at: Falsification · AE4", stage: 5 },
    { name: "Card-segment GNPA rise", why: "<b>Runner-up · Moderate</b> — partly sector-wide (AE1 partial)", at: "at: Ranking", stage: 6, kept: true },
    { name: "Write-off-led NPA improvement", why: "<b>Discovery H-01 · Strong</b> — survived 8 of 9 tests", at: "at: Ranking", stage: 6, kept: true },
  ];

  const QUARTERS = ["Q1 FY25", "Q2 FY25", "Q3 FY25", "Q4 FY25", "Q1 FY26", "Q2 FY26", "Q3 FY26", "Q4 FY26", "Q1 FY27"];
  const SLIP = [1.38, 1.41, 1.40, 1.40, 1.55, 1.73, 1.92, 2.06, 2.20];
  const GNPA = [2.40, 2.36, 2.31, 2.12, 1.98, 1.86, 1.76, 1.68, 1.62];
  const PEER_MED = [1.41, 1.41, 1.42, 1.42, 1.42, 1.42, 1.43, 1.44, 1.44];
  const PEERS = [
    [1.18, 1.19, 1.20, 1.19, 1.21, 1.20, 1.20, 1.19, 1.18],
    [1.28, 1.30, 1.29, 1.31, 1.30, 1.31, 1.32, 1.31, 1.32],
    [1.35, 1.36, 1.35, 1.37, 1.36, 1.37, 1.38, 1.38, 1.37],
    [1.40, 1.39, 1.41, 1.40, 1.41, 1.40, 1.42, 1.43, 1.43],
    [1.43, 1.44, 1.43, 1.44, 1.43, 1.44, 1.44, 1.45, 1.45],
    [1.52, 1.53, 1.52, 1.54, 1.55, 1.56, 1.58, 1.59, 1.59],
    [1.62, 1.63, 1.64, 1.66, 1.70, 1.76, 1.82, 1.86, 1.90],
    [1.70, 1.72, 1.73, 1.74, 1.80, 1.86, 1.92, 1.95, 1.98],
  ];
  const WO_SHARE = [null, null, null, 62, 65, 70, 73, 74, 77];
  const NARR = ["“Growth with quality”", "", "", "“Collections strong”", "“Strong collection efficiency”", "“Slippages within comfort band”", "“Recoveries and collections”", "“Best-in-class collections”", "“Calibrating unsecured growth”"];
  const EVENTS = [null, null, null, ["E1", "Rate cycle turns"], null, ["E2", "Sector rule update"], null, null, ["P1", "First press coverage"]];

  const SIX = [
    ["What changed", "Fresh slippages began rising in <b>Q1 FY26</b> and rose for <b>5 consecutive quarters</b> (1.40% → 2.20%)."],
    ["Why it is unusual", "The headline GNPA ratio improved at the same time — through <b>write-offs (71%)</b>, not recoveries or upgrades (29%)."],
    ["What management said", "“Strong collection efficiency” cited in <b>5 of 6 calls</b>; “calibrating unsecured growth” first appears only in Q1 FY27."],
    ["What the numbers show", "Write-offs <b>₹11,748 cr</b> of ₹16,546 cr total reductions; NPA movement reconciles in 6 of 6 quarters."],
    ["How peers behaved", "Peer-median slippage <b>flat (+0.02 pp)</b>; 6 of 8 peers flat or falling; peer-median write-off share 46%."],
    ["What survived", "<b>8 of 9</b> falsification tests. Denominator effect partially explains the headline (24 of 69 bps)."],
  ];

  const CONTRACT = ["Discovery", "Why it matters", "Evidence", "Timeline", "Numbers", "Counterargument", "Falsification condition", "Evidence strength"];

  const WHY = [
    "The headline asset-quality improvement is mostly resolution by write-off, not cure: NPAs left the book without cash coming back.",
    "New stress is rising underneath: fresh slippage is up 0.80 pp in five quarters while the peer median is flat — the forward credit-cost signal.",
    "Management's attribution diverges from the data: collections are credited in 5 of 6 calls, yet recoveries and upgrades are only 29% of reductions.",
    "It is company-specific, not a cycle: the subject sits outside the peer interquartile range in 4 of the last 4 quarters.",
    "It was visible in filings four quarters before the first press coverage.",
  ];

  const NUMBERS = [
    ["Gross NPA ratio, Q3 FY25 → Q1 FY27", "2.31% → 1.62%", "—", "Results · notes", null],
    ["Write-offs ÷ all NPA reductions, 6Q", "71.0%", "46%", "Derived · NPA movement", "wo"],
    ["Fresh slippages, 6Q", "₹14,953 cr", "—", "Results · notes · p. 37", "fs"],
    ["Fresh-slippage ratio, Q1 FY27 (ann.)", "2.20%", "1.44%", "Derived ratio", "slip"],
    ["Peer-median slippage, Q1 FY27", "1.44%", "—", "8 peer filings", "peer"],
    ["Lagged GNPA ratio (advances t−4)", "1.86%", "—", "Denominator test · AE4", "lag"],
    ["Calls attributing improvement to collections", "5 / 6", "—", "Claim ledger", "claims"],
  ];

  const FAMILIES = [
    { fn: "COMPANY", fd: "Quarterly results and notes, investor decks, earnings-call transcripts, annual report.", fc: "Tier 1–2 · 14 documents" },
    { fn: "REGULATOR", fd: "RBI sector slippage and write-off series; dated sector events E1 and E2.", fc: "Tier 1R · 3 series" },
    { fn: "PEER COMPANIES", fd: "Same-quarter NPA movement disclosures of 8 same-archetype banks.", fc: "Tier 1 · 48 filings" },
    { fn: "JOURNALISM", fd: "Used only to date first coverage (Q1 FY27). Not counted as corroboration.", fc: "Tier 4 · dating only", excluded: true },
  ];

  const EV = {
    fs: {
      v: "+₹14,953 cr", k: "Fresh slippages — six quarters", tag: "NPA MOVEMENT IDENTITY",
      formula: [["", "Opening GNPA · 11,550"], ["+", "Fresh slippages · 14,953"], ["−", "Upgrades · 1,892"], ["−", "Recoveries · 2,906"], ["−", "Write-offs · 11,748"]],
      res: "= Closing GNPA · 9,957",
      check: "11,550 + 14,953 − 1,892 − 2,906 − 11,748 = 9,957 ✓ · reconciles in each of 6 quarters",
      doc: "Quarterly results — notes to accounts", dm: "Company · Tier 1 · cross-checked against annual report FY26<br>Q4 FY25 – Q1 FY27 · 6 filings · archived copy SHA-256 recorded",
      page: "fs",
    },
    wo: {
      v: "71.0%", k: "Write-offs ÷ all NPA reductions", tag: "DERIVED RATIO",
      formula: [["", "Write-offs · 11,748"], ["÷", "( Upgrades 1,892 + Recoveries 2,906 + Write-offs 11,748 )"]],
      res: "= 11,748 ÷ 16,546 = 71.0%",
      check: "Inputs reconciled through the NPA movement identity · peer median 46% on the same definition",
      doc: "Quarterly results — notes to accounts", dm: "Company · Tier 1 · 6 filings<br>Peer comparison: 8 peer filings, same quarters",
      page: "wo",
    },
    slip: {
      v: "2.20%", k: "Fresh-slippage ratio, annualised, Q1 FY27", tag: "DERIVED RATIO",
      formula: [["", "Fresh slippages Q1 FY27 · 3,266"], ["× 4", "annualised"], ["÷", "Opening standard advances · 5,93,800"]],
      res: "= 2.20%",
      check: "Slippage input = passage value · advances = balance-sheet value of prior quarter ✓",
      doc: "Quarterly results — notes and balance sheet", dm: "Company · Tier 1 · Q1 FY27<br>Advances cross-checked against XBRL",
      page: "fs",
    },
    peer: {
      v: "1.44%", k: "Peer-median slippage, Q1 FY27", tag: "PEER EXPECTATION",
      formula: [["", "median( slippage ratio of 8 same-archetype banks )"], ["", "IQR 1.32 – 1.59"]],
      res: "= 1.44%",
      check: "Each peer ratio built with the same identity and the same definition · 8 / 8 reconciled",
      doc: "Peer quarterly results — notes to accounts", dm: "Peer company family · Tier 1 · 8 filings, Q1 FY27<br>Peers labelled A–H in this prototype",
      page: "peer",
    },
    lag: {
      v: "1.86%", k: "Lagged GNPA ratio (advances t−4)", tag: "DENOMINATOR TEST · AE4",
      formula: [["", "GNPA Q1 FY27 · 9,957"], ["÷", "Gross advances Q1 FY26 (t−4)"]],
      res: "= 1.86% (vs reported 1.62%)",
      check: "Improvement on lagged basis 45 bps vs 69 bps reported · 24 bps is growth dilution",
      doc: "Quarterly results — balance sheet", dm: "Company · Tier 1 · Q1 FY26 and Q1 FY27",
      page: "fs",
    },
    claims: {
      v: "5 / 6", k: "Calls attributing improvement to collections", tag: "CLAIM LEDGER",
      formula: [["", "count( calls where attribution = collections )"], ["÷", "calls in window · 6"]],
      res: "= 5 / 6",
      check: "Each claim typed with speaker, date and passage ID · write-offs never named as the driver",
      doc: "Earnings-call transcripts", dm: "Company · Tier 2 · Q4 FY25 – Q1 FY27 · 6 transcripts",
      page: "claims",
    },
  };
  const EV_ORDER = ["fs", "wo", "slip", "peer", "lag", "claims"];

  const PAGES = {
    fs: `<div class="ph"><span>QUARTERLY RESULTS · NOTES TO ACCOUNTS · Q1 FY27</span><span>p. 37 · illustrative</span></div>
      <h4>Movement of gross non-performing assets (₹ crore)</h4>
      <table>
        <tr><td>Opening balance</td><td class="r">9,977</td></tr>
        <tr class="hl"><td>Additions — fresh slippages</td><td class="r">3,266</td></tr>
        <tr><td>Reductions — upgradations</td><td class="r">(292)</td></tr>
        <tr><td>Reductions — recoveries</td><td class="r">(481)</td></tr>
        <tr><td>Reductions — write-offs</td><td class="r">(2,513)</td></tr>
        <tr><td><b>Closing balance</b></td><td class="r"><b>9,957</b></td></tr>
      </table>
      <p>Gross NPAs as a percentage of gross advances stood at 1.62% as at the end of the quarter.</p>
      <span class="synth">SYNTHETIC RENDER</span>`,
    wo: `<div class="ph"><span>QUARTERLY RESULTS · NOTES TO ACCOUNTS · Q1 FY27</span><span>p. 37 · illustrative</span></div>
      <h4>Movement of gross non-performing assets (₹ crore)</h4>
      <table>
        <tr><td>Opening balance</td><td class="r">9,977</td></tr>
        <tr><td>Additions — fresh slippages</td><td class="r">3,266</td></tr>
        <tr><td>Reductions — upgradations</td><td class="r">(292)</td></tr>
        <tr><td>Reductions — recoveries</td><td class="r">(481)</td></tr>
        <tr class="hl"><td>Reductions — write-offs</td><td class="r">(2,513)</td></tr>
        <tr><td><b>Closing balance</b></td><td class="r"><b>9,957</b></td></tr>
      </table>
      <span class="synth">SYNTHETIC RENDER</span>`,
    peer: `<div class="ph"><span>PEER PANEL · SAME-QUARTER DISCLOSURES · Q1 FY27</span><span>8 filings · illustrative</span></div>
      <h4>Fresh-slippage ratio, annualised (%)</h4>
      <table>
        <tr><td>Peer A</td><td class="r">1.18</td></tr><tr><td>Peer B</td><td class="r">1.32</td></tr>
        <tr><td>Peer C</td><td class="r">1.37</td></tr><tr class="hl"><td>Median of 8</td><td class="r">1.44</td></tr>
        <tr><td>Peer F</td><td class="r">1.59</td></tr><tr><td>Peer H</td><td class="r">1.98</td></tr>
      </table>
      <span class="synth">SYNTHETIC RENDER</span>`,
    claims: `<div class="ph"><span>EARNINGS CALL TRANSCRIPT · Q2 FY26</span><span>p. 6 · illustrative</span></div>
      <h4>Management commentary — asset quality</h4>
      <p>“…the improvement in our gross NPA ratio this quarter reflects <b style="background:#e9e9eb;outline:1.5px solid #0a0a0b;padding:0 2px">strong collection efficiency</b> across our retail and commercial portfolios, and slippages remain within our comfort band…”</p>
      <p style="color:#8e8e94">Claim C-0412 · speaker: CFO · attribution → collections · metric → GNPA ratio · direction ↓</p>
      <span class="synth">SYNTHETIC RENDER</span>`,
  };

  const DOCS = [
    ["Quarterly results — notes to accounts", "Company", "Company", "1", "Q4 FY25 – Q1 FY27", "6 filings"],
    ["Integrated filing (XBRL) — financial results", "Exchange", "Company", "1", "Q4 FY25 – Q1 FY27", "6 files"],
    ["Annual report FY26 — notes 18, 19", "Company", "Company", "1", "FY26", "p. 214–219"],
    ["Earnings-call transcripts", "Company", "Company", "2", "Q4 FY25 – Q1 FY27", "6 calls"],
    ["Peer quarterly results (Banks A–H)", "Peers", "Peer company", "1", "Q1 FY25 – Q1 FY27", "72 filings"],
    ["RBI sector slippage and write-off series", "RBI", "Regulator", "1R", "FY25 – FY27", "3 series"],
    ["Financial press — first coverage", "Press", "Journalism", "4", "Q1 FY27", "dating only"],
  ];

  const TESTS = [
    ["AE1", "Sector-wide effect / peer-specificity", "“Slippages rose everywhere this cycle.”", "Company vs 8-peer distribution each quarter; share of peers co-moving", "6 of 8 peers flat or falling · residual +0.76 pp", "pass"],
    ["AE2", "Regulatory / macro shock", "“A dated sector event caused it.”", "Difference vs peers, ±1 quarter around events E1 and E2", "peer Δ +0.02 pp vs subject Δ +0.80 pp", "pass"],
    ["AE3", "Accounting artefact", "“A write-off policy change, merger or reclassification.”", "Disclosure-diff on notes and policies; discontinuity flags", "no policy change · post-merger regime only", "pass"],
    ["AE4", "Denominator effect", "“Fast loan growth diluted the ratio.”", "Lagged GNPA ratio (t−4, t−8); same-quarter YoY", "explains 24 of 69 bps · share and slippage unaffected", "partial"],
    ["AE5", "One-off event / chosen window", "“One quarter, or a cherry-picked window.”", "Specification curve over 24 window choices", "holds in 22 of 24 specifications", "pass"],
    ["AE6", "Management already disclosed", "“This is already known.”", "Claim ledger + Tier-4 coverage search", "never attributed to write-offs · no coverage before Q1 FY27", "pass"],
    ["AE7", "Data integrity", "“The numbers are wrong.”", "Identity reconciliation; second-document cross-check", "reconciles 6 / 6 quarters · results = annual report", "pass"],
    ["AE8", "Alternative mechanism", "“Something else explains both series.”", "Corollary predictions on data not used to build the hypothesis", "2 / 2 corollaries consistent", "pass"],
    ["AE9", "Counter-evidence search", "“Independent sources contradict it.”", "12 bounded queries · tier allow-list · LLM classifies, cites passages", "0 contradicting facts from independent families", "pass"],
  ];

  const COROLLARIES = [
    ["If resolution is write-off-led, credit cost should rise with a 1–2 quarter lag.", "credit cost +38 bps over 4Q", "consistent"],
    ["If new stress is in unsecured retail, card and personal-loan GNPA should rise before the total.", "card-segment GNPA +0.9 pp from Q2 FY26", "consistent"],
  ];

  const FALS_COND = "Reconsider if the fresh-slippage ratio falls back below 1.60% for two consecutive quarters and write-offs fall below 40% of GNPA reductions.";

  const RULES = [
    { g: "STRONG", active: true, crit: [["✓", "≥3 independent source families"], ["✓", "Persistence ≥4 quarters"], ["✓", "Outside peer IQR in ≥3 of last 4 quarters"], ["✓", "No test failed · at most one partial"], ["✓", "Key numbers confirmed in 2 documents"]] },
    { g: "MODERATE", crit: [["·", "≥2 independent source families"], ["·", "Persistence ≥3 quarters"], ["·", "Exactly one test partially explains it"]] },
    { g: "WEAK", crit: [["·", "Anything that passes the gates but not Moderate"], ["·", "Reported only if nothing better exists, clearly labelled"]] },
  ];

  const METHOD = [
    { g: "DATA", steps: [["01", "Structured financial data", "XBRL first; PDF tables with page anchors; every extraction checked against accounting identities; bitemporal facts.", "CODE"], ["02", "Driver decomposition", "Archetype identity trees — NPA flows, RoA tree, funding mix — so candidates are economically meaningful.", "CODE"]] },
    { g: "EXPECT", steps: [["03", "Peer residualisation", "Same-archetype peers, same calendar quarters. Sector and macro effects are removed before anything is called unusual.", "CODE"], ["04", "Management claim ledger", "Attributions and guidance, timestamped and mapped to metrics; promises scored against later actuals.", "LLM READS · CODE SCORES"]] },
    { g: "BREACH", steps: [["05", "Candidate generation", "Robust surprise against self, peers and narrative, with persistence. Every candidate is kept and logged — none hand-picked.", "CODE"]] },
    { g: "PROVE", steps: [["06", "Independent evidence", "Corroboration counted by source family; syndicated copies collapsed; Tier 4–5 never sole evidence.", "CODE"], ["07", "Falsification battery", "Nine pre-registered alternative-explanation tests plus testable consequences.", "CODE · BOUNDED SEARCH"]] },
    { g: "REPORT", steps: [["08", "Discovery ranking", "Gates, weighted geometric score and a deterministic strength rule.", "CODE"], ["09", "Provenance rendering", "Every number → formula → inputs → document → page → passage. Prose is digit-free.", "CODE · LLM WRITES"]] },
  ];

  const ARCH = [
    ["Banks", "NPA flows, lagged ratios, deposit franchise, RWA density, priority-sector and divergence notes", 3, "HDFC Bank · ICICI Bank · SBI · Kotak Mahindra Bank · Axis Bank"],
    ["NBFCs & HFCs", "AUM on- and off-book, borrowing mix, Stage 1/2/3 migration, co-lending, rating-rationale mirror", 3, "Bajaj Finance · Shriram Finance · Jio Financial Services"],
    ["Insurers", "APE mix, VNB margin, persistency, bancassurance concentration, embedded-value walk", 2, "HDFC Life · SBI Life"],
    ["Market infra & holdcos", "Generic identities: segment revenue, turnover data, regulatory calendar, look-through to subsidiaries", 1, "BSE · Bajaj Finserv"],
  ];

  const SETS = [
    ["Practice", "Generic code may be tuned here", ["HDFC Bank", "Axis Bank", "Bajaj Finance"], true],
    ["Held-out NIFTY 50", "Never used for development", ["ICICI Bank", "SBI", "Kotak Mahindra Bank", "Shriram Finance", "HDFC Life", "SBI Life", "Bajaj Finserv", "Jio Financial Services", "BSE"]],
    ["Non-NIFTY · tie-break simulation", "Plus as-of backtests using only documents known at a past date", ["Federal Bank", "IDFC First Bank", "AU Small Finance Bank", "Bank of Baroda", "IndusInd Bank", "Cholamandalam Finance", "LIC Housing Finance", "ICICI Prudential Life"]],
  ];

  const BENCH = [
    ["Evidence correctness", "Hand-audit 30 numbers per report against the source passage", "headline 100% · overall ≥98%"],
    ["Calculation correctness", "Unit tests on every formula; reconciliation pass rate", "100% tests · ≥90% reconciled"],
    ["Source quality", "Families per discovery; share of evidence by tier", "≥2 families always · ≥3 in half"],
    ["Temporal correctness", "Change-point and first-visible quarter checked by hand", "≥90%"],
    ["Discovery novelty", "Blind A/B vs a strong deep-research baseline, rated by finance students", "win rate ≥70%"],
    ["Falsification quality", "Planted adversarial cases correctly demoted", "≥90%"],
    ["Reproducibility", "Same snapshot run 5×", "identical top discovery 5 / 5"],
    ["Generalisation", "Held-out + non-NIFTY: ≥Moderate discovery with correct numbers", "≥70% of runs"],
    ["Latency", "End-to-end live run, p50 / p95", "≤6.5 / ≤9 min"],
  ];

  /* =====================================================================
     RENDER — static sections
     ===================================================================== */

  function renderHome() {
    const list = $("#stageList");
    list.innerHTML = "";
    STAGES.forEach((s) => {
      const row = h("div", "stage-row");
      row.innerHTML = `<span class="n">${s.n}</span><div><div class="t">${s.t}</div><div class="d">${s.d}</div></div><span class="kind ${s.kind !== "code" ? "llm" : ""}">${s.kind}</span>`;
      list.appendChild(row);
    });
  }

  function renderRunShell() {
    const rail = $("#rail");
    rail.innerHTML = "";
    STAGES.forEach((s) => {
      const el = h("div", "rail-step");
      el.innerHTML = `<div class="n">${s.n}</div><div class="t">${s.t === "BUILD EXPECTATIONS" ? "BUILD<br>EXPECTATIONS" : s.t === "FIND BREACHES" ? "FIND BREACHES" : s.t}</div><div class="st">—</div><div class="bar"><i></i></div>`;
      rail.appendChild(el);
    });
    const funnel = $("#funnel");
    funnel.innerHTML = "";
    FUNNEL.forEach((f) => {
      const row = h("div", "funnel-row" + (f.final ? " final" : ""));
      row.innerHTML = `<div class="count">${f.c}</div><div class="barwrap"><div class="fbar"><i></i></div><div class="flabel"><span>${f.l}</span><span class="gate">${f.g}</span></div></div>`;
      funnel.appendChild(row);
    });
    const rej = $("#rejects");
    rej.innerHTML = "";
    REJECTS.forEach((r) => {
      const el = h("div", "rej");
      el.innerHTML = `<div class="top"><span class="name">${r.name}</span><span class="verdict ${r.kept ? "kept" : ""}">${r.kept ? "Retained" : "Rejected"}</span></div><div class="why">${r.why}</div><div class="at">${r.at}</div>`;
      rej.appendChild(el);
    });
    $("#log").innerHTML = "";
    $("#runClock").textContent = "SIM · 00:00";
    $("#runDone").classList.remove("on");
  }

  function sentenceHTML() {
    return `Over six quarters the subject bank's gross NPA ratio fell from 2.31% to 1.62% — but <span class="ref" data-ev="wo">71% of all NPA reductions were write-offs</span>, while its <span class="ref" data-ev="slip">fresh-slippage ratio rose from 1.40% to 2.20%</span> as the <span class="ref" data-ev="peer">peer median stayed flat at 1.44%</span>. Management credited <span class="ref" data-ev="claims">collections in 5 of 6 earnings calls</span>.`;
  }

  /* ---------- SVG charts ---------- */
  const W = 400, H = 210, PL = 34, PR = 8, PT = 14, PB = 26;
  const xAt = (i) => PL + (i * (W - PL - PR)) / 8;
  function yScale(min, max) { return (v) => PT + ((max - v) * (H - PT - PB)) / (max - min); }
  function axes(y, ticks, fmt) {
    let s = "";
    ticks.forEach((t) => {
      s += `<line x1="${PL}" x2="${W - PR}" y1="${y(t)}" y2="${y(t)}" stroke="#ececee" stroke-width="1"/>`;
      s += `<text x="${PL - 6}" y="${y(t) + 3}" text-anchor="end" font-family="JetBrains Mono" font-size="8.5" fill="#8e8e94">${fmt(t)}</text>`;
    });
    [0, 2, 4, 6, 8].forEach((i) => {
      s += `<text x="${xAt(i)}" y="${H - 8}" text-anchor="middle" font-family="JetBrains Mono" font-size="8.5" fill="#8e8e94">${QUARTERS[i]}</text>`;
    });
    return s;
  }
  const path = (vals, y) => vals.map((v, i) => (v == null ? "" : `${i ? "L" : "M"}${xAt(i).toFixed(1)},${y(v).toFixed(1)}`)).join(" ");
  const dots = (vals, y) => vals.map((v, i) => `<circle cx="${xAt(i)}" cy="${y(v)}" r="2.8" fill="#fff" stroke="#0a0a0b" stroke-width="1.5"/>`).join("");
  const windowRect = (y0, y1) => `<rect x="${xAt(4) - 10}" y="${y0}" width="${W - PR - xAt(4) + 10}" height="${y1 - y0}" fill="#f4f4f5"/>`;

  function chartSelf() {
    const y = yScale(1.0, 2.3);
    return `<svg viewBox="0 0 ${W} ${H}">${windowRect(PT, H - PB)}${axes(y, [1.0, 1.4, 1.8, 2.2], (t) => t.toFixed(1) + "%")}
      <rect x="${PL}" y="${y(1.47)}" width="${W - PL - PR}" height="${y(1.33) - y(1.47)}" fill="#e6e6e8" fill-opacity=".6" stroke="#8e8e94" stroke-dasharray="3 2" stroke-width=".8"/>
      <text x="${PL + 6}" y="${y(1.47) - 5}" font-family="JetBrains Mono" font-size="8.5" fill="#5f5f65">expected band · own history</text>
      <line x1="${xAt(4)}" x2="${xAt(4)}" y1="${PT - 6}" y2="${H - PB}" stroke="#0a0a0b" stroke-dasharray="2 2"/>
      <text x="${xAt(4) + 4}" y="${PT + 2}" font-family="JetBrains Mono" font-size="8.5" fill="#0a0a0b">change point</text>
      <path d="${path(SLIP, y)}" fill="none" stroke="#0a0a0b" stroke-width="2"/>${dots(SLIP, y)}
      <text x="${xAt(8) - 4}" y="${y(2.2) - 8}" text-anchor="end" font-family="JetBrains Mono" font-size="9" font-weight="600" fill="#0a0a0b">2.20%</text></svg>`;
  }
  function chartPeer() {
    const y = yScale(1.0, 2.3);
    let p = PEERS.map((s) => `<path d="${path(s, y)}" fill="none" stroke="#c4c4c9" stroke-width="1"/>`).join("");
    return `<svg viewBox="0 0 ${W} ${H}">${windowRect(PT, H - PB)}${axes(y, [1.0, 1.4, 1.8, 2.2], (t) => t.toFixed(1) + "%")}${p}
      <path d="${path(PEER_MED, y)}" fill="none" stroke="#2e2e31" stroke-width="1.4" stroke-dasharray="5 3"/>
      <path d="${path(SLIP, y)}" fill="none" stroke="#0a0a0b" stroke-width="2"/>${dots(SLIP, y)}
      <text x="${xAt(8) - 4}" y="${y(2.2) - 8}" text-anchor="end" font-family="JetBrains Mono" font-size="9" font-weight="600" fill="#0a0a0b">subject 2.20%</text>
      <rect x="${PL + 4}" y="${y(1.12) - 8}" width="168" height="12" fill="#fff"/>
      <text x="${PL + 8}" y="${y(1.12)}" font-family="JetBrains Mono" font-size="8.5" fill="#2e2e31">- - peer median — peers ━ subject</text></svg>`;
  }
  function chartNarr() {
    const y = yScale(0, 100);
    let bars = "";
    WO_SHARE.forEach((v, i) => {
      if (v == null) return;
      bars += `<rect x="${xAt(i) - 9}" y="${y(v)}" width="18" height="${y(0) - y(v)}" fill="#0a0a0b"/>`;
      bars += `<text x="${xAt(i)}" y="${y(v) - 5}" text-anchor="middle" font-family="JetBrains Mono" font-size="8.5" fill="#2e2e31">${v}</text>`;
    });
    return `<svg viewBox="0 0 ${W} ${H}"><rect x="${xAt(3) - 16}" y="${PT}" width="${W - PR - xAt(3) + 16}" height="${H - PT - PB}" fill="#f4f4f5"/>${axes(y, [0, 25, 50, 75, 100], (t) => t + "%")}
      <line x1="${PL}" x2="${W - PR}" y1="${y(50)}" y2="${y(50)}" stroke="#0a0a0b" stroke-dasharray="5 3" stroke-width="1.2"/>
      <line x1="${PL}" x2="${W - PR}" y1="${y(46)}" y2="${y(46)}" stroke="#8e8e94" stroke-dasharray="2 2" stroke-width="1"/>
      <rect x="${PL + 2}" y="${y(50) - 14}" width="108" height="11" fill="#fff"/>
      <text x="${PL + 6}" y="${y(50) - 5}" font-family="JetBrains Mono" font-size="8.5" fill="#0a0a0b">collections-led: &lt;50%</text>${bars}</svg>`;
  }

  function renderDiscovery() {
    $("#discSentence").innerHTML = sentenceHTML();
    $("#contract").innerHTML = CONTRACT.map((c) => `<span>${c}</span>`).join("");
    $("#six").innerHTML = SIX.map(([q, a]) => `<div><div class="q">${q}</div><div class="a">${a}</div></div>`).join("");

    const ex = [
      ["SELF", "expectation 01", "What does its own history predict?", chartSelf(), [["Expected slippage (pre-window band)", "1.33–1.47%"], ["Observed, Q1 FY27", "2.20%"], ["Breach", "+0.80 pp · 5Q outside band", true]]],
      ["PEER", "expectation 02", "What do comparable banks show, same quarters?", chartPeer(), [["Peer median (IQR)", "1.44% (1.32–1.59)"], ["Subject, Q1 FY27", "2.20%"], ["Breach", "+0.76 pp · 6 of 8 peers flat", true]]],
      ["NARRATIVE", "expectation 03", "What did management say drives the numbers?", chartNarr(), [["Claimed driver (5 of 6 calls)", "collections"], ["Implied write-off share", "< 50%"], ["Breach · observed share", "71% (peer median 46%)", true]]],
    ];
    $("#expectGrid").innerHTML = ex.map(([n, idx, q, svg, rows]) =>
      `<div class="expect"><div class="xh"><span class="xname">${n}</span><span class="xidx">${idx}</span></div><div class="xq">${q}</div>${svg}
       <div class="xrows">${rows.map(([k, v, b]) => `<div class="xrow ${b ? "breach" : ""}"><span class="k">${k}</span><span class="v">${v}</span></div>`).join("")}</div></div>`).join("");

    $("#whyList").innerHTML = WHY.map((w, i) => `<li><span class="i">0${i + 1}</span><span>${w}</span></li>`).join("");

    $("#numbersTable").innerHTML = `<tr><th>Metric</th><th class="r">Value</th><th class="r">Peer median</th><th>Source</th></tr>` +
      NUMBERS.map(([m, v, p, s, ev]) => `<tr><td>${m}</td><td class="r">${ev ? `<span class="linknum" data-ev="${ev}">${v}</span>` : `<span class="mono">${v}</span>`}</td><td class="r mono">${p}</td><td><span class="srcref">${s}</span></td></tr>`).join("");

    renderTimeline();
    $("#falsCond1").textContent = FALS_COND;
    $("#families").innerHTML = FAMILIES.map((f) => `<div class="family ${f.excluded ? "excluded" : ""}"><div class="fn">${f.fn}</div><div class="fd">${f.fd}</div><div class="fc">${f.fc}</div></div>`).join("");
  }

  function renderTimeline() {
    const win = (i) => (i >= 4 ? " win" : "");
    let g = `<div class="tl-grid"><div class="tl-cell tl-head">Lane</div>`;
    QUARTERS.forEach((q, i) => (g += `<div class="tl-cell tl-head${i >= 4 ? " win" : ""}">${q}</div>`));
    g += `<div class="tl-cell tl-lane">Company numbers<small>slippage · GNPA ratio</small></div>`;
    QUARTERS.forEach((q, i) => {
      const up = i >= 4;
      g += `<div class="tl-cell${win(i)}"><div class="tl-val ${up ? "up" : ""}">${SLIP[i].toFixed(2)}%${up ? " ↑" : ""}</div><div class="tl-val" style="color:#8e8e94">${GNPA[i].toFixed(2)}%${i >= 3 ? " ↓" : ""}</div></div>`;
    });
    g += `<div class="tl-cell tl-lane">Management narrative<small>claim ledger · calls</small></div>`;
    NARR.forEach((n, i) => (g += `<div class="tl-cell${win(i)}"><div class="tl-mark"><span class="q"${i === 8 ? ' style="font-weight:600;color:#0a0a0b"' : ""}>${n}</span></div></div>`));
    g += `<div class="tl-cell tl-lane">Peer movement<small>8-bank median slippage</small></div>`;
    PEER_MED.forEach((v, i) => (g += `<div class="tl-cell${win(i)}"><div class="tl-val">${v.toFixed(2)}%</div>${i === 8 ? '<div class="tl-mark" style="color:#8e8e94">2 of 8 rising</div>' : ""}</div>`));
    g += `<div class="tl-cell tl-lane">External events<small>illustrative</small></div>`;
    EVENTS.forEach((e, i) => (g += `<div class="tl-cell${win(i)}">${e ? `<span class="tl-ev">${e[0]}</span><div class="tl-mark">${e[1]}</div>` : ""}</div>`));
    g += `</div>`;

    const c = (i) => ((i + 0.5) / 9) * 100;
    const pts = [[3, "EVENT", "E1 · Q4 FY25", ""], [4, "NUMBERS<br>CHANGE", "Q1 FY26", ""], [5, "SYSTEM DETECTS<br>BREACH", "Q2 FY26 results", "sys"], [8, "PUBLIC<br>COVERAGE", "Q1 FY27", ""]];
    let track = `<div class="gap-line" style="left:${c(3)}%;right:${100 - c(8)}%"></div>`;
    pts.forEach(([i, t, s, cls]) => (track += `<div class="gap-pt ${cls}" style="left:${c(i)}%"><div class="gt">${t}</div><div class="gm"></div><div class="gs">${s}</div></div>`));
    track += `<div class="gap-bracket" style="left:${c(4)}%;right:${100 - c(8)}%"></div>`;
    track += `<div class="gap-label" style="left:${(c(4) + c(8)) / 2}%">VISIBILITY GAP · visible in filings 4 quarters before first coverage</div>`;
    g += `<div class="gap-row"><div class="tl-lane">Visibility gap<small>knowledge time</small></div><div class="gap-track">${track}</div></div>`;
    $("#timeline").innerHTML = g;
  }

  function renderFalsification() {
    $("#squares").innerHTML = TESTS.map((t) => `<i class="${t[5] === "partial" ? "partial" : ""}"></i>`).join("");
    $("#testsTable").innerHTML = `<tr><th>ID</th><th>Test</th><th>Alternative explanation</th><th>Procedure (code)</th><th>Result</th><th style="text-align:right">Verdict</th></tr>` +
      TESTS.map(([id, n, a, p, r, v]) => `<tr><td class="id">${id}</td><td class="name">${n}</td><td class="alt">${a}</td><td class="proc">${p}</td><td class="res">${r}</td><td class="verdict"><span class="pill ${v}">${v.toUpperCase()}</span></td></tr>`).join("");
    $("#corollaries").innerHTML = COROLLARIES.map(([p, r, v]) => `<div class="co"><span class="p">${p}</span><span class="r">${r}</span><span style="text-align:right"><span class="pill pass">${v.toUpperCase()}</span></span></div>`).join("");
    $("#falsCond2").textContent = FALS_COND;
    $("#strengthRules").innerHTML = RULES.map((r) => `<div class="srule ${r.active ? "active" : ""}"><div class="sh"><span class="g">${r.g}</span><span class="label" style="color:inherit">${r.active ? "assigned" : ""}</span></div>${r.crit.map(([c, t]) => `<div class="crit"><span class="c">${c}</span><span>${t}</span></div>`).join("")}</div>`).join("");
  }

  let currentEv = "fs";
  function renderEvidence(id) {
    currentEv = EV[id] ? id : "fs";
    $("#evList").innerHTML = EV_ORDER.map((k) => `<button class="ev-item ${k === currentEv ? "active" : ""}" data-ev="${k}"><div class="v">${EV[k].v}</div><div class="k">${EV[k].k}</div><div class="tag">${EV[k].tag}</div></button>`).join("");
    const e = EV[currentEv];
    const formula = e.formula.map(([op, t]) => `<div><span class="op">${op}</span>${t}</div>`).join("") + `<div><span class="op"></span><span class="res">${e.res}</span></div>`;
    $("#chain").innerHTML = `
      <div class="chain-step"><div class="lab" data-n="01">Derived value</div><div><div class="derived-v">${e.v}</div><div class="derived-k">${e.k}</div></div></div>
      <div class="chain-step"><div class="lab" data-n="02">Formula</div><div class="formula">${formula}</div></div>
      <div class="chain-step"><div class="lab" data-n="03">Input check</div><div><span class="recon">${e.check}</span><div class="srcref" style="margin-top:8px">Inputs are typed facts with value, unit, period, basis and passage ID. Unreconciled facts can never be a headline number.</div></div></div>
      <div class="chain-step"><div class="lab" data-n="04">Source document</div><div class="doc"><div><div class="dn">${e.doc}</div><div class="dm">${e.dm}</div></div><span class="btn-ghost" style="padding:5px 10px;font-size:10px">Open source ↗</span></div></div>
      <div class="chain-step" style="border-bottom:0"><div class="lab" data-n="05">Page &amp; passage</div><div><div class="page-mock">${PAGES[e.page]}</div><div class="page-cap">Highlighted passage resolves the input value · synthetic page render</div></div></div>`;
  }

  function renderDocs() {
    $("#docsTable").innerHTML = `<tr><th>Document</th><th>Publisher</th><th>Family</th><th>Tier</th><th>Period</th><th class="r">Scope</th></tr>` +
      DOCS.map((d) => `<tr><td>${d[0]}</td><td>${d[1]}</td><td>${d[2]}</td><td class="mono">${d[3]}</td><td class="mono">${d[4]}</td><td class="r mono">${d[5]}</td></tr>`).join("");
  }

  function renderMethod() {
    $("#methodFlow").innerHTML = METHOD.map((m, i) => `<div class="mgroup"><div class="gh"><span class="g">${m.g}</span><span class="arrow" style="${i < METHOD.length - 1 ? "" : "visibility:hidden"}">→</span></div>${m.steps.map(([n, t, d, k]) => `<div class="mstep"><div class="mn">${n}</div><div class="mt">${t}</div><div class="md">${d}</div><div class="mk">${k}</div></div>`).join("")}</div>`).join("");
    $("#arch").innerHTML = ARCH.map(([n, d, depth, m]) => `<div><div class="an">${n}</div><div class="ad">${d}</div><div class="depth">${[0, 1, 2].map((i) => `<i class="${i < depth ? "" : "off"}"></i>`).join("")}</div><div class="label" style="margin-top:6px">Planned depth</div><div class="members">${m}</div></div>`).join("");
    $("#sets").innerHTML = SETS.map(([t, d, cos, fill]) => `<div><div class="eyebrow dark">${t}</div><div class="muted small mt8">${d}</div><div class="co-list">${cos.map((c) => `<span class="${fill ? "fill" : ""}">${c}</span>`).join("")}</div></div>`).join("");
    $("#benchTable").innerHTML = `<tr><th>Dimension</th><th>Method</th><th>Target</th><th class="r">Status</th></tr>` +
      BENCH.map(([d, m, t]) => `<tr><td style="font-weight:600">${d}</td><td class="muted">${m}</td><td class="mono">${t}</td><td class="r"><span class="chip">Planned</span></td></tr>`).join("");
  }

  /* =====================================================================
     RUN — simulated research run (~14 s)
     ===================================================================== */

  const STAGE_MS = 1700;
  const SIM_TOTAL = 5 * 60 + 48; // displayed simulated run time 05:48
  let runState = "idle"; // idle | running | done
  let timers = [];
  let clockTimer = null;

  function clearTimers() { timers.forEach(clearTimeout); timers = []; if (clockTimer) clearInterval(clockTimer); clockTimer = null; }
  const fmtClock = (s) => `SIM · ${String(Math.floor(s / 60)).padStart(2, "0")}:${String(Math.floor(s % 60)).padStart(2, "0")}`;

  function applyStage(i, full) {
    const steps = $$(".rail-step");
    steps.forEach((el, k) => {
      el.classList.toggle("done", k < i || (full && k === i));
      el.classList.toggle("active", k === i && !full);
      if (k < i || (full && k === i)) { el.querySelector(".st").textContent = STAGES[k].st; el.querySelector(".bar i").style.width = "100%"; }
    });
    const log = $("#log");
    const [head, lines] = LOG[i];
    log.appendChild(h("div", "log-line stage", `<span class="s">▸</span><span>${head}</span>`));
    lines.forEach((l, j) => {
      const add = () => { log.appendChild(h("div", "log-line" + (j === lines.length - 1 ? " hl" : ""), `<span class="s">·</span><span>${l}</span>`)); log.scrollTop = log.scrollHeight; };
      if (full) add(); else timers.push(setTimeout(add, 180 + j * ((STAGE_MS - 300) / lines.length)));
    });
    log.scrollTop = log.scrollHeight;
    if (!full) {
      const bar = steps[i].querySelector(".bar i");
      bar.style.transition = `width ${STAGE_MS}ms linear`;
      requestAnimationFrame(() => (bar.style.width = "100%"));
      steps[i].querySelector(".st").textContent = "running…";
      timers.push(setTimeout(() => { steps[i].querySelector(".st").textContent = STAGES[i].st; }, STAGE_MS - 100));
    }
    $$(".funnel-row").forEach((row, k) => {
      if (FUNNEL[k].stage <= i) { const delay = full ? 0 : (k - FUNNEL.findIndex((f) => f.stage === FUNNEL[k].stage)) * 500 + 300;
        const on = () => { row.classList.add("on"); row.querySelector(".fbar i").style.width = FUNNEL[k].w + "%"; };
        if (full || row.classList.contains("on")) on(); else timers.push(setTimeout(on, delay)); }
    });
    $$(".rej").forEach((el, k) => {
      if (REJECTS[k].stage <= i && !el.classList.contains("on")) {
        const same = REJECTS.filter((r, j) => r.stage === REJECTS[k].stage && j < k).length;
        if (full) el.classList.add("on"); else timers.push(setTimeout(() => el.classList.add("on"), 250 + same * 380));
      }
    });
  }

  function finishRun() {
    clearTimers();
    renderRunShell();
    STAGES.forEach((_, i) => applyStage(i, true));
    $$(".rail-step").forEach((el) => { el.classList.add("done"); el.classList.remove("active"); });
    $("#runClock").textContent = fmtClock(SIM_TOTAL);
    $("#runDone").classList.add("on");
    runState = "done";
  }

  function startRun() {
    clearTimers();
    renderRunShell();
    runState = "running";
    const t0 = performance.now();
    const total = STAGE_MS * STAGES.length;
    clockTimer = setInterval(() => {
      const f = Math.min(1, (performance.now() - t0) / total);
      $("#runClock").textContent = fmtClock(f * SIM_TOTAL);
    }, 100);
    STAGES.forEach((_, i) => timers.push(setTimeout(() => applyStage(i, false), i * STAGE_MS)));
    timers.push(setTimeout(() => {
      if (clockTimer) clearInterval(clockTimer);
      $$(".rail-step").forEach((el) => { el.classList.add("done"); el.classList.remove("active"); });
      $("#runClock").textContent = fmtClock(SIM_TOTAL);
      $("#runDone").classList.add("on");
      runState = "done";
    }, total + 200));
  }

  /* =====================================================================
     ROUTER
     ===================================================================== */

  const ROUTES = {
    research: { view: "view-research", nav: "research", ctx: false },
    run: { view: "view-run", nav: "research", ctx: true },
    discovery: { view: "view-discovery", nav: "discoveries", ctx: true },
    falsification: { view: "view-falsification", nav: "discoveries", ctx: true },
    evidence: { view: "view-evidence", nav: "evidence", ctx: true },
    methodology: { view: "view-methodology", nav: "methodology", ctx: false },
    generalization: { view: "view-generalization", nav: "methodology", ctx: false },
  };

  function route() {
    const raw = (location.hash || "#/research").replace(/^#\/?/, "");
    const [name, arg] = raw.split("/");
    const r = ROUTES[name] || ROUTES.research;
    $$(".view").forEach((v) => v.classList.toggle("active", v.id === r.view));
    $$(".nav a").forEach((a) => a.classList.toggle("active", a.dataset.nav === r.nav));
    $("#contextbar").classList.toggle("hidden", !r.ctx);
    if (name === "run" && runState === "idle") finishRun();
    if (name === "evidence") renderEvidence(arg || currentEv);
    if (!VIDEO) window.scrollTo(0, 0);
  }

  function go(name) {
    if (location.hash === "#/" + name) route(); else location.hash = "#/" + name;
  }

  /* =====================================================================
     EVENTS
     ===================================================================== */

  function bind() {
    $("#runBtn").addEventListener("click", () => {
      const b = $("#runBtn");
      b.classList.add("pressed");
      setTimeout(() => b.classList.remove("pressed"), 160);
      runState = "running";
      go("run");
      startRun();
    });
    document.addEventListener("click", (e) => {
      const ref = e.target.closest("[data-ev]");
      if (!ref) return;
      const id = ref.dataset.ev;
      if (ref.classList.contains("ev-item")) { renderEvidence(id); history.replaceState(null, "", "#/evidence/" + id); return; }
      location.hash = "#/evidence/" + id;
    });
    window.addEventListener("hashchange", route);
  }

  /* =====================================================================
     INIT
     ===================================================================== */

  renderHome();
  renderRunShell();
  renderDiscovery();
  renderFalsification();
  renderEvidence("fs");
  renderDocs();
  renderMethod();
  bind();
  if (STATIC) finishRun();
  route();

  if (VIDEO) {
    window.SIGNAL = {
      go,
      run: () => { go("run"); startRun(); },
      finish: finishRun,
      evidence: (id) => { location.hash = "#/evidence/" + id; },
      state: () => runState,
    };
  }
})();
