---
name: risk-assessment
description: The method for turning outputs/rules.json, outputs/analytics.json and outputs/history.json into a rated procurement risk register. The agent writes cited judgments to outputs/risk-ratings.json; build_register.py resolves every citation, fills every figure, scores on the council's own matrix and renders outputs/risk-register.md plus the auditor decision template outputs/auditor-comments.md. Loaded by the risk-assessor sub-agent.
---

# risk-assessment

The two analysts produced facts: what the payments show (`analytics.json`)
and what past audits and the council's strategy say (`history.json`).
Rating risks is a judgment, and judgments drift without a fixed method.
This skill is that method. The split of work is strict:

| The agent (judgment) | `build_register.py` (computation and checks) |
| --- | --- |
| picks the risks, from the theme table | resolves every `[rule:]`, `[metric:]`, `[history:]` citation |
| scores likelihood and impact 1–5 with the rubric | fills every `{{$.path}}` placeholder from analytics.json |
| writes justifications with citation tags | computes score = L × I, the matrix label and the band from history.json |
| recommends in or out of scope | drops a risk whose L or I justification has no resolvable citation |
| applies auditor decisions on a re-run | checks repeat-finding uplifts, typed figures, revisions; writes both files |

Files:

| | Path |
| --- | --- |
| Judgments (agent writes) | `outputs/risk-ratings.json` |
| Builder (run, never edit) | `.claude/skills/risk-assessment/build_register.py` |
| Register (builder writes) | `outputs/risk-register.md` |
| Decision template (builder writes, auditor fills) | `outputs/auditor-comments.md` |

```bash
.venv/bin/python .claude/skills/risk-assessment/build_register.py
```

## 1. Citations and placeholders

Every likelihood and impact justification cites at least one source:

- `[rule:CPR-20]`: a `rule_id` in `outputs/rules.json`.
- `[metric:$.tests.split_purchases.by_threshold.25000.headline_general_procurement.windows]`:
  a JSONPath into `outputs/analytics.json` that ends on a **scalar**
  (number, string, boolean). Lists and objects do not resolve.
  Keys that contain a dot (`24999.99`, `baseline_0.5T_to_1.5T`) cannot be
  addressed; cite the equivalent key (`25000`) or another metric.
- `[history:AUD-07]`: an `id` anywhere in `outputs/history.json` (audits,
  risk themes, discrepancies, scoring-method entries).

Every figure in prose is a placeholder, `{{$.tests.duplicates.different_time.groups}}`,
never a typed number. The builder fills it and warns when it finds a typed
figure (three or more digits, or a `£` followed by a digit) outside a
placeholder. Treat that warning as a failure. Rule IDs, history IDs and
the 1–5 scores themselves are not figures.

## 2. Themes

Work through this table. Each theme becomes at most one risk (`R-01`, `R-02`,
... in table order, numbering only the risks you keep). A theme with no
rule, no metric and no history item is excluded with a one-line reason.

| # | Theme | Rules to look for | Metrics to look for | History to look for |
| --- | --- | --- | --- | --- |
| 1 | Contract splitting to stay under a procedure threshold | anti-avoidance rule (6.16); App B rows | `split_purchases` headline (general procurement) per threshold | audits of purchasing / accounts payable |
| 2 | Payments clustering just below a quote or tender threshold | App B rows A, B1, B2 | `threshold_clustering` band vs comparator, general procurement | same |
| 3 | High-value suppliers with no published contract notice | App B rows B1/B2/D (CDP notice), 10.4 (Contract Register), 5.2.1 | `off_contract` unmatched general procurement | contract-management audits |
| 4 | Spend after a contract notice ended (extensions) | App C row D | `expired_notice_spend` | contract-management audits |
| 5 | Spend above the awarded value (variations) | App C row E | `spend_vs_award` flagged | same |
| 6 | Duplicate or repeated payments | 10.1 (written evidence of purchases) | `duplicates.different_time` general procurement | accounts payable audits |
| 7 | Waivers and exceptions to competition | 7.2, 7.3, 7.4.x, 7.5.x | none observable: say so | any audit naming waivers |
| 8 | Award approval and Key Decisions for the largest contracts | 4.3, App A rows 2–4, 7.4.3 | `split_purchases.by_threshold.500000` headline; high-value tier | governance audits |
| 9 | Care and education placements bought outside competition | App C row F | placement windows / duplicates / high-value placement tier | social care commissioning audits |
| 10 | Grants and transfer payments treated as contracts | none in rules.json (1.6.2 is excluded as a definition): rely on metrics and history | high-value suppliers, `grant` tag | grants audits |
| 11 | Agency staff procurement | App B rows, 6.16 | high-value tier, `agency_staff` tag | workforce audits |

Do not add a theme that is not in the table unless the auditor's comments
ask for it.

