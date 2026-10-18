"""Risk-indicator tests over outputs/analytics-full/spend-clean.csv.

Thresholds come only from outputs/rules.json. Writes outputs/analytics.json
and full lists to outputs/analytics-full/. Indicators, not findings.
"""
import datetime as dt
import difflib
import json
import os
import re
import sys

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "outputs")
FULL = os.path.join(OUT, "analytics-full")
TAGS = ["general_procurement", "care_or_education_placement", "grant",
        "agency_staff", "premises_non_procurement"]
RE_COMPETITION = re.compile(r"QUOT|TENDER", re.I)
RE_PUBLICATION = re.compile(r"CONTRACT NOTICE|CONTRACTS FINDER|\bCDP\b", re.I)
GENERIC = set("""AND OF THE SERVICES SERVICE GROUP CARE COMPANY HOMES HOME HOUSE
UNIVERSITY COUNCIL TRUST SOLUTIONS CONSULTANCY CONSULTING ASSOCIATES PARTNERSHIP
NETWORK CENTRE CENTER TRAVEL CARS COACHES TAXIS CONSTRUCTION HEALTHCARE HEALTH
SCHOOL SCHOOLS EDUCATION SUPPORT LIVING CHILDREN CHILDRENS SEN BERKSHIRE WEST
SOUTH NORTH EAST READING NEWBURY THATCHAM HUNGERFORD SOUTHERN SYSTEMS SOFTWARE
HOUSING SECURITY CLEANING FOSTERING COMMUNITY BUSINESS MANAGEMENT FACILITIES
SUPPLIES CATERING TRANSPORT ENGINEERING HIRE PROPERTY PROPERTIES VALLEY""".split())
CAVEAT = ("contracts.csv holds published notices, not a contract register. It holds "
          "awards published on Contracts Finder in roughly the last five years. A "
          "contract awarded earlier (e.g. long-running waste or highways contracts), "
          "one advertised only on Find a Tender, a framework call-off recorded under "
          "another buyer, or an exempt placement will have no notice here. \"No "
          "notice found\" is therefore an indicator to check against the council's "
          "contract register, never evidence of off-contract spend.")


def fail(msg):
    print(f"STOP: {msg}")
    sys.exit(1)


def r2(x):
    return round(float(x), 2)


# ---------------------------------------------------------------- rules
def load_rules():
    p = os.path.join(OUT, "rules.json")
    if not os.path.exists(p):
        fail("outputs/rules.json missing")
    d = json.load(open(p))
    return d


def rule_by_clause(rules, clause):
    return [r["rule_id"] for r in rules if r["clause"] == clause]


def derive_thresholds(d):
    rules = [r for r in d["rules"] if r["type"] in ("threshold", "approver", "anti-avoidance")]
    acc = {}
    for r in rules:
        for side in ("low", "high"):
            v = r.get(f"threshold_{side}")
            if v is None:
                continue
            e = acc.setdefault(float(v), {"value": v, "rule_ids": [], "low_inclusive": set(),
                                          "high_inclusive": set(), "competition_rule_ids": [],
                                          "publication_rule_ids": []})
            e["rule_ids"].append(r["rule_id"])
            e[f"{side}_inclusive"].add(r.get(f"threshold_{side}_inclusive"))
            if RE_COMPETITION.search(r.get("required_action") or ""):
                e["competition_rule_ids"].append(r["rule_id"])
            if side == "low" and RE_PUBLICATION.search(r.get("required_action") or ""):
                e["publication_rule_ids"].append(r["rule_id"])
    out, warnings = [], []
    for v in sorted(acc):
        e = acc[v]
        lows = {x for x in e["low_inclusive"] if x is not None}
        highs = {x for x in e["high_inclusive"] if x is not None}
        # "inclusive" = an amount equal to the threshold is in the triggered band
        if lows:
            inclusive = True in lows if len(lows) == 1 else True
            if len(lows) > 1:
                warnings.append(f"{v}: conflicting lower-bound inclusivity across rules; treated as inclusive")
        elif highs:
            inclusive = (False in highs) if len(highs) == 1 else True
            if len(highs) > 1:
                warnings.append(f"{v}: conflicting upper-bound inclusivity across rules; treated as inclusive")
        else:
            inclusive = True
        if any(l == h for l in lows for h in highs):
            warnings.append(f"{v}: lower-bound and upper-bound inclusivity overlap or leave a gap at exactly this value (see rules.json notes)")
        out.append({"value": e["value"], "inclusive": inclusive,
                    "competition_triggering": bool(e["competition_rule_ids"]),
                    "publication_rule_ids": sorted(set(e["publication_rule_ids"])),
                    "rule_ids": sorted(set(e["rule_ids"])),
                    "competition_rule_ids": sorted(set(e["competition_rule_ids"]))})
    return out, warnings


