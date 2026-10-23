# Handoff: SIGNAL, finals Q&A assistant

> Paste this whole file into ChatGPT at the start of the session, before the finals.

---

## 0. Your job (instructions for ChatGPT)

You are helping **Team The Blacklisted** answer judges' questions live during the finals of **"Finding the Next Signal"** (ATMOS 2026, BITS Pilani Hyderabad, Track A). Our project is **SIGNAL**. I will type or paste each judge's question. You reply with an answer **I can read out loud straight away.**

**How to answer:**

- Put the direct answer in the first sentence. Then give 2–4 short supporting sentences. Keep it under about 30 seconds of speech (roughly 70 words) unless I ask for more.
- Write plain spoken English: no headings, no bullet lists, no markdown.
- Use our own terms: _three expectations (self, peer, narrative)_, _breach_, _six gates_, _the nine alternative-explanation tests (AE1 to AE9)_, _source families_, _provenance_, _archetype_, _visibility gap_.
- If a question is hostile, agree with the fair part first, then explain the design choice. Never get defensive.
- **Never invent results, accuracy figures, benchmark numbers or live-run outcomes.** Section 9 states exactly what is built. Benchmark numbers in our materials are **targets, not measured results.** The example discovery is **synthetic.** If a question needs a fact that isn't in this file, say so and suggest an honest answer.
- Never give an investment recommendation. The brief forbids it.
- If I type "longer", expand to about 60 seconds. If I type "shorter", give one sentence.

---

## 1. The brief (what the organisers asked for)

**Challenge:** Build an **autonomous financial research agent** that, given **any NIFTY 50 company in the chosen track**, investigates public information **on its own** and uncovers a **non-obvious, evidence-backed financial insight.** No dataset is provided; the public internet is the research environment. There must be **no company-specific tuning.**

**What it should be:** not a chatbot, a news summariser, a report generator or a database wrapper. It should be an investigator that discovers, connects, calculates, reasons, challenges and proves.

**What the system must do:** Discover → Connect → Calculate → Reason → Challenge (look for contradictory evidence and alternative explanations) → Prove (an auditable evidence trail).

**Required output, 8 elements per discovery:**

1. The Discovery: one clear sentence
2. Why It Matters: 3–5 bullets
3. Evidence: multiple independent sources, with links
4. Timeline: when the change emerged and how it developed
5. Numbers: only the calculations needed
6. Counterargument: the strongest alternative explanation
7. Falsification Condition: what future evidence would change the conclusion
8. Evidence Strength: Strong, Moderate or Weak, with the reasoning shown

The output can be a report or an interactive dashboard. Every major claim must be traceable to documents, figures, dates and passages, and must not rest on a single source.

**Track A, Banking, NBFCs & Financial Services.** Example angles: is loan-book growth moving against asset quality; hidden dependency on banks, co-lending partners or funders; how the funding mix or customer profile changed over five years.

**Finals (25 Oct 2026, online):** 10-minute presentation and live demo, then 15 minutes of Q&A. Judges pick a NIFTY 50 company from the track on the spot. In a tie-break they may use **any listed company in the sector, including outside the NIFTY 50.**

**Judging criteria:** discovery quality, evidence quality, novelty (would a dashboard or summariser miss it?), temporal reasoning, cross-source reasoning, falsifiability, explainability, robustness, and generality and autonomy. **Not judged:** which model, how many agents, how visually complex the UI is, report length, or investment recommendations.

**Rules:** public data only; no hard-coding for specific companies; every claim must link to a source; unsupported or invented claims are penalised; no investment recommendation.

---

## 2. SIGNAL in one paragraph

SIGNAL is an autonomous financial research system built on one idea: **computed, not retrieved.** A non-obvious finding is, by definition, not written down anywhere, so retrieval can only return what someone has already said. SIGNAL builds **three independent expectations** for a company: its **own history** (self), **same-archetype peers in the same quarter** (peer), and **what management said** (narrative). It investigates where the numbers **persistently break** those expectations. A breach becomes a discovery only after it passes **six gates**, including **nine pre-registered falsification tests** that run as code over data. **Every number** in the output resolves to formula → inputs → document → page → highlighted passage. **The LLM never types a number.**

