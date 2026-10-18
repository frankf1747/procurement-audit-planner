"""Clean spend workbooks and the Contracts Finder notice export.

Writes outputs/analytics-full/{spend-clean.csv, spend-excluded.csv,
notices-clean.csv, cleaning-log.json}. Read-only on data/.
"""
import glob
import json
import os
import re
import sys

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "outputs", "analytics-full")
os.makedirs(OUT, exist_ok=True)

EXPECTED = ["Service", "Expenditure category", "Narrative", "Date",
            "Net amount", "Supplier name"]
STOP_TOKENS = {"LTD", "LIMITED", "PLC", "LLP", "LLC", "INC", "CIC", "CIO",
               "UK", "THE"}

RE_PENSION = r"LGPS|PENSION|SUPERANNUATION"
RE_INTER_SUPPLIER = (r"\b(?:COUNCIL|BOROUGH|COUNTY|CNCL|NHS|POLICE|FIRE AUTHORITY|"
                     r"FIRE AND RESCUE|HMRC|HM REVENUE|DEPARTMENT FOR|MINISTRY OF)\b")
RE_INTER_NARR = r"JOINT ARRANGEMENTS"
PLACEMENT_SERVICES = ("Adult Social Care", "Children's Social Care", "Education")
PLACEMENT_NARR = {"Private Contractors", "Other agencies", "Voluntary Associations"}
RE_GRANT = r"GRANT"
RE_AGENCY = r"AGENCY"
RE_PREMISES = r"RENT|RATES|WATER RATES|LEASE"

COUNCIL_NAMES = {"west berkshire council", "west berkshire"}


def fail(msg):
    print(f"STOP: {msg}")
    sys.exit(1)


def normalise_supplier(name):
    if name is None or (isinstance(name, float) and pd.isna(name)):
        return ""
    s = str(name).upper()
    s = s.replace("&", " AND ")
    s = re.sub(r"\([^)]*\)", " ", s)
    s = re.sub(r"\[[^\]]*\]", " ", s)
    s = re.sub(r"\b(T/AS?|T\.A\.|TRADING AS)(?=\s|$).*$", " ", s)
    s = re.sub(r"['\u2019`]", "", s)  # drop apostrophes so POTTINGER'S -> POTTINGERS
    s = re.sub(r"[^A-Z0-9 ]", " ", s)
    toks = [t for t in s.split() if t not in STOP_TOKENS]
    return " ".join(toks)


def find_header(path):
    raw = pd.read_excel(path, sheet_name="Data to publish", header=None)
    hits = raw.index[raw.iloc[:, 0].astype(str).str.strip() == "Service"].tolist()
    if not hits:
        fail(f"{path}: no row whose first cell is 'Service'")
    return hits[0]


def load_spend():
    files = sorted(glob.glob(os.path.join(DATA, "spend", "*.xlsx")) +
                   glob.glob(os.path.join(DATA, "spend", "*.csv")))
    if not files:
        fail("no spend files in data/spend/")
    frames, per_file = [], {}
    for f in files:
        base = os.path.basename(f)
        if f.endswith(".csv"):
            hdr = 0
            df = pd.read_csv(f)
        else:
            hdr = find_header(f)
            df = pd.read_excel(f, sheet_name="Data to publish", header=hdr)
        df.columns = [str(c).strip() for c in df.columns]
        if list(df.columns) != EXPECTED:
            fail(f"{base}: columns {list(df.columns)} != expected {EXPECTED}")
        df = df.dropna(how="all")
        # sheet row (1-based): header at 0-based index hdr -> sheet row hdr+1;
        # data row with dataframe index i -> sheet row hdr + 2 + i
        df["source_file"] = base
        df["row_id"] = [f"{base}:{hdr + 2 + i}" for i in df.index]
        if not pd.api.types.is_datetime64_any_dtype(df["Date"]):
            parsed = pd.to_datetime(df["Date"], format="%m/%d/%y %H:%M",
                                    errors="coerce")
            alt = pd.to_datetime(df["Date"], format="%m/%d/%Y %H:%M",
                                 errors="coerce")
            parsed = parsed.fillna(alt)
            alt2 = pd.to_datetime(df["Date"], format="%m/%d/%y", errors="coerce")
            df["Date"] = parsed.fillna(alt2)
        per_file[base] = {"header_row_sheet": int(hdr + 1), "rows": int(len(df))}
        frames.append(df)
    spend = pd.concat(frames, ignore_index=True)
    amt = pd.to_numeric(spend["Net amount"], errors="coerce")
    nulls = {
        "date": int(spend["Date"].isna().sum()),
        "amount": int(amt.isna().sum()),
        "supplier": int(spend["Supplier name"].isna().sum()),
    }
    if any(nulls.values()):
        fail(f"null/unparseable values: {nulls}")
    spend["Net amount"] = amt
    neg = int((amt < 0).sum())
    if neg:
        fail(f"{neg} negative amounts present; stopping per method")
    spend["pay_date"] = spend["Date"].dt.normalize()
    spend["timestamp"] = spend["Date"].dt.strftime("%Y-%m-%d %H:%M:%S.%f")
    spend["supplier_norm"] = spend["Supplier name"].map(normalise_supplier)
    return spend, files, per_file


