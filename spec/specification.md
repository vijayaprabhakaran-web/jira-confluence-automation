# Feature Specification: Jira Sprint Progress Dashboard

**Feature Branch**: `001-jira-sprint-dashboard`
**Created**: 2026-10-05
**Status**: Draft
**Input**: Existing `project_spec.md`, `DATA_CONTRACT.md`, and approved stack in `spec/constitution.md`.

## Summary

**Project name**: Jira Sprint Progress Dashboard

**Purpose**: Help an internal team understand current and historical sprint progress, surface delivery risks, and assess likely completion using historical velocity.

**Primary users**: Scrum masters and engineering managers responsible for one team's sprint.

**Data classification**: Internal team data.

This specification is authoritative for the React, Node.js, Express, and PostgreSQL prototype. The older `project_spec.md` and pandas-based `DATA_CONTRACT.md` are historical inputs, not implementation contracts for this prototype. The prototype is a local, single-team dashboard backed by seeded sample data. Live Jira and Confluence integrations are out of scope; a later Jira phase must remain read-only unless separately authorized.

## User Scenarios & Testing

### User Story 1 - Review sprint health (Priority: P1)

As a scrum master or engineering manager, I want to open the dashboard and select a current or historical sprint so I can quickly understand its overall status.

**Why this priority**: Sprint health is the dashboard's primary purpose and the starting point for all other analysis.

**Independent Test**: Start the application with the sample provider and open a sample sprint without configuring Jira credentials.

**Acceptance Scenarios**:

1. **Given** a valid sample sprint is available, **When** the user opens the dashboard, **Then** the sprint name, actual dates when available, elapsed and remaining days when calculable, issue-count completion, story-point completion, committed work, completed work, remaining estimated work, and unestimated work are shown.
2. **Given** more than one sprint is available, **When** the user selects a different sprint, **Then** all summary values and issue details update to the selected sprint.
3. **Given** the selected sprint has no issues, **When** the summary is rendered, **Then** the dashboard explains that progress cannot be calculated rather than presenting a misleading percentage.

### User Story 2 - Understand progress over time (Priority: P1)

As a scrum master or engineering manager, I want to compare planned and actual remaining work over the selected sprint's real dates so I can see whether progress is tracking to plan.

**Why this priority**: The timeline and burndown answer whether the sprint is progressing as expected.

**Independent Test**: Load a fixture with dated sprint boundaries, completed issues, and estimates; verify chart values for both issue count and story points.

**Acceptance Scenarios**:

1. **Given** the sprint has valid start and end dates, **When** the user views progress analysis, **Then** planned and actual remaining work are plotted against those dates without assuming a fixed sprint length.
2. **Given** issue estimates are present, **When** the user selects the story-point view, **Then** unestimated issues are excluded from point totals and are reported separately.
3. **Given** the chart or a metric segment is selected, **When** the selection is applied, **Then** the related issue list is filtered to the matching work.
4. **Given** the sprint dates or required history are missing, **When** a timeline or forecast cannot be calculated, **Then** the dashboard explains which data is missing.

### User Story 3 - Identify and inspect sprint risks (Priority: P1)

As a scrum master or engineering manager, I want to see blocked, overdue, scope-changed, and capacity-risk work and filter to the affected issues so I can decide what needs attention.

**Why this priority**: Risk signals are the main operational action the dashboard supports.

**Independent Test**: Use a sample sprint containing at least one example of each risk type and verify the counts, issue lists, and filters.

**Acceptance Scenarios**:

1. **Given** a sprint contains blocked, overdue, or post-start-added issues, **When** the risk panel is displayed, **Then** each calculable risk count and its matching issues are visible.
2. **Given** the user selects a risk signal, **When** the issue list updates, **Then** every displayed issue matches that signal and unrelated issues are excluded.
3. **Given** capacity, estimates, dates, or other required data is missing, **When** a risk cannot be calculated, **Then** the dashboard states why instead of treating missing data as zero.

### User Story 4 - Compare against historical velocity (Priority: P2)

As a scrum master or engineering manager, I want a completion forecast based on prior comparable sprints so I can set expectations using the team's observed delivery.

**Why this priority**: A forecast adds planning context after current-sprint health and risk are visible.

**Independent Test**: Load completed historical sprints with valid completed-point totals and verify that a forecast is shown; remove sufficient history and verify an explanation is shown instead.

**Acceptance Scenarios**:

1. **Given** sufficient comparable historical sprint data exists, **When** the selected sprint is analyzed, **Then** the dashboard displays the historical velocity reference and a forecast.
2. **Given** history or completed-point data is insufficient, **When** a reliable forecast is not possible, **Then** the dashboard clearly reports that limitation.

### User Story 5 - Inspect an issue (Priority: P2)

