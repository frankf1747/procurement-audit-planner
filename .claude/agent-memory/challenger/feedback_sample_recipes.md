---
name: sample-recipe-checks
description: How to find weak samples in the audit program by reading recipe clauses (exclusions, order key, sample unit) against analytics.json top20 lists
metadata:
  type: feedback
---

Read each test's sample recipe clause by clause before reading its table. The weak points tend to be in the recipe, not in the rows drawn.

- **"excluding suppliers already drawn in T-x"**: check what T-x actually tests. An exclusion can move the highest-value suppliers out of the test that matters (for example award approval) into one that checks something else (for example contract coverage).
- **Order key**: compare a ratio-ordered or count-ordered sample with the flagged list's `top20` in analytics.json. If the flagged population is barely larger than the sample size, items left out at the tail can be the largest £ exposures. Ask for the sample to take all flagged items.
- **Sample unit**: tests built on groups or windows (duplicates, split windows) sometimes sample *transactions*. Count the distinct groups and suppliers actually drawn against the population group count.
- **Tag filters**: a filter on dominant_tag misses suppliers whose names signal another theme (for example staffing suppliers tagged general procurement). Scan the unmatched/top20 lists by name.
- **Cross-test overlap**: the same row IDs can appear in several tests, which inflates the headline count of sampled transactions.

- **Phrase asks the builder can execute**: the planner's sample builder works only by column filter, order key, exclusion and per-item count. It declines asks that name a supplier or set a per-supplier cap. Phrase those asks as a column filter, or as a fieldwork step in the test text (for example "review list X and apply this test to up to N").
- **Exclusions are by supplier**: an "exclude rows drawn in T-x" ask removes every payment from those suppliers, not just the shared rows. Overlap between tests is usually cheap, so don't spend a challenge on it.
- **Public-body payees**: inter-authority rows with a "Private Contractors" narrative stay in the population, so check samples for council or NHS payees and ask for a pass route that fits them.

**Why:** these produced the most actionable round-one challenges; the planner can fix each by editing one recipe.
**How to apply:** for every test, write down the filter, order key, exclusions and unit, then check each against the matching analytics.json path before drafting a challenge. See also [[coverage-reason-checks]].
