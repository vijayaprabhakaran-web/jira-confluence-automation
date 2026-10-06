# Specification Clarification Register

Review of `spec/constitution.md`, `spec/specification.md`, `project_spec.md`, and `DATA_CONTRACT.md`.

**Status**: All review questions are closed for the prototype. `Answered` items have been added to `spec/specification.md`; `Out of scope` items are explicitly excluded from this prototype. The original questions below remain for traceability, not as open blockers.

## Dispositions

| Item | Disposition and decision |
| --- | --- |
| Q-001 | **Answered**: `spec/specification.md` is authoritative for the React/Node/PostgreSQL prototype. The Streamlit/Python project spec and pandas contract are historical references; migrate or retire them before implementation. |
| Q-002 | **Answered**: PostgreSQL is required. Seed it deterministically from sample fixtures; startup reads persisted data and fails clearly if the database is unavailable. |
| Q-003 | **Answered**: Dated issue snapshots supply actual sample burndown and preserve state history. Live Jira changelog ingestion is out of scope. |
| Q-004 | **Answered**: Scope addition uses `added_to_sprint_at`, not issue creation date; snapshots record membership changes and preserve earlier scope. |
| Q-005 | **Answered**: Store unmapped status as `normalized_status = NULL`; display `Unmapped`, count as incomplete, allow an unmapped filter, and never count it as `Done`. |
| Q-006 | **Out of scope**: Confluence workflows, endpoints, storage, and UI are excluded from this Jira dashboard prototype. |
| Q-007 | **Answered**: `sprints.is_current` identifies the current sprint; a partial unique index allows at most one. The root route opens it or shows an unselected picker when none exists. |
| Q-008 | **Out of scope**: Live Jira API integration, credentials, pagination, and upstream refresh are deferred. This prototype uses sample data only; a later Jira feature must define these details and remain read-only by default. |
| Q-009 | **Out of scope**: Shared deployment, authentication, and authorization are excluded. Bind frontend/backend to loopback for one local operator. |
| Q-010 | **Answered**: The spec defines issue-count and point denominators, committed baseline, current remaining work, zero-estimate behavior, and in-scope/removal semantics. |
| Q-011 | **Answered**: Use UTC calendar dates with inclusive boundaries; default `asOf` is current UTC date, and all dashboard requests share it. |
| Q-012 | **Answered**: Capacity risk is true only when known committed baseline points exceed known capacity; missing inputs make it unavailable and unestimated issues are reported separately. |
| Q-013 | **Answered**: Health is `Insufficient data`, `At risk`, or `On track` using the rules in Calculation Decisions. |
| Q-014 | **Answered**: Use the median of three to five latest eligible completed sprints and median duration; forecast estimated remaining points only, with the unavailable/zero-work cases defined in the spec. |
| Q-015 | **Answered**: Normative TypeScript-style API response shapes, nullable fields, error envelope, HTTP statuses, and stable error codes are specified. |
| Q-016 | **Answered**: Same-dimension filters are OR; different dimensions are AND; matching is exact (text is trimmed/case-insensitive); results are key-sorted. **Out of scope**: pagination, because prototype datasets are capped at 30 issues per sprint and 12 historical sprints. |
| Q-017 | **Answered**: Startup applies migrations/seeds only during setup and reads persisted data without overwriting it. Manual sample refresh is synchronous, transactional, per-sprint, and rejects a concurrent refresh; failed refresh preserves prior data. |
| Q-018 | **Answered**: Seed four default sample mappings; full-set updates validate normalized unique keys and atomically re-normalize issues/snapshots; local last-write-wins applies. **Out of scope**: mapping audit history and shared-user authorization. |
| Q-019 | **Answered**: The spec defines finite non-negative `NUMERIC(8,2)` bounds, date ordering, keys, cascades, retention behavior, and query indexes for the single-source prototype. |
| Q-020 | **Answered**: Compose runs only PostgreSQL on loopback with a named volume and `pg_isready`; migrations precede deterministic seed; `down` retains data and `down -v` explicitly deletes it. Required local variables are listed. |
| Q-021 | **Answered**: Empty, loading, no-match, stale, missing-data, unmapped, and failed-refresh UI states are defined. **Out of scope**: partial upstream provider failures, because live integrations are excluded. |
| Q-022 | **Answered**: Support 768, 1024, and 1440 px layouts, keyboard paths, visible focus, non-color status, and textual chart alternatives. CI runs axe-core on primary routes; manual keyboard checks cover all critical controls. |
| Q-023 | **Answered**: Prototype limit is 30 issues per sprint and 12 historical sprints; local API p95 is at most 500 ms and usable dashboard content renders within 2 seconds. Freshness is shown using effective snapshot and last-import timestamps. **Out of scope**: Jira-mode latency/freshness targets. |
| Q-024 | **Out of scope**: External Jira navigation is disabled; URLs are escaped non-clickable text until a later integration specifies an HTTPS host allowlist. |
| Q-025 | **Answered**: Pin React 18.3.1, Vite 8.3.3, TypeScript 7.0.2, Node 24.21.0, npm 11.19.0, Express 5.2.1, PostgreSQL 15.14, Docker CLI 29.8.1, and Docker Compose 5.5.1. Commit exact npm lockfile versions; use the PostgreSQL 15.14 image tag. |

