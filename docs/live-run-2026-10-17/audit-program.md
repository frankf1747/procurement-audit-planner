# Audit program

*Generated 2026-10-17 by `build_pack.py` from `audit-plan.json`, `risk-register.md` (revision 1), `auditor-comments.md` by Live test (Claude, on Frank Fu instruction) dated 2026-10-17, `rules.json` and `analytics.json`. Status: DRAFT for challenge, QA review and auditor sign-off.*

**Indicators, not findings.** Every test below checks a control against a pattern in public data. Nothing here asserts wrongdoing by the council, a department, an officer or a supplier.

10 risks in scope, 11 controls, 17 tests, 329 sampled transactions. Samples are drawn by the builder from `analytics-full/` by the recipe stated under each test, and every transaction is listed with its workbook row.


## R-01: Payments to one supplier grouped under a procedure threshold [12 (High; Medium - High)]

**Audit objective.** Conclude whether requirements are aggregated before the quote or tender route is chosen, so that payments grouped under a tier reflect separate requirements rather than one split requirement.

**C-01.1. Expected control.** Requirements are aggregated before the procurement route is chosen; no contract is split or disaggregated to keep it below a quote or tender tier, and the procurement's progress is documented and kept for three years. [CPR-12, CPR-52, CPR-53, CPR-54, CPR-06, CPR-30] Owner: Relevant Service Director.

**T-01.1. Test.** For each sampled window at the £25,000 tier, obtain the orders, invoices and quotation records behind the sampled payments and establish whether they meet one requirement. Pass: the payments are separate requirements each correctly below the tier; or the requirement was treated as one and quoted via the Procurement Portal from at least three sources (App B row B1 for goods and services, row B2 for works) or tendered; or a contract on the Contract Register, a Purchasing Scheme call-off, an approved inter-authority or shared-service agreement, or an approved waiver covers it. Otherwise fail. [CPR-12, CPR-53, CPR-54, CPR-30, metric:$.tests.split_purchases.by_threshold.25000.headline_general_procurement.windows]  
**Evidence to inspect:** Purchase orders, invoices, Procurement Portal quotation records, the procurement file, Contract Register entry  
**Sample:** 10 items from `split-purchases.csv`, where threshold = 25000, dominant_tag = general_procurement, largest window_total first, largest 5 payments per item; 49 transactions

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

**T-01.2. Test.** For each sampled window at the £5,000 tier, obtain the orders and invoices behind the sampled payments and establish whether they meet one requirement. Pass: the payments are separate requirements; or, where the window total is below £25,000, the combined requirement had at least one quote from an appropriate source (App B row A) and, where it was tendered, the invitation to tender was published; or, where the window total is £25,000 or more, quotes were invited via the Procurement Portal from at least three sources (App B row B1 for goods and services, row B2 for works) or the requirement was tendered; or a contract, Purchasing Scheme call-off, approved inter-authority or shared-service agreement, or approved waiver covers it. Otherwise fail. [CPR-12, CPR-52, CPR-53, CPR-54, CPR-06, metric:$.tests.split_purchases.by_threshold.5000.headline_general_procurement.windows]  
**Evidence to inspect:** Purchase orders, invoices, quotation records, published invitation to tender where one was issued  
**Sample:** 10 items from `split-purchases.csv`, where threshold = 5000, dominant_tag = general_procurement, largest window_total first, largest 5 payments per item, excluding suppliers and rows already drawn in T-01.1; 40 transactions

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


## R-02: Payments clustering just below a quote or tender threshold [12 (High; Medium - High)]

**Audit objective.** Conclude whether payments just below a quote or tender tier are backed by the quotes that tier requires, or by evidence that they are separate requirements.

**C-02.1. Expected control.** The quote or tender route is set by the total value of the requirement, so a payment just below a tier is either a whole requirement below it or is backed by the quotes the higher tier requires. [CPR-52, CPR-53, CPR-54, CPR-12]

**T-02.1. Test.** For each sampled payment in the band just below £25,000, obtain the order, invoice and quote evidence, and list other payments to the same supplier for the same requirement. Pass: the requirement as a whole is below the tier and at least one quote was sought; or, where related payments take the requirement over the tier, quotes were invited via the Procurement Portal from at least three sources (App B row B1 or B2); or a contract, Purchasing Scheme call-off, approved inter-authority or shared-service agreement, or approved waiver covers it. Otherwise fail. [CPR-52, CPR-53, CPR-54, metric:$.tests.threshold_clustering.by_threshold.25000.by_tag.general_procurement.rows]  
**Evidence to inspect:** Purchase order, invoice, quotation records, the supplier's other payments for the same requirement  
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

