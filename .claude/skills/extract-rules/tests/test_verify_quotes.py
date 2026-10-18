#!/usr/bin/env python3
"""Test verify_quotes.py on two fixtures built from the real PDF.

Usage (from the project root):
  .venv/bin/python .claude/skills/extract-rules/tests/test_verify_quotes.py

good.json: seven hand-picked rules with real quotes (one spanning a page
break), one null parameter, every other clause excluded as a placeholder.
It must pass every check.

bad.json: good.json with one planted error per check. Each planted error
must be reported, and nothing else.

Both fixtures are written to tests/fixtures/ so they can be inspected.
Placeholder exclusions are fixture scaffolding, not a classification of the
PDF: the skill itself has not been run.
"""
import copy
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
ROOT = SKILL.parents[2]
PDF = ROOT / "data/contract-rules.pdf"
VERIFY = SKILL / "verify_quotes.py"
OUT = HERE / "fixtures"
sys.path.insert(0, str(SKILL))
import verify_quotes as vq  # noqa: E402


def rule(rid, clause, page, type_, scope, condition, low, low_inc, low_ref, high, high_inc, high_ref,
         action, approver, evidence, quote):
    return {"rule_id": rid, "clause": clause, "page": page, "type": type_, "scope": scope,
            "condition": condition,
            "threshold_low": low, "threshold_low_inclusive": low_inc, "threshold_low_ref": low_ref,
            "threshold_high": high, "threshold_high_inclusive": high_inc, "threshold_high_ref": high_ref,
            "required_action": action, "approver": approver, "evidence_source": evidence,
            "verbatim_quote": quote}


RULES = [
    rule("CPR-01", "4.3", 3, "approver", "all", "contract award valued over £500,000",
         500000, False, None, None, None, None,
         "treat the award as a Key Decision of the Council", "the Council (Key Decision)",
         "Forward Plan entry and Key Decision record",
         "Any contract award with a value over £500,000 is a Key Decision of the Council."),
    rule("CPR-02", "6.15", [4, 5], "procedure", "all", "estimating Total Contract Value for any procurement",
         None, None, None, None, None, None,
         "estimate the value over the full potential duration including extensions", None,
         "procurement file value estimate",
         "Total Contract Value is a genuine estimate of the total value over the full potential "
         "duration of the contract, not just the initial term. This includes: … All planned extensions "
         "(even if optional)"),
    rule("CPR-03", "6.16", 5, "anti-avoidance", "all", "any contract",
         None, None, None, None, None, None,
         "do not split or disaggregate a contract to avoid the Rules", None,
         "spend records for the same supplier and requirement",
         "There shall be no artificial splitting or disaggregation of a contract to avoid the application "
         "of the provisions of the Procurement Legislation and/or these Rules."),
    rule("CPR-04", "10.1", 8, "procedure", "all", "any purchase",
         None, None, None, None, None, None,
         "keep written (including electronic) evidence of the purchase", None,
         "purchase order, invoice or contract",
         "There should be written evidence of all purchases (which shall include electronic evidence)."),
    rule("CPR-05", "App B row A", 12, "threshold", "all",
         "total value exclusive of VAT above £1,000 and less than £25,000",
         1000, False, None, 25000, False, None,
         "seek at least one quote from an appropriate source", None,
         "quote record on the purchase file",
         "Above £1,000 and less than £25,000 … At least one quote must be sought from an appropriate source."),
    rule("CPR-06", "App B row B1", 12, "threshold", "goods-services",
         "goods and services, £25,000 or more and less than the Threshold",
         25000, True, None, None, False, "threshold_goods_services",
         "invite at least three quotes via the Procurement Portal; publish a contract notice on the CDP", None,
         "Procurement Portal RFQ record; CDP contract notice",
         "£25,000 or more and less than the Threshold … Invitations to quote must be sent via the "
         "Procurement Portal to at least three appropriate sources, … A contract notice must be "
         "published on the CDP"),
    rule("CPR-07", "App C row D", 14, "approver", "all",
         "extension of an existing contract that provides for the extension",
         None, None, None, None, None, None,
         "obtain S151 Officer approval for the extension", "S151 Officer",
         "S151 Officer approval record",
         "The proposed contract is an extension to an existing contract where the existing contract "
         "provides for such extension. … Approval of the S151 Officer"),
]


def printed_clauses():
    n = vq.pdf_pages(PDF)
    found = {}
    for p in range(1, n + 1):
        raw = vq.strip_footer(vq.page_text(PDF, p), p)
        for m in re.finditer(r"^\s*(\d+(?:\.\d+)+)\s*$", raw, re.M):
            found.setdefault(m.group(1), p)
    for c, p in [("App A row 1", 11), ("App B row C", 12), ("App B row D", 12), ("App B row B2", 12),
                 ("App C row A", 14), ("App C row B", 14), ("App C row C", 14), ("App C row E", 14),
                 ("App C row F", 15)]:
        found[c] = p
    return n, found