def triggered(amount, t):
    return amount >= t["value"] if t["inclusive"] else amount > t["value"]


def below(amount, t):
    return ~triggered(amount, t)


# ---------------------------------------------------------------- matching
def distinct_tokens(name):
    return {t for t in name.split() if t not in GENERIC and len(t) >= 3}


def build_matcher(spend_names, notice_names):
    sp_tok = {n: distinct_tokens(n) for n in spend_names}
    no_tok = {n: distinct_tokens(n) for n in notice_names}
    sp_count, no_count = {}, {}
    for toks, cnt in ((sp_tok, sp_count), (no_tok, no_count)):
        for ts in toks.values():
            for t in ts:
                cnt[t] = cnt.get(t, 0) + 1
    nset = set(notice_names)

    def match_supplier(name):
        if not name:
            return "none", "", ""
        if name in nset:
            return "exact", name, "normalised names equal"
        best, bestr = "", 0.0
        for n in notice_names:
            r = difflib.SequenceMatcher(None, name, n).ratio()
            if r > bestr:
                best, bestr = n, r
        if bestr >= 0.85:
            return "near_ratio", best, f"SequenceMatcher ratio {bestr:.3f}"
        a = sp_tok[name]
        for n in notice_names:
            b = no_tok[n]
            if not a or not b:
                continue
            small, large = (a, b) if len(a) <= len(b) else (b, a)
            if small <= large:
                if len(small) >= 2:
                    return "near_contain", n, f"distinctive tokens {sorted(small)} subset (>=2 tokens)"
                tok = next(iter(small))
                if sp_count.get(tok) == 1 and no_count.get(tok) == 1:
                    return "near_contain", n, f"unique single distinctive token {tok}"
        return "none", "", ""
    return match_supplier


# ---------------------------------------------------------------- tests
def tag_split(df, amount_col="Net amount"):
    return {t: {"rows": int((df["tag"] == t).sum()),
                "gbp": r2(df.loc[df["tag"] == t, amount_col].sum())} for t in TAGS}


def threshold_clustering(sp, thresholds):
    res, frames = {}, []
    for t in thresholds:
        T = float(t["value"])
        a = sp["Net amount"]
        band = (a >= 0.9 * T) & below(a, t)
        comp = triggered(a, t) & (a < 1.1 * T)
        base = (a >= 0.5 * T) & (a < 1.5 * T)
        b = sp[band].copy()
        b["threshold"] = t["value"]
        frames.append(b)
        conc = (b.groupby("supplier_norm")["Net amount"].agg(["count", "sum"])
                .sort_values(["count", "sum"], ascending=False).head(20))
        res[str(t["value"])] = {
            "threshold": t["value"], "inclusive": t["inclusive"], "rule_ids": t["rule_ids"],
            "band_definition": f"0.9*T <= amount {'<' if t['inclusive'] else '<='} T",
            "band": {"count": int(band.sum()), "gbp": r2(sp.loc[band, "Net amount"].sum())},
            "comparator_above": {"definition": f"T {'<=' if t['inclusive'] else '<'} amount < 1.1*T",
                                 "count": int(comp.sum()), "gbp": r2(sp.loc[comp, "Net amount"].sum())},
            "baseline_0.5T_to_1.5T": {"count": int(base.sum()), "gbp": r2(sp.loc[base, "Net amount"].sum())},
            "by_tag": tag_split(b),
            "supplier_concentration_top20": [
                {"supplier": s, "count": int(r["count"]), "gbp": r2(r["sum"])} for s, r in conc.iterrows()],
            "top20": [{"row_id": r["row_id"], "supplier": r["Supplier name"], "amount": r2(r["Net amount"]),
                       "date": str(r["pay_date"])[:10], "service": r["Service"], "tag": r["tag"]}
                      for _, r in b.sort_values("Net amount", ascending=False).head(20).iterrows()],
        }
    allb = pd.concat(frames) if frames else sp.head(0)
    allb.to_csv(os.path.join(FULL, "threshold-clustering.csv"), index=False)
    return {"name": "payments within 10% below each threshold in rules.json",
            "parameters": {"band_low_factor": 0.9, "comparator_high_factor": 1.1,
                           "baseline": [0.5, 1.5]},
            "file": "outputs/analytics-full/threshold-clustering.csv", "by_threshold": res}