**T-02.2. Test.** At the one-quote tier, where the band below £1,000 is fuller than the band above it (323 against 216 across all tags), take one sampled payment per supplier and list that supplier's other payments for the same requirement. Pass: the requirement as a whole is at or below the tier; or at least one quote from an appropriate source is held for the combined requirement; or a contract or Purchasing Scheme call-off covers it. Otherwise fail. [CPR-52, CPR-12, metric:$.tests.threshold_clustering.by_threshold.1000.by_tag.general_procurement.rows, metric:$.tests.threshold_clustering.by_threshold.1000.comparator_above.count]  
**Evidence to inspect:** Purchase order, invoice, quotation record, the supplier's other payments for the same requirement  
**Sample:** 10 items from `threshold-clustering.csv`, where threshold = 1000, tag = general_procurement, Net amount ≤ 999.99, largest Net amount first, one item per supplier_norm; 10 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P04_-_published.xlsx:300` | 2026-07-08 | WEAVAWAY TRAVEL LTD | £999.32 | Education & SEND |
| 2 | `Over500_2026_P03_-_published.xlsx:209` | 2026-06-04 | Sikandar Hayat t/a Prompt Cars | £996.43 | Education & SEND |
| 3 | `Over500_2026_P02_-_published.xlsx:341` | 2026-05-01 | Go Green Taxis Ltd | £995.95 | Education & SEND |
| 4 | `Over500_2026_P03_-_published.xlsx:17` | 2026-06-30 | PHF Training | £995.00 | Community Services |
| 5 | `Over500_2026_P03_-_published.xlsx:831` | 2026-06-15 | PRESTIGE NETWORK | £993.48 | Children's Social Care |
| 6 | `Over500_2026_P03_-_published.xlsx:61` | 2026-06-30 | MECE FIRE & SECURITY LTD | £991.01 | Environment |
| 7 | `Over500_2026_P04_-_published.xlsx:158` | 2026-07-08 | POTTINGER'S HIRE SERVICE | £990.83 | Education & SEND |
| 8 | `Over500_2026_P03_-_published.xlsx:463` | 2026-06-16 | P S Aylmer Veterinary Consultancy | £990.50 | Community Services |
| 9 | `Over500_2026_P04_-_published.xlsx:242` | 2026-07-15 | Rygor Commercials Ltd | £990.06 | Environment |
| 10 | `Over500_2026_P04_-_published.xlsx:179` | 2026-07-08 | A1 CARS | £990.00 | Education & SEND |


## R-03: High-value suppliers with no published contract notice [12 (High; Medium - High)]

**Audit objective.** Conclude whether suppliers paid above the publication tier are supplied under a contract let by the route the Rules require and recorded on the Contract Register.

**C-03.1. Expected control.** Contracts above the publication tier are let by the Appendix B route for their value, advertised and tendered electronically as the Rules require (CDP notices approved and issued by the Service Lead for Procurement and Commissioning or delegate), made in writing, notified to the Service Lead for Commissioning and Procurement and recorded on the published Contract Register. [CPR-53, CPR-56, CPR-10, CPR-11, CPR-13, CPR-32, CPR-33, CPR-07, CPR-27] Owner: Relevant Service Director; Service Lead for Commissioning and Procurement (register).

**T-03.1. Test.** For each sampled supplier with no matching notice, trace the sampled payments to the Contract Register, a framework or other Purchasing Scheme call-off, a Find a Tender notice, or a contract let before the notice export period. Pass: a written contract covering the payments is on the Contract Register and was let by the Appendix B route for its value (quotes or tender via the Procurement Portal; advertised on the CDP above the Procurement Legislation threshold, with the CDP notice approved and issued by the Service Lead for Procurement and Commissioning or delegate); or a Purchasing Scheme call-off with the advice clause 8.2 requires and the App C row C approvals; or an approved inter-authority or shared-service agreement inspected; or an approved waiver or exclusion (tested in T-07.2). Otherwise fail. A missing Contracts Finder notice alone is not a fail. [CPR-53, CPR-56, CPR-10, CPR-11, CPR-13, CPR-32, CPR-33, CPR-07, CPR-27, metric:$.tests.off_contract.unmatched_by_tag.general_procurement.suppliers]  
**Evidence to inspect:** Contract Register extract, signed contract, tender or quotation records, framework call-off and advice record, award notification to the Service Lead  
**Sample:** 10 items from `high-value-suppliers.csv`, where dominant_tag = general_procurement, match_class = none, annualised_estimate ≥ 25000, largest annualised_estimate first, 5 payments per supplier; 42 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P04_-_published.xlsx:793` | 2026-07-13 | VolkerHighways Ltd | £998,987.64 | Environment |
| 1 | `Over500_2026_P04_-_published.xlsx:603` | 2026-07-28 | VolkerHighways Ltd | £855,750.25 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:684` | 2026-06-22 | VolkerHighways Ltd | £366,872.38 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:699` | 2026-06-08 | VolkerHighways Ltd | £329,988.88 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:709` | 2026-05-05 | VolkerHighways Ltd | £311,353.42 | Environment |
| 2 | `Over500_2026_P02_-_published.xlsx:2196` | 2026-05-27 | VEOLIA ES WEST BERKSHIRE LTD (CHAPS ONLY) | £2,201,856.40 | Environment |
| 2 | `Over500_2026_P03_-_published.xlsx:2146` | 2026-06-29 | VEOLIA ES WEST BERKSHIRE LTD (CHAPS ONLY) | £2,180,425.32 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:3194` | 2026-07-27 | VEOLIA ES WEST BERKSHIRE LTD (CHAPS ONLY) | £1,803,783.32 | Environment |
| 3 | `Over500_2026_P03_-_published.xlsx:2144` | 2026-06-25 | Millbrook Healthcare Limited | £1,141,918.00 | Finance, Property & Procurement |
| 3 | `Over500_2026_P03_-_published.xlsx:2216` | 2026-06-03 | Millbrook Healthcare Limited | £1,141,918.00 | Finance, Property & Procurement |
| 3 | `Over500_2026_P04_-_published.xlsx:3789` | 2026-07-29 | Millbrook Healthcare Limited | £1,141,918.00 | Finance, Property & Procurement |
| 3 | `Over500_2026_P04_-_published.xlsx:3311` | 2026-07-29 | Millbrook Healthcare Limited | £33,611.35 | Finance, Property & Procurement |
| 4 | `Over500_2026_P02_-_published.xlsx:665` | 2026-05-15 | The Better Group Ltd | £64,500.00 | Adult Social Care |
| 4 | `Over500_2026_P02_-_published.xlsx:666` | 2026-05-15 | The Better Group Ltd | £58,833.00 | Adult Social Care |
| 4 | `Over500_2026_P03_-_published.xlsx:670` | 2026-06-01 | The Better Group Ltd | £48,784.37 | Adult Social Care |
| 4 | `Over500_2026_P04_-_published.xlsx:783` | 2026-07-29 | The Better Group Ltd | £48,518.00 | Adult Social Care |
| 4 | `Over500_2026_P02_-_published.xlsx:667` | 2026-05-19 | The Better Group Ltd | £41,125.00 | Adult Social Care |
| 5 | `Over500_2026_P02_-_published.xlsx:473` | 2026-05-27 | SoftwareONE UK Ltd | £375,697.68 | Transformation, Customer & ICT |
| 5 | `Over500_2026_P02_-_published.xlsx:474` | 2026-05-27 | SoftwareONE UK Ltd | £85,871.04 | Transformation, Customer & ICT |
| 5 | `Over500_2026_P02_-_published.xlsx:653` | 2026-05-27 | SoftwareONE UK Ltd | £59,650.56 | Transformation, Customer & ICT |
| 5 | `Over500_2026_P02_-_published.xlsx:654` | 2026-05-27 | SoftwareONE UK Ltd | £1,759.34 | Transformation, Customer & ICT |
| 6 | `Over500_2026_P02_-_published.xlsx:2200` | 2026-05-13 | Livity Life Ltd | £135,591.03 | Finance, Property & Procurement |
| 6 | `Over500_2026_P03_-_published.xlsx:3087` | 2026-06-17 | Livity Life Ltd | £127,886.78 | Finance, Property & Procurement |
| 6 | `Over500_2026_P04_-_published.xlsx:3310` | 2026-07-13 | Livity Life Ltd | £50,961.45 | Finance, Property & Procurement |
| 6 | `Over500_2026_P04_-_published.xlsx:3197` | 2026-07-13 | Livity Life Ltd | £46,409.47 | Finance, Property & Procurement |
| 6 | `Over500_2026_P02_-_published.xlsx:2199` | 2026-05-13 | Livity Life Ltd | £42,882.27 | Finance, Property & Procurement |
| 7 | `Over500_2026_P04_-_published.xlsx:784` | 2026-07-10 | E W BEARD LTD | £64,202.50 | Education & SEND |
| 7 | `Over500_2026_P02_-_published.xlsx:674` | 2026-05-20 | E W BEARD LTD | £60,039.70 | Education & SEND |
| 7 | `Over500_2026_P02_-_published.xlsx:675` | 2026-05-20 | E W BEARD LTD | £55,594.00 | Education & SEND |
| 7 | `Over500_2026_P03_-_published.xlsx:664` | 2026-06-10 | E W BEARD LTD | £38,672.00 | Education & SEND |
| 7 | `Over500_2026_P02_-_published.xlsx:672` | 2026-05-20 | E W BEARD LTD | £36,170.52 | Education & SEND |
| 8 | `Over500_2026_P02_-_published.xlsx:2198` | 2026-05-13 | SLOUGH BOROUGH COUNCIL | £296,177.15 | Finance, Property & Procurement |
| 9 | `Over500_2026_P03_-_published.xlsx:183` | 2026-06-03 | Sikandar Hayat t/a Prompt Cars | £73,296.50 | Education & SEND |
| 9 | `Over500_2026_P03_-_published.xlsx:203` | 2026-06-03 | Sikandar Hayat t/a Prompt Cars | £26,085.00 | Education & SEND |
| 9 | `Over500_2026_P03_-_published.xlsx:208` | 2026-06-03 | Sikandar Hayat t/a Prompt Cars | £17,607.50 | Education & SEND |
| 9 | `Over500_2026_P03_-_published.xlsx:162` | 2026-06-03 | Sikandar Hayat t/a Prompt Cars | £9,944.00 | Education & SEND |
| 9 | `Over500_2026_P04_-_published.xlsx:220` | 2026-07-21 | Sikandar Hayat t/a Prompt Cars | £3,743.00 | Education & SEND |
| 10 | `Over500_2026_P02_-_published.xlsx:530` | 2026-05-27 | Elior UK PLC | £23,694.03 | Adult Social Care |
| 10 | `Over500_2026_P03_-_published.xlsx:440` | 2026-06-16 | Elior UK PLC | £23,516.69 | Adult Social Care |
| 10 | `Over500_2026_P04_-_published.xlsx:533` | 2026-07-28 | Elior UK PLC | £23,173.08 | Adult Social Care |
| 10 | `Over500_2026_P03_-_published.xlsx:433` | 2026-06-17 | Elior UK PLC | £18,592.30 | Adult Social Care |
| 10 | `Over500_2026_P02_-_published.xlsx:525` | 2026-05-13 | Elior UK PLC | £18,371.14 | Adult Social Care |

