# risk-assessor memory (method lessons only; never evidence, never ratings)

- **Skill example rule IDs are illustrative, not the real ones** (2026-10-17). Why: the SKILL.md example cites a rule ID for anti-avoidance that is a different rule in rules.json. Apply: look up rule IDs by `clause` / `type` in the current rules.json every run (e.g. find `"type": "anti-avoidance"`).
- **impact_scale is ordered from the highest score down** (2026-10-17). Why: `[history:$.scoring_method.impact_scale[N]]` index is not the score. Apply: check `impact_scale[N].score` before citing; entries carry `evidence`, so the JSONPath citation resolves.
- **Not every test has a general-procurement split** (2026-10-17). threshold_clustering gives a per-tag band count but the comparator only across all tags; spend_vs_award has no tag split at all. Apply: say so in the justification instead of inventing a GP comparator; cite `by_tag.general_procurement.rows` for the band.
- **Dotted keys** (`24999.99`, `baseline_0.5T_to_1.5T`) cannot be addressed; use the `25000` key for the publication tier (2026-10-17).
- **Typed-figure check catches 3+ digit numbers, including years and thresholds in prose** (2026-10-17). Apply: write "the publication tier" or a `{{$...threshold}}` placeholder; never write a year or £ amount.
- **Repeat uplift needs an adverse audit on the same theme**; check each adverse audit's title/relevance against the theme and, if not the same, cite it in the justification with "no repeat uplift" rather than forcing one (2026-10-17).
