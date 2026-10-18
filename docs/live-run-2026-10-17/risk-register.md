# Procurement risk register

*Generated 2026-10-17 by `build_register.py` from `risk-ratings.json`, `rules.json`, `analytics.json` and `history.json`.*

*Revision 1, following auditor comments by Live test (Claude, on Frank Fu instruction) dated 2026-10-17: R-07 amended (recommended scope out of scope -> in scope as the auditor asked); R-10 rejected (moved to excluded: grants will be covered by a separate grants review).*

**Indicators, not findings.** Every risk below describes a pattern in public data or a control the rules require. Nothing here asserts wrongdoing by the council, a department, an officer or a supplier.

**Scoring method.** Likelihood and impact on the council's own 1–5 scales (Risk Management Strategy 2024–2027, as extracted into `history.json`); score = likelihood × impact; matrix label from the council's 5×5 matrix (Figure 1); band and escalation from its RAG table (Table 4).
**Conflict in the method, not resolved here:** the RAG table escalates to the Corporate Risk Register from a score of 15, while the register inclusion rule says a score of 9 or above. Bands below follow the RAG table; the column 'Meets register inclusion score' marks the other rule.
- Method discrepancy recorded in history.json: [history:DISC-01] Prose labels Medium as (2); Table 1 and Figure 1 give Medium as 3.
- Method discrepancy recorded in history.json: [history:DISC-02] Impact budget-share bands overlap: Medium printed '0.1% - 0.3%', Major printed '0.25% - 1%'.
- Method discrepancy recorded in history.json: [history:DISC-03] Personal/Staff or Customers column for ratings 2 and 1 prints financial-loss amounts (£1,000+ / up to £1,000) that differ from the Financial column for the same ratings (£17.5k-£175k / under £17.5k).
- Method discrepancy recorded in history.json: [history:DISC-04] Band name differs: Table 4 calls 8-12 'Medium - High (Amber)'; Figure 1 labels those cells 'High'.
- Method discrepancy recorded in history.json: [history:DISC-05] Corporate Risk Register inclusion: Figure 4 says score 9 or above; Table 4 says add to CRR at Extreme 15-25; 6.3 says extreme (Red) risks are escalated for a decision on Directorate or Corporate register.
- Method discrepancy recorded in history.json: [history:DISC-06] Typo 'extrene' for 'extreme'.
- Method discrepancy recorded in history.json: [history:DISC-07] Reputation appetite headed 'Open', but this sentence uses the Table 3 'Cautious' descriptor wording ('Little chance of significant repercussions'); the paragraph ends seeking an open reputational risk.
- Method discrepancy recorded in history.json: [history:DISC-08] Evaluation level names differ: 4.1 uses Gross/Actual/Expected level; Appendix 2 uses Gross/Current/Expected Net risk rating.
- Method discrepancy recorded in history.json: [history:DISC-09] Appetite guidance cited as 'v.2., August2021' in 5.2 but 'V1.0, October 2020' in Appendix 2.
- Method discrepancy recorded in history.json: [history:DISC-10] Figure 4 names a 'Governance and Ethics Committee'; elsewhere the strategy refers to the Governance Committee.
- Method discrepancy recorded in history.json: [history:DISC-11] Policy statement points to Appendix A for the risk management policy; the contents list it as Appendix 1 (Appendix A is the strategy itself on p.5).

## Summary

| ID | Risk | L | I | Score | Matrix label | Band | Meets register inclusion score | Recommended scope |
|---|---|---|---|---|---|---|---|---|
| R-01 | Payments to one supplier grouped under a procedure threshold | 4 | 3 | 12 | High | Medium - High | yes | in scope |
| R-02 | Payments clustering just below a quote or tender threshold | 4 | 3 | 12 | High | Medium - High | yes | in scope |
| R-03 | High-value suppliers with no published contract notice | 3 | 4 | 12 | High | Medium - High | yes | in scope |
| R-04 | Spend continuing after a published contract notice ended | 3 | 3 | 9 | High | Medium - High | yes | in scope |
| R-05 | Spend running above the awarded contract value | 3 | 4 | 12 | High | Medium - High | yes | in scope |
| R-06 | Repeated payments of the same amount to the same supplier | 3 | 3 | 9 | High | Medium - High | yes | in scope |
| R-07 | Waivers and exceptions to competition | 1 | 4 | 4 | Moderate | Moderate | no | in scope |
| R-08 | Award approval and Key Decisions for the largest contracts | 3 | 4 | 12 | High | Medium - High | yes | in scope |
| R-09 | Care and education placements bought outside competition | 2 | 4 | 8 | High | Medium - High | no | in scope |
| R-11 | Agency staff bought without a visible contract route | 2 | 4 | 8 | High | Medium - High | no | in scope |