**T-03.2. Test.** For each sampled supplier whose name only nearly matches a notice, confirm with the procurement team whether the candidate notice is the same supplier. Where it is, check the contract behind the notice covers the sampled payments and is on the Contract Register; where it is not, test the supplier as in T-03.1. Pass: as T-03.1. Otherwise fail. [CPR-07, CPR-33, metric:$.tests.off_contract.per_match_class.near_contain.suppliers, metric:$.tests.off_contract.per_match_class.near_ratio.suppliers]  
**Evidence to inspect:** Candidate notice, Contract Register entry, signed contract, Companies House record of the supplier  
**Sample:** 6 items from `high-value-suppliers.csv`, where dominant_tag = general_procurement, match_class = ['near_ratio', 'near_contain'], annualised_estimate ≥ 25000, largest annualised_estimate first, 3 payments per supplier, (only 6 available); 18 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P03_-_published.xlsx:661` | 2026-06-08 | ANDY AND ES LIMITED | £59,335.72 | Education & SEND |
| 1 | `Over500_2026_P04_-_published.xlsx:1283` | 2026-07-15 | ANDY AND ES LIMITED | £56,941.82 | Education & SEND |
| 1 | `Over500_2026_P02_-_published.xlsx:670` | 2026-05-13 | ANDY AND ES LIMITED | £54,881.31 | Education & SEND |
| 2 | `Over500_2026_P02_-_published.xlsx:173` | 2026-05-26 | Glen Cleaning Company Ltd | £5,829.96 | Finance, Property & Procurement |
| 2 | `Over500_2026_P04_-_published.xlsx:148` | 2026-07-01 | Glen Cleaning Company Ltd | £5,829.96 | Finance, Property & Procurement |
| 2 | `Over500_2026_P04_-_published.xlsx:399` | 2026-07-24 | Glen Cleaning Company Ltd | £5,829.96 | Finance, Property & Procurement |
| 3 | `Over500_2026_P04_-_published.xlsx:247` | 2026-07-09 | BAILEYS OF NEWBURY | £6,592.17 | Education & SEND |
| 3 | `Over500_2026_P04_-_published.xlsx:186` | 2026-07-14 | BAILEYS OF NEWBURY | £6,035.29 | Education & SEND |
| 3 | `Over500_2026_P04_-_published.xlsx:180` | 2026-07-08 | BAILEYS OF NEWBURY | £6,006.45 | Education & SEND |
| 4 | `Over500_2026_P04_-_published.xlsx:278` | 2026-07-14 | D J TRAVEL | £7,035.00 | Adult Social Care |
| 4 | `Over500_2026_P04_-_published.xlsx:279` | 2026-07-14 | D J TRAVEL | £6,846.00 | Adult Social Care |
| 4 | `Over500_2026_P02_-_published.xlsx:217` | 2026-05-18 | D J TRAVEL | £6,700.00 | Adult Social Care |
| 5 | `Over500_2026_P04_-_published.xlsx:232` | 2026-07-10 | Kennet & Avon Group | £2,970.00 | Education & SEND |
| 5 | `Over500_2026_P02_-_published.xlsx:277` | 2026-05-26 | Kennet & Avon Group | £1,890.00 | Education & SEND |
| 5 | `Over500_2026_P04_-_published.xlsx:293` | 2026-07-24 | Kennet & Avon Group | £1,755.00 | Education & SEND |
| 6 | `Over500_2026_P04_-_published.xlsx:297` | 2026-07-08 | POTTINGER'S HIRE SERVICE | £1,981.67 | Education & SEND |
| 6 | `Over500_2026_P02_-_published.xlsx:291` | 2026-05-27 | POTTINGER'S HIRE SERVICE | £1,450.00 | Education & SEND |
| 6 | `Over500_2026_P04_-_published.xlsx:176` | 2026-07-27 | POTTINGER'S HIRE SERVICE | £1,450.00 | Education & SEND |


## R-04: Spend continuing after a published contract notice ended [9 (High; Medium - High)]

**Audit objective.** Conclude whether payments made after a published contract ended are covered by an approved extension or a replacement contract.

**C-04.1. Expected control.** A contract is extended only where it provides for extension and the S151 Officer approves it before expiry; otherwise a replacement contract is let under the Rules and recorded on the Contract Register. [CPR-60, CPR-33, CPR-07] Owner: S151 Officer (extension approval).

**T-04.1. Test.** For each sampled supplier, obtain the contract behind the ended notice and the sampled payments' invoices, and compare the invoice periods with the contract term. Pass: the payments are for supply delivered within the original term; or the contract provides for extension and the S151 Officer approved it before the end date; or a replacement contract let under the Rules and on the Contract Register covers the payments; or an approved waiver covers them (tested in T-07.2). Otherwise fail. [CPR-60, CPR-33, metric:$.tests.expired_notice_spend.by_dominant_tag.general_procurement, metric:$.tests.expired_notice_spend.gbp_in_window]  
**Evidence to inspect:** Original contract and its extension clause, S151 Officer extension approval with date, replacement contract and Contract Register entry, invoices  
**Sample:** 8 items from `expired-notice-spend.csv`, where dominant_tag = general_procurement, largest total_gbp first, 5 payments per supplier, (only 8 available); 17 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P03_-_published.xlsx:704` | 2026-06-16 | Hope & Clay (Construction) Ltd | £91,306.75 | Environment |
| 2 | `Over500_2026_P03_-_published.xlsx:58` | 2026-06-03 | BERKSHIRE MECHANICAL SERVICES | £8,250.00 | Development & Housing |
| 2 | `Over500_2026_P03_-_published.xlsx:42` | 2026-06-03 | BERKSHIRE MECHANICAL SERVICES | £6,250.00 | Development & Housing |
| 2 | `Over500_2026_P03_-_published.xlsx:279` | 2026-06-09 | BERKSHIRE MECHANICAL SERVICES | £5,585.00 | Development & Housing |
| 2 | `Over500_2026_P03_-_published.xlsx:52` | 2026-06-09 | BERKSHIRE MECHANICAL SERVICES | £4,000.00 | Development & Housing |
| 2 | `Over500_2026_P04_-_published.xlsx:374` | 2026-07-03 | BERKSHIRE MECHANICAL SERVICES | £3,400.00 | Development & Housing |
| 3 | `Over500_2026_P04_-_published.xlsx:856` | 2026-07-14 | Berkshire Womens Aid | £39,569.75 | Public Health & Wellbeing |
| 3 | `Over500_2026_P04_-_published.xlsx:721` | 2026-07-14 | Berkshire Womens Aid | £13,427.75 | Public Health & Wellbeing |
| 4 | `Over500_2026_P02_-_published.xlsx:467` | 2026-05-08 | G7 BUSINESS SOLUTIONS LIMITED | £5,469.78 | Finance, Property & Procurement |
| 4 | `Over500_2026_P03_-_published.xlsx:531` | 2026-06-10 | G7 BUSINESS SOLUTIONS LIMITED | £5,469.78 | Finance, Property & Procurement |
| 4 | `Over500_2026_P03_-_published.xlsx:721` | 2026-06-10 | G7 BUSINESS SOLUTIONS LIMITED | £1,365.00 | Finance, Property & Procurement |
| 4 | `Over500_2026_P04_-_published.xlsx:1309` | 2026-07-15 | G7 BUSINESS SOLUTIONS LIMITED | £1,365.00 | Finance, Property & Procurement |
| 4 | `Over500_2026_P02_-_published.xlsx:762` | 2026-05-19 | G7 BUSINESS SOLUTIONS LIMITED | £910.00 | Finance, Property & Procurement |
| 5 | `Over500_2026_P02_-_published.xlsx:459` | 2026-05-15 | CACI Limited | £12,071.67 | Children's Social Care |
| 6 | `Over500_2026_P03_-_published.xlsx:686` | 2026-06-22 | Morton Pattison Ltd | £1,102.00 | Environment |
| 7 | `Over500_2026_P03_-_published.xlsx:821` | 2026-06-03 | Davis and Associates Consultancy Limited | £800.00 | Chief Executive |
| 8 | `Over500_2026_P04_-_published.xlsx:58` | 2026-07-20 | Tactical Facilities Management Ltd | £681.94 | Development & Housing |