Tagline: _Find the breach. Trace the evidence. Try to break the hypothesis._ Short form: **Expect · Breach · Survive.**

---

## 3. The mechanism

### Three expectations

| Expectation              | Source                                                                                                      | What it catches                              |
| ------------------------ | ----------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| **Self** (temporal)      | The company's own history, broken into drivers (e.g. GNPA into slippages, upgrades, recoveries, write-offs) | Breaks from its own trajectory               |
| **Peer** (cross-section) | 6–10 same-archetype peers in the same quarter, ranked by size, including non-NIFTY                          | Company-specific moves vs sector-wide noise  |
| **Narrative** (claims)   | Timestamped guidance, earnings-call attributions, MD&A, held in a "claim and promise ledger"                | Gaps between what was said and what happened |

Expected vs observed = **breach**, which is a **candidate, not a discovery.**

### Six gates (every one must pass)

G1 **Reconciled**: numbers satisfy accounting identities. G2 **Corroborated**: at least 2 independent source families. G3 **Specific**: not explained by peers. G4 **Survives tests**: the 9 alternative explanations. G5 **Predicts**: a testable consequence it wasn't built from. G6 **Persistent**: holds across time windows.

(STRATEGY.md also has a formal version: G1 reconciled, G2 ≥2 families, G3 ≥2 quarters persistence, G4 AE3 and AE7 not failed.)

### Nine alternative-explanation tests (pre-registered, deterministic code)

| ID  | Alternative                        | Test                                                                                                                                               |
| --- | ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| AE1 | Sector-wide effect                 | Company vs peer distribution each quarter. If ≥70% of peers co-move and the residual is insignificant, it fails and is relabelled a "sector story" |
| AE2 | Regulatory / macro shock           | Difference-in-differences vs peers within ±1 quarter of dated sector events (e.g. RBI risk-weight change, Nov 2023)                                |
| AE3 | Accounting / definitional artefact | Disclosure-diff on notes and policies; merger and restatement flags. A critical gate                                                               |
| AE4 | Denominator / base effect          | Lagged ratios (GNPA ÷ advances at t−4 and t−8), same-quarter YoY, seasonality                                                                      |
| AE5 | One-off / cherry-picked window     | Specification curve over all reasonable windows. Below 70% holding = fail; 70–90% = partial                                                        |
| AE6 | Already known / disclosed          | Claim ledger plus news-coverage search. If known, it gets a novelty penalty (demoted)                                                              |
| AE7 | Data error                         | Re-derive from a second document or family; reconciliation status                                                                                  |
| AE8 | Other mechanism                    | Corollary predictions tested on data not used to form the hypothesis                                                                               |
| AE9 | Counter-evidence                   | Bounded search (≤12 queries, tier allow-list); the LLM classifies passages as support, contradict or irrelevant                                    |

The **strongest surviving alternative becomes the reported counterargument.** Tests are registered before results are computed, so the goalposts can't move.

### Falsification condition

It's generated from the primary driver. **Threshold:** back inside the peer IQR or its own pre-change range. **Duration:** 2 consecutive quarters. Plus a **mechanism-kill clause** and a **sector clause** ("or if the peer median moves to the company's level").

### Evidence-strength rule (deterministic, not an LLM opinion)

- **Strong:** ≥3 families; persistence ≥4 quarters; outside the peer IQR in ≥3 of the last 4 quarters; no AE fails; at most one partial; key numbers confirmed in 2 documents.
- **Moderate:** ≥2 families; ≥3 quarters; exactly one AE partially explains it.
- **Weak:** everything else. Reported only if nothing better exists, and clearly labelled.

### Scoring

Score = weighted geometric mean of (surprise, specificity, persistence, materiality, corroboration, survival) × narrative-gap multiplier × novelty multiplier. A geometric mean means one weak dimension sinks the candidate. Z-scores are **ranking heuristics, not p-values.**

### Contradiction detection (five types, all computed)

