#!/usr/bin/env python3
"""Verify a rules.json produced by the extract-rules skill against the PDF.

Usage: verify_quotes.py RULES_JSON PDF_PATH

Checks
  1. Top level: JSON object with source, parameters, rules, excluded, notes;
     source.sha256 matches the PDF and source.pages its page count.
  2. Schema: every rule has every field with the right type and an allowed
     value; thresholds are as-printed numbers with inclusive flags; approver
     rules name an approver; at least one anti-avoidance rule exists.
  3. rule_ids are unique and sequential: CPR-01, CPR-02, ... with no gaps.
  4. Parameters: every *_ref names a declared parameter; every parameter is
     null unless it carries supplied_by and supplied_on; unused ones warn.
  5. Quotes: every verbatim_quote (each " … " piece, in order) appears on
     its stated page(s), and every threshold figure appears in its quote.
  6. Coverage: every clause number printed in the PDF, and every App B / App
     C row label, is in rules or excluded (or under an excluded ancestor),
     and no clause is in both. Excluded reasons are one line.
  7. Notes: each has clauses, pages and a one-line issue; pages exist.

Text comparison is on pdftotext's plain output for the page, after light
normalisation: page footer removed, bullet glyphs removed, curly quotes and
dashes made straight, Unicode NFKC, whitespace collapsed. Nothing else is
forgiven, so a one-word change fails.

Exit code 0 when every check passes, 1 otherwise.
"""
import hashlib
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

RULE_FIELDS = {
    "rule_id": str, "clause": str, "page": (int, list), "type": str,
    "scope": str, "condition": str,
    "threshold_low": (int, float, type(None)),
    "threshold_low_inclusive": (bool, type(None)),
    "threshold_low_ref": (str, type(None)),
    "threshold_high": (int, float, type(None)),
    "threshold_high_inclusive": (bool, type(None)),
    "threshold_high_ref": (str, type(None)),
    "required_action": str, "approver": (str, type(None)),
    "evidence_source": str, "verbatim_quote": str,
}
TYPES = {"threshold", "approver", "anti-avoidance", "procedure"}
SCOPES = {"all", "goods-services", "works-concession-light-touch"}
TOP_KEYS = {"source", "parameters", "rules", "excluded", "notes"}
CLAUSE_RE = re.compile(r"^(\d+(?:\.\d+)+|App A row [1-4]|App B row (?:A|B1|B2|C|D)|"
                       r"App B notes|App C row [A-F]|App C closing)$")
PIECE_SPLIT = re.compile(r"\s*(?:…|\.\.\.)\s*")
MIN_PIECE = 15


def pdf_pages(pdf):
    out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, check=True).stdout
    return int(re.search(r"^Pages:\s+(\d+)", out, re.M).group(1))


def page_text(pdf, p):
    return subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), str(pdf), "-"],
                          capture_output=True, text=True, check=True).stdout


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"[-]", " ", s)            # private-use bullet glyphs
    s = s.translate(str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"',
                                   "–": "-", "—": "-", " ": " "}))
    return re.sub(r"\s+", " ", s).strip()


def strip_footer(raw, page):
    """Drop the Word file-name line and the trailing page number (the footer
    lines can come out separated from each other in plain text)."""
    raw = re.sub(r"^\S+\.docx\s*$", "", raw, flags=re.M)
    return re.sub(rf"\n\s*{page}\s*$", "", raw.rstrip("\f\n "))


def amounts_in(text):
    """Every £ figure printed in text, as a number: £500,000, £2.5million, £24,999.99."""
    vals = set()
    for num, mil in re.findall(r"£\s?([\d,]+(?:\.\d+)?)\s?(million|m\b)?", text):
        v = float(num.replace(",", ""))
        vals.add(v * 1_000_000 if mil else v)
    return vals


def ancestors(clause):
    parts = clause.split(".")
    return [".".join(parts[:i]) for i in range(2, len(parts))]


