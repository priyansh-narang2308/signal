# FINDING THE NEXT SIGNAL — Strategic Master Document
**ATMOS 2026 · BITS Pilani Hyderabad · Autonomous Financial Research Hackathon**
Prepared 8 Oct 2026. Round 1 deadline: **19 Oct, 11:59 PM IST (11 days left)**. Finals: **25 Oct (17 days left)**.

**Labels used throughout**
- **[F]**: a fact from a source, linked in place or in the Sources appendix.
- **[I]**: an inference backed by research; the reasoning is shown.
- **[H]**: a strategic hypothesis, i.e. our judgement, to be checked by the benchmark.
- **(verify)**: believed true but not re-checked from a primary source in this session. Check it in Phase 0.

---

## A. Executive Verdict

**Track:** **Track A — Banking, NBFCs & Financial Services.** Runner-up: Track D (Pharma), the better choice only under the conditions in §D.

**Core thesis, in two sentences that should open the Round 1 PDF:**
> *A non-obvious finding is, almost by definition, not written down anywhere — so retrieval can only find what someone has already said. The discovery has to be **computed** across documents, and a computed anomaly is not a discovery until it has **survived a serious attempt to explain it away**.*

**Mechanism: "Expectation-Breach Discovery".** For any company, the system builds three explicit, computable *expectations* and looks for persistent breaches of them:
1. **Self expectation (time).** The company's own history, applied to *decomposed drivers* rather than headline ratios. An example is a GNPA change split into slippages, upgrades, recoveries and write-offs.
2. **Peer expectation (cross-section).** Same-archetype peers in the same quarter. This removes sector-wide and macro effects, which is exactly the counterargument the brief's worked example falls into.
3. **Narrative expectation (claims).** A timestamped ledger of what management *said* drives results and what they *promised*, extracted from calls, presentations and the MD&A.

A **candidate** is a breach of one or more of these expectations. It becomes a **discovery** only if it passes four gates:
- **Numbers reconcile:** extracted figures pass accounting-identity checks.
- **Independent corroboration:** at least two *independent source families* support it.
- **Pre-registered falsification:** it survives a battery of tests drawn from a fixed taxonomy of alternative explanations, such as sector-wide effects, regulatory shocks, mergers or restatements, denominator effects, one-offs, data errors, and "management already said it".
- **Testable consequence:** it makes a predicted *consequence* that is then checked in data the hypothesis was not built from.

**Why this wins:**
- **The search space is bounded and economically meaningful.** Candidates come from accounting-identity driver trees and the claim ledger, never from mining correlations. That answers "why isn't this a spurious correlation?"
- **The LLM never types a number.** Every figure in the output is a rendered reference to a computed node, and the node traces to a highlighted passage on a PDF page. That answers "where exactly did this number come from?"
- **The output shows a discovery funnel**, for example: "143 candidates → 11 passed the gates → 1 survived falsification → 5 rejected, with reasons." That answers "aren't you cherry-picking?" and shows robustness directly.
- **Generality comes from regulatory formats, not company tuning.** Indian banks, NBFCs and insurers report in RBI- and IRDAI-mandated formats, so the identity trees are archetype-level by construction. The same code runs on any listed bank, which is the tie-break scenario.
- **Track A has the richest independent evidence families** of any track: RBI sector data, Pillar 3, credit-rating rationales, peer filings and regulatory actions. Triangulation is therefore real rather than "three news sites rewriting one press release."

**What we deliberately do *not* build:**
- a multi-agent swarm
- a graph database
- a vector store as the core
- an MCTS research planner
- fine-tuning
- a chat interface

Each was evaluated and found not to increase discovery quality enough to justify its risk (§F, §T).

**Output:** an **interactive dashboard** officially, laid out as an equity-research note with every claim clickable through to its lineage. It also exports to PDF.

---

## B. Competition Deconstruction

### B1. What the brief literally requires [F, from the participant brief]

| Area | Requirement |
|---|---|
| Input at finals | **One NIFTY 50 company from our track, chosen by the judges on the spot**, run live |
| Tie-break | Judges may run us on **any listed company in the sector, including outside NIFTY 50** |
| Autonomy | "without company-specific tuning or manual help" |
| Required output (per discovery) | Discovery sentence; Why it matters (3–5 bullets); Evidence (multiple *independent* sources, with links); Timeline; Numbers (only what is needed); Counterargument (the strongest one); Falsification condition; Evidence strength (Strong/Moderate/Weak **with reasoning shown**) |
| Traceability | "Every major claim must be traceable to the specific documents, figures, dates and passages." "Findings should not rest on a single article or document." |
| Format | Report OR dashboard, judged equally |
| Data | Public only; paid data is not allowed unless publicly accessible |
| Prohibited | Hard-coded analysis or results for specific companies; investment recommendations; plagiarism; unsupported claims (penalised) |
| Round 1 | PDF, 1 page appreciated and **2 pages maximum**, named `TeamName_TrackA_Round1.pdf`; optional GitHub link plus a **≤2-minute demo video** on a NIFTY 50 company from the track |
| Round 1 judged on | Clarity, feasibility, originality, generalisation, and handling of discovery, triangulation, temporal reasoning and self-falsification. "An MVP is not required to qualify, but a working system is a strong signal." |
| Finals | 10 minutes of presentation plus live demo, then 15 minutes of Q&A, online |
| Finals criteria | Discovery quality · Evidence quality · Novelty · Temporal reasoning · Cross-source reasoning · Falsifiability · Explainability · Robustness · Generality & autonomy |
| **NOT judged** | Foundation model choice; **number of agents**; **visual complexity of the UI**; **report length**; investment recommendation |

### B2. Implicit and hidden requirements [I]

1. **Novelty is defined relative to "a conventional finance dashboard or simple summariser"**, not relative to a top sell-side analyst. That is a reachable bar. Anything that appears as a headline ratio on Screener or Moneycontrol, or that is stated in the press release, fails it. Anything that needs **decomposition, cross-document alignment, peer residualisation or temporal alignment of narrative against numbers** passes it.
2. **"Multiple independent sources" is a trap.** Most teams will count three URLs. Three news articles rewriting one company press release are *one* source. Judges with research backgrounds will know this. Independence has to be modelled explicitly (§K, §P).
3. **The worked example's counterargument shows what they consider the main failure mode:** *sector-wide effects mistaken for company-specific ones*. It is rated "Moderate" for exactly this reason. A system that can *quantitatively* separate company-specific from sector-wide effects addresses the organisers' own stated concern.
4. **"Typical flow … build a timeline → detect patterns and contradictions."** Contradictions between narrative and numbers are expected as a first-class output, not decoration.
5. **"Evidence strength … with the reasoning shown"** rules out an unexplained LLM label. We need a deterministic, displayable rubric.
6. **The angles are "guidance, not a checklist … may uncover a story none of them cover."** The agent must *choose* angles, and should show *why* it chose them. The funnel does this.
7. **The tie-break covers non-NIFTY companies**, so generalisation is tested adversarially in close contests. Practising only on NIFTY names is risky.
8. **Finals are online and live**, so we need latency budgets, network-failure handling and reproducibility.
9. **"Numbers: only the calculations and metrics needed."** They value parsimony and will penalise metric dumps.
10. **No investment recommendation.** The writer must be guarded against "buy/sell/target price" language.

### B3. Competition objective function [H]

P(win) = P(shortlist | Round 1 PDF + MVP video) × P(win | finals).

For the finals we model the score as weighted judge criteria. The weights are our inference from wording, ordering and repetition:

| Criterion | Weight | Why this weight |
|---|---|---|
| Discovery quality (non-obviousness) | 18% | Listed first; it is the title of the event |
| Evidence quality / traceability | 16% | Repeated 4+ times in the brief, and unsupported claims are *penalised* |
| Robustness / falsifiability | 14% | Two criteria; "Challenge" and "Prove" are core verbs |
| Generality & autonomy | 14% | The live random company plus the tie-break make it existential: if the run fails, everything else is zero |
| Novelty vs dashboard/summariser | 10% | Overlaps with discovery quality but is judged separately |
| Temporal reasoning | 10% | Explicit criterion and an explicit output element |
| Cross-source reasoning | 9% | Explicit criterion |
| Explainability | 9% | Explicit criterion; drives Q&A survival |

**The hardest pair to satisfy at once is Non-obviousness × Evidence strength.** Obvious findings are easy to evidence. Non-obvious ones tend to rest on thin evidence. The third, conflicting axis is **Generality**: general systems drift toward generic findings. The fourth is **Live reliability**: rich pipelines are fragile.

### B4. The fundamental technical bottleneck

There are two parts to it.

1. **Candidate generation and selection without company tuning.** The system has to decide *which* of thousands of possible relationships deserves investigation, and has to do it with priors that transfer across companies.
2. **Correct numbers from messy Indian PDFs.** Multi-column tables, ₹ crore/lakh/million units, standalone vs consolidated figures, restatements and merger discontinuities all cause errors. One wrong headline number in front of a research-head judge destroys credibility for the whole run.

The rest of the system (retrieval, writing, UI) is solved commodity engineering.

### B5. "Impressive demo, poor score" vs "simple-looking, high score" [I]

**Looks impressive, scores poorly:**
- A swarm of 6–10 named agents chatting, with an animated graph.
- A 20-page AI-written report.
- A "knowledge graph" visual.
- Discoveries that restate the investor presentation ("NIM compressed due to rate cuts"), the press ("CD ratio rose after the merger") or Screener ratios.
- A counterargument like "macro headwinds may affect performance".
- A falsification condition like "if fundamentals deteriorate".
- Citations to news aggregators.
- Numbers that are subtly wrong.

**Looks simple, scores highly:**
- One sentence, backed by five computed numbers, each clickable to a highlighted line in a filing.
- A peer chart showing the company diverging from 8 peers.
- A two-row timeline: what management said vs what the numbers did.
- A list of the five alternative explanations tested, with the data that ruled each in or out.
- A funnel showing what was considered and rejected.
- A falsification condition with numeric thresholds and a date.

---

## C. Hidden Difficulty

The stated problem is "find a non-obvious insight." The real problem has four parts:

1. **Selection under multiplicity.** With ~150 driver metrics × 20 quarters × peers, some metric will look anomalous by chance. If the selection step isn't disciplined, the LLM will turn noise into a compelling story. The defence has four layers:
   - a fixed, pre-declared metric library per archetype
   - robust statistics
   - persistence and window-robustness requirements
   - peer residualisation and corroboration gates
   We also show the funnel openly.
2. **Attribution.** Separate company-specific effects from sector, macro and regulatory effects, and from accounting artefacts such as mergers (e.g. HDFC Ltd into HDFC Bank, July 2023, (verify)), reclassifications, Ind AS changes and restatements. This is causal inference with ~20 data points. We cannot prove causation, so we must be honest and *structured* about it: difference-vs-peers around dated events, plus mechanism corollaries.
3. **Knowing what is "non-obvious".** We operationalise it in three ways:
   - (a) the finding is not stated in the company's own materials (claim-ledger check)
   - (b) it is not covered prominently by Tier-4 news (coverage search)
   - (c) it requires computation across ≥2 documents
   We also measure a **visibility gap**: how many quarters the signal sat in filings before it was first covered.