As a dashboard user, I want to expand an issue's details and see its source URL when supplied so I can identify the related record without losing dashboard context.

**Why this priority**: Risk and progress summaries are more useful when users can identify the work behind them.

**Independent Test**: Select an issue with complete and partial optional fields, expand it, and activate its Jira link when present.

**Acceptance Scenarios**:

1. **Given** an issue is in the filtered list, **When** the user expands it, **Then** its key, summary, type, normalized status, assignee, story points when present, due date when present, risk indicators, and Jira URL when available are shown.
2. **Given** an issue has a Jira URL in the prototype, **When** its details are shown, **Then** the URL is rendered as escaped, non-clickable text. External navigation is out of scope for this prototype.
3. **Given** optional issue data is absent, **When** details are shown, **Then** missing values are presented clearly and are not fabricated.

### User Story 6 - Refresh dashboard data (Priority: P2)

As a dashboard user, I want the application to load persisted sprint data on open and provide a visible action to reimport the selected sample fixture so I can tell how current the local data is.

**Why this priority**: Users need visible freshness information to trust operational metrics.

**Independent Test**: Load the app, invoke refresh, and verify the last-refreshed value and failure behavior.

**Acceptance Scenarios**:

1. **Given** the application opens, **When** PostgreSQL is available, **Then** the dashboard loads persisted data and shows the last successful sample import without automatically overwriting stored data.
2. **Given** the user invokes manual refresh, **When** the sample refresh succeeds, **Then** the selected fixture is reimported transactionally and the timestamp updates.
3. **Given** refresh fails, **When** the failure is reported, **Then** the user sees a clear error and the application does not claim that stale data was refreshed successfully.

### User Story 7 - Configure status mapping (Priority: P2)

As a local dashboard operator, I want to map source statuses to the normalized categories so sample or imported statuses are interpreted consistently without changing calculation code.

**Why this priority**: Status normalization is required for correct progress and risk calculations, but the sample dashboard remains useful with its default mappings.

**Independent Test**: Change a local mapping, reload the sprint view, and verify that the issue's normalized category and derived metrics change while the source status remains unchanged.

**Acceptance Scenarios**:

1. **Given** the default sample mappings are loaded, **When** the operator views settings, **Then** each sample source status has exactly one normalized category.
2. **Given** a valid complete mapping set is submitted, **When** it is saved, **Then** the updated local mapping is applied on subsequent calculations and no external service is called.
3. **Given** a mapping is missing, duplicated, or targets an invalid category, **When** it is submitted, **Then** the request is rejected and the previously saved mapping remains unchanged.

### Edge Cases

- A sprint has no issues or no estimated issues; show unavailable point progress when its denominator is zero.
- A sprint start date or end date is missing, or the start date is after the end date.
- The dashboard date is before the sprint starts or after it ends.
- An issue has no due date, creation date, resolution date, assignee, estimate, or Jira URL.
- A Jira source status has no configured normalized-status mapping.
- A snapshot date has no complete observation for every issue in the sprint.
- An issue is `Blocked`; it is not complete unless its normalized status is `Done`.
- The selected sprint has no comparable historical sprints or historical sprints have missing estimates.
- Capacity is absent, is zero, or cannot be compared with committed work.
- A filter matches no issues.
- The Jira API times out, returns an authorization error, rate-limits a request, or returns partial data.

## Requirements

### Functional Requirements