## R-01: Payments to one supplier grouped under a procedure threshold

**Risk.** Purchases may be split across several payments to one supplier so that each payment stays below a quote or tender threshold, a pattern to test against the anti-splitting rule.

**Likelihood 4 (Almost Certain).** Rubric row 4: the split-purchase test shows a general-procurement signal at more than one threshold: 80 windows at the one-quote tier [metric:$.tests.split_purchases.by_threshold.1000.headline_general_procurement.windows], 99 at the next tier [metric:$.tests.split_purchases.by_threshold.5000.headline_general_procurement.windows] and 42 crossing the publication tier [metric:$.tests.split_purchases.by_threshold.25000.headline_general_procurement.windows], tested against the anti-avoidance rule [rule:CPR-12]. Not raised to 5: the accounts payable and contract letting audits gave Reasonable Assurance [history:AUD-15] [history:AUD-01], so there is no adverse opinion on this theme and no repeat uplift.

**Impact 3 (Medium).** Medium on the council's scale [history:$.scoring_method.impact_scale[2]]: windows crossing the publication tier would have required Procurement Portal quotes from three sources [rule:CPR-53]; on a reasonable worst case [history:$.scoring_method.combination.reasonable_worst_case] that is a reasonable possibility of successful challenge. The general-procurement windows at that tier total £2,372,829.90 of spend [metric:$.tests.split_purchases.by_threshold.25000.headline_general_procurement.gbp]; this is spend under review, not loss, so the financial column is not used to go higher.

**Score 12: High; band Medium - High.** Escalation: Seek assurance that identified controls are effective. Response: Allocate to Service Director to put in place Controls Assurance..

**Evidence**

- [rule:CPR-12] clause 6.16: "There shall be no artificial splitting or disaggregation of a contract to avoid the application of the provisions of the Procurement…"
- [rule:CPR-52] clause App B row A: "Above £1,000 and less than £25,000 … At least one quote must be sought from an appropriate source."
- [rule:CPR-53] clause App B row B1: "£25,000 or more and less than the Threshold … Invitations to quote must be sent via the Procurement Portal to at least three appropriate…"
- [metric:$.tests.split_purchases.by_threshold.1000.headline_general_procurement.windows] = 80
- [metric:$.tests.split_purchases.by_threshold.5000.headline_general_procurement.windows] = 99
- [metric:$.tests.split_purchases.by_threshold.25000.headline_general_procurement.windows] = 42
- [metric:$.tests.split_purchases.by_threshold.25000.headline_general_procurement.gbp] = 2,372,829.90
- [history:AUD-15] Accounts Payable: Reasonable Assurance (audit-completed-work-2025-26-q3.pdf, p.1)

**Proposed focus.** For the largest general-procurement windows at the publication tier, obtain orders, quotes and invoices and test whether the payments form one requirement that should have been quoted or tendered as a whole. Sample source: `analytics-full/split-purchases.csv`.

## R-02: Payments clustering just below a quote or tender threshold

**Risk.** Payment values may be set just below a quote or tender threshold, which indicates a pattern to test against the procedure each threshold triggers.

**Likelihood 4 (Almost Certain).** Rubric row 4: general-procurement payments sit in the band just below more than one threshold: 88 below the one-quote tier [metric:$.tests.threshold_clustering.by_threshold.1000.by_tag.general_procurement.rows] [rule:CPR-52], 48 below the next tier [metric:$.tests.threshold_clustering.by_threshold.5000.by_tag.general_procurement.rows] [rule:CPR-06] and 10 below the publication tier [metric:$.tests.threshold_clustering.by_threshold.25000.by_tag.general_procurement.rows] [rule:CPR-53]. Caveat for the auditor: the comparator band just above each threshold is only reported across all tags, not for general procurement; across all tags the band below exceeds the band above only at the one-quote tier (323 against 216) [metric:$.tests.threshold_clustering.by_threshold.1000.comparator_above.count], and not at the publication tier (46 against 52) [metric:$.tests.threshold_clustering.by_threshold.25000.comparator_above.count]. No adverse audit on the theme [history:AUD-15], so no repeat uplift.