## R-05: Spend running above the awarded contract value [12 (High; Medium - High)]

**Audit objective.** Conclude whether spend running above a published award value is covered by the award's value basis or by a variation approved as the Rules require.

**C-05.1. Expected control.** A variation of scope is approved before it takes effect: in writing by the Monitoring Officer and S151 Officer below the Threshold, and by the relevant board on a report with their recommendation above it. [CPR-61, CPR-62] Owner: Monitoring Officer and S151 Officer; relevant board above the Threshold.

**T-05.1. Test.** For every flagged supplier (ratio at or above 1.25), obtain the contract, its value basis and any variations, and reconcile them to the sampled payments. Confirm the Threshold figure before fieldwork, then apply the approval route for the contract's value. Pass: the award value is an estimate or maximum that the contract terms show covers the spend; or the spend falls under other contracts with the supplier, each on the Contract Register; or a variation was approved in advance by the approver for the contract's value. Otherwise fail. [CPR-61, CPR-62, metric:$.tests.spend_vs_award.suppliers_flagged, metric:$.tests.spend_vs_award.flagged_annualised_estimate]  
**Evidence to inspect:** Contract and award report showing the value basis, variation approvals with dates, board report where above the Threshold, invoices  
**Sample:** 12 items from `spend-vs-award.csv`, where ratio ≥ 1.25, largest annualised_estimate first, 5 payments per supplier; 42 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P02_-_published.xlsx:437` | 2026-05-20 | Newbury & District Ltd | £60,797.19 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:267` | 2026-06-01 | Newbury & District Ltd | £59,626.76 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:270` | 2026-06-30 | Newbury & District Ltd | £59,007.20 | Environment |
| 1 | `Over500_2026_P04_-_published.xlsx:363` | 2026-07-27 | Newbury & District Ltd | £58,759.29 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:269` | 2026-06-12 | Newbury & District Ltd | £14,852.00 | Environment |
| 2 | `Over500_2026_P04_-_published.xlsx:905` | 2026-07-22 | NEC SOFTWARE SOLUTIONS UK LIMITED | £129,125.00 | Finance, Property & Procurement |
| 2 | `Over500_2026_P04_-_published.xlsx:492` | 2026-07-22 | NEC SOFTWARE SOLUTIONS UK LIMITED | £91,629.15 | Finance, Property & Procurement |
| 2 | `Over500_2026_P04_-_published.xlsx:487` | 2026-07-22 | NEC SOFTWARE SOLUTIONS UK LIMITED | £52,054.00 | Finance, Property & Procurement |
| 2 | `Over500_2026_P04_-_published.xlsx:494` | 2026-07-24 | NEC SOFTWARE SOLUTIONS UK LIMITED | £15,094.00 | Finance, Property & Procurement |
| 2 | `Over500_2026_P04_-_published.xlsx:488` | 2026-07-22 | NEC SOFTWARE SOLUTIONS UK LIMITED | £13,063.00 | Finance, Property & Procurement |
| 3 | `Over500_2026_P03_-_published.xlsx:2130` | 2026-06-09 | TWO SAINTS LTD | £38,775.00 | Development & Housing |
| 3 | `Over500_2026_P04_-_published.xlsx:3181` | 2026-07-22 | TWO SAINTS LTD | £38,775.00 | Development & Housing |
| 3 | `Over500_2026_P02_-_published.xlsx:2160` | 2026-05-12 | TWO SAINTS LTD | £27,147.69 | Development & Housing |
| 3 | `Over500_2026_P02_-_published.xlsx:2161` | 2026-05-13 | TWO SAINTS LTD | £27,147.69 | Development & Housing |
| 3 | `Over500_2026_P02_-_published.xlsx:2162` | 2026-05-27 | TWO SAINTS LTD | £27,147.69 | Development & Housing |
| 4 | `Over500_2026_P04_-_published.xlsx:321` | 2026-07-14 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £4,074.00 | Education & SEND |
| 4 | `Over500_2026_P04_-_published.xlsx:266` | 2026-07-14 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £4,018.00 | Education & SEND |
| 4 | `Over500_2026_P04_-_published.xlsx:467` | 2026-07-09 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £4,018.00 | Education & SEND |
| 4 | `Over500_2026_P04_-_published.xlsx:261` | 2026-07-13 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £3,956.00 | Education & SEND |
| 4 | `Over500_2026_P04_-_published.xlsx:267` | 2026-07-14 | FD TRAVELS LIMITED T/A SCHOOL EXPRESS | £3,792.50 | Education & SEND |
| 5 | `Over500_2026_P04_-_published.xlsx:1276` | 2026-07-22 | WCL UK Ltd (Trading as Everything ICT) | £102,882.78 | Education & SEND |
| 6 | `Over500_2026_P03_-_published.xlsx:371` | 2026-06-08 | IDOX SOFTWARE LTD | £48,579.20 | Community Services |
| 6 | `Over500_2026_P02_-_published.xlsx:462` | 2026-05-20 | IDOX SOFTWARE LTD | £2,647.21 | Development & Housing |
| 7 | `Over500_2026_P04_-_published.xlsx:207` | 2026-07-22 | ACE WHEELCHAIR TRAVEL | £4,840.00 | Education & SEND |
| 7 | `Over500_2026_P04_-_published.xlsx:328` | 2026-07-29 | ACE WHEELCHAIR TRAVEL | £3,916.00 | Education & SEND |
| 7 | `Over500_2026_P04_-_published.xlsx:445` | 2026-07-22 | ACE WHEELCHAIR TRAVEL | £3,520.00 | Education & SEND |
| 7 | `Over500_2026_P03_-_published.xlsx:232` | 2026-06-09 | ACE WHEELCHAIR TRAVEL | £3,300.00 | Education & SEND |
| 7 | `Over500_2026_P02_-_published.xlsx:370` | 2026-05-12 | ACE WHEELCHAIR TRAVEL | £3,080.00 | Education & SEND |
| 8 | `Over500_2026_P03_-_published.xlsx:396` | 2026-06-10 | BookingLab Limited | £24,000.00 | Transformation, Customer & ICT |
| 9 | `Over500_2026_P04_-_published.xlsx:313` | 2026-07-08 | Valley Cars | £3,173.00 | Education & SEND |
| 9 | `Over500_2026_P03_-_published.xlsx:222` | 2026-06-02 | Valley Cars | £2,505.00 | Education & SEND |
| 9 | `Over500_2026_P02_-_published.xlsx:354` | 2026-05-06 | Valley Cars | £2,338.00 | Education & SEND |
| 9 | `Over500_2026_P04_-_published.xlsx:462` | 2026-07-08 | Valley Cars | £2,040.00 | Education & SEND |
| 9 | `Over500_2026_P02_-_published.xlsx:233` | 2026-05-05 | Valley Cars | £2,004.00 | Education & SEND |
| 10 | `Over500_2026_P03_-_published.xlsx:384` | 2026-06-04 | Exacom Systems Ltd | £12,105.85 | Development & Housing |
| 11 | `Over500_2026_P02_-_published.xlsx:460` | 2026-05-20 | Softcat Ltd | £8,979.02 | Education & SEND |
| 11 | `Over500_2026_P03_-_published.xlsx:375` | 2026-06-17 | Softcat Ltd | £2,025.98 | Transformation, Customer & ICT |
| 12 | `Over500_2026_P03_-_published.xlsx:276` | 2026-06-30 | SMS-Environmental Ltd | £2,070.00 | Adult Social Care |
| 12 | `Over500_2026_P04_-_published.xlsx:365` | 2026-07-09 | SMS-Environmental Ltd | £1,335.60 | Adult Social Care |
| 12 | `Over500_2026_P03_-_published.xlsx:29` | 2026-06-22 | SMS-Environmental Ltd | £1,175.00 | Adult Social Care |
| 12 | `Over500_2026_P02_-_published.xlsx:17` | 2026-05-28 | SMS-Environmental Ltd | £1,129.15 | Adult Social Care |
| 12 | `Over500_2026_P02_-_published.xlsx:19` | 2026-05-27 | SMS-Environmental Ltd | £759.16 | Adult Social Care |


