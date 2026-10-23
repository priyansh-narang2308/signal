"""Expect · Breach · Survive — the deterministic core.

Every number in the output is computed here. No language model is involved.
"""
import datetime as dt
import math
import statistics as st

from . import library

WINDOW = 4


# ---------------------------------------------------------------- helpers
def _med(xs):
    xs = [x for x in xs if x is not None]
    return st.median(xs) if xs else None


def _mad(xs, m):
    xs = [x for x in xs if x is not None]
    return st.median([abs(x - m) for x in xs]) if xs else 0.0


def _q(xs, p):
    xs = sorted(x for x in xs if x is not None)
    if not xs:
        return None
    k = (len(xs) - 1) * p
    lo, hi = math.floor(k), math.ceil(k)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def _logistic(x):
    return 1 / (1 + math.exp(-x))


def _d(s):
    return dt.date.fromisoformat(s)


def _floor(kind):
    return 2.0 if kind == "growth" else 0.05


def series(records, metric):
    """{period_end: value} for one company and one metric."""
    lv = {}
    for r in records:
        try:
            v = metric["f"](r["raw"])
        except (KeyError, ZeroDivisionError, TypeError):
            v = None
        if v is not None and math.isfinite(v):
            lv[r["end"]] = v
    if metric["kind"] != "growth":
        return lv
    out = {}
    for end, v in lv.items():
        d = _d(end)
        for end0, v0 in lv.items():
            if abs((d - _d(end0)).days - 365) <= 10 and v0 and v0 > 0 and v is not None:
                out[end] = 100 * (v / v0 - 1)
    return out


def raw_series(records, canon):
    return {r["end"]: r["raw"][canon] for r in records if canon in r["raw"]}


def op_income_series(records):
    out = {}
    for r in records:
        x = r["raw"]
        if all(k in x for k in ("interest_earned", "interest_expended", "other_income")):
            out[r["end"]] = x["interest_earned"] - x["interest_expended"] + x["other_income"]
    return out


# ---------------------------------------------------------------- tests
def test_sector(t_change, peer_changes):
    valid = [c for c in peer_changes.values() if c is not None]
    if len(valid) < 3:
        return "partial", "only %d peers with comparable data" % len(valid), None
    co = [c for c in valid if c * t_change > 0 and abs(c) >= 0.5 * abs(t_change)]
    share = len(co) / len(valid)
    res = "%d of %d peers moved the same way" % (len(co), len(valid))
    if share >= 0.6:
        return "fail", res + " — sector-wide", share
    if share >= 0.35:
        return "partial", res + " — partly sector-wide", share
    return "pass", res + " — company-specific", share


def test_regulatory(cp_end, co_share):
    if not cp_end:
        return "pass", "no change point to align with events", []
    d = _d(cp_end)
    near = [(e, txt) for e, txt in library.SECTOR_EVENTS if -200 <= (d - _d(e)).days <= 45]
    if not near:
        return "pass", "no dated sector event within ±1 quarter of the change point", []
    if co_share is not None and co_share >= 0.35:
        return "partial", "%s near the change point and peers co-moved" % near[-1][1], near
    return "pass", "%s near the change point, but peers did not move — not event-driven" % near[-1][1], near


def test_discontinuity(size_series, cp_end, quarters):
    jumps = []
    keys = [q for q in quarters if q in size_series]
    for a, b in zip(keys, keys[1:]):
        va, vb = size_series[a], size_series[b]
        if va and va > 0 and abs(vb / va - 1) > 0.30:
            jumps.append(b)
    if not jumps:
        return "pass", "no discontinuity in scale (no quarter-on-quarter jump > 30%)", jumps
    if cp_end and any(abs((_d(j) - _d(cp_end)).days) <= 100 for j in jumps):
        return "fail", "scale jump at %s coincides with the change point (merger / reclassification?)" % jumps[0], jumps
    return "pass", "scale jump at %s, outside the breach window" % jumps[0], jumps