**Impact 3 (Medium).** Medium on the council's scale [history:$.scoring_method.impact_scale[2]]: on a reasonable worst case [history:$.scoring_method.combination.reasonable_worst_case] the payments just below the publication tier avoid the three-source Procurement Portal quote [rule:CPR-53]; the general-procurement band there totals £239,427.82 [metric:$.tests.threshold_clustering.by_threshold.25000.by_tag.general_procurement.gbp], within the Medium financial descriptor.

**Score 12: High; band Medium - High.** Escalation: Seek assurance that identified controls are effective. Response: Allocate to Service Director to put in place Controls Assurance..

**Evidence**

- [rule:CPR-52] clause App B row A: "Above £1,000 and less than £25,000 … At least one quote must be sought from an appropriate source."
- [rule:CPR-06] clause 5.2: "Details of every invitation to tender for contracts to provide goods and/or services with a value that exceeds £5,000."
- [rule:CPR-53] clause App B row B1: "£25,000 or more and less than the Threshold … Invitations to quote must be sent via the Procurement Portal to at least three appropriate…"
- [metric:$.tests.threshold_clustering.by_threshold.1000.by_tag.general_procurement.rows] = 88
- [metric:$.tests.threshold_clustering.by_threshold.5000.by_tag.general_procurement.rows] = 48
- [metric:$.tests.threshold_clustering.by_threshold.25000.by_tag.general_procurement.rows] = 10
- [metric:$.tests.threshold_clustering.by_threshold.1000.band.count] = 323
- [metric:$.tests.threshold_clustering.by_threshold.1000.comparator_above.count] = 216

**Proposed focus.** For general-procurement payments in the band below the publication tier, check the quote evidence held and whether related payments to the same supplier exceed the tier when combined. Sample source: `analytics-full/threshold-clustering.csv`.

## R-03: High-value suppliers with no published contract notice

**Risk.** Suppliers paid above the publication tier may be supplied without a contract that was advertised, published and recorded on the Contract Register as the rules require; no matching notice is an indicator to check against the register, not evidence of off-contract spend.

**Likelihood 3 (Likely).** Rubric row 3: one test designed for the rule shows a general-procurement signal: 191 general-procurement suppliers above the publication tier (annualised estimate) have no exact-match active notice [metric:$.tests.off_contract.unmatched_by_tag.general_procurement.suppliers], against the publication and register rules [rule:CPR-53] [rule:CPR-07] [rule:CPR-33]. The data cannot see the council's Contract Register itself [metric:$.contracts.register_present], and frameworks, older contracts and Find a Tender notices will legitimately be absent. The contract letting audit gave Reasonable Assurance [history:AUD-01], so no repeat uplift.

**Impact 4 (Major).** Major on the council's scale [history:$.scoring_method.impact_scale[1]]: on a reasonable worst case [history:$.scoring_method.combination.reasonable_worst_case] spend of this size without a published, competed contract carries a high possibility of legal challenge under the above-threshold procedures [rule:CPR-56]; the largest unmatched general-procurement supplier has an annualised estimate of £29,511,688.84 [metric:$.tests.off_contract.unmatched_general_procurement_top20[0].annualised_estimate], and the strategy names procurement contract management as a source of risk [history:$.risk_themes[7]].

**Score 12: High; band Medium - High.** Escalation: Seek assurance that identified controls are effective. Response: Allocate to Service Director to put in place Controls Assurance..

**Evidence**

- [rule:CPR-53] clause App B row B1: "£25,000 or more and less than the Threshold … Invitations to quote must be sent via the Procurement Portal to at least three appropriate…"
- [rule:CPR-56] clause App B row D: "Procurement Legislation Procedures apply– full competitive tender process with at least five written tenders sought (where appropriate) via…"
- [rule:CPR-07] clause 5.2.1: "A register of contracts, including those in progress and those awarded, with key information such as the contract value, duration and…"
- [rule:CPR-33] clause 10.4: "The relevant Service Director must formally notify the Service Lead for Commissioning and Procurement (or nominated officer) of the award…"
- [metric:$.tests.off_contract.unmatched_by_tag.general_procurement.suppliers] = 191
- [metric:$.tests.off_contract.unmatched_by_tag.general_procurement.annualised_estimate] = 99,551,762.72
- [metric:$.contracts.register_present] = False
- [history:AUD-01] Contract Letting: Reasonable Assurance (audit-completed-work-2024-25-annual.pdf, p.1)

