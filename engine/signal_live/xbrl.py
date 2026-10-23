"""Generic XBRL instance parser.

Exchange XBRL taxonomies change over time, so nothing here depends on a fixed
tag list. Every fact is read with its context; the current-quarter,
non-dimensional context is selected; values are returned by local tag name.
"""
import datetime as dt
import re
import xml.etree.ElementTree as ET


def _local(tag):
    return tag.rsplit("}", 1)[-1]


def _date(s):
    s = (s or "").strip()[:10]
    try:
        return dt.date.fromisoformat(s)
    except ValueError:
        return None


def _num(text):
    t = (text or "").strip().replace(",", "")
    if not t:
        return None
    neg = t.startswith("(") and t.endswith(")")
    t = t.strip("()")
    try:
        v = float(t)
    except ValueError:
        return None
    return -v if neg else v


def parse(raw):
    """Return {'period_end', 'period_start', 'facts': {name: value}, 'text': {...},
    'units': {name: unit}, 'contexts': n}."""
    root = ET.fromstring(raw)
    contexts = {}
    for el in root.iter():
        if _local(el.tag) != "context":
            continue
        cid = el.get("id")
        start = end = inst = None
        dims = False
        for sub in el.iter():
            n = _local(sub.tag)
            if n == "startDate":
                start = _date(sub.text)
            elif n == "endDate":
                end = _date(sub.text)
            elif n == "instant":
                inst = _date(sub.text)
            elif n in ("explicitMember", "typedMember"):
                dims = True
        contexts[cid] = {"start": start, "end": end or inst, "instant": inst is not None, "dims": dims}

    units = {}
    for el in root.iter():
        if _local(el.tag) == "unit":
            txt = " ".join((m.text or "") for m in el.iter() if _local(m.tag) == "measure")
            units[el.get("id")] = txt.split(":")[-1].strip().lower()

    raw_facts = []
    for el in root.iter():
        ref = el.get("contextRef")
        if not ref or ref not in contexts:
            continue
        raw_facts.append((_local(el.tag), ref, el.text, el.get("unitRef")))

    # Current reporting period: latest end date among ~quarterly durations.
    quarter_ctx = [c for c in contexts.values()
                   if not c["dims"] and c["start"] and c["end"] and 75 <= (c["end"] - c["start"]).days <= 100]
    if quarter_ctx:
        period_end = max(c["end"] for c in quarter_ctx)
    else:
        ends = [c["end"] for c in contexts.values() if c["end"]]
        period_end = max(ends) if ends else None

    def rank(c):
        """Lower is better: current quarter duration, then instant at period end, then others."""
        if c["dims"] or c["end"] != period_end:
            return None
        if c["instant"]:
            return 1
        days = (c["end"] - c["start"]).days if c["start"] else 999
        if 75 <= days <= 100:
            return 0
        return 2  # year-to-date etc.

    facts, text, unit_of, best = {}, {}, {}, {}
    for name, ref, val, uref in raw_facts:
        c = contexts[ref]
        r = rank(c)
        v = _num(val)
        if v is None:
            if val and val.strip() and name not in text:
                text[name] = val.strip()[:300]
            continue
        if r is None:
            continue
        if name not in best or r < best[name]:
            best[name] = r
            facts[name] = v
            unit_of[name] = units.get(uref, "")

    period_start = None
    if quarter_ctx:
        period_start = max((c for c in quarter_ctx if c["end"] == period_end), key=lambda c: c["start"])["start"]
    return {"period_end": period_end, "period_start": period_start, "facts": facts,
            "units": unit_of, "text": text, "contexts": len(contexts)}


def quarter_label(d):
    """Indian fiscal quarter label, e.g. 2025-06-30 -> 'Q1 FY26'."""
    if d is None:
        return "?"
    fy = d.year + 1 if d.month >= 4 else d.year
    q = {6: 1, 9: 2, 12: 3, 3: 4}.get(d.month)
    if q is None:
        q = ((d.month - 4) % 12) // 3 + 1
    return "Q%d FY%02d" % (q, fy % 100)


def basis(parsed):
    """'standalone' / 'consolidated' / '' from the filing's own text facts."""
    for k, v in parsed["text"].items():
        if re.search(r"standalone|consolidated", k, re.I) or re.search(r"nature.*report", k, re.I):
            lv = v.lower()
            if "consolidated" in lv:
                return "consolidated"
            if "standalone" in lv:
                return "standalone"
    return ""
