---
name: challenger-sample-lessons
description: Sample-recipe and test-wording patterns the challenger rejected in Phase 3, and the fixes it accepted
metadata:
  type: feedback
---

Build these in from v1 to save challenge rounds.

- **Duplicates:** the sample unit is the repeat group, not the row. Use `kind: rows` with `distinct_by: group` on `duplicates.csv`, and have the step pull the partner payments in each group.
- **Small flagged sets** (e.g. spend-vs-award flags): sample every flagged item using a `where_min` on the flag column. Ordering by ratio alone left out the largest-value suppliers.
- **No cross-risk supplier exclusion when the controls differ.** Excluding the contract-coverage suppliers from the award-approval test was rejected, because the largest suppliers then got no approver test. Use `exclude_drawn_in` only between tests of the same control.
- **Pass routes must be complete.** Each "Pass:" names every legitimate route, plus "otherwise fail" where publication or quotes are at stake. Public-body payees can appear under a private-contractor narrative, so supplier tests need an "approved inter-authority or shared-service agreement inspected" route.
- **Conditional "above the Threshold" tests** with a null threshold were rejected as having no population. Have the auditor confirm the figure before fieldwork, and apply the test to every identified contract.
- **Tag gaps** (risk-specific supplier types tagged general procurement): add a fieldwork step to review the unmatched top 20 and test up to two, rather than naming suppliers.
- **Out-of-scope decisions:** the challenger wants the memo Limitations to state the spend left untested, as placeholders plus the related audit history. That is not a scope change; it can go in from v1.

**Why:** each of these cost a challenge round in the first Phase 3 run.
**How to apply:** check every recipe and pass sentence against this list before the first build. Related: [[builder-pitfalls]].
