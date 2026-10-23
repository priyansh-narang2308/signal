"""Generate synthetic NSE-shaped filings for offline tests (SIGNAL_OFFLINE=1).
Not used in live runs. Values are random but obey the bank operating identity."""
import datetime as dt
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
os.environ["SIGNAL_OFFLINE"] = "1"
from signal_live import nse  # noqa: E402

BANKS = ["AXISBANK", "HDFCBANK", "ICICIBANK", "KOTAKBANK", "INDUSINDBK", "FEDERALBNK", "IDFCFIRSTB"]
ENDS = []
d = dt.date(2023, 9, 30)
for _ in range(13):
    ENDS.append(d)
    m = d.month + 3
    y = d.year + (1 if m > 12 else 0)
    m = m - 12 if m > 12 else m
    last = {3: 31, 6: 30, 9: 30, 12: 31}[m]
    d = dt.date(y, m, last)

TPL = """<?xml version="1.0" encoding="UTF-8"?>
<xbrli:xbrl xmlns:xbrli="http://www.xbrl.org/2003/instance" xmlns:in-capmkt="http://www.sebi.gov.in/xbrl/2024-05-31/in-capmkt">
<xbrli:context id="OneD"><xbrli:entity><xbrli:identifier scheme="x">{sym}</xbrli:identifier></xbrli:entity><xbrli:period><xbrli:startDate>{start}</xbrli:startDate><xbrli:endDate>{end}</xbrli:endDate></xbrli:period></xbrli:context>
<xbrli:context id="OneI"><xbrli:entity><xbrli:identifier scheme="x">{sym}</xbrli:identifier></xbrli:entity><xbrli:period><xbrli:instant>{end}</xbrli:instant></xbrli:period></xbrli:context>
<xbrli:context id="PrevD"><xbrli:entity><xbrli:identifier scheme="x">{sym}</xbrli:identifier></xbrli:entity><xbrli:period><xbrli:startDate>{pstart}</xbrli:startDate><xbrli:endDate>{pend}</xbrli:endDate></xbrli:period></xbrli:context>
<xbrli:unit id="INR"><xbrli:measure>iso4217:INR</xbrli:measure></xbrli:unit>
<xbrli:unit id="pure"><xbrli:measure>xbrli:pure</xbrli:measure></xbrli:unit>
<in-capmkt:NatureOfReportStandaloneConsolidated contextRef="OneD">Standalone</in-capmkt:NatureOfReportStandaloneConsolidated>
{facts}
</xbrli:xbrl>"""


def gen(sym, i_bank):
    rnd = random.Random(sym)
    rows = []
    size = rnd.uniform(0.6, 2.0) * 3e11
    gnpa_pct = rnd.uniform(1.2, 2.6)
    for i, end in enumerate(ENDS):
        g = 1.035 ** i
        ie_ = size * g
        iexp = ie_ * rnd.uniform(0.52, 0.56)
        oi = ie_ * rnd.uniform(0.17, 0.2)
        opinc = ie_ - iexp + oi
        opex = opinc * rnd.uniform(0.42, 0.46)
        prov_share = rnd.uniform(0.10, 0.13)
        gp = gnpa_pct + rnd.uniform(-0.05, 0.05)
        if sym == "AXISBANK" and i >= 9:  # injected company-specific stress
            prov_share = 0.13 + 0.035 * (i - 8)
            gp = gnpa_pct + 0.18 * (i - 8)
        prov = opinc * prov_share
        pbt = opinc - opex - prov
        pat = pbt * 0.75
        adv = ie_ * 13
        gnpa = adv * gp / 100
        nnpa = gnpa * rnd.uniform(0.22, 0.27)
        facts = {"InterestEarned": ie_, "InterestExpended": iexp, "OtherIncome": oi, "OperatingExpenses": opex,
                 "ProvisionsOtherThanTaxAndContingencies": prov, "ProfitLossFromOrdinaryActivitiesBeforeTax": pbt,
                 "ProfitLossForThePeriod": pat, "GrossNonPerformingAssets": gnpa, "NetNonPerformingAssets": nnpa}
        lines = ['<in-capmkt:%s contextRef="OneD" unitRef="INR" decimals="0">%.0f</in-capmkt:%s>' % (k, v, k) for k, v in facts.items()]
        lines.append('<in-capmkt:PercentageOfGrossNpa contextRef="OneI" unitRef="pure" decimals="2">%.2f</in-capmkt:PercentageOfGrossNpa>' % gp)
        lines.append('<in-capmkt:PercentageOfNetNpa contextRef="OneI" unitRef="pure" decimals="2">%.2f</in-capmkt:PercentageOfNetNpa>' % (gp * 0.25))
        lines.append('<in-capmkt:InterestEarned contextRef="PrevD" unitRef="INR" decimals="0">%.0f</in-capmkt:InterestEarned>' % (ie_ * 0.9))
        start = dt.date(end.year if end.month > 3 else end.year, end.month - 2 if end.month > 2 else 1, 1)
        url = "https://nsearchives.nseindia.com/corporate/xbrl/%s_%s.xml" % (sym, end.isoformat())
        xml = TPL.format(sym=sym, start=start.isoformat(), end=end.isoformat(), pstart=(start - dt.timedelta(days=365)).isoformat(),
                         pend=(end - dt.timedelta(days=365)).isoformat(), facts="\n".join(lines))
        with open(nse._cache_path("xbrl", url.split("//", 1)[-1]), "w") as f:
            f.write(xml)
        rows.append({"symbol": sym, "consolidated": "Non-Consolidated", "period": "Quarterly",
                     "toDate": end.strftime("%d-%b-%Y"), "filingDate": (end + dt.timedelta(days=20)).strftime("%d-%b-%Y %H:%M:%S"),
                     "xbrl": url})
    with open(nse._cache_path("filings", sym) + ".json", "w") as f:
        json.dump(rows[::-1], f)


for i, s in enumerate(BANKS):
    gen(s, i)
print("fixtures written:", len(BANKS), "banks ×", len(ENDS), "quarters")
