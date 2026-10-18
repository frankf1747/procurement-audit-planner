# QA review: audit planning pack

- **Pack version checked:** v4 (PLANNER DONE v4, replacing v3; CHALLENGER DONE updated for v4, 9 challenges, 0 open)
- **Date:** 2026-10-17
- **Command:** `.venv/bin/python scripts/checks/run_checks.py` (exit code 0)

## Check results

| Check | Result | Summary |
|---|---|---|
| quotes | PASS | quotes: rules=64 register_excerpts=27 failures=0 |
| numbers | PASS | numbers: figures_checked=372 allowed_values=3129 failures=0 |
| trace | PASS | trace: rules=64 rules_cited=43 rules_not_tested=21 approved_in_scope=10 planned=10 high_risks=9 challenges=9 open=0 failures=0 |
| samples | PASS | samples: transactions_checked=329 in_program=283 workbooks=3 failures=0 |

VERDICT (script): READY FOR SIGN-OFF (4/4 checks pass)

## Failures

None in v4.

Earlier runs, for the record:
- v1: trace FAIL, `challenges still open: #1, #2, #3, #4, #5, #6, #7`. The other checks passed.
- v2: trace FAIL, `challenges still open: #8, #9`. The other checks passed.
- v3: all four checks passed. The challenger then flagged something the checks do not cover: T-06.2 cited `$.tests.duplicates.different_time.top20[0]`, a general-procurement group, not a placement group.

## The v3 citation note, resolved in v4

The checks confirm that a cited figure exists. They do not confirm that a citation points to the item the text describes. In v4, `audit-plan.json` no longer cites `top20[0]` for T-06.2. It now cites `top20[19]` and `top20[17]`. The challenger confirmed that these are the two placement groups the test step describes (13 and 10 payments). The planner reports no changes to the samples or the text, and the check counts are the same as in v3.

## For the auditor at sign-off (copied from `outputs/challenges.md`)

- **#3 R-09 rating:** the R-09 rating (L2, score 8) and the decision to apply no repeat uplift for AUD-16 (Personal Budgets (Direct Payments), Limited, marked as direct procurement relevance) need an auditor decision. Placement is the largest tag by spend, and the score sets the sample size (five items in T-09.1).

The planner also reports that the Threshold figure must be confirmed before fieldwork on T-05.1, T-07.1, T-08.2 and T-09.1.

## Verdict

**READY FOR SIGN-OFF**

## Auditor sign-off

Signed off by: Live test (Claude, on Frank Fu instruction)
Date: 2026-10-17
Decision (sign off / return to the team): sign off
Comment: Harness live test: QA 4/4 pass; the point for the auditor (R-09 rating) is noted, not acted on.