## 3. Likelihood rubric (1–5)

Use the first row that fits, reading from the top. Two runs on the same
evidence must give the same score.

| Score | When |
| --- | --- |
| 5 | A data signal in general procurement (row 3 test) **and** an adverse audit opinion (Limited or Weak) on the same theme in history.json |
| 4 | A data signal in general procurement from two or more tests or thresholds, **or** one signal plus a repeat finding |
| 3 | A data signal in general procurement from one test designed for the rule |
| 2 | Flagged items exist only in tags where the pattern is expected (placements, grants, premises), or the metric is empty but the rule is high-stakes |
| 1 | The rule exists, the data cannot observe it, and history shows no concern |

A "data signal" is a non-zero count in the general-procurement headline of
the test. A test with zero flagged items is evidence of absence for that
test only.

**Repeat-finding uplift.** If history.json records an audit on the same
theme with an adverse opinion (Limited Assurance or Weak), raise likelihood
by one point (max 5), set `"repeat_uplift": {"history": "<id>"}` on the
risk, and say so in the justification. The builder fails an uplift whose
history item is not an audit with an adverse opinion.

**Unobservable controls** (waivers, approvals, register completeness):
score on the rule and the gap, say in the justification that the data
cannot observe the control, and keep the risk only if the rule is cited.

## 4. Impact (1–5)

Use the council's impact scale in `history.json` → `scoring_method`
(financial, reputation, compliance columns). Pick the score whose
descriptors best fit the theme's exposure, and cite both the scale entry
(`[history:...]`) and the exposure metric or rule threshold. If
`scoring_method.usable` is false, use the fallback 1 Very low … 5 Very high
and the builder states the fallback in the register header.

## 5. Ratings file (`outputs/risk-ratings.json`)

```json
{
  "generated_at": "YYYY-MM-DD",
  "risks": [
    {
      "id": "R-01",
      "theme": 1,
      "title": "Payments to one supplier grouped under a procedure threshold",
      "statement": "Purchases may be split across payments so each stays below a quote or tender threshold.",
      "likelihood": 4,
      "likelihood_justification": "... {{$.tests.split_purchases.by_threshold.25000.headline_general_procurement.windows}} windows ... [metric:$.tests.split_purchases.by_threshold.25000.headline_general_procurement.windows] [rule:CPR-20]",
      "impact": 3,
      "impact_justification": "... [history:SM-IMP-3] [rule:CPR-53]",
      "evidence": ["rule:CPR-20", "metric:$.tests.split_purchases.by_threshold.25000.headline_general_procurement.gbp"],
      "proposed_focus": "Test the largest general-procurement windows against quotes and orders.",
      "sample_source": "split-purchases.csv",
      "recommend_in_scope": true,
      "repeat_uplift": null,
      "auditor_override": false
    }
  ],
  "excluded": [{"theme": 10, "reason": "one line"}],
  "revision": null
}
```

- `statement` and `title` are qualitative: no figures, no supplier,
  officer or department names. Indicator language only ("may", "indicates",
  "pattern to test"), never wrongdoing.
- `evidence` lists citations (without brackets) that the register prints as
  evidence lines; a `rule:` entry prints the rule's quote excerpt.
- `sample_source` names a file in `outputs/analytics-full/` the planner can
  sample from.
- `recommend_in_scope`: your recommendation. The auditor decides.

## 6. Re-run after the auditor gate (revision)

When `outputs/auditor-comments.md` has decisions, apply them and add:

```json
"revision": {"number": 1, "changes": [
  {"id": "R-09", "type": "amended", "what": "likelihood 2 -> 3 as the auditor asked"},
  {"id": "R-10", "type": "rejected"}
]}
```

- approve: leave the risk unchanged.
- amend: change exactly what the comment asks; if it sets a score the
  evidence alone would not, set `"auditor_override": true` and keep at least
  one real citation.
- reject: move the risk to `excluded` with `"id"` and the auditor's reason.

Increase `number` on each later revision. The builder fails if a decision
is unapplied, if a risk changed that the auditor did not ask about, or if
an approved risk is missing. It writes the revision header and the closing
"Auditor decisions" section itself.

## 7. Conflicting thresholds in the scoring method

If history.json records a conflict (for example the RAG band table and the
Corporate Risk Register inclusion rule draw the line at different scores),
the builder uses the RAG band table for bands, marks the other rule in the
register header, and never resolves it silently.

## 8. Loop and report

Run the builder, fix every FAIL and WARN by correcting citations,
placeholders or wording (never by editing the builder), and repeat until it
prints `0 failures, 0 warnings`. Report: risks rated and excluded, the
summary table (ID, title, L, I, score, band, recommendation), any fallback
or conflict marked in the header, and the request for the auditor to record
a decision for every risk in `outputs/auditor-comments.md`.
