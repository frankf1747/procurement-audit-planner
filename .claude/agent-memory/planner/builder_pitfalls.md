---
name: builder-pitfalls
description: build_pack.py traps hit while writing audit-plan.json (row_id delimiters, literal-figure check, jpath keys, file and column names that differ from the skill examples)
metadata:
  type: feedback
---

Check these before the first build; each cost a rebuild.

- **groups kind splits `row_ids` on `;` or `,` only.** An earlier analytics run wrote space-separated row_ids in `split-purchases.csv`, so every groups sample failed with "row_id ... not found". The lead had analyse.py fixed to join with "; ". If it recurs, report `PLANNER BLOCKED` to the lead; do not switch to `kind: none`.
- Grouped-payment windows can hold dozens of payments: set `per_group_n` (5 for split windows) or one test pulls well over a hundred transactions.
- `split-purchases.csv` has no `window_id` or `supplier_norm`; it has `supplier`. Use `key: supplier`, `distinct_by: supplier`. `exclude_drawn_in` cannot exclude suppliers there (only row ids).
- File names differ from the skill example: `split-purchases.csv`, `duplicates.csv` (row-level, columns `group`, `tier`), not `*-windows.csv` / `duplicates-groups.csv`.
- Literal-figure check (`£\d` or any 3+ digit number) runs on memo, control, step and evidence text. "£500" in "payments over £500" fails; use a placeholder or words. Thresholds in control text need `£{{$.tests...threshold}}`.
- jpath splits on dots, so keys like `by_threshold.24999.99` cannot be cited; use the 25000 key.
- The register's own rule citations (risk-ratings.json, including out-of-scope risks) count toward rule coverage, so only rules outside them need a control/test cite or a not-tested reason. CPR-48 (App A row 1) is easy to miss.
- high-value-suppliers.csv already holds only suppliers at or above the publication tier; still state `where_min annualised_estimate` so the tier is visible in the recipe.