- **FR-001**: The system MUST support one team's current and historical sprints.
- **FR-002**: The prototype MUST load a complete sample dashboard without Jira credentials.
- **FR-003**: Sample data MUST contain 11-30 issues, a mix of stories, tasks, and bugs, unestimated issues, examples of blocked, overdue, and post-start-added work, capacity pressure, daily issue snapshots spanning at least one sprint, and at least three completed historical sprints for a forecast.
- **FR-004**: Users MUST be able to select an available sprint.
- **FR-005**: The sprint summary MUST show sprint name, actual start and end dates, elapsed and remaining days when calculable, completion by issue count and story points, committed, completed, and remaining estimated work, unestimated work, and a textual sprint-health state.
- **FR-006**: Issue-count completion MUST include every in-scope issue. When the issue count is zero, the system MUST report the value as unavailable rather than divide by zero.
- **FR-007**: Story-point progress MUST include only issues with valid estimates. Missing estimates MUST remain distinct from zero-point estimates and MUST be reported separately.
- **FR-008**: An issue MUST count as complete only when its normalized status is `Done`; `Blocked` MUST NOT count as complete.
- **FR-009**: The progress view MUST provide a planned line and actual remaining work from dated issue snapshots over the selected sprint's actual dates. It MUST support issue-count and story-point views where required data exists, show gaps rather than interpolating missing actual snapshots, and explain when the baseline or snapshots are incomplete.
- **FR-010**: The system MUST show blocked, overdue, scope-added-after-start, and capacity-versus-work risk signals when their input data permits calculation.
- **FR-011**: An issue MUST be considered overdue only when it is incomplete and its due date is before the dashboard date. An issue MUST be considered scope-added when its sprint-membership date is after the sprint start date; issue creation date MUST NOT be used as a substitute.
- **FR-012**: The dashboard MUST explain missing data or insufficient history whenever it prevents a metric, risk, or forecast from being calculated.
- **FR-013**: Users MUST be able to filter by normalized status, issue type, assignee, and risk signal. Selecting a metric or chart segment MUST filter the related issue list.
- **FR-014**: Issue details MUST include issue key, summary, issue type, normalized status, assignee, story points and due date when present, risk indicators, and Jira URL when available.
- **FR-015**: In this prototype, a provided Jira URL MUST be rendered as escaped, non-clickable text. External link navigation is out of scope until a later integration defines an allowlisted HTTPS Jira host.
- **FR-016**: The system MUST show a visible refresh action and last-refreshed timestamp; it MUST distinguish successful refresh from failed refresh.
- **FR-017**: Jira workflow statuses MUST map to normalized categories `To Do`, `In Progress`, `Done`, and `Blocked` without embedding provider-specific status values in calculation logic.
- **FR-018**: The sample provider and future Jira provider MUST use the same normalized data contract.
- **FR-019**: Live Jira and Confluence integration MUST NOT be implemented in this prototype. Any later Jira integration MUST be read-only by default, obtain credentials from server-side secret configuration, and never commit, expose, or log credentials.
- **FR-020**: Core controls MUST be keyboard-operable, status meaning MUST NOT rely on color alone, and the layout MUST remain usable at desktop and tablet widths.
- **FR-021**: The backend MUST expose the versioned JSON API described below. The browser MUST send dashboard requests only to this backend API.
- **FR-022**: PostgreSQL MUST persist normalized sprint, issue, history, daily snapshot, status-mapping, and refresh metadata using the model below. Sample fixture loading and refresh MUST update local records only.
- **FR-023**: Users MUST be able to view and update local source-status mappings without changing calculation code; mapping updates MUST NOT modify Jira or Confluence.
- **FR-024**: The prototype MUST bind the frontend and backend to loopback interfaces and MUST NOT be deployed for shared network access. Authentication and authorization for shared deployment are out of scope.
- **FR-025**: The prototype MUST use a local dashboard date in UTC. Summary, issue, risk, burndown, and forecast calculations MUST use the same `asOf` date.
- **FR-026**: For the defined sample dataset of at most 30 issues per sprint and 12 historical sprints, API p95 response time MUST be at most 500 ms and the dashboard MUST render usable sample content within 2 seconds on a supported development machine.

### Key Entities

- **Sprint**: Stable identifier, name, optional calendar-date start and end dates, optional capacity in story points, and a current-sprint flag. At most one sprint is current.
- **Issue**: Key, summary, source issue type and status, nullable normalized status when unmapped, optional assignee, optional non-negative story-point estimate, optional due/creation/resolution dates, optional sprint-membership date, and optional Jira URL. Missing estimates are null, not zero.
- **Historical Sprint**: Stable identifier, name, optional calendar-date start/end dates, optional committed points, and optional completed points.
- **Issue Snapshot**: Sprint and issue identifiers, observation date, in-sprint membership, normalized status, and estimate as observed on that date. Snapshots preserve history needed for burndown and scope calculations.
- **Sprint Dataset**: One sprint, its issue collection, and historical sprint data used by the same provider contract for sample and live sources.
- **Status Mapping**: Configurable mapping from sample source statuses to `To Do`, `In Progress`, `Done`, or `Blocked` in this prototype. Future provider-specific mappings are out of scope.

Dates are calendar dates rather than timestamps. Present numeric values MUST be finite and non-negative. An unmapped source status is stored with `normalized_status = NULL`, remains visible with an `Unmapped` label, counts as incomplete for issue-count progress and overdue checks, and is excluded from status-specific mapped counts. It MUST NOT be silently treated as `Done`.

## Calculation Decisions

