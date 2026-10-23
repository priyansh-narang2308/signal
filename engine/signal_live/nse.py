"""NSE public-filing access with polite rate limiting and an on-disk cache.

Only public exchange pages are used. Every response is cached under
engine/cache/, so a company fetched once is available offline afterwards.

Set SIGNAL_OFFLINE=1 to read only from engine/fixtures/ (used for tests).
"""
import gzip
import http.cookiejar
import json
import os
import re
import time
import urllib.parse
import urllib.request
import zlib

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(HERE, "cache")
FIXTURES = os.path.join(HERE, "fixtures")
OFFLINE = os.environ.get("SIGNAL_OFFLINE") == "1"

BASE = "https://www.nseindia.com"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
MIN_GAP = 0.8  # seconds between live requests

_jar = http.cookiejar.CookieJar()
_opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(_jar))
_last = [0.0]
_warm = [False]


class FetchError(Exception):
    pass


def _cache_path(kind, key):
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", key)[-150:]
    d = os.path.join(FIXTURES if OFFLINE else CACHE, kind)
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, safe)


def _decode(resp):
    raw = resp.read()
    enc = (resp.headers.get("Content-Encoding") or "").lower()
    if enc == "gzip":
        raw = gzip.decompress(raw)
    elif enc == "deflate":
        raw = zlib.decompress(raw)
    elif enc == "br":
        raise FetchError("server sent brotli; retrying without it")
    return raw


def _get(url, referer=BASE + "/", accept="application/json, text/plain, */*", tries=3):
    last_err = None
    for attempt in range(tries):
        gap = time.time() - _last[0]
        if gap < MIN_GAP:
            time.sleep(MIN_GAP - gap)
        req = urllib.request.Request(url, headers={
            "User-Agent": UA,
            "Accept": accept,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Referer": referer,
            "Connection": "keep-alive",
        })
        try:
            with _opener.open(req, timeout=25) as r:
                _last[0] = time.time()
                return _decode(r)
        except Exception as e:  # noqa: BLE001
            _last[0] = time.time()
            last_err = e
            # session cookies expire: re-warm and retry
            _warm[0] = False
            warm()
            time.sleep(1.5 * (attempt + 1))
    raise FetchError("%s -> %s" % (url, last_err))


def warm():
    """Visit the home page once so NSE sets its session cookies."""
    if OFFLINE or _warm[0]:
        return
    for path in ("/", "/market-data/live-equity-market"):
        try:
            req = urllib.request.Request(BASE + path, headers={
                "User-Agent": UA, "Accept": "text/html,application/xhtml+xml",
                "Accept-Language": "en-US,en;q=0.9", "Accept-Encoding": "gzip, deflate"})
            with _opener.open(req, timeout=25) as r:
                _decode(r)
        except Exception:  # noqa: BLE001
            pass
        time.sleep(0.6)
    _warm[0] = True


def _json(kind, key, url, referer, max_age_h):
    path = _cache_path(kind, key) + ".json"
    if os.path.exists(path):
        age_h = (time.time() - os.path.getmtime(path)) / 3600
        if OFFLINE or age_h < max_age_h:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
    if OFFLINE:
        raise FetchError("offline: no fixture for %s/%s" % (kind, key))
    warm()
    data = json.loads(_get(url, referer=referer).decode("utf-8", "replace"))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    return data


def quote(symbol):
    s = urllib.parse.quote(symbol)
    return _json("quote", symbol, BASE + "/api/quote-equity?symbol=" + s,
                 BASE + "/get-quotes/equity?symbol=" + s, max_age_h=24 * 7)


def filings(symbol):
    """Quarterly financial-results filings (with XBRL links) for a symbol."""
    s = urllib.parse.quote(symbol)
    url = (BASE + "/api/corporates-financial-results?index=equities&symbol=" + s +
           "&period=Quarterly")
    data = _json("filings", symbol, url,
                 BASE + "/companies-listing/corporate-filings-financial-results", max_age_h=12)
    if isinstance(data, dict):
        for k in ("data", "rows", "results"):
            if isinstance(data.get(k), list):
                return data[k]
        return []
    return data or []


def xbrl(url):
    """Download one XBRL instance (cached forever: filings are immutable)."""
    path = _cache_path("xbrl", url.split("//", 1)[-1])
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f.read()
    if OFFLINE:
        raise FetchError("offline: no fixture for " + url)
    warm()
    raw = _get(url, referer=BASE + "/", accept="application/xml,text/xml,*/*")
    if b"<" not in raw[:200]:
        raise FetchError("not XML: " + url)
    with open(path, "wb") as f:
        f.write(raw)
    return raw


def find_xbrl_url(row):
    """NSE has used several field names over time; find the XBRL link defensively."""
    for k in ("xbrl", "xbrlFile", "xbrl_file", "XBRL", "xbrlUrl"):
        v = row.get(k)
        if isinstance(v, str) and v.lower().endswith(".xml"):
            return v if v.startswith("http") else "https://nsearchives.nseindia.com" + v
    for v in row.values():
        if isinstance(v, str) and v.lower().endswith(".xml") and "xbrl" in v.lower():
            return v if v.startswith("http") else "https://nsearchives.nseindia.com" + v
    return None
