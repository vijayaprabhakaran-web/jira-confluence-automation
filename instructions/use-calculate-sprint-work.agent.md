---
name: Use Calculate Sprint Work
description: "Use the sprint-work CLI to summarize supplied committed, completed, remaining, and unestimated work."
user-invocable: true
---
- Use this instruction when the user asks to summarize sprint work from already-aggregated sprint totals.
- Run `python tools/calculate_sprint_work.py` from the project root.
- Pass only known values using `--committed-points`, `--completed-points`, and `--unestimated-issues`.
  + `--committed-points` is the non-negative story-point total committed at sprint start.
  + `--completed-points` is the non-negative story-point total completed in the sprint.
  + `--unestimated-issues` is the non-negative count of in-scope issues whose estimate is missing; pass `0` when none are unestimated.
- Treat zero as a known value, not as missing data. Omit a flag only when its value is unknown; the tool will report that metric as unavailable.
- Remaining committed work is `max(committed points - completed points, 0)` and is available only when both corresponding inputs are provided.
- If no metric is available, the tool prints that sprint work data is unavailable; do not substitute guessed values.
- Do not claim the tool aggregates issue records or integrates with Jira; it summarizes the numeric totals supplied by the user.
- Run the command and present its output labels and values as printed: `Committed work`, `Completed work`, `Remaining committed work`, and `Unestimated work`.
- If the tool rejects an input, explain which value must be corrected; do not report a result from invalid inputs.