Attribution (management credits X, the decomposition shows Y); guidance (missed or quietly revised promises); attention (a big driver gets little airtime); cross-document (deck ≠ results ≠ XBRL ≠ annual report); peer (management blames the industry, but peers don't show it). Conflicting numbers resolve by tier: XBRL > audited AR > results PDF > deck > transcript > rating rationale > news. Conflicts are surfaced, never silently resolved.

### Temporal reasoning

**Bitemporal facts:** valid time (the period a number describes) and knowledge time (when it was first disclosed). This answers when a change began (change point), when it became visible, whether the narrative led or lagged the numbers, and when the press noticed (the **visibility gap**). Mergers split a series into regimes. An "as-of" mode enables time-travel backtests.

### Evidence independence

Each document belongs to a **family**: company, auditor, regulator, rating agency, peer company, industry body, or journalism (original reporting only). Corroboration counts **families, not documents.** Syndicated copies of one press release count **once** (near-duplicate detection). Aggregators like Screener and Trendlyne are **never** used as evidence.

---

## 4. Pipeline (8 stages; target 5–7 minutes per live run)

1. **Ingest:** filings, results, investor decks, transcripts, annual reports, rating actions, RBI data, from NSE/BSE announcements (which LODR requires companies to file).
2. **Normalize:** XBRL first (exact numbers from Q4 FY25 onward); PDF tables with page anchors; vision for complex tables. Everything is checked against identities (e.g. opening + slippages − upgrades − recoveries − write-offs = closing). Anything unreconciled can never be a headline number. Units, fiscal calendars and standalone vs consolidated basis are normalised.
3. **Expect:** driver panel for the target and peers; claim ledger from transcripts; disclosure-diff (KPIs appearing or disappearing, new notes); rating-rationale "mirror" evidence.
4. **Breach:** robust surprise vs own history and vs peers, persistence, narrative gap, and disclosure triggers. Candidates are clustered so near-duplicates don't repeat.
5. **Triangulate:** independent source families.
6. **Falsify:** the AE1–AE9 battery plus corollaries.
7. **Rank:** gates plus the score plus the strength rule.
8. **Discover:** the 8 required elements. Prose is written by the LLM from evidence IDs only. A regex rejects any digit typed by the LLM, and a guard rejects recommendation language.

**Architecture principles:** deterministic by default, with the LLM used only where language is the problem. One orchestrator (a Python state machine), not a swarm of agents. Relational provenance (every artefact has an ID and every derived value lists its inputs).

**Code decides:** XBRL parsing, reconciliation, driver decomposition, peer residualisation, statistics, tests, gates, scoring, and every number. **The LLM reads and writes:** typed claims from transcripts, mechanism proposals with computable corollaries, counter-evidence search planning, and digit-free prose bound to evidence IDs.

**Tech stack (planned design):** Python 3.12 state machine; httpx with caching; NSE/BSE filing endpoints and static archives; one web-search API plus a fallback for rating rationales, regulator pages and news; XBRL parser plus PyMuPDF/pdfplumber plus vision for tables; DuckDB/SQLite for facts, claims, derived values, tests and provenance; SQLite FTS5 (BM25) for passage retrieval; pandas, numpy and scipy with robust stats (median/MAD) and simple change-point detection; YAML metric libraries per archetype; LLM at temperature 0 with responses cached by input hash, for replayability; React front end with a pdf.js highlight viewer. No graph DB, no vector DB as the core, no multi-agent debate (deliberately removed).

**Pre-indexing policy:** a mirror of public filings for about 60 listed financials and generic sector series may be pre-indexed by the same crawler. Done live for the target: fetching new filings, extraction, claim ledger, candidates, hypotheses, falsification and the report. Never: any per-company prompt, rule, metric or expected answer. A "cold mode" with the cache disabled can be shown on request.

---

## 5. Generalisation

Defined at the **archetype level, not the company level.** Indian banks, NBFCs and insurers report in regulator-prescribed formats, so driver trees are archetype-level by construction. An archetype router reads the reporting taxonomy.

- **Banks:** NPA flows, lagged ratios, deposit franchise, RWA density, priority sector, divergence notes (HDFC, ICICI, SBI, Kotak, Axis).
- **NBFCs/HFCs:** AUM on- and off-book, borrowing mix, Stage 1/2/3 migration, co-lending, rating-rationale mirror (Bajaj Finance, Shriram, Jio Financial).
- **Insurers:** APE mix, VNB margin, persistency, bancassurance concentration, EV walk (HDFC Life, SBI Life).
- **Market infra and holdcos:** generic identities, regulatory calendar, look-through (BSE, Bajaj Finserv).

Thin-history companies such as Jio Financial and BSE trigger an honest "capping" guard rather than a forced story.

**Benchmark design (planned):** practice set HDFC Bank, Axis, Bajaj Finance. Held-out NIFTY set ICICI, SBI, Kotak, Shriram, HDFC Life, SBI Life, Bajaj Finserv, Jio Financial, BSE. Non-NIFTY tie-break simulation Federal Bank, IDFC First, AU SFB, Bank of Baroda, IndusInd, Cholamandalam, LIC Housing, ICICI Pru Life. Plus as-of backtests.

**Target metrics (NOT measured; never quote them as results):** headline numbers 100% correct and ≥98% overall; ≥2 families always; ≥70% of held-out runs give a ≥Moderate discovery; same snapshot run 5 times gives an identical top discovery; p50 ≤6.5 min.

**Planned adversarial cases:** a sector-wide NIM squeeze must be labelled sector (AE1). HDFC–HDFC Ltd merger (July 2023) loan-growth spike must not be reported (AE3). Restatements, thin history, corrupted PDFs, news vs filing conflicts (the filing wins), syndicated fake news, prompt injection inside PDFs, and the Nov 2023 RBI risk-weight change (AE2).

---

## 6. The example discovery (SYNTHETIC — illustrative only)

> Over six quarters, the subject bank's gross NPA ratio fell from 2.31% to 1.62%, but **71% of all NPA reductions were write-offs**, while its fresh-slippage ratio rose from 1.40% to 2.20% as the peer median stayed flat at 1.44%. Management credited **collections in 5 of 6 earnings calls.**

Meaning: the headline improvement is real, but it is **write-off-led, not collections-led**, and it coincides with a **company-specific** rise in new stress that peers don't share.

- **Strength: STRONG.** Survived 8/9 tests; 3 independent source families; 5 quarters of persistence; outside the peer IQR in 4 of 4 quarters; visibility gap of 4 quarters; 143 candidates considered.
- **Funnel:** 143 candidate breaches → 31 structurally valid → 11 corroborated → 4 company-specific → 2 survived falsification → 1 discovery.
- **Rejected examples:** NIM compression (sector-wide, 7 of 8 peers moved together, AE1); CASA decline (management had already disclosed it, AE6); advances growth jump (accounting artefact, portfolio acquisition, AE3); provision coverage rise (denominator effect, AE4); other-income spike (one-off treasury gain); cost-to-income drift (insufficient independent evidence).
- **Counterargument (AE4, partial):** fast loan growth dilutes the GNPA ratio. On a 4-quarter-lagged basis the improvement shrinks from 69 bps to 45 bps (the denominator explains 24 of 69 bps). It doesn't overturn the finding, because the write-off share (71% vs peer median 46%) and the slippage rise are unaffected.
- **Falsification condition:** reconsider if the slippage ratio returns inside the peer range for 2 consecutive quarters, or if the peer-median slippage rises to the subject's level (then it's sector-wide). Mechanism-kill clause: if credit cost falls while write-offs stay elevated, the write-off-led explanation is wrong.
- **Timeline:** fresh slippages began rising in Q1 FY26 and rose for 5 consecutive quarters. "Calibrating unsecured growth" first appears in management language only in Q1 FY27.
- **Provenance example:** +₹14,953 cr fresh slippages over six quarters. Formula: opening GNPA 11,550 + slippages 14,953 − upgrades 1,892 − recoveries 2,906 − write-offs 11,748 = closing 9,957; reconciles in all 6 quarters. Source: quarterly results, notes to accounts, p. 37 (illustrative), Tier 1, SHA-256 of the archived copy recorded.