## Blocking Conflicts and Feasibility

### Q-001 - Which architecture is authoritative? (Blocker)

`project_spec.md` specifies Streamlit/Python and `DATA_CONTRACT.md` defines a pandas-based `SprintDataset`; the constitution and this feature specification instead specify React, Node.js/Express, and PostgreSQL. The specification says the new stack is intended to replace the old one, but the source documents have not been migrated.

**Clarify**: Is the React/Node/PostgreSQL design the approved replacement? If yes, should `project_spec.md` and `DATA_CONTRACT.md` be rewritten as part of this feature before planning? If not, which document and stack govern implementation?

### Q-002 - Is PostgreSQL required for the sample prototype? (Blocker)

FR-002 requires a complete sample dashboard without Jira credentials. FR-022 requires sprint, issue, history, mapping, and refresh data to persist in PostgreSQL. The Assumptions section leaves open whether sample data is loaded into PostgreSQL or served directly from fixtures.

**Clarify**: Must the prototype start PostgreSQL and seed it from `data/sample/`, or may the sample provider serve fixtures directly? Which data must be persisted, and what should happen when PostgreSQL is unavailable?

### Q-003 - How can the system calculate historical burndown? (Blocker)

FR-009 requires actual remaining work by date, but `sprint_issues` stores only one current row per issue with current normalized status, `created_at`, and `resolved_at`. The specification says burndown points can be derived from sprint and issue dates and that no daily snapshot table is required. Those fields cannot reconstruct status changes, reopened issues, estimate changes, removed scope, or the original sprint commitment over time.

**Clarify**: Which source of change history is authoritative: Jira changelog events, daily snapshots, or another event table? What data establishes the day-one scope and estimate baseline? If historical state is unavailable, should actual burndown be limited to sample data or removed from live-data claims?

### Q-004 - What constitutes scope added after sprint start? (Blocker)

FR-011 and the data contract use an issue's `created_at` date to identify scope added after sprint start. An issue can be created before a sprint and added to it later, so creation date is not necessarily sprint-membership date.

**Clarify**: Is scope change based on issue creation or the date the issue was added to the sprint? If it means sprint membership, which Jira event/field supplies that date, and how are removed or re-added issues handled?

### Q-005 - How are unmapped Jira statuses represented? (Blocker)

The spec requires unmapped statuses to be surfaced, but `sprint_issues.normalized_status` is `NOT NULL` and limited to four values. `source_status` is nullable, and no fifth `Unknown` category or quarantine/error representation is defined. The mapping screen also prevents saving unless each configured status is mapped, but it does not define newly discovered statuses.

**Clarify**: Should an unmapped issue be excluded with a data-quality warning, stored with a nullable normalized status, or represented by an explicit `Unknown` value? How can the issue still appear in detail and filters without being counted as complete?

## Product and Integration Scope

### Q-006 - Is Confluence part of this release?

The constitution describes Jira and Confluence automation, while this feature specification explicitly says no Confluence workflow or endpoint is included. No Confluence user story, screen, data model, permission scope, or acceptance criterion is defined.

**Clarify**: Confirm Confluence is out of scope for this feature and tracked separately, or provide the specific Confluence workflow required here.

