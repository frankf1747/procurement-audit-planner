"""Re-derive one flagged item per test independently from spend-clean.csv
(and notices-clean.csv / the source workbook) and compare to analytics.json."""
import re
import json
import os

import openpyxl
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FULL = os.path.join(ROOT, "outputs", "analytics-full")
A = json.load(open(os.path.join(ROOT, "outputs", "analytics.json")))
sp = pd.read_csv(os.path.join(FULL, "spend-clean.csv"), parse_dates=["pay_date"])
months = sp["pay_date"].dt.to_period("M").nunique()
factor = 12 / months
T = A["tests"]
results = []


def check(name, ok, detail):
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


def close(a, b):
    return abs(float(a) - float(b)) < 0.01


# 1 threshold_clustering: top row at 25000; verify band and the workbook cell
tc = T["threshold_clustering"]["by_threshold"]["25000"]
r = tc["top20"][0]
row = sp[sp["row_id"] == r["row_id"]].iloc[0]
in_band = 0.9 * 25000 <= row["Net amount"] < 25000
fname, srow = r["row_id"].rsplit(":", 1)
ws = openpyxl.load_workbook(os.path.join(ROOT, "data", "spend", fname), read_only=True)["Data to publish"]
cells = next(ws.iter_rows(min_row=int(srow), max_row=int(srow), values_only=True))
check("threshold_clustering@25000", in_band and close(cells[4], r["amount"]) and str(cells[5]).strip() == str(r["supplier"]).strip(),
      f"row_id {r['row_id']} workbook amount={cells[4]} supplier={cells[5]!r} in band={in_band}")

# 2 split_purchases: top general_procurement window at 25000
w = T["split_purchases"]["by_threshold"]["25000"]["headline_general_procurement"]["top20"][0]
m = ((sp["supplier_norm"] == w["supplier"]) & (sp["pay_date"] >= w["window_start"]) &
     (sp["pay_date"] <= w["window_end"]) & (sp["Net amount"] < 25000))
check("split_purchases@25000", close(sp.loc[m, "Net amount"].sum(), w["window_total"]) and int(m.sum()) == w["n_payments"],
      f"supplier {w['supplier']} {w['window_start']}..{w['window_end']} re-sum={round(sp.loc[m, 'Net amount'].sum(), 2)} n={int(m.sum())} vs {w['window_total']} n={w['n_payments']}; row_ids {w['row_ids']}")

# 3 high_value_suppliers: top general_procurement supplier at publication tier
h = T["high_value_suppliers"]["tiers"]["publication_threshold"]["by_dominant_tag"]["general_procurement"]["top20"][0]
s = sp.loc[sp["supplier_norm"] == h["supplier"], "Net amount"].sum()
check("high_value_suppliers", close(s * factor, h["annualised_estimate"]),
      f"supplier {h['supplier']} re-sum={round(s, 2)} x {factor} = {round(s * factor, 2)} vs {h['annualised_estimate']}; sample row_ids {h['row_ids_sample']}")

# 4 duplicates: top different_time group
d = T["duplicates"]["different_time"]["top20"][0]
m = ((sp["supplier_norm"] == d["supplier"]) & ((sp["Net amount"] - d["amount"]).abs() < 0.005) &
     (sp["pay_date"] >= d["first_date"]) & (sp["pay_date"] <= d["last_date"]))
ids = set(re.split(r"[;,\s]+", d["row_ids"].strip()))
check("duplicates.different_time", int(m.sum()) == d["n"] and set(sp.loc[m, "row_id"]) == ids and sp.loc[m, "timestamp"].nunique() > 1,
      f"supplier {d['supplier']} amount {d['amount']} rows={int(m.sum())} vs n={d['n']}; distinct timestamps={sp.loc[m, 'timestamp'].nunique()}; row_ids {d['row_ids']}")

if A["contracts"]["contracts_present"]:
    n = pd.read_csv(os.path.join(FULL, "notices-clean.csv"), parse_dates=["start_date", "end_date"])
    ws_start = sp["pay_date"].min()
    # 5 off_contract: top unmatched general_procurement supplier has no exact active notice
    o = T["off_contract"]["unmatched_general_procurement_top20"][0]
    act = n[(n["end_date"].isna()) | (n["end_date"] >= ws_start)]
    s = sp.loc[sp["supplier_norm"] == o["supplier"], "Net amount"].sum()
    check("off_contract", o["supplier"] not in set(act["supplier_norm"]) and close(s * factor, o["annualised_estimate"]),
          f"supplier {o['supplier']} absent from active notice names; annualised {round(s * factor, 2)} vs {o['annualised_estimate']}; sample row_ids {o['row_ids_sample']}")
    # 6 expired_notice_spend
    if T["expired_notice_spend"]["top20"]:
        e = T["expired_notice_spend"]["top20"][0]
        mine = n[n["supplier_norm"] == e["supplier"]]
        check("expired_notice_spend", len(mine) > 0 and bool((mine["end_date"] < ws_start).all()),
              f"supplier {e['supplier']} notices={len(mine)} latest end={mine['end_date'].max().date()} < window start {ws_start.date()}; notice {e['notice_id']}; sample row_ids {e['row_ids_sample']}")
    # 7 spend_vs_award
    if T["spend_vs_award"]["top20"]:
        v = T["spend_vs_award"]["top20"][0]
        nn = n[n["notice_id"] == v["notice_id"]].iloc[0]
        yrs = (nn["end_date"] - nn["start_date"]).days / 365.25
        s = sp.loc[sp["supplier_norm"] == v["supplier"], "Net amount"].sum()
        ratio = s * factor / (nn["awarded_value"] / yrs)
        check("spend_vs_award", abs(ratio - v["ratio"]) < 0.01,
              f"supplier {v['supplier']} notice {v['notice_id']} ratio {round(ratio, 2)} vs {v['ratio']}; sample row_ids {v['row_ids_sample']}")

print(f"{sum(results)}/{len(results)} checks passed")