4. **Grounded numbers.** Extraction has to be *self-verifying*: NPA movement tables must reconcile, segments must sum to totals, and the XBRL value must equal the PDF value. Anything unreconciled is either excluded or flagged.

---

## D. Track Analysis

### D1. Candidate companies (current NIFTY 50, as of Oct 2026)

Source: Wikipedia's constituent table (Dec 2025), plus NSE Indices' Aug 2026 release in which **BSE Ltd replaced Wipro, effective 30 Sep 2026** [F].

| Track | NIFTY 50 names | Distinct business archetypes |
|---|---|---|
| **A** Financials | HDFC Bank, ICICI Bank, SBI, Kotak, Axis (banks); Bajaj Finance, Shriram Finance (NBFCs); Jio Financial (nascent NBFC/holdco); HDFC Life, SBI Life (life insurers); Bajaj Finserv (holdco); **BSE (exchange, added 30 Sep 2026)** → **12** | 5 (bank, NBFC, life insurer, holdco, market infrastructure) |
| **B** Energy/Power | NTPC, Power Grid, Coal India, ONGC, Reliance (possibly Adani Ent.) → **5–6** | 5 (gen utility, transmission, coal miner, upstream O&G, conglomerate): one company per archetype |
| **C** Consumer/FMCG/Retail | HUL, ITC, Nestlé, Tata Consumer (+ arguably Titan, Asian Paints, Trent, Eternal) → **4–8** | 4–6 (staples, conglomerate, paints, jewellery, apparel retail, quick-commerce platform) |
| **D** Pharma/Healthcare | Sun, Cipla, Dr Reddy's, Apollo Hospitals, Max Healthcare → **5** | 2 (pharma, hospitals), very different from each other |

Financial Services is ~35–36% of NIFTY weight; FMCG ~6%; Healthcare ~4.5%; Power ~3% (NSE factsheet via Bajaj AMC, Apr 2026; Angel One, Aug 2026) [F].

### D2. Per-track assessment

