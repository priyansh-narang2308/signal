"""SIGNAL command line.

    python3 engine/cli.py run ICICIBANK        # full live run, prints the discovery
    python3 engine/cli.py probe AXISBANK       # check NSE access + show which tags were found
    python3 engine/cli.py prefetch             # warm the cache for the whole Track A universe
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from signal_live import library, nse, panel, run, xbrl  # noqa: E402


def cmd_probe(sym):
    print("1) NSE session ...", end=" ", flush=True)
    nse.warm()
    print("ok")
    print("2) filings list ...", end=" ", flush=True)
    rows = nse.filings(sym)
    print("%d rows" % len(rows))
    if rows:
        print("   keys:", ", ".join(sorted(rows[0].keys()))[:400])
    urls = [nse.find_xbrl_url(r) for r in rows]
    urls = [u for u in urls if u]
    print("   rows with an XBRL link: %d" % len(urls))
    if not urls:
        print("   first row:", json.dumps(rows[0])[:600] if rows else "-")
        return
    print("3) first XBRL ...", urls[0])
    p = xbrl.parse(nse.xbrl(urls[0]))
    print("   period end %s · %d numeric facts · basis %s" % (p["period_end"], len(p["facts"]), xbrl.basis(p) or "?"))
    mapped = library.map_facts(p["facts"])
    print("   mapped canonical facts:")
    for k, (v, t) in sorted(mapped.items()):
        print("     %-18s %-55s %s" % (k, t, v))
    unm = [n for n in p["facts"] if n not in {t for _, t in mapped.values()}]
    print("   unmapped tags (first 60):", ", ".join(sorted(unm)[:60]))
    print("4) panel ...")
    recs = panel.build(sym)
    for r in recs:
        print("   %s  %-10s  %2d mapped  %-12s %s" % (r["end"], r["label"], len(r["raw"]), r["basis"], r["url"].rsplit("/", 1)[-1][:60]))
    if recs:
        print("5) newest quarter mapped facts (%s):" % recs[-1]["label"])
        for k, v in sorted(recs[-1]["raw"].items()):
            print("     %-18s %-50s %s" % (k, recs[-1]["tags"][k], v))


def cmd_rows(sym):
    """Diagnose filings that have no recognised XBRL link (e.g. Integrated Filings)."""
    import urllib.parse
    nse.warm()
    rows = nse.filings(sym)
    no = [r for r in rows if not nse.find_xbrl_url(r)]
    print("%d rows, %d without a recognised XBRL link" % (len(rows), len(no)))
    print("\nNEWEST 3 ROWS (full):")
    def key(r):
        d = panel._row_period_end(r)
        return d.isoformat() if d else ""
    for r in sorted(rows, key=key, reverse=True)[:3]:
        print(json.dumps(r)[:900])
        print("-")
    s = urllib.parse.quote(sym)
    cands = [
        "/api/integrated-filing-results?index=equities&symbol=%s" % s,
        "/api/integrated-filing-results?index=equities&symbol=%s&period=Quarterly" % s,
        "/api/corporates-integrated-filing?index=equities&symbol=%s" % s,
        "/api/integrated-filing-financials?index=equities&symbol=%s" % s,
        "/api/corporate-integrated-filing?index=equities&symbol=%s" % s,
        "/api/corporates-financial-results?index=equities&symbol=%s&period=Quarterly&type=Integrated%%20Filing-%%20Financials" % s,
        "/api/results-comparision?symbol=%s" % s,
    ]
    print("\nCANDIDATE ENDPOINTS:")
    for c in cands:
        try:
            raw = nse._get(nse.BASE + c, tries=1)
            print("OK  ", c, "->", raw[:400].decode("utf-8", "replace").replace("\n", " "))
        except Exception as e:  # noqa: BLE001
            print("FAIL", c, "->", str(e)[:120])
        print()


def cmd_run(sym):
    job = run.Job(sym)
    shown = [0]

    def watch():
        while not job.done:
            for s, t, k in job.log[shown[0]:]:
                print(("\n" if k == "stage" else "   ") + t)
            shown[0] = len(job.log)
            time.sleep(0.3)
    import threading
    th = threading.Thread(target=watch, daemon=True)
    th.start()
    run.execute(job)
    time.sleep(0.5)
    for s, t, k in job.log[shown[0]:]:
        print(("\n" if k == "stage" else "   ") + t)
    if job.error:
        print("\nFAILED:", job.error)
        return 1
    d = job.result.get("discovery")
    print("\n" + "=" * 70)
    if not d:
        print(job.result.get("note"))
        return 0
    print("DISCOVERY [%s]\n%s\n" % (d["strength"], d["sentence"]))
    for w in d["why"]:
        print(" -", w)
    print("\nCounterargument:", d["counter"]["text"])
    print("Falsification:", d["falsification"])
    print("\nTests:")
    for t in job.result["tests"]:
        print("  %-4s %-8s %s" % (t[0], t[5].upper(), t[4]))
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    with open(os.path.join(HERE, "results", sym.upper() + ".json"), "w", encoding="utf-8") as f:
        json.dump(job.result, f)
    try:
        import export_report
        export_report.generate_html_report(sym)
    except Exception as e:
        print("Report export warning:", e)
    print("\nwriter:", job.result.get("writer"), "· run time %.0fs" % job.result.get("run_seconds", 0))
    return 0


def cmd_prefetch(only=None):
    syms = [s for s, (_, a) in library.UNIVERSE.items() if not only or a == only]
    for s in syms:
        t = time.time()
        try:
            r = panel.build(s)
            print("%-12s %2d quarters  (%.0fs)" % (s, len(r), time.time() - t))
        except Exception as e:  # noqa: BLE001
            print("%-12s FAILED %s" % (s, str(e)[:80]))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    c = sys.argv[1]
    if c == "probe":
        cmd_probe(sys.argv[2].upper())
    elif c == "rows":
        cmd_rows(sys.argv[2].upper())
    elif c == "run":
        sys.exit(cmd_run(sys.argv[2].upper()))
    elif c == "prefetch":
        cmd_prefetch(sys.argv[2] if len(sys.argv) > 2 else None)
    else:
        print(__doc__)