The prototype's input shows "HDFC Bank", but all outputs say "the subject bank". **None of these figures is a real finding about HDFC Bank or any company.**

---

## 7. What we presented (6-slide deck, about 5 minutes)

1. **Title:** SIGNAL, "Computed, not retrieved."; self/peer/narrative → breach.
2. **Problem and idea:** retrieval finds what's said; dashboards show ratios, not drivers; summarisers repeat the narrative; the three expectations.
3. **How it works:** 8 stages, 6 gates, "code decides / the LLM reads and writes".
4. **Funnel and falsification:** 143 → 1; the nine AE tests.
5. **The output:** the discovery sentence, STRONG / 8 of 9 / 3 families / 5 quarters, the provenance chain, all 8 elements.
6. **The judging criteria:** how SIGNAL addresses each of the nine; public data only; stack.

## 8. The prototype we demoed (about 5 minutes)

An HTML/CSS/JS interface prototype at `submission/prototype/index.html`. It **replays a simulated research run on a synthetic panel.** Every output screen is labelled "Illustrative prototype output" and the header says "Prototype · simulation." Screens:

- **Research:** company input (HDFC Bank, auto-detected bank archetype), period Q1 FY22 → Q1 FY27, 8-peer panel, output contract; RUN RESEARCH.
- **Run (about 14 seconds):** stage rail, research log, live funnel 143 → 1, and the rejected and retained candidates, each with its reason and stage.
- **Discovery:** the sentence, the strength card, the six summary tiles, the three expectation charts, why it matters, numbers (clickable), timeline swimlanes, counterargument, falsification condition, evidence by family.
- **Evidence trail:** derived value → formula → input check → source document → highlighted page passage.
- **Falsification:** "Try to break the discovery"; registered and executed timestamps; the AE table with procedure, result and verdict; SURVIVED 8/9; corollaries; strength rule.
- **Methodology / Generalization:** code vs LLM split, score formula, archetypes, benchmark design, target metrics marked "planned".