## R-06: Repeated payments of the same amount to the same supplier [9 (High; Medium - High)]

**Audit objective.** Conclude whether repeated same-amount payments to one supplier on different payment runs each rest on written evidence of a distinct purchase.

**C-06.1. Expected control.** Each payment is supported by written evidence of the purchase, so a repeated invoice is identified before payment or recovered after it. [CPR-31]

**T-06.1. Test.** For each sampled group, pull every payment in the same group from the duplicates list and match each to its own invoice and order or contract schedule. Pass: each payment has a distinct invoice for a distinct supply or period; or the repeat was identified and a credit note or recovery is on record. Otherwise fail. [CPR-31, metric:$.tests.duplicates.different_time.by_tag.general_procurement.groups, metric:$.tests.duplicates.different_time.by_tag.general_procurement.gbp_beyond_first]  
**Evidence to inspect:** Invoices, purchase orders or contract payment schedules, credit notes or recovery records  
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

**T-06.2. Test.** For each sampled placement group, pull every payment in the same group from the duplicates list and match each to the placement agreement and invoice. Also apply this test to every placement group in the duplicates top 20 in analytics.json with five or more payments, since the row sample is ordered by payment amount and does not reach the groups with the largest amount beyond the first payment. Pass: each payment relates to a distinct service user or a distinct period on the placement agreement or invoice; or the repeat was identified and a credit note or recovery is on record. Otherwise fail. [CPR-31, metric:$.tests.duplicates.different_time.by_tag.care_or_education_placement.groups, metric:$.tests.duplicates.different_time.by_tag.care_or_education_placement.gbp_beyond_first, metric:$.tests.duplicates.different_time.top20[19].gbp_beyond_first, metric:$.tests.duplicates.different_time.top20[17].gbp_beyond_first]  
**Evidence to inspect:** Placement agreements, provider invoices showing service user and period, credit notes or recovery records  
**Sample:** 10 items from `duplicates.csv`, where tier = different_time, tag = care_or_education_placement, largest Net amount first, one item per group; 10 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P02_-_published.xlsx:2092` | 2026-05-26 | Amegreen Childrens Services | £34,431.08 | Children's Social Care |
| 2 | `Over500_2026_P04_-_published.xlsx:3081` | 2026-07-20 | Amegreen Childrens Services | £34,431.08 | Children's Social Care |
| 3 | `Over500_2026_P02_-_published.xlsx:2091` | 2026-05-26 | Amegreen Childrens Services | £33,320.40 | Children's Social Care |
| 4 | `Over500_2026_P03_-_published.xlsx:2032` | 2026-06-17 | Amegreen Childrens Services | £33,320.40 | Children's Social Care |
| 5 | `Over500_2026_P02_-_published.xlsx:2246` | 2026-05-19 | Phoenix Child Care Limited -The Grange School | £32,711.33 | Education (DSG Funded) & Other Education Grants |
| 6 | `Over500_2026_P02_-_published.xlsx:2266` | 2026-05-26 | Huckleberry House | £30,918.75 | Education (DSG Funded) & Other Education Grants |
| 7 | `Over500_2026_P03_-_published.xlsx:1708` | 2026-06-24 | Brighter Living Care Ltd | £26,734.96 | Adult Social Care |
| 8 | `Over500_2026_P03_-_published.xlsx:1656` | 2026-06-24 | Brighter Living Care Ltd | £26,596.08 | Adult Social Care |
| 9 | `Over500_2026_P02_-_published.xlsx:2272` | 2026-05-26 | ACORN CARE & EDUCATION LTD | £25,533.70 | Education (DSG Funded) & Other Education Grants |
| 10 | `Over500_2026_P02_-_published.xlsx:2033` | 2026-05-12 | Care Services To You | £23,989.77 | Children's Social Care |


## R-07: Waivers and exceptions to competition [4 (Moderate; Moderate)]

**Audit objective.** Conclude whether waivers and exceptions to competition are documented and approved in advance by the officers the Rules name, at the level their value requires.

**C-07.1. Expected control.** Competition is waived only in the circumstances of clause 7.2, by the Monitoring Officer and/or S151 Officer, approved in advance at the level the contract value requires (S151 Officer up to the Threshold; with Monitoring Officer and Executive Director consultation and an exception report up to £500,000; the Executive above it), fully documented, reported to the relevant board in advance where required, with the S151 Officer's record that the circumstances are genuinely exceptional; or competition is excluded under the Procurement Legislation with the Monitoring Officer's prior written approval. [CPR-19, CPR-20, CPR-21, CPR-22, CPR-23, CPR-24, CPR-25, CPR-26, CPR-57] Owner: Monitoring Officer and S151 Officer.

**T-07.1. Test.** Obtain the record of waivers and exceptions granted in the spend window, or confirmation that none is kept. Take the five largest above £24,999.99 (all if fewer) and inspect each. Pass: the reason fits clause 7.2; it was approved before award by the officer or body the value requires; the documentation and the S151 Officer's record are complete; and the board report was made in advance where required; or competition was excluded under the Procurement Legislation with the Monitoring Officer's prior written approval. Otherwise fail. No waiver record kept is itself reported. [CPR-19, CPR-20, CPR-21, CPR-22, CPR-23, CPR-24, CPR-25, CPR-26, CPR-57]  
**Evidence to inspect:** Waiver and exception record, approval with date, exception report, board report, S151 Officer's record of reasons  
**Sample:** drawn from the council's waiver and exception record (not visible in the spend data): five largest above the waiver value, all if fewer

**T-07.2. Test.** Where T-03.1, T-03.2, T-04.1, T-05.1, T-08.2 or T-11.1 relies on a waiver or exclusion rather than a contract, extension, variation or framework route, obtain the waiver and test it as in T-07.1. Pass and fail as T-07.1. [CPR-20, CPR-24, CPR-26, metric:$.tests.off_contract.unmatched_by_tag.general_procurement.suppliers]  
**Evidence to inspect:** Waiver or exclusion record and its approvals for each item relying on one  
**Sample:** follow-through on the items sampled in T-03.1, T-03.2, T-04.1, T-05.1, T-08.2 and T-11.1 that rely on a waiver or exclusion


## R-08: Award approval and Key Decisions for the largest contracts [12 (High; Medium - High)]

**Audit objective.** Conclude whether the largest awards were taken as Key Decisions or approved by the Executive, and every award at the Appendix A level for its value.

**C-08.1. Expected control.** A contract over £500,000 is awarded as a Key Decision, with Executive approval from £2,500,000, works at that value are fully tendered, and the requirement is not split below the Key Decision value. [CPR-04, CPR-50, CPR-51, CPR-55, CPR-12] Owner: Relevant Service Director with the Portfolio Holder; the Executive.

**T-08.1. Test.** For each window whose payments combine above £500,000, identify the contract the sampled payments are made under and its total contract value. Pass: a Key Decision by the Service Director with the Portfolio Holder on a written report, or Executive approval from £2,500,000, is on record; works at that value were fully tendered (App B row C) or let under the Procurement Legislation; or the payments are shown to be separate requirements each below the Key Decision value. Otherwise fail. [CPR-04, CPR-50, CPR-51, CPR-55, metric:$.tests.split_purchases.by_threshold.500000.headline_general_procurement.windows]  
**Evidence to inspect:** Contract, Key Decision record or Executive minute, written award report, tender records  
**Sample:** 2 items from `split-purchases.csv`, where threshold = 500000, dominant_tag = general_procurement, largest window_total first, largest 5 payments per item, (only 2 available); 9 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P03_-_published.xlsx:699` | 2026-06-08 | VolkerHighways Ltd | £329,988.88 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:701` | 2026-06-09 | VolkerHighways Ltd | £307,338.45 | Environment |
| 1 | `Over500_2026_P03_-_published.xlsx:729` | 2026-06-08 | VolkerHighways Ltd | £299,416.56 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:711` | 2026-05-26 | VolkerHighways Ltd | £200,305.25 | Environment |
| 1 | `Over500_2026_P02_-_published.xlsx:702` | 2026-05-13 | VolkerHighways Ltd | £195,844.36 | Environment |
| 2 | `Over500_2026_P02_-_published.xlsx:473` | 2026-05-27 | SoftwareONE UK Ltd | £375,697.68 | Transformation, Customer & ICT |
| 2 | `Over500_2026_P02_-_published.xlsx:474` | 2026-05-27 | SoftwareONE UK Ltd | £85,871.04 | Transformation, Customer & ICT |
| 2 | `Over500_2026_P02_-_published.xlsx:653` | 2026-05-27 | SoftwareONE UK Ltd | £59,650.56 | Transformation, Customer & ICT |
| 2 | `Over500_2026_P02_-_published.xlsx:654` | 2026-05-27 | SoftwareONE UK Ltd | £1,759.34 | Transformation, Customer & ICT |

