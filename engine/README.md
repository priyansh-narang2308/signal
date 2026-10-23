# SIGNAL live engine

This engine runs SIGNAL for real on any NSE-listed financial company. It:

- fetches the company's quarterly XBRL filings, plus those of same-archetype peers;
- computes the driver metrics;
- finds persistent breaches of the company's own history and of its peers;
- runs the falsification tests as code;
- shows the 8 required elements in the dashboard.

It needs nothing installed beyond Python 3, because it uses only the standard library. The written text comes from a free OpenRouter model. That part is optional: without an API key, a deterministic template writes the text instead.

## Start it
```
cd ~/Developer/finding-next
python3 engine/server.py
```
Open http://127.0.0.1:8765, type a symbol (for example ICICIBANK, SBIN or BAJFINANCE) and click **RUN RESEARCH**.

## Free text model (optional)
Create a file called `engine/.env` containing your key:
```
OPENROUTER_API_KEY=sk-or-...
```
The engine tries free models in this order: llama-3.3-70b, deepseek-chat, gemma-3, mistral-small, qwen-2.5. To use different ones, add a line like `OPENROUTER_MODELS=model1:free,model2:free`.

## Command line
```
python3 engine/cli.py probe AXISBANK    # check NSE access and which XBRL tags were mapped
python3 engine/cli.py run ICICIBANK     # full run in the terminal
python3 engine/cli.py prefetch bank     # download filings for all banks ahead of time (do this before the finals)
```

## What is real and what isn't built yet
**Real, computed live:**
- fetching the filings and parsing the XBRL
- the metric library for banks, NBFCs and other financial companies
- the expected range from the company's own history
- the peer comparison, persistence and the change point
- these tests: AE1 sector-wide, AE2 RBI policy dates, AE3 discontinuity, AE4 denominator, AE5 window sensitivity, AE7 reconciliation, AE8 testable consequence
- the strength rule
- the evidence trail, with links to the filings

**Not in this build:** AE6 (checking earnings-call transcripts) and AE9 (web search for contradicting evidence). The dashboard shows both as NOT RUN.
