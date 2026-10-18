# Procurement audit: planning memo

*Generated 2026-10-17 by `build_pack.py` from `audit-plan.json`, `risk-register.md` (revision 1), `auditor-comments.md` by Live test (Claude, on Frank Fu instruction) dated 2026-10-17, `rules.json` and `analytics.json`. Status: DRAFT for challenge, QA review and auditor sign-off.*

**Indicators, not findings.** Every test below checks a control against a pattern in public data. Nothing here asserts wrongdoing by the council, a department, an officer or a supplier.

## Purpose

This audit tests whether the council's procurement controls operate as the Contract Procedure Rules require, focusing on the patterns that full-population analysis of published spend flagged as risk indicators. The patterns are indicators to investigate, not findings: each test checks a control against the evidence the Rules require and allows for every legitimate route.

## Background

8,534 payments over five hundred pounds worth £66,778,104.78 from 3 monthly workbooks (2026-05-01 to 2026-07-31) remain after excluding redacted-supplier, statutory pension and inter-authority rows [metric:$.population.rows_after_exclusions]. Of these, 2,126 payments worth £28,318,367.76 are general procurement [metric:$.population.tags.general_procurement.gbp]; the rest are tagged as care or education placements, grants, agency staff or premises costs.
Contracts Finder holds 141 award notices for the council, 62 of them active in the spend window [metric:$.contracts.active_in_window]. The council's own Contract Register is not public [metric:$.contracts.register_present], so notice matching is a proxy for it.
Recent internal audits gave Reasonable Assurance on contract letting [history:AUD-01] and accounts payable [history:AUD-15]. Personal Budgets (Direct Payments) received Limited Assurance [history:AUD-16]; the register treats it as a different theme from placements commissioned under the social care exclusion and applies no repeat uplift to R-09, a judgment it flags for the auditor to confirm.

## Scope

The register lists 10 rated risks. The auditor recorded 11 decisions by Live test (Claude, on Frank Fu instruction) dated 2026-10-17: 10 risks are approved and in scope, and 1 is not.

| ID | Risk | Score | Band | Decision | Auditor comment |
|---|---|---|---|---|---|
| R-01 | Payments to one supplier grouped under a procedure threshold | 12 | Medium - High | approve | Approved as rated. |
| R-02 | Payments clustering just below a quote or tender threshold | 12 | Medium - High | approve | Approved as rated. |
| R-03 | High-value suppliers with no published contract notice | 12 | Medium - High | approve | Approved as rated. |
| R-04 | Spend continuing after a published contract notice ended | 9 | Medium - High | approve | Approved as rated. |
| R-05 | Spend running above the awarded contract value | 12 | Medium - High | approve | Approved as rated. |
| R-06 | Repeated payments of the same amount to the same supplier | 9 | Medium - High | approve | Approved as rated. |
| R-07 | Waivers and exceptions to competition | 4 | Moderate | amend | Set recommended scope to in scope: waivers are not visible in the spend data, so fieldwork must test the waiver record directly. |
| R-08 | Award approval and Key Decisions for the largest contracts | 12 | Medium - High | approve | Approved as rated. |
| R-09 | Care and education placements bought outside competition | 8 | Medium - High | approve | Approved as rated. |
| R-11 | Agency staff bought without a visible contract route | 8 | Medium - High | approve | Approved as rated. |

**Not in scope**

- R-10: Grants and transfer payments that may be contracts: reject; Rejected by the auditor: grants will be covered by a separate grants review.

## Approach

Testable rules were extracted from the Contract Procedure Rules with clause references and verbatim quotes. Python scripts tested every payment against those thresholds: clustering below a tier, split purchases within 30 days, high-value suppliers with no matching notice, same-amount repeats within 7 days, spend after a notice ended, and spend against the award value. The risk-assessor rated each risk on the council's own likelihood and impact scales, citing a rule, a metric or an audit history item for every rating; the auditor then approved the scope set out above.
For each approved risk the programme names the control the Rules require, a test step with complete pass routes, and a targeted sample drawn by script from the flagged lists: ten items for risks scored nine or above, five for lower, every item where fewer are flagged (and every flagged supplier for spend against award), and the largest payments within each grouped window or supplier. Every sampled transaction is verified against the cleaned spend data. Waivers (R-07) are not visible in the data and are tested from the council's own waiver record and as a follow-through on other tests.

The programme holds 11 expected controls and 17 test steps, with 329 sampled transactions worth £34,801,040.92, each traceable to its row in the council's published workbooks (see `audit-program.md` and `outputs/samples/`).

## Rules coverage

43 of 64 rules in `rules.json` are cited by a risk, a control or a test. The remaining 21 are not tested in this audit, for these reasons:

- procurement-design duty (social value consideration); no approved risk addresses it and the records sampled cannot show it: CPR-01
- monthly reporting of contracts let to the relevant board; internal governance reporting outside the approved risks and not evidenced in the records sampled: CPR-08
- tender-conduct controls inside a procurement exercise (portal format, late tenders, opening, evaluation, award basis); no approved risk addresses tender conduct and the spend data cannot show it: CPR-14, CPR-15, CPR-16, CPR-17, CPR-18
- contract content, execution, insurance, bond and indemnity requirements; no approved risk addresses contract terms: CPR-34, CPR-35, CPR-36, CPR-37, CPR-38, CPR-39, CPR-40, CPR-41, CPR-42, CPR-43, CPR-44, CPR-45, CPR-46, CPR-47

## Limitations

- Annualised estimates scale 3 months of spend by 4 [metric:$.population.annualisation_factor]; they are estimates, not contract values.
- The Rules do not print the Procurement Legislation Threshold figures, so no analytics test ran at those tiers. The auditor should confirm the figures before fieldwork on T-05.1, T-07.1, T-08.2 and T-09.1, which apply approval levels set by the Threshold.
- Contracts Finder notices are not a contract register: frameworks, older contracts, Find a Tender notices and exempt placements will legitimately be absent, so a missing notice is an indicator to trace, never evidence of off-contract spend. Suppliers below £25,000 annualised were not classed [metric:$.tests.off_contract.parameters.threshold].
- 2,015 redacted-supplier payments worth £2,746,746.71 are excluded from all supplier-level tests [metric:$.population.excluded.redacted_supplier.rows].
- Dates are payment-run timestamps, not invoice dates, and only payments over five hundred pounds are published, so split-purchase and duplicate counts are lower bounds.
- Across all tags the band just below £25,000 holds 46 payments against 52 just above it [metric:$.tests.threshold_clustering.by_threshold.25000.comparator_above.count], so T-02.1 tests a band with no clustering excess; it is kept because the three-quote tier starts there.
- R-05 covers only the 23 suppliers matched exactly to one active single-supplier notice with an award value [metric:$.tests.spend_vs_award.suppliers_compared]; spend against award is not measured for any other supplier.
- Award values in Contracts Finder may be estimates or maxima, so a ratio at or above 1.25 is an indicator to reconcile, not an overspend [metric:$.tests.spend_vs_award.parameters.ratio_flag].
- Left untested: R-10 was rejected for a separate grants review, so 339 grant-tagged payments worth £6,033,599.82 are not tested here [metric:$.population.tags.grant.gbp]; the audit history extracted for this plan records no grants audit.

## Review and sign-off

The challenger's points and their status are in `challenges.md`; points marked *for the auditor* need a decision at sign-off. The QA reviewer's checks and verdict are in `review.md`, which ends with the sign-off block.
