# Implementation Tasks: Jira Sprint Progress Dashboard

**Source**: `spec/specification.md`, `spec/plan.md`, and `spec/constitution.md`
**Scope**: Local, single-team, sample-data prototype only.

## Task Rules

- Complete tasks in ID order unless dependencies allow parallel work within the same feature slice.
- Finish and verify one Phase 3 vertical slice before beginning the next. A slice includes its domain behavior, persistence/API path, UI, and focused tests.
- Do not implement live Jira/Confluence integration, shared deployment/authentication, Jira navigation, or pagination in these tasks.
- A task is complete only when its acceptance criteria pass and the change is reviewed against the constitution.

## Phase 1 - Backend Setup (Database and API Skeleton)

- [ ] **T001 Reconcile project authority**
  - Description: Remove conflicting architecture guidance so implementers use one approved source of truth.
  - Dependencies: None.
  - Acceptance Criteria: `spec/specification.md` and `spec/constitution.md` are identified as authoritative for this prototype; `project_spec.md` and `DATA_CONTRACT.md` are updated or clearly marked historical so they no longer prescribe Streamlit/Python or pandas implementation.

- [ ] **T002 Establish npm workspaces and pinned toolchain**
  - Description: Create reproducible workspace package manifests and install scripts for the approved stack.
  - Dependencies: T001.
  - Acceptance Criteria: Root, `backend/`, and `packages/contracts/` manifests define npm workspaces; direct versions match the specification; one root lockfile is committed; `npm ci` succeeds from a clean checkout.

- [ ] **T003 Configure local PostgreSQL service**
  - Description: Provide the local PostgreSQL runtime required by backend persistence and tests.
  - Dependencies: T002.
  - Acceptance Criteria: `docker-compose.yml` defines PostgreSQL `15.14`, binds only `127.0.0.1:5432`, uses a named volume and `pg_isready` health check, and reads secrets from ignored local `.env`; Compose starts a healthy database without hard-coded credentials.

- [ ] **T004 Define shared TypeScript contracts**
  - Description: Define language-level request, response, and data contracts shared by frontend and backend.
  - Dependencies: T002.
  - Acceptance Criteria: `packages/contracts/` exports typed Sprint, Issue, Historical Sprint, Issue Snapshot, Status Mapping, API response, and Error shapes matching the JSON contracts in the specification, including nullable/unmapped values.

- [ ] **T005 Create versioned database migrations**
  - Description: Implement the PostgreSQL schema and database-enforced integrity rules.
  - Dependencies: T003, T004.
  - Acceptance Criteria: Migrations create all six specified tables with primary/foreign keys, nullability, numeric bounds, date checks, one-current-sprint constraint, cascade rules, and query indexes; an invalid-value test confirms constraints reject bad data.

- [ ] **T006 Create representative sample fixtures**
  - Description: Build deterministic, credential-free data that exercises normal and edge-case dashboard behavior.
  - Dependencies: T004.
  - Acceptance Criteria: Fixtures include 11-30 issues, Stories/Tasks/Bugs, mapped and unmapped statuses, missing and zero estimates, all four risk examples, daily snapshots including the sprint-start baseline, and at least three completed historical sprints; no credentials or external confidential data are present.

- [ ] **T007 Implement migration and deterministic seed commands**
  - Description: Make schema setup and sample loading repeatable for developers and tests.
  - Dependencies: T005, T006.
  - Acceptance Criteria: A clean database migrates and seeds through documented npm scripts; running the seed twice produces the same rows without duplicates; startup does not overwrite existing data.

- [ ] **T008 Build Express API skeleton and readiness route**
  - Description: Establish a secure backend process and minimal database-aware HTTP boundary for later feature endpoints.
  - Dependencies: T002, T003, T004, T005.
  - Acceptance Criteria: Express validates required environment variables, binds to loopback, mounts `/api/v1`, returns the standard error envelope, and exposes a readiness route that accurately reports PostgreSQL availability without leaking credentials or stack traces.

**Phase 1 milestone**: A clean install starts PostgreSQL, migrates/seeds sample records, and starts a loopback-only Express skeleton with passing readiness and schema checks.

## Phase 2 - Frontend Setup (UI Skeleton and Routing)

- [ ] **T009 Bootstrap the React and Vite application**
  - Description: Install and configure the version-pinned frontend toolchain and application entry point.
  - Dependencies: T002.
  - Acceptance Criteria: `frontend/` uses React `18.3.1`, Vite `8.3.3`, and TypeScript `7.0.2`; the dev server starts and renders the empty application shell.

