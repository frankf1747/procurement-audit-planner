---
name: running-checks
description: How run_checks.py behaves for QA - exit codes, and how trace reacts to challenges.md missing or open while the challenger is still working
metadata:
  type: reference
---

- Run from project root: `.venv/bin/python scripts/checks/run_checks.py`. No flags needed; it prints each check's SUMMARY line, then a results table and a VERDICT line. Exit 0 = all pass, exit 1 = BLOCKED.
- The printed table can be copied verbatim into `outputs/review.md`.
- Trace fails with `challenges.md missing` before the challenger writes the file, and with `challenges still open: #...` while rows are open. Both belong to the challenger, not the planner. Do not send them to the planner as fixes; they clear once the challenger sends CHALLENGER DONE.
- Items for the auditor are listed under "## For the auditor at sign-off" at the end of `outputs/challenges.md`. Copy them into review.md.
- Agent teams transport may be unavailable; the lead then relays messages and wants protocol messages under a MESSAGES heading at the end of the report.