def good_fixture():
    n, clauses = printed_clauses()
    used = {r["clause"] for r in RULES}
    excluded = []
    for c, p in clauses.items():
        if c in used or any(a in [e["clause"] for e in excluded] for a in vq.ancestors(c)):
            continue
        excluded.append({"clause": c, "page": p, "reason": "fixture placeholder, not a classification"})
    return {
        "source": {"file": "data/contract-rules.pdf", "pages": n,
                   "sha256": hashlib.sha256(PDF.read_bytes()).hexdigest(),
                   "title": "Contract Rules", "extracted_with": "fixture"},
        "parameters": {"threshold_goods_services": {
            "value": None, "printed_as": "the Threshold (Goods and Services)",
            "defined_in": ["1.4", "App B notes"], "note": "fixture"}},
        "rules": copy.deepcopy(RULES),
        "excluded": excluded,
        "notes": [{"clauses": ["App A row 2", "App A row 3"], "pages": [11],
                   "issue": "A value of exactly £500,000 falls in neither band."}],
    }


def bad_fixture(good):
    bad = copy.deepcopy(good)
    r = {x["rule_id"]: x for x in bad["rules"]}
    planted = {}

    r["CPR-03"]["page"] = 4
    planted["wrong page"] = "CPR-03: quote not on page 4 (found on page [5])"
    r["CPR-04"]["verbatim_quote"] = r["CPR-04"]["verbatim_quote"].replace("written evidence", "written proof")
    planted["one-word misquote"] = "CPR-04: quote not on page 8 (not found anywhere in the PDF)"
    r["CPR-07"]["rule_id"] = "CPR-08"
    planted["rule_id gap"] = "CPR-08: rule_id out of sequence, expected CPR-07"
    r["CPR-06"]["threshold_high_ref"] = "threshold_works"
    planted["undeclared parameter"] = "CPR-06: threshold_high_ref 'threshold_works' is not declared in parameters"
    bad["parameters"]["threshold_goods_services"]["value"] = 214904
    planted["parameter filled from memory"] = "parameter threshold_goods_services: value 214904 set without supplied_by"
    r["CPR-05"]["threshold_high"] = 20000
    planted["threshold not as printed"] = "CPR-05: threshold_high 20000 is not printed in the quote"
    r["CPR-01"]["threshold_low_inclusive"] = None
    planted["missing inclusive flag"] = "CPR-01: threshold_low is set but threshold_low_inclusive is null"
    del r["CPR-02"]["evidence_source"]
    planted["missing field"] = "CPR-02: missing fields ['evidence_source']"
    bad["excluded"] = [e for e in bad["excluded"] if e["clause"] != "9.2"]
    planted["clause not covered"] = "clause 9.2 (page 7) is in neither rules nor excluded"
    bad["excluded"].append({"clause": "6.16", "page": 5, "reason": "fixture"})
    planted["clause in both lists"] = "clause 6.16 is both a rule and excluded"
    bad["excluded"][0]["reason"] = "definition only\nsecond line"
    planted["multi-line reason"] = "excluded[0] (1.1): reason must be one line"
    bad["source"]["sha256"] = "0" * 64
    planted["wrong PDF hash"] = "source.sha256 '0000"
    return bad, planted


def run(path):
    p = subprocess.run([sys.executable, str(VERIFY), str(path), str(PDF)], capture_output=True, text=True)
    return p.returncode, p.stdout


def main():
    OUT.mkdir(exist_ok=True)
    good = good_fixture()
    bad, planted = bad_fixture(good)
    (OUT / "good.json").write_text(json.dumps(good, indent=2, ensure_ascii=False) + "\n")
    (OUT / "bad.json").write_text(json.dumps(bad, indent=2, ensure_ascii=False) + "\n")

    ok = True
    code, out = run(OUT / "good.json")
    print("good.json:", out.strip().splitlines()[-1])
    if code != 0:
        ok = False
        print(out)

    code, out = run(OUT / "bad.json")
    fails = [l for l in out.splitlines() if l.startswith("FAIL: ")]
    print(f"bad.json: exit {code}, {len(fails)} failure(s) for {len(planted)} planted errors")
    for name, expect in planted.items():
        hit = any(expect in l for l in fails)
        print(f"  {'caught' if hit else 'MISSED'}  {name}")
        ok &= hit
    unexpected = [l for l in fails if not any(e in l for e in planted.values())]
    for l in unexpected:
        print(f"  UNEXPECTED  {l}")
    ok &= code == 1 and not unexpected
    print("VERIFIER TESTS PASSED" if ok else "VERIFIER TESTS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