**Track A — Financials**
- *Disclosure quality:* the highest of any sector [I]. RBI prescribes formats for notes to accounts and for analytical ratios in results. The notes include NPA movement tables, divergence disclosures, concentration of deposits/advances/NPAs, transfers of loan exposures, and PSL. Pillar 3 disclosures are quarterly, and RBI is expanding them in 2026 [F]. Since Q4 FY25, results are filed in XBRL through NSE "Integrated Filing–Financial" [F], so recent quarters come as exact machine-readable numbers.
- *Independent external families:*
  - RBI sector data (sectoral credit deployment, bank-group data)
  - RBI regulatory actions and penalties
  - credit-rating rationales (CRISIL, ICRA, CARE, India Ratings). These are free, independent, and disclose NBFC borrowing mix, liquidity and co-lending/off-book AUM [F: e.g. ICRA's InCred rationale gives a banks/NBFCs/capital-markets borrowing split]
  - IRDAI data for insurers (verify)
  - exchange turnover data for BSE
  - MFIN/credit-bureau industry reports for segment stress (verify)
- *Discovery surface:* the deepest of any track. Examples:
  - NPA flow decomposition: write-off-driven vs recovery-driven improvement
  - lagged NPA ratios, i.e. the growth-dilution illusion
  - Stage 2 build-up before Stage 3 (Ind AS NBFCs)
  - CASA erosion and cost-of-deposit drift
  - incremental CD ratio
  - RWA density shifts (mix change, or regulatory risk-weight effects)
  - funding-mix migration around **dated regulatory shocks** (RBI raised risk weights on bank loans to NBFCs in Nov 2023 and partly reversed it from 1 Apr 2025 [F])
  - co-lending dependence: the new Co-Lending Directions took effect 1 Jan 2026 [F]
  - PSLC purchases as a sign of weak priority-sector origination (verify that disclosure exists in notes)
  - RBI divergence disclosures [F: thresholds of >10% of PBT-before-provisions or >15% of incremental GNPA]
  - guidance-vs-delivery records on credit cost and growth
  - bancassurance concentration for insurers
  - derivatives dependence for BSE
- *Comparability:* excellent within each archetype. Peer universe: ~35 listed banks, 50+ listed NBFCs/HFCs, 7+ listed insurers. The tie-break is very well supported.
- *Entity resolution:* moderate. There are subsidiaries (HDFC Bank → HDB Financial; SBI → SBI Cards/SBI Life; Bajaj Finserv → Bajaj Finance/Bajaj Allianz), and mergers break the history.
- *Weaknesses:*
  - **Archetype heterogeneity:** the judges could pick BSE, Jio Financial or Bajaj Finserv.
  - **Familiarity:** the big banks are the most-analysed companies in India, so the "non-obvious" bar is higher for experts. It stays reachable against the brief's "dashboard/summariser" definition.
  - **Crowding:** likely a popular track among finance-club teams [I].
  - Bank PDFs are long, though formats are standard.

**Track B — Energy & Power**
- *External data:* the best of any track. CEA monthly installed capacity, monthly RE generation reports, Grid-India, coal ministry production, PPAC, CERC orders [F: CEA monthly reports exist as PDFs; no official API found]. The brief's angle "announced vs commissioned capacity" maps directly onto CEA data, which is very checkable.
- *Fatal weakness:* **five companies, five archetypes.** That means one practice company per archetype, i.e. no out-of-sample practice. Reliance is a conglomerate whose energy story is buried in O2C, Jio and retail. Power Grid and NTPC are regulated-return businesses with constrained discovery surfaces. Coal India and ONGC are commodity- and policy-driven, so most signals are macro and fail the company-specificity test.
- *Tie-break* (Tata Power, Adani Green, JSW Energy, NHPC, SJVN, Torrent Power, …): decent, but archetypes multiply.
- Crowding is low, which is a plus.

**Track C — Consumer/FMCG/Retail**
- *The worked example is Track C.* [I] Many teams will choose C because they were given a template, and judges have already seen "price vs volume" in their own brief. Reproducing it reads as unoriginal.
- *External data is weak.* Nielsen and Kantar volume data are paid; only GST, CPI and rural-wage data are free and all are macro-level. Volume disclosure is inconsistent: HUL reports underlying volume growth, and many others report nothing comparable (verify per company).
- Archetypes are heterogeneous (ITC conglomerate, Titan jewellery, Trent apparel, Eternal quick commerce).
- Live risk is lower because FMCG documents are short. Discovery surface is moderate: working capital, A&P intensity, channel mix, pricing.

**Track D — Pharma & Healthcare**
- *External data is excellent for the 3 pharma names:*
  - USFDA Data Dashboard (inspection classifications, warning letters, with a JSON API)
  - import alerts (separate source; FDA notes foreign actions are often import alerts not shown in the dashboard [F])
  - ANDA approvals and the Orange Book
  - US drug-shortage data
  - NPPA price controls
- This enables the brief's exact angle, "a regulatory development hit its financials in filings before mainstream coverage", with independent government data and precise dates. The story types are potent: US generics concentration in one molecule, site-status-to-revenue linkage, a quiet business-model shift to specialty or CDMO.
- *Weaknesses:*
  - only 5 NIFTY names, 2 of which are **hospitals**, where FDA machinery is irrelevant (ARPOB, occupancy, bed additions, payor mix)
  - smaller practice set
  - judges are finance-club oriented [I], so pharma-regulatory depth may be judged less expertly but could also impress
- Tie-break universe: 20+ listed pharma and hospital companies.

### D3. Track-selection scoring [H]

Each criterion is scored 1–10, then weighted.

| Criterion (weight) | Why it matters | A | B | C | D |
|---|---|---|---|---|---|
| Disclosure richness & standardisation (15) | Extraction reliability, decomposition depth | 9 | 7 | 6 | 7 |
| Independent external evidence families (15) | Triangulation, cross-source criterion | 8 | 10 | 4 | 9 |
| Archetype homogeneity / generalisation risk (15) | Random company plus tie-break | 5 | 2 | 5 | 5 |
| Discovery surface (identities, forensic patterns) (15) | Non-obviousness supply | 10 | 6 | 6 | 8 |
| Tie-break universe & peer depth (10) | Peer residualisation, out-of-NIFTY readiness | 10 | 7 | 8 | 8 |
| Judge alignment (10) | Organisers are a finance club; a research-head judge (§B, inference) | 9 | 6 | 7 | 6 |
| Crowding (less is better) (10) | Differentiation | 5 | 9 | 3 | 7 |
| Live-demo / extraction risk (10) | Reliability | 6 | 5 | 7 | 6 |
| **Weighted total (/1000)** | | **780** | 645 | 565 | 705 |

**Decision: Track A.** Its main weakness, archetype heterogeneity, can be *engineered around*: deep modules for banks and NBFCs (≈8 of 12 names), a solid insurer module, and a generic module for holdco and exchange. B's weakness (one company per archetype) and C's weakness (no independent volume data, an anchored example) are structural and cannot be engineered around.

**When D beats A** [H]: if a team member has real pharma or regulatory domain knowledge, *and* the team wants to avoid crowding. Even then, the mechanism in this document transfers unchanged: FDA events become the "dated regulatory shocks" and geographic or segment revenue becomes the identity tree.

---

## E. Competitor Landscape (simulated 20 strong teams)

### E1. The average strong team [I]
- **Stack:** LangGraph or CrewAI with Planner → Researcher(s) → Analyst → Critic/"Devil's Advocate" → Writer; Tavily/Perplexity/Serper search; PDFs chunked into a vector DB (Chroma or pgvector); **Screener.in scraped for financial tables**; GPT/Claude/Gemini; a Streamlit or Next.js dashboard with Plotly charts.
- **Findings:** management's narrative restated, or well-known news ("HDFC Bank's CD ratio rose after the merger; it's slowing loan growth to fix it").
- **Evidence:** 3–6 URLs, mostly news (often syndicated copies of the same PR).
- **Counterargument:** generated by the critic agent and generic.
- **Falsification:** vague.
- **Numbers:** a mix of Screener data, LLM-transcribed figures and occasional hallucinations.
- **Provenance:** links to whole documents, not passages.

Two side problems: Screener's ToS grants only "personal, non-commercial transitory viewing" [F], and it is not a primary source.

### E2. The top 5% [I]
- Structured financial data from XBRL or reliable parsing; a ratio panel; peer comparison against 3–5 peers; a timeline chart.
- Sometimes GraphRAG or a Neo4j "financial knowledge graph".
- A critic loop with retrieval for counter-evidence; passage-level citations.
- Possibly earnings-call sentiment and tone over time.
- Good UI.
- **What they still miss:**
  - systematic candidate generation (they *pick* an angle from the brief's suggestions, usually the first one)
  - peer residualisation applied to every candidate
  - source-independence accounting
  - pre-registered falsification
  - a test that the finding is not already known
  - reconciliation-verified numbers
  - "as-of" time travel
  - a visible rejection funnel

### E3. The "obvious winning-looking" architectures that will be common
1. A multi-agent research crew with bull/bear debate.
2. A knowledge-graph or GraphRAG "connect the dots" system.
3. Sentiment/tone analysis of earnings calls.
4. Ratio-anomaly dashboards with LLM explanations.
5. A "deep research" clone (iterative search → report).

### E4. What we will do that they probably won't (central differentiators) [H]
1. **Identity-constrained candidate generation + peer residualisation for *every* candidate**, with a visible funnel (tested → gated → survived → rejected with reasons).
2. **A claim and promise ledger:** every causal attribution and forward guidance statement is timestamped, mapped to a metric and scored against later actuals. This produces narrative–number lead/lag analysis and a "promise-keeping" record.
3. **Source-family independence accounting.** Company documents count as one family; syndicated news is deduplicated; regulator, rating agency, peer and auditor are separate families.
4. **Reconciliation-verified extraction, and a rule that the LLM never types a digit.**
5. **Pre-registered falsification with mechanism corollaries:** each hypothesis must predict something it was not built from, and that prediction is tested.
6. **A visibility-gap measurement:** the first quarter the signal was visible in filings vs the first Tier-4 coverage. This is quantified non-obviousness.
7. **Time-travel backtests in the benchmark:** run the system "as of" a date before a now-known event and show it flagged the precursors.
8. **A cross-entity mirror:** evidence about the company from *other* entities' disclosures (rating rationales, peer/counterparty notes, co-lending announcements). This directly answers the brief's "dependency … not visible from its own disclosures alone."

---

## F. Candidate Approaches (14 directions)

Each direction is summarised, then compared in the table in F2.

1. **Generic multi-agent RAG researcher (baseline).** Planner, researchers, critic, writer over search plus a vector DB. It discovers whatever the text says, so it is novel only by accident. The likely judge attack, "isn't this a summariser?", lands. It is easy to copy and has no moat.
2. **Anomaly-first quant screen.** Robust z-scores of ratios vs own history and peers, with an LLM explaining the top anomalies. Strong numbers and bounded search; on its own it is weak on narrative, corroboration and attribution. Attack: "statistically interesting, economically meaningless?"
3. **Narrative-vs-numbers contradiction engine.** Extract management claims and test them against computed facts. Directly matches the "contradictions" language and is very explainable. On its own it depends on claim-extraction quality and finds only contradictions of *stated* claims, missing unnarrated breaches.
4. **Disclosure-diff ("Lazy Prices") engine.** Diff annual-report notes, risk language and KPI sets year over year; flag KPI disappearance, definition changes and new notes. There is academic grounding: changes in 10-K language predict future earnings and returns, and investors are inattentive to them (Cohen, Malloy & Nguyen, *J. Finance* 2020 [F]). Excellent "where to look" triggers, but a trigger is not a discovery and needs quantification.
5. **Identity decomposition / driver attribution.** DuPont-style trees per archetype (NPA flows, RoA tree, funding mix, EV walk). Generates *economically meaningful* candidates with exact arithmetic and generalises at archetype level. Needs peer and narrative baselines to rank candidates.
6. **Cross-entity counterparty mirror.** Build exposures from *other* entities' disclosures: rating rationales, partner announcements, bank notes on NBFC exposure, BRSR "openness of business" concentration metrics [F: BRSR Core requires concentration of purchases/sales with dealers/trading houses/related parties]. Uniquely answers the "hidden dependency" angle, but data is sparse and irregular, entity resolution is hard, and coverage is uneven.
7. **Regulatory event study.** Given dated sector shocks (RBI risk weights, co-lending rules, SEBI F&O curbs, IRDAI surrender norms), estimate each company's differential exposure against peers (difference-in-differences). Strong attribution and very temporal, and it plays to a geo-economic and macro-oriented judge [I]. Few events and small n; it is a *test* more than a generator.
8. **Forensic scores** (Beneish M, Sloan accruals, Piotroski, cash conversion). Well known and credible, but designed for industrials. They mostly **don't apply to banks**, where accruals and working-capital logic differ. Partial fit only.
9. **GraphRAG / knowledge-graph multi-hop.** Entity-relation graph from documents with multi-hop queries. It looks impressive but is graph-structured retrieval of what text says, so it has the same novelty ceiling as #1 at higher cost and risk. Reject as core.
10. **Guidance-credibility tracker (promise ledger).** Forward-looking statements → realised outcomes → credibility over time, plus revision patterns. Highly temporal, auditable and rarely done systematically. A subset of #3; adopt.
11. **Adversarial debate tournament** (bull vs bear agents with an LLM judge). Popular and theatrical. LLM debate improves rhetoric, not evidence: both sides can hallucinate, and the judge rewards fluency. Reject; real falsification needs *data tests*.
12. **Analyst-consensus divergence.** Requires consensus estimates, which are paid (Bloomberg/Refinitiv/Trendlyne premium). Infeasible under the public-data rule.
13. **Alternative data** (app downloads, job postings, web traffic, Google Trends). Mostly paid, noisy or not reproducible; weak for financials. Reject, except possibly job postings as a niche signal.
14. **Hypothesis tree search (MCTS over research questions).** Over-engineered: nondeterministic, slow, hard to explain, and the value of the search is dominated by the quality of the candidate generator. Reject.

### F2. Comparison (1–10, higher is better) [H]

| # | Approach | Discovery | Evidence | Novelty | Temporal | Cross-src | Falsif. | Explain | Robust | General | Feasible (17 d) | Demo rel. | Differentiation |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Multi-agent RAG | 3 | 4 | 2 | 3 | 5 | 3 | 5 | 3 | 7 | 8 | 5 | 1 |
| 2 | Quant anomaly screen | 6 | 8 | 6 | 6 | 3 | 4 | 7 | 5 | 8 | 8 | 8 | 5 |
| 3 | Narrative-vs-numbers | 7 | 7 | 7 | 7 | 6 | 6 | 9 | 6 | 7 | 7 | 7 | 7 |
| 4 | Disclosure-diff | 6 | 7 | 8 | 7 | 4 | 4 | 7 | 5 | 8 | 6 | 7 | 8 |
| 5 | Identity decomposition | 7 | 9 | 7 | 7 | 4 | 5 | 9 | 7 | 8 | 7 | 8 | 6 |
| 6 | Counterparty mirror | 8 | 6 | 9 | 5 | 9 | 5 | 6 | 5 | 4 | 4 | 4 | 9 |
| 7 | Regulatory event study | 6 | 8 | 7 | 9 | 7 | 8 | 8 | 8 | 7 | 7 | 7 | 7 |
| 8 | Forensic scores | 4 | 7 | 4 | 5 | 2 | 4 | 6 | 5 | 3 | 8 | 8 | 3 |
| 9 | GraphRAG | 4 | 5 | 3 | 3 | 6 | 3 | 4 | 3 | 6 | 4 | 3 | 3 |
| 10 | Promise ledger | 7 | 8 | 8 | 9 | 6 | 7 | 9 | 7 | 8 | 7 | 7 | 8 |
| 11 | Debate tournament | 3 | 3 | 3 | 2 | 3 | 4 | 5 | 3 | 7 | 8 | 6 | 2 |
| 12 | Consensus divergence | — | — | — | — | — | — | — | — | — | 1 | — | — |
| 13 | Alt data | 4 | 3 | 6 | 5 | 5 | 3 | 4 | 3 | 3 | 3 | 3 | 5 |
| 14 | MCTS planner | 5 | 4 | 5 | 4 | 5 | 4 | 3 | 4 | 6 | 3 | 3 | 6 |

**Takeaway.** No single direction wins; the strong ones are *complementary*:
- **#5 and #2** generate economically grounded candidates.
- **#3 and #10** add the narrative baseline and the temporal story.
- **#4** adds triggers that change where to look.
- **#7** supplies the attribution tests.
- **#6** supplies the cross-entity evidence that makes triangulation independent.

The winning concept fuses them under one principle, **expectation breach + falsification**, and drops #1, #8, #9, #11, #12, #13 and #14 as cores.

---

## G. Winning Concept

**"Expectation-Breach Discovery Engine" for Indian financials.** Working names: *Breach* or *Counterfactual*; avoid buzzwords.

> **Given a company, the system computes what we should expect to see — from its own history, from its peers in the same quarter, and from what its management said — and investigates the places where reality persistently breaks those expectations. Every breach is then attacked with a fixed battery of alternative explanations. Only breaches that survive, are material, are corroborated by independent source families, and are not already stated by the company or the press are reported as discoveries.**

### Five mechanisms

**Discovery (3):**
- **M1. Driver panel.** Identity-constrained metrics for the target and same-archetype peers over 12–20 quarters, with robust surprise scores against self and against peers.
- **M2. Claim & promise ledger.** Timestamped attributions and guidance mapped to metrics; narrative attention per call; promise-keeping record.
- **M3. Disclosure-diff triggers.** Disclosure items or KPIs that appear or disappear, definition changes, new notes (divergence, co-lending, TLE), auditor or KMP changes, rating actions.

**Safety (2):**
- **S1. Verified numbers.** XBRL-first extraction with arithmetic reconciliation; the LLM never types a digit.
- **S2. Falsification battery + source-family independence.** A pre-registered taxonomy of alternative explanations with deterministic tests, mechanism corollaries and evidence-strength rules.

**Track-A booster:** **M4. Cross-entity mirror** (rating rationales, counterparty disclosures, regulator actions), used as an independent evidence family and as a source of candidates.

---

## H. Core Innovation (the one thing to say if we have 10 seconds)

**Discoveries are computed as persistent breaches of three independent expectations (self, peers, narrative), and they must survive pre-registered attempts to explain them away before they are reported.**

What makes it differentiated rather than a screen:
- **Peer residualisation is built into candidate generation**, so sector-wide stories are demoted automatically. This is the failure mode in the brief's own worked example.
- **The narrative baseline turns an anomaly into a story.** "The numbers moved" becomes "the numbers moved against what management said, starting in Q2 FY25, two quarters before management changed its language." That one sentence covers temporal reasoning, contradiction and cross-source reasoning.
- **The funnel makes the process auditable.** We show what was rejected and why, which no summariser can do.

---

## I. Architecture

### I1. Principles
- **Deterministic by default; the LLM only where language is the problem.** That means reading unstructured text into typed records, articulating mechanisms, planning counter-evidence searches, and writing prose bound to evidence IDs.
- **One orchestrator with tools, not a swarm.** The pipeline is an explicit state machine with stage deadlines. Agentic loops are allowed in exactly three places: (1) acquiring a missing document, (2) counter-evidence search and reading, (3) hypothesis articulation.
- **Relational provenance.** Every artefact has an ID and every derived value lists its inputs.

### I2. Components (why each exists)

| Layer | Choice | Why it exists / why not the alternative |
|---|---|---|
| Orchestration | Python 3.12 state machine (plain code; LangGraph optional only if it saves time) | Determinism, stage deadlines, replay. Agent frameworks add nondeterminism without discovery value. |
| Acquisition | `httpx` with persistent cache; NSE and BSE corporate-filing endpoints (undocumented JSON used by their own websites; session cookie; ≤1 req/s); static archive URLs (`nsearchives.nseindia.com/corporate/...`, BSE `AttachLive`) | **Exchange announcements are the canonical discovery path.** LODR requires results, presentations, transcripts (within ~5 working days [F]), rating actions and board outcomes to be filed with the exchanges. That avoids SEO and search fragility for Tier 1–2 documents. |
| Web search | One API (Brave/Tavily/Exa/Serper) + one fallback; domain allow-list by tier | Needed only for Tier 3–4 documents: rating rationales, regulator pages, news coverage and counter-evidence. |
| Parsing | XBRL first (Integrated Filing–Financial, from Q4 FY25 [F]); PyMuPDF/pdfplumber for text and tables; LLM vision on page images for complex tables | XBRL is exact for recent quarters. Older quarters and investor decks need PDF/table extraction. Vision handles merged cells. **Every extraction passes reconciliation checks.** |
| Storage | **DuckDB/SQLite** (facts, claims, derived values, tests, provenance) + file store (PDFs, page PNGs with highlight boxes) | The queries are lineage lookups and time-series computations: relational wins. A **graph DB adds nothing** that a foreign-key DAG doesn't already give. |
| Text retrieval | **SQLite FTS5 (BM25)** over page-level passages + LLM rerank; embeddings optional | Claim and evidence lookup is mostly lexical with financial synonyms (ontology expansion). Add vectors only if the benchmark shows recall gains. |
| Compute | pandas/numpy/scipy; robust stats (median/MAD); simple change-point detection (rolling-median shift + persistence; optional `ruptures` PELT) | Small n, so simple robust methods beat fancy ones and are explainable. |
| Metric library | YAML per archetype: formulas, identities, synonyms, expected signs, materiality mapping | Archetype-level domain knowledge, *not* company tuning; it applies to every bank. |
| LLM | Strong model for hypothesis and falsification reasoning; mid model for extraction; small model for classification. Temperature 0 and response caching keyed by input hash. | Model choice is not judged. Caching gives replayability. |
| Frontend | React (Vite/Next) + Recharts + pdf.js viewer with highlight overlay; PDF export via headless browser print | Click-through lineage is the core UX. |
| Observability | JSONL run trace (stage, inputs, outputs, timings, tokens) rendered as the **live funnel** | Doubles as the demo narrative and as audit evidence. |

### I3. Data model (core tables)

- `entity`: `symbol, isin, name, aliases[], archetype, parent, subsidiaries[]`
- `document`: `doc_id, url, archive_sha256, publisher, family, tier, doc_type, period, published_at, retrieved_at`
- `passage`: `passage_id, doc_id, page, bbox/char_span, text`
- `fact`: `fact_id, entity, metric, period_end, value, unit, scale, basis (standalone|consolidated), passage_id, method (xbrl|table|vision), reconciled (bool), recon_rule, version (as-reported|restated), known_at`
- `derived`: `node_id, metric, entity, period, formula, input_ids[], value`
- `claim`: `claim_id, entity, speaker, role, date, passage_id, type (attribution|guidance|assertion|denial), metric, direction, magnitude, horizon`
- `event`: `event_id, scope (sector|company), date, type, source passage`
- `candidate`: `cand_id, metrics[], breach_type (self|peer|narrative|disclosure), scores{}`
- `hypothesis`: `hyp_id, cand_id, statement, mechanism, corollaries[]`
- `test`: `test_id, hyp_id, ae_type, procedure, result (pass|partial|fail), evidence_ids[]`
- `discovery`: `disc_id, hyp_id, strength, rationale, rendered_report_id`

---

## J. Discovery Pipeline (end-to-end, live)

**Stage 0 · Resolve (≈5 s).** Symbol → ISIN, legal names, aliases and subsidiaries. **Archetype router:** read the results XBRL taxonomy (banking / NBFC Ind AS / insurance / general; (verify) that Integrated Filing uses distinct taxonomies) and the NSE industry classification. Then select the peer set: same archetype, ranked by size proximity, 6–10 peers, including non-NIFTY companies.

**Stage 1 · Acquire (≈30–90 s live delta; history cached).**
- From exchange announcements, last 5 years: results, investor presentations, transcripts, annual reports, rating actions, board outcomes, press releases, and regulatory penalty or embargo notices.
- From regulators: sector series (RBI) and dated sector events (the regulatory calendar, generic).
- Rating rationales via targeted search on agency domains.
- Peers come from the cache, refreshed for the latest quarter.

**Stage 2 · Extract & reconcile (≈60–120 s, parallel).**
- XBRL facts are taken directly.
- PDF tables are extracted with page anchors, then checked against identities:
  - NPA movement: opening + additions − upgrades − recoveries − write-offs = closing
  - segments sum to total
  - balance sheet balances
  - PDF value = XBRL value where both exist
  - deck value = results value
- Failures are re-extracted with vision. Anything still failing is marked `unreconciled` and *cannot* be a headline number.
- Units and scale are normalised (₹ cr/lakh/mn), along with fiscal calendars (Q1 = Apr–Jun) and basis (standalone vs consolidated).
- **Discontinuity detector:** mergers and restatements (totals jumping more than X% with a corporate-action event) split the series into regimes.

**Stage 3 · Build baselines (≈20–40 s).**
- M1: the driver panel for target and peers.
- M2: the claim and promise ledger. LLM extraction over transcripts and decks into typed claims, metric mapping through the ontology, then deterministic scoring of guidance against actuals.
- M3: disclosure-diff. Section-aligned diff of AR notes and KPI inventories across years (KPI appeared/disappeared, definition text changed, new note types).
- M4: mirror evidence (rating-rationale facts such as borrowing mix and top-lender concentration; regulator actions).

**Stage 4 · Generate & rank candidates (seconds).** For every metric node, compute:
- self-surprise: robust z of the recent window vs the pre-window
- peer-surprise: robust z of the company vs the cross-section, and of its trend slope vs the peer slope distribution
- persistence: share of recent quarters in breach
- narrative gap: driver contribution vs management attention share, and contradiction with explicit attributions
- disclosure triggers that touch the node
Candidates are clustered by mechanism family to avoid near-duplicates. The **pre-falsification score** (§O) is computed and the top K = 5–8 move on.

**Stage 5 · Hypothesise (≈30 s).** For each candidate, the LLM receives *only* the linked evidence bundle (node values, claims and triggers, by ID) and must output structured fields:
- a mechanism statement
- which alternative-explanation types apply
- **2–3 corollary predictions**, written as computable queries over the panel (e.g. "if growth was driven by unsecured lending, credit cost should rise with a 2–4 quarter lag")
- the evidence IDs it relies on
Hypotheses that cite non-existent IDs are rejected automatically.

**Stage 6 · Falsify (≈60–90 s).** Run the AE battery (§N): deterministic tests over the panel, plus a bounded agentic counter-evidence search (≤12 queries per hypothesis, tier allow-list), then the corollary tests and the coverage/novelty search.

**Stage 7 · Score & select (seconds).**
- Apply gates, compute the final score and assign the strength rule.
- Pick 1 primary discovery plus up to 2 secondary ones.
- Keep the rejected list, with reasons.

**Stage 8 · Compose & render (≈30 s).**
- The writer LLM fills a template whose number slots can only be filled with `{node_id}` references, which are rendered at display time.
- A post-check regex rejects any digit in LLM prose that is not inside a reference.
- A guard rejects recommendation language.
- Output: the 8 required elements, plus the funnel and the lineage.

**Total target: p50 ≈ 5–6 minutes, p95 ≤ 8 minutes**, with stage deadlines and graceful degradation (§Q).

---

## K. Evidence / Provenance

1. **The lineage chain is a DAG of IDs:** Discovery → Hypothesis → (supporting tests, contradicting tests) → Derived nodes → Facts → Passages → Documents (URL + SHA-256 of the archived copy + page PNG with highlight). Claims and events attach to hypotheses and tests in the same way.
2. **Click-through UX.** Click any number to open a drawer showing the formula, the input facts (each with source, page and highlighted crop), the reconciliation rule passed, the original URL and the archived copy. Click any claim quote to see speaker, date, call and page. A judge can audit any number in about 2 clicks.
3. **Why relational, not a graph DB:** lineage is a fixed-depth DAG, and the hard parts are time-series computation and reconciliation, which SQL and pandas handle better. We render the DAG as a graph *view* without storing it in a graph *database*.
4. **Evidence independence.** Each document gets a `family`:
   - company (results, deck, transcript, AR, PR)
   - auditor (audit report, EoM/qualification)
   - regulator (RBI/SEBI/IRDAI/exchange data)
   - rating agency
   - peer company
   - industry body
   - journalism (original reporting only)
   Corroboration is counted by **distinct families**, not documents. Near-duplicate news is collapsed using MinHash or shingle similarity plus an "according to a press release" pattern check.
5. **Restatements:** both `as-reported` and `restated` values are kept, with `known_at`. Analysis uses restated values; the "when was it visible" analysis uses as-reported values.

---

## L. Temporal Reasoning

**Bitemporal facts:** every fact has *valid time* (the period it describes) and *knowledge time* (when it was first disclosed, from the announcement timestamp). This enables:
- **"When did it begin?"** A change point in the driver series (valid time).
- **"When did it become visible?"** The first disclosure in which the breach crossed threshold (knowledge time).
- **"Did the narrative lead or lag the numbers?"** The quarter management first mentioned or attributed the driver (claim ledger) vs the change-point quarter. Language shifts are tracked too: attention share by call, and first use of hedging terms (e.g. "normalising", "calibrated growth").
- **"When did the press notice?"** The first Tier-4 coverage date. The **visibility gap** is that date minus the first-visible disclosure date.
- **"Before and after?"** Sector events (regulatory calendar) and company events (management change, rating action, capital raise, embargo, merger) on the same axis.
- **"Did competitors experience it?"** Peer series aligned on the same calendar quarters, with the share of peers breaching in the same direction.
- **Lagged ratios:** e.g. GNPA_t / Advances_{t−4} and t−8 to strip out growth dilution, a classic analyst technique that dashboards don't show.
- **Regime handling:** mergers and business-model transitions split series. Comparisons are made within a regime or on a pro-forma basis, and the split is disclosed.
- **"As-of" mode:** the store can be queried at a past knowledge time, which powers the time-travel backtests (§V).

**Timeline output:** two swimlanes (Numbers | Narrative) plus an events lane, with markers for change point, first visible and first covered.

---

## M. Contradiction Detection

Five contradiction types, all computed:
1. **Attribution contradiction.** Management attributes an outcome to driver X, but the decomposition shows that driver Y contributed most. Example form: "improved collections" claimed while ≥60% of the GNPA reduction came from write-offs.
2. **Guidance contradiction.** A promise is missed repeatedly, or quietly revised. The promise ledger records the hit rate, average miss, direction bias and the number of revisions.
3. **Attention contradiction.** A driver contributes heavily to the change but gets little management airtime, or airtime falls as the metric worsens. This is measured by attention share from sentence classification.
4. **Cross-document contradiction.** A number in the deck ≠ the results PDF ≠ XBRL ≠ the AR, or a rating rationale's description (e.g. borrowing mix, liquidity) diverges from the company's own framing.
5. **Peer contradiction.** Management cites an industry-wide cause, but peers don't show it (peer residual test).

**Resolution policy for conflicting numbers:** XBRL > audited AR > results PDF > deck > transcript > rating rationale > news. A conflict is never silently resolved. It is surfaced as evidence ("deck rounds 2.14% to 2.1%" is benign; "deck 2.1% vs results 2.6%" is a finding or a flag).

---

## N. Self-Falsification Engine

For every hypothesis, the system fills a **pre-registration card** *before* running tests, so it cannot move the goalposts afterwards:

| Question | How it is answered automatically |
|---|---|
| 1. What must be true? | Mechanism statement plus the identity nodes involved |
| 2. Supporting evidence? | The node breaches and claims that generated it |
| 3. What would weaken it? | Generated from the AE taxonomy below plus corollaries |
| 4. Alternative explanations? | All applicable AE types, chosen by rule from the archetype and metric family, plus LLM proposals mapped onto AE types |
| 5. What distinguishes them? | Each AE type has a fixed test procedure (below) |
| 6. Which periods? | Pre/post change point; window-robustness over all start dates in a range |
| 7. Which competitors? | The archetype peer set (6–10), including non-NIFTY |
| 8. Which macro/regulatory variables? | The sector event calendar: rate cycle, risk-weight changes, co-lending rules, SEBI/IRDAI rule dates |
| 9. Which future observation invalidates it? | The falsification condition (below) |

### The alternative-explanation taxonomy and its tests

| AE | Alternative explanation | Deterministic test | Effect |
|---|---|---|---|
| AE1 | **Sector-wide** | Company vs peer distribution each quarter. Share of peers moving the same way; company residual vs peer median; rank stability | ≥70% of peers co-move and the residual is insignificant → *fail* (relabel as a "sector story", or a "company is more/less exposed" variant) |
| AE2 | **Regulatory/macro shock** | Is there a dated sector event within ±1 quarter of the change point? Difference-in-differences: change for the company minus the peer median change around the event | Peers show the same jump → partial or fail; company-specific excess survives |
| AE3 | **Accounting / definitional artefact** | Disclosure-diff on definitions; merger/restatement flags; segment reclassification; Ind AS or policy change notes | A discontinuity explains the breach → *fail* (critical gate) |
| AE4 | **Denominator / base / seasonality** | Lagged ratios; same-quarter YoY; Q4 write-off and recovery seasonality; one-off items | Effect vanishes → fail |
| AE5 | **Noise / cherry-picked window** | Specification curve: recompute over all reasonable window starts and lengths; report the share of specifications where the sign and threshold hold | <70% → fail; 70–90% → partial |
| AE6 | **Already known / stated** (novelty) | Claim ledger: did management explicitly state it? Coverage search: is it prominent in Tier-4 news? | Stated and covered → novelty penalty (not falsified, but demoted) |
| AE7 | **Data error** | Key numbers re-derived from a second document/family; reconciliation status | Mismatch → gate fail |
| AE8 | **Mechanism failure** | **Corollary predictions** tested on data *not used* to generate the hypothesis | Corollaries fail → hypothesis downgraded or replaced by an alternative |
| AE9 | **Counter-evidence in the wild** | Bounded search for explicit contrary facts (rating rationale, regulator data, peer commentary); the LLM reads and classifies each as support/contradict/irrelevant with passage IDs | Strong contrary fact from an independent family → partial or fail |

**Falsification condition generator.** It uses the hypothesis's primary driver metric:
- **Threshold:** the level that would put the company back inside the peer IQR, or within its own pre-change-point range.
- **Duration:** 2 consecutive quarters, plus a **mechanism-kill clause** taken from the corollary.
- **Sector clause:** "or if the peer median moves to the company's level."

Example format (fictional):
> Reconsider if gross slippage ratio is < 1.6% for two consecutive quarters **and** write-offs fall below 40% of GNPA reduction; or if the peer median slippage ratio rises to ≥ the company's level (i.e., the effect becomes sector-wide).

**Why this is not "ask the LLM for counterarguments":**
- The alternatives come from a fixed taxonomy.
- The tests are code over data.
- Results are recorded before the narrative is written.
- The strongest *surviving* alternative becomes the reported counterargument, with its evidence.

---

## O. Discovery Scoring

### O1. Gates (all must pass)
- **G1:** headline numbers reconciled (S1) or confirmed by a second document.
- **G2:** at least 2 independent source families.
- **G3:** persistence of at least 2 quarters (not a single-quarter blip).
- **G4:** AE3 (accounting artefact) and AE7 (data error) not failed.

### O2. Score (weighted geometric mean, so one weak dimension sinks the candidate)

`Score = GM_w( Surprise, Specificity, Persistence, Materiality, Corroboration, Survival ) × NarrativeGap × Novelty`

| Component | Definition | Why |
|---|---|---|
| **Surprise** | Logistic of robust z (median/MAD) of recent window vs own pre-window | Change over time |
| **Specificity** | Logistic of the company's residual vs the peer cross-section, and of its trend slope vs the peer slope distribution | Kills sector-wide stories (the worked example's failure) |
| **Persistence** | Share of recent quarters in breach × specification-curve robustness | Kills noise and cherry-picked windows |
| **Materiality** | Impact on PBT, RoA or net worth (e.g. "if credit cost reverted to peer median: X% of PBT"), mapped to [0,1] | Economic meaning, not just statistical |
| **Corroboration** | Distinct independent families: 1→0.3, 2→0.7, ≥3→1.0 | Triangulation, independence-aware |
| **Survival** | Severity-weighted share of AE tests passed | Robustness |
| **NarrativeGap** (multiplier) | Contra-narrated 1.5 · unnarrated 1.25 · acknowledged 1.0 · explicitly flagged and widely covered 0.6 | Non-obviousness and contradiction |
| **Novelty** (multiplier) | Visibility gap ≥2 quarters → ×1.2; prominent Tier-4 coverage → ×0.7 | "Would a summariser miss it?" |

### O3. Evidence-strength rule (shown verbatim in the output; deterministic)
- **Strong:** ≥3 families; persistence ≥4 quarters; company outside the peer IQR in ≥3 of the last 4 quarters; no AE fails; at most one partial; key numbers confirmed across 2 documents.
- **Moderate:** ≥2 families; persistence ≥3 quarters; exactly one AE partially explains it (e.g. partly sector-wide). This is the worked example's rating, by design.
- **Weak:** everything else. Reported only if nothing better exists, and clearly labelled.

### O4. How this avoids the classic failures
- **Spurious correlations:** the search runs over identity-tree nodes with an economic interpretation, never arbitrary pairs.
- **Cherry-picking:** the full funnel is shown, the window is tested by the specification curve, and the metric library is pre-declared.
- **Confirmation bias:** cards are pre-registered; the critic is a set of data tests, not an LLM persona. The LLM reads counter-evidence under an instruction to classify, not to argue.
- **Narrative bias:** prose is written *after* scoring, from evidence IDs only.
- **Weak, duplicate or contaminated evidence:** family counting, syndication deduplication and the tier allow-list.
- **Hallucinated relationships:** hypotheses must cite existing IDs; corollaries must be computable; no LLM digits.

**Statistical honesty for Q&A:** with 12–20 quarterly points, z-scores are *ranking heuristics, not p-values*. With ~150 nodes, chance alone yields a handful of |z|>2 breaches. That is why we require persistence, peer specificity and corroboration jointly, and why we publish the funnel. A judge who asks about multiple testing should get exactly this answer.

---

## P. Data Strategy

### P1. Source hierarchy (tier = credibility; family = independence)

| Tier | Sources | Family | Use |
|---|---|---|---|
| 1 | Results (XBRL + PDF), annual reports (notes, audit report), shareholding (Reg 31, XBRL), Pillar 3, regulatory filings | Company / Auditor | Facts |
| 1R | RBI (DBIE sector credit, bank-group stats, FSR, penalties/actions, circulars); SEBI/IRDAI circulars and data; exchange turnover data | Regulator | Sector baselines, events, independent facts |
| 2 | Investor presentations, earnings-call transcripts and audio (LODR Reg 46 [F]), press releases | Company | Claims, KPIs |
| 3 | Credit-rating rationales (CRISIL/ICRA/CARE/India Ratings); peer filings; industry bodies (MFIN, credit bureaus), (verify) access | Rating / Peer / Industry | Independent corroboration, mirror evidence |
| 4 | Original reporting in high-quality financial journalism (Business Standard, ET, Mint, Reuters, Moneycontrol originals) | Journalism | Coverage dating, context, counter-evidence |
| 5 | Aggregators, blogs, broker summaries, Screener/Trendlyne | — | **Never as evidence.** At most a pointer to a primary source. |

**Interaction rules:**
- A Tier-4/5 item can *point to* evidence but never *be* the only evidence for a number.
- Conflicts resolve upward by tier (§M).
- Corroboration counts families, not documents.

### P2. Source-by-source feasibility

| Source | Access method | Official API? | Feasibility / risk | Depth | Failure modes |
|---|---|---|---|---|---|
| NSE corporate filings (announcements, results incl. **XBRL** since Q4 FY25, annual reports, shareholding) | Website JSON endpoints (undocumented; require a session cookie from the homepage) + static archive PDFs | **No documented public API found** [F] | Works with polite rate limiting; may block bursts; ToS unverified → low-volume, cached, non-commercial research use | 5+ years | Cookie expiry, 401/403, format drift |
| BSE corporate announcements | `api.bseindia.com` JSON used by the site (Referer header) + `AttachLive` PDFs; community libraries exist [F]; bselib warns of IP blacklisting under load [F] | No public API (BSE sells licensed data [F]) | Mirror/fallback for NSE | 10+ years | Rate limit, blocking |
| Company IR sites | Direct fetch | n/a | Heterogeneous; prefer exchange copies | Varies | Broken links, JS-rendered pages |
| XBRL (Integrated Filing–Financial) | From NSE results page "XBRL FILE LINK" [F] | File-based | Exact numbers; taxonomy parsing needed | Q4 FY25 onward | Taxonomy variants, missing tags |
| RBI DBIE / Handbook | Web export (Excel/CSV); **no official API found** [F] | No | Pre-download sector series (generic, not company-specific) | Decades | Site changes |
| RBI press releases (penalties, actions), circulars | HTML | No | Event calendar | Decades | — |
| Pillar 3 / LCR / NSFR | Bank websites, regulatory disclosure sections [F] | No | Per-bank URL discovery via search | 3–10 yrs (archive rules changing [F]) | Inconsistent URLs |
| Rating rationales | Agency websites (CRISIL HTML; ICRA PDF viewer) [F] | No | Search by entity name on agency domains | ~10 yrs | Name matching, JS viewers |
| IRDAI insurer data / public disclosure forms | IRDAI site; insurer sites (verify) | No | Insurer archetype | Years | PDFs |
| BSE/NSE turnover data | Exchange reports | Partly downloadable | BSE archetype | Years | Format drift |
| Web search | Commercial API (Brave/Tavily/Exa/Serper) | Yes | Tier 3–4 discovery; counter-evidence | — | Quota; result drift → cache |
| Screener/Trendlyne | — | — | **Excluded as evidence** (ToS: "personal, non-commercial transitory viewing" [F]; not primary) | — | — |

### P3. Pre-indexing policy (fair-play statement for the judges)
- **Pre-indexed:**
  - a *mirror of public filings* for ~60 listed financials (all NIFTY Track A names plus peers and non-NIFTY candidates), built by the same crawler the live system uses
  - generic sector series and the regulatory calendar
  - peer extraction panels (peer baselines only)
- **Done live, for the target company:**
  - delta fetch of new filings
  - target-company extraction from the documents
  - claim ledger, disclosure-diff, candidate generation, hypothesis, falsification, counter-evidence search and composition
- **Never:**
  - any per-company prompt, rule, metric or expected answer
- We demonstrate a **cold mode** on request: cache disabled for the target, with longer latency. This is how we answer "is anything precomputed?"

---

## Q. Live Demo Strategy

### Q1. Execution and latency budget (target company, warm cache)

| Stage | Budget | Degradation if exceeded |
|---|---|---|
| Resolve + route | 5 s | Default to the generic archetype |
| Delta acquisition | 60 s | Use the cached corpus; mark "data as of <date>" |
| Extraction + reconciliation | 120 s | Fall back to XBRL-only quarters plus the reconciled subset |
| Baselines (panel, claims, diff, mirror) | 60 s | Skip the mirror; claims from the last 6 calls only |
| Candidates | 5 s | — |
| Hypotheses (top 6) | 40 s | Top 4 |
| Falsification + counter-search | 90 s | Deterministic AE tests only; web counter-search marked "not run" |
| Compose + render | 30 s | Template-only text |
| **Total** | **~6.5 min p50; hard cap 9 min** | |

### Q2. Reliability engineering
- **Snapshot and replay mode:**
  - the corpus snapshot is identified by hash
  - LLM calls are cached by input hash at temperature 0
  - the same snapshot reproduces the same output exactly
  This is legitimate reproducibility, not hard-coding: the same mode works for every company.
- **Redundancy:** NSE → BSE → cache for documents; two search providers; two LLM providers or models.
- **Prepared fallbacks:** a recorded full run on 3 companies (video) in case the network fails; say so openly if it is used.
- **Thin-data guard:** for JioFin-like cases (short history), the system *says* "insufficient history for temporal claims" and switches emphasis to cross-sectional, promise-ledger and mirror evidence, with strength capped at Moderate. Honesty here scores robustness points.
- **Prompt-injection guard:** PDF text is treated as data. Extraction prompts are schema-bound, and imperative text inside documents is ignored (also tested in §V).

### Q3. Demo choreography
Ask the judges to pick the company at **minute 0**. Start the run, and present the thesis and architecture while the **live funnel** streams. Reveal the output at about minute 6–7.

---

## R. Round 1 Strategy (≤2 pages; aim for 1 dense page + 1 visual page)

**Page 1: the idea (text + 1 diagram)**
1. **Title line:** "<Team> · Track A · An expectation-breach discovery engine for Indian financials."
2. **The insight (2 sentences):** the "computed, not retrieved" thesis plus "survives being explained away".
3. **Why existing approaches fail (3 bullets):**
   - summarisers and RAG can only find what's already written
   - dashboards show headline ratios, not decomposed drivers against peers and narrative
   - LLM "critics" argue but don't test
4. **Mechanism diagram:** a triangle (Self · Peers · Narrative) → breaches → falsification battery → discovery, with the funnel numbers.
5. **Workflow (one line per stage):** Resolve → Acquire (exchange filings, regulator, rating agencies) → Extract & reconcile → Baselines → Candidates → Hypotheses with corollaries → Falsify → Score → Render.
6. **Generalisation:** archetype router (bank / NBFC / insurer / generic), driven by regulatory reporting formats; no company-specific logic; peer universe beyond NIFTY; benchmark on held-out and non-NIFTY companies.

**Page 2: proof it is real (visual-heavy)**
1. **Output mock:** a dashboard screenshot (from the MVP) showing the 8 elements, the timeline swimlanes and a lineage drawer.
2. **Falsification table:** the 9 AE types × tests (compact).
3. **Evidence rules:** tiers, families and the strength rule (3 lines).
4. **Stack (1 line):** Python, DuckDB, XBRL + PDF parsing, FTS5, LLM (extraction and reasoning, temperature 0, cached), React + pdf.js.
5. **Build plan:** 4 milestones to 25 Oct.
6. **Benchmark plan:** held-out companies plus **time-travel backtests**.

**Omit:** organiser research, buzzwords, agent counts, long data-source lists, investment language.

**Attach the MVP video (≤2 min), cut as follows:**
- 0–15 s: pick a company
- 15–60 s: funnel streaming
- 60–100 s: discovery + click-through to a highlighted PDF line
- 100–120 s: falsification table + rejected candidates

---

## S. Finals Strategy (10 min + 15 min Q&A)

| Time | Content |
|---|---|
| 0:00–0:30 | "Pick any Track A company." Start the run live. |
| 0:30–2:00 | The thesis: computed, not retrieved; expectation breach; survive falsification. |
| 2:00–4:30 | Architecture, narrated against the **live funnel** (candidates appearing, peers loading, AE tests passing or failing). |
| 4:30–8:30 | Output walkthrough: discovery sentence → numbers (**invite the judge to click any number**) → timeline swimlanes (narrative vs numbers, visibility gap) → strongest counterargument (the surviving AE) → falsification condition → strength rule → **rejected candidates and why**. |
| 8:30–10:00 | Proof of generality: benchmark table (held-out plus non-NIFTY) and one **time-travel backtest** ("as of <date>, the system ranked the precursor #k"). |

**Q&A prep: hostile questions and answers**
1. *"Why is this non-obvious?"* It is not stated by management (claim ledger shows it), not prominent in the press (coverage search), it needs ≥2 documents plus peer data to compute, and it sat in filings for N quarters before coverage (visibility gap).
2. *"Couldn't a Bloomberg-style dashboard show this?"* A dashboard shows the GNPA ratio. It does not decompose the change into flows, residualise against 8 peers, align it with 8 calls of management attributions, or test 9 alternative explanations.
3. *"Where exactly did this number come from?"* Click it: formula → inputs → page and passage → archived PDF hash.
4. *"What would disprove this?"* The falsification condition, with thresholds and dates, plus the mechanism-kill clause.
5. *"Isn't this just sector-wide?"* Show the AE1 result and the peer chart.
6. *"Multiple testing?"* Ranking heuristics, not p-values; joint gates; the published funnel.
7. *"Is anything company-specific?"* The metric library is archetype-level (any bank). Show the YAML, and offer to run on a non-NIFTY bank right now.
8. *"Did you precompute?"* The pre-indexing policy, and cold mode.
9. *"Why should we trust LLM extraction?"* XBRL first, reconciliation checks, unreconciled numbers never headline, and the measured extraction accuracy from the benchmark.
10. *"What if the LLM anchors on its first hypothesis?"* Top-K hypotheses are tested in parallel, the scoring is deterministic, and the LLM doesn't choose the winner.
11. *"Correlation vs causation?"* We claim *association + mechanism + survived alternatives*, never proof. The difference-vs-peers design around dated events is the strongest causal evidence available with public data.
12. *"What if the company changed its business model?"* The regime detector splits the series and the report says so.

---

## T. Red-Team Analysis

| Attack | Severity | Response |
|---|---|---|
| "It's just a ratio screen with an LLM on top." | High | **Fix and explain.** The screen is the *candidate generator*. Discovery requires the narrative gap, corroboration across families, and survival of falsification. Show a rejected high-z candidate killed by AE1 or AE3. |
| "An archetype metric library is company-specific tuning." | Medium | **Accept and explain.** It is sector domain knowledge defined by regulatory formats and applies identically to ~35 banks. Show it running on a non-NIFTY bank. |
| "Over-engineered for 17 days." | High | **Simplify.** The MVP is bank + NBFC modules with M1+M2+S1+S2 and a minimal M3 (KPI disappearance and new-note detection only). M4 and insurers come later; the generic module covers the rest. No graph DB, no vector DB, no swarm. |
| "PDF extraction will break live." | High | **Fix.** XBRL first (recent 6 quarters exact); pre-extracted peers; reconciliation; cache fallback; stage deadlines. |
| "Undocumented NSE/BSE endpoints might block you." | Medium | **Fix.** Dual exchange mirror, warm cache, low request volume, static archive URLs. |
| "BSE / JioFin / Bajaj Finserv break your archetypes." | Medium | **Accept partially.** The generic module (universal identities, claim ledger, disclosure-diff, shareholding, rating actions) plus the thin-data honesty guard. A specific BSE angle (derivatives revenue dependence vs SEBI F&O rule dates) comes free from the generic identities and the regulatory calendar. Rehearse all 12. |
| "Big banks are over-analysed; nothing you find is new to experts." | Medium | **Accept and explain.** The brief defines novelty against dashboards and summarisers. We also *measure* novelty (claim ledger, coverage, visibility gap) and demote known stories. |
| "LLM still hallucinates mechanisms." | Medium | **Fix.** Mechanisms must cite IDs and produce computable corollaries, and a failed corollary downgrades the hypothesis. Prose is written after scoring and contains no digits. |
| "Too slow." | Medium | **Fix.** About 6 minutes, overlapped with the presentation; stage caps. |
| "Hard to explain in 10 minutes." | Medium | **Simplify the story** to three words: *Expect · Breach · Survive*. |
| "Easy to copy." | Low | Not within 17 days. The moat is execution quality: reconciliation, the AE battery and benchmark evidence. |
| "Bad data in, confident output out." | Medium | Gates G1, G4 and AE7 make data errors visible, and the report states unreconciled items. |
| "Small-sample statistics are meaningless." | Medium | **Accept and explain.** Ranking heuristics, joint gates, specification curves, and honesty in Q&A. |
| "What if no candidate survives?" | Medium | **Accept.** Report the best Moderate or Weak finding *with explicit strength*, plus the rejected list. Honesty beats a forced story, and the brief's own example is Moderate. |

**Removed for not increasing discovery quality:** Neo4j/knowledge graph; vector DB as the core; multi-agent personas; debate; MCTS planner; sentiment scores (replaced by attribution and attention measures, which are more specific); alt-data; fine-tuning.

---

## U. Build Roadmap (today 8 Oct → Round 1 on 19 Oct → Finals on 25 Oct)

Assumes 2–4 people. **Critical path: S1 (numbers), then M1 (panel), then S2 (falsification), then the UI.**

| Phase | Dates | Deliverable | Technical work | Risk | Acceptance criteria |
|---|---|---|---|---|---|
| **0 Validate** | 8–9 Oct | Data-access report; benchmark split | Hit NSE/BSE endpoints for 3 banks + 1 NBFC; confirm XBRL availability and taxonomy; confirm transcripts are in announcements; fetch 2 rating rationales; RBI series download; verify every "(verify)" item here; **freeze practice set** (HDFC Bank, Axis, Bajaj Finance) vs **holdout** (ICICI, SBI, Kotak, Shriram + non-NIFTY: e.g. Federal Bank, AU SFB, IDFC First, Cholamandalam, IndusInd) | Endpoint blocking | 5 years of docs retrievable for 4 companies in under 10 min |
| **1 Ingest** | 9–12 Oct | Doc store + facts for banks/NBFCs | Crawler + cache; XBRL parser; PDF table extraction (results, NPA movement, segments); reconciliation rules; unit/period normalisation; merger discontinuity flag | Table extraction quality | ≥98% of headline facts correct on 3 practice companies (hand-checked); reconciliation pass rate ≥90% |
| **2 Discovery core** | 11–15 Oct | M1 panel + M2 ledger + M3-lite + candidate ranking | Bank and NBFC YAML libraries (~60–80 nodes each); robust stats; peer panel (8 peers); claim extraction schema; promise scoring; KPI-disappearance and new-note diff | Ontology mapping errors | Top-10 candidates on practice companies judged "economically meaningful" by team review ≥7/10 |
| **3 Provenance** | 13–16 Oct | Lineage DAG + PDF highlight viewer | IDs everywhere; page PNG renders with bbox; lineage API | bbox accuracy | Any number → passage in ≤2 clicks |
| **4 Falsification** | 14–17 Oct | AE1–AE8 deterministic + AE9 bounded search + strength rule | Specification curve; DiD vs peers around calendar events; coverage search; corollary executor | Corollary expressiveness | At least one practice candidate correctly *rejected* by AE1/AE3; strength labels reproducible |
| **5 Output + Round 1** | 16–19 Oct | Dashboard v1, **2-min video**, **Round 1 PDF** | 8-element template with node refs; timeline swimlanes; funnel; PDF export | Polish vs. time | Submit by **18 Oct night** (one day buffer) |
| **6 Evaluate** | 19–22 Oct | Benchmark report | Run on all holdouts + non-NIFTY + time-travel backtests; error analysis | Weak results | ≥70% of holdout runs yield ≥Moderate discovery with 100% correct headline numbers |
| **7 Harden** | 20–23 Oct | Insurer module, generic module, BSE/JioFin rehearsal; latency | Insurer YAML (APE mix, VNB margin, persistency, bancassurance concentration, EV walk); generic identities; stage deadlines; caching; failover | Scope creep | All 12 NIFTY Track A names complete in ≤9 min |
| **8 Demo prep** | 23–25 Oct | Rehearsed 10-minute script, Q&A bank, failure drills | 5 full dress rehearsals with random company draws; network-kill drill; backup video | Nerves, network | 5/5 rehearsals succeed live |

**Minimum system that proves the core hypothesis (by 15 Oct):** for a bank, the NPA-flow + funding + profitability panel vs 8 peers, plus the claim ledger from 8 calls, produces at least one candidate that survives AE1/AE3/AE5 and is not stated by management.

---

## V. Evaluation Benchmark

### V1. Test set
- **Practice (may tune generic code):** HDFC Bank, Axis Bank, Bajaj Finance.
- **Holdout NIFTY:** ICICI Bank, SBI, Kotak, Shriram Finance, HDFC Life, SBI Life, Bajaj Finserv, Jio Financial, BSE.
- **Holdout non-NIFTY (tie-break simulation):** e.g. Federal Bank, IDFC First, AU SFB, Bank of Baroda, IndusInd, Cholamandalam, M&M Finance, LIC Housing, ICICI Pru Life.
- **Time-travel backtests** (system run "as of" a date before public revelation, using only documents with `known_at` earlier than that date). Candidate events, **all to be verified in Phase 0**:
  - IndusInd Bank's derivative-accounting discrepancy disclosure (early 2025)
  - RBI business restrictions on Bajaj Finance's eCOM/Insta EMI card (Nov 2023)
  - RBI restrictions on Kotak's digital onboarding (Apr 2024)
  - IIFL Finance gold-loan restrictions (Mar 2024)
  - the microfinance stress cycle visible in bank MFI books (2024)
  - historical divergence disclosures (e.g. Yes Bank, FY16–FY17)

  **The question is *not* "did it predict the event"** (that would overclaim). It is: did the top-10 candidates as of the earlier date include the precursor metric, e.g. MFI-segment slippage or a reconciliation anomaly?

### V2. Metrics

| Dimension | Metric | Target |
|---|---|---|
| Evidence correctness | Hand-audit 30 random numbers per report against the source passage | Headline 100%; overall ≥98% |
| Calculation correctness | Unit tests on every formula; reconciliation pass rate | 100% of tests; ≥90% pass |
| Source quality | Share of evidence by tier; families per discovery | ≥2 families always; ≥3 in ≥50% |
| Temporal correctness | Change-point quarter and first-visible date checked by hand | ≥90% |
| Discovery novelty | **Blind A/B:** our output vs a strong baseline (frontier "deep research" agent given the same company and the brief's 8-element template), rated by 2–3 finance students on non-obviousness and evidence | Win rate ≥70% |
| Contradiction handling | Planted conflicts (deck vs results) surfaced | 100% |
| Falsification quality | Adversarial cases correctly demoted (below) | ≥90% |
| Reproducibility | Same snapshot run 5× → identical top discovery | 5/5 |
| Generalisation | Holdout + non-NIFTY: ≥Moderate discovery with correct numbers | ≥70% |
| Latency | p50 / p95 | ≤6.5 / ≤9 min |

### V3. Adversarial cases
1. **Sector-wide shock:** system-wide NIM compression in a rate-cut cycle. Must be labelled sector-wide (AE1), not discovered.
2. **Merger discontinuity:** HDFC Bank around July 2023. A loan-growth spike must not be reported (AE3).
3. **Restatement:** an as-reported vs restated mismatch is handled.
4. **Thin history:** JioFin/BSE. Must trigger the honest-capping guard.
5. **Missing quarter / corrupted PDF:** degrades gracefully.
6. **Conflicting numbers:** a news article contradicts the filing. The filing wins and the conflict is flagged.
7. **Planted fake or syndicated news:** collapsed by family or deduplication; never counted.
8. **Prompt injection inside a PDF** ("ignore previous instructions…"): ignored.
9. **Regulatory-event confound:** the Nov 2023 risk-weight change. The NBFC funding-mix shift must be tested against peers (AE2) before being attributed to the company.

---

## W. Final Winning Thesis

Most teams will build a research *assistant*: agents that search, read and summarise, then ask themselves for counterarguments. Their discoveries will be whatever the documents already say, and their evidence will be URLs.

We build a research *instrument*. It computes what a company's own history, its peers and its management lead us to expect, finds where reality persistently breaks those expectations, and then tries hard to explain each break away using a pre-registered battery of data tests. It reports only what survives, with every number traceable to a highlighted line in a public filing and the rejected hypotheses on display.

That maps one-to-one onto the judging criteria:
- **Discovery:** computed breaches.
- **Novelty:** measured by narrative gap and visibility gap.
- **Temporal:** bitemporal facts, change points and narrative lead/lag.
- **Cross-source:** independent families.
- **Falsifiability:** the AE battery plus corollaries.
- **Explainability:** click-through lineage plus the funnel.
- **Robustness:** peer residualisation and specification curves.
- **Generality:** archetype libraries derived from regulatory formats, tested on held-out and non-NIFTY companies.

Track A is where Indian public disclosure is most standardised and independent evidence is most plentiful, which is where this mechanism is strongest. It also aligns with what a finance-club panel led by a practising research head is most equipped to appreciate (inference).

---

## Appendix 1 — Organizer & Judge Research

**[F] Facts**
- **Economics Association, BITS Hyderabad:** the official student body for M.Sc. Economics. Its signature ATMOS events are Courtroom, Arthashastra (business quiz) and finance workshops. Its flagship conclave **Finnovate** has run since 2017; it also hosts guest lectures and a student blog (BITS Hyderabad Economics page).
- **ATMOS:** the techno-management festival of BITS Hyderabad, founded 2012. The 2024 edition ran 8–10 Nov 2024 and included hackathons (ETV Bharat, Adda247). No public page for "Finding the Next Signal" or ATMOS 2026 was found.
- **The Wall Street Club, BITS Hyderabad:** no public web presence was found in searches. We cannot say anything verified about its prior events.
- **Vinit Bolinjkar:** Head of Research at **Ventura Securities**, Mumbai; 20+ years in equity research; leads the firm's research and daily market calls. His personal site frames his approach as **geo-economic** (oil, trade, currencies, geopolitics → Indian markets), **"valuation-first and contrarian"**, and "**signal over noise**". He runs a newsletter named "Signal vs Noise", cites a "12 Dimensions valuation framework" (contents not public), and his recent topics include Indian IT and AI disruption and the data-centre build-out. His media commentary covers CPI and RBI policy (InvestmentGuru India). Ventura's research team published on the Sep 2026 NIFTY rejig (BSE replacing Wipro).
- **Unverified:** a search-engine summary of his LinkedIn mentioned free valuation spreadsheets covering NIFTY 50, banking/financial and consumer stocks. **This could not be confirmed on a primary page; do not cite it.**

**[I] Inferences (the evidence is stated in each)**
- The event title "Finding the Next **Signal**" echoes his "signal vs noise" vocabulary, so the framing likely reflects the prize partner's thinking. Our language should be about *signal separated from noise*, measured explicitly; the funnel *is* that.
- A geo-economic, macro-aware research head will likely test whether a finding is really macro or regulatory. Our AE2 (regulatory/macro shock, difference vs peers) answers this directly.
- "Valuation-first, contrarian, avoid hype" suggests sensitivity to buzzword architectures and a preference for the materiality of a finding (impact on earnings or book). Hence the Materiality component and the "not judging number of agents" emphasis.
- The organisers being finance and economics student bodies suggests judges comfortable with banking metrics, which supports Track A and its deeper scrutiny.

**[H] Speculation** (do not rely on it): other panel members may include Ventura analysts or BITS faculty; tie-break companies may be mid-caps.

## Appendix 2 — Key regulatory facts used (with sources)
- **XBRL:** results must be filed via NSE "Integrated Filing–Financial" XBRL from 1 Apr 2025, the same day as the PDF; PDF Quick Results were discontinued (NSE circular NSE/CML/2025/20, 2 Apr 2025). The governance XBRL is due 30 days after quarter-end.
- **Earnings calls (LODR Reg 46(2)(oa)):** audio/video recordings are due promptly (before the next trading day or within 24 h); transcripts within 5 working days (SEBI 2021 per Money9; company filings cite Reg 46(2)(oa)). Check the current consolidated text.
- **RBI divergence disclosure** is triggered when additional provisioning exceeds 10% of reported profit before provisions and contingencies, or additional GNPA exceeds 15% of published incremental GNPA (RBI, 1 Apr 2019). The disclosure goes in the notes to accounts, and SEBI requires it to accompany annual results.
- **Risk weights:** RBI raised risk weights on bank exposures to NBFCs (+25 pp where the rating-based weight was below 100%) in Nov 2023, and reversed that from 1 Apr 2025. Consumer credit remains at 125% (Business Standard; Khaitan).
- **Co-Lending Arrangements Directions 2025:** issued 6 Aug 2025, effective 1 Jan 2026. Each partner retains a minimum of 10%; discretionary CLM-2 ended (Vinod Kothari; Mondaq).
- **NBFC funding:** bank borrowings rose to ~43% of NBFC funding in FY26, projected ~45% in FY27 (CRISIL via KNN, Apr 2026).
- **Pillar 3:** banks publish quarterly regulatory disclosures. RBI proposed an expanded uniform Pillar 3 in May 2026; LCR/NSFR move into Pillar 3 from Q1 FY28 per an Aug 2026 amendment (Vinod Kothari; Angel One).
- **BRSR Core "openness of business":** concentration of purchases and sales with trading houses, dealers and related parties is mandatory; coverage widens to the top 1000 listed entities in FY27 (KPMG; GreenSutra).
- **NIFTY 50:** BSE Ltd replaced Wipro effective 30 Sep 2026 (NSE Indices press release, 10 Aug 2026). There were no changes in the Mar 2026 review.
- **Lazy Prices:** changes in periodic-filing language predict future earnings, news and returns; investors are inattentive (Cohen, Malloy, Nguyen, J. Finance 75(3), 2020).
- **LLM confirmation bias:** LLM agents tend to propose confirming rather than falsifying tests; prompting for counterexamples improved rule discovery from 42% to 56% (arXiv 2604.02485, 2026). This motivates *data-test* falsification rather than prompt-only critics.
- **FinanceBench:** retrieval-augmented frontier models of 2023 failed or refused most of a 150-question sample (arXiv 2311.11944). This motivates XBRL-first, reconciliation-verified numbers.

## Appendix 3 — Archetype driver libraries (v0, to be completed in Phase 2)

These are archetype-level formulas only. Nothing here names a company.

**Bank**
- **Growth:** advances by segment (retail sub-products, agri, MSME, corporate; secured vs unsecured); deposits (CASA, retail TD, bulk); CD ratio and *incremental* CD ratio.
- **Margins:** yield on advances, cost of deposits, NIM; RoA tree (NII, fees, opex, credit cost, tax, all as a share of average assets).
- **Asset-quality flows:** slippages ÷ opening advances, upgrades, recoveries, write-offs, recoveries from written-off accounts. GNPA/NNPA, PCR, lagged GNPA (t−4, t−8), write-off-adjusted GNPA, restructured book, segment GNPA.
- **Capital & liquidity:** CET1, RWA density (RWA ÷ assets), LCR, NSFR.
- **Concentration:** top-20 depositors, borrowers and NPAs.
- **Compliance:** PSL achievement, PSLC trades (verify the disclosure), divergence note, RBI penalties.
- **Claims:** guidance on growth, NIM, credit cost and CD ratio.

**NBFC / HFC**
- **AUM:** by product; on-book vs off-book (DA, securitisation, co-lending); disbursement ÷ AUM (implied runoff).
- **Borrowing mix:** banks, NCD, CP, ECB, securitisation, deposits; cost of funds; ALM buckets; liquidity buffer.
- **Asset quality:** Stage 1/2/3 shares and ECL coverage (Stage 2 as a leading indicator); write-offs; collection efficiency.
- **Profitability & capital:** NIM, opex ÷ AUM, credit cost, RoA, leverage.
- **Mirror (rating rationales):** top-lender concentration, liquidity commentary.
- **Events:** RBI actions; dated regulatory events (risk weights Nov 2023 → Apr 2025; Co-Lending Directions Jan 2026).

**Life insurer**
- **Business:** APE by product (ULIP, par, non-par, protection, annuity); channel mix with bancassurance concentration (mirror against the parent bank's distribution disclosures).
- **Value:** VNB and margin; EV walk (unwind + VNB + operating variance + economic variance), which is an identity.
- **Quality:** persistency (13th/61st month), commission ratio, surrender ratio, solvency.
- **External & events:** IRDAI monthly new-business data (verify); IRDAI rule dates such as surrender-value norms (verify date).

**Generic (holdco / exchange / any company)**
- **Universal identities:** revenue by segment, margin bridge, working capital, cash conversion, debt and leverage.
- **Governance & ownership:** related-party share, auditor changes and qualifications, shareholding drift (promoter, pledge, FII/DII), rating actions, KMP changes.
- **Holdco:** look-through to listed subsidiaries.
- **Exchange:** revenue by segment, own and industry turnover data, and SEBI rule dates.

**Illustrative discovery shapes (fictional; to show form, not real findings)**
- *Bank:* "GNPA ratio improved by X bps over N quarters, but ≥Y% of the reduction came from write-offs, while the gross slippage ratio rose and the peer median was flat. Management attributed the improvement to collections in K of the last M calls."
- *NBFC:* "Off-book share (DA + co-lending) rose from A% to B% in the four quarters after the Nov 2023 risk-weight increase, about 2× the peer median shift. A rating rationale shows bank term-loan share falling over the same window. Management described funding as 'diversified' throughout."
- *Insurer:* "VNB margin expansion is fully explained by product-mix shift to non-par, not by the improving persistency management highlighted. Bancassurance share via the parent rose to Z%, raising single-channel dependence."

## Sources
- Participant brief (attached .docx), primary source of truth
- NIFTY 50 constituents: https://en.wikipedia.org/wiki/NIFTY_50
- NIFTY rejig Aug 2026 (BSE replaces Wipro): https://niftyindices.com/Press_Release/ind_prs10082026.pdf · https://www.venturasecurities.com/news/indian-markets/bse-replaces-wipro-in-nifty-50-as-nse-announces-major-index-rejig/ · https://www.5paisa.com/news/bse-to-join-nifty-50-wipro-to-exit-from-september-30-in-index-rejig
- NIFTY Mar 2026 review (no change): https://niftyindices.com/Press_Release/ind_prs23022026.pdf
- Sector weights: https://www.bajajamc.com/knowledge-centre/nifty-50-sector-weightage · https://stockmojo.in/index-weightage/nifty
- Vinit Bolinjkar: https://vinitbolinjkar.com/ · https://in.linkedin.com/in/vinitbolinjkar · https://investmentguruindia.com/newsdetail/quote-on-cpi-data-by-vinit-bolinjkar--head-of-research-at-ventura-securities-271088
- Economics Association BITS Hyderabad: https://id.bits-pilani.ac.in/hyderabad/Economics/Economics
- ATMOS: https://en.wikipedia.org/wiki/ATMOS_(festival) · https://www.etvbharat.com/en/!technology/atmos-2024-tech-fiesta-bits-pilani-hyderabad-campus-enn24110705487
- NSE XBRL / Integrated Filing: https://ca2013.com/wp-content/uploads/2025/04/NSE-Circular_02.04.2025.pdf · https://ca2013.com/wp-content/uploads/2025/04/NSE_Circular_Integrated-Filing-Governance_01.04.2025.pdf · https://www.nseindia.com/companies-listing/corporate-filings-financial-results
- BSE data licensing and community libraries: https://www.bseindia.com/market_data_products.html?flag=eod · https://pypi.org/project/bse · https://bselib.readthedocs.io/
- Earnings-call disclosure: https://money9.com/news/equities/sebi-asks-listed-cos-to-make-analyst-call-recording-public-in-24-hours-19397.html
- RBI divergence disclosure: https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=11521 · https://archives.nseindia.com/content/equities/SEBI_Circular_31102019.pdf
- Risk weights: https://khaitanco.com/thought-leadership/relief-for-NBFCs-and-Microfinance-Institutions · https://www.business-standard.com/amp/finance/news/nbfc-funding-strategy-rbi-regulations-bank-loans-2025-125031100586_1.html
- Co-lending 2025: https://vinodkothari.com/2025/08/rbi-issues-co-lending-directions-2025/ · https://www.mondaq.com/india/fund-finance/1679822/rbis-2025-co-lending-regime-balancing-prudence-growth-and-protection
- Rating rationales (example): https://www.crisil.com/mnt/winshare/Ratings/RatingList/RatingDocs/IncredFinancialServicesLimited_December%2031_%202024_RR_360289.html · https://www.icra.in/Rating/ShowRationalReportFilePdfViewer/144002
- NBFC funding mix: https://knnindia.co.in/news/newsdetails/sectors/financefintech/nbfcs-to-rely-more-on-bank-borrowings-in-fy27-amid-softer-lending-rates-crisil-ratings
- Pillar 3: https://vinodkothari.com/2026/08/rbi-amends-pillar-3-to-require-disclosure-of-liquidity-risks-and-measures/ · https://www.angelone.in/news/economy/rbi-proposes-stricter-basel-pillar-3-disclosures-on-capital-and-risk-for-banks · https://www.rbl.bank.in/investor-relations/regulatory/basel-capital-instruments-lcr-disclosures
- RBI DBIE / sectoral credit: https://website.rbi.org.in/web/rbi/-/press-releases/sectoral-deployment-of-bank-credit-december-2016-39420 · https://website.rbi.org.in/documents/87730/39710577/83889.pdf
- BRSR Core: https://assets.kpmg.com/content/dam/kpmg/in/pdf/2023/07/firstnotes-sebi-framework-on-brsr-core-value-chain-disclosures-assurance-by-listed-entities.pdf · https://greensutra.in/question/brsr-core-openness-of-business/
- Screener ToS: https://www.screener.in/guides/terms
- FDA data (Track D): https://www.fda.gov/about-fda/performance-data/fda-data-dashboard · https://www.fda.gov/science-research/health-informatics-fda/openfda
- CEA (Track B): https://cea.nic.in/monthly-installed-capacity-report/?lang=en · https://cea.nic.in/wp-content/uploads/resd/2026/04/Broad_Overview_of_RE_Generation_March_2026.pdf
- Lazy Prices: https://www.nber.org/papers/w25084
- LLM confirmation bias: https://www.alphaxiv.org/abs/2604.02485
- FinanceBench / financial QA hallucination: https://www.alphaxiv.org/abs/2311.11944v1 · https://papers.nips.cc/paper_files/paper/2025/hash/b8badadce3f482ba340ff870f4894441-Abstract-Datasets_and_Benchmarks_Track.html
- Financial AI product landscape: https://cryptobriefing.com/rogo-arr-triples-50m-surpasses-hebbia/ · https://allmind.ai/research/best-ai-tools-equity-research-2026 (vendor-authored; treat with caution)
