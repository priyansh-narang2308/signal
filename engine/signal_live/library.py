"""Archetype-level metric library.

Nothing here names a company. Tags are matched by pattern because exchange
XBRL tag names vary between taxonomy versions; the same patterns apply to every
bank, every NBFC, every insurer.
"""
import re

# Track A universe used to form same-archetype peer panels (NIFTY 50 + non-NIFTY).
UNIVERSE = {
    # private banks
    "HDFCBANK": ("HDFC Bank", "bank"), "ICICIBANK": ("ICICI Bank", "bank"),
    "KOTAKBANK": ("Kotak Mahindra Bank", "bank"), "AXISBANK": ("Axis Bank", "bank"),
    "INDUSINDBK": ("IndusInd Bank", "bank"), "FEDERALBNK": ("Federal Bank", "bank"),
    "IDFCFIRSTB": ("IDFC First Bank", "bank"), "BANDHANBNK": ("Bandhan Bank", "bank"),
    "RBLBANK": ("RBL Bank", "bank"), "YESBANK": ("Yes Bank", "bank"),
    "AUBANK": ("AU Small Finance Bank", "bank"), "KARURVYSYA": ("Karur Vysya Bank", "bank"),
    # public sector banks
    "SBIN": ("State Bank of India", "bank"), "BANKBARODA": ("Bank of Baroda", "bank"),
    "PNB": ("Punjab National Bank", "bank"), "CANBK": ("Canara Bank", "bank"),
    "UNIONBANK": ("Union Bank of India", "bank"), "INDIANB": ("Indian Bank", "bank"),
    "BANKINDIA": ("Bank of India", "bank"),
    # NBFCs and HFCs
    "BAJFINANCE": ("Bajaj Finance", "nbfc"), "SHRIRAMFIN": ("Shriram Finance", "nbfc"),
    "CHOLAFIN": ("Cholamandalam Investment", "nbfc"), "M&MFIN": ("Mahindra & Mahindra Financial", "nbfc"),
    "MUTHOOTFIN": ("Muthoot Finance", "nbfc"), "LICHSGFIN": ("LIC Housing Finance", "nbfc"),
    "SUNDARMFIN": ("Sundaram Finance", "nbfc"), "POONAWALLA": ("Poonawalla Fincorp", "nbfc"),
    "LTF": ("L&T Finance", "nbfc"), "ABCAPITAL": ("Aditya Birla Capital", "nbfc"),
    "PNBHOUSING": ("PNB Housing Finance", "nbfc"), "JIOFIN": ("Jio Financial Services", "nbfc"),
    # insurers
    "HDFCLIFE": ("HDFC Life", "insurer"), "SBILIFE": ("SBI Life", "insurer"),
    "ICICIPRULI": ("ICICI Prudential Life", "insurer"), "ICICIGI": ("ICICI Lombard", "insurer"),
    "LICI": ("Life Insurance Corporation", "insurer"),
    # market infrastructure and holding companies
    "BAJAJFINSV": ("Bajaj Finserv", "generic"), "BSE": ("BSE", "generic"),
    "CDSL": ("CDSL", "generic"), "MCX": ("MCX", "generic"),
}

ARCH_LABEL = {"bank": "Bank", "nbfc": "NBFC / HFC", "insurer": "Insurer", "generic": "Market infra / holdco"}


def archetype_from_industry(text):
    t = (text or "").lower()
    if "bank" in t:
        return "bank"
    if "insur" in t:
        return "insurer"
    if any(w in t for w in ("finance", "nbfc", "housing", "financial", "lending", "credit")):
        return "nbfc"
    return "generic"


