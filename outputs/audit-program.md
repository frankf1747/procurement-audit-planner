# Audit program

*Generated 2026-10-17 by `build_pack.py` from `audit-plan.json`, `risk-register.md` (revision 2), `auditor-comments.md` by Frank Fu (decisions drafted by Claude on Frank Fu's instruction) dated 2026-10-17, `rules.json` and `analytics.json`. Status: DRAFT for challenge, QA review and auditor sign-off.*

**Indicators, not findings.** Every test below checks a control against a pattern in public data. Nothing here asserts wrongdoing by the council, a department, an officer or a supplier.

9 risks in scope, 11 controls, 16 tests, 238 sampled transactions. Samples are drawn by the builder from `analytics-full/` by the recipe stated under each test, and every transaction is listed with its workbook row.


## R-01: Payments to one supplier grouped under a procedure threshold [12 (High; Medium - High)]

**Audit objective.** Conclude whether payments grouped to one supplier within thirty days relate to a single requirement, and if so whether the procedure for the combined value was followed.

**C-01.1. Expected control.** Requirements are aggregated and the procurement route is chosen on the combined value, not on individual orders; the route and its progress are documented. [CPR-12, CPR-52, CPR-53, CPR-54, CPR-06, CPR-30] Owner: Relevant Service Director.

**T-01.1. Test.** For each sampled window (one per supplier, largest combined value first), obtain the orders behind the largest payments drawn (the rest of the window is listed in the flagged file), invoices and any quotes or contract. Determine whether the payments are one requirement. Pass: the payments are separate requirements, or call-offs under a contract or portal exercise that covers the combined value. [CPR-12, CPR-53, CPR-54, metric:$.tests.split_purchases.by_threshold.25000.headline_general_procurement.windows]  
**Evidence to inspect:** Purchase orders, invoices, quotation or portal records, contract or framework reference, procurement file  
**Sample:** 10 items from `split-purchases.csv`, where threshold = 25000, dominant_tag = general_procurement, largest window_total first, largest 5 payments per item, one item per supplier; 49 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P02_-_published.xlsx:2185` | 2026-05-20 | VolkerHighways Ltd | £19,420.72 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:723` | 2026-05-05 | VolkerHighways Ltd | £18,033.36 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:701` | 2026-05-12 | VolkerHighways Ltd | £17,896.87 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:2179` | 2026-05-19 | VolkerHighways Ltd | £17,882.35 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:2178` | 2026-05-05 | VolkerHighways Ltd | £16,916.01 | Environment |
| 2 | `Over500_2026_P03_-_published.xlsx:13` | 2026-06-01 | The Better Group Ltd | £24,088.98 | Children's Social Care |
| 2 | `Over500_2026_P03_-_published.xlsx:2397` | 2026-06-01 | The Better Group Ltd | £22,361.26 | Adult Social Care |
| 2 | `Over500_2026_P02_-_published.xlsx:9` | 2026-05-28 | The Better Group Ltd | £20,457.43 | Adult Social Care |
| 2 | `Over500_2026_P02_-_published.xlsx:10` | 2026-05-28 | The Better Group Ltd | £19,605.14 | Children's Social Care |
| 2 | `Over500_2026_P03_-_published.xlsx:2396` | 2026-06-01 | The Better Group Ltd | £18,039.18 | Adult Social Care |
| 3 | `Over500_2026_P03_-_published.xlsx:269` | 2026-06-12 | Newbury & District Ltd | £14,852.00 | Environment |
| 3 | `Over500_2026_P03_-_published.xlsx:268` | 2026-06-01 | Newbury & District Ltd | £13,826.61 | Environment |
| 3 | `Over500_2026_P03_-_published.xlsx:274` | 2026-06-30 | Newbury & District Ltd | £13,663.85 | Environment |
| 3 | `Over500_2026_P03_-_published.xlsx:171` | 2026-06-02 | Newbury & District Ltd | £10,529.33 | Education & SEND |
| 3 | `Over500_2026_P03_-_published.xlsx:336` | 2026-06-02 | Newbury & District Ltd | £9,861.00 | Education & SEND |
| 4 | `Over500_2026_P04_-_published.xlsx:450` | 2026-07-08 | WEAVAWAY TRAVEL LTD | £9,615.23 | Education & SEND |
| 4 | `Over500_2026_P04_-_published.xlsx:452` | 2026-07-08 | WEAVAWAY TRAVEL LTD | £9,483.38 | Education & SEND |
| 4 | `Over500_2026_P04_-_published.xlsx:183` | 2026-07-08 | WEAVAWAY TRAVEL LTD | £8,226.54 | Education & SEND |
| 4 | `Over500_2026_P04_-_published.xlsx:456` | 2026-07-24 | WEAVAWAY TRAVEL LTD | £8,097.04 | Education & SEND |
| 4 | `Over500_2026_P04_-_published.xlsx:305` | 2026-07-24 | WEAVAWAY TRAVEL LTD | £7,986.00 | Education & SEND |
| 5 | `Over500_2026_P04_-_published.xlsx:735` | 2026-07-13 | Roadside Technologies Ltd | £21,000.00 | Environment |
| 5 | `Over500_2026_P04_-_published.xlsx:733` | 2026-07-13 | Roadside Technologies Ltd | £11,188.22 | Environment |
| 5 | `Over500_2026_P04_-_published.xlsx:1287` | 2026-07-13 | Roadside Technologies Ltd | £10,298.22 | Environment |
| 5 | `Over500_2026_P04_-_published.xlsx:601` | 2026-07-13 | Roadside Technologies Ltd | £9,103.64 | Environment |
| 5 | `Over500_2026_P04_-_published.xlsx:740` | 2026-07-13 | Roadside Technologies Ltd | £9,103.64 | Environment |
| 6 | `Over500_2026_P02_-_published.xlsx:284` | 2026-05-28 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £3,120.00 | Education & SEND |
| 6 | `Over500_2026_P02_-_published.xlsx:424` | 2026-05-28 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £2,940.00 | Education & SEND |
| 6 | `Over500_2026_P02_-_published.xlsx:427` | 2026-05-28 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £2,925.00 | Education & SEND |
| 6 | `Over500_2026_P02_-_published.xlsx:265` | 2026-05-12 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £2,912.00 | Education & SEND |
| 6 | `Over500_2026_P02_-_published.xlsx:422` | 2026-05-28 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £2,910.00 | Education & SEND |
| 7 | `Over500_2026_P02_-_published.xlsx:530` | 2026-05-27 | Elior UK PLC | £23,694.03 | Adult Social Care |
| 7 | `Over500_2026_P03_-_published.xlsx:440` | 2026-06-16 | Elior UK PLC | £23,516.69 | Adult Social Care |
| 7 | `Over500_2026_P03_-_published.xlsx:433` | 2026-06-17 | Elior UK PLC | £18,592.30 | Adult Social Care |
| 7 | `Over500_2026_P03_-_published.xlsx:434` | 2026-06-11 | Elior UK PLC | £11,935.93 | Adult Social Care |
| 8 | `Over500_2026_P02_-_published.xlsx:404` | 2026-05-26 | BROADWAY CARS | £4,015.38 | Education & SEND |
| 8 | `Over500_2026_P02_-_published.xlsx:418` | 2026-05-27 | BROADWAY CARS | £3,900.00 | Education & SEND |
| 8 | `Over500_2026_P02_-_published.xlsx:412` | 2026-05-27 | BROADWAY CARS | £3,900.00 | Education & SEND |
| 8 | `Over500_2026_P02_-_published.xlsx:416` | 2026-05-27 | BROADWAY CARS | £3,900.00 | Education & SEND |
| 8 | `Over500_2026_P02_-_published.xlsx:364` | 2026-05-12 | BROADWAY CARS | £3,747.69 | Education & SEND |
| 9 | `Over500_2026_P03_-_published.xlsx:688` | 2026-06-01 | R&A Haines Building Contractors | £20,332.89 | Development & Housing |
| 9 | `Over500_2026_P03_-_published.xlsx:742` | 2026-06-30 | R&A Haines Building Contractors | £18,707.55 | Development & Housing |
| 9 | `Over500_2026_P03_-_published.xlsx:740` | 2026-06-30 | R&A Haines Building Contractors | £16,600.00 | Development & Housing |
| 9 | `Over500_2026_P03_-_published.xlsx:733` | 2026-06-01 | R&A Haines Building Contractors | £9,666.85 | Development & Housing |
| 9 | `Over500_2026_P03_-_published.xlsx:709` | 2026-06-09 | R&A Haines Building Contractors | £5,487.25 | Development & Housing |
| 10 | `Over500_2026_P03_-_published.xlsx:649` | 2026-06-18 | Triple Value Impact | £24,244.00 | Chief Executive |
| 10 | `Over500_2026_P03_-_published.xlsx:641` | 2026-06-17 | Triple Value Impact | £13,275.00 | Chief Executive |
| 10 | `Over500_2026_P03_-_published.xlsx:2393` | 2026-06-17 | Triple Value Impact | £13,110.00 | Chief Executive |
| 10 | `Over500_2026_P03_-_published.xlsx:2392` | 2026-06-17 | Triple Value Impact | £10,787.00 | Chief Executive |
| 10 | `Over500_2026_P03_-_published.xlsx:642` | 2026-06-17 | Triple Value Impact | £6,612.00 | Chief Executive |

**T-01.2. Test.** For each sampled window at the lower tier, obtain the orders behind the largest payments drawn (the rest of the window is listed in the flagged file) and invoices and confirm whether the requirement was one purchase; if so, confirm the quote and publication steps for the combined value were followed. Pass: separate requirements, or quotes and publication evidenced for the combined value. [CPR-12, CPR-52, CPR-06, metric:$.tests.split_purchases.by_threshold.5000.headline_general_procurement.windows]  
**Evidence to inspect:** Purchase orders, invoices, quotations, published invitation details  
**Sample:** 10 items from `split-purchases.csv`, where threshold = 5000, dominant_tag = general_procurement, largest window_total first, largest 5 payments per item, one item per supplier, excluding suppliers and rows already drawn in T-01.1; 40 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 3 | `Over500_2026_P04_-_published.xlsx:227` | 2026-07-22 | COMPASS EXECUTIVE CARS (UK) LTD | £4,455.00 | Education & SEND |
| 3 | `Over500_2026_P04_-_published.xlsx:478` | 2026-07-21 | COMPASS EXECUTIVE CARS (UK) LTD | £3,885.00 | Education & SEND |
| 3 | `Over500_2026_P04_-_published.xlsx:235` | 2026-07-15 | COMPASS EXECUTIVE CARS (UK) LTD | £3,654.00 | Education & SEND |
| 3 | `Over500_2026_P04_-_published.xlsx:429` | 2026-07-15 | COMPASS EXECUTIVE CARS (UK) LTD | £3,264.50 | Adult Social Care |
| 3 | `Over500_2026_P04_-_published.xlsx:288` | 2026-07-30 | COMPASS EXECUTIVE CARS (UK) LTD | £3,135.00 | Education & SEND |
| 4 | `Over500_2026_P03_-_published.xlsx:2627` | 2026-06-24 | MAISHA STAFFING SOLUTIONS LTD | £4,485.00 | Children's Social Care |
| 4 | `Over500_2026_P03_-_published.xlsx:2644` | 2026-06-19 | MAISHA STAFFING SOLUTIONS LTD | £3,895.50 | Children's Social Care |
| 4 | `Over500_2026_P02_-_published.xlsx:2085` | 2026-05-28 | MAISHA STAFFING SOLUTIONS LTD | £3,049.50 | Children's Social Care |
| 4 | `Over500_2026_P02_-_published.xlsx:2613` | 2026-05-27 | MAISHA STAFFING SOLUTIONS LTD | £2,242.50 | Children's Social Care |
| 4 | `Over500_2026_P02_-_published.xlsx:2612` | 2026-05-27 | MAISHA STAFFING SOLUTIONS LTD | £2,242.50 | Children's Social Care |
| 5 | `Over500_2026_P04_-_published.xlsx:3213` | 2026-07-31 | VolkerHighways Ltd | £4,876.74 | Environment |
| 5 | `Over500_2026_P04_-_published.xlsx:1296` | 2026-07-16 | VolkerHighways Ltd | £4,797.35 | Environment |
| 5 | `Over500_2026_P04_-_published.xlsx:602` | 2026-07-13 | VolkerHighways Ltd | £4,081.14 | Environment |
| 5 | `Over500_2026_P04_-_published.xlsx:3309` | 2026-07-17 | VolkerHighways Ltd | £3,337.15 | Environment |
| 5 | `Over500_2026_P04_-_published.xlsx:3303` | 2026-07-14 | VolkerHighways Ltd | £3,323.18 | Environment |
| 6 | `Over500_2026_P04_-_published.xlsx:220` | 2026-07-21 | Sikandar Hayat t/a Prompt Cars | £3,743.00 | Education & SEND |
| 6 | `Over500_2026_P04_-_published.xlsx:292` | 2026-07-22 | Sikandar Hayat t/a Prompt Cars | £3,307.50 | Education & SEND |
| 6 | `Over500_2026_P04_-_published.xlsx:271` | 2026-07-21 | Sikandar Hayat t/a Prompt Cars | £3,192.00 | Education & SEND |
| 6 | `Over500_2026_P04_-_published.xlsx:221` | 2026-07-21 | Sikandar Hayat t/a Prompt Cars | £3,168.00 | Education & SEND |
| 6 | `Over500_2026_P04_-_published.xlsx:435` | 2026-07-27 | Sikandar Hayat t/a Prompt Cars | £3,152.00 | Education & SEND |
| 7 | `Over500_2026_P03_-_published.xlsx:221` | 2026-06-01 | ABC TRAVEL (WOKINGHAM) LIMITED T/A ABC TRAVEL | £3,825.00 | Education & SEND |
| 7 | `Over500_2026_P03_-_published.xlsx:197` | 2026-06-01 | ABC TRAVEL (WOKINGHAM) LIMITED T/A ABC TRAVEL | £3,720.00 | Education & SEND |
| 7 | `Over500_2026_P02_-_published.xlsx:259` | 2026-05-06 | ABC TRAVEL (WOKINGHAM) LIMITED T/A ABC TRAVEL | £3,472.00 | Education & SEND |
| 7 | `Over500_2026_P02_-_published.xlsx:362` | 2026-05-11 | ABC TRAVEL (WOKINGHAM) LIMITED T/A ABC TRAVEL | £3,180.00 | Education & SEND |
| 7 | `Over500_2026_P02_-_published.xlsx:352` | 2026-05-06 | ABC TRAVEL (WOKINGHAM) LIMITED T/A ABC TRAVEL | £3,150.00 | Education & SEND |
| 8 | `Over500_2026_P03_-_published.xlsx:307` | 2026-06-30 | Glen Cleaning Company Ltd | £2,543.28 | Adult Social Care |
| 8 | `Over500_2026_P04_-_published.xlsx:127` | 2026-07-20 | Glen Cleaning Company Ltd | £2,439.00 | Adult Social Care |
| 8 | `Over500_2026_P03_-_published.xlsx:132` | 2026-06-30 | Glen Cleaning Company Ltd | £1,911.14 | Community Services |
| 8 | `Over500_2026_P04_-_published.xlsx:166` | 2026-07-24 | Glen Cleaning Company Ltd | £1,851.88 | Community Services |
| 8 | `Over500_2026_P04_-_published.xlsx:129` | 2026-07-28 | Glen Cleaning Company Ltd | £1,533.99 | Children's Social Care |
| 9 | `Over500_2026_P04_-_published.xlsx:156` | 2026-07-08 | ALMAAZ 59 LTD ( T/A SCHOOL TRAVEL) | £3,880.00 | Adult Social Care |
| 9 | `Over500_2026_P04_-_published.xlsx:440` | 2026-07-08 | ALMAAZ 59 LTD ( T/A SCHOOL TRAVEL) | £3,401.00 | Education & SEND |
| 9 | `Over500_2026_P04_-_published.xlsx:231` | 2026-07-08 | ALMAAZ 59 LTD ( T/A SCHOOL TRAVEL) | £3,054.50 | Education & SEND |
| 9 | `Over500_2026_P04_-_published.xlsx:442` | 2026-07-08 | ALMAAZ 59 LTD ( T/A SCHOOL TRAVEL) | £2,660.00 | Education & SEND |
| 9 | `Over500_2026_P04_-_published.xlsx:464` | 2026-07-08 | ALMAAZ 59 LTD ( T/A SCHOOL TRAVEL) | £2,641.00 | Education & SEND |
| 10 | `Over500_2026_P04_-_published.xlsx:246` | 2026-07-08 | WEAVAWAY TRAVEL LTD | £4,549.40 | Education & SEND |
| 10 | `Over500_2026_P04_-_published.xlsx:250` | 2026-07-24 | WEAVAWAY TRAVEL LTD | £3,831.07 | Education & SEND |
| 10 | `Over500_2026_P04_-_published.xlsx:309` | 2026-07-08 | WEAVAWAY TRAVEL LTD | £2,974.60 | Education & SEND |
| 10 | `Over500_2026_P04_-_published.xlsx:198` | 2026-07-24 | WEAVAWAY TRAVEL LTD | £2,504.93 | Education & SEND |
| 10 | `Over500_2026_P04_-_published.xlsx:459` | 2026-07-08 | WEAVAWAY TRAVEL LTD | £2,312.52 | Education & SEND |


## R-02: Single payments sitting just below a quote or tender threshold [12 (High; Medium - High)]

**Audit objective.** Conclude whether payments just below a quote or tender threshold are complete requirements procured with the quotes their value needs.

**C-02.1. Expected control.** Quotes are sought for each purchase at the level its full requirement value sets in Appendix B, and orders are not set to fall under a band. [CPR-52, CPR-53, CPR-54, CPR-06, CPR-12] Owner: Relevant Service Director.

**T-02.1. Test.** For each payment in the band just below the publication tier, obtain the order, invoice and quotes. Confirm the payment is a complete requirement and compare the quotes held with what the full requirement value needs. Pass: complete requirement with the quotes its value needs, or part of a larger order covered by a portal exercise. Also pass: the payment is made under an approved inter-authority or shared-service agreement, with the agreement and its approval inspected. [CPR-53, CPR-52, metric:$.tests.threshold_clustering.by_threshold.25000.by_tag.general_procurement.rows]  
**Evidence to inspect:** Purchase order, invoice, quotations, requirement specification, inter-authority or shared-service agreement and approval where the payee is a public body  
**Sample:** 10 items from `threshold-clustering.csv`, where threshold = 25000, tag = general_procurement, largest Net amount first; 10 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P04_-_published.xlsx:1281` | 2026-07-29 | The Better Group Ltd | £24,476.02 | Adult Social Care |
| 2 | `Over500_2026_P02_-_published.xlsx:2201` | 2026-05-15 | WOKINGHAM BOROUGH COUNCIL | £24,416.73 | Finance, Property & Procurement |
| 3 | `Over500_2026_P03_-_published.xlsx:649` | 2026-06-18 | Triple Value Impact | £24,244.00 | Chief Executive |
| 4 | `Over500_2026_P02_-_published.xlsx:560` | 2026-05-12 | DevComms South East Ltd | £24,227.07 | Development & Housing |
| 5 | `Over500_2026_P03_-_published.xlsx:13` | 2026-06-01 | The Better Group Ltd | £24,088.98 | Children's Social Care |
| 6 | `Over500_2026_P03_-_published.xlsx:396` | 2026-06-10 | BookingLab Limited | £24,000.00 | Transformation, Customer & ICT |
| 7 | `Over500_2026_P02_-_published.xlsx:530` | 2026-05-27 | Elior UK PLC | £23,694.03 | Adult Social Care |
| 8 | `Over500_2026_P03_-_published.xlsx:683` | 2026-06-08 | VolkerHighways Ltd | £23,591.22 | Environment |
| 9 | `Over500_2026_P03_-_published.xlsx:440` | 2026-06-16 | Elior UK PLC | £23,516.69 | Adult Social Care |
| 10 | `Over500_2026_P04_-_published.xlsx:533` | 2026-07-28 | Elior UK PLC | £23,173.08 | Adult Social Care |

**T-02.2. Test.** For each payment in the band just below the tender-publication figure (one per supplier, largest first), obtain the order, invoice and quote. Pass: the payment is the complete requirement and a quote is on file; or, where it is part of a larger requirement above the tender-publication figure, publication of the invitation is evidenced. Otherwise fail. [CPR-52, CPR-06, metric:$.tests.threshold_clustering.by_threshold.5000.by_tag.general_procurement.rows]  
**Evidence to inspect:** Purchase order, invoice, quotation  
**Sample:** 10 items from `threshold-clustering.csv`, where threshold = 5000, tag = general_procurement, largest Net amount first, one item per supplier_norm, excluding suppliers and rows already drawn in T-02.1; 10 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P03_-_published.xlsx:652` | 2026-06-02 | Zurich | £5,000.00 | Finance, Property & Procurement |
| 2 | `Over500_2026_P04_-_published.xlsx:633` | 2026-07-31 | GREENHAM TRUST LTD | £5,000.00 | Community Services |
| 3 | `Over500_2026_P02_-_published.xlsx:465` | 2026-05-29 | CIVICA  UK LTD | £4,995.00 | Development & Housing |
| 4 | `Over500_2026_P04_-_published.xlsx:551` | 2026-07-01 | Helen Redding Education Consultancy Ltd | £4,987.50 | Education & SEND |
| 5 | `Over500_2026_P04_-_published.xlsx:1302` | 2026-07-22 | SCBS LTD | £4,979.43 | Development & Housing |
| 6 | `Over500_2026_P04_-_published.xlsx:713` | 2026-07-29 | RH Environmental Limited | £4,975.00 | Community Services |
| 7 | `Over500_2026_P03_-_published.xlsx:719` | 2026-06-30 | ADF ENVIRONMENTAL LTD | £4,950.00 | Development & Housing |
| 8 | `Over500_2026_P03_-_published.xlsx:698` | 2026-06-03 | WSP UK  LTD | £4,934.60 | Environment |
| 9 | `Over500_2026_P03_-_published.xlsx:459` | 2026-06-25 | LOCAL GOVERNMENT PROPERTY CONSULTANTS (LGPC) | £4,925.00 | Finance, Property & Procurement |
| 10 | `Over500_2026_P04_-_published.xlsx:234` | 2026-07-15 | Mark Dillon t/a Penmar Transport Ltd | £4,920.00 | Education & SEND |


## R-03: High-value suppliers with no matching published contract notice [12 (High; Medium - High)]

**Audit objective.** Conclude whether spend with the largest general-procurement suppliers above the publication tier is covered by a contract recorded on the council's register, a compliant framework call-off or an approved exception.

**C-03.1. Expected control.** Every contract at or above the publication tier is let through a portal exercise with a contract notice approved for issue, and recorded on the published contract register; framework use is confirmed before call-off. [CPR-53, CPR-07, CPR-33, CPR-11, CPR-10, CPR-27] Owner: Service Lead for Procurement and Commissioning.

**T-03.1. Test.** Check the near-match list first. For each sampled supplier with no matching notice, match it to the council's contract register and obtain the contract, framework call-off (with the advice confirming entitlement) or approved exception covering the payments drawn. Pass: a contract, call-off or exception covers the spend and the contract is on the register. Also pass: the payment is made under an approved inter-authority or shared-service agreement, with the agreement and its approval inspected. [CPR-07, CPR-33, CPR-53, CPR-27, metric:$.tests.off_contract.unmatched_by_tag.general_procurement.suppliers]  
**Evidence to inspect:** Contract register extract, contract or call-off documents, framework advice, CDP notice, exception approval, inter-authority or shared-service agreement and approval where the payee is a public body  
**Sample:** 10 items from `high-value-suppliers.csv`, where match_class = none, dominant_tag = general_procurement, annualised_estimate ≥ 25000, largest annualised_estimate first, 3 payments per supplier; 28 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P04_-_published.xlsx:793` | 2026-07-13 | VolkerHighways Ltd | £998,987.64 | Environment |
| 1 | `Over500_2026_P04_-_published.xlsx:603` | 2026-07-28 | VolkerHighways Ltd | £855,750.25 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:684` | 2026-06-22 | VolkerHighways Ltd | £366,872.38 | Environment |
| 2 | `Over500_2026_P02_-_published.xlsx:2196` | 2026-05-27 | VEOLIA ES WEST BERKSHIRE LTD (CHAPS ONLY) | £2,201,856.40 | Environment |
| 2 | `Over500_2026_P03_-_published.xlsx:2146` | 2026-06-29 | VEOLIA ES WEST BERKSHIRE LTD (CHAPS ONLY) | £2,180,425.32 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:3194` | 2026-07-27 | VEOLIA ES WEST BERKSHIRE LTD (CHAPS ONLY) | £1,803,783.32 | Environment |
| 3 | `Over500_2026_P03_-_published.xlsx:2144` | 2026-06-25 | Millbrook Healthcare Limited | £1,141,918.00 | Finance, Property & Procurement |
| 3 | `Over500_2026_P03_-_published.xlsx:2216` | 2026-06-03 | Millbrook Healthcare Limited | £1,141,918.00 | Finance, Property & Procurement |
| 3 | `Over500_2026_P04_-_published.xlsx:3789` | 2026-07-29 | Millbrook Healthcare Limited | £1,141,918.00 | Finance, Property & Procurement |
| 4 | `Over500_2026_P02_-_published.xlsx:665` | 2026-05-15 | The Better Group Ltd | £64,500.00 | Adult Social Care |
| 4 | `Over500_2026_P02_-_published.xlsx:666` | 2026-05-15 | The Better Group Ltd | £58,833.00 | Adult Social Care |
| 4 | `Over500_2026_P03_-_published.xlsx:670` | 2026-06-01 | The Better Group Ltd | £48,784.37 | Adult Social Care |
| 5 | `Over500_2026_P02_-_published.xlsx:473` | 2026-05-27 | SoftwareONE UK Ltd | £375,697.68 | Transformation, Customer & ICT |
| 5 | `Over500_2026_P02_-_published.xlsx:474` | 2026-05-27 | SoftwareONE UK Ltd | £85,871.04 | Transformation, Customer & ICT |
| 5 | `Over500_2026_P02_-_published.xlsx:653` | 2026-05-27 | SoftwareONE UK Ltd | £59,650.56 | Transformation, Customer & ICT |
| 6 | `Over500_2026_P02_-_published.xlsx:2200` | 2026-05-13 | Livity Life Ltd | £135,591.03 | Finance, Property & Procurement |
| 6 | `Over500_2026_P03_-_published.xlsx:3087` | 2026-06-17 | Livity Life Ltd | £127,886.78 | Finance, Property & Procurement |
| 6 | `Over500_2026_P04_-_published.xlsx:3310` | 2026-07-13 | Livity Life Ltd | £50,961.45 | Finance, Property & Procurement |
| 7 | `Over500_2026_P04_-_published.xlsx:784` | 2026-07-10 | E W BEARD LTD | £64,202.50 | Education & SEND |
| 7 | `Over500_2026_P02_-_published.xlsx:674` | 2026-05-20 | E W BEARD LTD | £60,039.70 | Education & SEND |
| 7 | `Over500_2026_P02_-_published.xlsx:675` | 2026-05-20 | E W BEARD LTD | £55,594.00 | Education & SEND |
| 8 | `Over500_2026_P02_-_published.xlsx:2198` | 2026-05-13 | SLOUGH BOROUGH COUNCIL | £296,177.15 | Finance, Property & Procurement |
| 9 | `Over500_2026_P03_-_published.xlsx:183` | 2026-06-03 | Sikandar Hayat t/a Prompt Cars | £73,296.50 | Education & SEND |
| 9 | `Over500_2026_P03_-_published.xlsx:203` | 2026-06-03 | Sikandar Hayat t/a Prompt Cars | £26,085.00 | Education & SEND |
| 9 | `Over500_2026_P03_-_published.xlsx:208` | 2026-06-03 | Sikandar Hayat t/a Prompt Cars | £17,607.50 | Education & SEND |
| 10 | `Over500_2026_P02_-_published.xlsx:530` | 2026-05-27 | Elior UK PLC | £23,694.03 | Adult Social Care |
| 10 | `Over500_2026_P03_-_published.xlsx:440` | 2026-06-16 | Elior UK PLC | £23,516.69 | Adult Social Care |
| 10 | `Over500_2026_P04_-_published.xlsx:533` | 2026-07-28 | Elior UK PLC | £23,173.08 | Adult Social Care |


## R-04: Payments continuing after a published contract notice ended [9 (High; Medium - High)]

**Audit objective.** Conclude whether payments made after a published notice ended are covered by a newer contract or an approved extension.

**C-04.1. Expected control.** A contract is extended only under its extension provision and with S151 Officer approval before payments continue beyond its end date. [CPR-60, CPR-33] Owner: S151 Officer.

**T-04.1. Test.** For each flagged supplier, obtain the current contract or the extension and the S151 approval, and compare their dates with the payment dates drawn. Pass: a newer contract or an approved extension covers every payment date. [CPR-60, metric:$.tests.expired_notice_spend.by_dominant_tag.general_procurement]  
**Evidence to inspect:** Current contract or extension letter, S151 approval, contract register entry  
**Sample:** 8 items from `expired-notice-spend.csv`, where dominant_tag = general_procurement, largest total_gbp first, 3 payments per supplier, (only 8 available); 13 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P03_-_published.xlsx:704` | 2026-06-16 | Hope & Clay (Construction) Ltd | £91,306.75 | Environment |
| 2 | `Over500_2026_P03_-_published.xlsx:58` | 2026-06-03 | BERKSHIRE MECHANICAL SERVICES | £8,250.00 | Development & Housing |
| 2 | `Over500_2026_P03_-_published.xlsx:42` | 2026-06-03 | BERKSHIRE MECHANICAL SERVICES | £6,250.00 | Development & Housing |
| 2 | `Over500_2026_P03_-_published.xlsx:279` | 2026-06-09 | BERKSHIRE MECHANICAL SERVICES | £5,585.00 | Development & Housing |
| 3 | `Over500_2026_P04_-_published.xlsx:856` | 2026-07-14 | Berkshire Womens Aid | £39,569.75 | Public Health & Wellbeing |
| 3 | `Over500_2026_P04_-_published.xlsx:721` | 2026-07-14 | Berkshire Womens Aid | £13,427.75 | Public Health & Wellbeing |
| 4 | `Over500_2026_P02_-_published.xlsx:467` | 2026-05-08 | G7 BUSINESS SOLUTIONS LIMITED | £5,469.78 | Finance, Property & Procurement |
| 4 | `Over500_2026_P03_-_published.xlsx:531` | 2026-06-10 | G7 BUSINESS SOLUTIONS LIMITED | £5,469.78 | Finance, Property & Procurement |
| 4 | `Over500_2026_P03_-_published.xlsx:721` | 2026-06-10 | G7 BUSINESS SOLUTIONS LIMITED | £1,365.00 | Finance, Property & Procurement |
| 5 | `Over500_2026_P02_-_published.xlsx:459` | 2026-05-15 | CACI Limited | £12,071.67 | Children's Social Care |
| 6 | `Over500_2026_P03_-_published.xlsx:686` | 2026-06-22 | Morton Pattison Ltd | £1,102.00 | Environment |
| 7 | `Over500_2026_P03_-_published.xlsx:821` | 2026-06-03 | Davis and Associates Consultancy Limited | £800.00 | Chief Executive |
| 8 | `Over500_2026_P04_-_published.xlsx:58` | 2026-07-20 | Tactical Facilities Management Ltd | £681.94 | Development & Housing |


## R-05: Spend running above the published award value [9 (High; Medium - High)]

**Audit objective.** Conclude whether spend above the published award's annual rate is covered by an approved variation or explained by the award terms.

**C-05.1. Expected control.** Variations to a contract are approved in advance by the Monitoring Officer and S151 Officer, or by the relevant board above the Threshold, before spend exceeds the award. [CPR-61, CPR-62] Owner: Monitoring Officer and S151 Officer; relevant board above the Threshold.

**T-05.1. Test.** For every flagged supplier (largest annualised estimate first), obtain the award, any variations and their approvals, and compare the approved value with spend to date. Pass: the award is a maximum or estimate that covers spend, or an approved variation does. [CPR-61, CPR-62, metric:$.tests.spend_vs_award.suppliers_flagged]  
**Evidence to inspect:** Award notice and contract, variation documents, Monitoring Officer, S151 or board approvals, spend to date  
**Sample:** 12 items from `spend-vs-award.csv`, where ratio ≥ 1.25, largest annualised_estimate first, 3 payments per supplier; 28 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P02_-_published.xlsx:437` | 2026-05-20 | Newbury & District Ltd | £60,797.19 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:267` | 2026-06-01 | Newbury & District Ltd | £59,626.76 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:270` | 2026-06-30 | Newbury & District Ltd | £59,007.20 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:905` | 2026-07-22 | NEC SOFTWARE SOLUTIONS UK LIMITED | £129,125.00 | Finance, Property & Procurement |
| 2 | `Over500_2026_P04_-_published.xlsx:492` | 2026-07-22 | NEC SOFTWARE SOLUTIONS UK LIMITED | £91,629.15 | Finance, Property & Procurement |
| 2 | `Over500_2026_P04_-_published.xlsx:487` | 2026-07-22 | NEC SOFTWARE SOLUTIONS UK LIMITED | £52,054.00 | Finance, Property & Procurement |
| 3 | `Over500_2026_P03_-_published.xlsx:2130` | 2026-06-09 | TWO SAINTS LTD | £38,775.00 | Development & Housing |
| 3 | `Over500_2026_P04_-_published.xlsx:3181` | 2026-07-22 | TWO SAINTS LTD | £38,775.00 | Development & Housing |
| 3 | `Over500_2026_P02_-_published.xlsx:2160` | 2026-05-12 | TWO SAINTS LTD | £27,147.69 | Development & Housing |
| 4 | `Over500_2026_P04_-_published.xlsx:321` | 2026-07-14 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £4,074.00 | Education & SEND |
| 4 | `Over500_2026_P04_-_published.xlsx:266` | 2026-07-14 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £4,018.00 | Education & SEND |
| 4 | `Over500_2026_P04_-_published.xlsx:467` | 2026-07-09 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £4,018.00 | Education & SEND |
| 5 | `Over500_2026_P04_-_published.xlsx:1276` | 2026-07-22 | WCL UK Ltd (Trading as Everything ICT) | £102,882.78 | Education & SEND |
| 6 | `Over500_2026_P03_-_published.xlsx:371` | 2026-06-08 | IDOX SOFTWARE LTD | £48,579.20 | Community Services |
| 6 | `Over500_2026_P02_-_published.xlsx:462` | 2026-05-20 | IDOX SOFTWARE LTD | £2,647.21 | Development & Housing |
| 7 | `Over500_2026_P04_-_published.xlsx:207` | 2026-07-22 | ACE WHEELCHAIR TRAVEL | £4,840.00 | Education & SEND |
| 7 | `Over500_2026_P04_-_published.xlsx:328` | 2026-07-29 | ACE WHEELCHAIR TRAVEL | £3,916.00 | Education & SEND |
| 7 | `Over500_2026_P04_-_published.xlsx:445` | 2026-07-22 | ACE WHEELCHAIR TRAVEL | £3,520.00 | Education & SEND |
| 8 | `Over500_2026_P03_-_published.xlsx:396` | 2026-06-10 | BookingLab Limited | £24,000.00 | Transformation, Customer & ICT |
| 9 | `Over500_2026_P04_-_published.xlsx:313` | 2026-07-08 | Valley Cars | £3,173.00 | Education & SEND |
| 9 | `Over500_2026_P03_-_published.xlsx:222` | 2026-06-02 | Valley Cars | £2,505.00 | Education & SEND |
| 9 | `Over500_2026_P02_-_published.xlsx:354` | 2026-05-06 | Valley Cars | £2,338.00 | Education & SEND |
| 10 | `Over500_2026_P03_-_published.xlsx:384` | 2026-06-04 | Exacom Systems Ltd | £12,105.85 | Development & Housing |
| 11 | `Over500_2026_P02_-_published.xlsx:460` | 2026-05-20 | Softcat Ltd | £8,979.02 | Education & SEND |
| 11 | `Over500_2026_P03_-_published.xlsx:375` | 2026-06-17 | Softcat Ltd | £2,025.98 | Transformation, Customer & ICT |
| 12 | `Over500_2026_P03_-_published.xlsx:276` | 2026-06-30 | SMS-Environmental Ltd | £2,070.00 | Adult Social Care |
| 12 | `Over500_2026_P04_-_published.xlsx:365` | 2026-07-09 | SMS-Environmental Ltd | £1,335.60 | Adult Social Care |
| 12 | `Over500_2026_P03_-_published.xlsx:29` | 2026-06-22 | SMS-Environmental Ltd | £1,175.00 | Adult Social Care |


## R-06: Repeated payments of the same amount to the same supplier [9 (High; Medium - High)]

**Audit objective.** Conclude whether repeated payments of the same amount to the same supplier within seven days are each backed by a separate supply.

**C-06.1. Expected control.** Each payment is backed by written evidence of a distinct purchase (order and invoice), so a repeat of the same invoice is stopped before payment or recovered. [CPR-31]

**T-06.1. Test.** The sample unit is the repeat group: one payment is drawn per group, largest amount first. For each, obtain its invoice and order and those of every other payment in its group (listed under the same group in the flagged file). Pass: distinct invoices for distinct supplies; otherwise record the recovery or credit note. [CPR-31, metric:$.tests.duplicates.different_time.by_tag.general_procurement.groups]  
**Evidence to inspect:** Invoices, purchase orders, credit notes or recovery records  
**Sample:** 10 items from `duplicates.csv`, where tier = different_time, tag = general_procurement, largest Net amount first, one item per group; 10 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P04_-_published.xlsx:3308` | 2026-07-15 | VolkerHighways Ltd | £101,925.86 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:3210` | 2026-07-13 | VolkerHighways Ltd | £54,241.36 | Environment |
| 3 | `Over500_2026_P02_-_published.xlsx:2160` | 2026-05-12 | TWO SAINTS LTD | £27,147.69 | Development & Housing |
| 4 | `Over500_2026_P04_-_published.xlsx:3184` | 2026-07-13 | VolkerHighways Ltd | £17,882.35 | Environment |
| 5 | `Over500_2026_P02_-_published.xlsx:8` | 2026-05-13 | Pavillion Publishing and Media Ltd | £9,084.60 | Adult Social Care |
| 6 | `Over500_2026_P04_-_published.xlsx:598` | 2026-07-13 | Roadside Technologies Ltd | £5,594.11 | Environment |
| 7 | `Over500_2026_P04_-_published.xlsx:259` | 2026-07-13 | BROADWAY CARS | £5,330.00 | Education & SEND |
| 8 | `Over500_2026_P03_-_published.xlsx:459` | 2026-06-25 | LOCAL GOVERNMENT PROPERTY CONSULTANTS (LGPC) | £4,925.00 | Finance, Property & Procurement |
| 9 | `Over500_2026_P03_-_published.xlsx:431` | 2026-06-17 | BRITISH TELECOM | £4,364.06 | Transformation, Customer & ICT |
| 10 | `Over500_2026_P04_-_published.xlsx:467` | 2026-07-09 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £4,018.00 | Education & SEND |

**T-06.2. Test.** The sample unit is the repeat group: one payment is drawn per same-run group, largest amount first. For each, obtain the invoices behind every payment in its group (listed under the same group in the flagged file). Pass: distinct invoices for distinct supplies; otherwise record the recovery or credit note. [CPR-31, metric:$.tests.duplicates.same_timestamp.by_tag.general_procurement.groups]  
**Evidence to inspect:** Invoices, purchase orders, payment run records  
**Sample:** 10 items from `duplicates.csv`, where tier = same_timestamp, tag = general_procurement, largest Net amount first, one item per group; 10 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P04_-_published.xlsx:601` | 2026-07-13 | Roadside Technologies Ltd | £9,103.64 | Environment |
| 2 | `Over500_2026_P03_-_published.xlsx:2134` | 2026-06-18 | SEISMIC SEWAGE SYSTEMS LTD | £5,360.00 | Environment |
| 3 | `Over500_2026_P04_-_published.xlsx:3663` | 2026-07-29 | MAISHA STAFFING SOLUTIONS LTD | £3,737.50 | Children's Social Care |
| 4 | `Over500_2026_P02_-_published.xlsx:2612` | 2026-05-27 | MAISHA STAFFING SOLUTIONS LTD | £2,242.50 | Children's Social Care |
| 5 | `Over500_2026_P03_-_published.xlsx:2628` | 2026-06-25 | MAISHA STAFFING SOLUTIONS LTD | £2,242.50 | Children's Social Care |
| 6 | `Over500_2026_P04_-_published.xlsx:162` | 2026-07-21 | COMPASS EXECUTIVE CARS (UK) LTD | £2,178.00 | Education & SEND |
| 7 | `Over500_2026_P03_-_published.xlsx:165` | 2026-06-30 | DANIEL GRIFFITHS T/A BLUEBIRD PASSENGER SERVICES | £2,050.00 | Education & SEND |
| 8 | `Over500_2026_P03_-_published.xlsx:716` | 2026-06-25 | AMR CONSULT LTD | £2,046.67 | Education & SEND |
| 9 | `Over500_2026_P04_-_published.xlsx:160` | 2026-07-14 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £1,886.00 | Education & SEND |
| 10 | `Over500_2026_P03_-_published.xlsx:324` | 2026-06-02 | DANIEL GRIFFITHS T/A BLUEBIRD PASSENGER SERVICES | £1,500.00 | Education & SEND |


## R-07: Waivers and exceptions to competition not approved or recorded [4 (Moderate; Moderate)]

**Audit objective.** Conclude whether waivers, exceptions and exclusions from competition are sought in advance, approved at the level the Rules set and fully recorded.

**C-07.1. Expected control.** Each waiver or exception is limited to the permitted circumstances, sought in advance, approved by the Monitoring Officer and/or S151 Officer at the level its value sets, reported to the relevant board and fully documented. [CPR-19, CPR-20, CPR-21, CPR-22, CPR-23, CPR-24, CPR-25, CPR-26] Owner: Monitoring Officer and/or S151 Officer.

**T-07.1. Test.** Obtain the waiver and exception register for the spend window. Select five entries, largest value first, and confirm for each the circumstance relied on, the advance approval at the right level, the board report and the S151 record. Pass: every element present and dated before award. [CPR-19, CPR-20, CPR-22, CPR-24, CPR-26]  
**Evidence to inspect:** Waiver and exception register, exception reports, approvals, board minutes  
**Sample:** document test: five register entries, largest value first, selected at fieldwork

**C-07.2. Expected control.** A contract let under an exclusion from the Procurement Legislation has prior written Monitoring Officer approval, and relevant board approval where its value exceeds the Threshold. [CPR-57, CPR-64] Owner: Monitoring Officer; relevant board.

**T-07.2. Test.** Obtain the record of contracts let under an exclusion in the spend window (excluding placements, which are out of scope). Select five, largest value first, and confirm the prior Monitoring Officer approval and, above the Threshold, board approval. Pass: approvals present and dated before award. [CPR-57, CPR-64]  
**Evidence to inspect:** Exclusion record, Monitoring Officer approvals, board minutes  
**Sample:** document test: five exclusion records, largest value first, selected at fieldwork


## R-08: Award approval and Key Decisions for the largest contracts [12 (High; Medium - High)]

**Audit objective.** Conclude whether the largest purchases carry the award decision, Key Decision and contract documentation their value requires.

**C-08.1. Expected control.** Each award rests on a decision by the approver Appendix A sets for its total value, including a Key Decision above £500,000 and Executive approval in the highest band. [CPR-02, CPR-04, CPR-05, CPR-48, CPR-49, CPR-50, CPR-51, CPR-55] Owner: Relevant Service Director; Portfolio Holder; the Executive.

**T-08.1. Test.** For each general-procurement window above the Key Decision level, identify the contract the payments fall under and obtain its award decision. Confirm the approver and the Key Decision record match Appendix A for the contract's total value. Pass: decision by the right approver, dated before award. Where the contract is for works, a concession or light-touch services, also obtain the Portal record of the five written tenders sought and the advert. [CPR-04, CPR-50, metric:$.tests.split_purchases.by_threshold.500000.headline_general_procurement.windows, CPR-55]  
**Evidence to inspect:** Award decision, Key Decision record, board report, Forward Plan entry, Portal tender record and advert for works, concession or light-touch contracts  
**Sample:** 2 items from `split-purchases.csv`, where threshold = 500000, dominant_tag = general_procurement, largest window_total first, largest 10 payments per item, (only 2 available); 14 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P03_-_published.xlsx:699` | 2026-06-08 | VolkerHighways Ltd | £329,988.88 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:701` | 2026-06-09 | VolkerHighways Ltd | £307,338.45 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:729` | 2026-06-08 | VolkerHighways Ltd | £299,416.56 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:711` | 2026-05-26 | VolkerHighways Ltd | £200,305.25 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:702` | 2026-05-13 | VolkerHighways Ltd | £195,844.36 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:692` | 2026-05-13 | VolkerHighways Ltd | £185,970.32 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:705` | 2026-05-20 | VolkerHighways Ltd | £157,038.29 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:706` | 2026-05-27 | VolkerHighways Ltd | £149,153.26 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:710` | 2026-05-12 | VolkerHighways Ltd | £119,381.40 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:2184` | 2026-05-19 | VolkerHighways Ltd | £101,925.86 | Environment |
| 2 | `Over500_2026_P02_-_published.xlsx:473` | 2026-05-27 | SoftwareONE UK Ltd | £375,697.68 | Transformation, Customer & ICT |
| 2 | `Over500_2026_P02_-_published.xlsx:474` | 2026-05-27 | SoftwareONE UK Ltd | £85,871.04 | Transformation, Customer & ICT |
| 2 | `Over500_2026_P02_-_published.xlsx:653` | 2026-05-27 | SoftwareONE UK Ltd | £59,650.56 | Transformation, Customer & ICT |
| 2 | `Over500_2026_P02_-_published.xlsx:654` | 2026-05-27 | SoftwareONE UK Ltd | £1,759.34 | Transformation, Customer & ICT |

**T-08.2. Test.** For each of the largest general-procurement suppliers by annualised estimate, identify the contract and obtain its award decision. Confirm the approver matches Appendix A for the contract's total value. Pass: decision by the right approver, dated before award. Also pass: the payment is made under an approved inter-authority or shared-service agreement, with the agreement and its approval inspected. [CPR-02, CPR-49, CPR-51, metric:$.tests.high_value_suppliers.tiers.publication_threshold.headline_general_procurement_suppliers]  
**Evidence to inspect:** Award decision, delegation record, board report, inter-authority or shared-service agreement and approval where the payee is a public body  
**Sample:** 10 items from `high-value-suppliers.csv`, where dominant_tag = general_procurement, annualised_estimate ≥ 25000, largest annualised_estimate first, 2 payments per supplier, excluding suppliers and rows already drawn in T-08.1; 18 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P02_-_published.xlsx:2196` | 2026-05-27 | VEOLIA ES WEST BERKSHIRE LTD (CHAPS ONLY) | £2,201,856.40 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:2146` | 2026-06-29 | VEOLIA ES WEST BERKSHIRE LTD (CHAPS ONLY) | £2,180,425.32 | Environment |
| 2 | `Over500_2026_P03_-_published.xlsx:2144` | 2026-06-25 | Millbrook Healthcare Limited | £1,141,918.00 | Finance, Property & Procurement |
| 2 | `Over500_2026_P03_-_published.xlsx:2216` | 2026-06-03 | Millbrook Healthcare Limited | £1,141,918.00 | Finance, Property & Procurement |
| 3 | `Over500_2026_P02_-_published.xlsx:665` | 2026-05-15 | The Better Group Ltd | £64,500.00 | Adult Social Care |
| 3 | `Over500_2026_P02_-_published.xlsx:666` | 2026-05-15 | The Better Group Ltd | £58,833.00 | Adult Social Care |
| 4 | `Over500_2026_P02_-_published.xlsx:2200` | 2026-05-13 | Livity Life Ltd | £135,591.03 | Finance, Property & Procurement |
| 4 | `Over500_2026_P03_-_published.xlsx:3087` | 2026-06-17 | Livity Life Ltd | £127,886.78 | Finance, Property & Procurement |
| 5 | `Over500_2026_P02_-_published.xlsx:437` | 2026-05-20 | Newbury & District Ltd | £60,797.19 | Environment |
| 5 | `Over500_2026_P03_-_published.xlsx:267` | 2026-06-01 | Newbury & District Ltd | £59,626.76 | Environment |
| 6 | `Over500_2026_P04_-_published.xlsx:784` | 2026-07-10 | E W BEARD LTD | £64,202.50 | Education & SEND |
| 6 | `Over500_2026_P02_-_published.xlsx:674` | 2026-05-20 | E W BEARD LTD | £60,039.70 | Education & SEND |
| 7 | `Over500_2026_P02_-_published.xlsx:669` | 2026-05-26 | ASCIA CONSTRUCTION LIMITED | £332,579.29 | Education & SEND |
| 8 | `Over500_2026_P04_-_published.xlsx:905` | 2026-07-22 | NEC SOFTWARE SOLUTIONS UK LIMITED | £129,125.00 | Finance, Property & Procurement |
| 8 | `Over500_2026_P04_-_published.xlsx:492` | 2026-07-22 | NEC SOFTWARE SOLUTIONS UK LIMITED | £91,629.15 | Finance, Property & Procurement |
| 9 | `Over500_2026_P02_-_published.xlsx:2198` | 2026-05-13 | SLOUGH BOROUGH COUNCIL | £296,177.15 | Finance, Property & Procurement |
| 10 | `Over500_2026_P03_-_published.xlsx:2130` | 2026-06-09 | TWO SAINTS LTD | £38,775.00 | Development & Housing |
| 10 | `Over500_2026_P04_-_published.xlsx:3181` | 2026-07-22 | TWO SAINTS LTD | £38,775.00 | Development & Housing |

**C-08.2. Expected control.** Contracts above the Threshold have a written procurement report kept for three years, a written contract in an approved form, and are sealed. [CPR-28, CPR-29, CPR-32, CPR-47] Owner: Relevant Service Director; Monitoring Officer.

**T-08.3. Test.** Before fieldwork, record the Threshold figure the auditor confirms for each contract type. Apply this test to every contract identified in T-08.1 and T-08.2: for each one whose value exceeds that Threshold, obtain the procurement report, the signed contract and the sealing record. Pass: report held, contract in approved form, contract sealed. Contracts below the confirmed Threshold are recorded as not applicable, with the figure used. [CPR-28, CPR-32, CPR-47]  
**Evidence to inspect:** Procurement report, signed contract, sealing register  
**Sample:** performed on the contracts identified in T-08.1 and T-08.2; no further transactions drawn


## R-11: Agency staff bought without a competed contract [8 (High; Medium - High)]

**Audit objective.** Conclude whether agency staff above the publication tier are bought under a competed contract or a compliant framework call-off with the approvals its value requires.

**C-11.1. Expected control.** Agency staff are bought under a competed contract or a framework whose use was confirmed in advance, with Monitoring Officer approval for any direct call-off and award approval at the Appendix A level. Agency requirements are not split to avoid the Rules. [CPR-27, CPR-59, CPR-53, CPR-50, CPR-51, CPR-12, CPR-04] Owner: Monitoring Officer; relevant Service Director.

**T-11.1. Test.** For each agency staff supplier above the publication tier, obtain the contract or framework call-off, the framework advice, the Monitoring Officer approval for any direct award and the award approval, and compare them with the payments drawn. Pass: a competed route and approvals cover the spend. In addition, review the unmatched general-procurement top 20 for staffing or agency suppliers and apply this test to up to two of them, largest annualised estimate first. [CPR-59, CPR-27, metric:$.tests.off_contract.unmatched_by_tag.agency_staff.suppliers, metric:$.tests.off_contract.unmatched_by_tag.general_procurement.suppliers]  
**Evidence to inspect:** Contract or framework call-off, framework advice, Monitoring Officer approval, award decision  
**Sample:** 1 item from `high-value-suppliers.csv`, where dominant_tag = agency_staff, annualised_estimate ≥ 25000, largest annualised_estimate first, 5 payments per supplier, (only 1 available); 5 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P03_-_published.xlsx:9` | 2026-06-15 | Comensura Ltd | £107,880.99 | Strategy & Governance |
| 1 | `Over500_2026_P02_-_published.xlsx:5` | 2026-05-12 | Comensura Ltd | £104,728.31 | Strategy & Governance |
| 1 | `Over500_2026_P04_-_published.xlsx:19` | 2026-07-31 | Comensura Ltd | £103,047.79 | Strategy & Governance |
| 1 | `Over500_2026_P03_-_published.xlsx:12` | 2026-06-08 | Comensura Ltd | £101,567.70 | Strategy & Governance |
| 1 | `Over500_2026_P04_-_published.xlsx:6` | 2026-07-15 | Comensura Ltd | £100,668.47 | Strategy & Governance |

**T-11.2. Test.** For the agency staff window above the Key Decision level, identify the contract or call-off the payments fall under and obtain the Key Decision record and award approval for its total value. Confirm the payments were not split from one requirement. Pass: Key Decision and approval at the Appendix A level cover the combined value. [CPR-04, CPR-12, metric:$.tests.split_purchases.by_threshold.500000.by_tag.agency_staff.windows]  
**Evidence to inspect:** Key Decision record, award decision, contract or call-off  
**Sample:** 1 item from `split-purchases.csv`, where threshold = 500000, dominant_tag = agency_staff, largest window_total first, largest 5 payments per item, excluding suppliers and rows already drawn in T-11.1, (only 1 available); 3 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P02_-_published.xlsx:7` | 2026-05-27 | Comensura Ltd | £96,142.42 | Strategy & Governance |
| 1 | `Over500_2026_P03_-_published.xlsx:11` | 2026-06-22 | Comensura Ltd | £94,539.37 | Strategy & Governance |
| 1 | `Over500_2026_P03_-_published.xlsx:10` | 2026-06-16 | Comensura Ltd | £84,878.50 | Strategy & Governance |


## Prepared-by-client (PBC) request list

Derived from the test steps above. Each item names the tests that need it.

| # | Risk | Item requested | For tests |
|---|---|---|---|
| 1 | R-01 | Purchase orders and invoices for the sampled windows | T-01.1 |
| 2 | R-01 | Quotation, portal or contract records covering the sampled windows | T-01.1 |
| 3 | R-01 | Purchase orders, invoices and quotations for the lower-tier windows | T-01.2 |
| 4 | R-02 | Purchase orders, invoices and quotations for the sampled near-threshold payments | T-02.1 |
| 5 | R-02 | Purchase orders, invoices and quotations for the lower-band payments | T-02.2 |
| 6 | R-03 | Council contract register for the spend window | T-03.1 |
| 7 | R-03 | Contracts, framework call-offs or exception approvals for the sampled suppliers | T-03.1 |
| 8 | R-04 | Current contracts or extensions and S151 approvals for the flagged suppliers | T-04.1 |
| 9 | R-05 | Contracts, variations and approvals for the flagged suppliers | T-05.1 |
| 10 | R-05 | Spend to date against each sampled contract | T-05.1 |
| 11 | R-06 | Invoices and orders for the sampled repeat payments and their group partners | T-06.1 |
| 12 | R-06 | Invoices and payment run records for the same-run repeat payments | T-06.2 |
| 13 | R-07 | Waiver and exception register for the spend window | T-07.1 |
| 14 | R-07 | Exception reports, approvals and board minutes for the selected entries | T-07.1 |
| 15 | R-07 | Record of contracts let under an exclusion, with approvals | T-07.2 |
| 16 | R-08 | Award decisions and Key Decision records for the contracts behind the sampled windows | T-08.1 |
| 17 | R-08 | Award decisions for the contracts of the sampled largest suppliers | T-08.2 |
| 18 | R-08 | Procurement reports, signed contracts and sealing register entries for the contracts identified | T-08.3 |
| 19 | R-11 | Agency staff contract or framework call-off, with advice and approvals | T-11.1 |
| 20 | R-11 | Contracts or call-offs for up to two staffing suppliers selected from the unmatched general-procurement list | T-11.1 |
| 21 | R-11 | Key Decision record and award approval for the agency staff window above the Key Decision level | T-11.2 |
