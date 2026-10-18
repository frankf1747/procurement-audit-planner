# Procurement risk register

*Generated 2026-10-17 by `build_register.py` from `risk-ratings.json`, `rules.json`, `analytics.json` and `history.json`.*

*Revision 2, following auditor comments by Frank Fu (decisions drafted by Claude on Frank Fu's instruction) dated 2026-10-17: no ratings changed; decisions recorded.*

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
| R-02 | Single payments sitting just below a quote or tender threshold | 4 | 3 | 12 | High | Medium - High | yes | in scope |
| R-03 | High-value suppliers with no matching published contract notice | 3 | 4 | 12 | High | Medium - High | yes | in scope |
| R-04 | Payments continuing after a published contract notice ended | 3 | 3 | 9 | High | Medium - High | yes | in scope |
| R-05 | Spend running above the published award value | 3 | 3 | 9 | High | Medium - High | yes | in scope |
| R-06 | Repeated payments of the same amount to the same supplier | 3 | 3 | 9 | High | Medium - High | yes | in scope |
| R-07 | Waivers and exceptions to competition not approved or recorded | 1 | 4 | 4 | Moderate | Moderate | no | in scope |
| R-08 | Award approval and Key Decisions for the largest contracts | 3 | 4 | 12 | High | Medium - High | yes | in scope |
| R-09 | Care and education placements bought outside competition | 2 | 3 | 6 | Moderate | Moderate | no | out of scope |
| R-11 | Agency staff bought without a competed contract | 2 | 4 | 8 | High | Medium - High | no | in scope |

## R-01: Payments to one supplier grouped under a procedure threshold

**Risk.** Purchases may be split across several payments so that each stays below a quote or tender threshold, which the anti-avoidance rule prohibits. This is a pattern to test, not a finding.

**Likelihood 4 (Almost Certain).** Data signal in general procurement at more than one threshold: 42 supplier windows combine sub-threshold payments to cross the publication tier of 25,000 [metric:$.tests.split_purchases.by_threshold.25000.headline_general_procurement.windows], 99 cross 5,000 [metric:$.tests.split_purchases.by_threshold.5000.headline_general_procurement.windows] and 2 cross 500,000 [metric:$.tests.split_purchases.by_threshold.500000.headline_general_procurement.windows], against the rule that a contract must not be split or disaggregated [rule:CPR-12]. Rubric row 4. The most recent purchasing audit is not adverse [history:AUD-15], so no repeat uplift. Windows are indicators: recurring call-offs under one contract also produce them.

**Impact 3 (Medium).** Medium on the council's scale [history:$.scoring_method.impact_scale[2]]: the general-procurement windows at the publication tier total 2,372,829.90 [metric:$.tests.split_purchases.by_threshold.25000.headline_general_procurement.gbp], and splitting at that tier would bypass the three-quote portal requirement [rule:CPR-53], a reasonable possibility of challenge rather than a probable one.

**Score 12: High; band Medium - High.** Escalation: Seek assurance that identified controls are effective. Response: Allocate to Service Director to put in place Controls Assurance..

**Evidence**

- [rule:CPR-12] clause 6.16: "There shall be no artificial splitting or disaggregation of a contract to avoid the application of the provisions of the Procurement…"
- [rule:CPR-53] clause App B row B1: "£25,000 or more and less than the Threshold … Invitations to quote must be sent via the Procurement Portal to at least three appropriate…"
- [metric:$.tests.split_purchases.by_threshold.25000.headline_general_procurement.windows] = 42
- [metric:$.tests.split_purchases.by_threshold.25000.headline_general_procurement.gbp] = 2,372,829.90
- [metric:$.tests.split_purchases.by_threshold.5000.headline_general_procurement.windows] = 99
- [metric:$.tests.split_purchases.by_threshold.500000.headline_general_procurement.windows] = 2
- [history:AUD-15] Accounts Payable: Reasonable Assurance (audit-completed-work-2025-26-q3.pdf, p.1)

**Proposed focus.** Take the largest general-procurement windows at the publication tier and above, and test whether the grouped payments relate to one requirement and whether quotes, a portal exercise or a contract cover the combined value. Sample source: `analytics-full/split-purchases.csv`.

## R-02: Single payments sitting just below a quote or tender threshold

**Risk.** Individual payments may be set just under a quote or tender threshold to avoid the procedure the rules require. This is an indicator to test against the comparator band above each threshold.

**Likelihood 4 (Almost Certain).** Data signal in general procurement at more than one threshold: 10 general-procurement payments fall in the band just below the publication tier [metric:$.tests.threshold_clustering.by_threshold.25000.by_tag.general_procurement.rows], 48 below 5,000 [metric:$.tests.threshold_clustering.by_threshold.5000.by_tag.general_procurement.rows] and 88 below 1,000 [metric:$.tests.threshold_clustering.by_threshold.1000.by_tag.general_procurement.rows], the bands set by App B rows A, B1 and B2 [rule:CPR-52] [rule:CPR-53]. Rubric row 4. Across all tags the comparator band just above the publication tier holds 52 payments against 46 below it [metric:$.tests.threshold_clustering.by_threshold.25000.comparator_above.count], so the band shows no excess at that tier overall; the signal is the presence of general-procurement payments to test, not a proven cluster. No adverse purchasing audit [history:AUD-15].

**Impact 3 (Medium).** Medium on the council's scale [history:$.scoring_method.impact_scale[2]]: the general-procurement payments just below the publication tier total 239,427.82 [metric:$.tests.threshold_clustering.by_threshold.25000.by_tag.general_procurement.gbp], in the scale's Medium financial range, and the procedure avoided would be the three-quote portal exercise [rule:CPR-53].

**Score 12: High; band Medium - High.** Escalation: Seek assurance that identified controls are effective. Response: Allocate to Service Director to put in place Controls Assurance..

**Evidence**

- [rule:CPR-52] clause App B row A: "Above £1,000 and less than £25,000 … At least one quote must be sought from an appropriate source."
- [rule:CPR-53] clause App B row B1: "£25,000 or more and less than the Threshold … Invitations to quote must be sent via the Procurement Portal to at least three appropriate…"
- [metric:$.tests.threshold_clustering.by_threshold.25000.by_tag.general_procurement.rows] = 10
- [metric:$.tests.threshold_clustering.by_threshold.25000.by_tag.general_procurement.gbp] = 239,427.82
- [metric:$.tests.threshold_clustering.by_threshold.25000.band.count] = 46
- [metric:$.tests.threshold_clustering.by_threshold.25000.comparator_above.count] = 52
- [metric:$.tests.threshold_clustering.by_threshold.5000.by_tag.general_procurement.rows] = 48

**Proposed focus.** Sample general-procurement payments in the band below the publication tier and below the tender-publication figure, and check whether each payment is a complete requirement with the quotes its value needs, or part of a larger order. Sample source: `analytics-full/threshold-clustering.csv`.

## R-03: High-value suppliers with no matching published contract notice

**Risk.** Spend with some suppliers above the publication tier may not be covered by a published contract or recorded on the contract register. The notice export is not a register, so a missing notice is an indicator to check, never evidence of off-contract spend.

**Likelihood 3 (Likely).** One test designed for the rule shows a general-procurement signal: 191 general-procurement suppliers at or above the publication tier have no exact-match active notice [metric:$.tests.off_contract.unmatched_by_tag.general_procurement.suppliers], against the requirements to run a portal exercise at that tier [rule:CPR-53] and to keep a published register of contracts [rule:CPR-07] [rule:CPR-33]. Rubric row 3. The latest contract-letting audit is not adverse [history:AUD-01], so no repeat uplift. Older contracts, framework call-offs and notices published elsewhere will appear here without being off contract.

**Impact 4 (Major).** Major on the council's scale [history:$.scoring_method.impact_scale[1]]: the unmatched general-procurement suppliers carry an annualised estimate of 99,551,762.72 [metric:$.tests.off_contract.unmatched_by_tag.general_procurement.annualised_estimate], and where spend exceeds the statutory threshold without advertisement [rule:CPR-10] the compliance descriptor is a high possibility of legal challenge. The council's compliance appetite names high value transactions [history:$.risk_themes[10]].

**Score 12: High; band Medium - High.** Escalation: Seek assurance that identified controls are effective. Response: Allocate to Service Director to put in place Controls Assurance..

**Evidence**

- [rule:CPR-53] clause App B row B1: "£25,000 or more and less than the Threshold … Invitations to quote must be sent via the Procurement Portal to at least three appropriate…"
- [rule:CPR-07] clause 5.2.1: "A register of contracts, including those in progress and those awarded, with key information such as the contract value, duration and…"
- [rule:CPR-33] clause 10.4: "The relevant Service Director must formally notify the Service Lead for Commissioning and Procurement (or nominated officer) of the award…"
- [rule:CPR-10] clause 6.10: "All contract opportunities which are above the relevant Procurement Legislation thresholds must be advertised on the CDP database"
- [metric:$.tests.off_contract.unmatched_by_tag.general_procurement.suppliers] = 191
- [metric:$.tests.off_contract.unmatched_by_tag.general_procurement.annualised_estimate] = 99,551,762.72
- [metric:$.tests.high_value_suppliers.tiers.publication_threshold.headline_general_procurement_suppliers] = 228
- [history:AUD-01] Contract Letting: Reasonable Assurance (audit-completed-work-2024-25-annual.pdf, p.1)

**Proposed focus.** Request the council's contract register and match the largest unmatched general-procurement suppliers to a contract, framework call-off or approved exception; review the near-match list before sampling. Sample source: `analytics-full/high-value-suppliers.csv`.

## R-04: Payments continuing after a published contract notice ended

**Risk.** Some suppliers may be paid after their published contract term ended without an approved extension. A newer contract may exist with no notice, so this is an indicator to check.

**Likelihood 3 (Likely).** One test designed for the rule shows a general-procurement signal: 8 general-procurement suppliers were paid in the window although every matching notice had ended before it started [metric:$.tests.expired_notice_spend.by_dominant_tag.general_procurement], against the requirement for S151 approval of an extension [rule:CPR-60]. Rubric row 3. The latest contract-letting audit is not adverse [history:AUD-01].

**Impact 3 (Medium).** Medium on the council's scale [history:$.scoring_method.impact_scale[2]]: in-window spend with these suppliers is 243,364.42 [metric:$.tests.expired_notice_spend.gbp_in_window], within the scale's Medium financial range, and an unapproved extension is a reasonable possibility of challenge [rule:CPR-60]. The strategy names procurement contract management as a source of risk [history:$.risk_themes[7]].

**Score 9: High; band Medium - High.** Escalation: Seek assurance that identified controls are effective. Response: Allocate to Service Director to put in place Controls Assurance..

**Evidence**

- [rule:CPR-60] clause App C row D: "The proposed contract is an extension to an existing contract where the existing contract provides for such extension. … Approval of the…"
- [metric:$.tests.expired_notice_spend.suppliers] = 8
- [metric:$.tests.expired_notice_spend.gbp_in_window] = 243,364.42
- [metric:$.tests.expired_notice_spend.annualised_estimate] = 973,457.68
- [history:$.risk_themes[7]] Contracts & partnerships: contractor failure, procurement contract management (risk-management-strategy-2024-27.pdf, p.33)

**Proposed focus.** For each flagged supplier, obtain the current contract or the approved extension and the S151 approval covering the payment dates. Sample source: `analytics-full/expired-notice-spend.csv`.

## R-05: Spend running above the published award value

**Risk.** Spend with some contracted suppliers may run beyond the awarded value without an approved variation. Award values may be estimates or maxima, so this is an indicator to check against variations.

**Likelihood 3 (Likely).** One test designed for the rule shows a signal: 12 of 23 suppliers matched to a single active notice have an annualised estimate at or above the flag ratio of the award's annual rate [metric:$.tests.spend_vs_award.suppliers_flagged], against the approval required for a contract variation [rule:CPR-61] [rule:CPR-62]. The test compares only suppliers holding a published notice and carries no tag split. Rubric row 3. No adverse contract audit in history [history:AUD-01].

**Impact 3 (Medium).** Medium on the council's scale [history:$.scoring_method.impact_scale[2]]: the flagged suppliers carry an annualised estimate of 5,353,417.28 [metric:$.tests.spend_vs_award.flagged_annualised_estimate], but the excess over award is unknown until variations are seen; an unapproved variation [rule:CPR-62] is a reasonable possibility of challenge.

**Score 9: High; band Medium - High.** Escalation: Seek assurance that identified controls are effective. Response: Allocate to Service Director to put in place Controls Assurance..

**Evidence**

- [rule:CPR-61] clause App C row E: "The proposed contract is a variation of the scope of an existing contract … For contract value below the Threshold prior written approval…"
- [rule:CPR-62] clause App C row E: "The proposed contract is a variation of the scope of an existing contract … For contract value greater than the Threshold, approval of the…"
- [metric:$.tests.spend_vs_award.suppliers_flagged] = 12
- [metric:$.tests.spend_vs_award.suppliers_compared] = 23
- [metric:$.tests.spend_vs_award.flagged_annualised_estimate] = 5,353,417.28

**Proposed focus.** For the flagged suppliers, obtain the award, any approved variations and the board or Monitoring Officer and S151 approvals, and compare them with spend to date. Sample source: `analytics-full/spend-vs-award.csv`.

## R-06: Repeated payments of the same amount to the same supplier

**Risk.** Some payments may be duplicates of earlier payments of the same amount to the same supplier within a week. Legitimate repeat charges also produce this pattern, so it is an indicator to test.

**Likelihood 3 (Likely).** One test designed for the rule shows a general-procurement signal: 35 general-procurement groups repeat the same amount to the penny across different payment runs within seven days [metric:$.tests.duplicates.different_time.by_tag.general_procurement.groups], where every purchase must be backed by written evidence [rule:CPR-31]. Rubric row 3. The accounts payable audit gave Reasonable Assurance [history:AUD-15], so no repeat uplift.

**Impact 3 (Medium).** Medium on the council's scale [history:$.scoring_method.impact_scale[2]]: the general-procurement amount beyond the first payment in each group is 299,374.24 [metric:$.tests.duplicates.different_time.by_tag.general_procurement.gbp_beyond_first], within the scale's Medium financial range, and the strategy names financial control and fraud as a source of risk [history:$.risk_themes[5]].

**Score 9: High; band Medium - High.** Escalation: Seek assurance that identified controls are effective. Response: Allocate to Service Director to put in place Controls Assurance..

**Evidence**

- [rule:CPR-31] clause 10.1: "There should be written evidence of all purchases (which shall include electronic evidence)."
- [metric:$.tests.duplicates.different_time.by_tag.general_procurement.groups] = 35
- [metric:$.tests.duplicates.different_time.by_tag.general_procurement.gbp_beyond_first] = 299,374.24
- [metric:$.tests.duplicates.same_timestamp.by_tag.general_procurement.groups] = 33
- [history:AUD-15] Accounts Payable: Reasonable Assurance (audit-completed-work-2025-26-q3.pdf, p.1)

**Proposed focus.** Trace the largest general-procurement groups to invoices and orders to confirm each payment is for a separate supply, and check for recovery of any true duplicate. Sample source: `analytics-full/duplicates.csv`.

## R-07: Waivers and exceptions to competition not approved or recorded

**Risk.** Competition may be waived without the approvals, exception report or record the rules require. The spend data cannot observe waivers, so this is a control gap to confirm, not a pattern in the data.

**Likelihood 1 (Rare).** The rules limit waivers above their threshold to urgency or Executive Director circumstances [rule:CPR-19], require approval by the Monitoring Officer and/or S151 Officer [rule:CPR-20] and full documentation [rule:CPR-24] [rule:CPR-26]. The spend data cannot observe waivers or their approvals, and no audit in history names waivers; the latest contract-letting audit is not adverse [history:AUD-01]. Rubric row 1.

**Impact 4 (Major).** Major on the council's scale [history:$.scoring_method.impact_scale[1]]: exceptions above the relevant threshold and over the Key Decision level need S151, Monitoring Officer and Executive approval [rule:CPR-22] [rule:CPR-23], and an unsupported waiver of competition carries a high possibility of legal challenge.

**Score 4: Moderate; band Moderate.** Escalation: None. Response: Monitor risk.

**Evidence**

- [rule:CPR-19] clause 7.2: "Subject to 7.4 the requirement for the Council to conduct a competitive purchasing process, contracts with a value of more than £24,999.99,…"
- [rule:CPR-20] clause 7.3: "Only the Monitoring Officer and/or the S.151 Officer may grant a waiver or an exception to these Rules"
- [rule:CPR-24] clause 7.5.1: "All exceptions or waivers to these Rules must: … be fully documented;"
- [rule:CPR-26] clause 7.5.3: "be subject to approval by the S.151 Officer who shall record they have considered the reasons for the waiver and that they are satisfied…"
- [rule:CPR-23] clause 7.4.3: "for contracts over £500,000 the S.151 Officer and the Monitoring Officer will make a recommendation to the Executive provided an exception…"
- [history:AUD-01] Contract Letting: Reasonable Assurance (audit-completed-work-2024-25-annual.pdf, p.1)

**Proposed focus.** Request the waiver and exception register for the period and walk through approval and recording for a few entries; no data-driven sample is possible. Sample source: `analytics-full/high-value-suppliers.csv`.

## R-08: Award approval and Key Decisions for the largest contracts

**Risk.** The largest purchases may proceed without the Key Decision, Portfolio Holder or Executive approval that their value requires. This is an indicator to test against decision records.

**Likelihood 3 (Likely).** One test shows a general-procurement signal at the Key Decision level: 2 general-procurement supplier windows combine payments above 500,000 within thirty days [metric:$.tests.split_purchases.by_threshold.500000.headline_general_procurement.windows], where an award over that value is a Key Decision [rule:CPR-04] [rule:CPR-50] and the highest band needs the Executive [rule:CPR-51]. No single general-procurement payment sits just below that level [metric:$.tests.threshold_clustering.by_threshold.500000.by_tag.general_procurement.rows]. Rubric row 3. Approval records themselves cannot be observed in the data, and no governance audit in history is adverse [history:AUD-01].

**Impact 4 (Major).** Major on the council's scale [history:$.scoring_method.impact_scale[1]]: the general-procurement windows at this level total 3,509,528.75 [metric:$.tests.split_purchases.by_threshold.500000.headline_general_procurement.gbp], and an award without its Key Decision [rule:CPR-04] carries a high possibility of legal challenge and national adverse publicity.

**Score 12: High; band Medium - High.** Escalation: Seek assurance that identified controls are effective. Response: Allocate to Service Director to put in place Controls Assurance..

**Evidence**

- [rule:CPR-04] clause 4.3: "Any contract award with a value over £500,000 is a Key Decision of the Council."
- [rule:CPR-50] clause App A row 3: "Above £500,000 and less than £2.5million … The award of these contracts shall be a Key Decision delegated to the relevant Service Director…"
- [rule:CPR-51] clause App A row 4: "Contracts with a value in excess of £2.5million shall require Executive approval"
- [metric:$.tests.split_purchases.by_threshold.500000.headline_general_procurement.windows] = 2
- [metric:$.tests.split_purchases.by_threshold.500000.headline_general_procurement.gbp] = 3,509,528.75
- [metric:$.tests.threshold_clustering.by_threshold.500000.by_tag.general_procurement.rows] = 0

**Proposed focus.** For the general-procurement windows at the Key Decision level and the largest annualised suppliers, obtain the award decision and confirm the approver matches Appendix A. Sample source: `analytics-full/split-purchases.csv`.

## R-09: Care and education placements bought outside competition

**Risk.** Placements bought under the social care exclusion may lack the recorded reasons for the choice of provider that the rules require. Recurring placement fees are expected, so this is an indicator to test.

**Likelihood 2 (Unlikely).** Flagged items sit only in the placement tag, where recurring payments are expected: 129 placement windows cross the publication tier [metric:$.tests.split_purchases.by_threshold.25000.care_or_education_placement.windows] and 204 placement repeat-amount groups appear [metric:$.tests.duplicates.different_time.by_tag.care_or_education_placement.groups]. The row F exclusion requires reasons for the choice of provider on the case notes [rule:CPR-63], which the data cannot observe. Rubric row 2. The care-purchasing audit gave Reasonable Assurance [history:AUD-18]; the Limited Assurance audit of personal budgets [history:AUD-16] covers direct payments to service users, a different purchasing route, so no repeat uplift is applied.

**Impact 3 (Medium).** Medium on the council's scale [history:$.scoring_method.impact_scale[2]]: placement spend in the window is 30,571,711.30 [metric:$.population.tags.care_or_education_placement.gbp], but the control at stake is a case-note record [rule:CPR-63], whose failure fits external agency criticism rather than legal challenge. The strategy records inflation pressure in purchased social care [history:$.risk_themes[1]].

**Score 6: Moderate; band Moderate.** Escalation: None. Response: Monitor risk.

**Evidence**

- [rule:CPR-63] clause App C row F: "Service Directors must ensure that a record of the reasons for the choice of provider is maintained on the individual's case notes."
- [metric:$.tests.split_purchases.by_threshold.25000.care_or_education_placement.windows] = 129
- [metric:$.tests.duplicates.different_time.by_tag.care_or_education_placement.groups] = 204
- [metric:$.population.tags.care_or_education_placement.gbp] = 30,571,711.30
- [history:AUD-18] Purchase of Residential and Nursing Care Provision: Reasonable Assurance (audit-completed-work-2025-26-q3.pdf, p.1)
- [history:AUD-16] Personal Budgets (Direct Payments): Limited Assurance (audit-completed-work-2025-26-q3.pdf, p.1)

**Proposed focus.** Sample the largest placement windows and confirm the reasons for the provider choice are recorded on the case notes. Sample source: `analytics-full/split-purchases.csv`.

## R-11: Agency staff bought without a competed contract

**Risk.** Agency staff may be bought above the publication tier without a competed contract or framework call-off. Framework call-offs often carry no notice of their own, so this is an indicator to test.

**Likelihood 2 (Unlikely).** The signal sits in the agency staff tag, outside the general-procurement headline, so rubric rows 5 to 3 do not apply and row 2 is the nearest fit: 1 agency supplier at or above the publication tier has no matching notice [metric:$.tests.off_contract.unmatched_by_tag.agency_staff.suppliers] and 1 agency window crosses the Key Decision level [metric:$.tests.split_purchases.by_threshold.500000.by_tag.agency_staff.windows], against the portal quote requirement [rule:CPR-53] and the anti-avoidance rule [rule:CPR-12]. No workforce audit in history is adverse [history:AUD-14].

**Impact 4 (Major).** Major on the council's scale [history:$.scoring_method.impact_scale[1]]: the unmatched agency spend carries an annualised estimate of 5,102,208.60 [metric:$.tests.off_contract.unmatched_by_tag.agency_staff.annualised_estimate], in the scale's Major financial range, and a purchase of that size without a competed route needs approval at the level Appendix A sets for its value [rule:CPR-50] [rule:CPR-51].

**Score 8: High; band Medium - High.** Escalation: Seek assurance that identified controls are effective. Response: Allocate to Service Director to put in place Controls Assurance..

**Evidence**

- [rule:CPR-53] clause App B row B1: "£25,000 or more and less than the Threshold … Invitations to quote must be sent via the Procurement Portal to at least three appropriate…"
- [rule:CPR-51] clause App A row 4: "Contracts with a value in excess of £2.5million shall require Executive approval"
- [rule:CPR-59] clause App C row C: "The proposed contract is being awarded under a Purchasing Scheme (refer to 8 above) … Prior written approval from the Monitoring Officer is…"
- [metric:$.tests.off_contract.unmatched_by_tag.agency_staff.suppliers] = 1
- [metric:$.tests.off_contract.unmatched_by_tag.agency_staff.annualised_estimate] = 5,102,208.60
- [metric:$.tests.split_purchases.by_threshold.500000.by_tag.agency_staff.windows] = 1

**Proposed focus.** Confirm the contract or framework under which agency staff are bought, the Monitoring Officer approval for any direct call-off, and the award approval for its value. Sample source: `analytics-full/high-value-suppliers.csv`.

## Excluded

- R-10: Grants and transfer payments that may be contracts: Rejected by the auditor: Grants will be covered by a separate grants review.

## Auditor decisions

Recorded by Frank Fu (decisions drafted by Claude on Frank Fu's instruction) on 2026-10-17.

| ID | Decision | Comment | How it was applied |
|---|---|---|---|
| R-01 | approve | Strongest data signal in general procurement; test as proposed. | kept as rated |
| R-02 | approve | Approved as rated at step 5.1 (closing the gate). | kept as rated |
| R-03 | approve | Approved as rated at step 5.1 (closing the gate). | kept as rated |
| R-04 | approve | Approved as rated at step 5.1 (closing the gate). | kept as rated |
| R-05 | approve | Approved as rated at step 5.1 (closing the gate). | kept as rated |
| R-06 | approve | Approved as rated at step 5.1 (closing the gate). | kept as rated |
| R-07 | amend | Set recommended scope to in scope: waivers cannot be seen in the spend data, so fieldwork must test the waiver and exception record directly. | [] |
| R-08 | approve | Approved as rated at step 5.1 (closing the gate). | kept as rated |
| R-09 | approve | Approved as rated at step 5.1 (closing the gate). | kept as rated |
| R-11 | approve | Approved as rated at step 5.1 (closing the gate). | kept as rated |
| R-10 | reject | Grants will be covered by a separate grants review. | moved to Excluded with the auditor's reason |