**C-08.2. Expected control.** Every award rests on a decision by the approver Appendix A names for its total contract value, against an approved budget provision and after the supplier suitability checks, and above the Threshold a written procurement report is produced and kept for three years. [CPR-02, CPR-03, CPR-05, CPR-09, CPR-48, CPR-49, CPR-50, CPR-51, CPR-28, CPR-29] Owner: Relevant Service Director.

**T-08.2. Test.** For each sampled supplier, identify the contract behind the sampled payments, establish its total contract value and the Appendix A row it falls in, and inspect the award decision. Confirm the Threshold figure before fieldwork. Pass: the decision was taken by the approver that row names, with the recommendations and written report it requires; the award record shows the approved budget provision and the supplier suitability checks; and the procurement report is kept where above the Threshold; or a Purchasing Scheme call-off or waiver carries the App C approvals. Otherwise fail. [CPR-48, CPR-49, CPR-50, CPR-51, CPR-28, CPR-03, CPR-09, metric:$.tests.high_value_suppliers.tiers.publication_threshold.headline_general_procurement_suppliers]  
**Evidence to inspect:** Contract, award decision record, written procurement report, Key Decision record or Executive minute where applicable, budget line, supplier suitability checks on the procurement file  
**Sample:** 10 items from `high-value-suppliers.csv`, where dominant_tag = general_procurement, annualised_estimate ≥ 500000, largest annualised_estimate first, 3 payments per supplier; 28 transactions

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
| 7 | `Over500_2026_P02_-_published.xlsx:437` | 2026-05-20 | Newbury & District Ltd | £60,797.19 | Environment |
| 7 | `Over500_2026_P03_-_published.xlsx:267` | 2026-06-01 | Newbury & District Ltd | £59,626.76 | Environment |
| 7 | `Over500_2026_P03_-_published.xlsx:270` | 2026-06-30 | Newbury & District Ltd | £59,007.20 | Environment |
| 8 | `Over500_2026_P04_-_published.xlsx:784` | 2026-07-10 | E W BEARD LTD | £64,202.50 | Education & SEND |
| 8 | `Over500_2026_P02_-_published.xlsx:674` | 2026-05-20 | E W BEARD LTD | £60,039.70 | Education & SEND |
| 8 | `Over500_2026_P02_-_published.xlsx:675` | 2026-05-20 | E W BEARD LTD | £55,594.00 | Education & SEND |
| 9 | `Over500_2026_P02_-_published.xlsx:669` | 2026-05-26 | ASCIA CONSTRUCTION LIMITED | £332,579.29 | Education & SEND |
| 10 | `Over500_2026_P04_-_published.xlsx:905` | 2026-07-22 | NEC SOFTWARE SOLUTIONS UK LIMITED | £129,125.00 | Finance, Property & Procurement |
| 10 | `Over500_2026_P04_-_published.xlsx:492` | 2026-07-22 | NEC SOFTWARE SOLUTIONS UK LIMITED | £91,629.15 | Finance, Property & Procurement |
| 10 | `Over500_2026_P04_-_published.xlsx:487` | 2026-07-22 | NEC SOFTWARE SOLUTIONS UK LIMITED | £52,054.00 | Finance, Property & Procurement |


