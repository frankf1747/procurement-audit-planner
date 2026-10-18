---
name: extract-rules
description: Extract every testable rule from data/contract-rules.pdf (West Berkshire Council Contract Rules) into outputs/rules.json, with clause, page, thresholds as printed, required action, approver, evidence source and a verbatim quote checked against the PDF page. Use when the user runs /extract-rules or asks to (re)build rules.json.
---

# extract-rules

Turn the council's Contract Rules PDF into `outputs/rules.json`: a list of
testable rules that later steps depend on. The spend-analyst takes every £
threshold from this file, the risk register cites rules by `rule_id`, and QA
re-checks every quote against the PDF. So every figure and every quote here
must be exactly as printed, and nothing may be filled in from memory.

Input: `data/contract-rules.pdf` (read-only). Output: `outputs/rules.json`.
Verifier: `.claude/skills/extract-rules/verify_quotes.py` (next to this file).

If the PDF is missing or `pdftotext` is not installed, stop and report. Do not
work from memory of what council contract rules usually say.

## 1. Read the document the way it is laid out

Extract both views, one page at a time so every quote has a page:

```bash
mkdir -p /tmp/extract-rules
n=$(pdfinfo data/contract-rules.pdf | awk '/^Pages:/{print $2}')
for p in $(seq 1 "$n"); do
  pdftotext -f $p -l $p        data/contract-rules.pdf /tmp/extract-rules/p$p.txt
  pdftotext -f $p -l $p -layout data/contract-rules.pdf /tmp/extract-rules/p$p.layout.txt
done
```

Read every page. What this document looks like (15 pages, Word export):

- **Body, pages 1–10**: numbered sections 1–11. Clause numbers go up to four
  levels (`4.1.3.1`, `10.7.9.1`). Some lines that carry a number are really
  headings (`6.23 Evaluations of Quotes and Tenders`). Some sections have
  unnumbered sub-headings (`Preliminaries`, `Advertising`, `Contract Value &
  Aggregation`, `Indemnities`, `Sealing`, ...).
- **Appendix A, page 11**: delegated authority to award, by Total Contract
  Value. Four rows, no row labels: up to the Threshold; above the Threshold
  and less than £500,000; above £500,000 and less than £2.5million;
  £2.5million or more.
- **Appendix B, pages 12–13**: financial thresholds and mandatory processes.
  Rows `A`, `B1`, `B2`, `C`, `D`, then footnotes `*`, `**`, `***`, `****` on
  page 13.
- **Appendix C, pages 14–15**: exclusions from competition. Rows `A`–`F`, then
  a closing sentence on page 15.
- **Page footer**: every page ends with `$3inav0bz.docx` and the page number.
  The footer number equals the PDF page number. Never quote the footer.
- **Bullets** come out as the private-use glyph U+F0B7. Never put it in a quote.

Use the **plain** text for quotes: it keeps each table cell's lines together.
Use the **-layout** text to see which cells sit on the same table row (in
plain text, the cells of one row follow one another, column by column).

## 2. Clause identifiers

- Body: the printed number, e.g. `"6.16"`, `"7.4.2"`, `"10.7.9.1"`.
- Appendix rows: `"App A row 1"` to `"App A row 4"` (top to bottom),
  `"App B row A"`, `"App B row B1"`, `"App B row B2"`, `"App B row C"`,
  `"App B row D"`, `"App B notes"` (footnotes), `"App C row A"` to
  `"App C row F"`, `"App C closing"` (the closing sentence on page 15).

## 3. Classify every clause

Walk the document clause by clause. Each numbered clause and each appendix row
goes into exactly one place:

- **`rules`**: it is testable. Something an auditor could check against
  records: a £ threshold that triggers a procedure, a required action, a
  required approval, or the ban on splitting. One rule per testable
  requirement. A clause with two separate requirements (for example a
  threshold and a separate approval) gives two rules.
