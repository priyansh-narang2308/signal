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
        print("   %s  %-10s  %d mapped  %s" % (r["end"], r["label"], len(r["raw"]), r["basis"]))


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
    elif c == "run":
        sys.exit(cmd_run(sys.argv[2].upper()))
    elif c == "prefetch":
        cmd_prefetch(sys.argv[2] if len(sys.argv) > 2 else None)
    else:
        print(__doc__)