def main(rules_path, pdf_path):
    fails, warns = [], []
    pdf = Path(pdf_path)
    if not pdf.exists():
        print(f"FAIL: PDF not found: {pdf}")
        return 1
    try:
        doc = json.loads(Path(rules_path).read_text())
    except (OSError, json.JSONDecodeError) as e:
        print(f"FAIL: cannot read {rules_path}: {e}")
        return 1

    # 1. top level and source
    if not isinstance(doc, dict) or set(doc) != TOP_KEYS:
        got = sorted(doc) if isinstance(doc, dict) else type(doc).__name__
        print(f"FAIL: top level must be an object with exactly {sorted(TOP_KEYS)}; got {got}")
        return 1
    n_pages = pdf_pages(pdf)
    src = doc["source"]
    sha = hashlib.sha256(pdf.read_bytes()).hexdigest()
    if src.get("sha256") != sha:
        fails.append(f"source.sha256 {src.get('sha256')!r} does not match the PDF ({sha[:12]}…)")
    if src.get("pages") != n_pages:
        fails.append(f"source.pages is {src.get('pages')!r}; the PDF has {n_pages}")

    raw_pages = {p: page_text(pdf, p) for p in range(1, n_pages + 1)}
    pages = {p: norm(strip_footer(t, p)) for p, t in raw_pages.items()}

    params = doc["parameters"]
    rules, excluded, notes = doc["rules"], doc["excluded"], doc["notes"]
    for name, v in (("parameters", params), ("rules", rules), ("excluded", excluded), ("notes", notes)):
        if not isinstance(v, dict if name == "parameters" else list):
            print(f"FAIL: {name} has the wrong type")
            return 1

    # 4a. parameters declared correctly
    for key, p in params.items():
        if not isinstance(p, dict) or "value" not in p:
            fails.append(f"parameter {key}: must be an object with a value field")
            continue
        if p["value"] is not None and not (p.get("supplied_by") and p.get("supplied_on")):
            fails.append(f"parameter {key}: value {p['value']!r} set without supplied_by and supplied_on "
                         "(named thresholds stay null until an auditor supplies them)")
        for f in ("printed_as", "defined_in"):
            if not p.get(f):
                fails.append(f"parameter {key}: missing {f}")

    # 2-5. rules
    used_params = set()
    rule_clauses = set()
    for i, r in enumerate(rules, 1):
        rid = r.get("rule_id", f"rules[{i - 1}]") if isinstance(r, dict) else f"rules[{i - 1}]"
        if not isinstance(r, dict):
            fails.append(f"{rid}: not an object")
            continue
        if isinstance(r.get("clause"), str):
            rule_clauses.add(r["clause"])      # count coverage even if the rule is malformed
        missing = [f for f in RULE_FIELDS if f not in r]
        extra = [f for f in r if f not in RULE_FIELDS]
        if missing:
            fails.append(f"{rid}: missing fields {missing}")
        if extra:
            fails.append(f"{rid}: unknown fields {extra}")
        bad = [f for f, t in RULE_FIELDS.items() if f in r and (
               not isinstance(r[f], t)
               or (isinstance(r[f], bool) and bool not in (t if isinstance(t, tuple) else (t,))))]
        if bad:
            fails.append(f"{rid}: wrong type for {bad}")
            continue
        if missing:
            continue

        # 3. sequential ids
        want = f"CPR-{i:02d}"
        if r["rule_id"] != want:
            fails.append(f"{rid}: rule_id out of sequence, expected {want}")

        if not CLAUSE_RE.match(r["clause"]):
            fails.append(f"{rid}: clause {r['clause']!r} is not a recognised clause identifier")
        if r["type"] not in TYPES:
            fails.append(f"{rid}: type {r['type']!r} not in {sorted(TYPES)}")
        if r["scope"] not in SCOPES:
            fails.append(f"{rid}: scope {r['scope']!r} not in {sorted(SCOPES)}")
        for f in ("condition", "required_action", "evidence_source", "verbatim_quote"):
            if not r[f].strip():
                fails.append(f"{rid}: {f} is empty")
        if r["type"] == "approver" and not (r["approver"] or "").strip():
            fails.append(f"{rid}: approver rule with no approver")

        # thresholds as printed
        for side in ("low", "high"):
            val, inc, ref = r[f"threshold_{side}"], r[f"threshold_{side}_inclusive"], r[f"threshold_{side}_ref"]
            if val is not None and ref is not None:
                fails.append(f"{rid}: threshold_{side} has both a value and a ref")
            if val is not None:
                if val < 0:
                    fails.append(f"{rid}: threshold_{side} is negative")
                if isinstance(val, float) and round(val * 100) != val * 100:
                    fails.append(f"{rid}: threshold_{side} {val} has more than two decimals")
            if ref is not None:
                used_params.add(ref)
                if ref not in params:
                    fails.append(f"{rid}: threshold_{side}_ref {ref!r} is not declared in parameters")
            if (val is not None or ref is not None) and inc is None:
                fails.append(f"{rid}: threshold_{side} is set but threshold_{side}_inclusive is null")
            if val is None and ref is None and inc is not None:
                fails.append(f"{rid}: threshold_{side}_inclusive set on an open-ended side")
        lo, hi = r["threshold_low"], r["threshold_high"]
        if lo is not None and hi is not None and lo >= hi:
            fails.append(f"{rid}: threshold_low {lo} is not below threshold_high {hi}")

        # 5. quote on its page(s)
        pg = r["page"] if isinstance(r["page"], list) else [r["page"]]
        if not pg or not all(isinstance(p, int) and 1 <= p <= n_pages for p in pg) \
                or pg != list(range(pg[0], pg[0] + len(pg))):
            fails.append(f"{rid}: page {r['page']!r} is not a valid page or run of consecutive pages")
            continue
        hay = " ".join(pages[p] for p in pg)
        pieces = [norm(x) for x in PIECE_SPLIT.split(r["verbatim_quote"]) if x.strip()]
        pos = 0
        for piece in pieces:
            if len(piece) < MIN_PIECE:
                fails.append(f"{rid}: quote piece {piece!r} is shorter than {MIN_PIECE} characters")
                continue
            at = hay.find(piece, pos)
            if at < 0:
                where = [p for p in range(1, n_pages + 1) if piece in pages[p]]
                hint = f" (found on page {where})" if where else " (not found anywhere in the PDF)"
                fails.append(f"{rid}: quote not on page {r['page']}{hint}: {piece[:70]!r}")
            else:
                pos = at + len(piece)
        printed = amounts_in(r["verbatim_quote"])
        for side in ("low", "high"):
            val = r[f"threshold_{side}"]
            if val is not None and float(val) not in printed:
                fails.append(f"{rid}: threshold_{side} {val} is not printed in the quote "
                             f"(quote has {sorted(printed) or 'no £ figures'})")

    if rules and not any(isinstance(r, dict) and r.get("type") == "anti-avoidance" for r in rules):
        fails.append("no rule has type anti-avoidance (the no-splitting rule must be flagged)")
    for key in params:
        if key not in used_params:
            warns.append(f"parameter {key} is declared but no rule refers to it")

    # 6. excluded and coverage
    excl_clauses = set()
    for j, e in enumerate(excluded):
        tag = f"excluded[{j}]"
        if not isinstance(e, dict) or not {"clause", "page", "reason"} <= set(e):
            fails.append(f"{tag}: needs clause, page and reason")
            continue
        if not CLAUSE_RE.match(str(e["clause"])):
            fails.append(f"{tag}: clause {e['clause']!r} is not a recognised clause identifier")
        if not isinstance(e["page"], int) or not 1 <= e["page"] <= n_pages:
            fails.append(f"{tag}: page {e['page']!r} is not a page of the PDF")
        reason = e["reason"] if isinstance(e["reason"], str) else ""
        if not reason.strip() or "\n" in reason or len(reason) > 200:
            fails.append(f"{tag} ({e['clause']}): reason must be one line of at most 200 characters")
        if e["clause"] in excl_clauses:
            fails.append(f"{tag}: clause {e['clause']} excluded twice")
        excl_clauses.add(e["clause"])
    for c in sorted(rule_clauses & excl_clauses):
        fails.append(f"clause {c} is both a rule and excluded")

    printed_clauses = {}
    for p, raw in raw_pages.items():
        for m in re.finditer(r"^\s*(\d+(?:\.\d+)+)\s*$", strip_footer(raw, p), re.M):
            printed_clauses.setdefault(m.group(1), p)
    # appendix row labels: from each "Contract Rules - Appendix X" heading to the next
    heading = re.compile(r"^Contract Rules - Appendix ([A-Z])\s*$", re.M)
    app_of_page, current = {}, None
    for p in range(1, n_pages + 1):
        m = heading.search(raw_pages[p])
        current = m.group(1) if m else current
        app_of_page[p] = current
    for p, app in app_of_page.items():
        if app in ("B", "C"):
            for lab in re.findall(r"^\s*(A|B|B1|B2|C|D|E|F)\s*$", strip_footer(raw_pages[p], p), re.M):
                printed_clauses.setdefault(f"App {app} row {lab}", p)
    covered = rule_clauses | excl_clauses
    for c, p in sorted(printed_clauses.items()):
        if c in covered or any(a in excl_clauses for a in ancestors(c)):
            continue
        fails.append(f"clause {c} (page {p}) is in neither rules nor excluded")
    if "A" in app_of_page.values() and not any(c.startswith("App A") for c in covered):
        fails.append("Appendix A has no entry in rules or excluded")
    for c in sorted(covered):
        if re.match(r"^\d", c) and c not in printed_clauses:
            fails.append(f"clause {c} is listed but is not printed in the PDF")

    # 7. notes
    for k, n in enumerate(notes):
        tag = f"notes[{k}]"
        if not isinstance(n, dict) or not {"clauses", "pages", "issue"} <= set(n):
            fails.append(f"{tag}: needs clauses, pages and issue")
            continue
        if not n["clauses"] or not isinstance(n["clauses"], list):
            fails.append(f"{tag}: clauses must be a non-empty list")
        if not n["pages"] or not all(isinstance(p, int) and 1 <= p <= n_pages for p in n["pages"]):
            fails.append(f"{tag}: pages {n['pages']!r} are not pages of the PDF")
        if not isinstance(n["issue"], str) or not n["issue"].strip() or "\n" in n["issue"]:
            fails.append(f"{tag}: issue must be one line")

    n_rules = len(rules)
    by_type = {}
    for r in rules:
        if isinstance(r, dict):
            by_type[r.get("type")] = by_type.get(r.get("type"), 0) + 1
    print(f"rules: {n_rules} {by_type} | excluded: {len(excluded)} | parameters: {len(params)} | notes: {len(notes)}")
    for w in warns:
        print(f"WARN: {w}")
    for f in fails:
        print(f"FAIL: {f}")
    if fails:
        print(f"{len(fails)} failure(s)")
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__.split("\n\n")[1])
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2]))