**Proposed focus.** Trace the largest unmatched general-procurement suppliers to the Contract Register, framework call-off records or Find a Tender notices; where none exists, request the waiver or exception record. Sample source: `analytics-full/high-value-suppliers.csv`.

## R-04: Spend continuing after a published contract notice ended

**Risk.** Payments may continue after the contract they were let under has ended, without the approved extension the rules require; a newer contract may exist without a published notice.

**Likelihood 3 (Likely).** Rubric row 3: one test designed for the rule shows a general-procurement signal: 8 general-procurement suppliers were paid in the window although every matching notice had ended before it [metric:$.tests.expired_notice_spend.by_dominant_tag.general_procurement], to be tested against the extension approval rule [rule:CPR-60]. The contract letting audit gave Reasonable Assurance [history:AUD-01], so no repeat uplift.

**Impact 3 (Medium).** Medium on the council's scale [history:$.scoring_method.impact_scale[2]]: the flagged suppliers were paid £243,364.42 in the window [metric:$.tests.expired_notice_spend.gbp_in_window], within the Medium financial descriptor, and spend after expiry without S151 approval [rule:CPR-60] is a reasonable possibility of successful challenge.

**Score 9: High; band Medium - High.** Escalation: Seek assurance that identified controls are effective. Response: Allocate to Service Director to put in place Controls Assurance..

**Evidence**

- [rule:CPR-60] clause App C row D: "The proposed contract is an extension to an existing contract where the existing contract provides for such extension. … Approval of the…"
- [metric:$.tests.expired_notice_spend.by_dominant_tag.general_procurement] = 8
- [metric:$.tests.expired_notice_spend.gbp_in_window] = 243,364.42
- [metric:$.tests.expired_notice_spend.annualised_estimate] = 973,457.68
- [history:AUD-01] Contract Letting: Reasonable Assurance (audit-completed-work-2024-25-annual.pdf, p.1)

**Proposed focus.** For each flagged supplier, request the extension approval or the replacement contract and check its dates against the payments in the window. Sample source: `analytics-full/expired-notice-spend.csv`.

## R-05: Spend running above the awarded contract value

**Risk.** Spend with some contracted suppliers may run above the value awarded, which indicates a variation to test against the approvals the rules require; published award values may be estimates or maxima.

**Likelihood 3 (Likely).** Rubric row 3: one test designed for the rule shows a signal: 12 of 23 compared suppliers run at or above the flag ratio of the award's annual rate [metric:$.tests.spend_vs_award.suppliers_flagged], tested against the variation rules [rule:CPR-61] [rule:CPR-62]. The test has no tag split, so the general-procurement share cannot be shown; it only covers suppliers matched to a published notice. The contract letting audit gave Reasonable Assurance [history:AUD-01], so no repeat uplift.

**Impact 4 (Major).** Major on the council's scale [history:$.scoring_method.impact_scale[1]]: the flagged suppliers' annualised estimate is £5,353,417.28 [metric:$.tests.spend_vs_award.flagged_annualised_estimate] and the highest ratio is 13.84 [metric:$.tests.spend_vs_award.top20[0].ratio]; a variation above the Threshold needs a board report with Monitoring Officer and S151 recommendation [rule:CPR-62], and on a reasonable worst case [history:$.scoring_method.combination.reasonable_worst_case] an unapproved one carries a high possibility of challenge.

**Score 12: High; band Medium - High.** Escalation: Seek assurance that identified controls are effective. Response: Allocate to Service Director to put in place Controls Assurance..

**Evidence**

- [rule:CPR-61] clause App C row E: "The proposed contract is a variation of the scope of an existing contract … For contract value below the Threshold prior written approval…"
- [rule:CPR-62] clause App C row E: "The proposed contract is a variation of the scope of an existing contract … For contract value greater than the Threshold, approval of the…"
- [metric:$.tests.spend_vs_award.suppliers_flagged] = 12
- [metric:$.tests.spend_vs_award.suppliers_compared] = 23
- [metric:$.tests.spend_vs_award.flagged_annualised_estimate] = 5,353,417.28
- [metric:$.tests.spend_vs_award.top20[0].ratio] = 13.84