### Q-007 - How is the current sprint identified and selected by default?

The product supports current and historical sprints, but the `sprints` table has no state/current marker and the sprint-list response does not say which sprint is current. Deriving current state from dates fails when dates are missing or multiple sprints overlap. `/` is specified to open the default available sprint without defining that default.

**Clarify**: Is current sprint state configured, imported from a Jira board, or inferred from dates? What should the root route select when there are zero or multiple current sprints?

### Q-008 - Is live Jira integration in the prototype or a later release?

The prototype is sample-data-only, but the API includes Jira-backed refresh behavior and the database supports `source='jira'`. The transition point between prototype and future integration is unclear.

**Clarify**: Which release includes Jira Cloud reads? For that release, identify the Jira site/base URL, project and board selection, sprint/issue/history endpoints, required fields, pagination behavior, account identity/token format, required scopes, and environment variable names. Confirm that Jira remains read-only.

### Q-009 - What access model protects internal data and mapping changes?

OAuth sign-in is out of scope, while the app handles internal team data and exposes `PUT /api/v1/status-mappings`. The spec warns against exposing the settings screen in shared deployment but does not define whether the prototype is local-only or network-accessible.

**Clarify**: Is deployment restricted to localhost, a trusted network, or shared users? What authentication and authorization protect dashboard data and mapping updates? If no auth is in v1, should the mapping update endpoint/screen be disabled outside local development?

## Metric and Time Semantics

### Q-010 - Define progress denominators and remaining-work formulas

The spec distinguishes issue-count and story-point progress, but does not state the exact formulas or how scope additions/removals and estimate changes affect committed, completed, and remaining totals. Zero-point estimates are valid under the non-negative constraint but their display and denominator treatment are unspecified.

**Clarify**: Define each numerator and denominator, treatment of zero-point estimates, cancelled/removed issues, post-start scope, re-estimation, and whether remaining points are current estimates on incomplete issues or committed points minus completed points.

### Q-011 - Define date boundaries and dashboard date consistently

Dates are calendar dates, but elapsed/remaining day calculations, sprint-boundary inclusivity, weekends/holidays, and display timezone are unspecified. `asOf` is accepted by the summary endpoint but not by the issue or risk endpoints, although overdue status appears in all three.

**Clarify**: Define the dashboard timezone, day-count convention, start/end inclusivity, and behavior before/after sprint dates. Make all overdue-sensitive endpoints use the same `asOf` value or explicitly define a single server-provided dashboard date.

### Q-012 - Define capacity-risk calculation

The risk is described as capacity versus committed/completed/remaining work, but no formula or threshold exists. Capacity is optional, and unestimated issues may make point comparisons incomplete.

**Clarify**: State the comparison, threshold, treatment of missing/zero capacity and unestimated work, and whether capacity risk is a binary signal, ratio, or both.

### Q-013 - Define sprint-health states

The summary must show a textual health indicator, but the health states, thresholds, inputs, and precedence among blocked, overdue, capacity, and progress signals are not specified.

**Clarify**: Define the states and their calculation/threshold rules, or make the dashboard show component signals without collapsing them into a single health rating.

### Q-014 - Define historical-velocity forecast

“Comparable” sprints, minimum history, velocity statistic, treatment of incomplete/abnormal sprints, and the actual forecast calculation are open. The response promises a forecast result without defining whether that is a completion date, probability, or remaining-point estimate.

**Clarify**: Define eligible history, minimum count, statistic, formula, forecast output, and how scope changes or missing estimates affect it.

## API Contract

### Q-015 - Make request and response schemas implementable

The endpoint table names conceptual response fields but omits complete JSON schemas, field types/nullability, and computed metric names. Error behavior says client/service error without defining HTTP status codes or mapping error codes. Refresh success/failure response status is unspecified.

**Clarify**: Publish example or schema definitions for every request and response, including `availability`/`reason`, timestamps, numeric precision, error codes, and HTTP status codes. Define validation for unknown sprint IDs, invalid dates, unknown filters, and upstream failures.

### Q-016 - Define filtering and result limits

Repeated filter parameters are listed, but it is unclear whether multiple values within a filter are ORed, whether different filter types are ANDed, how matching is case-sensitive, and whether the API paginates or sorts issue results.