def test_denominator(metric, records, win, pre, ratio_dir):
    if metric["kind"] == "growth":
        return "n/a", "growth metric — no denominator", None
    num = metric.get("num")
    if not num:
        return "n/a", "ratio reported directly; no numerator series tagged", None
    ns = raw_series(records, num) if num != "op_income" else op_income_series(records)
    if metric["id"] in ("gnpa_pct", "nnpa_pct") and num in ("gnpa_amt", "nnpa_amt"):
        ns = raw_series(records, num)
    nw, np_ = _med([ns.get(q) for q in win]), _med([ns.get(q) for q in pre])
    if nw is None or not np_:
        return "n/a", "numerator not available in tagged facts", None
    g = nw / np_ - 1
    txt = "numerator (%s) %+.0f%% vs pre-window" % (num.replace("_", " "), 100 * g)
    if abs(g) < 0.03:
        return "partial", txt + " — ratio move is mostly the denominator", g
    if g * ratio_dir > 0:
        return "pass", txt + " — moves with the ratio", g
    return "fail", txt + " — opposite to the ratio: denominator-driven", g


def test_window(vals, quarters, main_sign, floor):
    hold = total = 0
    for w in (2, 3, 4, 5):
        if len(quarters) < w + 3:
            continue
        win, rest = quarters[-w:], quarters[:-w]
        for pre in (rest, rest[-4:]):
            pv = [vals[q] for q in pre if q in vals]
            wv = [vals[q] for q in win if q in vals]
            if len(pv) < 2 or not wv:
                continue
            m = _med(pv)
            sc = max(1.4826 * _mad(pv, m), 0.05 * abs(m), floor / 2)
            z = (_med(wv) - m) / sc
            total += 1
            if z * main_sign > 0 and abs(z) >= 1:
                hold += 1
    if not total:
        return "partial", "too few quarters for a specification curve", 0
    share = hold / total
    txt = "holds in %d of %d window specifications" % (hold, total)
    if share >= 0.75:
        return "pass", txt, share
    if share >= 0.5:
        return "partial", txt, share
    return "fail", txt, share


def test_integrity(records, arche):
    ok = n = 0
    name = None
    for r in records:
        for nm, fn in library.IDENTITIES.get(arche, []):
            res = fn(r["raw"])
            if res is None:
                continue
            name = nm
            lhs, rhs = res
            n += 1
            tol = max(abs(rhs) * 0.03, abs(lhs) * 0.03, 1.0)
            if abs(lhs - rhs) <= tol:
                ok += 1
    if not n:
        return "partial", "identity not computable from tagged facts; values as reported", (0, 0, None)
    txt = "%s reconciles in %d / %d quarters" % (name.split(":")[0], ok, n)
    if ok / n >= 0.8:
        return "pass", txt, (ok, n, name)
    if ok / n >= 0.5:
        return "partial", txt, (ok, n, name)
    return "fail", txt, (ok, n, name)


