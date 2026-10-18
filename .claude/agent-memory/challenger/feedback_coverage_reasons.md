---
name: coverage-reason-checks
description: How to test the memo's not-tested rule reasons and limitations, and how to navigate the oversized analytics.json
metadata:
  type: feedback
---

- **"Threshold is null" reasons**: open the rule in rules.json and check `threshold_low` and `threshold_high` separately. A rule can carry a usable lower bound even when its upper bound refers to the null statutory Threshold. Also check any test whose population depends on the null figure: it may not be able to pass or fail.
- **Pass criteria**: for each near-threshold test, ask whether a split or part order would still pass. Pass criteria often check only the lowest-band requirement (one quote) and ignore the next rule up (publication).
- **Memo limitations**: diff them against the register's risk-level caveats (comparator results, which population a test covers) and against `$.population.limitations` and `$.population.excluded` in analytics.json.
- **Rating and scope**: compare an out-of-scope tag's share of `$.population.total_gbp` and its window or group counts with general procurement. Pair this with any Limited, Weak or Unsatisfactory history item, then route it to the auditor while still giving the planner a memo-level ask.
- **analytics.json is too large for one Read.** Grep the top-level keys with the pattern `^    "[a-z_]+": \{` to get section line numbers, then Read by offset.

**Why:** these checks surfaced coverage and test gaps that a read of the memo alone would miss.
**How to apply:** run them in round one, after the sample-recipe pass ([[sample-recipe-checks]]).
