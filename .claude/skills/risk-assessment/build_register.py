#!/usr/bin/env python3
"""Validate outputs/risk-ratings.json and render the risk register.

Usage: build_register.py [--ratings outputs/risk-ratings.json] [--rules outputs/rules.json]
       [--analytics outputs/analytics.json] [--history outputs/history.json]
       [--comments outputs/auditor-comments.md] [--out-dir outputs]

The agent judges; this script computes and checks:
  citations   [rule:ID], [metric:$.path] (scalar only) and [history:ID] resolve.
              A risk whose likelihood or impact justification has no resolvable
              citation is dropped (listed under "Excluded"); a citation that does
              not resolve is a failure.
  figures     {{$.path}} placeholders are filled from analytics.json; a figure
              typed in prose (3+ digits or £ and a digit) is a warning.
  names       no supplier name from analytics.json appears in a title,
              statement, justification or proposed focus (warning).
  uplift      a repeat_uplift cites a history audit with an adverse opinion.
  scoring     score = likelihood x impact; matrix label from the council's
              5x5 matrix and band from its RAG table (history.json
              scoring_method); conflicts are marked in the header; fallback
              1-5 Very low..Very high when no usable method.
  revision    when auditor-comments.md holds decisions: every decision is
              applied, nothing else changed, the revision number increases.
Writes outputs/risk-register.md, outputs/auditor-comments.md (decisions kept)
and outputs/register-state.json (the snapshot the next revision is checked
against). Exit 0 when there are no failures.
"""
import argparse, datetime, json, re, sys
from collections import OrderedDict
from pathlib import Path

CITE_RE = re.compile(r"\[(rule|metric|history):((?:[^\[\]]|\[\d+\])+)\]")
PH_RE = re.compile(r"\{\{(\$[^}]+)\}\}")
NUM_RE = re.compile(r"£\s?\d|\b\d{3,}\b")
ADVERSE = re.compile(r"\b(limited|weak|no assurance|minimal)\b", re.I)
FALLBACK_LABELS = {1: "Very low", 2: "Low", 3: "Medium", 4: "High", 5: "Very high"}
REQ = ["id", "title", "statement", "likelihood", "likelihood_justification", "impact",
       "impact_justification", "evidence", "proposed_focus", "sample_source", "recommend_in_scope"]


def jpath(obj, path):
    if not path.startswith("$"):
        return False, None
    cur = obj
    for key, idx in re.findall(r"\.([^.\[\]]+)|\[(\d+)\]", path[1:]):
        try:
            cur = cur[int(idx)] if idx else cur[key]
        except (KeyError, IndexError, TypeError):
            return False, None
    return True, cur


def fmt(v):
    if isinstance(v, bool) or v is None:
        return str(v)
    if isinstance(v, float):
        return f"{v:,.2f}" if v != int(v) else f"{int(v):,}"
    if isinstance(v, int):
        return f"{v:,}"
    return str(v)


def index_ids(node, out=None, parent_key=""):
    """Every dict with an 'id' anywhere in history.json -> (dict, the list it sits in)."""
    out = {} if out is None else out
    if isinstance(node, dict):
        if isinstance(node.get("id"), str):
            out.setdefault(node["id"], (node, parent_key))
        for k, v in node.items():
            index_ids(v, out, k)
    elif isinstance(node, list):
        for v in node:
            index_ids(v, out, parent_key)
    return out


def supplier_names(an):
    names = set()
    def walk(n):
        if isinstance(n, dict):
            for k, v in n.items():
                if k in ("supplier", "supplier_name_original", "supplier_norm") and isinstance(v, str) and len(v) >= 5:
                    names.add(v.upper())
                walk(v)
        elif isinstance(n, list):
            for v in n:
                walk(v)
    walk(an)
    names.discard("REDACTED")
    return names


