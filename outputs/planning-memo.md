# Procurement audit: planning memo

*Generated 2026-10-17 by `build_pack.py` from `audit-plan.json`, `risk-register.md` (revision 2), `auditor-comments.md` by Frank Fu (decisions drafted by Claude on Frank Fu's instruction) dated 2026-10-17, `rules.json` and `analytics.json`. Status: DRAFT for challenge, QA review and auditor sign-off.*

**Indicators, not findings.** Every test below checks a control against a pattern in public data. Nothing here asserts wrongdoing by the council, a department, an officer or a supplier.

## Purpose

This audit tests whether the council's procurement controls under the Contract Procedure Rules operate as designed in the areas where the full spend population shows risk indicators. Every pattern named in this pack is an indicator to investigate, not a finding: legitimate call-offs, recurring charges, older contracts and framework purchases all produce the same patterns.
The pack covers only the risks the auditor approved and placed in scope at the gate. Care and education placements, and grants, are outside this pack by the auditor's decision.

## Background

8,534 payments from the council's published expenditure data across 3 months (2026-05-01 to 2026-07-31), totalling £66,778,104.78, were analysed against the Rules after statutory, inter-authority and redacted rows were excluded [metric:$.population.rows_after_exclusions] [metric:$.population.total_gbp].
General procurement accounts for 2,126 of those payments, worth £28,318,367.76 with 518 suppliers [metric:$.population.tags.general_procurement.gbp]. Most samples are drawn from this tag; agency staff are sampled under their own risk.
Published contract notices for the council (141 rows in the Contracts Finder export) were matched to suppliers; 674 suppliers have an annualised estimate at or above the publication tier of £25,000 [metric:$.tests.high_value_suppliers.tiers.publication_threshold.suppliers].

## Scope

The register lists 10 rated risks. The auditor recorded 11 decisions by Frank Fu (decisions drafted by Claude on Frank Fu's instruction) dated 2026-10-17: 9 risks are approved and in scope, and 2 are not.

| ID | Risk | Score | Band | Decision | Auditor comment |
|---|---|---|---|---|---|
| R-01 | Payments to one supplier grouped under a procedure threshold | 12 | Medium - High | approve | Strongest data signal in general procurement; test as proposed. |
| R-02 | Single payments sitting just below a quote or tender threshold | 12 | Medium - High | approve | Approved as rated at step 5.1 (closing the gate). |
| R-03 | High-value suppliers with no matching published contract notice | 12 | Medium - High | approve | Approved as rated at step 5.1 (closing the gate). |
| R-04 | Payments continuing after a published contract notice ended | 9 | Medium - High | approve | Approved as rated at step 5.1 (closing the gate). |
| R-05 | Spend running above the published award value | 9 | Medium - High | approve | Approved as rated at step 5.1 (closing the gate). |
| R-06 | Repeated payments of the same amount to the same supplier | 9 | Medium - High | approve | Approved as rated at step 5.1 (closing the gate). |
| R-07 | Waivers and exceptions to competition not approved or recorded | 4 | Moderate | amend | Set recommended scope to in scope: waivers cannot be seen in the spend data, so fieldwork must test the waiver and exception record directly. |
| R-08 | Award approval and Key Decisions for the largest contracts | 12 | Medium - High | approve | Approved as rated at step 5.1 (closing the gate). |
| R-11 | Agency staff bought without a competed contract | 8 | Medium - High | approve | Approved as rated at step 5.1 (closing the gate). |

**Not in scope**

- R-09: Care and education placements bought outside competition: approve; rated, recommended out of scope; approved as rated
- R-10: Grants and transfer payments that may be contracts: reject; Rejected by the auditor: Grants will be covered by a separate grants review.

## Approach

Testable rules were extracted from the Contract Procedure Rules with clause references. Python analysed the whole population for grouped payments, payments just below thresholds, suppliers with no matching notice, spend after a notice ended, spend above an award and repeated amounts. Each risk was rated on the council's own likelihood and impact scales, and the auditor approved scope at the gate.
For each approved risk the pack names the control the Rules require, a test of that control and a targeted sample drawn by script from the flagged lists, largest value first. Sample size follows the risk score: ten items at a score of nine or above, five below, all items where fewer exist. Off-contract and high-value work uses the auditor's publication tier of £25,000, so smaller suppliers are never questioned on notice coverage.
Waivers, exceptions and exclusions cannot be seen in the spend data, so they are tested from the council's own records rather than from a transaction sample.

The programme holds 11 expected controls and 16 test steps, with 238 sampled transactions worth £27,377,574.11, each traceable to its row in the council's published workbooks (see `audit-program.md` and `outputs/samples/`).

## Rules coverage

39 of 64 rules in `rules.json` are cited by a risk, a control or a test. The remaining 25 are not tested in this audit, for these reasons:

- consideration duty, not a control observable in spend or notice data: CPR-01
- budget provision is a finance control outside the procurement risks the auditor approved: CPR-03
- governance reporting step outside the spend data and not named in an approved risk: CPR-08
- tender handling and evaluation steps inside a procurement file; the approved risks test the route and approval chosen, not how tenders were evaluated: CPR-09, CPR-13, CPR-14, CPR-15, CPR-16, CPR-17, CPR-18
- procedure above the statutory Threshold, whose value is null in the Rules extract; the auditor confirms the Threshold before T-08.3, and award approval for the largest contracts is tested under R-08: CPR-56
- contract terms, indemnities, bonds and insurance are contract content; no approved risk covers them: CPR-34, CPR-35, CPR-36, CPR-37, CPR-38, CPR-39, CPR-40, CPR-41, CPR-42, CPR-43, CPR-44, CPR-45, CPR-46
- Provider Selection Regime contracts cannot be identified in the spend data and no approved risk covers them: CPR-58

## Limitations

- The population is the council's published expenditure above its publication floor only, so grouped-payment and repeat-amount counts are lower bounds. Dates are payment-run timestamps, not invoice dates.
- The notice export is not a contract register: contracts awarded before the export period, advertised elsewhere, or called off from another buyer's framework will have no notice. A missing or ended notice is an indicator to check against the council's register, never evidence of off-contract spend. Near-match supplier names are candidates for the auditor to confirm.
- Annualised estimates scale a short window and may misstate seasonal or one-off spend. Award values in notices may be estimates or framework maxima.
- The statutory procurement threshold is not set as a figure in the Rules extract, so tests above it are framed as conditional on the value the auditor confirms.
- At the publication tier the band just above the threshold holds 52 payments against 46 just below it, so R-02 tests the presence of near-threshold payments, not a proven cluster [metric:$.tests.threshold_clustering.by_threshold.25000.comparator_above.count].
- The spend-versus-award test covers only the 23 suppliers matched to a single active notice with an award value; suppliers with several candidate notices or none are not compared [metric:$.tests.spend_vs_award.suppliers_compared].
- 2,015 rows with a redacted supplier name, worth £2,746,746.71, are excluded from every supplier-level test [metric:$.population.excluded.redacted_supplier.rows].
- Care and education placement spend of £30,571,711.30, against analysed spend of £66,778,104.78, is left untested by the auditor's scope decision on R-09; the related personal-budgets audit gave Limited Assurance [history:AUD-16] [metric:$.population.tags.care_or_education_placement.gbp].

## Review and sign-off

The challenger's points and their status are in `challenges.md`; points marked *for the auditor* need a decision at sign-off. The QA reviewer's checks and verdict are in `review.md`, which ends with the sign-off block.
