"""SIGNAL local server — serves the dashboard and runs live research jobs.

    python3 engine/server.py            # then open http://127.0.0.1:8765
"""
import json
import os
import sys
import threading
import urllib.parse
import uuid
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from signal_live import library, run  # noqa: E402
import export_report

UI = os.path.join(os.path.dirname(HERE), "submission", "prototype")
RESULTS = os.path.join(HERE, "results")
REPORTS = export_report.REPORTS_DIR
os.makedirs(RESULTS, exist_ok=True)
os.makedirs(REPORTS, exist_ok=True)
JOBS = {}


def _start(symbol):
    jid = uuid.uuid4().hex[:10]
    job = run.Job(symbol)
    JOBS[jid] = job

    def work():
        run.execute(job)
        if job.result:
            with open(os.path.join(RESULTS, job.symbol.upper() + ".json"), "w", encoding="utf-8") as f:
                json.dump(job.result, f)
            try:
                export_report.generate_html_report(job.symbol)
            except Exception as e:
                sys.stderr.write(f"  Report export error: {e}\n")
    threading.Thread(target=work, daemon=True).start()
    return jid


class H(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=UI, **k)

    def log_message(self, fmt, *args):
        try:
            line = fmt % args
        except Exception:
            line = f"{fmt} {args}"
        if "/api/job/" not in line:
            sys.stderr.write("  " + line + "\n")

    def _json(self, obj, code=200):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def end_headers(self):
        if self.path.endswith((".js", ".css", ".html")) or self.path == "/":
            self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(u.query)
        p = u.path
        if p.startswith("/.well-known/"):
            return self._json({}, 404)
        if p == "/api/health":
            return self._json({"ok": True, "mode": "live", "offline": os.environ.get("SIGNAL_OFFLINE") == "1"})
        if p == "/api/universe":
            return self._json([{"symbol": s, "name": n, "archetype": a} for s, (n, a) in library.UNIVERSE.items()])
        if p == "/api/run":
            sym = (qs.get("symbol") or [""])[0].strip().upper()
            if not sym:
                return self._json({"error": "symbol required"}, 400)
            return self._json({"job": _start(sym)})
        if p.startswith("/api/job/"):
            job = JOBS.get(p.rsplit("/", 1)[-1])
            if not job:
                return self._json({"error": "unknown job"}, 404)
            try:
                since = int((qs.get("since") or ["0"])[0])
            except (ValueError, TypeError):
                since = 0
            st = job.state(since)
            if job.done and job.result:
                st["result"] = job.result
            return self._json(st)
        if p.startswith("/api/cached/"):
            sym = p.rsplit("/", 1)[-1].upper()
            path = os.path.join(RESULTS, sym + ".json")
            if os.path.exists(path):
                with open(path, encoding="utf-8") as f:
                    return self._json(json.load(f))
            return self._json({"error": "no cached result"}, 404)
        if p.startswith("/api/report/"):
            sym = p.rsplit("/", 1)[-1].upper()
            rep_path = os.path.join(REPORTS, f"{sym}_RESEARCH_DOSSIER.html")
            if not os.path.exists(rep_path):
                rep_path = export_report.generate_html_report(sym)
            if rep_path and os.path.exists(rep_path):
                with open(rep_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Cache-Control", "no-store")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
            return self._json({"error": f"no report for {sym}"}, 404)
        if p.startswith("/reports/"):
            fname = os.path.basename(p)
            fpath = os.path.join(REPORTS, fname)
            if os.path.exists(fpath):
                with open(fpath, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Cache-Control", "no-store")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
            return self._json({"error": "report not found"}, 404)
        if p in ("/view/filing", "/api/filing"):
            furl = (qs.get("url") or [""])[0].strip()
            if not furl:
                return self._json({"error": "url parameter required"}, 400)
            try:
                from signal_live import nse, xbrl
                raw = nse.xbrl(furl)
                parsed = xbrl.parse(raw)
                mapped = library.map_facts(parsed.get("facts", {}))
                html = self._render_filing_inspector(furl, parsed, mapped)
                body = html.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Cache-Control", "no-store")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            except Exception as e:
                return self._json({"error": f"Failed to inspect filing: {e}"}, 500)
        if p == "/":
            self.path = "/index.html"
        return super().do_GET()

    def _render_filing_inspector(self, url, parsed, mapped):
        from signal_live import xbrl
        period = parsed.get("period_end", "Unknown")
        basis = xbrl.basis(parsed) or "Standalone"
        facts = parsed.get("facts", {})
        LABEL_MAP = {
            "interest_earned": "Interest Earned (Gross)",
            "interest_expended": "Interest Expended (Interest Expense)",
            "other_income": "Other / Non-Interest Income",
            "total_income": "Total Income",
            "opex": "Operating Expenses",
            "employee": "Employee Cost",
            "provisions": "Provisions & Contingencies",
            "pbt": "Profit Before Tax (PBT)",
            "pat": "Profit After Tax (PAT / Net Profit)",
            "gnpa_amt": "Gross Non-Performing Assets (GNPA Amount)",
            "gnpa_pct": "Gross NPA Ratio (%)",
            "nnpa_amt": "Net Non-Performing Assets (NNPA Amount)",
            "nnpa_pct": "Net NPA Ratio (%)",
            "car": "Capital Adequacy Ratio (CAR / CET1 %)",
            "roa": "Return on Assets (ROA %)",
        }
        def fmt_val(k, v):
            if "pct" in k or k in ("car", "roa"):
                return f"{v:.2f}%"
            cr = v / 10000000.0
            return f"₹{cr:,.2f} cr ({v:,.0f})"
        rows_mapped = "".join(f"""
        <tr>
            <td style="font-weight:600; padding:10px 14px; border-bottom:1px solid #e5e7eb;">{LABEL_MAP.get(k, k.replace('_', ' ').title())}</td>
            <td style="text-align:right; font-family:ui-monospace,SFMono-Regular,monospace; font-weight:700; padding:10px 14px; border-bottom:1px solid #e5e7eb;">{fmt_val(k, v)}</td>
            <td style="font-family:ui-monospace,SFMono-Regular,monospace; color:#6b7280; font-size:11px; padding:10px 14px; border-bottom:1px solid #e5e7eb;">{tag}</td>
        </tr>
        """ for k, (v, tag) in sorted(mapped.items()))
        rows_all = "".join(f"""
        <tr>
            <td style="font-family:ui-monospace,SFMono-Regular,monospace; font-weight:600; padding:6px 12px; border-bottom:1px solid #f3f4f6; font-size:12px;">{k}</td>
            <td style="text-align:right; font-family:ui-monospace,SFMono-Regular,monospace; padding:6px 12px; border-bottom:1px solid #f3f4f6; font-size:12px;">{f'{v:,.2f}' if isinstance(v, (int, float)) else str(v)}</td>
        </tr>
        """ for k, v in sorted(facts.items()))
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>SIGNAL — Official Regulatory Filing Inspector</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: #f9fafb; color: #111827; margin: 0; padding: 32px 48px; font-size: 13px; }}
  .card {{ background: #fff; border: 1px solid #e5e7eb; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-bottom: 24px; padding: 24px; }}
  .head {{ display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 2px solid #111827; padding-bottom: 16px; margin-bottom: 20px; }}
  .title {{ font-size: 18px; font-weight: 800; letter-spacing: 0.05em; }}
  .sub {{ font-size: 12px; color: #6b7280; margin-top: 4px; }}
  .badge {{ display: inline-block; background: #111827; color: #fff; padding: 3px 8px; font-size: 10px; font-weight: 700; border-radius: 4px; text-transform: uppercase; margin-left: 8px; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 12px; }}
  th {{ background: #f3f4f6; text-align: left; padding: 10px 14px; font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; color: #4b5563; border-bottom: 2px solid #e5e7eb; }}
  .btn {{ display: inline-flex; align-items: center; gap: 6px; background: #111827; color: #fff; padding: 8px 14px; font-size: 11px; font-weight: 600; text-decoration: none; border-radius: 4px; border: 1px solid #111827; }}
  .btn-outline {{ background: #fff; color: #111827; border: 1px solid #d1d5db; }}
  .btn:hover {{ opacity: 0.9; }}
</style>
</head>
<body>
<div class="card">
  <div class="head">
    <div>
      <div class="title">REGULATORY FILING INSPECTOR <span class="badge">Audited XBRL</span></div>
      <div class="sub">National Stock Exchange of India (NSE) Corporate Filing Archives</div>
    </div>
    <div style="display: flex; gap: 10px;">
      <a class="btn btn-outline" href="{url}" target="_blank" rel="noopener">Download Raw NSE XML ↗</a>
      <a class="btn" href="javascript:window.close()">Close Window</a>
    </div>
  </div>

  <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; background: #f9fafb; padding: 14px 18px; border-radius: 6px; border: 1px solid #e5e7eb; margin-bottom: 24px;">
    <div><div style="font-size:10px; font-weight:700; color:#6b7280; text-transform:uppercase;">Period End</div><div style="font-family:ui-monospace,monospace; font-size:14px; font-weight:700; margin-top:2px;">{period}</div></div>
    <div><div style="font-size:10px; font-weight:700; color:#6b7280; text-transform:uppercase;">Reporting Basis</div><div style="font-family:ui-monospace,monospace; font-size:14px; font-weight:700; margin-top:2px;">{basis}</div></div>
    <div><div style="font-size:10px; font-weight:700; color:#6b7280; text-transform:uppercase;">Mapped Metrics</div><div style="font-family:ui-monospace,monospace; font-size:14px; font-weight:700; margin-top:2px;">{len(mapped)} canonical facts</div></div>
    <div><div style="font-size:10px; font-weight:700; color:#6b7280; text-transform:uppercase;">Total Tagged Facts</div><div style="font-family:ui-monospace,monospace; font-size:14px; font-weight:700; margin-top:2px;">{len(facts)} disclosures</div></div>
  </div>

  <h3 style="font-size: 13px; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 10px 0;">Audited Financial Statement Items (Normalized &amp; Reconciled)</h3>
  <table>
    <thead>
      <tr>
        <th style="width: 35%;">Financial Metric</th>
        <th style="width: 35%; text-align: right;">Audited Canonical Value</th>
        <th style="width: 30%;">Underlying Exchange XBRL Tag</th>
      </tr>
    </thead>
    <tbody>
      {rows_mapped}
    </tbody>
  </table>
</div>

<details class="card">
  <summary style="font-weight: 700; cursor: pointer; font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; color: #4b5563;">
    View All {len(facts)} Raw Tagged Facts Extracted from Instance Document ▾
  </summary>
  <table style="margin-top: 16px;">
    <thead>
      <tr>
        <th style="width: 60%;">Tag Identifier</th>
        <th style="width: 40%; text-align: right;">Reported Value</th>
      </tr>
    </thead>
    <tbody>
      {rows_all}
    </tbody>
  </table>
</details>
</body>
</html>
"""

    def do_HEAD(self):
        return self.do_GET()


def main():
    port = int(os.environ.get("PORT", "8765"))
    srv = ThreadingHTTPServer(("127.0.0.1", port), H)
    print("\n  SIGNAL live server  →  http://127.0.0.1:%d\n  (Ctrl+C to stop)\n" % port)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