- [ ] **T010 Add application routes and root behavior**
  - Description: Establish navigation paths for all specified screens before feature content is added.
  - Dependencies: T009.
  - Acceptance Criteria: Routes exist for `/`, `/sprints/:sprintId`, `/sprints/:sprintId/progress`, `/sprints/:sprintId/issues`, and `/settings/status-mappings`; `/` selects the current sprint or shows an unselected picker; unknown routes show a defined not-found state.

- [ ] **T011 Add typed API client and shared request handling**
  - Description: Create one typed frontend boundary for backend requests and common response/error handling.
  - Dependencies: T004, T008, T009.
  - Acceptance Criteria: Frontend requests target only `/api/v1`; client inputs/outputs use shared contracts; loading, HTTP error, and unavailable-API responses are represented without embedding database or integration secrets in the browser.

- [ ] **T012 Create shared layout and state placeholders**
  - Description: Add reusable page chrome and accessible placeholder states for the UI skeleton.
  - Dependencies: T009, T010.
  - Acceptance Criteria: Each route has a page shell and distinct loading, empty, and error placeholders; controls have labels and visible keyboard focus; no feature calculations or external calls are present.

- [ ] **T013 Add frontend route and shell tests**
  - Description: Verify routing and shared states independently of the backend and database.
  - Dependencies: T010, T011, T012.
  - Acceptance Criteria: Automated tests cover all routes, current/no-current root behavior, not-found state, and mocked API loading/unavailable states; tests pass without PostgreSQL or credentials.

**Phase 2 milestone**: The React shell and all routes render, use the typed backend client, and pass route/state smoke tests.

## Phase 3 - Feature Implementation (One Feature at a Time)

Complete each feature group before starting the next. Each group includes focused domain/API/UI tests and must pass its acceptance criteria before proceeding.

### Feature A - Sprint Selection and Overview

- [ ] **T014 Implement date and sprint-summary calculations**
  - Description: Build provider-independent calculations used by the sprint selector and summary screen.
  - Dependencies: T004, T005, T006.
  - Acceptance Criteria: Unit tests cover UTC/inclusive date calculations, no-issue and zero-denominator behavior, issue-count and story-point progress, unestimated work, health states, and missing data using fixed `asOf` dates.

- [ ] **T015 Implement sprint list and summary data access/API**
  - Description: Connect sprint and summary domain results to PostgreSQL-backed REST endpoints.
  - Dependencies: T008, T014.
  - Acceptance Criteria: `GET /api/v1/sprints` and `GET /api/v1/sprints/{sprintId}/summary` return the specified contracts, order current sprint first, use consistent `asOf`, and return documented 400/404/503 errors.

- [ ] **T016 Implement sprint selector and overview UI**
  - Description: Present selected sprint identity and core progress metrics in the React dashboard.
  - Dependencies: T010, T011, T015.
  - Acceptance Criteria: User can select current or historical sprint and see dates, progress by issue count/points, committed/completed/remaining estimates, unestimated count, health, and no-data explanations; switching sprint updates all values.

- [ ] **T017 Verify overview feature slice**
  - Description: Validate the complete sprint overview journey across domain, API, and UI boundaries.
  - Dependencies: T014, T015, T016.
  - Acceptance Criteria: P1 sprint-health scenarios pass in domain/API/UI tests against PostgreSQL-backed sample data; no live service or credentials are required.

### Feature B - Status Normalization and Issue Details

- [ ] **T018 Implement sample status normalization rules**
  - Description: Normalize configured sample source statuses while preserving unknown statuses as unmapped.
  - Dependencies: T005, T006.
  - Acceptance Criteria: Four default mappings normalize exactly; matching trims whitespace and ignores case; unknown values persist as null normalized status and remain incomplete; unit tests cover invalid and duplicate mappings.

- [ ] **T019 Implement status-mapping API and atomic update**
  - Description: Expose local mapping read/update operations and preserve the previous state if validation or persistence fails.
  - Dependencies: T008, T018.
  - Acceptance Criteria: Mapping GET/PUT endpoints return the specified schemas; invalid or duplicate rows are rejected; a valid replacement re-normalizes issues/snapshots transactionally; a failed update preserves the previous mappings and data.

- [ ] **T020 Implement local status-mapping settings UI**
  - Description: Provide the local operator with an accessible view and editor for sample status mappings.
  - Dependencies: T010, T011, T019.
  - Acceptance Criteria: Operator can view/edit complete sample mappings, receives accessible validation errors, saves valid changes, and sees a clear local-only notice; API failures preserve the displayed saved state.