- **`excluded`**: anything else, with a one-line reason. Typical reasons:
  definition or background only; legal citation; heading only; guidance
  ("should consider", "may be sought"); not about procurement (sealing of
  mortgages, instructing Counsel); lead-in sentence whose testable content
  sits in its sub-clauses; untestable from spend and contract records.

A parent clause whose sub-clauses carry the requirement (for example `7.4`,
with the content in `7.4.1`–`7.4.3`) is listed itself, in `excluded` with
the reason "lead-in to 7.4.1–7.4.3", or as a rule if it is testable on its
own. The verifier checks that every clause number in the PDF appears in
`rules` or `excluded`, unless an ancestor clause is excluded as a whole
(an excluded `1.3` covers its bullet list; an excluded `11.10` covers
`11.10.1`–`11.10.3`). A clause must not appear in both lists.

When unsure whether a clause is testable, exclude it and say why. Never guess.

## 4. Rule fields

```json
{
  "rule_id": "CPR-07",
  "clause": "App B row B1",
  "page": 12,
  "type": "threshold",
  "scope": "goods-services",
  "condition": "goods and services contract, total value exclusive of VAT £25,000 or more and less than the Threshold",
  "threshold_low": 25000,
  "threshold_low_inclusive": true,
  "threshold_low_ref": null,
  "threshold_high": null,
  "threshold_high_inclusive": false,
  "threshold_high_ref": "threshold_goods_services",
  "required_action": "send invitations to quote via the Procurement Portal to at least three appropriate sources (at least one SME or VCSE and one local supplier where appropriate and possible); publish a contract notice on the CDP",
  "approver": null,
  "evidence_source": "Procurement Portal RFQ record with invitee list; CDP contract notice",
  "verbatim_quote": "Invitations to quote must be sent via the Procurement Portal to at least three appropriate sources, … A contract notice must be published on the CDP"
}
```

- `rule_id`: `CPR-01`, `CPR-02`, ... in document order, no gaps.
- `clause`: as in section 2. `page`: the PDF page the quote is on (an
  integer). If the quote crosses a page break, a list of consecutive pages,
  e.g. `[4, 5]`.
- `type`, one of:
  - `threshold`: a £ value triggers a procedure (App B rows, 6.19, 11.11, 5.2).
  - `approver`: a named role or body must approve or decide (App A rows,
    7.4.x, App C rows, 11.4.2).
  - `anti-avoidance`: the rule against splitting or disaggregating a
    contract to avoid the rules (6.16). There must be at least one.
  - `procedure`: a required action with no £ trigger and no approver
    (written evidence of all purchases, award notified to the Contract
    Register, records kept three years).
- `scope`: `all`, `goods-services` or `works-concession-light-touch`, as
  the clause states. Default `all` when the clause names no contract type.