## R-09: Care and education placements bought outside competition [8 (High; Medium - High)]

**Audit objective.** Conclude whether placements bought under the social care exclusion record the reasons for the provider chosen and, above the Threshold, carry board approval.

**C-09.1. Expected control.** Service Directors ensure the reasons for the choice of provider are recorded on the individual's case notes, and a placement contract above the Threshold under the exclusion is approved by the relevant board. [CPR-63, CPR-64, CPR-58] Owner: Relevant Service Director.

**T-09.1. Test.** For the sampled payments in each placement window, identify the placement and inspect the case notes for the reasons the provider was chosen. Confirm the Threshold figure before fieldwork and, for every placement contract whose annual or total value exceeds it, obtain the board approval. Pass: the reasons are recorded and board approval is held where required; or the placement was let under a competed contract or framework on the Contract Register; or it was awarded under the Provider Selection Regime with its key decisions recorded. Otherwise fail. Recurring payments alone are not an exception. [CPR-63, CPR-64, CPR-58, metric:$.tests.split_purchases.by_threshold.25000.care_or_education_placement.windows]  
**Evidence to inspect:** Case notes, placement agreement, board approval of the exclusion, Contract Register or framework entry  
**Sample:** 5 items from `split-purchases.csv`, where threshold = 25000, dominant_tag = care_or_education_placement, largest window_total first, largest 5 payments per item; 25 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P04_-_published.xlsx:1850` | 2026-07-08 | BUPA Care Services | £10,400.00 | Adult Social Care |
| 1 | `Over500_2026_P04_-_published.xlsx:2908` | 2026-07-08 | BUPA Care Services | £9,903.62 | Adult Social Care |
| 1 | `Over500_2026_P04_-_published.xlsx:1824` | 2026-07-08 | BUPA Care Services | £9,903.62 | Adult Social Care |
| 1 | `Over500_2026_P04_-_published.xlsx:1043` | 2026-07-08 | BUPA Care Services | £9,903.62 | Adult Social Care |
| 1 | `Over500_2026_P04_-_published.xlsx:1039` | 2026-07-08 | BUPA Care Services | £9,903.62 | Adult Social Care |
| 2 | `Over500_2026_P03_-_published.xlsx:2198` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,534.90 | Education (DSG Funded) & Other Education Grants |
| 2 | `Over500_2026_P03_-_published.xlsx:2196` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,534.90 | Education (DSG Funded) & Other Education Grants |
| 2 | `Over500_2026_P03_-_published.xlsx:2191` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,534.90 | Education (DSG Funded) & Other Education Grants |
| 2 | `Over500_2026_P03_-_published.xlsx:2192` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,534.90 | Education (DSG Funded) & Other Education Grants |
| 2 | `Over500_2026_P03_-_published.xlsx:2193` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,534.90 | Education (DSG Funded) & Other Education Grants |
| 3 | `Over500_2026_P04_-_published.xlsx:2239` | 2026-07-01 | Affinity Trust Support Ltd | £24,926.00 | Adult Social Care |
| 3 | `Over500_2026_P03_-_published.xlsx:1629` | 2026-06-24 | Affinity Trust Support Ltd | £17,444.96 | Adult Social Care |
| 3 | `Over500_2026_P03_-_published.xlsx:1678` | 2026-06-24 | Affinity Trust Support Ltd | £14,080.00 | Adult Social Care |
| 3 | `Over500_2026_P04_-_published.xlsx:2342` | 2026-07-01 | Affinity Trust Support Ltd | £14,080.00 | Adult Social Care |
| 3 | `Over500_2026_P04_-_published.xlsx:2350` | 2026-07-08 | Affinity Trust Support Ltd | £13,237.62 | Adult Social Care |
| 4 | `Over500_2026_P02_-_published.xlsx:2245` | 2026-05-19 | Phoenix Child Care Limited -The Grange School | £23,210.00 | Education (DSG Funded) & Other Education Grants |
| 4 | `Over500_2026_P02_-_published.xlsx:2258` | 2026-05-20 | Phoenix Child Care Limited -The Grange School | £23,210.00 | Education (DSG Funded) & Other Education Grants |
| 4 | `Over500_2026_P02_-_published.xlsx:2262` | 2026-05-21 | Phoenix Child Care Limited -The Grange School | £23,210.00 | Education (DSG Funded) & Other Education Grants |
| 4 | `Over500_2026_P02_-_published.xlsx:2259` | 2026-05-20 | Phoenix Child Care Limited -The Grange School | £23,076.67 | Education (DSG Funded) & Other Education Grants |
| 4 | `Over500_2026_P03_-_published.xlsx:2229` | 2026-06-17 | Phoenix Child Care Limited -The Grange School | £22,295.24 | Education (DSG Funded) & Other Education Grants |
| 5 | `Over500_2026_P02_-_published.xlsx:1508` | 2026-05-20 | GCH (Alder) Ltd t/a Hungerford Care Home | £18,144.00 | Adult Social Care |
| 5 | `Over500_2026_P02_-_published.xlsx:1573` | 2026-05-20 | GCH (Alder) Ltd t/a Hungerford Care Home | £6,580.00 | Adult Social Care |
| 5 | `Over500_2026_P03_-_published.xlsx:1497` | 2026-06-17 | GCH (Alder) Ltd t/a Hungerford Care Home | £6,580.00 | Adult Social Care |
| 5 | `Over500_2026_P02_-_published.xlsx:1018` | 2026-05-20 | GCH (Alder) Ltd t/a Hungerford Care Home | £6,000.00 | Adult Social Care |
| 5 | `Over500_2026_P03_-_published.xlsx:2714` | 2026-06-17 | GCH (Alder) Ltd t/a Hungerford Care Home | £6,000.00 | Adult Social Care |

**T-09.2. Test.** For every placement window whose payments combine above £500,000, identify the placement contracts behind the sampled payments and their annual or total value. Confirm the Threshold figure before fieldwork and, for every contract above it, obtain the relevant board's approval of the exclusion; inspect the case notes for the sampled payments as in T-09.1. Payments already drawn in T-09.1 are not drawn again, but the board-approval step applies to every provider in this sample. Pass: board approval is held for each contract above the Threshold and the reasons are recorded; or the placement was let under a competed contract or framework on the Contract Register, or under the Provider Selection Regime with its key decisions recorded. Otherwise fail. [CPR-64, CPR-63, CPR-58, metric:$.tests.split_purchases.by_threshold.500000.care_or_education_placement.windows, metric:$.tests.split_purchases.by_threshold.500000.care_or_education_placement.gbp]  
**Evidence to inspect:** Placement contracts with their annual or total value, board approval of the exclusion, case notes, Contract Register or framework entry  
**Sample:** 5 items from `split-purchases.csv`, where threshold = 500000, dominant_tag = care_or_education_placement, largest window_total first, largest 5 payments per item, excluding suppliers and rows already drawn in T-09.1; 14 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P04_-_published.xlsx:1073` | 2026-07-08 | BUPA Care Services | £9,903.62 | Adult Social Care |
| 2 | `Over500_2026_P03_-_published.xlsx:2172` | 2026-06-17 | Oaklands SEN School Berkshire Limited | £20,534.90 | Education (DSG Funded) & Other Education Grants |
| 3 | `Over500_2026_P04_-_published.xlsx:2320` | 2026-07-08 | Affinity Trust Support Ltd | £28,512.00 | Adult Social Care |
| 3 | `Over500_2026_P03_-_published.xlsx:1628` | 2026-06-24 | Affinity Trust Support Ltd | £26,394.66 | Adult Social Care |
| 4 | `Over500_2026_P02_-_published.xlsx:2254` | 2026-05-20 | Phoenix Child Care Limited -The Grange School | £33,799.71 | Education (DSG Funded) & Other Education Grants |
| 4 | `Over500_2026_P02_-_published.xlsx:2244` | 2026-05-19 | Phoenix Child Care Limited -The Grange School | £32,944.66 | Education (DSG Funded) & Other Education Grants |
| 4 | `Over500_2026_P02_-_published.xlsx:2246` | 2026-05-19 | Phoenix Child Care Limited -The Grange School | £32,711.33 | Education (DSG Funded) & Other Education Grants |
| 4 | `Over500_2026_P02_-_published.xlsx:2251` | 2026-05-19 | Phoenix Child Care Limited -The Grange School | £32,711.33 | Education (DSG Funded) & Other Education Grants |
| 4 | `Over500_2026_P02_-_published.xlsx:2248` | 2026-05-19 | Phoenix Child Care Limited -The Grange School | £32,711.33 | Education (DSG Funded) & Other Education Grants |
| 5 | `Over500_2026_P02_-_published.xlsx:823` | 2026-05-13 | RUSKIN MILL TRUST | £179,236.76 | Adult Social Care |
| 5 | `Over500_2026_P02_-_published.xlsx:1822` | 2026-05-13 | RUSKIN MILL TRUST | £151,859.86 | Adult Social Care |
| 5 | `Over500_2026_P03_-_published.xlsx:802` | 2026-06-02 | RUSKIN MILL TRUST | £122,817.82 | Adult Social Care |
| 5 | `Over500_2026_P03_-_published.xlsx:2676` | 2026-06-02 | RUSKIN MILL TRUST | £93,223.17 | Adult Social Care |
| 5 | `Over500_2026_P03_-_published.xlsx:801` | 2026-06-02 | RUSKIN MILL TRUST | £2,959.60 | Adult Social Care |