- The dashboard date defaults to the current UTC calendar date. All date-only ranges are inclusive. Elapsed days are `clamp(asOf - startDate + 1, 0, totalDays)`; remaining days are `totalDays - elapsedDays`. Weekends and holidays are calendar days. A missing or reversed date range makes date-based metrics unavailable.
- Every request contributing to one rendered dashboard MUST use the same `asOf` date. If no complete snapshot exists on `asOf`, calculations use the most recent complete snapshot before it and identify its observation date as stale.
- Issue-count completion is `Done issues / all in-scope issues`; unmapped issues are included in the denominator and not the numerator. Story-point completion is `Done estimated points / all in-scope estimated points`, rounded to one decimal place. A zero denominator yields unavailable (`null`), not zero percent. A valid estimate of zero is retained but adds zero to point totals.
- Committed points are the sum of estimates in the complete baseline snapshot on the sprint start date. Current completed points are estimates for in-scope issues currently mapped `Done`; remaining points are estimates for in-scope issues not `Done`. Current progress is not capped at committed points, so post-start scope and re-estimation remain visible. Unestimated work is counted separately and does not enter point sums.
- An issue removed from a sprint has `is_in_scope = false` from its effective removal date and is excluded from later totals; earlier snapshots remain unchanged. A cancelled issue that remains in scope is incomplete unless its status is explicitly mapped to `Done`.
- An issue is overdue when it is incomplete (including unmapped) and `due_date < asOf`. Scope added is based on `added_to_sprint_at > start_date`; if that field is missing, scope-change status is unavailable for that issue and the dashboard reports the missing data.
- Capacity risk is calculable only when capacity and committed points are present. It is true when committed points exceed capacity points; unestimated issues are excluded from the comparison and shown separately.
- Health is `Insufficient data` when no complete current snapshot or valid sprint dates are available; otherwise it is `At risk` when there is at least one blocked or overdue issue, capacity risk is true, or the estimated-work forecast falls after sprint end. It is `On track` otherwise. Scope additions alone remain a separate signal and do not change health.
- Actual burndown uses complete issue snapshots for each observation date and has gaps where dates are missing; values are not interpolated. Planned remaining work declines linearly in calendar days from the committed baseline on the sprint start date to zero on the end date. A one-day sprint has no planned line and reports that reason.
- Forecast uses the three to five most recent completed historical sprints for this single team that have valid dates and completed points. It uses the median completed points per sprint and median inclusive sprint duration. Estimated remaining points divided by median velocity, multiplied by median duration, is rounded up to calendar days and added to `asOf`. Zero estimated remaining points forecasts `asOf`. Fewer than three eligible sprints, zero median velocity, or missing current estimates makes the forecast unavailable. The forecast applies to estimated work only; unestimated incomplete issues are displayed as a limitation.

## API Contract

The backend exposes JSON over REST beneath `/api/v1`. Identifiers in paths are URL-encoded. Date-only request and response values use `YYYY-MM-DD`; refresh timestamps use ISO 8601 UTC. All responses use the normalized internal contract, not raw provider-specific payloads. The prototype API serves sample data only.

| Method and path | Request data | Response data and behavior |
| --- | --- | --- |
| `GET /api/v1/sprints` | Optional `scope=current\|history\|all` query; defaults to `all`. | `{ items: [{ sprintId, name, startDate, endDate, isCurrent }], total }`, ordered current first, then start date descending, then ID ascending. |
| `GET /api/v1/sprints/{sprintId}/summary` | Optional `asOf=YYYY-MM-DD`; defaults to the current UTC date. | Selected sprint, the effective snapshot date, elapsed/remaining days, issue-count and point metrics, risk counts, health state/reasons, and last successful refresh time. |
| `GET /api/v1/sprints/{sprintId}/issues` | Optional repeated `status`, `issueType`, and `assignee` filters, `risk=blocked\|overdue\|scope-change\|capacity\|unmapped`, and `asOf=YYYY-MM-DD`. | `{ items: [Issue], total, asOf, effectiveSnapshotDate }`. An empty match returns an empty list, not an error. |
| `GET /api/v1/sprints/{sprintId}/burndown` | Required `metric=issueCount\|storyPoints`; optional `asOf=YYYY-MM-DD`. | `{ availability, reason, metric, startDate, endDate, points: [{ date, plannedRemaining, actualRemaining }] }`. Only observed actual dates are returned; gaps are not interpolated. |
| `GET /api/v1/sprints/{sprintId}/risks` | Optional `type=blocked\|overdue\|scope-change\|capacity\|unmapped` and `asOf=YYYY-MM-DD`. | `{ items: [{ type, count, calculable, reason, issueKeys }], asOf, effectiveSnapshotDate }`. |
| `GET /api/v1/sprints/{sprintId}/forecast` | Optional `asOf=YYYY-MM-DD`. | `{ availability, reason, eligibleSprintCount, medianVelocityPoints, medianDurationDays, estimatedRemainingPoints, forecastDate, excludesUnestimatedWork }`. |
| `GET /api/v1/status-mappings` | No body. | `{ mappings: [{ sourceSystem, sourceStatus, normalizedStatus }] }`. Prototype mappings are for sample source statuses only. |
| `PUT /api/v1/status-mappings` | `{ "mappings": [{ "sourceSystem": "sample", "sourceStatus": "In Progress", "normalizedStatus": "In Progress" }] }`. | Validates and replaces the full local mapping set transactionally, re-normalizes stored sample snapshots, and returns `{ mappings }`. |
| `POST /api/v1/sprints/{sprintId}/refresh` | No body. | Synchronously reloads and transactionally upserts that sprint's sample fixture; returns `{ status: "succeeded", completedAt }`. A failure returns an error and preserves prior data. |

