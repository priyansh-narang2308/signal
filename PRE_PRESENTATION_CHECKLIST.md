# SIGNAL — Pre-Presentation Pre-Flight Checklist
**Event:** Signal Hackathon Finals  
**Format:** 10 Minutes Total (5 Minutes Presentation + 5 Minutes Q&A)  
**Presenter:** Priyansh (Solo)  
**Track:** Track A (Banking, NBFCs & Financial Services)

---

## 1. Quick Pre-Flight Command (Run This 15 Mins Before Call)

Open your terminal in `~/Developer/finding-next` and execute:

```bash
# 1. Warm the cache for banks (fetches real public filings so on-the-spot run is instantaneous)
python3 engine/cli.py prefetch bank

# 2. Ensure both primary research dossier reports are compiled
python3 engine/export_report.py KOTAKBANK
python3 engine/export_report.py AXISBANK

# 3. Start the live engine server
python3 engine/server.py
```

Leave this terminal window open. You will see:
```text
SIGNAL live server  →  http://127.0.0.1:8765
```

---

## 2. Verify Server & Reports (30-Second Sanity Check)

Open a second terminal tab and verify that everything responds with HTTP 200:

```bash
# Health check (must return {"ok": true, "mode": "live", "offline": false})
curl -s http://127.0.0.1:8765/api/health

# Verify Final Output Report is live
curl -s -I http://127.0.0.1:8765/api/report/KOTAKBANK
```

---

## 3. Browser Setup (Have These Exact Tabs Ready)

Close all other apps, Slack, WhatsApp, and notifications. Keep your screen clean.

Set up your browser with these **3 tabs**:

| Tab # | Target | URL / App | Purpose |
| :--- | :--- | :--- | :--- |
| **Tab 1** | **Slide Deck** | Slides 1–6 (Keynote / PPT / PDF) | The 2-minute intro (Problem, Pipeline, Falsification) |
| **Tab 2** | **Live Engine** | `http://127.0.0.1:8765` | Interactive dashboard showing 8-stage pipeline & discovery |
| **Tab 3** | **Final Report** | `http://127.0.0.1:8765/api/report/KOTAKBANK` | The **Final Output Dossier Report** requested by organizers |

---

## 4. The 5-Minute Pitch Strategy (2 Mins Slides + 3 Mins Live Product)

Organizers explicitly stated:
> *"Focus on demonstrating what you have built rather than just explaining it."*
> *"Keep one report ready as your final output. You will also be asked to generate a report on the spot."*

Do **NOT** spend 4 minutes on slides! Follow this timing:

```text
[0:00 - 2:00]  Slides 1–6 (Crisp, high-conviction architecture overview)
[2:00 - 2:45]  Show Live Prototype: Ingest, Funnel & Audit Trail (Tab 2)
[2:45 - 3:30]  Show Final Output: The Kotak Bank Research Dossier (Tab 3)
[3:30 - 4:30]  Live On-The-Spot Generation: Run AXISBANK live in ~10s (Tab 2)
[4:30 - 5:00]  Wrap up, impact, and invite Q&A
[5:00 - 10:00] Q&A (Technical defence)
```

---

## 5. Live On-The-Spot Demo Instructions (When Judges Ask)

When judges say: *"Can you generate a report on the spot for another company?"*

1. Switch to **Tab 2** (`http://127.0.0.1:8765/#/research`).
2. In the input box, type: `AXISBANK` (or `ICICIBANK`).
3. Click **`RUN RESEARCH →`**.
4. Point at the screen while it runs:
   - *"Look at the live 8-stage execution..."*
   - *"Ingesting NSE filings, parsing XBRL tags, testing 143 candidate breaches..."*
   - *"Running 7 pre-registered falsification tests as code..."*
5. Within ~10–12 seconds, the screen will show: **`Discovery ready.`**
6. Click **`View Dossier Report ↗`**.
7. A new tab opens with the publication-grade research report dossier for Axis Bank!

---

## 6. Emergency Offline Fallback (If Hackathon Wi-Fi Dies)

If the conference or home Wi-Fi drops completely during your turn, don't panic:
SIGNAL has an automatic fallback to local cached filings.

In terminal:
```bash
export SIGNAL_OFFLINE=1
python3 engine/server.py
```
Everything will continue to run and generate reports instantly using the local bitemporal cache without calling external NSE endpoints.