# ---------------------------------------------------------------- main
def analyse(target, records, peers, arche):
    """target: symbol; records: target quarter records; peers: {sym: records}."""
    lib = library.METRICS.get(arche, library.METRICS["generic"])
    quarters = [r["end"] for r in records][-16:]
    labels = {r["end"]: r["label"] for r in records}
    recmap = {r["end"]: r for r in records}
    size_canon = next((c for c in ("interest_earned", "revenue", "total_income") if any(c in r["raw"] for r in records)), None)
    size_series = raw_series(records, size_canon) if size_canon else {}
    integ = test_integrity(records, arche)

    checks = breaches = 0
    cands, rejected = [], []
    for m in lib:
        tv = series(records, m)
        q = [x for x in quarters if x in tv]
        if len(q) < WINDOW + 2:
            continue
        win, pre = q[-WINDOW:], q[:-WINDOW]
        pv = [tv[x] for x in pre]
        med_pre = _med(pv)
        floor = _floor(m["kind"])
        scale = max(1.4826 * _mad(pv, med_pre), 0.05 * abs(med_pre), floor / 2)
        band = (med_pre - 2 * scale, med_pre + 2 * scale)
        med_win = _med([tv[x] for x in win])
        self_z = (med_win - med_pre) / scale
        sign = 1 if med_win >= med_pre else -1

        ps = {s: series(recs, m) for s, recs in peers.items()}
        peer_med, peer_q1, peer_q3, resid = {}, {}, {}, []
        for x in q:
            vals = [p[x] for p in ps.values() if x in p]
            if len(vals) >= 3:
                peer_med[x], peer_q1[x], peer_q3[x] = _med(vals), _q(vals, .25), _q(vals, .75)
        out_self = [x for x in win if (tv[x] - band[1] if sign > 0 else band[0] - tv[x]) > 0]
        rsign = 0
        out_peer = []
        if all(x in peer_med for x in win):
            resid = [tv[x] - peer_med[x] for x in win]
            rsign = 1 if _med(resid) >= 0 else -1
            out_peer = [x for x in win if (tv[x] > peer_q3[x] if rsign > 0 else tv[x] < peer_q1[x])]
            iqr = _med([peer_q3[x] - peer_q1[x] for x in win]) or floor
            peer_z = _med(resid) / max(iqr / 1.349, floor / 2)
        else:
            peer_z = 0.0
        checks += 2 * len(win)
        breaches += len(out_self) + len(out_peer)

        # change point: first quarter after which values stay on the breach side of the own band
        cp = None
        for i, x in enumerate(q):
            if all((tv[y] - band[1] if sign > 0 else band[0] - tv[y]) > -0.5 * scale for y in q[i:]) and i >= len(pre) - 2:
                cp = x
                break
        if cp is None:
            cp = (out_self or out_peer or win)[0]
        peer_changes = {}
        for s, p in ps.items():
            a = [p[x] for x in pre if x in p]
            b = [p[x] for x in win if x in p]
            peer_changes[s] = (_med(b) - _med(a)) if len(a) >= 2 and len(b) >= 2 else None

        c = dict(metric=m, values=tv, quarters=q, win=win, pre=pre, med_pre=med_pre, med_win=med_win,
                 band=band, scale=scale, self_z=self_z, sign=sign, peer_med=peer_med, peer_q1=peer_q1,
                 peer_q3=peer_q3, peer_z=peer_z, rsign=rsign, out_self=out_self, out_peer=out_peer, cp=cp,
                 peer_series=ps, peer_changes=peer_changes)
        if not out_self and not out_peer:
            continue
        cands.append(c)

    funnel = {"checks": checks, "breaches": breaches, "metrics": len(cands)}
    stage = {"valid": [], "corrob": [], "specific": [], "survived": []}
    for c in cands:
        m = c["metric"]
        persist = max(len(c["out_self"]), len(c["out_peer"]))
        tests = {}
        tests["AE7"] = integ
        tests["AE3"] = test_discontinuity(size_series, c["cp"], c["quarters"])
        if persist < 2 or tests["AE3"][0] == "fail" or integ[0] == "fail":
            why = "single-quarter blip" if persist < 2 else ("discontinuity in scale" if tests["AE3"][0] == "fail" else "numbers do not reconcile")
            rejected.append((c, "Structural validity", why))
            continue
        stage["valid"].append(c)
        if not (len(c["out_self"]) >= 2 and len(c["out_peer"]) >= 2 and c["rsign"] == c["sign"]):
            rejected.append((c, "Corroboration", "breach visible against %s only" % ("own history" if len(c["out_self"]) >= 2 else "peers")))
            continue
        stage["corrob"].append(c)
        tests["AE1"] = test_sector(c["med_win"] - c["med_pre"], c["peer_changes"])
        if tests["AE1"][0] == "fail":
            rejected.append((c, "Peer residualisation · AE1", tests["AE1"][1]))
            continue
        stage["specific"].append(c)
        tests["AE2"] = test_regulatory(c["cp"], tests["AE1"][2])
        tests["AE4"] = test_denominator(m, records, c["win"], c["pre"], c["sign"])
        tests["AE5"] = test_window(c["values"], c["quarters"], c["sign"], _floor(m["kind"]))
        tests["AE8"] = corollary(c, records, peers, arche)
        c["tests"] = tests
        fails = [k for k in ("AE2", "AE4", "AE5") if tests[k][0] == "fail"]
        if fails:
            rejected.append((c, "Falsification · " + fails[0], tests[fails[0]][1]))
            continue
        stage["survived"].append(c)

    for c in cands:
        c.setdefault("tests", {"AE7": integ})
        c["score"] = score(c)
        c["strength"], c["strength_why"] = strength(c)

    pool = stage["survived"] or stage["specific"] or stage["corrob"] or stage["valid"] or cands
    ranked = sorted(pool, key=lambda c: c["score"], reverse=True)
    funnel.update(valid=len(stage["valid"]), corrob=len(stage["corrob"]), specific=len(stage["specific"]),
                  survived=len(stage["survived"]), discovery=1 if stage["survived"] else 0)
    return {"ranked": ranked, "rejected": rejected, "funnel": funnel, "labels": labels, "quarters": quarters,
            "integrity": integ, "recmap": recmap, "fallback_level": None if stage["survived"] else
            ("specific" if stage["specific"] else "corrob" if stage["corrob"] else "valid" if stage["valid"] else "candidate" if cands else None)}


