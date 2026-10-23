"""Assemble the eight required elements + evidence trail from computed results."""
import html

from . import analyze, library, llm

AE_META = {
    "AE1": ("Sector-wide effect / peer-specificity", "“Every comparable firm moved the same way.”", "Company change vs each same-archetype peer over the same quarters; share co-moving"),
    "AE2": ("Regulatory / macro shock", "“A dated sector event caused it.”", "Change point vs dated RBI events (±1 quarter); peer co-movement around them"),
    "AE3": ("Accounting artefact / discontinuity", "“A merger or reclassification.”", "Quarter-on-quarter scale jumps > 30% near the change point"),
    "AE4": ("Denominator effect", "“The ratio moved because the base moved.”", "Numerator growth vs ratio direction, window vs pre-window"),
    "AE5": ("One-off / chosen window", "“One quarter, or a cherry-picked window.”", "Specification curve over window lengths and baselines"),
    "AE6": ("Already disclosed", "“Management already said this.”", "Claim ledger over call transcripts"),
    "AE7": ("Data integrity", "“The numbers are wrong.”", "Accounting-identity reconciliation on every quarter's tagged facts"),
    "AE8": ("Testable consequence", "“If true, something else should show it.”", "Profit growth vs peer median in the breach window (not used to build the hypothesis)"),
    "AE9": ("Counter-evidence search", "“Independent sources contradict it.”", "Bounded search of rating rationales and regulator data"),
}
NOT_RUN = {"AE6": "not run in this build — transcript ingestion is roadmap", "AE9": "not run in this build — web counter-evidence search is roadmap"}


def fmt(v, kind):
    if v is None:
        return "—"
    return ("%+.1f%%" % v) if kind == "growth" else ("%.2f%%" % v)


def fmt_pp(v, kind):
    return ("%+.1f pp" % v) if kind == "growth" else ("%+.2f pp" % v)


def crore(v):
    if v is None:
        return "—"
    x = v / 1e7 if abs(v) >= 1e6 else v
    return "₹{:,.0f} cr".format(x)


def esc(s):
    return html.escape(str(s))