def split_purchases(sp, thresholds, anti_ids):
    res, all_rows = {}, []
    for t in [x for x in thresholds if x["competition_triggering"]]:
        T = float(t["value"])
        sub = sp[below(sp["Net amount"], t)].sort_values("pay_date")
        best = {}
        for sup, g in sub.groupby("supplier_norm"):
            if len(g) < 2:
                continue
            dates = g["pay_date"].values
            amts = g["Net amount"].values
            for i in range(len(g)):
                end = dates[i] + pd.Timedelta(days=30).to_timedelta64()
                m = (dates >= dates[i]) & (dates < end)
                if m.sum() < 2:
                    continue
                tot = amts[m].sum()
                if not triggered(pd.Series([tot]), t).iloc[0]:
                    continue
                if sup not in best or tot > best[sup][0]:
                    best[sup] = (tot, g[m])
        rows = []
        for sup, (tot, w) in best.items():
            tg = w.groupby("tag")["Net amount"].sum()
            rows.append({"threshold": t["value"], "supplier": sup,
                         "supplier_name_original": w["Supplier name"].iloc[0],
                         "window_start": str(w["pay_date"].min())[:10],
                         "window_end": str(w["pay_date"].max())[:10],
                         "n_payments": int(len(w)), "window_total": r2(tot),
                         "distinct_amounts": int(w["Net amount"].round(2).nunique()),
                         "services": "; ".join(sorted(w["Service"].astype(str).unique())),
                         "dominant_tag": tg.idxmax(), "mixed_tags": bool(len(tg) > 1),
                         "row_ids": "; ".join(w["row_id"])})
        df = pd.DataFrame(rows)
        all_rows.append(df)
        if df.empty:
            res[str(t["value"])] = {"threshold": t["value"], "windows": 0}
            continue
        by_tag = {tg: {"windows": int((df["dominant_tag"] == tg).sum()),
                       "gbp": r2(df.loc[df["dominant_tag"] == tg, "window_total"].sum())} for tg in TAGS}
        gp = df[df["dominant_tag"] == "general_procurement"]
        pl = df[df["dominant_tag"] == "care_or_education_placement"]
        cols = ["supplier", "window_start", "window_end", "n_payments", "window_total",
                "distinct_amounts", "services", "row_ids"]
        res[str(t["value"])] = {
            "threshold": t["value"], "inclusive": t["inclusive"],
            "rule_ids": sorted(set(anti_ids + t["rule_ids"])),
            "windows": int(len(df)), "distinct_suppliers": int(df["supplier"].nunique()),
            "gbp": r2(df["window_total"].sum()), "by_tag": by_tag,
            "headline_general_procurement": {"windows": int(len(gp)), "gbp": r2(gp["window_total"].sum()),
                                             "top20": gp.sort_values("window_total", ascending=False).head(20)[cols].to_dict("records")},
            "care_or_education_placement": {"windows": int(len(pl)), "gbp": r2(pl["window_total"].sum()),
                                            "note": "periodic care fees legitimately recur; separate from headline",
                                            "top20": pl.sort_values("window_total", ascending=False).head(20)[cols].to_dict("records")},
        }
    full = pd.concat(all_rows) if all_rows else pd.DataFrame()
    full.to_csv(os.path.join(FULL, "split-purchases.csv"), index=False)
    return {"name": "same supplier, 2+ sub-threshold payments within 30 calendar days totalling at or over a competition-triggering threshold",
            "parameters": {"window_days": 30, "min_payments": 2,
                           "window_anchor": "each payment date, next 30 calendar days",
                           "dedup": "highest-total window per supplier per threshold",
                           "payments_considered": "only payments individually below the threshold"},
            "file": "outputs/analytics-full/split-purchases.csv", "by_threshold": res}