def exclusions(spend):
    sup = spend["Supplier name"].astype(str).str.strip()
    narr = spend["Narrative"].astype(str)
    reason = pd.Series("", index=spend.index)
    redacted = sup.str.upper() == "REDACTED"
    pension = narr.str.upper().str.contains(RE_PENSION, regex=True)
    inter = ((sup.str.upper().str.contains(RE_INTER_SUPPLIER, regex=True) |
              narr.str.upper().str.contains(RE_INTER_NARR, regex=True)) &
             (narr.str.strip() != "Private Contractors"))
    reason[inter] = "inter_authority"
    reason[pension] = "pension_statutory"
    reason[redacted] = "redacted_supplier"
    return reason


REASONS = {
    "redacted_supplier": "Supplier shown as 'Redacted' covers many payees under one label; unusable for supplier-level tests",
    "pension_statutory": "Pension/LGPS/superannuation contributions are statutory, not procurement",
    "inter_authority": "Payments to other public bodies (councils, NHS, police, HMRC, government departments) or joint arrangements, excluding 'Private Contractors' narrative",
}


def tag(df):
    svc = df["Service"].astype(str)
    narr = df["Narrative"].astype(str)
    nu = narr.str.upper()
    placement = svc.str.startswith(PLACEMENT_SERVICES) & narr.str.strip().isin(PLACEMENT_NARR)
    t = pd.Series("general_procurement", index=df.index)
    t[nu.str.contains(RE_PREMISES, regex=True)] = "premises_non_procurement"
    t[nu.str.contains(RE_AGENCY, regex=True)] = "agency_staff"
    t[nu.str.contains(RE_GRANT, regex=True)] = "grant"
    t[placement] = "care_or_education_placement"  # first match wins
    return t


def parse_supplier_blocks(field):
    if not isinstance(field, str) or not field.strip():
        return []
    s = field.strip()
    if s.startswith("["):
        s = s[1:]
    if s.endswith("]"):
        s = s[:-1]
    out = []
    for blk in s.split("]["):
        parts = blk.split("|")
        name = parts[0].strip() if parts else ""
        ch = ""
        if len(parts) >= 4 and parts[2].strip() == "COMPANIES_HOUSE":
            ch = parts[3].strip()
        if name:
            out.append((name, ch))
    return out


def load_contracts(window_start):
    path = os.path.join(DATA, "contracts.csv")
    if not os.path.exists(path):
        return None, {"contracts_present": False}
    c = pd.read_csv(path)
    log = {"contracts_present": True, "rows_in_file": int(len(c)), "warnings": []}
    sup_col = [col for col in c.columns if col.startswith("Supplier [")]
    need = ["Notice Identifier", "Organisation Name", "Title", "OJEU Procedure Type",
            "Awarded Value", "Contract start date", "Contract end date",
            "Awarded Date", "Published Date"]
    missing = [n for n in need if n not in c.columns]
    if missing or len(sup_col) != 1:
        fail(f"contracts.csv missing columns {missing} or packed supplier column")
    sup_col = sup_col[0]
    org = c["Organisation Name"].astype(str).str.strip().str.lower()
    keep = org.isin(COUNCIL_NAMES)
    log["rows_for_council"] = int(keep.sum())
    log["rows_dropped_other_buyers"] = int((~keep).sum())
    log["organisation_names_kept"] = c.loc[keep, "Organisation Name"].value_counts().to_dict()
    log["organisation_names_dropped"] = c.loc[~keep, "Organisation Name"].value_counts().to_dict()
    if len(c) == 1000:
        log["warnings"].append("contracts.csv has exactly 1,000 rows: the Contracts Finder export cap may have truncated it")
    c = c[keep].copy()
    if len(c) < 20:
        log["warnings"].append(f"fewer than 20 council notices ({len(c)}); treated as absent")
        log["contracts_present"] = False
        return None, log
    for col in ["Contract start date", "Contract end date", "Awarded Date"]:
        raw = c[col]
        parsed = pd.to_datetime(raw, format="%d/%m/%Y", errors="coerce")
        bad = int((raw.notna() & parsed.isna()).sum())
        if bad:
            fail(f"contracts.csv: {bad} values in '{col}' fail %d/%m/%Y")
        c[col] = parsed
    pub = pd.to_datetime(c["Published Date"], format="ISO8601", utc=True, errors="coerce")
    if int((c["Published Date"].notna() & pub.isna()).sum()):
        fail("contracts.csv: Published Date fails ISO parse")
    c["Published Date"] = pub
    c["Awarded Value"] = pd.to_numeric(c["Awarded Value"], errors="coerce")
    rows = []
    for _, r in c.iterrows():
        blocks = parse_supplier_blocks(r[sup_col])
        for name, ch in blocks:
            rows.append({
                "notice_id": r["Notice Identifier"], "title": r["Title"],
                "procedure_type": str(r["OJEU Procedure Type"]).strip(),
                "awarded_value": r["Awarded Value"],
                "start_date": r["Contract start date"], "end_date": r["Contract end date"],
                "awarded_date": r["Awarded Date"], "published_date": r["Published Date"],
                "supplier_name": name, "companies_house_no": ch,
                "suppliers_on_notice": len(blocks),
            })
    n = pd.DataFrame(rows)
    n["supplier_norm"] = n["supplier_name"].map(normalise_supplier)
    n["source"] = "contracts_finder"
    n["active"] = n["end_date"].isna() | (n["end_date"] >= window_start)
    n["ended_before_window"] = ~n["active"]
    per_year = c["Published Date"].dt.year.value_counts().sort_index()
    log.update({
        "notices": int(c["Notice Identifier"].nunique()),
        "notices_without_supplier": int(sum(1 for v in c[sup_col] if not parse_supplier_blocks(v))),
        "notice_supplier_pairs": int(len(n)),
        "distinct_suppliers": int(n["supplier_norm"].nunique()),
        "active_pairs": int(n["active"].sum()),
        "ended_pairs": int(n["ended_before_window"].sum()),
        "active_notices": int(n.loc[n["active"], "notice_id"].nunique()),
        "ended_notices": int(n.loc[~n["active"], "notice_id"].nunique()),
        "zero_value_awards": int((c["Awarded Value"].fillna(0) == 0).sum()),
        "rows_per_year": {str(k): int(v) for k, v in per_year.items()},
        "published_range": [str(c["Published Date"].min().date()), str(c["Published Date"].max().date())],
        "procedure_types": c["OJEU Procedure Type"].astype(str).str.strip().value_counts().to_dict(),
    })
    if len(per_year) > 1:
        med = per_year.median()
        thin = [str(y) for y, v in per_year.items() if v < 0.25 * med]
        if thin:
            log["warnings"].append(f"publication years with fewer than a quarter of the median row count: {thin} (partial year or export cap)")
    return n, log