**Clarify**: Define combination semantics, accepted values, sort order, page/limit behavior, maximum page size, and the response fields needed to navigate results. State how unsupported filters are handled.

### Q-017 - Define refresh lifecycle and consistency

The UI refreshes on application open and manually; `POST /refresh` is per sprint, while sprint discovery may cover all history. `refresh_runs` supports `running`, but the API does not say whether refresh is synchronous or asynchronous, how concurrent refreshes behave, or what happens to previously stored data on a partial failure.

**Clarify**: Define refresh scope on startup/manual action, synchronous versus job/poll behavior, duplicate/concurrent request handling, retry/backoff, rate-limit handling, atomic versus partial upsert, deletion of issues no longer returned, stale-data display, and last-successful timestamp scope.

### Q-018 - Define status-mapping lifecycle

`PUT /status-mappings` replaces the complete mapping set, but default mappings, empty-set behavior, case sensitivity, duplicate normalization, update concurrency, and audit history are unspecified. There is no user story or acceptance scenario for changing mappings.

**Clarify**: Define initial/default mappings, exact source-status matching, save validation, whether deletes are allowed, concurrent update behavior, and tests/acceptance criteria for the mapping workflow.

## Data Model and Operations

### Q-019 - Complete persistence constraints and lifecycle

The table sketch omits bounds/precision for numeric values, a database-enforced finite-number rule despite the contract requiring finite values, sprint date-order checks, delete/cascade policy, and indexes for sprint issue filters. Provider identifiers and duplicate handling during import are not specified.

**Clarify**: Define numeric precision/ranges, date constraints, keys/uniqueness across providers, indexes required by query patterns, and retention/deletion behavior for sprint, issue, mapping, and refresh records.

### Q-020 - Define migrations, seed, and local Docker behavior

The constitution requires versioned migrations and PostgreSQL through Docker Compose, but the spec does not define how migrations run, how sample data is seeded/reset, what persists in the Docker volume, or how service readiness is detected. The repository's `docker-compose.yml` is currently an empty placeholder.

**Clarify**: Define the local startup and reset workflow, migration ownership/order, deterministic seed behavior, database volume retention, health checks, ports, and required environment variables. Keep credentials out of committed compose files.

## UI and Quality Requirements

### Q-021 - Define empty, loading, and degraded UI states

Some error states are named, but there is no complete behavior for no available sprints, first load, stale cached data after refresh failure, partially imported Jira data, or an unknown/unmapped status. A screen route for the root/default sprint is also unresolved in Q-007.

**Clarify**: Specify what each screen displays and allows during initial loading, empty data, missing fields, partial provider failure, stale data, and failed refresh. State whether partial results may be shown and how they are labeled.

### Q-022 - Make accessibility and responsive acceptance measurable

WCAG 2.1 AA, keyboard access, readable contrast, and tablet support are goals, but viewport sizes, required keyboard flows, chart alternatives, and automated/manual test criteria are absent.

**Clarify**: Define supported viewport widths and critical keyboard paths; require non-color chart/status alternatives, visible focus, semantic labels, and an accessibility test procedure.

### Q-023 - Define performance and freshness expectations

The dashboard is operational and calls external services, but no limits are set for API/UI response time, refresh duration, number of issues/history, cache age, or acceptable data freshness.

**Clarify**: Set expected dataset size and measurable latency/freshness targets for sample mode and Jira mode, plus user-visible behavior when they cannot be met.

### Q-024 - Validate outbound Jira links

Issue `jira_url` values are opened in a new tab, but allowed schemes/hosts and browser link protections are not defined.

**Clarify**: Restrict links to approved HTTPS Jira hosts and specify safe new-tab behavior so untrusted upstream values cannot navigate users to arbitrary schemes or sites.

## Version Decisions

### Q-025 - Pin a reproducible toolchain

The spec records Node.js 24.21.0, npm 11.19.0, and Docker CLI 29.8.1 from an environment report, but does not pin exact React 18, Vite, TypeScript, Express, PostgreSQL 15 image, or Docker Compose versions. Docker CLI version alone does not identify the Compose plugin/runtime.

**Clarify**: Select supported exact versions or controlled semver ranges for each direct dependency and container image, specify the Compose implementation/version, and state which versions are recorded in lockfiles versus developer prerequisites.