def supplier_totals(sp, factor):
    g = sp.groupby("supplier_norm")
    tot = g["Net amount"].sum()
    by_tag = sp.pivot_table(index="supplier_norm", columns="tag", values="Net amount",
                            aggfunc="sum", fill_value=0)
    df = pd.DataFrame({
        "total_gbp": tot.round(2),
        "annualised_estimate": (tot * factor).round(2),
        "n_payments": g.size(),
        "supplier_name_original": g["Supplier name"].agg(lambda s: s.value_counts().index[0]),
        "narratives": g["Narrative"].agg(lambda s: "; ".join(s.astype(str).value_counts().index[:3])),
        "services": g["Service"].agg(lambda s: "; ".join(s.astype(str).value_counts().index[:3])),
        "dominant_tag": by_tag.idxmax(axis=1),
        "spans_tags": (by_tag > 0).sum(axis=1) > 1,
        "row_ids_sample": g["row_id"].agg(lambda s: "; ".join(s.head(5))),
    })
    return df


def high_value(st, t_comp, t_pub, statutory_param):
    tiers, skipped = {}, []
    hv_cols = ["supplier_name_original", "annualised_estimate", "total_gbp", "n_payments",
               "narratives", "services", "spans_tags", "row_ids_sample"]
    for label, t in (("lowest_competition_threshold", t_comp), ("publication_threshold", t_pub)):
        if t is None:
            skipped.append({"test": "high_value_suppliers", "tier": label, "reason": "no such threshold in rules.json"})
            continue
        m = triggered(st["annualised_estimate"], t)
        sel = st[m]
        tables = {}
        for tg in TAGS:
            s = sel[sel["dominant_tag"] == tg].sort_values("annualised_estimate", ascending=False)
            tables[tg] = {"suppliers": int(len(s)), "gbp_in_window": r2(s["total_gbp"].sum()),
                          "annualised_estimate": r2(s["annualised_estimate"].sum())}
            if label == "publication_threshold":
                tables[tg]["top20"] = [dict(supplier=i, **{k: (r2(v) if isinstance(v, float) else (bool(v) if k == "spans_tags" else v)) for k, v in r.items()})
                                       for i, r in s.head(20)[hv_cols].iterrows()]
        tiers[label] = {"threshold": t["value"], "inclusive": t["inclusive"], "rule_ids": t["rule_ids"],
                        "suppliers": int(m.sum()), "annualised_estimate": r2(sel["annualised_estimate"].sum()),
                        "by_dominant_tag": tables,
                        "headline_general_procurement_suppliers": tables["general_procurement"]["suppliers"]}
    if statutory_param is None:
        skipped.append({"test": "high_value_suppliers", "tier": "statutory",
                        "reason": "rules.json parameter threshold_goods_services is null"})
    return tiers, skipped