def build(symbol, company, arche, records, peers, peer_names, res, log=None):
    labels = res["labels"]
    L = lambda q: labels.get(q, q)  # noqa: E731
    out = {"symbol": symbol, "company": company, "archetype": arche,
           "archetype_label": library.ARCH_LABEL.get(arche, arche),
           "peers": [{"symbol": s, "name": peer_names.get(s, s), "quarters": len(r)} for s, r in peers.items()],
           "period": "%s → %s" % (records[0]["label"], records[-1]["label"]) if records else "",
           "n_quarters": len(records), "n_filings": len(records) + sum(len(r) for r in peers.values()),
           "n_facts": sum(r.get("n_facts", 0) for r in records) + sum(x.get("n_facts", 0) for r in peers.values() for x in r)}
    out["funnel"] = funnel_rows(res["funnel"])
    rej = []
    for c, at, why in res["rejected"][:7]:
        rej.append({"name": c["metric"]["label"], "why": "<b>%s</b> — %s" % (esc(at.split(" · ")[0]), esc(why)), "at": "at: " + esc(at), "kept": False})
    for c in res["ranked"][:2]:
        rej.append({"name": c["metric"]["label"], "why": "<b>Retained · %s</b> — %s" % (c["strength"].title(), esc(c["strength_why"][:70])), "at": "at: Ranking", "kept": True})
    out["rejects"] = rej

    if not res["ranked"]:
        out["discovery"] = None
        out["note"] = "No metric breached its expectations persistently. SIGNAL reports no discovery rather than forcing one."
        return out

    c = res["ranked"][0]
    m, kind = c["metric"], c["metric"]["kind"]
    q, win = c["quarters"], c["win"]
    last = q[-1]
    tv = c["values"]
    pm_last = c["peer_med"].get(last)
    adverse = (c["sign"] > 0) == (m["bad"] == "up")
    direction = "rose" if c["sign"] > 0 else "fell"
    t1 = c.get("tests", {})
    ae1 = t1.get("AE1", ("n/a", "peer test not reached", None))
    n_run = [k for k, v in t1.items() if v[0] in ("pass", "partial", "fail")]
    n_pass = [k for k in n_run if t1[k][0] == "pass"]
    persist = max(len(c["out_self"]), len(c["out_peer"]))

    facts = {
        "C": (company, "company name"),
        "M": (m["label"], "the metric"),
        "N1": (fmt(c["med_pre"], kind), "%s median before the window (own history)" % m["label"]),
        "N2": (fmt(tv[last], kind), "%s in the latest quarter" % m["label"]),
        "N3": (fmt(pm_last, kind), "same-quarter peer median"),
        "N4": ("%d of %d" % (persist, analyze.WINDOW), "quarters in the window outside the expected range"),
        "N5": ("%d of %d" % (len(n_pass), len(n_run)), "falsification tests passed outright"),
        "N6": (ae1[1].split(" — ")[0], "peer co-movement result"),
        "Q_CP": (L(c["cp"]), "quarter the change began"),
        "Q_LAST": (L(last), "latest quarter"),
        "DIR": (direction, "direction of the move"),
        "TONE": ("adverse" if adverse else "favourable", "whether the move is adverse or favourable"),
    }
    partial = [(k, v) for k, v in t1.items() if v[0] == "partial"]
    counter_src = partial[0] if partial else ("AE1", ae1)
    facts["ALT"] = (counter_src[1][1], "strongest surviving alternative explanation (%s)" % counter_src[0])
    facts["ALT_NAME"] = (AE_META[counter_src[0]][0].lower(), "name of that alternative explanation")

    if log:
        log("writer: drafting prose from %d placeholders" % len(facts))
    d, writer = llm.write(facts, log=log)
    if not d:
        d = {
            "discovery": "{C}'s {M} {DIR} from {N1} to {N2} by {Q_LAST}, while the same-quarter peer median was {N3} — a break from both its own history and its peers that began in {Q_CP} and held for {N4} quarters.",
            "why": [
                "The move is outside the company's own expected range, so it is not ordinary quarter-to-quarter noise.",
                "Peers did not follow ({N6}), so the change is specific to {C} rather than a sector cycle.",
                "It has persisted for {N4} quarters of the window, which rules out a single-quarter event.",
                "The direction is {TONE} for the business, so it bears directly on earnings quality and risk.",
            ],
            "counter": ("Part of the move may reflect a {ALT_NAME}: {ALT}." if partial else
                        "The strongest alternative is a {ALT_NAME}; it was tested ({ALT}) and does not overturn the finding."),
        }
    out["writer"] = writer
    disc_plain = llm.fill(d["discovery"], facts)

    # underline evidence-linked values in the sentence
    s_html = esc(disc_plain)
    for key, ev in (("N2", "latest"), ("N1", "pre"), ("N3", "peer")):
        val = esc(facts[key][0])
        if val in s_html:
            s_html = s_html.replace(val, '<span class="ref" data-ev="%s">%s</span>' % (ev, val), 1)

    num_canon = m.get("num") if m.get("num") not in (None, "op_income") else None
    rec_last = res["recmap"][last]
    pre_lbl = "%s – %s" % (L(c["pre"][0]), L(c["pre"][-1]))
    out["discovery"] = {
        "metric": m["label"], "kind": kind, "sentence_html": s_html, "sentence": disc_plain,
        "sub": "%s %s against what its own history (%s) and %d same-archetype peers predicted. Every value is computed from exchange XBRL filings; the prose was written by %s from placeholders only." % (
            esc(m["label"]), direction, pre_lbl, len(peers), "a free language model" if writer != "template" else "the deterministic template"),
        "strength": c["strength"], "strength_why": c["strength_why"],
        "kv": [["Falsification tests passed", "%d / %d run" % (len(n_pass), len(n_run))],
               ["Independent source families", "2 (company, peers)"],
               ["Persistence", "%d of %d quarters" % (persist, analyze.WINDOW)],
               ["Peer-specific", "outside IQR %d of %dQ" % (len(c["out_peer"]), analyze.WINDOW)],
               ["Change point", L(c["cp"])],
               ["Candidate breaches", str(res["funnel"]["breaches"])]],
        "six": [
            ["What changed", "%s %s from <b>%s</b> to <b>%s</b>; the break began in <b>%s</b>." % (esc(m["label"]), direction, fmt(c["med_pre"], kind), fmt(tv[last], kind), esc(L(c["cp"])))],
            ["Why it is unusual", "Outside its own expected band (%s to %s) in <b>%d of %d</b> recent quarters." % (fmt(c["band"][0], kind), fmt(c["band"][1], kind), len(c["out_self"]), analyze.WINDOW)],
            ["How peers behaved", "Peer median <b>%s</b> in %s; %s." % (fmt(pm_last, kind), esc(L(last)), esc(ae1[1]))],
            ["What the numbers show", "Formula: %s. Inputs are tagged facts from %d quarterly XBRL filings." % (esc(m["formula"]), len(records))],
            ["Data integrity", esc(res["integrity"][1])],
            ["What survived", "<b>%d of %d</b> falsification tests passed outright; strength rule assigns <b>%s</b>." % (len(n_pass), len(n_run), c["strength"])],
        ],
        "why": [llm.fill(w, facts) for w in d["why"]][:5],
        "counter": {"label": "%s · %s" % (counter_src[0], AE_META[counter_src[0]][0]), "text": llm.fill(d.get("counter") or "", facts),
                    "sub": "Test result: " + counter_src[1][1]},
        "falsification": "Reconsider if %s returns inside its own pre-window range (%s to %s) for two consecutive quarters." % (
            m["label"], fmt(c["band"][0], kind), fmt(c["band"][1], kind)),
        "falsification_sub": "Or if the same-quarter peer median moves to the company's level — the effect would then be sector-wide, not company-specific.",
        "equation": {"exp": "%s ~%s (own history) · peers ~%s" % (m["label"], fmt(c["med_pre"], kind), fmt(_med(list(c["peer_med"].values())), kind)),
                     "obs": "%s %s in %s" % (m["label"], fmt(tv[last], kind), L(last)),
                     "breach": "%s %s against both its own history and its peers — persistent for %d of %d quarters." % (m["label"], direction, persist, analyze.WINDOW)},
        "charts": {
            "labels": [L(x) for x in q], "values": [tv[x] for x in q], "band": c["band"], "cp": q.index(c["cp"]) if c["cp"] in q else None,
            "win_start": q.index(win[0]), "median": [c["peer_med"].get(x) for x in q],
            "peers": [[ps.get(x) for x in q] for ps in c["peer_series"].values()],
            "driver": _driver(c, records, q, m),
            "kind": kind,
        },
        "expect_rows": {
            "self": [["Expected (pre-window band)", "%s – %s" % (fmt(c["band"][0], kind), fmt(c["band"][1], kind))],
                     ["Observed, " + L(last), fmt(tv[last], kind)],
                     ["Breach", "%s · %dQ outside band" % (fmt_pp(tv[last] - c["med_pre"], kind), len(c["out_self"]))]],
            "peer": [["Peer median, " + L(last), fmt(pm_last, kind)],
                     ["Peer IQR, " + L(last), "%s – %s" % (fmt(c["peer_q1"].get(last), kind), fmt(c["peer_q3"].get(last), kind))],
                     ["Breach", "%s · %s" % (fmt_pp(tv[last] - (pm_last or 0), kind), ae1[1].split(" — ")[0])]],
        },
        "timeline": {
            "labels": [L(x) for x in q[-9:]], "values": [fmt(tv[x], kind) for x in q[-9:]],
            "outside": [x in c["out_self"] for x in q[-9:]], "peer": [fmt(c["peer_med"].get(x), kind) for x in q[-9:]],
            "peer_out": [x in c["out_peer"] for x in q[-9:]], "filed": [res["recmap"][x]["filed"] for x in q[-9:]],
            "events": _events(q[-9:]), "cp": L(c["cp"]), "first_detect": L(win[min(1, len(win) - 1)] if len(c["out_self"]) >= 2 else win[-1]),
            "detect_filed": res["recmap"][win[min(1, len(win) - 1)]]["filed"], "last": L(last),
        },
        "families": [
            {"fn": "COMPANY", "fd": "%d quarterly results filings (XBRL), %s basis." % (len(records), records[-1]["basis"] or "as filed"), "fc": "Tier 1 · exchange filings"},
            {"fn": "PEER COMPANIES", "fd": "Same-quarter XBRL filings of %d same-archetype companies." % len(peers), "fc": "Tier 1 · %d filings" % sum(len(r) for r in peers.values())},
            {"fn": "REGULATOR", "fd": "Dated RBI policy events used by the regulatory test (AE2).", "fc": "Tier 1R · event calendar"},
            {"fn": "JOURNALISM", "fd": "Not used. News is never evidence for a number in SIGNAL.", "fc": "excluded", "excluded": True},
        ],
    }

    # numbers table + evidence trail
    ev = {}
    inp_rows = [[k, rec_last["tags"].get(k, "derived"), rec_last["raw"].get(k)] for k in m["inputs"] if k in rec_last["raw"]]
    ev["latest"] = {
        "v": fmt(tv[last], kind), "k": "%s, %s" % (m["label"], L(last)), "tag": "DERIVED · " + ("YOY GROWTH" if kind == "growth" else "RATIO"),
        "formula": [["", m["formula"]]] + [["·", "%s = %s" % (k.replace("_", " "), _fmt_input(k, v))] for k, _, v in inp_rows],
        "res": "= " + fmt(tv[last], kind),
        "check": res["integrity"][1],
        "doc": "Quarterly financial results — XBRL instance (%s)" % (rec_last["basis"] or "as filed"),
        "dm": "Company · Tier 1 · period ended %s · filed %s" % (rec_last["end"], rec_last["filed"]),
        "url": rec_last["url"],
        "passage": {"title": "Tagged facts used · %s" % L(last), "rows": [[t, _fmt_input(k, v), True] for k, t, v in inp_rows]},
    }
    pre_vals = [[L(x), fmt(tv[x], kind)] for x in c["pre"]]
    ev["pre"] = {
        "v": fmt(c["med_pre"], kind), "k": "Own-history expectation (pre-window median)", "tag": "SELF EXPECTATION",
        "formula": [["", "median( %s, %s )" % (m["label"], pre_lbl)], ["±", "2 × robust scale (1.4826 × MAD) = %s" % fmt_pp(2 * c["scale"], kind).replace("+", "")]],
        "res": "= %s · band %s – %s" % (fmt(c["med_pre"], kind), fmt(c["band"][0], kind), fmt(c["band"][1], kind)),
        "check": "Each input quarter computed from its own filing with the same formula",
        "doc": "Quarterly financial results — %d filings" % len(c["pre"]), "dm": "Company · Tier 1 · %s" % pre_lbl,
        "url": res["recmap"][c["pre"][-1]]["url"],
        "passage": {"title": "Pre-window values", "rows": [[a, b, False] for a, b in pre_vals]},
    }
    pv = [(peer_names.get(s, s), ps.get(last)) for s, ps in c["peer_series"].items()]
    ev["peer"] = {
        "v": fmt(pm_last, kind), "k": "Peer median, %s" % L(last), "tag": "PEER EXPECTATION",
        "formula": [["", "median( %s of each same-archetype peer, %s )" % (m["label"], L(last))]],
        "res": "= %s · IQR %s – %s" % (fmt(pm_last, kind), fmt(c["peer_q1"].get(last), kind), fmt(c["peer_q3"].get(last), kind)),
        "check": "Each peer value built with the identical formula from that peer's own XBRL filing",
        "doc": "Peer quarterly results — %d companies" % len(peers), "dm": "Peer company family · Tier 1 · %s" % L(last),
        "url": None,
        "passage": {"title": "Peer values · %s" % L(last), "rows": [[n, fmt(v, kind), False] for n, v in pv if v is not None]},
    }
    ev["persist"] = {
        "v": "%d / %d" % (persist, analyze.WINDOW), "k": "Quarters outside expectation", "tag": "PERSISTENCE",
        "formula": [["", "count( window quarters outside own band )  = %d" % len(c["out_self"])], ["", "count( window quarters outside peer IQR ) = %d" % len(c["out_peer"])]],
        "res": "= %d of %d" % (persist, analyze.WINDOW), "check": "Window: %s" % ", ".join(L(x) for x in win),
        "doc": "Derived from the series above", "dm": "No additional source", "url": None,
        "passage": {"title": "Window quarters", "rows": [[L(x), fmt(tv[x], kind), x in c["out_self"]] for x in win]},
    }
    if num_canon and num_canon in rec_last["raw"]:
        ev["num"] = {
            "v": _fmt_input(num_canon, rec_last["raw"][num_canon]), "k": "%s, %s" % (num_canon.replace("_", " ").capitalize(), L(last)),
            "tag": "REPORTED FACT", "formula": [["", "as reported · tag %s" % rec_last["tags"].get(num_canon, "")]],
            "res": "= " + _fmt_input(num_canon, rec_last["raw"][num_canon]), "check": res["integrity"][1],
            "doc": "Quarterly financial results — XBRL instance", "dm": "Company · Tier 1 · filed %s" % rec_last["filed"],
            "url": rec_last["url"],
            "passage": {"title": "Tagged fact", "rows": [[rec_last["tags"].get(num_canon, num_canon), _fmt_input(num_canon, rec_last["raw"][num_canon]), True]]},
        }
    out["evidence"] = {"order": [k for k in ("latest", "pre", "peer", "persist", "num") if k in ev], "items": ev}
    out["discovery"]["numbers"] = [
        ["%s, %s" % (m["label"], L(last)), fmt(tv[last], kind), fmt(pm_last, kind), "XBRL · filed %s" % rec_last["filed"], "latest"],
        ["Own-history expectation (%s)" % pre_lbl, fmt(c["med_pre"], kind), "—", "Derived · %d filings" % len(c["pre"]), "pre"],
        ["Peer median, %s" % L(last), fmt(pm_last, kind), "—", "%d peer filings" % len(peers), "peer"],
        ["Quarters outside expectation", "%d / %d" % (persist, analyze.WINDOW), "—", "Derived", "persist"],
    ] + ([[ev["num"]["k"], ev["num"]["v"], "—", "XBRL tag", "num"]] if "num" in ev else [])

    # falsification table
    tests = []
    for k in ("AE1", "AE2", "AE3", "AE4", "AE5", "AE6", "AE7", "AE8", "AE9"):
        name, alt, proc = AE_META[k]
        if k in NOT_RUN:
            tests.append([k, name, alt, proc, NOT_RUN[k], "notrun"])
        elif k in t1:
            tests.append([k, name, alt, proc, t1[k][1], t1[k][0]])
        else:
            tests.append([k, name, alt, proc, "not reached", "notrun"])
    out["tests"] = tests
    out["survived"] = {"pass": len(n_pass), "run": len(n_run),
                       "note": "; ".join("%s %s" % (k, t1[k][0]) for k in n_run if t1[k][0] != "pass") or "all run tests passed"}

    # docs table
    docs = [["%s — quarterly results (XBRL)" % company, "NSE", "Company", "1", out["period"], "%d filings" % len(records)]]
    for s, r in peers.items():
        if r:
            docs.append(["%s — quarterly results (XBRL)" % peer_names.get(s, s), "NSE", "Peer company", "1", "%s → %s" % (r[0]["label"], r[-1]["label"]), "%d filings" % len(r)])
    docs.append(["RBI policy calendar (dated events)", "RBI", "Regulator", "1R", "2023 – 2025", "%d events" % len(library.SECTOR_EVENTS)])
    out["docs"] = docs
    out["filings"] = [{"label": r["label"], "url": r["url"], "filed": r["filed"]} for r in records]

    if len(res["ranked"]) > 1:
        r2 = res["ranked"][1]
        out["runner_up"] = {"metric": r2["metric"]["label"], "strength": r2["strength"],
                            "text": "%s moved from %s to %s" % (r2["metric"]["label"], fmt(r2["med_pre"], r2["metric"]["kind"]), fmt(r2["values"][r2["quarters"][-1]], r2["metric"]["kind"]))}
    return out


