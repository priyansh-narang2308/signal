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

UI = os.path.join(os.path.dirname(HERE), "submission", "prototype")
RESULTS = os.path.join(HERE, "results")
os.makedirs(RESULTS, exist_ok=True)
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
        if p == "/":
            self.path = "/index.html"
        return super().do_GET()


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
