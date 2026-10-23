"""Build a quarterly fact panel for one company from its exchange XBRL filings."""
import datetime as dt
import re

from . import library, nse, xbrl

MAX_QUARTERS = 12


def _parse_row_date(s):
    if not s:
        return None
    s = str(s).strip()
    for fmt in ("%d-%b-%Y %H:%M:%S", "%d-%b-%Y %H:%M", "%d-%b-%Y", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d", "%d-%m-%Y", "%d %b %Y"):
        for cand in (s, s[:20], s[:11], s[:10]):
            try:
                return dt.datetime.strptime(cand, fmt).date()
            except ValueError:
                continue
    m = re.search(r"(\d{2})-([A-Za-z]{3})-(\d{4})", s)
    if m:
        try:
            return dt.datetime.strptime(m.group(0), "%d-%b-%Y").date()
        except ValueError:
            return None
    return None


def _row_basis(row):
    for k, v in row.items():
        if "consol" in k.lower() and isinstance(v, str):
            lv = v.lower()
            if "non" in lv or "standalone" in lv:
                return "standalone"
            if "consol" in lv:
                return "consolidated"
    return ""


def _row_period_end(row):
    for k in ("toDate", "to_date", "periodEnded", "period_end", "toDt"):
        d = _parse_row_date(row.get(k))
        if d:
            return d
    return None


def _row_filed(row):
    for k in ("filingDate", "broadCastDate", "broadcastDate", "exchdisstime", "submissionDate"):
        d = _parse_row_date(row.get(k))
        if d:
            return d
    return None


def company_name(symbol):
    if symbol in library.UNIVERSE:
        return library.UNIVERSE[symbol][0]
    try:
        q = nse.quote(symbol)
        return (q.get("info") or {}).get("companyName") or symbol
    except Exception:  # noqa: BLE001
        return symbol


def archetype(symbol):
    if symbol in library.UNIVERSE:
        return library.UNIVERSE[symbol][1]
    try:
        q = nse.quote(symbol)
        ind = q.get("industryInfo") or {}
        txt = " ".join(str(v) for v in ind.values()) + " " + str((q.get("metadata") or {}).get("industry", ""))
        return library.archetype_from_industry(txt)
    except Exception:  # noqa: BLE001
        return "generic"


def build(symbol, prefer="standalone", log=None, max_quarters=MAX_QUARTERS):
    """Return list of quarter records sorted oldest→newest."""
    rows = nse.filings(symbol)
    cands = []
    for row in rows:
        url = nse.find_xbrl_url(row)
        if not url:
            continue
        cands.append({"url": url, "end": _row_period_end(row), "filed": _row_filed(row), "basis": _row_basis(row)})
    # prefer requested basis when the listing tells us; newest filing per period wins (revisions)
    if any(c["basis"] == prefer for c in cands):
        cands = [c for c in cands if c["basis"] in (prefer, "")]
    cands.sort(key=lambda c: (c["end"] or dt.date.min, c["filed"] or dt.date.min), reverse=True)

    out, seen = [], set()
    for c in cands:
        if len(out) >= max_quarters:
            break
        if c["end"] and c["end"] in seen:
            continue
        try:
            parsed = xbrl.parse(nse.xbrl(c["url"]))
        except Exception as e:  # noqa: BLE001
            if log:
                log("skip filing (%s): %s" % (c["end"], str(e)[:80]))
            continue
        pe = parsed["period_end"] or c["end"]
        if pe is None or pe in seen:
            continue
        b = xbrl.basis(parsed) or c["basis"]
        if b and b != prefer and any(x["basis"] == prefer for x in cands):
            continue
        mapped = library.map_facts(parsed["facts"])
        if not mapped:
            continue
        seen.add(pe)
        out.append({
            "end": pe.isoformat(), "label": xbrl.quarter_label(pe), "filed": (c["filed"] or pe).isoformat(),
            "url": c["url"], "basis": b or "", "raw": {k: v[0] for k, v in mapped.items()},
            "tags": {k: v[1] for k, v in mapped.items()}, "n_facts": len(parsed["facts"]),
        })
    out.sort(key=lambda r: r["end"])
    return out