## R-11: Agency staff bought without a visible contract route [8 (High; Medium - High)]

**Audit objective.** Conclude whether agency staff are bought under a competed contract or a documented Purchasing Scheme call-off with the approvals the Rules require.

**C-11.1. Expected control.** Agency staff above the publication tier are bought under a contract let by the Appendix B route, or under a Purchasing Scheme after advice confirming entitlement and coverage, with the Monitoring Officer's prior written approval where no further competition is held. [CPR-56, CPR-27, CPR-59, CPR-12] Owner: Relevant Service Director; Monitoring Officer (direct call-off).

**T-11.1. Test.** For each sampled agency supplier, identify the contract or framework the sampled payments are made under. Also review the narratives of the unmatched general-procurement top 20 in the analytics for agency staff supply and test up to two on the same basis. Pass: a contract let by the Appendix B route and on the Contract Register; or a Purchasing Scheme call-off with the clause 8.2 advice and, for a direct award, the Monitoring Officer's prior written approval; or an approved waiver (tested in T-07.2). Otherwise fail. [CPR-56, CPR-27, CPR-59, metric:$.tests.off_contract.unmatched_by_tag.agency_staff.suppliers, metric:$.population.tags.agency_staff.gbp]  
**Evidence to inspect:** Contract or framework agreement, call-off record, procurement advice, Monitoring Officer approval  
**Sample:** 1 item from `high-value-suppliers.csv`, where dominant_tag = agency_staff, annualised_estimate ≥ 25000, largest annualised_estimate first, 5 payments per supplier, (only 1 available); 5 transactions

| # | Row ID | Date | Supplier | Amount | Service |
|---|---|---|---|---|---|
| 1 | `Over500_2026_P03_-_published.xlsx:9` | 2026-06-15 | Comensura Ltd | £107,880.99 | Strategy & Governance |
| 1 | `Over500_2026_P02_-_published.xlsx:5` | 2026-05-12 | Comensura Ltd | £104,728.31 | Strategy & Governance |
| 1 | `Over500_2026_P04_-_published.xlsx:19` | 2026-07-31 | Comensura Ltd | £103,047.79 | Strategy & Governance |
| 1 | `Over500_2026_P03_-_published.xlsx:12` | 2026-06-08 | Comensura Ltd | £101,567.70 | Strategy & Governance |
| 1 | `Over500_2026_P04_-_published.xlsx:6` | 2026-07-15 | Comensura Ltd | £100,668.47 | Strategy & Governance |


## Prepared-by-client (PBC) request list

Derived from the test steps above. Each item names the tests that need it.

| # | Risk | Item requested | For tests |
|---|---|---|---|
| 1 | R-01 | Purchase orders, invoices and quotation records for the sampled split-purchase windows | T-01.1, T-01.2 |
| 2 | R-01 | Procurement file or Contract Register entry for any contract covering the sampled windows | T-01.1 |
| 3 | R-02 | Purchase orders, invoices and quotation records for the sampled near-threshold payments | T-02.1 |
| 4 | R-02 | Purchase orders, invoices and quotation records for the sampled one-quote-tier payments | T-02.2 |
| 5 | R-03 | Contract Register extract for the spend window | T-03.1 |
| 6 | R-03 | Signed contract and tender or quotation records for each sampled supplier | T-03.1 |
| 7 | R-03 | Framework or Purchasing Scheme call-off records and the advice obtained, where used | T-03.1 |
| 8 | R-03 | Confirmation of supplier identity for each near-match notice, with the contract behind it | T-03.2 |
| 9 | R-04 | Contract and extension approval, or replacement contract, for each sampled supplier | T-04.1 |
| 10 | R-04 | Invoices for the sampled payments | T-04.1 |
| 11 | R-05 | Contract, award report and all variations for each flagged supplier | T-05.1 |
| 12 | R-05 | Board reports approving variations above the Threshold | T-05.1 |
| 13 | R-06 | Invoices and orders for every payment in the sampled repeat-payment groups | T-06.1 |
| 14 | R-06 | Credit notes or recovery records for any repeat identified | T-06.1 |
| 15 | R-06 | Placement agreements and provider invoices for every payment in the sampled placement repeat-payment groups | T-06.2 |
| 16 | R-07 | Record of waivers and exceptions granted in the spend window | T-07.1 |
| 17 | R-07 | Approval, exception report and board report for each sampled waiver | T-07.1 |
| 18 | R-07 | Waiver or exclusion record for any sampled supplier relying on one | T-07.2 |
| 19 | R-08 | Key Decision record or Executive minute and award report for the contracts behind the sampled windows | T-08.1 |
| 20 | R-08 | Award decision record and procurement report for each sampled supplier's contract | T-08.2 |
| 21 | R-09 | Case-note extracts recording the provider choice for the sampled placements | T-09.1 |
| 22 | R-09 | Placement agreements and any board approval of the exclusion | T-09.1 |
| 23 | R-09 | Board approvals of the exclusion for placement contracts above the Threshold with the sampled providers | T-09.2 |
| 24 | R-11 | Contract or framework call-off record for each sampled agency supplier | T-11.1 |
| 25 | R-11 | Procurement advice and Monitoring Officer approval for any direct call-off | T-11.1 |