# ---------------------------------------------------------------- scoring method
def parse_range(text):
    """'15 -25' -> (15, 25); 'Up to 3' -> (1, 3); '8-12' -> (8, 12)."""
    t = str(text)
    m = re.search(r"(\d+)\s*[-–]\s*(\d+)", t)
    if m:
        return int(m.group(1)), int(m.group(2))
    m = re.search(r"up to\s*(\d+)", t, re.I)
    if m:
        return 1, int(m.group(1))
    m = re.search(r"(\d+)\s*(?:\+|or above|and above)", t, re.I)
    if m:
        return int(m.group(1)), 25
    return None


def load_method(hist):
    """Normalise history.json scoring_method into
    {usable, matrix: {(L, I): label}, bands: [(lo, hi, level, escalation, response)],
     crr_threshold, l_labels, i_labels, notes, refs}."""
    sm = hist.get("scoring_method") or {}
    m = {"usable": bool(sm.get("usable")), "matrix": {}, "bands": [], "crr_threshold": None,
         "l_labels": {}, "i_labels": {}, "notes": [], "refs": []}
    for e in sm.get("likelihood_scale") or []:
        if isinstance(e, dict) and "score" in e:
            m["l_labels"][int(e["score"])] = e.get("label", "")
    for e in sm.get("impact_scale") or []:
        if isinstance(e, dict) and "score" in e:
            m["i_labels"][int(e["score"])] = e.get("label", "")
    comb = sm.get("combination") or {}
    cells = comb.get("matrix_cells") or comb.get("matrix") or comb.get("cells") or []
    if isinstance(cells, dict):
        cells = [{"likelihood": int(k.split(",")[0].strip("() LI=")), "impact": int(k.split(",")[1].strip("() LI=")), "label": v}
                 for k, v in cells.items() if "," in k]
    for c in cells if isinstance(cells, list) else []:
        if isinstance(c, dict):
            L = c.get("likelihood") or c.get("L")
            I = c.get("impact") or c.get("I")
            lab = c.get("label") or c.get("matrix_label")
            if L and I and lab:
                m["matrix"][(int(L), int(I))] = lab
        elif isinstance(c, list):  # rows by impact, columns by likelihood
            pass
    rows = comb.get("matrix_by_impact_row") or comb.get("matrix_rows") or comb.get("rows")
    if isinstance(rows, list) and not m["matrix"]:
        for r in rows:
            if isinstance(r, dict) and "impact" in r and isinstance(r.get("labels"), list):
                for L, lab in enumerate(r["labels"], 1):
                    m["matrix"][(L, int(r["impact"]))] = lab
    for b in sm.get("bands") or []:
        if not isinstance(b, dict):
            continue
        rng = b.get("score_range") or b.get("range") or b.get("current_score") or b.get("score")
        lo_hi = (b.get("score_low"), b.get("score_high")) if b.get("score_low") else parse_range(rng)
        if lo_hi and lo_hi[0] is not None:
            m["bands"].append((int(lo_hi[0]), int(lo_hi[1] if lo_hi[1] is not None else 25), b.get("level", ""),
                               b.get("escalation", ""), b.get("response", "")))
    crr = sm.get("corporate_register_threshold")
    if isinstance(crr, dict):   # prefer the register's own inclusion rule (Figure 4) when both are recorded
        crr = (crr.get("figure_4") or {}).get("value") if isinstance(crr.get("figure_4"), dict) else \
              (crr.get("score") or crr.get("value") or crr.get("min_score"))
    mm = re.search(r"\d+", str(crr)) if crr is not None else None
    if mm:
        m["crr_threshold"] = int(mm.group(0))
    top = {d.get("id"): d for d in hist.get("discrepancies") or [] if isinstance(d, dict)}
    for d in sm.get("discrepancies") or []:
        m["notes"].append(top.get(d, {"id": d}) if isinstance(d, str) else d)
    for k in ("likelihood_scale", "impact_scale", "combination", "bands", "corporate_register_threshold"):
        v = sm.get(k)
        if isinstance(v, dict) and v.get("id"):
            m["refs"].append(v["id"])
    if not (m["l_labels"] and m["i_labels"] and m["bands"]):
        m["usable"] = False
    return m


def band_for(method, score):
    for lo, hi, level, esc, resp in method["bands"]:
        if lo <= score <= hi:
            return level, esc, resp
    return None, None, None


