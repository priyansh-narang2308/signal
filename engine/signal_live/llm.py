"""Prose writer. Uses a free OpenRouter model; falls back to a deterministic template.

The model receives computed facts as placeholders ({N1}, {Q_CP}, ...) and must
write digit-free prose. Any digit outside a placeholder rejects the draft, so
the model can never type or alter a number.
"""
import json
import os
import re
import urllib.request

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_MODELS = [
    "meta-llama/llama-3.3-70b-instruct:free",
    "deepseek/deepseek-chat-v3-0324:free",
    "google/gemma-3-27b-it:free",
    "mistralai/mistral-small-3.2-24b-instruct:free",
    "qwen/qwen-2.5-72b-instruct:free",
]
PH = re.compile(r"\{[A-Z][A-Z0-9_]*\}")


def _env():
    path = os.path.join(HERE, ".env")
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.strip().split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def _clean(s):
    return PH.sub("", s or "")


def _valid(d, keys):
    if not isinstance(d, dict):
        return False
    if not isinstance(d.get("discovery"), str) or "{N1}" not in d["discovery"] and "{N2}" not in d["discovery"]:
        return False
    why = d.get("why")
    if not isinstance(why, list) or not 3 <= len(why) <= 5:
        return False
    texts = [d["discovery"], d.get("counter", "")] + [str(w) for w in why]
    for t in texts:
        if re.search(r"\d", _clean(t)):
            return False
        for ph in PH.findall(t):
            if ph[1:-1] not in keys:
                return False
    if re.search(r"\b(buy|sell|invest|target price|recommend)\b", " ".join(texts), re.I):
        return False
    return True


def _call(model, prompt, key):
    body = json.dumps({
        "model": model,
        "temperature": 0,
        "max_tokens": 700,
        "messages": [
            {"role": "system", "content": "You are a sell-side research editor. Reply with JSON only."},
            {"role": "user", "content": prompt},
        ],
    }).encode()
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=body, headers={
        "Authorization": "Bearer " + key, "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/priyansh-narang2308/signal", "X-Title": "SIGNAL"})
    with urllib.request.urlopen(req, timeout=45) as r:
        data = json.loads(r.read().decode("utf-8"))
    txt = data["choices"][0]["message"]["content"]
    m = re.search(r"\{.*\}", txt, re.S)
    return json.loads(m.group(0)) if m else None


PROMPT = """Write the prose for a financial research finding. Use ONLY the facts below.
Every number, date or quarter MUST be written as its placeholder exactly as given (for example {N1}).
Never write any digit yourself. No investment advice. Plain, precise English.

Facts (placeholder = meaning):
%s

Return JSON with exactly these keys:
{"discovery": "ONE sentence stating the finding; must use {N1} and {N2}",
 "why": ["3 to 5 short sentences on why it matters, each grounded in the facts"],
 "counter": "ONE sentence giving the strongest alternative explanation, from the test results"}
"""


def write(facts, log=None):
    """facts: {placeholder_key: (value_text, meaning)}. Returns (dict, source)."""
    _env()
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    keys = set(facts)
    if key:
        lines = "\n".join("{%s} = %s" % (k, meaning) for k, (_, meaning) in facts.items())
        models = [m.strip() for m in os.environ.get("OPENROUTER_MODELS", "").split(",") if m.strip()] or DEFAULT_MODELS
        for model in models:
            for _attempt in range(2):
                try:
                    d = _call(model, PROMPT % lines, key)
                    if _valid(d, keys):
                        return d, model
                    if log:
                        log("writer draft from %s rejected by digit guard; retrying" % model.split("/")[-1])
                except Exception as e:  # noqa: BLE001
                    if log:
                        log("writer %s unavailable (%s)" % (model.split("/")[-1], str(e)[:60]))
                    break
    return None, "template"


def fill(text, facts):
    return PH.sub(lambda m: str(facts.get(m.group(0)[1:-1], (m.group(0),))[0]), text)