### API Semantics and Errors

- All dashboard requests in one view MUST share one `asOf` value. If omitted, it is the current UTC calendar date. The effective observation date is the latest complete daily snapshot on or before `asOf`; it is returned so the UI can label stale data. No snapshot on or before `asOf` makes snapshot-dependent fields unavailable.
- A success response uses `availability: "available" | "partial" | "unavailable"` where applicable and a nullable human-readable `reason`. Dates are strings or `null`; percentages are numbers rounded to one decimal place or `null`; absent optional values are `null`, not omitted or fabricated.
- `Issue` is `{ issueKey, summary, issueType, sourceStatus, normalizedStatus, assignee, storyPoints, dueDate, createdAt, addedToSprintAt, resolvedAt, jiraUrl, riskSignals }`. `normalizedStatus` is one of the four normalized values or `null`; `riskSignals` may include `unmapped`.
- Within one filter dimension, repeated values use OR; different dimensions use AND. Status/risk values are exact enums. `issueType` and `assignee` are trimmed, case-insensitive exact matches. Wildcards are unsupported. Results are sorted by `issueKey` ascending. The prototype limits a selected sprint to 30 issues and includes at most 12 historical sprints, so pagination is out of scope. Invalid filters return `400`.
- `400` means invalid input/filter, `404` means an unknown sprint, `409` means a conflicting refresh for the same sprint, `503` means PostgreSQL or the sample provider is unavailable, and `500` means an unexpected server error. Errors use `{ "error": { "code": "...", "message": "...", "details": [] } }`; responses MUST NOT contain credentials, stack traces, or raw upstream bodies.
- A successful refresh returns `200`. A failed refresh returns `503`, records a sanitized failed refresh row, and leaves the last successful data and timestamp unchanged. Refresh is synchronous and serialized per sprint; a concurrent request for that sprint returns `409`.

The following TypeScript-style shapes are normative JSON contracts; `null` represents unavailable or absent optional data, while fields are always present unless marked optional:

```ts
type Availability = "available" | "partial" | "unavailable";
type NormalizedStatus = "To Do" | "In Progress" | "Done" | "Blocked";
type RiskType = "blocked" | "overdue" | "scope-change" | "capacity" | "unmapped";

type SprintListResponse = {
	items: Array<{
		sprintId: string; name: string; startDate: string | null; endDate: string | null; isCurrent: boolean;
	}>;
	total: number;
};

type Issue = {
	issueKey: string; summary: string; issueType: string; sourceStatus: string;
	normalizedStatus: NormalizedStatus | null; assignee: string | null; storyPoints: number | null;
	dueDate: string | null; createdAt: string | null; addedToSprintAt: string | null;
	resolvedAt: string | null; jiraUrl: string | null; riskSignals: RiskType[];
};

type RiskItem = { type: RiskType; count: number | null; calculable: boolean; reason: string | null; issueKeys: string[] };
type RiskResponse = { items: RiskItem[]; asOf: string; effectiveSnapshotDate: string | null };

type SummaryResponse = {
	sprint: SprintListResponse["items"][number]; asOf: string; effectiveSnapshotDate: string | null;
	elapsedDays: number | null; remainingDays: number | null;
	progress: {
		issueCount: { completed: number; total: number; percent: number | null };
		storyPoints: { committed: number | null; completed: number | null; remaining: number | null; percent: number | null };
		unestimatedIssues: number;
	};
	health: { state: "On track" | "At risk" | "Insufficient data"; reasons: string[] };
	risks: RiskItem[]; lastSuccessfulRefreshAt: string | null;
};

type IssueListResponse = { items: Issue[]; total: number; asOf: string; effectiveSnapshotDate: string | null };
type BurndownResponse = {
	availability: Availability; reason: string | null; metric: "issueCount" | "storyPoints";
	startDate: string | null; endDate: string | null;
	points: Array<{ date: string; plannedRemaining: number | null; actualRemaining: number | null }>;
};
type ForecastResponse = {
	availability: Availability; reason: string | null; eligibleSprintCount: number; sprintIdsUsed: string[];
	medianVelocityPoints: number | null; medianDurationDays: number | null;
	estimatedRemainingPoints: number | null; forecastDate: string | null; excludesUnestimatedWork: boolean;
};
type StatusMappingsResponse = {
	mappings: Array<{ sourceSystem: "sample"; sourceStatus: string; normalizedStatus: NormalizedStatus }>;
};
type RefreshResponse = { status: "succeeded"; completedAt: string };
type ErrorResponse = {
	error: { code: string; message: string; details: Array<{ field: string; issue: string }> };
};
```

