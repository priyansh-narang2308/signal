# SIGNAL — Round 1 submission package

**Finding the Next Signal · ATMOS 2026 · Track A — Banking, NBFCs & Financial Services**

SIGNAL is an autonomous financial research system with one organising idea: **computed, not retrieved.**

- **Expectations:** it builds three — the company's own history, same-archetype peers in the same quarter, and management's stated narrative.
- **Breaches:** it investigates where the numbers persistently break those expectations.
- **Reporting:** a breach is reported only after it survives a pre-registered falsification battery.
- **Provenance:** every number in the output resolves to formula → inputs → document → page → passage.

The full strategy is in `../../STRATEGY.md`.

## What is in this folder

| Path | What it is |
|---|---|
| `pdf/TheBlacklisted_TrackA_Round1.pdf` | The Round 1 solution brief: 2 A4 pages. The earlier, denser version is kept in `pdf/backup/`. |
| `prototype/` | Interactive HTML prototype: `index.html`, `styles.css`, `script.js`, local fonts in `assets/`. |
| `screenshots/` | Screenshot states 01–07, captured at 1440×900 @2x. |
| `video/SIGNAL_Demo.mp4` | The demo film, 1920×1080, 30 fps, 119 s, with burned-in subtitles. |
| `video/SIGNAL_Demo_clean.mp4` | The same film without subtitles. |
| `video/SIGNAL_Demo.srt` / `.vtt` | Subtitle files. |
| `video/narration.wav`, `video/music.wav` | The narration stem and the score/sound-design stem. |
| `source/` | Everything needed to rebuild the deliverables (below). |

## Honesty note — read this before presenting

- **The prototype is a front-end simulation.** It replays a *synthetic* research run.
- **No figure in the prototype, PDF or video is a real finding** about HDFC Bank or any other company. Peers are labelled A–H. Page references and document renders are marked as illustrative.
- **The synthetic NPA data reconciles exactly** (opening + slippages − upgrades − recoveries − write-offs = closing, in every quarter), so the example obeys the same rules the real system enforces.
- **Benchmark targets are targets.** The PDF and the prototype label them as planned. Nothing claims measured accuracy.
- **The company input shows HDFC Bank, but outputs refer to "the subject bank".** This keeps synthetic numbers from being read as a claim about a real company.

## Run the prototype

Open `prototype/index.html` in Chrome; it works from `file://`. Or serve the folder:

```bash
cd submission && python3 -m http.server 8765
```

Then visit `http://127.0.0.1:8765/prototype/index.html`.

**Flow:** Research → **RUN RESEARCH** (a 14 s simulated run with stages, funnel and rejected candidates) → **Open discovery** → click any underlined claim or number to open its evidence trail. Then **Falsification**, then **Methodology → Generalization**.

**URL modes:**
- `?static=1` renders every state fully revealed. Used for screenshots.
- `?video=1` exposes a deterministic control API, `window.SIGNAL`, which the film uses.

## Rebuild the deliverables

Requires Node, Python 3 and ffmpeg. Start a server from `submission/` with `python3 -m http.server 8765`, then:

| Step | Command (run from `source/`) | Output |
|---|---|---|
| Screenshots + PDF crops | `node tools/shoot.js` | `screenshots/`, `source/crops/` |
| PDF | `node tools/render_pdf.js "The Blacklisted"` | `pdf/TheBlacklisted_TrackA_Round1.pdf` |
| Narration (Kokoro) | `cd video && python3 tts.py <dir with kokoro-v1.0.onnx + voices-v1.0.bin>` | `lines/*.wav` |
| Cues + narration track | `python3 cues.py` | `cues.json`, `.srt`, `.vtt`, `narration.wav` |
| Frames | `node frames.js <framesDir> 30` | 3,570 JPEG frames; also writes `sfx.json` |
| Score + mix | `python3 music.py` | `music.wav`, `mix.wav` |
| Subtitle overlays | `node subs.js ../review/cues` | one PNG per cue |
| Encode | `./encode.sh <framesDir>` | final MP4s in `../../video/` |

`tools/` pins `playwright@1.54`. The scripts point at a local "Chrome for Testing" build; edit the `CHROME` path at the top of each script if yours differs.

## Audio provenance and licensing

- **Narration** is Kokoro-82M (ONNX build `kokoro-onnx`, voice `af_heart`), an open-weight Apache-2.0 text-to-speech model. Model files come from the `thewh1teagle/kokoro-onnx` GitHub releases.
- **Music and sound design** are generated procedurally by `video/music.py`: synthesised pads, filtered noise ticks, a sub pulse and a synthetic reverb. They are original to this submission, with no samples and no third-party tracks, so there is nothing to license.
- **Fonts:**
  - Inter, Source Serif 4 and JetBrains Mono, all under the SIL Open Font License.
  - Bundled from `@fontsource`.

## Before you submit

1. **Set the team name.** Run `node tools/render_pdf.js "<Team>"`. The PDF currently says "Team Name".
2. **Rename the PDF** to `<TeamName>_TrackA_Round1.pdf`, as the brief requires.
3. **Prepare the optional MVP upload.** The brief asks for a GitHub link plus a ≤2-minute video. `SIGNAL_Demo.mp4` is 1:59.
4. **Label the repo honestly.** If you push this folder as the MVP repo, say clearly in its README that the current build is a UI prototype on simulated data.