def main():
    spend, files, per_file = load_spend()
    rows_raw = len(spend)
    reason = exclusions(spend)
    spend["tag"] = tag(spend)
    excl = spend[reason != ""].copy()
    excl["exclusion"] = reason[reason != ""]
    clean = spend[reason == ""].copy()

    window_start = spend["pay_date"].min()
    cols = ["row_id", "source_file", "Service", "Expenditure category", "Narrative",
            "Date", "timestamp", "pay_date", "Net amount", "Supplier name",
            "supplier_norm", "tag"]
    clean[cols].to_csv(os.path.join(OUT, "spend-clean.csv"), index=False)
    excl[cols + ["exclusion"]].to_csv(os.path.join(OUT, "spend-excluded.csv"), index=False)

    excluded = {}
    for k, why in REASONS.items():
        m = excl["exclusion"] == k
        excluded[k] = {"rows": int(m.sum()), "gbp": round(float(excl.loc[m, "Net amount"].sum()), 2),
                       "reason": why}

    notices, clog = load_contracts(window_start)
    if notices is not None:
        notices.to_csv(os.path.join(OUT, "notices-clean.csv"), index=False)
    register_present = os.path.exists(os.path.join(DATA, "contract-register.csv"))

    log = {
        "files": [os.path.basename(f) for f in files],
        "per_file": per_file,
        "rows_raw": int(rows_raw),
        "rows_after_exclusions": int(len(clean)),
        "date_min": str(spend["pay_date"].min().date()),
        "date_max": str(spend["pay_date"].max().date()),
        "months_covered": int(spend["pay_date"].dt.to_period("M").nunique()),
        "total_gbp_raw": round(float(spend["Net amount"].sum()), 2),
        "total_gbp_clean": round(float(clean["Net amount"].sum()), 2),
        "excluded": excluded,
        "tags": {t: {"rows": int((clean["tag"] == t).sum()),
                     "gbp": round(float(clean.loc[clean["tag"] == t, "Net amount"].sum()), 2),
                     "suppliers": int(clean.loc[clean["tag"] == t, "supplier_norm"].nunique())}
                 for t in ["care_or_education_placement", "grant", "agency_staff",
                           "premises_non_procurement", "general_procurement"]},
        "regexes": {"pension_statutory": RE_PENSION, "inter_authority_supplier": RE_INTER_SUPPLIER,
                    "inter_authority_narrative": RE_INTER_NARR, "grant": RE_GRANT,
                    "agency_staff": RE_AGENCY, "premises_non_procurement": RE_PREMISES,
                    "placement_services_prefix": list(PLACEMENT_SERVICES),
                    "placement_narratives": sorted(PLACEMENT_NARR)},
        "contracts": clog,
        "register_present": register_present,
    }
    with open(os.path.join(OUT, "cleaning-log.json"), "w") as fh:
        json.dump(log, fh, indent=2, default=str)
    print(json.dumps({k: log[k] for k in ["rows_raw", "rows_after_exclusions", "date_min",
                                          "date_max", "months_covered", "per_file"]}, default=str))
    print("excluded:", json.dumps(excluded))
    print("tags:", json.dumps(log["tags"]))
    print("contracts:", json.dumps({k: v for k, v in clog.items() if k not in ("organisation_names_dropped",)}, default=str))


if __name__ == "__main__":
    main()
