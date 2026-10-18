#!/usr/bin/env python3
"""Test build_register.py on fixtures, against the real rules/analytics/history.

Usage (from the project root, after rules.json, analytics.json and history.json exist):
  .venv/bin/python .claude/skills/risk-assessment/tests/test_build_register.py

1. first run: one good risk and one broken risk (its likelihood justification
   cites nothing that resolves) -> the good risk is rated, the broken one is
   dropped to Excluded, and a bad citation, a typed figure and a false uplift
   are each reported.
2. revision: the auditor approves R-01 and rejects R-02 -> applying the
   decision passes; changing R-01 without being asked fails.
Writes into a temporary folder; never touches outputs/.
"""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BUILD = HERE.parent / "build_register.py"
OUT = ROOT / "outputs"

GOOD = {
    "id": "R-01", "theme": 1, "title": "Payments grouped under a procedure threshold",
    "statement": "Purchases may be split across payments so each stays below a quote threshold.",
    "likelihood": 3,
    "likelihood_justification": "{{$.tests.split_purchases.by_threshold.25000.headline_general_procurement.windows}} "
                                "general-procurement windows [metric:$.tests.split_purchases.by_threshold.25000.headline_general_procurement.windows] "
                                "against the no-splitting rule [rule:CPR-20].",
    "impact": 3,
    "impact_justification": "Medium on the council's scale [history:$.scoring_method.impact_scale[2]].",
    "evidence": ["rule:CPR-20", "metric:$.tests.split_purchases.by_threshold.25000.headline_general_procurement.gbp"],
    "proposed_focus": "Test the largest windows against quotes and orders.",
    "sample_source": "split-purchases.csv", "recommend_in_scope": True, "repeat_uplift": None, "auditor_override": False,
}
BROKEN = {**GOOD, "id": "R-02", "title": "Broken risk",
          "likelihood_justification": "Judged likely from experience [metric:$.tests.no_such_test.count].",
          "impact_justification": "Typed figure 25000 here [rule:CPR-20].",
          "repeat_uplift": {"history": "AUD-01"}}


def run(tmp):
    p = subprocess.run([sys.executable, str(BUILD), "--ratings", str(tmp / "risk-ratings.json"),
                        "--comments", str(tmp / "auditor-comments.md"), "--out-dir", str(tmp),
                        "--rules", str(OUT / "rules.json"), "--analytics", str(OUT / "analytics.json"),
                        "--history", str(OUT / "history.json")], capture_output=True, text=True, cwd=ROOT)
    return p.returncode, p.stdout


def expect(name, cond):
    print(f"  {'ok  ' if cond else 'FAIL'} {name}")
    return cond


def main():
    ok = True
    tmp = Path(tempfile.mkdtemp(prefix="regtest-"))
    (tmp / "analytics-full").symlink_to(OUT / "analytics-full")
    try:
        print("1. first run: one good risk, one broken")
        (tmp / "risk-ratings.json").write_text(json.dumps({"generated_at": "2026-10-17", "risks": [GOOD, BROKEN], "excluded": [], "revision": None}))
        code, out = run(tmp)
        reg = (tmp / "risk-register.md").read_text()
        ok &= expect("exits 1 (bad citation is a failure)", code == 1)
        ok &= expect("bad metric path reported", "R-02.likelihood: citation does not resolve: metric:$.tests.no_such_test.count" in out)
        ok &= expect("broken risk dropped to Excluded", "- R-02: Broken risk: no resolvable citation in the likelihood justification" in reg)
        ok &= expect("good risk rated with score 9 and council label", "| R-01 | Payments grouped under a procedure threshold | 3 | 3 | 9 |" in reg)
        ok &= expect("placeholder filled", "{{" not in reg)
        ok &= expect("template has one row for R-01", (tmp / "auditor-comments.md").read_text().count("| R-01 |") == 1)

        print("2. typed figure and false uplift on an otherwise valid risk")
        bad2 = {**BROKEN, "likelihood_justification": GOOD["likelihood_justification"]}
        (tmp / "risk-ratings.json").write_text(json.dumps({"risks": [GOOD, bad2], "excluded": [], "revision": None}))
        code, out = run(tmp)
        ok &= expect("typed figure warned", "R-02.impact_justification: figure typed in prose" in out)
        ok &= expect("uplift without adverse opinion fails", "R-02: repeat_uplift cites AUD-01, which has no adverse opinion" in out)

        print("3. clean first run, then a revision")
        (tmp / "risk-ratings.json").write_text(json.dumps({"risks": [GOOD, {**GOOD, "id": "R-02", "title": "Second risk"}], "excluded": [], "revision": None}))
        code, out = run(tmp)
        ok &= expect("clean run passes with 0 failures, 0 warnings", code == 0 and "0 failures, 0 warnings" in out)
        c = (tmp / "auditor-comments.md").read_text()
        c = c.replace("Reviewer: ", "Reviewer: Test Auditor").replace("Date: ", "Date: 2026-10-17")
        c = c.replace("| in scope |  |  |", "| in scope | approve | ok |", 1)
        c = c.replace("| in scope |  |  |", "| in scope | reject | covered elsewhere |", 1)
        (tmp / "auditor-comments.md").write_text(c)
        changed = {**GOOD, "likelihood": 4}
        (tmp / "risk-ratings.json").write_text(json.dumps({"risks": [changed], "excluded": [{"id": "R-02", "reason": "covered elsewhere"}],
                                                           "revision": {"number": 1, "changes": [{"id": "R-02", "type": "rejected"}]}}))
        code, out = run(tmp)
        ok &= expect("unrequested change to an approved risk fails", code == 1 and "R-01: changed since the last revision" in out)
        (tmp / "risk-ratings.json").write_text(json.dumps({"risks": [GOOD], "excluded": [{"id": "R-02", "reason": "covered elsewhere"}],
                                                           "revision": {"number": 1, "changes": [{"id": "R-02", "type": "rejected"}]}}))
        code, out = run(tmp)
        reg = (tmp / "risk-register.md").read_text()
        ok &= expect("applied revision passes", code == 0)
        ok &= expect("revision header written", "*Revision 1, following auditor comments by Test Auditor dated 2026-10-17" in reg)
        ok &= expect("rejected decision kept in the template", "| R-02 | Second risk |" in (tmp / "auditor-comments.md").read_text())
        code, out = run(tmp)
        ok &= expect("rebuilding the same revision is idempotent", code == 0)
    finally:
        shutil.rmtree(tmp)
    print("BUILDER TESTS PASSED" if ok else "BUILDER TESTS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