# ---- raw tag patterns: (canonical, include regex, exclude regex) ----------
RAW = [
    ("interest_earned", r"^(total)?interestearned$|^interestincome$|^totalinterestincome$", r"net|other"),
    ("interest_expended", r"^(total)?interestexpended$|^interestexpense$", r"net"),
    ("other_income", r"^otherincome$", r""),
    ("opex", r"^(total)?operatingexpenses$", r""),
    ("provisions", r"provisions.*other.*than.*tax|^provisionsandcontingencies$", r"tax(es)?$|deferred"),
    ("pbt", r"^profit(loss)?(from(ordinary)?activities)?beforetax$|^profitbeforetax$|beforeexceptional.*tax", r""),
    ("pat", r"^profit(loss)?for(the)?period$|^netprofit(loss)?for(the)?period$|^profitlossforperiodfromcontinuingoperations$", r"attributable|minority|noncontrolling|beforetax"),
    ("gnpa_amt", r"gross(npa|nonperformingassets|nonperformingasset)s?$|^grossnpa", r"percent|ratio|percentage"),
    ("nnpa_amt", r"^net(npa|nonperformingassets|nonperformingasset)s?$|^netnpa$", r"percent|ratio|percentage|gross"),
    ("gnpa_pct", r"(percent|percentage|ratio).*gross.*(npa|nonperforming)|gross.*(npa|nonperforming).*(percent|percentage|ratio)", r""),
    ("nnpa_pct", r"(percent|percentage|ratio).*net.*(npa|nonperforming)|^(?!.*gross).*net.*(npa|nonperforming).*(percent|percentage|ratio)|^percentageofnpa$", r"gross"),
    ("roa", r"returnonassets", r""),
    ("car", r"capitaladequacyratio|cet1|commonequitytier1", r"additional"),
    ("revenue", r"^revenuefromoperations$|^totalrevenuefromoperations$", r""),
    ("finance_costs", r"^financecosts?$", r""),
    ("impairment", r"impairment.*financial|^impairmentoffinancialinstruments$", r""),
    ("employee", r"^employeebenefitsexpense$|^employeebenefitexpense$|^employeescost$", r""),
    ("other_expenses", r"^otherexpenses$", r""),
    ("total_income", r"^(total)?income$|^totalincome$|^incomefromoperationsandotherincome$", r""),
    ("total_expenses", r"^(total)?expenses$|^totalexpenses$", r"other|employee|interest"),
]
_RAW_C = [(c, re.compile(inc), re.compile(exc) if exc else None) for c, inc, exc in RAW]


def map_facts(facts):
    """Map one filing's local-name facts to canonical names. Returns {canon: (value, tag)}."""
    out = {}
    names = sorted(facts.keys(), key=len)
    for canon, inc, exc in _RAW_C:
        for name in names:
            low = name.lower()
            if inc.search(low) and not (exc and exc.search(low)):
                out[canon] = (facts[name], name)
                break
    # percentages reported as fractions in some filings
    for k in ("gnpa_pct", "nnpa_pct", "roa", "car"):
        if k in out and 0 < abs(out[k][0]) < 0.2 and k != "roa":
            out[k] = (out[k][0] * 100, out[k][1])
    return out


# ---- derived metrics ---------------------------------------------------------
# kind: "ratio" (level in %), "growth" (YoY %).  bad: which direction is adverse.
# num/den: canonical inputs, used by the denominator test (AE4).
def _op_income(r):
    try:
        return r["interest_earned"] - r["interest_expended"] + r["other_income"]
    except KeyError:
        return None


