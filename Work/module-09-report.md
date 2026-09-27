# Module 09 Completion Report

## Tracked Files
```
backlog.md
```

## Backlog Commit History
```
13a6f68 (HEAD -> master) Add implementation backlog
```

## backlog.md Contents
# Implementation Backlog

**Delivery priority:** Ship a usable sample-data MVP first. Add Jira Cloud read integration after the core dashboard is working. Add focused tests alongside each feature, then complete cross-cutting validation in the Testing phase.

## Setup

- [x] Verify the project virtual environment and install declared runtime dependencies (`streamlit` and `pandas`).
- [x] Add a sample-data provider with sprint metadata, 18 representative issues, and historical sprint velocity data in `data_source.py`.
- [x] Define and document the shared sprint, issue, and history data contract, including normalized status values and nullable estimates/dates.
- [ ] Add configurable mappings from source workflow statuses to `To Do`, `In Progress`, `Done`, and `Blocked` without embedding mapping decisions in calculations.
- [ ] Establish the application and test folder structure, including a Streamlit entry point and a test runner configuration.
- [ ] Confirm dependency constraints and add test-only dependencies needed by the chosen test runner.

## Core Features

- [ ] Implement date-aware sprint calculations using each sprint's actual start and end dates, including elapsed and remaining days.
- [ ] Calculate issue-count completion and estimated story-point completion separately; exclude unestimated issues from point totals and report them explicitly.
- [ ] Calculate committed, completed, remaining, and unestimated work, with clear handling for zero estimates and missing sprint data.
- [ ] Build a burndown data model for planned and actual remaining issue count and story points across the selected sprint's dates.
- [ ] Calculate historical completed-point velocity and a completion forecast; report when history or estimates are insufficient for a reliable forecast.
- [ ] Derive blocked, overdue, scope-added, and capacity-risk signals from issue and sprint data; return explanatory states when a signal cannot be calculated.
- [ ] Add focused unit tests for progress, date boundaries, burndown, forecast, unestimated issues, and each risk rule as the calculations are implemented.
- [ ] Build the Streamlit sample-data dashboard with a sprint selector and summary metrics for sprint dates, progress, remaining work, and health.
- [ ] Add progress views for burndown, planned-versus-actual work, and historical velocity, with issue-count and story-point views where the data supports them.
- [ ] Add risk summaries and corresponding issue lists for blocked, overdue, scope changes, and capacity pressure.
- [ ] Add expandable issue details for key, summary, type, source and normalized status, assignee, estimate, due date, risk indicators, and available Jira link.
- [ ] Add filters for normalized status, issue type, assignee, and risk signal; make summary metrics and chart selections filter the relevant issue list.
- [ ] Add visible refresh behavior and a last-refreshed timestamp; refresh sample data automatically when the app opens and provide a manual refresh control.
- [ ] Make status and health meaning clear through text and icon/shape cues rather than color alone; label controls and charts for keyboard and assistive-technology use.
- [ ] Verify the layout remains readable and controls do not overlap at desktop and tablet widths.
- [ ] Keep the first-run experience complete using sample data and requiring no Jira credentials.

## Integration

- [ ] Implement a Jira Cloud read adapter behind the shared sprint, issue, and history data contract; keep dashboard calculations independent of the adapter.
- [ ] Read Jira connection settings and API credentials from local environment variables, with no secrets committed, displayed, or written to logs.
- [ ] Fetch the selected board's current and historical sprints and the issues needed for dashboard calculations through Jira REST API endpoints.
- [ ] Map Jira sprint dates, issue types, statuses, assignees, story points, due dates, creation/resolution dates, and issue URLs into the shared contract.
- [ ] Support configurable Jira workflow-status mappings without changes to calculation code.
- [ ] Handle pagination, timeouts, API errors, missing fields, and rate limits with actionable user-facing messages that do not expose credentials.
- [ ] Connect manual refresh and app-open refresh to the configured source while preserving sample-data operation when Jira integration is not configured.
- [ ] Add adapter tests with mocked Jira responses, including pagination, incomplete data, authentication failure, and safe error handling.

## Testing

- [ ] Run the full unit suite against calculation edge cases, including sprint boundary dates, zero-point issues, missing dates, empty history, and incomplete work.
- [ ] Run data-contract tests against both sample data and mocked Jira data to ensure both sources produce equivalent normalized fields.
- [ ] Add an app smoke test confirming the dashboard starts and renders with sample data and no Jira credentials.
- [ ] Exercise the main workflows: select a sprint, change filters, select a metric or chart segment, expand issue details, and refresh.
- [ ] Validate acceptance criteria for progress, unestimated work, actual-date burndown, forecast availability, and all risk filters.
- [ ] Check keyboard-only operation, accessible labels, contrast, focus visibility, and non-color status cues against WCAG 2.1 AA-oriented requirements.
- [ ] Check desktop and tablet layouts for readable content, usable controls, and absence of overlap.
- [ ] Run the documented test, lint, and type/static-check commands and resolve project-related failures.

## Documentation

- [ ] Write a project README with prerequisites, virtual-environment setup, install commands, and instructions to launch the Streamlit app.
- [ ] Document the shared data contract, normalized statuses, sample-data scenarios, and calculation assumptions.
- [ ] Document Jira Cloud configuration, required environment variables, API permissions, local secret handling, and how to run without Jira.
- [ ] Document how to run tests and perform the desktop/tablet and accessibility checks.
- [ ] Record prototype limitations and out-of-scope behavior, including no write-back, no OAuth, no real-time streaming, and one-team scope.