Stable error codes are `VALIDATION_ERROR` (`400`), `SPRINT_NOT_FOUND` (`404`), `REFRESH_IN_PROGRESS` (`409`), `DATABASE_UNAVAILABLE` or `SAMPLE_PROVIDER_UNAVAILABLE` (`503`), and `INTERNAL_ERROR` (`500`).

## UI Screens

### Sprint Overview

- Route: `/sprints/{sprintId}`; `/` opens the current sprint when one exists, otherwise it shows the sprint selector without a selection.
- Shows the sprint selector, name, dates, elapsed/remaining days, health indicator, issue-count and point completion, committed/completed/remaining estimated work, unestimated count, refresh control, and last successful refresh time.
- Selecting a sprint loads that sprint's overview and keeps its identity visible.

### Progress Analysis

- Route: `/sprints/{sprintId}/progress`.
- Shows planned versus actual burndown, a segmented issue-count/story-point control, a historical-velocity reference, and forecast availability or its reason.
- Selecting a chart segment filters the associated issue list and exposes a clear way to remove that filter.

### Risks and Issues

- Route: `/sprints/{sprintId}/issues`.
- Shows blocked, overdue, scope-change, and capacity-risk counts with text/icon indicators; filters for normalized status, issue type, assignee, and risk; and the matching issue list.
- Expanding an issue shows all available contract fields. A Jira URL is escaped and displayed as non-clickable text. Missing optional values are labeled as unavailable rather than fabricated.
- No-match, unmapped-status, missing-data, loading, refresh-failure, and stale-data states have explicit messages.

### Status Mapping

- Route: `/settings/status-mappings`.
- Shows source statuses and their normalized categories, allows a user to edit the local mapping set, and explains that changes affect dashboard interpretation only, not Jira/Confluence records.
- Default sample mappings are `To Do` to `To Do`, `In Progress` to `In Progress`, `Done` to `Done`, and `Blocked` to `Blocked`.
- Source matching trims whitespace and compares case-insensitively. Duplicate source keys after normalization are rejected. The full non-empty mapping set must target exactly one of `To Do`, `In Progress`, `Done`, or `Blocked` per row.
- Saving re-normalizes all retained sample issues and snapshots in one transaction. A failed update leaves prior mappings and snapshots intact. In this local-only prototype, updates use last-write-wins; mapping audit history and shared-user authorization are out of scope.
- An unmapped source status remains visible as `Unmapped`, is included as incomplete in issue-count progress, is eligible for overdue detection, and is not counted as `Done` or any mapped status.

The application loads automatically into the current sprint when one is marked current. If none is current, the sprint selector is shown without selecting one; if no sprints exist, an empty state explains that sample data is unavailable. Loading, no-match, missing data, stale snapshots, unmapped status, and failed refresh states must be visibly distinct. All screens meet FR-020: keyboard operation, visible focus, readable contrast, text/icon status alternatives, and no horizontal overlap at 768 px and wider. Charts also provide an accessible textual/table equivalent. CI runs axe-core scans on primary routes with zero critical or serious violations; manual keyboard checks cover sprint selection, filters, issue expansion, chart alternatives, refresh, and status mapping. The application is for localhost use only; shared deployment and authentication are out of scope.

## PostgreSQL Data Model

PostgreSQL 15.14 is the persistence store for normalized data. The sample provider seeds the same tables used by a future provider. Schema changes use versioned migrations. The single-team prototype does not require a team table. Foreign-key dependents of a sprint are deleted with that sprint, except refresh history, which retains its row with a null sprint reference.