METRICS = {
    "bank": [
        dict(id="gnpa_pct", label="Gross NPA ratio", kind="ratio", bad="up", f=lambda r: r.get("gnpa_pct"),
             formula="Gross NPAs ÷ gross advances (as reported)", num="gnpa_amt", den=None, inputs=["gnpa_pct", "gnpa_amt"]),
        dict(id="nnpa_pct", label="Net NPA ratio", kind="ratio", bad="up", f=lambda r: r.get("nnpa_pct"),
             formula="Net NPAs ÷ net advances (as reported)", num="nnpa_amt", den=None, inputs=["nnpa_pct", "nnpa_amt"]),
        dict(id="pcr", label="Provision coverage (NPA)", kind="ratio", bad="down",
             f=lambda r: 100 * (1 - r["nnpa_amt"] / r["gnpa_amt"]) if r.get("gnpa_amt") and r.get("nnpa_amt") is not None else None,
             formula="1 − net NPAs ÷ gross NPAs", num="nnpa_amt", den="gnpa_amt", inputs=["gnpa_amt", "nnpa_amt"]),
        dict(id="credit_cost_share", label="Provisions ÷ operating income", kind="ratio", bad="up",
             f=lambda r: 100 * r["provisions"] / _op_income(r) if r.get("provisions") is not None and _op_income(r) else None,
             formula="Provisions (other than tax) ÷ (interest earned − interest expended + other income)",
             num="provisions", den="op_income", inputs=["provisions", "interest_earned", "interest_expended", "other_income"]),
        dict(id="cost_to_income", label="Cost-to-income", kind="ratio", bad="up",
             f=lambda r: 100 * r["opex"] / _op_income(r) if r.get("opex") is not None and _op_income(r) else None,
             formula="Operating expenses ÷ (interest earned − interest expended + other income)",
             num="opex", den="op_income", inputs=["opex", "interest_earned", "interest_expended", "other_income"]),
        dict(id="funding_cost_share", label="Interest expended ÷ interest earned", kind="ratio", bad="up",
             f=lambda r: 100 * r["interest_expended"] / r["interest_earned"] if r.get("interest_earned") and r.get("interest_expended") is not None else None,
             formula="Interest expended ÷ interest earned", num="interest_expended", den="interest_earned",
             inputs=["interest_expended", "interest_earned"]),
        dict(id="other_income_share", label="Other income ÷ operating income", kind="ratio", bad="up",
             f=lambda r: 100 * r["other_income"] / _op_income(r) if r.get("other_income") is not None and _op_income(r) else None,
             formula="Other income ÷ (interest earned − interest expended + other income)",
             num="other_income", den="op_income", inputs=["other_income", "interest_earned", "interest_expended"]),
        dict(id="nii_yoy", label="Net interest income growth (YoY)", kind="growth", bad="down",
             f=lambda r: (r["interest_earned"] - r["interest_expended"]) if r.get("interest_earned") and r.get("interest_expended") is not None else None,
             formula="(NII this quarter ÷ NII same quarter last year) − 1", num=None, den=None,
             inputs=["interest_earned", "interest_expended"]),
        dict(id="pat_yoy", label="Net profit growth (YoY)", kind="growth", bad="down", f=lambda r: r.get("pat"),
             formula="(Net profit ÷ net profit same quarter last year) − 1", num=None, den=None, inputs=["pat"]),
        dict(id="gnpa_amt_yoy", label="Gross NPA stock growth (YoY)", kind="growth", bad="up", f=lambda r: r.get("gnpa_amt"),
             formula="(Gross NPAs ÷ gross NPAs same quarter last year) − 1", num=None, den=None, inputs=["gnpa_amt"]),
    ],
    "nbfc": [
        dict(id="credit_cost_share", label="Impairment ÷ revenue", kind="ratio", bad="up",
             f=lambda r: 100 * r["impairment"] / r["revenue"] if r.get("impairment") is not None and r.get("revenue") else None,
             formula="Impairment on financial instruments ÷ revenue from operations", num="impairment", den="revenue",
             inputs=["impairment", "revenue"]),
        dict(id="funding_cost_share", label="Finance costs ÷ revenue", kind="ratio", bad="up",
             f=lambda r: 100 * r["finance_costs"] / r["revenue"] if r.get("finance_costs") is not None and r.get("revenue") else None,
             formula="Finance costs ÷ revenue from operations", num="finance_costs", den="revenue",
             inputs=["finance_costs", "revenue"]),
        dict(id="opex_share", label="Operating cost ÷ revenue", kind="ratio", bad="up",
             f=lambda r: 100 * (r.get("employee", 0) + r.get("other_expenses", 0)) / r["revenue"] if r.get("revenue") and (r.get("employee") is not None or r.get("other_expenses") is not None) else None,
             formula="(Employee benefits + other expenses) ÷ revenue from operations", num="employee", den="revenue",
             inputs=["employee", "other_expenses", "revenue"]),
        dict(id="pat_margin", label="Net profit margin", kind="ratio", bad="down",
             f=lambda r: 100 * r["pat"] / (r.get("total_income") or r["revenue"]) if r.get("pat") is not None and (r.get("total_income") or r.get("revenue")) else None,
             formula="Net profit ÷ total income", num="pat", den="total_income", inputs=["pat", "total_income"]),
        dict(id="revenue_yoy", label="Revenue growth (YoY)", kind="growth", bad="down", f=lambda r: r.get("revenue"),
             formula="(Revenue ÷ revenue same quarter last year) − 1", num=None, den=None, inputs=["revenue"]),
        dict(id="pat_yoy", label="Net profit growth (YoY)", kind="growth", bad="down", f=lambda r: r.get("pat"),
             formula="(Net profit ÷ net profit same quarter last year) − 1", num=None, den=None, inputs=["pat"]),
        dict(id="gnpa_pct", label="Gross Stage 3 / NPA ratio", kind="ratio", bad="up", f=lambda r: r.get("gnpa_pct"),
             formula="Gross Stage 3 assets ÷ gross loans (as reported)", num="gnpa_amt", den=None, inputs=["gnpa_pct"]),
    ],
    "generic": [
        dict(id="pat_margin", label="Net profit margin", kind="ratio", bad="down",
             f=lambda r: 100 * r["pat"] / (r.get("total_income") or r.get("revenue")) if r.get("pat") is not None and (r.get("total_income") or r.get("revenue")) else None,
             formula="Net profit ÷ total income", num="pat", den="total_income", inputs=["pat", "total_income"]),
        dict(id="expense_ratio", label="Total expenses ÷ total income", kind="ratio", bad="up",
             f=lambda r: 100 * r["total_expenses"] / r["total_income"] if r.get("total_expenses") is not None and r.get("total_income") else None,
             formula="Total expenses ÷ total income", num="total_expenses", den="total_income", inputs=["total_expenses", "total_income"]),
        dict(id="other_income_share", label="Other income ÷ total income", kind="ratio", bad="up",
             f=lambda r: 100 * r["other_income"] / r["total_income"] if r.get("other_income") is not None and r.get("total_income") else None,
             formula="Other income ÷ total income", num="other_income", den="total_income", inputs=["other_income", "total_income"]),
        dict(id="revenue_yoy", label="Revenue growth (YoY)", kind="growth", bad="down", f=lambda r: r.get("revenue") or r.get("total_income"),
             formula="(Revenue ÷ revenue same quarter last year) − 1", num=None, den=None, inputs=["revenue"]),
        dict(id="pat_yoy", label="Net profit growth (YoY)", kind="growth", bad="down", f=lambda r: r.get("pat"),
             formula="(Net profit ÷ net profit same quarter last year) − 1", num=None, den=None, inputs=["pat"]),
    ],
}
METRICS["insurer"] = METRICS["generic"]