**Proposed focus.** For the flagged suppliers with the highest ratios, obtain the contract, its value basis and any approved variation, and reconcile them to spend. Sample source: `analytics-full/spend-vs-award.csv`.

## R-06: Repeated payments of the same amount to the same supplier

**Risk.** Some payments of an identical amount to one supplier within a few days may be duplicates rather than separate purchases, a pattern to test against the written evidence each purchase should have.

**Likelihood 3 (Likely).** Rubric row 3: one test designed for the rule shows a general-procurement signal: 35 general-procurement groups of same-supplier, same-amount payments on different payment runs within seven days [metric:$.tests.duplicates.different_time.by_tag.general_procurement.groups], tested against the requirement to keep written evidence of each purchase [rule:CPR-31]. The accounts payable audit gave Reasonable Assurance [history:AUD-15], so no repeat uplift.

**Impact 3 (Medium).** Medium on the council's scale [history:$.scoring_method.impact_scale[2]]: on a reasonable worst case [history:$.scoring_method.combination.reasonable_worst_case] the general-procurement amount beyond the first payment in each group, £299,374.24 [metric:$.tests.duplicates.different_time.by_tag.general_procurement.gbp_beyond_first], falls within the Medium financial descriptor; many groups will be legitimate recurring charges [rule:CPR-31].

**Score 9: High; band Medium - High.** Escalation: Seek assurance that identified controls are effective. Response: Allocate to Service Director to put in place Controls Assurance..

**Evidence**

- [rule:CPR-31] clause 10.1: "There should be written evidence of all purchases (which shall include electronic evidence)."
- [metric:$.tests.duplicates.different_time.by_tag.general_procurement.groups] = 35
- [metric:$.tests.duplicates.different_time.by_tag.general_procurement.gbp_beyond_first] = 299,374.24
- [history:AUD-15] Accounts Payable: Reasonable Assurance (audit-completed-work-2025-26-q3.pdf, p.1)

**Proposed focus.** For the general-procurement groups with the largest amount beyond the first payment, match each payment to a distinct invoice and order, and confirm any recovery. Sample source: `analytics-full/duplicates.csv`.

## R-07: Waivers and exceptions to competition

**Risk.** Competition may be waived without the documented, advance approval the rules require; this control is not visible in the spend or notice data.

**Likelihood 1 (Rare).** Rubric row 1: the rules require waivers above the waiver value to be approved in advance by the Monitoring Officer and/or S151 Officer and documented [rule:CPR-19] [rule:CPR-20] [rule:CPR-24] [rule:CPR-26], but the data cannot observe waivers (no waiver metric exists), and no audit in history names waivers [history:AUD-01]. The unmatched-supplier indicator in R-03 may include waived awards but cannot show them [metric:$.tests.off_contract.unmatched_by_tag.general_procurement.suppliers].

**Impact 4 (Major).** Major on the council's scale [history:$.scoring_method.impact_scale[1]]: an exception for a contract over the Key Decision value must go to the Executive [rule:CPR-23]; on a reasonable worst case [history:$.scoring_method.combination.reasonable_worst_case] an unapproved waiver at that value carries a high possibility of legal challenge, and the strategy's compliance appetite refers to approved standards for high value transactions [history:$.risk_themes[10]].

**Score 4: Moderate; band Moderate.** Escalation: None. Response: Monitor risk.

**Evidence**

- [rule:CPR-19] clause 7.2: "Subject to 7.4 the requirement for the Council to conduct a competitive purchasing process, contracts with a value of more than £24,999.99,…"
- [rule:CPR-20] clause 7.3: "Only the Monitoring Officer and/or the S.151 Officer may grant a waiver or an exception to these Rules"
- [rule:CPR-23] clause 7.4.3: "for contracts over £500,000 the S.151 Officer and the Monitoring Officer will make a recommendation to the Executive provided an exception…"
- [rule:CPR-24] clause 7.5.1: "All exceptions or waivers to these Rules must: … be fully documented;"
- [rule:CPR-26] clause 7.5.3: "be subject to approval by the S.151 Officer who shall record they have considered the reasons for the waiver and that they are satisfied…"
- [history:AUD-01] Contract Letting: Reasonable Assurance (audit-completed-work-2024-25-annual.pdf, p.1)