| Table | Columns and constraints | Purpose |
| --- | --- | --- |
| `sprints` | `sprint_id TEXT PRIMARY KEY`, `name TEXT NOT NULL`, `start_date DATE NULL`, `end_date DATE NULL`, `capacity_points NUMERIC(8,2) NULL CHECK (capacity_points BETWEEN 0 AND 999999.99)`, `is_current BOOLEAN NOT NULL DEFAULT FALSE`, `source TEXT NOT NULL DEFAULT 'sample' CHECK (source = 'sample')`. | Stores sprint identity, dates, capacity, current selection, and source. Enforce `end_date >= start_date` when both are present and a partial unique index allowing at most one current sprint. |
| `sprint_issues` | `sprint_id TEXT NOT NULL REFERENCES sprints ON DELETE CASCADE`, `issue_key TEXT NOT NULL`, `summary TEXT NOT NULL`, `issue_type TEXT NOT NULL`, `source_status TEXT NOT NULL`, `normalized_status TEXT NULL CHECK (normalized_status IN ('To Do','In Progress','Done','Blocked'))`, `assignee TEXT NULL`, `story_points NUMERIC(8,2) NULL CHECK (story_points BETWEEN 0 AND 999999.99)`, `due_date DATE NULL`, `created_at DATE NULL`, `added_to_sprint_at DATE NULL`, `resolved_at DATE NULL`, `jira_url TEXT NULL`, `PRIMARY KEY (sprint_id, issue_key)`. | Stores the latest known issue attributes. Null estimate means unestimated; null normalized status means unmapped. |
| `sprint_issue_snapshots` | `sprint_id TEXT NOT NULL`, `issue_key TEXT NOT NULL`, `observed_on DATE NOT NULL`, `is_in_scope BOOLEAN NOT NULL`, `source_status TEXT NOT NULL`, `normalized_status TEXT NULL CHECK (normalized_status IN ('To Do','In Progress','Done','Blocked'))`, `story_points NUMERIC(8,2) NULL CHECK (story_points BETWEEN 0 AND 999999.99)`, `PRIMARY KEY (sprint_id, issue_key, observed_on)`, composite FK to `sprint_issues` with `ON DELETE CASCADE`. | Stores one state per issue per observed date, including source status, estimate, and sprint membership, for actual burndown and scope history. Fixtures provide daily complete snapshots; missed dates remain gaps. |
| `sprint_history` | `sprint_id TEXT PRIMARY KEY REFERENCES sprints ON DELETE CASCADE`, `committed_points NUMERIC(8,2) NULL CHECK (committed_points BETWEEN 0 AND 999999.99)`, `completed_points NUMERIC(8,2) NULL CHECK (completed_points BETWEEN 0 AND 999999.99)`. | Stores completed historical velocity inputs; sprint name and dates remain in `sprints`. |
| `status_mappings` | `source_system TEXT NOT NULL`, `source_status_key TEXT NOT NULL`, `source_status TEXT NOT NULL`, `normalized_status TEXT NOT NULL CHECK (normalized_status IN ('To Do','In Progress','Done','Blocked'))`, `PRIMARY KEY (source_system, source_status_key)`. | Stores normalized source mappings. `source_status_key` is trimmed lowercase source text. In this prototype `source_system` is `sample`. |
| `refresh_runs` | `refresh_run_id UUID PRIMARY KEY`, `sprint_id TEXT NULL REFERENCES sprints ON DELETE SET NULL`, `source TEXT NOT NULL CHECK (source = 'sample')`, `started_at TIMESTAMPTZ NOT NULL`, `completed_at TIMESTAMPTZ NULL`, `status TEXT NOT NULL CHECK (status IN ('running','succeeded','failed'))`, `error_summary TEXT NULL`. | Records local fixture refresh state and supports last-refreshed/error display. Error summaries are sanitized and contain no credentials or raw payloads. |

The API MUST map these rows to the Sprint, Issue, Historical Sprint, Issue Snapshot, and Status Mapping entities above. Add indexes on `sprint_issue_snapshots (sprint_id, observed_on)`, `sprint_issues (sprint_id, normalized_status)`, `sprint_issues (sprint_id, issue_type)`, and `sprint_issues (sprint_id, assignee)`. A database check MUST bound every numeric measure to a finite, non-negative `NUMERIC(8,2)` value. The prototype uses a named Docker volume and `pg_isready` health check. Local setup is `docker compose up -d db`, run versioned migrations, then load deterministic sample fixtures; `docker compose down -v` is the explicit destructive reset. Persisted fixtures MUST contain no real credentials or external confidential data.

## Technical Constraints

### Stack

- Frontend: React 18.3.1 and Vite 8.3.3.
- Frontend and backend source: TypeScript 7.0.2, consistent with the existing `.tsx` and `.ts` project skeleton.
- Backend: Node.js 24.21.0, npm 11.19.0, and Express 5.2.1.
- Database: PostgreSQL 15.14, using the `postgres:15.14` container image.
- Local containers: Docker CLI 29.8.1 and Docker Compose 5.5.1.
- Pin direct npm dependencies to these exact versions without semver ranges and commit the npm lockfile. Update versions only through a reviewed specification/lockfile change. Pin the PostgreSQL patch tag; image digest pinning is not required for this local prototype.

### Folder and Naming Conventions