# ---------------------------------------------------------------- decisions
def read_comments(path):
    out = {"reviewer": "", "date": "", "rows": OrderedDict()}
    if not path.exists():
        return out
    text = path.read_text(encoding="utf-8")
    m = re.search(r"^Reviewer:[ \t]*(.*)$", text, re.M)
    out["reviewer"] = m.group(1).strip() if m else ""
    m = re.search(r"^Date:[ \t]*(.*)$", text, re.M)
    out["date"] = m.group(1).strip() if m else ""
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 6 and re.fullmatch(r"R-\d+", cells[0]):
            out["rows"][cells[0]] = {"title": cells[1], "now": cells[2], "scope": cells[3],
                                     "decision": cells[4].lower(), "comment": "|".join(cells[5:]).strip()}
    return out


def snapshot(r):
    return {"title": r.get("title"), "statement": r.get("statement"), "likelihood": r.get("likelihood"),
            "impact": r.get("impact"), "recommend_in_scope": r.get("recommend_in_scope"),
            "likelihood_justification": r.get("likelihood_justification"),
            "impact_justification": r.get("impact_justification")}


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ratings", default="outputs/risk-ratings.json")
    ap.add_argument("--rules", default="outputs/rules.json")
    ap.add_argument("--analytics", default="outputs/analytics.json")
    ap.add_argument("--history", default="outputs/history.json")
    ap.add_argument("--comments", default="outputs/auditor-comments.md")
    ap.add_argument("--out-dir", default="outputs")
    a = ap.parse_args()
    out = Path(a.out_dir)
    fails, warns = [], []

    for p in (a.ratings, a.rules, a.analytics, a.history):
        if not Path(p).exists():
            print(f"FAIL  input missing: {p}")
            return 1
    R = json.loads(Path(a.ratings).read_text())
    rules = {r["rule_id"]: r for r in json.loads(Path(a.rules).read_text())["rules"]}
    an = json.loads(Path(a.analytics).read_text())
    hist = json.loads(Path(a.history).read_text())
    hid = index_ids(hist)
    method = load_method(hist)
    names = supplier_names(an)
    dec = read_comments(Path(a.comments))
    state_path = out / "register-state.json"
    prev = json.loads(state_path.read_text()) if state_path.exists() else None

    def resolve(text, where):
        good, bad = [], []
        for kind, ref in CITE_RE.findall(text or ""):
            ref = ref.strip()
            if kind == "rule":
                (good if ref in rules else bad).append(f"rule:{ref}")
            elif kind == "metric":
                found, val = jpath(an, ref)
                if found and not isinstance(val, (dict, list)):
                    good.append(f"metric:{ref}")
                else:
                    bad.append(f"metric:{ref}" + (" (not a scalar)" if found else ""))
            else:
                if ref.startswith("$"):
                    found, val = jpath(hist, ref)
                    (good if found and isinstance(val, dict) and (val.get("source") or val.get("evidence")) else bad).append(f"history:{ref}")
                else:
                    (good if ref in hid else bad).append(f"history:{ref}")
        for b in bad:
            fails.append(f"{where}: citation does not resolve: {b}")
        return good

    def fill(text, where, check_figures=True):
        def sub(m):
            found, val = jpath(an, m.group(1))
            if not found or isinstance(val, (dict, list)):
                fails.append(f"{where}: placeholder not resolvable {m.group(1)}")
                return "«unresolved»"
            return fmt(val)
        filled = PH_RE.sub(sub, text or "")
        if check_figures:
            bare = CITE_RE.sub("", PH_RE.sub("", text or ""))
            if NUM_RE.search(bare):
                warns.append(f"{where}: figure typed in prose; use a {{{{$.path}}}} placeholder: {bare.strip()[:70]!r}")
        return filled

    def name_check(text, where):
        up = (CITE_RE.sub("", text or "")).upper()
        hit = [n for n in names if re.search(rf"(?<![A-Z0-9]){re.escape(n)}(?![A-Z0-9])", up)]
        if hit:
            warns.append(f"{where}: supplier name in text: {sorted(hit)[:3]}")

    # ---- validate risks
    kept, dropped, ids = [], [], set()
    for i, r in enumerate(R.get("risks") or []):
        where = r.get("id", f"risks[{i}]")
        miss = [k for k in REQ if k not in r]
        if miss:
            fails.append(f"{where}: missing fields {miss}")
            continue
        if not re.fullmatch(r"R-\d{2}", r["id"]) or r["id"] in ids:
            fails.append(f"{where}: id must be R-NN and unique")
        ids.add(r["id"])
        for k in ("likelihood", "impact"):
            if not isinstance(r[k], int) or not 1 <= r[k] <= 5:
                fails.append(f"{where}: {k} must be an integer 1-5")
        lc = resolve(r["likelihood_justification"], f"{where}.likelihood")
        ic = resolve(r["impact_justification"], f"{where}.impact")
        for e in r.get("evidence") or []:
            resolve(f"[{e}]", f"{where}.evidence")
        if not lc or not ic:
            dropped.append({"id": r["id"], "title": r["title"],
                            "reason": f"no resolvable citation in the {'likelihood' if not lc else 'impact'} justification"})
            continue
        for k in ("title", "statement", "likelihood_justification", "impact_justification", "proposed_focus"):
            r[f"_{k}"] = fill(r[k], f"{where}.{k}", check_figures=True)
            name_check(r[k], f"{where}.{k}")
        for k in ("title", "statement"):
            if PH_RE.search(r[k]):
                warns.append(f"{where}.{k}: keep titles and statements qualitative (no placeholders)")
        up = r.get("repeat_uplift")
        if up:
            item = hid.get((up or {}).get("history", ""), (None, ""))[0]
            if not item:
                fails.append(f"{where}: repeat_uplift cites unknown history item {up}")
            elif not ADVERSE.search(str(item.get("opinion", "")) + " " + str(item.get("implementation_opinion", ""))):
                fails.append(f"{where}: repeat_uplift cites {up.get('history')}, which has no adverse opinion")
            if "uplift" not in r["likelihood_justification"].lower() and "repeat" not in r["likelihood_justification"].lower():
                warns.append(f"{where}: repeat uplift applied but not stated in the likelihood justification")
        src = r.get("sample_source") or ""
        if src and not (out / "analytics-full" / src).exists():
            fails.append(f"{where}: sample_source {src} not found in analytics-full/")
        L, I = r["likelihood"], r["impact"]
        r["_score"] = L * I
        if method["usable"]:
            r["_label"] = method["matrix"].get((L, I)) or "(not in matrix)"
            lvl, esc, resp = band_for(method, r["_score"])
            r["_band"], r["_esc"], r["_resp"] = lvl or "(no band)", esc or "", resp or ""
            if not lvl:
                warns.append(f"{where}: score {r['_score']} falls in no RAG band of the council's table")
        else:
            r["_label"] = FALLBACK_LABELS[max(1, min(5, round(r["_score"] / 5)))]
            r["_band"], r["_esc"], r["_resp"] = r["_label"], "", ""
        kept.append(r)
    excluded = list(R.get("excluded") or []) + dropped

    # ---- revision against auditor decisions
    decided = {k: v for k, v in dec["rows"].items() if v["decision"]}
    rev = R.get("revision")
    rev_no = None
    if decided:
        if not rev:
            fails.append("auditor-comments.md holds decisions but risk-ratings.json has no revision block")
        else:
            rev_no = rev.get("number")
            last = (prev or {}).get("revision") or 0
            if not isinstance(rev_no, int) or rev_no < last or rev_no < 1:
                fails.append(f"revision.number must be an integer of at least the last built revision ({last}) and 1")
            # compare against the register as it stood before this revision
            before = (prev or {}).get("baseline", {}) if rev_no == last else (prev or {}).get("risks", {})
            changes = {c.get("id"): c for c in rev.get("changes") or []}
            kept_ids = {r["id"] for r in kept}
            excl_ids = {x.get("id") for x in excluded if x.get("id")}
            applied_ref = (prev or {}).get("applied_baseline", {}) if rev_no == last else (prev or {}).get("applied", {})
            new = {rid: d for rid, d in decided.items() if applied_ref.get(rid) != d["decision"]}
            for rid, d in decided.items():
                if d["decision"] not in ("approve", "amend", "reject"):
                    fails.append(f"{rid}: decision {d['decision']!r} is not approve, amend or reject")
                elif d["decision"] == "reject":
                    if rid in kept_ids: fails.append(f"{rid}: rejected by the auditor but still rated")
                    if rid not in excl_ids: fails.append(f"{rid}: rejected but not listed in excluded with the reason")
                    if rid in new and changes.get(rid, {}).get("type") != "rejected":
                        fails.append(f"{rid}: rejection not recorded in revision.changes")
                elif d["decision"] == "amend":
                    if rid not in kept_ids: fails.append(f"{rid}: amended but missing from the register")
                    elif rid in new:
                        if changes.get(rid, {}).get("type") != "amended":
                            fails.append(f"{rid}: amendment not recorded in revision.changes")
                        elif rid in before and snapshot(next(r for r in kept if r["id"] == rid)) == before[rid]:
                            fails.append(f"{rid}: amendment recorded but nothing changed")
                elif d["decision"] == "approve":
                    if rid not in kept_ids: fails.append(f"{rid}: approved but missing from the register")
            for rid, c in changes.items():
                if rid not in new or {"amended": "amend", "rejected": "reject"}.get(c.get("type")) != new[rid]["decision"]:
                    fails.append(f"{rid}: revision.changes lists a {c.get('type')} change the auditor did not ask for in this revision")
            for r in kept:
                rid = r["id"]
                if rid in before and snapshot(r) != before[rid] and new.get(rid, {}).get("decision") != "amend":
                    fails.append(f"{rid}: changed since the last revision but the auditor did not ask for it")
                if rid not in before and before:
                    fails.append(f"{rid}: new risk added in a revision without an auditor request")
            for rid in before:
                if rid not in kept_ids and decided.get(rid, {}).get("decision") != "reject":
                    fails.append(f"{rid}: was in the last register and has disappeared without a rejection")

    # ---- render register
    today = R.get("generated_at") or str(datetime.date.today())
    sources = ", ".join(sorted({x["file"] for x in hist.get("source_documents", []) if x.get("file")}))
    md = ["# Procurement risk register\n"]
    md.append(f"*Generated {today} by `build_register.py` from `risk-ratings.json`, `rules.json`, `analytics.json` and `history.json`.*\n")
    if rev_no:
        who = f" by {dec['reviewer']}" if dec["reviewer"] else ""
        when = f" dated {dec['date']}" if dec["date"] else ""
        ch = rev.get("changes") or []
        what = "; ".join(f"{c['id']} {c['type']}" + (f" ({c['what']})" if c.get("what") else "") for c in ch) or "no ratings changed; decisions recorded"
        md.append(f"*Revision {rev_no}, following auditor comments{who}{when}: {what}.*\n")
    md.append("**Indicators, not findings.** Every risk below describes a pattern in public data or a control the rules "
              "require. Nothing here asserts wrongdoing by the council, a department, an officer or a supplier.\n")
    if method["usable"]:
        md.append("**Scoring method.** Likelihood and impact on the council's own 1–5 scales (Risk Management Strategy "
                  "2024–2027, as extracted into `history.json`); score = likelihood × impact; matrix label from the "
                  "council's 5×5 matrix (Figure 1); band and escalation from its RAG table (Table 4).")
        if method["crr_threshold"] is not None:
            crr_band = [b for b in method["bands"] if "corporate" in str(b[3]).lower()]
            if crr_band and crr_band[0][0] != method["crr_threshold"]:
                md.append(f"**Conflict in the method, not resolved here:** the RAG table escalates to the Corporate Risk "
                          f"Register from a score of {crr_band[0][0]}, while the register inclusion rule says a score of "
                          f"{method['crr_threshold']} or above. Bands below follow the RAG table; the column "
                          f"'Meets register inclusion score' marks the other rule.")
        for n in method["notes"]:
            if isinstance(n, dict) and n.get("id"):
                md.append(f"- Method discrepancy recorded in history.json: [history:{n['id']}] {n.get('what') or n.get('description') or n.get('issue') or ''}".rstrip())
        md.append("")
    else:
        md.append("**Scoring method: fallback.** history.json reports no usable council method; likelihood and impact "
                  "use 1 Very low … 5 Very high and the band is derived from the score.\n")
    md.append("## Summary\n")
    md.append("| ID | Risk | L | I | Score | Matrix label | Band | Meets register inclusion score | Recommended scope |")
    md.append("|---|---|---|---|---|---|---|---|---|")
    for r in kept:
        crr = "yes" if method["crr_threshold"] is not None and r["_score"] >= method["crr_threshold"] else "no"
        md.append(f"| {r['id']} | {r['title']} | {r['likelihood']} | {r['impact']} | {r['_score']} | {r['_label']} | "
                  f"{r['_band']} | {crr} | {'in scope' if r['recommend_in_scope'] else 'out of scope'} |")
    md.append("")
    for r in kept:
        md.append(f"## {r['id']}: {r['title']}\n")
        md.append(f"**Risk.** {r['_statement']}\n")
        ov = " *(auditor override)*" if r.get("auditor_override") else ""
        up = f" *(includes repeat-finding uplift, {r['repeat_uplift']['history']})*" if r.get("repeat_uplift") else ""
        lab = method["l_labels"].get(r["likelihood"], "") if method["usable"] else FALLBACK_LABELS[r["likelihood"]]
        ilab = method["i_labels"].get(r["impact"], "") if method["usable"] else FALLBACK_LABELS[r["impact"]]
        md.append(f"**Likelihood {r['likelihood']} ({lab}).**{ov}{up} {r['_likelihood_justification']}\n")
        md.append(f"**Impact {r['impact']} ({ilab}).** {r['_impact_justification']}\n")
        md.append(f"**Score {r['_score']}: {r['_label']}; band {r['_band']}.**" + (f" Escalation: {r['_esc']}. Response: {r['_resp']}." if r["_esc"] else "") + "\n")
        md.append("**Evidence**\n")
        for e in r.get("evidence") or []:
            kind, ref = e.split(":", 1)
            if kind == "rule" and ref in rules:
                q = rules[ref]["verbatim_quote"]
                ex = q if len(q) <= 140 else q[:140].rsplit(" ", 1)[0] + "…"
                ex = ex.replace('"', "'") if '"' in ex else ex
                md.append(f'- [rule:{ref}] clause {rules[ref]["clause"]}: "{ex}"')
            elif kind == "metric":
                found, val = jpath(an, ref)
                md.append(f"- [metric:{ref}] = {fmt(val) if found else '«unresolved»'}")
            elif kind == "history" and (ref in hid or ref.startswith("$")):
                it = hid[ref][0] if ref in hid else (jpath(hist, ref)[1] or {})
                label = it.get("audit_title") or it.get("theme") or it.get("what") or it.get("label") or it.get("item") or it.get("title") or ""
                if it.get("score") and it.get("label"):
                    label = f"{it['label']} ({it['score']})"
                op = f": {it['opinion']}" if it.get("opinion") else ""
                ev = it if it.get("source") else ((it.get("evidence") or [{}])[0] if isinstance(it.get("evidence"), list) else {})
                md.append(f"- [history:{ref}] {label}{op} ({ev.get('source', '')}, p.{ev.get('pdf_page', '?')})")
        md.append(f"\n**Proposed focus.** {r['_proposed_focus']} Sample source: `analytics-full/{r['sample_source']}`.\n")
    md.append("## Excluded\n")
    if excluded:
        for x in excluded:
            tag = x.get("id") or f"theme {x.get('theme', '?')}"
            md.append(f"- {tag}" + (f": {x['title']}" if x.get("title") else "") + f": {x.get('reason', '')}")
    else:
        md.append("None.")
    md.append("\n## Auditor decisions\n")
    if not decided:
        md.append("None recorded yet. The auditor records approve, amend or reject for each risk in "
                  "`outputs/auditor-comments.md`; the risk-assessor then re-runs and this register becomes a revision.")
    else:
        md.append(f"Recorded by {dec['reviewer'] or 'an unnamed reviewer'}" + (f" on {dec['date']}" if dec["date"] else "") + ".\n")
        md.append("| ID | Decision | Comment | How it was applied |\n|---|---|---|---|")
        for rid, d in dec["rows"].items():
            if not d["decision"]:
                continue
            how = {"approve": "kept as rated", "amend": (rev or {}).get("changes") and next((c.get("what", "amended") for c in rev["changes"] if c.get("id") == rid), "amended"),
                   "reject": "moved to Excluded with the auditor's reason"}.get(d["decision"], "")
            md.append(f"| {rid} | {d['decision']} | {d['comment']} | {how} |")
        open_ = [rid for rid, d in dec["rows"].items() if not d["decision"] and rid in {r['id'] for r in kept}]
        if open_:
            md.append(f"\nStill undecided: {', '.join(open_)}.")
    (out / "risk-register.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # ---- decision template (keeps every decision already recorded)
    t = ["# Auditor decisions on the risk register\n",
         f"Reviewer: {dec['reviewer']}", f"Date: {dec['date']}", "",
         "For each risk write **approve**, **amend** (say what to change) or **reject** (say why) in the Decision "
         "column, with a comment. A blank Decision means undecided. Then ask the risk-assessor to re-run.\n",
         "| ID | Risk | Now | Recommended scope | Decision | Comment |", "|---|---|---|---|---|---|"]
    listed = set()
    for r in kept:
        d = dec["rows"].get(r["id"], {})
        t.append(f"| {r['id']} | {r['title']} | {r['_score']} ({r['_band']}) | {'in scope' if r['recommend_in_scope'] else 'out of scope'} | "
                 f"{d.get('decision', '')} | {d.get('comment', '')} |")
        listed.add(r["id"])
    for rid, d in dec["rows"].items():
        if rid not in listed and d["decision"]:
            t.append(f"| {rid} | {d['title']} | {d['now']} | {d['scope']} | {d['decision']} | {d['comment']} |")
            listed.add(rid)
    lost = [rid for rid, d in dec["rows"].items() if d["decision"] and rid not in listed]
    for rid in lost:
        fails.append(f"{rid}: a recorded decision would be lost from auditor-comments.md")
    (out / "auditor-comments.md").write_text("\n".join(t) + "\n", encoding="utf-8")

    if not fails:
        cur = {r["id"]: snapshot(r) for r in kept}
        applied = {rid: d["decision"] for rid, d in decided.items()}
        last = (prev or {}).get("revision") or 0
        if rev_no and rev_no > last:      # a new revision: the previous build becomes its baseline
            state = {"revision": rev_no, "baseline": (prev or {}).get("risks", {}), "risks": cur,
                     "applied_baseline": (prev or {}).get("applied", {}), "applied": applied}
        elif rev_no:                      # rebuilding the same revision: keep its baseline
            state = {**prev, "risks": cur, "applied": applied}
        else:                             # first run, before any decision
            state = {"revision": 0, "baseline": {}, "risks": cur, "applied_baseline": {}, "applied": {}}
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

    for w in warns: print("WARN ", w)
    for f in fails: print("FAIL ", f)
    print(f"\nrisks rated: {len(kept)}; excluded: {len(excluded)} (dropped for citations: {len(dropped)}); "
          f"method: {'council' if method['usable'] else 'fallback'}; revision: {rev_no or 'none'}; "
          f"decisions recorded: {len([r for r in kept if r['id'] in decided])}/{len(kept)} rated risks"
          f" (+{len([k for k in decided if k not in {r['id'] for r in kept}])} rejected); {len(fails)} failures, {len(warns)} warnings")
    print(f"written: {out / 'risk-register.md'}, {out / 'auditor-comments.md'}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