---

## 9. Current build status (BE HONEST ABOUT THIS)

> **[TEAM: fill this in with one or two honest sentences before the call. Delete this line once done.]**
> Example: "The interface and the output format are complete. The live pipeline currently does X for banks; Y and Z are in progress."

What is verifiable from our repository today: the design (STRATEGY.md), the Round 1 PDF, the interface prototype (simulated data), screenshots, and a demo video. **There is no live data pipeline in the submitted repository.** If a judge asks whether SIGNAL can run live on a company they choose, **do not claim it can unless the team has filled in the status above saying so.** Suggested honest line:

> "What you saw is our interface replaying a synthetic run to show the exact output. [Status sentence.] The design is identical for every bank because the driver library is defined for the archetype, not for any one bank, so there's nothing company-specific to change."

---

## 10. Likely judge questions, with model answers

**"Run it on [Axis Bank / any company] now."**
Use the honest line in section 9. Don't improvise.

**"Why is this non-obvious?"**
It isn't stated by management (the claim ledger checks this), it isn't prominent in the press (coverage search), it needs at least two documents plus peer data to compute, and we measure the visibility gap: how many quarters it sat in filings before anyone talked about it.

**"Couldn't a Bloomberg-style dashboard show this?"**
A dashboard shows the GNPA ratio. It doesn't break the change into slippages, upgrades, recoveries and write-offs, compare it against eight peers, line it up with what management said in each call, and then test nine alternative explanations. That combination is the discovery.

**"Isn't this just a ratio screen with an LLM on top?"**
The screen is only the candidate generator. A discovery also needs the narrative gap, corroboration from independent source families, and survival of the falsification battery. Most high-scoring breaches get rejected, for example a NIM squeeze killed as sector-wide by AE1.

**"Where exactly did this number come from?"**
Every number is a computed node. Click it to see the formula, the input facts, the reconciliation check, and the document, page and highlighted passage, with a hash of the archived copy. The LLM never types a digit; a regex check rejects any that slip in.

**"Isn't it just sector-wide?"**
That's AE1, our first test. We compare the company with eight same-archetype peers every quarter. If 70% or more move together and the company's residual is insignificant, we relabel it a sector story and don't report it as a discovery.

