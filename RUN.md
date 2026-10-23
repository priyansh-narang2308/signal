# How to run SIGNAL

Two ways to open the dashboard. **For the finals, always use the live one.**

|                  | Live (real NSE data)           | Demo (synthetic replay)                                   |
| ---------------- | ------------------------------ | --------------------------------------------------------- |
| Start            | `python3 engine/server.py`     | double-click `submission/prototype/index.html`            |
| Open             | **http://127.0.0.1:8765**      | opens as `file://…` (or `:5500` with VS Code Live Server) |
| Badge, top-right | **LIVE · NSE FILINGS** (black) | PROTOTYPE · SIMULATION                                    |
| Company box      | editable: type any NSE symbol  | fixed: "HDFC Bank"                                        |

> If you see "HDFC Bank" that you can't edit, you're in demo mode. Go to **http://127.0.0.1:8765**.

---

## 1. Start the live dashboard

```
cd ~/Developer/finding-next
python3 engine/server.py
```

Leave this Terminal window open. Then open **http://127.0.0.1:8765** in Chrome.

Type a symbol (for example `ICICIBANK`) and click **RUN RESEARCH**. When it finishes, click **Open discovery** and click any underlined number to see its filing.

To stop the server, press `Ctrl + C` in that Terminal window.

## 2. Before the finals: download filings ahead of time (one-off, about 15–20 min)

The first run of a company downloads about 100 filings (the company plus 6 peers), which takes 1–3 minutes. Do it ahead of time so any company the judges pick runs in seconds:

```
python3 engine/cli.py prefetch bank
python3 engine/cli.py prefetch nbfc
```

Then do a test run on a few companies:

```
python3 engine/cli.py run AXISBANK
python3 engine/cli.py run SBIN
python3 engine/cli.py run BAJFINANCE
```

## 3. Symbols the judges might pick (Track A)

| Banks                                                             | NBFCs / HFCs                               | Others                        |
| ----------------------------------------------------------------- | ------------------------------------------ | ----------------------------- |
| HDFCBANK, ICICIBANK, SBIN, KOTAKBANK, AXISBANK, INDUSINDBK        | BAJFINANCE, SHRIRAMFIN, JIOFIN             | BAJAJFINSV, HDFCLIFE, SBILIFE |
| Tie-break: FEDERALBNK, IDFCFIRSTB, AUBANK, BANKBARODA, PNB, CANBK | Tie-break: CHOLAFIN, MUTHOOTFIN, LICHSGFIN | BSE, CDSL                     |

Banks and NBFCs give the richest output. Insurers and BSE use the generic library, which has fewer metrics.

## 4. Free text model (optional)

Without a key, a built-in template writes the text, and everything else is identical. To use a free model instead:

```
echo "OPENROUTER_API_KEY=sk-or-YOURKEY" > engine/.env
```

Then restart the server.

## 5. If something goes wrong

| Problem                                | Fix                                                                                                    |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| "address already in use"               | A server is already running. Use it, or run `PORT=8766 python3 engine/server.py` and open :8766        |
| Run stuck at INGEST for over 3 minutes | NSE is slow or blocking. Press Ctrl+C, wait 30 seconds, start again; cached companies still work       |
| "only N usable quarterly filings"      | The company has too little XBRL history (new listing). Pick another, or explain the thin-history guard |
| Page looks old                         | Press Cmd + Shift + R                                                                                  |
| Need the safe fallback                 | Open `index.html` directly: the synthetic demo, labelled as such                                       |

## 6. Command line reference

```
python3 engine/cli.py probe AXISBANK   # check NSE access and which facts were read
python3 engine/cli.py run ICICIBANK    # full run printed in the terminal
python3 engine/cli.py prefetch bank    # download filings ahead of time (bank | nbfc | insurer | generic)
```
