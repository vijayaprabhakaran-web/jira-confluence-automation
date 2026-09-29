---
name: Implement Burndown Model
description: "Implement and validate the pure sprint burndown data model for issue counts and story points."
user-invocable: true
---

Use this workflow for the burndown data-model task in `backlog.md`.

## Scope

- Read `project_spec.md`, `DATA_CONTRACT.md`, `data_contract.py`, `data_source.py`, and the selected backlog item before editing.
- Implement the model in a focused root-level `burndown.py`; keep it independent of Streamlit and data-source adapters.
- Add focused tests in `tests/test_burndown.py`. Do not change the shared data contract unless the required output cannot be represented without a contract change.
- Do not build the chart or dashboard view as part of this task.

## Behavior

- Accept a `SprintDataset` and an optional `as_of` date; default `as_of` to the current date and inject it in tests.
- Return one row for every calendar date from the actual sprint start through the actual sprint end, inclusive.
- Produce planned remaining issue-count and story-point series using a linear baseline from sprint start to zero at sprint end. Use issues with `created_at` on or before the sprint start as the baseline; the shared contract uses `created_at` to identify scope added after the sprint starts.
- Produce actual remaining series using issue creation and resolution dates. At each date, include issues created by that date and not resolved by the end of that date. Actual values after `as_of` must be missing, not projected.
- Count unestimated issues in issue-count series and exclude them from story-point totals. Preserve null estimates; never coerce them to zero.
- Treat a null `created_at` conservatively as present from sprint start, and document this assumption in code or the function documentation. A null `resolved_at` means the issue remains unresolved, per the shared contract.
- Raise a clear `ValueError` when sprint start or end is missing, or when the end is not after the start.

## Output

Return a pandas DataFrame with exactly these columns, in this order:

1. `date`
2. `planned_remaining_issues`
3. `actual_remaining_issues`
4. `planned_remaining_story_points`
5. `actual_remaining_story_points`

Document that planned story points use current issue estimates because the contract does not retain estimate history.

## Validation

- Add tests for inclusive date boundaries, linear planned values, scope added after sprint start, resolution-date behavior, unestimated issues, null dates, invalid sprint ranges, and missing actuals after `as_of`.
- Run the focused test file with `python -m pytest tests/test_burndown.py` when the project's test runner is available. If it is not installed or configured, report that limitation rather than installing dependencies without authorization.
- Do not mark the backlog item complete unless the focused tests pass.

## Response

Report `Implemented`, `Files`, `Validation`, and `Remaining`. State the DataFrame columns and any documented assumptions; do not claim actual historical values that cannot be derived from the available dates.