- [ ] **T021 Implement issue query and filter API**
  - Description: Query normalized sprint issues and apply the documented filter combination and sorting rules.
  - Dependencies: T008, T018.
  - Acceptance Criteria: `GET /api/v1/sprints/{sprintId}/issues` supports status/type/assignee/risk and `asOf`; same-dimension values use OR, dimensions use AND, text matching is trimmed/case-insensitive, output sorts by issue key, and no matches return an empty list.

- [ ] **T022 Implement issue list, details, and filters UI**
  - Description: Let users inspect issue details and narrow the list using the API filters.
  - Dependencies: T011, T020, T021.
  - Acceptance Criteria: User can filter issues and expand details; absent values display as unavailable; unmapped issues have a visible label; Jira URLs are escaped non-clickable text; filters can be cleared by keyboard.

### Feature C - Risk Analysis and Drill-Down

- [ ] **T023 Implement risk and health calculations**
  - Description: Calculate blocked, overdue, scope-change, capacity, and health results independently of UI and persistence.
  - Dependencies: T014, T018.
  - Acceptance Criteria: Unit tests cover blocked, overdue, post-start membership, capacity-over-commitment, missing inputs, removed issues, and unmapped statuses; dates use the shared `asOf` rule.

- [ ] **T024 Implement risk API response**
  - Description: Expose computed risk counts and associated issue keys through the documented API.
  - Dependencies: T015, T021, T023.
  - Acceptance Criteria: Risk endpoint returns counts, calculability/reason, and issue keys; each risk filter yields only matching issues; unavailable risk inputs are not reported as zero.

- [ ] **T025 Implement risk panel and drill-down UI**
  - Description: Show selectable risk signals and connect each selection to the matching issue list.
  - Dependencies: T016, T022, T024.
  - Acceptance Criteria: Blocked, overdue, scope-change, and capacity signals are selectable; selecting a signal filters the list correctly; status meaning is conveyed by text/icon as well as color.

### Feature D - Progress and Burndown

- [ ] **T026 Implement snapshot repository behavior**
  - Description: Read and maintain dated issue snapshots without synthesizing missing observations.
  - Dependencies: T005, T006, T007.
  - Acceptance Criteria: Repository reads complete dated snapshots, identifies effective snapshot date, preserves gaps, and keeps prior snapshots unchanged when current issue membership changes.

- [ ] **T027 Implement planned and actual burndown calculations**
  - Description: Derive burndown series from the baseline and historical snapshots using the approved calendar-day rules.
  - Dependencies: T014, T026.
  - Acceptance Criteria: Tests verify baseline from sprint-start snapshot, calendar-day planned line, issue-count/point actual values, gaps without interpolation, one-day/no-baseline unavailable states, and fixed `asOf` behavior.

- [ ] **T028 Implement burndown API endpoint**
  - Description: Serve validated issue-count or story-point burndown data from the backend.
  - Dependencies: T008, T027.
  - Acceptance Criteria: Endpoint validates metric and sprint ID, returns ordered date points plus availability/reason, and uses the same effective snapshot date as summary and issues.

- [ ] **T029 Implement progress analysis UI**
  - Description: Render both burndown metrics, forecast context, chart filtering, and accessible chart alternatives.
  - Dependencies: T011, T028.
  - Acceptance Criteria: User can switch issue-count/story-point view, inspect planned/actual lines and history reference, see unavailable/gap reasons, access a textual/table chart alternative, and use chart segments to filter issues.

### Feature E - Historical Velocity Forecast

- [ ] **T030 Implement forecast calculation**
  - Description: Calculate estimated-work completion forecasts from the configured eligible historical sprints.
  - Dependencies: T014, T026.
  - Acceptance Criteria: Unit tests select the three-to-five most recent eligible completed sprints, use median points and duration, round forecast days up, return `asOf` for zero remaining work, and explain insufficient history/zero velocity/missing estimates.

- [ ] **T031 Implement forecast API and UI**
  - Description: Expose forecast inputs/results and present the result and limitations in Progress Analysis.
  - Dependencies: T028, T030.
  - Acceptance Criteria: Forecast endpoint returns all specified fields and stable unavailable reasons; Progress Analysis displays forecast date, reference velocity, and the limitation for unestimated incomplete issues.

### Feature F - Refresh Lifecycle