def funnel_rows(f):
    return [
        {"c": f["breaches"], "l": "Candidate breaches", "g": "%d checks · self and peer expectations" % f["checks"]},
        {"c": f["valid"], "l": "Structurally valid", "g": "reconciled · ≥2Q persistence · no discontinuity"},
        {"c": f["corrob"], "l": "Corroborated", "g": "own history and peer filings agree"},
        {"c": f["specific"], "l": "Company-specific", "g": "survive peer residualisation (AE1)"},
        {"c": f["survived"], "l": "Survived falsification", "g": "AE2 · AE4 · AE5 not failed"},
        {"c": f["discovery"], "l": "Discovery", "g": "highest score · deterministic strength rule", "final": True},
    ]


def _med(xs):
    xs = [x for x in xs if x is not None]
    xs.sort()
    if not xs:
        return None
    n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


def _fmt_input(k, v):
    if v is None:
        return "—"
    if k.endswith("_pct") or k in ("roa", "car"):
        return "%.2f%%" % v
    return crore(v)


def _driver(c, records, q, m):
    num = m.get("num")
    den = m.get("den")
    if not num or m["kind"] == "growth":
        return None
    ns = analyze.raw_series(records, num) if num != "op_income" else analyze.op_income_series(records)
    ds = None
    if den:
        ds = analyze.op_income_series(records) if den == "op_income" else analyze.raw_series(records, den)
    if not ns:
        return None
    base_n = next((ns[x] for x in q if x in ns and ns[x]), None)
    base_d = next((ds[x] for x in q if ds and x in ds and ds[x]), None) if ds else None
    return {"num_label": num.replace("_", " "), "den_label": (den or "").replace("_", " ").replace("op income", "operating income"),
            "num": [100 * ns[x] / base_n if base_n and x in ns else None for x in q],
            "den": [100 * ds[x] / base_d if base_d and ds and x in ds else None for x in q] if ds else None}


def _events(qs):
    import datetime as dt
    out = []
    for x in qs:
        d = dt.date.fromisoformat(x)
        ev = [(e, t) for e, t in library.SECTOR_EVENTS if 0 <= (d - dt.date.fromisoformat(e)).days < 92]
        out.append(ev[0][1] if ev else "")
    return out
