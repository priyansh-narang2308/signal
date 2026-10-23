# Prototype walkthrough

**Time:** about 5 minutes
**Open:** `submission/prototype/index.html` in Chrome, starting on the Research screen

> **Read this first.** The prototype replays a run on a **synthetic panel.** Every screen carries an "Illustrative prototype output" label, and the header says "Prototype · simulation." The script says so once at the start, in one confident sentence. Don't present it as a live analysis of HDFC Bank. If a judge spots the label before you mention it, you lose credibility you can't get back.

---

## 1. Research screen (about 30 seconds)

_[Prototype on screen, Research tab.]_

This is SIGNAL's interface. One note before I start: what you're about to see is our **interface prototype, replaying a run on a synthetic panel.** The labels on each screen say so. It shows exactly what the system produces and how a person moves through it.

_[Point to the form.]_

You give it a company. Here that's a bank, so SIGNAL detects the **bank archetype** automatically. It sets the period (five years of quarters), builds a **panel of eight similar banks,** including some outside the NIFTY 50, and commits to the output: all eight required elements, with full provenance and **no investment recommendation.**

_[Point to the right panel.]_

On the right is what a run does, and the principle behind it: **computed, not retrieved.**

_[Click RUN RESEARCH.]_

---

## 2. The run (about 45 seconds; talk while it plays)

_[Point to the stage bar across the top.]_

Across the top are the eight stages from the slides: ingest, normalise, build expectations, find breaches, triangulate, falsify, rank and report.

_[Point to the left column.]_

On the left is the research log. Every step is written down, so a run can be **audited and replayed.**

_[Point to the middle as the funnel fills.]_

In the middle is the funnel: **143 candidates** narrowing down to **one discovery.**

_[Point to the right column.]_

And this column is the one we care most about: **rejected and retained.** Each rejected candidate shows **why** it was rejected and at **which stage.** A NIM compression was rejected because seven of eight peers moved the same way, so it's a sector story. A CASA decline was rejected because management had already disclosed it. A rise in provision coverage was rejected as a denominator effect.

**A summariser can't show you this. It doesn't know what it discarded.**

_[When "Discovery ready" appears, click Open discovery.]_

---

## 3. Discovery (about 1 minute 30 seconds)

_[Top of the Discovery page.]_

This is the discovery, in **one sentence.**

The bank's gross NPA ratio fell, which looks like an improvement. But **71% of the reduction came from write-offs,** while fresh slippages rose from 1.40% to 2.20% and peers stayed flat. And management credited **collections** in five of six calls.

_[Point to the sub-line.]_

So the improvement is real, but **it isn't what management says it is.**

_[Point to the Evidence strength card.]_

On the right is evidence strength: **Strong.** It survived eight of nine tests, has three independent source families, has persisted for five quarters, and was outside the peer range in four of four quarters. There is a **visibility gap of four quarters:** the numbers moved a year before anyone talked about it.

_[Point to the row of eight tags.]_

These tags confirm the report contains **all eight elements** the brief requires.

_[Scroll to Three expectations.]_

Here are the three expectations as charts. **Self:** history predicted about 1.4% slippage, and we're at 2.2%. **Peer:** the peer median stayed flat. **Narrative:** management kept pointing to collections, but write-offs did the work. Expected versus observed gives the **breach.**

_[Scroll to Timeline.]_

The timeline shows **when the story changed** and **when it became visible.** The numbers turned in Q1 FY26. Management's language only changed in Q1 FY27.

_[Scroll to Counterargument and Falsification condition.]_

We also report the strongest case **against** ourselves. Fast loan growth explains part of the headline: 24 of the 69 basis points. But it doesn't explain the write-off share or the rise in slippage.

And here is the **falsification condition:** what future data would make SIGNAL change its mind. It is written down in advance and checked every quarter.

_[Scroll to Evidence.]_

Finally, evidence is counted by **independent source family,** not by number of documents. Three news stories based on one press release count **once.**

---

## 4. Evidence trail (about 45 seconds)

_[Click an underlined number, or open the Evidence trail tab.]_

Any number in the report can be clicked. Take **₹14,953 crore** of fresh slippages.

_[Move down the chain.]_

First the **value.** Then the **formula,** the NPA movement identity: opening, plus slippages, minus upgrades, recoveries and write-offs, equals closing. Then the **check:** it reconciles in all six quarters. If it didn't, that number could never appear as a headline.

Then the **source document,** with its credibility tier and a hash of the archived copy. And then the **page and the highlighted passage** the number came from.

**From the claim to the exact line in the filing, in two clicks.**

---

## 5. Falsification (about 45 seconds)

_[Click the Falsification tab.]_

This is where we **try to break our own finding.**

_[Point to the "Registered / Executed" timestamps.]_

The tests are **registered before they run,** and the timestamps prove it.

_[Point down the table.]_

Each row is an alternative explanation, with the **procedure that tests it** and the result. Sector-wide effect: six of eight peers were flat, so it passes. Regulatory shock: peers barely moved around the dated events. Accounting change: none. Chosen time window: it holds in 22 of 24 window choices.

_[Point to the result box.]_

**Survived eight of nine.** The one partial is the denominator effect, and we disclosed it as the counterargument rather than hiding it.

_[Scroll to Evidence strength.]_

Strong, moderate or weak comes from a **fixed rule,** not the model's opinion.

---

## 6. Methodology and generalisation (about 30 seconds)

_[Click Methodology, then the Generalization sub-tab.]_

Last screen. Everything is defined **for a type of company, not for a specific company.** Indian banks, NBFCs and insurers report in formats the regulator prescribes, so one driver library covers **every bank, every NBFC and every insurer,** including companies outside the NIFTY 50.

_[Point to Benchmark design.]_

That's also how we evaluate it: practice companies, held-out NIFTY companies we never developed on, and non-NIFTY companies to simulate your tie-break.

---

## Close (about 15 seconds)

So that's SIGNAL. **Find the breach. Trace the evidence. Try to break the hypothesis.**

Thank you. We're happy to take your questions.

---

## If they ask "Can you run it on [another company] right now?"

Answer honestly and calmly. Don't improvise a live run with the prototype.

> "The interface you just saw replays a synthetic run to show the output. Here's exactly which parts of the pipeline run on live data today, and which are still in progress: [state your real status]. The design is the same for every bank, because the driver library is defined for the bank archetype, not for any one bank."

Before the call, agree as a team on **one honest sentence** for what is live and what isn't.
