# Module 08 Completion Report

## Tracked Files
.gitignore
README.md
calculator.py
calculator/operations.py
main.py
project_spec.md

## Spec Commit History
54589e9 (HEAD -> master) Add Jira dashboard requirements specification

## project_spec.md Contents
# Jira Sprint Progress Dashboard

## 1. Product Goal

Build an internal, desktop-first Streamlit dashboard that helps a scrum master or engineering manager understand the health and progress of one team's current or historical sprint.

The first release uses realistic sample data and keeps the data model ready for a future Jira Cloud integration.

## 2. Audience

- Primary users: scrum masters and engineering managers
- Data classification: internal team data only
- Primary device: desktop, with responsive tablet support

## 3. Scope

### In scope

- One team
- Current sprint and sprint history
- Actual sprint start and end dates, without assuming a fixed sprint duration
- Stories, tasks, and bugs
- Issue count and story points
- Unestimated issues shown separately from estimated work
- Burndown chart
- Historical-velocity completion forecast
- Configurable mapping from Jira statuses into To Do, In Progress, Done, and Blocked
- Risk signals for blocked issues, overdue work, scope changes, and capacity versus committed work
- Expandable issue details
- Dashboard filtering by the selected metric or chart segment
- Links from issues back to Jira when integration is available
- Automatic refresh when the app opens and a manual refresh control
- WCAG 2.1 AA-oriented accessibility, including keyboard-friendly controls, readable contrast, clear labels, and indicators that do not rely on color alone

### Out of scope for the prototype

- Writing changes back to Jira
- Real-time streaming updates
- Multi-team comparisons
- Jira plugin or embedded Jira deployment
- OAuth user sign-in
- Customer or external confidential data

## 4. Dashboard Experience

The visual direction is neutral and professional, with a balanced layout: prominent sprint-health metrics and charts, followed by expandable operational detail.

The landing view should answer these questions quickly:

1. How much of the sprint's committed work is complete?
2. Is progress tracking against the sprint timeline?
3. What risks need attention now?
4. Which issues are contributing to the risk?
5. How does this sprint compare with historical team velocity?

## 5. Required Views and Components

### Sprint summary

- Sprint name
- Start date, end date, and days elapsed/remaining
- Completion percentage by issue count
- Completion percentage by story points
- Committed, completed, remaining, and unestimated work
- Current sprint health indicator with text and icon/shape support

### Progress analysis

- Burndown chart using sprint dates
- Planned remaining work versus actual remaining work
- Issue-count and story-point views where the data supports both
- Historical velocity reference
- Forecast based on completed historical sprint velocity

### Risk analysis

- Blocked issue count and list
- Overdue issue count and list
- Scope added after sprint start
- Committed capacity compared with completed and remaining work
- Clear explanation when data is missing or a risk cannot be calculated

### Issue detail

- Issue key and summary
- Issue type
- Status and normalized status category
- Assignee
- Story points, when present
- Due date, when present
- Blocked/overdue/scope-change indicators
- Jira URL when available

## 6. Interaction Requirements

- Allow selection of a sprint from the available sprint history.
- Allow filtering by normalized status, issue type, assignee, and risk signal.
- Clicking a metric or chart segment should filter the relevant issue list.
- Allow users to expand issue details without leaving the dashboard.
- Open the corresponding Jira issue in a new browser tab when a Jira URL is available.
- Provide a visible refresh action and a last-refreshed timestamp.
- Preserve a usable layout on tablet widths without overlapping content.

## 7. Data and Integration

### Prototype data

- Use realistic sample data for a medium sprint of 11-30 issues.
- Include a mix of stories, tasks, and bugs.
- Include some unestimated issues.
- Include examples of blocked work, overdue work, scope changes, and capacity pressure.
- Include enough historical sprint data to calculate a meaningful velocity forecast.

### Future Jira Cloud integration

- Read Jira Cloud sprint and issue data through the REST API.
- Use a locally configured API token supplied through environment variables.
- Never commit or display credentials in source code, sample data, or logs.
- Keep the Jira adapter separate from dashboard calculations so sample data and live data use the same contract.
- Support configurable mapping of Jira workflow statuses into the normalized categories To Do, In Progress, Done, and Blocked.

## 8. Calculation Rules

- Sprint progress is calculated from the sprint's actual start and end dates.
- Estimated progress uses story points only for issues with valid points.
- Issue-count progress includes all in-scope issues.
- Unestimated issues are reported separately and are excluded from story-point totals.
- An issue is overdue when it is incomplete and its due date is before the current dashboard date.
- Scope change means an issue added after the sprint start date.
- Historical velocity is based on completed story points from prior comparable sprints.
- Forecasts must identify when insufficient history or missing estimates prevents a reliable result.

## 9. Acceptance Criteria

- A user can open the app and see a complete sample sprint dashboard without Jira credentials.
- The dashboard shows both issue-count and story-point progress.
- Unestimated work is visible and does not inflate story-point progress.
- The burndown uses the selected sprint's actual dates.
- Risk signals are visible for blocked, overdue, scope-changed, and capacity-risk work.
- Selecting a risk signal filters the issue list to matching issues.
- A historical-velocity forecast is shown when sufficient historical sample data exists.
- Status mappings can be changed without changing calculation code.
- Refresh behavior and the last-refreshed time are visible.
- Keyboard users can operate the main controls, and status meaning is not conveyed by color alone.
- The layout remains readable at desktop and tablet widths.
- No Jira credential is required for the prototype, and no credential is stored in the repository.

## 10. Suggested Implementation Order

1. Define the sample-data and normalized-status contracts.
2. Implement calculation functions with tests for progress, burndown, risks, and forecast behavior.
3. Build the Streamlit dashboard using sample data.
4. Add filtering, drill-down, refresh state, and Jira links.
5. Add the Jira Cloud adapter behind the same data contract.
6. Validate accessibility and desktop/tablet layouts.