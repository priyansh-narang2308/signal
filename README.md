# SIGNAL — Autonomous Financial Research System

> *A non-obvious finding is, almost by definition, not written down anywhere — so retrieval can only find what someone has already said. The discovery has to be **computed** across documents, and a computed anomaly is not a discovery until it has **survived a serious attempt to explain it away**.*

**ATMOS 2026 · BITS Pilani Hyderabad · Track A — Banking, NBFCs & Financial Services**

---

## What is SIGNAL?

SIGNAL is an autonomous financial research agent built for the *Finding the Next Signal* hackathon. Unlike conventional summarisers or retrieval-based tools, SIGNAL **computes** discoveries by constructing three independent expectations and investigating persistent breaches.

### The three expectations

| Expectation | Source | What it catches |
|---|---|---|
| **Self** (temporal) | Company's own decomposed history — e.g. GNPA split into slippages, upgrades, recoveries, write-offs | Breaks from the company's own trajectory |
| **Peer** (cross-section) | Same-archetype peers in the same quarter | Company-specific deviations vs. sector-wide noise |
| **Narrative** (claims) | Timestamped management guidance, analyst call promises, MD&A | Gaps between what was *said* and what *happened* |

### The discovery funnel

A breach becomes a discovery **only** after surviving four gates:

1. **Numbers reconcile** — extracted figures pass accounting-identity checks
2. **Independent corroboration** — supported by ≥2 independent source families
3. **Pre-registered falsification** — survives tests from a fixed taxonomy of alternative explanations
4. **Testable consequence** — predicts an outcome checkable in held-out data

### Provenance

Every number in the output resolves to:
```
Formula → Inputs → Document → Page → Highlighted passage
```
The LLM never types a number. Every figure is a rendered reference to a computed node.

---

## Repository structure

```
├── STRATEGY.md                  # Full strategic master document (955 lines)
├── submission/
│   ├── source/
│   │   ├── README.md            # Detailed build & run instructions
│   │   ├── crops/               # Cropped images for the PDF
│   │   ├── pdf/                 # HTML sources for the Round 1 brief
│   │   ├── review/              # Review assets and subtitle overlays
│   │   ├── tools/               # Playwright-based screenshot & PDF renderers
│   │   └── video/               # Video pipeline: TTS, music synthesis, encoding
│   ├── prototype/               # Interactive HTML/CSS/JS prototype
│   │   ├── index.html
│   │   ├── styles.css
│   │   ├── script.js
│   │   └── assets/fonts/        # Bundled open-source fonts
│   ├── pdf/                     # Final Round 1 PDF submission
│   ├── screenshots/             # 7 captured UI states (1440×900 @2x)
│   └── video/                   # Demo video, subtitles (media hosted externally)
└── .gitignore
```

---

## Run the prototype

The prototype is a self-contained HTML/CSS/JS application — no build step needed.

```bash
# Option 1: open directly
open submission/prototype/index.html

# Option 2: serve locally
cd submission && python3 -m http.server 8765
# Visit http://127.0.0.1:8765/prototype/index.html
```

**Flow:** Research → **RUN RESEARCH** (14s simulated run) → **Open discovery** → click any claim/number for evidence trail → **Falsification** → **Methodology** → **Generalization**

### URL modes

| Parameter | Effect |
|---|---|
| `?static=1` | Renders all states fully revealed (used for screenshots) |
| `?video=1` | Exposes `window.SIGNAL` control API (used by the demo film) |

---

## Rebuild deliverables

Requires **Node.js**, **Python 3**, and **ffmpeg**. See [`submission/source/README.md`](submission/source/README.md) for the full pipeline.

---

## Honesty note

- The prototype is a **front-end simulation** replaying a synthetic research run
- **No figure is a real finding** about HDFC Bank or any other company
- Synthetic NPA data reconciles exactly (the example obeys the same rules the real system enforces)
- Benchmark targets are labelled as planned, not measured

---

## Audio & font licensing

| Asset | Source | License |
|---|---|---|
| Narration | Kokoro-82M TTS (`af_heart` voice) | Apache-2.0 |
| Music & SFX | Procedurally generated (`music.py`) | Original — no samples |
| Inter, Source Serif 4, JetBrains Mono | `@fontsource` | SIL Open Font License |

---

## Team

**The Blacklisted** · ATMOS 2026