- `frontend/src/app/`: application entry and top-level composition.
- `frontend/src/features/sprints/`: sprint dashboard feature views and components.
- `frontend/src/components/`: reusable frontend components not owned by one feature.
- `frontend/src/api/`: typed client for the backend API; no Jira credentials or direct database access.
- `frontend/tests/`: frontend interaction tests.
- `backend/src/server.ts`: backend process entry point.
- `backend/src/routes/`: Express route registration and request/response boundary.
- `backend/src/services/`: application workflows that coordinate domain logic and providers.
- `backend/src/domain/`: provider-independent calculations and business rules.
- `backend/src/providers/sample/` and `backend/src/providers/jira/`: sample and Jira data adapters.
- `backend/src/config/`: validated server-side configuration.
- `backend/tests/`: backend unit and integration tests.
- `packages/contracts/src/`: shared request, response, and domain contract types.
- `data/sample/`: version-controlled, credential-free sample fixtures.
- `spec/`: project constitution and feature specifications.
- `docker-compose.yml`: local PostgreSQL service definition; secrets MUST come from local environment configuration and not be committed.
- React component files MUST use PascalCase and `.tsx`; non-component TypeScript modules MUST use camelCase and `.ts`; tests MUST use `*.test.ts` or `*.test.tsx` and remain in the relevant `tests/` directory.
- Docker Compose MUST expose PostgreSQL only on `127.0.0.1:5432`, use a named volume, and gate application startup on a `pg_isready` health check. The prototype runs the frontend/backend from the host; Compose starts only the database.
- Local database setup uses `docker compose up -d db`, then `npm run db:migrate` and `npm run db:seed` from the backend. Migrations run before seeding. Seeding is deterministic and idempotent. `docker compose down` preserves the volume; `docker compose down -v` is the documented destructive reset.
- Required local variables are `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `DATABASE_URL`, and `API_PORT`; values belong in an ignored local `.env` file. The committed `.env.example` MUST list variable names and non-secret placeholders only. The browser receives no database or integration credentials.

## Success Criteria

### Measurable Outcomes

- **SC-001**: A user can open the prototype and view a complete sample sprint dashboard without Jira credentials.
- **SC-002**: For every test fixture, issue-count and estimated story-point totals match independently calculated expected values; unestimated issues never inflate point totals.
- **SC-003**: The burndown uses the selected sprint's actual start and end dates and does not assume a fixed sprint duration.
- **SC-004**: Selecting each supported risk signal or chart segment leaves only matching issues in the issue list.
- **SC-005**: When a required field or history is missing, the affected metric or forecast is identified as unavailable with an explanation; it is never silently presented as zero.
- **SC-006**: The forecast is shown when its configured historical-data requirements are met and is withheld with an explanation when they are not.
- **SC-007**: Every primary dashboard control is keyboard-operable, status information is not color-only, and desktop and tablet layouts have no overlapping content.
- **SC-008**: A successful refresh updates the last-refreshed timestamp; a failed refresh is visibly reported and does not update the success timestamp.
- **SC-009**: Automated checks confirm that no Jira or Confluence credential is present in frontend bundles, sample data, committed files, or application logs.
- **SC-010**: With the defined maximum sample dataset, API p95 latency is at most 500 ms and usable dashboard content renders within 2 seconds on the supported local development setup.
- **SC-011**: Keyboard-only users can reach and operate sprint selection, filters, issue details, refresh, and status mapping; charts have a textual/table alternative; no horizontal overlap occurs at viewport widths of 768 px, 1024 px, and 1440 px.

## Assumptions

- The first release is an internal, single-team dashboard for scrum masters and engineering managers.
- The prototype uses sample fixtures seeded into PostgreSQL and requires no Jira or Confluence credentials. On initial setup, apply migrations and run the deterministic seed command. Application startup loads persisted data and does not automatically overwrite it; manual refresh reimports only the selected sprint fixture. Docker Compose is required to run the database.
- `spec/specification.md` and `spec/constitution.md` are authoritative for this prototype. The old Streamlit/Python `project_spec.md` and pandas `DATA_CONTRACT.md` are historical references and are out of scope as implementation contracts; migrate or retire them before implementation begins.
- Live Jira and Confluence integrations, OAuth/shared-user authentication, Jira writeback, real-time streaming, multi-team comparisons, Jira embedding, and external confidential data are out of scope for this prototype.
- The prototype listens only on loopback and is intended for one local operator. No access-control system is implemented.
- Unresolved decisions for later Jira/Confluence phases do not block this sample-only prototype and MUST be specified before those integrations are started.
- In the prototype, Jira URLs are displayed as escaped text only; navigating to external hosts is out of scope.

## Open Questions

All clarification items in `spec/clarify.md` are either resolved by this specification or explicitly out of scope for this prototype. Any later Jira/Confluence integration, shared deployment, or change to the approved stack requires a new feature specification and security/access decisions before implementation.