**"What about multiple testing / false positives?"**
With 12–20 quarterly points, our z-scores are ranking heuristics, not p-values, and with about 150 metrics chance alone produces a few big breaches. That's why we require persistence, peer specificity and independent corroboration jointly, test window sensitivity with a specification curve, and publish the whole funnel including rejections.

**"Is anything company-specific? Isn't the metric library tuning?"**
The library is defined by the regulator's reporting format, so it's the same for every bank: about 35 listed banks share it. There's no per-company prompt, rule, metric or expected answer. The test is held-out and non-NIFTY companies we never developed on.

**"Did you precompute results?"**
We may pre-index a mirror of public filings and generic sector series, using the same crawler. Extraction, the claim ledger, candidates, hypotheses, falsification and the report are designed to run live for the target. There's a cold mode with the cache disabled to prove it.

**"Why trust LLM extraction?"**
XBRL comes first, and it's exact for recent quarters. PDF tables are checked against accounting identities, and failures are re-extracted with vision. Anything still unreconciled is flagged and can never be a headline number.

**"What if the LLM anchors on its first hypothesis or hallucinates a mechanism?"**
Several candidates are tested in parallel. Hypotheses must cite existing evidence IDs and produce computable corollaries; a failed corollary downgrades the hypothesis. Scoring is deterministic, so the LLM never picks the winner.

**"Correlation vs causation?"**
We claim association, plus a mechanism, plus survival of the alternatives, never proof. Comparing against peers around dated events is the strongest causal evidence available from public data.

**"What would disprove your finding?"**
The falsification condition: a threshold, a duration, a mechanism-kill clause and a sector clause, written down before the result and checked every quarter.

**"What if nothing survives falsification?"**
We report the best Moderate or Weak finding with its strength stated clearly, along with the rejected list. A forced story would be worse; the brief's own worked example is rated Moderate.

**"What if the company had a merger or changed its business model?"**
A discontinuity detector splits the series into regimes and the report says so. For example, the HDFC–HDFC Ltd merger in July 2023 must not show up as a loan-growth discovery; that's AE3.

**"How do you handle conflicting numbers between sources?"**
They resolve upward by credibility tier: XBRL, then the audited annual report, results PDF, deck, transcript, rating rationale, and news last. A conflict is never silently resolved; it's surfaced as evidence or flagged.

**"How do you know sources are independent?"**
We count source families, not documents: company, auditor, regulator, rating agency, peer, industry body, and original journalism. Syndicated copies of one press release are deduplicated and count once.

**"How does it handle temporal reasoning?"**
Every fact has two times: the period it describes and when it was first disclosed. That lets us find when a change began, when it became visible, whether management's narrative led or lagged the numbers, and the gap before the press noticed.

**"Why one orchestrator instead of multi-agent?"**
Determinism and replayability. Agent swarms add nondeterminism without improving discovery. We allow agentic loops in only three places: fetching a missing document, the counter-evidence search, and writing up the hypothesis.

**"What about NBFCs, insurers, BSE, Jio Financial?"**
Each archetype has its own driver library: AUM and borrowing mix for NBFCs, APE mix and persistency for insurers, generic identities for market infrastructure. Thin-history companies trigger an honest guard instead of a forced story.

**"Why no graph or vector database?"**
Lineage is a fixed-depth chain of IDs, and the hard work is time-series computation and reconciliation, which SQL and pandas do better. Retrieval is mostly lexical with financial synonyms, so BM25 is enough; we'd add vectors only if the benchmark showed a gain.

**"How long does a run take?"**
The design target is 5–7 minutes per company, with a deadline for each stage and graceful fallback if a source is slow.

**"Why Track A?"**
Indian financial disclosure is the most standardised (regulator-prescribed formats, XBRL, mandatory transcripts), and there's plenty of independent evidence from the RBI and rating agencies. That's where this mechanism is strongest.

**"Do you give a buy/sell view?"**
No. SIGNAL reports a finding, the evidence and how strong it is. A guard rejects recommendation language, in line with the brief.

**"What's your benchmark accuracy?"**
Only if section 9 has real numbers. Otherwise: "Those are our targets, such as 100% correct headline numbers and at least 70% of held-out companies giving a Moderate-or-better discovery. We'll only quote measured results, and we haven't completed that benchmark yet."