def duplicates(sp):
    d = sp.copy()
    d["pence"] = (d["Net amount"] * 100).round().astype("int64")
    d = d.sort_values(["supplier_norm", "pence", "pay_date", "timestamp"])
    gid, prev, cur = [], None, -1
    for r in d[["supplier_norm", "pence", "pay_date"]].itertuples(index=False):
        if prev is None or r[0] != prev[0] or r[1] != prev[1] or (r[2] - prev[2]).days > 7:
            cur += 1
        gid.append(cur)
        prev = r
    d["group"] = gid
    size = d.groupby("group")["row_id"].transform("size")
    d = d[size >= 2].copy()
    nts = d.groupby("group")["timestamp"].transform("nunique")
    d["tier"] = (nts == 1).map({True: "same_timestamp", False: "different_time"})
    d.drop(columns=["pence"]).to_csv(os.path.join(FULL, "duplicates.csv"), index=False)
    out = {}
    for tier in ["same_timestamp", "different_time"]:
        x = d[d["tier"] == tier]
        g = x.groupby("group").agg(supplier=("supplier_norm", "first"), amount=("Net amount", "first"),
                                   n=("row_id", "size"), tag=("tag", "first"),
                                   first_date=("pay_date", "min"), last_date=("pay_date", "max"),
                                   row_ids=("row_id", "; ".join))
        g["beyond_first"] = g["amount"] * (g["n"] - 1)
        out[tier] = {
            "groups": int(len(g)), "rows": int(len(x)), "gbp_beyond_first": r2(g["beyond_first"].sum()),
            "by_tag": {tg: {"groups": int((g["tag"] == tg).sum()),
                            "gbp_beyond_first": r2(g.loc[g["tag"] == tg, "beyond_first"].sum())} for tg in TAGS},
            "top20": [{"supplier": r.supplier, "amount": r2(r.amount), "n": int(r.n), "tag": r.tag,
                       "first_date": str(r.first_date)[:10], "last_date": str(r.last_date)[:10],
                       "gbp_beyond_first": r2(r.beyond_first), "row_ids": r.row_ids}
                      for r in g.sort_values("amount", ascending=False).head(20).itertuples()],
        }
    return {"name": "same supplier, same amount to the penny, calendar dates within 7 days",
            "parameters": {"days": 7, "amount_match": "to the penny",
                           "grouping": "chained: consecutive payments of the same supplier and amount no more than 7 days apart",
                           "tiers": {"same_timestamp": "every row in the group has the identical Date timestamp",
                                     "different_time": "group spans more than one timestamp (higher signal)"}},
            "file": "outputs/analytics-full/duplicates.csv", **out}