def corollary(c, records, peers, arche):
    """AE8: a consequence not used to build the hypothesis — profitability vs peers should diverge in the
    direction implied by the breach (adverse breach → weaker profit growth than peers)."""
    m = c["metric"]
    if m["id"] == "pat_yoy":
        return "n/a", "breach is itself the profit metric", None
    pm = next((x for x in library.METRICS.get(arche, library.METRICS["generic"]) if x["id"] == "pat_yoy"), None)
    if not pm:
        return "n/a", "no profit series", None
    tv = series(records, pm)
    pvs = {s: series(r, pm) for s, r in peers.items()}
    diffs = []
    for q in c["win"]:
        vals = [p[q] for p in pvs.values() if q in p]
        if q in tv and len(vals) >= 3:
            diffs.append(tv[q] - _med(vals))
    if len(diffs) < 2:
        return "n/a", "profit growth not comparable across peers", None
    adverse = (c["sign"] > 0) == (m["bad"] == "up")
    d = _med(diffs)
    expect = -1 if adverse else 1
    txt = "profit growth %+.1f pp vs peer median in the window" % d
    if d * expect > 0:
        return "pass", txt + " — consistent", d
    return "partial", txt + " — not yet visible in profit", d


def score(c):
    t = c.get("tests", {})
    vals = {"pass": 1.0, "partial": 0.5, "fail": 0.0}
    run = [vals[v[0]] for v in t.values() if v[0] in vals]
    survival = sum(run) / len(run) if run else 0.5
    persist = max(len(c["out_self"]), len(c["out_peer"])) / WINDOW
    parts = [_logistic(abs(c["self_z"]) - 1.5), _logistic(abs(c["peer_z"]) - 1.0), max(persist, 0.05), max(survival, 0.05)]
    gm = math.exp(sum(math.log(p) for p in parts) / len(parts))
    adverse = (c["sign"] > 0) == (c["metric"]["bad"] == "up")
    return gm * (1.15 if adverse else 1.0)


def strength(c):
    t = c.get("tests", {})
    verdicts = [v[0] for v in t.values()]
    fails = verdicts.count("fail")
    partials = verdicts.count("partial")
    ps, pp = len(c["out_self"]), len(c["out_peer"])
    if fails == 0 and partials <= 1 and ps >= 3 and pp >= 3 and t.get("AE7", ("",))[0] == "pass" and "AE1" in t:
        return "STRONG", "no test failed, %d partial; outside own band %d/4 and peer IQR %d/4 quarters; numbers reconcile" % (partials, ps, pp)
    if fails == 0 and partials <= 2 and max(ps, pp) >= 2 and "AE1" in t:
        return "MODERATE", "no test failed, %d partial; persistence %d/4 quarters" % (partials, max(ps, pp))
    return "WEAK", "%d failed, %d partial; persistence %d/4 — reported only as the best available candidate" % (fails, partials, max(ps, pp))