**Proposed focus.** Not a standalone test: where R-03, R-04 or R-05 find no contract, extension or variation, request the waiver record and check approval was in advance and by the right officer. Sample source: `analytics-full/high-value-suppliers.csv`.

## R-08: Award approval and Key Decisions for the largest contracts

**Risk.** The largest purchases may proceed without the Key Decision or Executive approval the rules require for their value; the approvals themselves are not visible in the data.

**Likelihood 3 (Likely).** Rubric row 3: one test shows a general-procurement signal at the Key Decision tier: 2 general-procurement windows of individually smaller payments that combine above it [metric:$.tests.split_purchases.by_threshold.500000.headline_general_procurement.windows], tested against the Key Decision and award approval rules [rule:CPR-04] [rule:CPR-50] [rule:CPR-51]. Whether a Key Decision was taken cannot be observed in the data. The contract letting audit gave Reasonable Assurance [history:AUD-01], so no repeat uplift.

**Impact 4 (Major).** Major on the council's scale [history:$.scoring_method.impact_scale[1]]: the larger of these windows totals £2,986,550.13 [metric:$.tests.split_purchases.by_threshold.500000.headline_general_procurement.top20[0].window_total]; an award at this value without Executive approval [rule:CPR-51] carries a high possibility of challenge, and the strategy's compliance appetite refers to high value transactions [history:$.risk_themes[10]]. Spend under review is not loss, so the financial column is not used to go higher.

**Score 12: High; band Medium - High.** Escalation: Seek assurance that identified controls are effective. Response: Allocate to Service Director to put in place Controls Assurance..

**Evidence**

- [rule:CPR-04] clause 4.3: "Any contract award with a value over £500,000 is a Key Decision of the Council."
- [rule:CPR-50] clause App A row 3: "Above £500,000 and less than £2.5million … The award of these contracts shall be a Key Decision delegated to the relevant Service Director…"
- [rule:CPR-51] clause App A row 4: "Contracts with a value in excess of £2.5million shall require Executive approval"
- [metric:$.tests.split_purchases.by_threshold.500000.headline_general_procurement.windows] = 2
- [metric:$.tests.split_purchases.by_threshold.500000.headline_general_procurement.gbp] = 3,509,528.75
- [history:AUD-01] Contract Letting: Reasonable Assurance (audit-completed-work-2024-25-annual.pdf, p.1)

**Proposed focus.** For the general-procurement windows above the Key Decision tier, trace the contract and confirm the Key Decision or Executive approval and the written report that preceded award. Sample source: `analytics-full/split-purchases.csv`.

## R-09: Care and education placements bought outside competition

**Risk.** Placements bought under the social care exclusion may lack the recorded reasons for the choice of provider that the rules require; recurring placement payments are expected and are not themselves an indicator.

**Likelihood 2 (Unlikely).** Rubric row 2: the flagged items are in the placement tag, where the pattern is expected: 129 placement windows above the publication tier [metric:$.tests.split_purchases.by_threshold.25000.care_or_education_placement.windows] and 204 same-amount placement groups [metric:$.tests.duplicates.different_time.by_tag.care_or_education_placement.groups], against the row F record-keeping rule [rule:CPR-63]. The care purchasing audit gave Reasonable Assurance [history:AUD-18]. The Limited Assurance on direct payments [history:AUD-16] concerns payments to service users, not placements commissioned under the exclusion, so it is not treated as the same theme: no repeat uplift (flagged for the auditor to confirm).

**Impact 4 (Major).** Major on the council's scale [history:$.scoring_method.impact_scale[1]]: 307 placement suppliers are above the publication tier with an annualised estimate of £121,699,473.28 [metric:$.tests.high_value_suppliers.tiers.publication_threshold.by_dominant_tag.care_or_education_placement.annualised_estimate]; the strategy names inflation in purchased social care as a pressure [history:$.risk_themes[1]], and placements above the Threshold need board approval of the exclusion [rule:CPR-64].

**Score 8: High; band Medium - High.** Escalation: Seek assurance that identified controls are effective. Response: Allocate to Service Director to put in place Controls Assurance..

**Evidence**