- [ ] **T032 Implement transactional per-sprint fixture refresh**
  - Description: Reimport one sample sprint and its snapshots atomically while preserving prior successful data on failure.
  - Dependencies: T007, T026.
  - Acceptance Criteria: Refresh replaces the selected sprint's sample data and snapshots atomically, serializes concurrent requests, records succeeded/failed metadata, and preserves previous data if the operation fails.

- [ ] **T033 Implement refresh API behavior**
  - Description: Add the synchronous refresh endpoint with conflict and failure reporting.
  - Dependencies: T008, T032.
  - Acceptance Criteria: Successful refresh returns 200 with completion time; concurrent refresh returns 409; database/provider failure returns 503 with sanitized error and leaves last-success timestamp unchanged.

- [ ] **T034 Implement refresh UI and persisted startup behavior**
  - Description: Load existing database state on startup and expose manual refresh with clear freshness feedback.
  - Dependencies: T016, T033.
  - Acceptance Criteria: App startup reads stored sample data without overwriting it; user can refresh selected sprint; UI shows last successful import, stale data, loading, and failed-refresh states distinctly.

**Phase 3 milestone**: All seven workflows are implemented as tested domain-to-database-to-API-to-UI slices; P1/P2 acceptance scenarios pass.

## Phase 4 - Integration and Testing

- [ ] **T035 Add end-to-end prototype workflow tests**
  - Description: Verify complete user journeys against the composed frontend, backend, and PostgreSQL stack.
  - Dependencies: T017, T022, T025, T029, T031, T034.
  - Acceptance Criteria: A clean local run covers sprint selection, overview, issue/risk filtering, burndown, forecast, refresh, and status mapping against PostgreSQL.

- [ ] **T036 Verify failure, stale-data, and error contracts**
  - Description: Exercise degraded dependencies and boundary errors through the integrated system.
  - Dependencies: T035.
  - Acceptance Criteria: Tests cover unavailable PostgreSQL, failed/overlapping refresh, missing snapshots, unmapped status, invalid filters, unknown sprint, and stable error codes/statuses; failures never appear as success.

- [ ] **T037 Complete accessibility verification**
  - Description: Validate assistive and keyboard use across all primary screens and controls.
  - Dependencies: T035.
  - Acceptance Criteria: axe-core reports zero critical/serious violations on primary routes; manual keyboard checks pass for routes, filters, issue expansion, charts, refresh, and mapping; chart/status content has non-color text equivalents.

- [ ] **T038 Verify responsive layouts**
  - Description: Check desktop and tablet viewport behavior for layout, readability, and control access.
  - Dependencies: T035.
  - Acceptance Criteria: At 768 px, 1024 px, and 1440 px, all primary content remains readable without horizontal overlap; all controls remain reachable and text fits its container.

- [ ] **T039 Measure prototype performance**
  - Description: Measure API latency and first usable dashboard render at the specified sample-data ceiling.
  - Dependencies: T035.
  - Acceptance Criteria: At the maximum sample dataset (30 issues/sprint, 12 historical sprints), API p95 is <= 500 ms and usable dashboard content renders within 2 seconds on the documented development setup.

- [ ] **T040 Run secret and network-boundary checks**
  - Description: Confirm credentials remain server-side and local services are not exposed beyond loopback.
  - Dependencies: T035.
  - Acceptance Criteria: No credential appears in source, fixtures, built frontend, or logs; PostgreSQL, Express, and Vite listen only on loopback; browser requests use only the backend API.

- [ ] **T041 Document clean setup and reset**
  - Description: Document repeatable local development and explicit database reset workflows.
  - Dependencies: T035.
  - Acceptance Criteria: Documentation covers `npm ci`, Compose startup, migrations, seed, frontend/backend start, tests, refresh, volume persistence, and explicit destructive reset; a second developer can follow it without Jira/Confluence credentials.

- [ ] **T042 Release acceptance gate**
  - Description: Evaluate all final success criteria and block release on any unmet requirement.
  - Dependencies: T036, T037, T038, T039, T040, T041.
  - Acceptance Criteria: Every success criterion in `spec/specification.md` passes from a clean local setup; unresolved failures are recorded as blockers, and no out-of-scope integration or shared deployment has been added.

**Phase 4 milestone**: Integrated prototype passes end-to-end, reliability, accessibility, responsive, performance, security, and clean-setup gates.

## Environment Blocker

The last environment check found Docker Desktop installed but its daemon unavailable and WSL not installed. Resolve Docker/WSL startup before T003 can pass; an in-memory database is not an acceptable substitute for PostgreSQL in this plan.