- `condition`: one line in plain words: when the rule applies.
- Thresholds, **as printed**:
  - `threshold_low` / `threshold_high`: GBP as a number, exactly as printed
    (`£500,000` → `500000`, `£2.5million` → `2500000`). Use integers. Only
    where the PDF prints pence (7.2's `£24,999.99`) keep the printed value
    (`24999.99`) and add a `notes` entry; do not round.
  - `_inclusive`: `true` for "or more", "up to", "at least"; `false` for
    "above", "more than", "exceeds", "over", "less than". `null` only when
    that side has neither a value nor a reference.
  - `_ref`: when the bound is a named threshold with no figure ("the
    Threshold", "the relevant Threshold"), set the value to `null` and put a
    `parameters` key here. A bound has a value or a ref, never both.
  - Open-ended side (no upper limit, no lower limit): value, ref and
    inclusive all `null`.
- `required_action`: what must be done, in short imperative words.
- `approver`: the role(s) or body that must approve or decide, as printed
  ("S151 Officer", "relevant board"). `null` when the rule names none.
  Required for `type: "approver"`.
- `evidence_source`: the record an auditor would ask the council for to
  test the rule (portal RFQ log, CDP notice, exception report, decision
  record, board minute, contract register entry).
- `verbatim_quote`: copied character for character from the plain text of
  the stated page, without the clause number. Keep the PDF's own spelling,
  capitals and punctuation (curly apostrophes may be typed straight). Line
  breaks become single spaces. Where one rule needs words from separate
  table cells, join the pieces with ` … ` (space, ellipsis, space); each
  piece is checked separately and must appear in order on the page. Each
  piece is at least 15 characters. Every £ figure in the threshold fields
  must appear in the quote.

## 5. Parameters: named thresholds with no figure

The PDF names thresholds it never prints: clause 1.4 defines "Threshold" as
the figures in the Procurement Legislation published on the intranet, and
the App B `***` footnote says there are three: works and concession
contracts; goods and services; light touch contracts. Declare each one in
the top-level `parameters` object with a **null** value:

```json
"parameters": {
  "threshold_goods_services": {
    "value": null,
    "printed_as": "the Threshold (Goods and Services)",
    "defined_in": ["1.4", "App B notes"],
    "note": "Figure not printed in the PDF; published on the Procurement intranet page. To be supplied by the auditor."
  }
}
```

Do not fill in a value from memory or from the legislation, even if you
know the current figure. An auditor supplies it later by setting `value`
together with `supplied_by` and `supplied_on`. The verifier refuses a
non-null value without both. When a clause says "the relevant Threshold"
without naming a contract type, use the parameter that matches the rule's
`scope`. If scope is `all`, add a separate parameter
`threshold_relevant` (null, with a note that the applicable figure depends
on contract type). Every `_ref` must name a declared parameter.

## 6. Notes: contradictions and drafting gaps

Record in a top-level `notes` list anything in the PDF that is contradictory,
incomplete or ambiguous, so the auditor sees it. Do not resolve it yourself.
Each note has `clauses` (list), `pages` (list) and `issue` (one or two
sentences). Things to look for in this document include:

- gaps or overlaps between bands (for example exactly £500,000 in App A and
  App B rows B2/C; values of £1,000 and below in App B row A);
- the same value written differently (7.2 "more than £24,999.99" against App
  B "£25,000 or more");
- who may grant an exception (7.2.2 against 7.3);
- placeholders left in the text ("Part []", "Parts [] (Call-In) and []
  (Forward Plan)");
- a footnote marker defined but never used in the table (`***`), or used
  but never defined;
- a numbered line that is only a heading (6.23);
- wording that names the wrong document (App C row E asks for an
  "extension report" for a variation).

Only record what the text actually shows; each note must point to clauses
and pages that exist.

## 7. Output file

`outputs/rules.json` is one JSON object:

```json
{
  "source": {
    "file": "data/contract-rules.pdf",
    "pages": 15,
    "sha256": "<sha256 of the PDF>",
    "title": "Contract Rules (Part [] of the Constitution)",
    "extracted_with": "pdftotext (poppler), plain and -layout, per page"
  },
  "parameters": { ... },
  "rules": [ ... ],
  "excluded": [ { "clause": "1.1", "page": 1, "reason": "legal citation of s.135 LGA 1972; no requirement" } ],
  "notes": [ { "clauses": ["7.2", "App B row A"], "pages": [6, 12], "issue": "..." } ]
}
```

Compute the hash with `shasum -a 256 data/contract-rules.pdf` (do not type
it from memory).

## 8. Verify, fix, repeat

Run the verifier, then fix every failure it reports and run it again until
it prints `ALL CHECKS PASSED`:

```bash
.venv/bin/python .claude/skills/extract-rules/verify_quotes.py outputs/rules.json data/contract-rules.pdf
```

Fix a failing quote by copying it again from the page text, never by
loosening the verifier. If a rule cannot be quoted exactly, move its clause
to `excluded` with the reason.

## 9. Report

When the verifier passes, report in under 200 words: the number of rules by
type, the number of excluded clauses, every parameter (all null), the
anti-avoidance rule ID, the notes in one line each, and the verifier's
final line. Do not repeat the rules themselves.
