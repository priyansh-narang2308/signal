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


_TAG = re.compile(r"<[^>]+>")
_ATTR = re.compile(r'([\w:.-]+)\s*=\s*("([^"]*)"|\'([^\']*)\')')


def _attrs(s):
    return {m.group(1).split(":")[-1] if m.group(1).count(":") and m.group(1).split(":")[0] not in ("xmlns",) else m.group(1): (m.group(3) if m.group(3) is not None else m.group(4)) for m in _ATTR.finditer(s)}


def _ix_num(text, a):
    t = _TAG.sub("", text or "").strip().replace("&nbsp;", "").replace(" ", "")
    fmt = (a.get("format") or "").lower()
    if t in ("", "-", "–", "—") or "zero" in fmt or "dash" in fmt:
        v = 0.0
    else:
        if "comma-decimal" in fmt or "numcommadecimal" in fmt:
            t = t.replace(".", "").replace(",", ".")
        else:
            t = t.replace(",", "")
        v = _num(t)
        if v is None:
            return None
    try:
        v *= 10 ** int(a.get("scale") or 0)
    except ValueError:
        pass
    if a.get("sign") == "-":
        v = -v
    return v


def _parse_inline(raw):
    """Inline XBRL (HTML) → same structure as a plain instance document."""
    txt = raw.decode("utf-8", "replace")
    contexts = {}
    for m in re.finditer(r"<(?:\w+:)?context\b([^>]*)>(.*?)</(?:\w+:)?context>", txt, re.S | re.I):
        a = _attrs(m.group(1))
        body = m.group(2)
        g = lambda tag: (re.search(r"<(?:\w+:)?%s\b[^>]*>\s*([^<]+?)\s*<" % tag, body, re.I) or [None, None])[1]  # noqa: E731
        start, end, inst = _date(g("startDate")), _date(g("endDate")), _date(g("instant"))
        dims = bool(re.search(r"explicitMember|typedMember", body, re.I))
        contexts[a.get("id")] = {"start": start, "end": end or inst, "instant": inst is not None, "dims": dims}
    units = {}
    for m in re.finditer(r"<(?:\w+:)?unit\b([^>]*)>(.*?)</(?:\w+:)?unit>", txt, re.S | re.I):
        meas = re.findall(r"<(?:\w+:)?measure[^>]*>\s*([^<]+?)\s*<", m.group(2), re.I)
        units[_attrs(m.group(1)).get("id")] = (meas[-1] if meas else "").split(":")[-1].lower()
    raw_facts, text_facts = [], []
    for m in re.finditer(r"<ix:nonFraction\b([^>]*)>(.*?)</ix:nonFraction>", txt, re.S | re.I):
        a = _attrs(m.group(1))
        name = (re.search(r'\bname\s*=\s*"([^"]+)"', m.group(1)) or [None, ""])[1].split(":")[-1]
        v = _ix_num(m.group(2), a)
        if name and v is not None:
            raw_facts.append((name, a.get("contextRef"), v, a.get("unitRef")))
    for m in re.finditer(r"<ix:nonNumeric\b([^>]*)>(.*?)</ix:nonNumeric>", txt, re.S | re.I):
        name = (re.search(r'\bname\s*=\s*"([^"]+)"', m.group(1)) or [None, ""])[1].split(":")[-1]
        text_facts.append((name, _TAG.sub("", m.group(2)).strip()[:300]))
    return contexts, units, raw_facts, text_facts


def parse(raw):
    """Return {'period_end', 'period_start', 'facts': {name: value}, 'text': {...},
    'units': {name: unit}, 'contexts': n}."""
    head = raw[:4000].lower()
    if b"<html" in head or b"ix:header" in raw[:200000].lower() or b"nonfraction" in raw[:400000].lower():
        contexts, units, raw_facts, text_facts = _parse_inline(raw)
        return _finish(contexts, units, raw_facts, text_facts, numeric=True)
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
    return _finish(contexts, units, raw_facts, [], numeric=False)


def _finish(contexts, units, raw_facts, text_facts, numeric):
    raw_facts = [f for f in raw_facts if f[1] in contexts]

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
    for name, val in text_facts:
        if name and val and name not in text:
            text[name] = val
    for name, ref, val, uref in raw_facts:
        c = contexts[ref]
        r = rank(c)
        v = val if numeric else _num(val)
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
