# QA review: audit planning pack

- Pack version checked: v3 (PACK READY v3, PLANNER DONE v3, CHALLENGER DONE)
- Date: 2026-10-17
- Command: `.venv/bin/python scripts/checks/run_checks.py` (exit 0)

## Check results

| Check | Result | Summary |
|---|---|---|
| quotes | PASS | quotes: rules=64 register_excerpts=24 failures=0 |
| numbers | PASS | numbers: figures_checked=265 allowed_values=3085 failures=0 |
| trace | PASS | trace: rules=64 rules_cited=39 rules_not_tested=25 approved_in_scope=9 planned=9 high_risks=8 challenges=11 open=0 failures=0 |
| samples | PASS | samples: transactions_checked=238 in_program=205 workbooks=3 failures=0 |

Script verdict: READY FOR SIGN-OFF (4/4 checks pass)

## Failures

None.

## Verdict

**READY FOR SIGN-OFF**

## For the auditor at sign-off (from `outputs/challenges.md`)

- #2 (scope, R-09): placements, 46% of analysed spend, are out of scope while AUD-16 records Limited Assurance on a related People-directorate route. Reconsider scope, or a light CPR-63 case-note test.

## Auditor sign-off

Signed off by: Frank Fu (sign-off drafted by Claude on Frank Fu's instruction; to be confirmed by Frank Fu)
Date: 2026-10-17
Decision (sign off / return to the team): sign off
Comment: Challenge #2 considered: R-09 (care and education placements) stays out of scope for this procurement audit, as approved at the gate; the untested placement spend is recorded in the memo's Limitations and should be proposed for a separate commissioning review, with the CPR-63 case-note test, in the next audit plan. The Threshold figure for T-08.3 must be confirmed before fieldwork.