# Reconciliation identities (AE7): (name, function(raw)->(lhs, rhs) or None)
def _ident_bank(r):
    need = ("interest_earned", "interest_expended", "other_income", "opex", "provisions", "pbt")
    if not all(k in r for k in need):
        return None
    lhs = r["interest_earned"] - r["interest_expended"] + r["other_income"] - r["opex"] - r["provisions"]
    return lhs, r["pbt"]


def _ident_income(r):
    if not all(k in r for k in ("total_income", "total_expenses", "pbt")):
        return None
    return r["total_income"] - r["total_expenses"], r["pbt"]


IDENTITIES = {
    "bank": [("Operating identity: NII + other income − opex − provisions = PBT (before exceptional items)", _ident_bank)],
    "nbfc": [("Income identity: total income − total expenses = PBT", _ident_income)],
    "generic": [("Income identity: total income − total expenses = PBT", _ident_income)],
    "insurer": [("Income identity: total income − total expenses = PBT", _ident_income)],
}

# Dated sector events used by the regulatory / macro test (AE2). Public, generic, not company-specific.
SECTOR_EVENTS = [
    ("2023-11-16", "RBI raises risk weights on consumer credit and bank lending to NBFCs"),
    ("2024-10-09", "RBI shifts monetary policy stance to neutral"),
    ("2025-02-07", "RBI cuts repo rate by 25 bps"),
    ("2025-02-25", "RBI restores risk weights on bank lending to NBFCs"),
    ("2025-04-09", "RBI cuts repo rate by 25 bps"),
    ("2025-06-06", "RBI cuts repo rate by 50 bps and CRR by 100 bps"),
]