# ---------------------------------------------------------------- main
def main():
    d = load_rules()
    rules = d["rules"]
    thresholds, th_warn = derive_thresholds(d)
    log = json.load(open(os.path.join(FULL, "cleaning-log.json")))
    sp = pd.read_csv(os.path.join(FULL, "spend-clean.csv"), parse_dates=["pay_date"])
    sp["supplier_norm"] = sp["supplier_norm"].fillna("")
    months = log["months_covered"]
    factor = 12 / months
    params = d.get("parameters", {})
    skipped = []
    for k, p in params.items():
        if p.get("value") is None:
            skipped.append({"test": "threshold_clustering, split_purchases, high_value_suppliers, off_contract",
                            "tier": k, "reason": f"rules.json parameter {k} is null ({p.get('printed_as')}); rules bounded by it are not tested at that figure"})

    anti_ids = [r["rule_id"] for r in rules if r["type"] == "anti-avoidance"]
    comp = [t for t in thresholds if t["competition_triggering"]]
    t_comp = comp[0] if comp else None
    pubs = [t for t in thresholds if t["publication_rule_ids"]]
    t_pub = pubs[0] if pubs else None

    tests = {}
    tests["threshold_clustering"] = threshold_clustering(sp, thresholds)
    tests["split_purchases"] = split_purchases(sp, thresholds, anti_ids)

    st = supplier_totals(sp, factor)
    tiers, sk = high_value(st, t_comp, t_pub, params.get("threshold_goods_services", {}).get("value"))
    skipped += sk
    st.to_csv(os.path.join(FULL, "supplier-totals.csv"))
    tests["high_value_suppliers"] = {
        "name": "suppliers whose annualised estimate is at or over a threshold",
        "parameters": {"annualisation_factor": factor, "months_covered": months,
                       "field_label": "annualised estimate",
                       "headline_tier": "publication_threshold",
                       "method_note": ("The lowest competition-triggering threshold (App B row A, one quote) "
                                       "is below the smallest possible annualised estimate in an over-£500 "
                                       "population, so that tier selects nearly every supplier; it is "
                                       "reported as counts only. The headline uses the lowest threshold whose "
                                       "rule requires publishing a contract notice, which is also the floor "
                                       "below which Contracts Finder carries no notices.")},
        "rule_ids": sorted(set((t_pub or {}).get("rule_ids", []))),
        "file": "outputs/analytics-full/high-value-suppliers.csv", "tiers": tiers}

    contracts_present = bool(log["contracts"].get("contracts_present"))
    register_present = bool(log.get("register_present"))
    matching = {}
    row_e = rule_by_clause(rules, "App C row E")
    row_d = rule_by_clause(rules, "App C row D")
    row_f = rule_by_clause(rules, "App C row F")
    hv_pub = st[triggered(st["annualised_estimate"], t_pub)].copy() if t_pub else st.head(0)
    if contracts_present or register_present:
        n = pd.read_csv(os.path.join(FULL, "notices-clean.csv"), parse_dates=["start_date", "end_date"])
        n["supplier_norm"] = n["supplier_norm"].fillna("")
        active = n[n["active"]]
        ended = n[~n["active"]]
        active_names = sorted(set(active["supplier_norm"]) - {""})
        matcher = build_matcher(sorted(set(st.index)), active_names)
        mrows = []
        for s in st.index:
            cls, cand, why = matcher(s)
            mrows.append({"supplier": s, "match_class": cls, "candidate": cand, "rule_fired": why})
        mdf = pd.DataFrame(mrows).set_index("supplier")
        mdf.join(st[["supplier_name_original", "annualised_estimate", "dominant_tag"]]).to_csv(
            os.path.join(FULL, "supplier-match.csv"))
        near = mdf[mdf["match_class"].str.startswith("near")].join(st[["supplier_name_original", "annualised_estimate"]])
        near.to_csv(os.path.join(FULL, "near-matches.csv"))
        vc = mdf["match_class"].value_counts()
        matching = {c: int(vc.get(c, 0)) for c in ["exact", "near_ratio", "near_contain", "none"]}
        matching["near_matches_file"] = "outputs/analytics-full/near-matches.csv"
        matching["note"] = "near matches are candidates for the auditor to confirm and are not counted as matches"

        hv_pub = hv_pub.join(mdf)
        unmatched = hv_pub[hv_pub["match_class"] != "exact"]
        per_class = {c: {"suppliers": int((hv_pub["match_class"] == c).sum()),
                         "annualised_estimate": r2(hv_pub.loc[hv_pub["match_class"] == c, "annualised_estimate"].sum())}
                     for c in ["exact", "near_ratio", "near_contain", "none"]}
        un_tag = {tg: {"suppliers": int((unmatched["dominant_tag"] == tg).sum()),
                       "annualised_estimate": r2(unmatched.loc[unmatched["dominant_tag"] == tg, "annualised_estimate"].sum())}
                  for tg in TAGS}
        ug = unmatched[unmatched["dominant_tag"] == "general_procurement"].sort_values("annualised_estimate", ascending=False)
        tests["off_contract"] = {
            "name": "suppliers at or over the publication threshold (annualised estimate) with no exact-match notice among active notices",
            "contracts_present": contracts_present, "register_present": register_present,
            "caveat": CAVEAT,
            "scope_note": "Only suppliers at or above the publication threshold are classed; Contracts Finder does not carry smaller awards, so results must never be used to question smaller suppliers.",
            "parameters": {"threshold": t_pub["value"] if t_pub else None, "match_set": "active notices (end date on/after spend window start, or blank)"},
            "rule_ids": sorted(set((t_pub or {}).get("rule_ids", []) + row_f)),
            "placement_note": f"care and education placements may be exempt from competition under App C row F ({', '.join(row_f)})",
            "per_match_class": per_class, "unmatched_by_tag": un_tag,
            "unmatched_general_procurement_top20": [
                {"supplier": i, "supplier_name_original": r["supplier_name_original"],
                 "annualised_estimate": r2(r["annualised_estimate"]), "match_class": r["match_class"],
                 "candidate": r["candidate"], "row_ids_sample": r["row_ids_sample"]}
                for i, r in ug.head(20).iterrows()],
            "file": "outputs/analytics-full/high-value-suppliers.csv"}
        if t_pub is None:
            skipped.append({"test": "off_contract", "tier": "publication", "reason": "no publication threshold in rules.json"})
        skipped.append({"test": "off_contract", "tier": "statutory", "reason": "rules.json parameter threshold_goods_services is null"})

        # expired_notice_spend
        ended_names = set(ended["supplier_norm"]) - {""}
        active_set = set(active_names)
        exp = st[[s in ended_names and s not in active_set for s in st.index]].copy()
        info = ended.sort_values("end_date").groupby("supplier_norm").agg(
            latest_end_date=("end_date", "max"), notice_id=("notice_id", "last"),
            procedure_type=("procedure_type", "last"))
        exp = exp.join(info)
        exp.sort_values("annualised_estimate", ascending=False).to_csv(os.path.join(FULL, "expired-notice-spend.csv"))
        window_start = sp["pay_date"].min()
        tests["expired_notice_spend"] = {
            "name": "suppliers paid in the window whose every exact-match notice ended before the window started",
            "parameters": {"window_start": str(window_start)[:10], "match": "exact"},
            "rule_ids": row_d, "caveat": CAVEAT + " A newer contract or approved extension may exist with no notice.",
            "suppliers": int(len(exp)), "gbp_in_window": r2(exp["total_gbp"].sum()),
            "annualised_estimate": r2(exp["annualised_estimate"].sum()),
            "by_dominant_tag": {tg: int((exp["dominant_tag"] == tg).sum()) for tg in TAGS},
            "top20": [{"supplier": i, "annualised_estimate": r2(r["annualised_estimate"]),
                       "latest_end_date": str(r["latest_end_date"])[:10], "notice_id": r["notice_id"],
                       "procedure_type": r["procedure_type"], "row_ids_sample": r["row_ids_sample"]}
                      for i, r in exp.sort_values("annualised_estimate", ascending=False).head(20).iterrows()],
            "file": "outputs/analytics-full/expired-notice-spend.csv"}

        # spend_vs_award
        cand = active[(active["suppliers_on_notice"] == 1) & (active["awarded_value"] > 0) &
                      active["start_date"].notna() & active["end_date"].notna()].copy()
        cand["contract_years"] = (cand["end_date"] - cand["start_date"]).dt.days / 365.25
        cand = cand[cand["contract_years"] > 0]
        cand["award_annual_rate"] = cand["awarded_value"] / cand["contract_years"]
        cnt = cand.groupby("supplier_norm").size()
        multi = sorted(cnt[cnt > 1].index)
        one = cand[cand["supplier_norm"].isin(cnt[cnt == 1].index)].set_index("supplier_norm")
        sva = st.join(one[["notice_id", "awarded_value", "contract_years", "award_annual_rate", "start_date", "end_date"]], how="inner")
        sva["ratio"] = sva["annualised_estimate"] / sva["award_annual_rate"]
        sva.sort_values("ratio", ascending=False).to_csv(os.path.join(FULL, "spend-vs-award.csv"))
        flag = sva[sva["ratio"] >= 1.25]
        tests["spend_vs_award"] = {
            "name": "annualised estimate at or over 1.25x the award's annual rate (exact match, one active single-supplier notice, Awarded Value > 0)",
            "parameters": {"ratio_flag": 1.25, "contract_years": "(end - start) days / 365.25"},
            "rule_ids": row_e,
            "caveat": "Awarded Value may be an estimate or maximum; ratios are indicators of spend beyond the award to check against approved variations.",
            "suppliers_compared": int(len(sva)), "suppliers_flagged": int(len(flag)),
            "suppliers_with_multiple_candidate_notices_skipped": len(multi),
            "flagged_annualised_estimate": r2(flag["annualised_estimate"].sum()),
            "top20": [{"supplier": i, "notice_id": r["notice_id"], "ratio": round(float(r["ratio"]), 2),
                       "annualised_estimate": r2(r["annualised_estimate"]), "awarded_value": r2(r["awarded_value"]),
                       "contract_years": round(float(r["contract_years"]), 2), "row_ids_sample": r["row_ids_sample"]}
                      for i, r in flag.sort_values("ratio", ascending=False).head(20).iterrows()],
            "file": "outputs/analytics-full/spend-vs-award.csv"}
    else:
        reason = "no contracts.csv or contract register in data/"
        for k in ("off_contract", "expired_notice_spend", "spend_vs_award"):
            tests[k] = {"skipped": True, "reason": reason}
            skipped.append({"test": k, "tier": "all", "reason": reason})
    hv_pub.to_csv(os.path.join(FULL, "high-value-suppliers.csv"))

    tests["duplicates"] = duplicates(sp)

    cl = log["contracts"]
    analytics = {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "scripts": ["scripts/clean.py", "scripts/analyse.py"],
        "population": {"files": log["files"], "rows_raw": log["rows_raw"],
                       "rows_after_exclusions": log["rows_after_exclusions"],
                       "date_min": log["date_min"], "date_max": log["date_max"],
                       "months_covered": months, "annualisation_factor": factor,
                       "total_gbp": log["total_gbp_clean"], "total_gbp_raw": log["total_gbp_raw"],
                       "excluded": log["excluded"], "tags": log["tags"],
                       "tag_rule_ids": {"care_or_education_placement": row_f,
                                        "grant": "clause 1.6.2 (grant treated as a contract; rows tagged, not excluded)"},
                       "limitations": ["population is expenditure over £500 only; split-purchase and duplicate results are lower bounds",
                                       "Date is a payment-run timestamp, not an invoice date; window logic uses calendar dates",
                                       "Redacted supplier rows are excluded from all supplier-level tests"]},
        "thresholds": [{k: t[k] for k in ("value", "inclusive", "competition_triggering", "rule_ids", "publication_rule_ids")}
                       for t in thresholds],
        "threshold_warnings": th_warn,
        "skipped": skipped,
        "contracts": {"contracts_present": contracts_present, "register_present": register_present,
                      "rows_in_file": cl.get("rows_in_file", 0), "rows_for_council": cl.get("rows_for_council", 0),
                      "notice_supplier_pairs": cl.get("notice_supplier_pairs", 0),
                      "distinct_suppliers": cl.get("distinct_suppliers", 0),
                      "active_in_window": cl.get("active_notices", 0), "ended_before_window": cl.get("ended_notices", 0),
                      "active_pairs": cl.get("active_pairs", 0), "ended_pairs": cl.get("ended_pairs", 0),
                      "zero_value_awards": cl.get("zero_value_awards", 0), "rows_per_year": cl.get("rows_per_year", {}),
                      "published_range": cl.get("published_range", ["", ""]), "warnings": cl.get("warnings", []),
                      "caveat": CAVEAT},
        "matching": matching,
        "tests": tests,
    }
    with open(os.path.join(OUT, "analytics.json"), "w") as fh:
        json.dump(analytics, fh, indent=2, default=str)

    # terse headline print
    print("thresholds:", [(t["value"], t["inclusive"], t["competition_triggering"]) for t in thresholds])
    print("threshold warnings:", th_warn)
    for k, v in tests["threshold_clustering"]["by_threshold"].items():
        print("cluster", k, v["band"], "above:", v["comparator_above"]["count"])
    for k, v in tests["split_purchases"]["by_threshold"].items():
        print("split", k, v.get("windows"), v.get("gbp"), "GP:", {x: v["headline_general_procurement"][x] for x in ("windows", "gbp")} if v.get("windows") else "")
    for k, v in tiers.items():
        print("hv", k, v["suppliers"], v["annualised_estimate"], "GP:", v["headline_general_procurement_suppliers"])
    print("matching:", matching)
    for k in ("off_contract", "expired_notice_spend", "spend_vs_award"):
        v = tests[k]
        print(k, {x: v[x] for x in v if x in ("per_match_class", "suppliers", "annualised_estimate", "suppliers_compared", "suppliers_flagged", "flagged_annualised_estimate", "suppliers_with_multiple_candidate_notices_skipped")})
    for tier in ("same_timestamp", "different_time"):
        v = tests["duplicates"][tier]
        print("dup", tier, v["groups"], v["rows"], v["gbp_beyond_first"])


if __name__ == "__main__":
    main()
