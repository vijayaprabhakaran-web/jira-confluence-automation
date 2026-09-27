# Shared Data Contract

The sample provider and future Jira adapter use `SprintDataset` from `data_contract.py`.
It contains one sprint record and two pandas tables. The table column names below are
required; a value may be null only where explicitly indicated.

## Sprint

| Field | Type | Nullable | Meaning |
| --- | --- | --- | --- |
| `sprint_id` | string | no | Stable sprint identifier |
| `name` | string | no | Display name |
| `start_date` | date | yes | Actual sprint start date |
| `end_date` | date | yes | Actual sprint end date |
| `capacity_points` | number | yes | Team capacity in story points |

## Issues table

| Field | Type | Nullable | Meaning |
| --- | --- | --- | --- |
| `issue_key` | string | no | Issue identifier, such as `PROJ-101` |
| `summary` | string | no | Issue summary |
| `issue_type` | string | no | Source issue type, such as Story, Task, or Bug |
| `status` | status category | no | Normalized category defined below |
| `assignee` | string | yes | Current assignee display name |
| `story_points` | number | yes | Estimate; null means unestimated, not zero |
| `due_date` | date | yes | Issue due date |
| `created_at` | date | yes | Creation date, used to identify scope added after sprint start |
| `resolved_at` | date | yes | Resolution date; null means unresolved |
| `jira_url` | URL string | yes | Link to the source issue when available |

The normalized `status` categories are `To Do`, `In Progress`, `Done`, and `Blocked`.
Adapters retain source workflow statuses separately when mapping is introduced; calculations
consume only the normalized category. A blocked issue is not considered complete unless its
normalized category is `Done`.

## History table

| Field | Type | Nullable | Meaning |
| --- | --- | --- | --- |
| `sprint_id` | string | no | Stable historical sprint identifier |
| `name` | string | no | Display name |
| `start_date` | date | yes | Actual sprint start date |
| `end_date` | date | yes | Actual sprint end date |
| `committed_points` | number | yes | Story points committed at sprint start |
| `completed_points` | number | yes | Story points completed in the sprint |

Dates are calendar dates, not timestamps. Numeric values must be finite and non-negative when
present. Missing estimates remain null and must not be coerced to zero. Empty tables must still
provide the required columns.