- [rule:CPR-63] clause App C row F: "Service Directors must ensure that a record of the reasons for the choice of provider is maintained on the individual's case notes."
- [rule:CPR-64] clause App C closing: "In the interests of clarity where an exemption is applied all contracts with an annual or total value of more than the Threshold must be…"
- [metric:$.tests.split_purchases.by_threshold.25000.care_or_education_placement.windows] = 129
- [metric:$.tests.high_value_suppliers.tiers.publication_threshold.by_dominant_tag.care_or_education_placement.annualised_estimate] = 121,699,473.28
- [history:AUD-18] Purchase of Residential and Nursing Care Provision: Reasonable Assurance (audit-completed-work-2025-26-q3.pdf, p.1)
- [history:AUD-16] Personal Budgets (Direct Payments): Limited Assurance (audit-completed-work-2025-26-q3.pdf, p.1)

**Proposed focus.** For the largest placement windows, check the case notes record the reasons for the provider chosen and, above the Threshold, that the board approved the exclusion. Sample source: `analytics-full/split-purchases.csv`.

## R-11: Agency staff bought without a visible contract route

**Risk.** Agency staff spend may be bought without a competed contract or a documented framework call-off; framework call-offs often carry no council notice, so this is an indicator to check.

**Likelihood 2 (Unlikely).** Nearest rubric row 2: the agency staff tag is outside the general-procurement headline the higher rows require; within it, 1 supplier above the publication tier has no matching notice [metric:$.tests.off_contract.unmatched_by_tag.agency_staff.suppliers] and 1 window combines above the Key Decision tier [metric:$.tests.split_purchases.by_threshold.500000.by_tag.agency_staff.windows], against the tender and anti-splitting rules [rule:CPR-56] [rule:CPR-12]. The recruitment audit gave Reasonable Assurance and is not about buying agency staff [history:AUD-14], so no repeat uplift.

**Impact 4 (Major).** Major on the council's scale [history:$.scoring_method.impact_scale[1]]: the unmatched agency supplier has an annualised estimate of £5,102,208.60 [metric:$.tests.off_contract.unmatched_by_tag.agency_staff.annualised_estimate]; spend at that level without a compliant route [rule:CPR-59] carries a high possibility of challenge. Spend under review is not loss, so the financial column is not used to go higher.

**Score 8: High; band Medium - High.** Escalation: Seek assurance that identified controls are effective. Response: Allocate to Service Director to put in place Controls Assurance..

**Evidence**

- [rule:CPR-56] clause App B row D: "Procurement Legislation Procedures apply– full competitive tender process with at least five written tenders sought (where appropriate) via…"
- [rule:CPR-59] clause App C row C: "The proposed contract is being awarded under a Purchasing Scheme (refer to 8 above) … Prior written approval from the Monitoring Officer is…"
- [rule:CPR-12] clause 6.16: "There shall be no artificial splitting or disaggregation of a contract to avoid the application of the provisions of the Procurement…"
- [metric:$.tests.off_contract.unmatched_by_tag.agency_staff.suppliers] = 1
- [metric:$.tests.off_contract.unmatched_by_tag.agency_staff.annualised_estimate] = 5,102,208.60
- [metric:$.population.tags.agency_staff.gbp] = 1,285,541.24
- [history:AUD-14] Recruitment (Talent Attraction) and Retention: Reasonable Assurance (audit-completed-work-2025-26-q3.pdf, p.1)

**Proposed focus.** Confirm the contract or framework under which the main agency supplier is engaged, and the Monitoring Officer approval of any direct call-off. Sample source: `analytics-full/high-value-suppliers.csv`.

## Excluded

- R-10: Rejected by the auditor: grants will be covered by a separate grants review.

## Auditor decisions

Recorded by Live test (Claude, on Frank Fu instruction) on 2026-10-17.

| ID | Decision | Comment | How it was applied |
|---|---|---|---|
| R-01 | approve | Approved as rated. | kept as rated |
| R-02 | approve | Approved as rated. | kept as rated |
| R-03 | approve | Approved as rated. | kept as rated |
| R-04 | approve | Approved as rated. | kept as rated |
| R-05 | approve | Approved as rated. | kept as rated |
| R-06 | approve | Approved as rated. | kept as rated |
| R-07 | amend | Set recommended scope to in scope: waivers are not visible in the spend data, so fieldwork must test the waiver record directly. | recommended scope out of scope -> in scope as the auditor asked |
| R-08 | approve | Approved as rated. | kept as rated |
| R-09 | approve | Approved as rated. | kept as rated |
| R-11 | approve | Approved as rated. | kept as rated |
| R-10 | reject | Grants will be covered by a separate grants review. | moved to Excluded with the auditor's reason |
