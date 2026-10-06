# Implementation Plan: Jira Sprint Progress Dashboard

**Source**: `spec/specification.md` and `spec/constitution.md`
**Status**: Draft implementation sequence
**Scope**: Local, single-team, sample-data prototype. Live Jira/Confluence integration, shared deployment, authentication, external link navigation, and pagination are excluded.

## Approach

Follow four dependency-ordered phases: establish the backend and database contract; set up the frontend shell and routes; implement one user-facing feature at a time as a backend-to-UI vertical slice; then run full integration, accessibility, performance, and security checks. Each milestone has an exit gate. Keep unit and feature tests inside the phase where the behavior is built; Phase 4 adds full-system verification rather than postponing all tests until the end.

## Phases and Milestones

### Phase 1 - Backend Setup (Database and API Skeleton)

**Work**

- Reconcile or retire the legacy Streamlit/Python `project_spec.md` and pandas `DATA_CONTRACT.md`; treat `spec/specification.md` and `spec/constitution.md` as authoritative.
- Populate the root, `backend/`, and `packages/contracts/` npm workspace manifests; pin the approved versions and commit the exact npm lockfile.
- Configure PostgreSQL 15.14 through Docker Compose on `127.0.0.1:5432`, with a named volume, `pg_isready` health check, and ignored local `.env` support.
- Add Express startup, validated environment configuration, loopback binding, common error envelope, and an API router skeleton under `/api/v1`. Add a health/readiness route that reports database readiness without exposing secrets.
- Define shared TypeScript contracts for sprints, issues, history, issue snapshots, mappings, API responses, and errors in `packages/contracts/`.
- Add versioned migrations for all six specified tables, constraints, indexes, current-sprint uniqueness, and foreign-key deletion policies.
- Add deterministic sample fixtures, idempotent seeding, and database scripts. Do not add live Jira or Confluence clients.

**Milestone M1 - Backend foundation ready**

- A clean `npm ci` succeeds from the root using the pinned lockfile.
- Compose starts healthy PostgreSQL 15.14 with its port bound only to loopback.
- Migrations and repeatable sample seed succeed; schema constraints are tested.
- The Express skeleton starts on loopback and reports database readiness; no external credentials are required.

### Phase 2 - Frontend Setup (UI Skeleton and Routing)

**Work**

- Populate `frontend/package.json` with the pinned React 18.3.1, Vite 8.3.3, and TypeScript 7.0.2 toolchain.
- Create the Vite entry point, React application shell, typed API client, route handling, shared layout, and common loading/error/empty-state components.
- Add routes for `/`, `/sprints/:sprintId`, `/sprints/:sprintId/progress`, `/sprints/:sprintId/issues`, and `/settings/status-mappings`.
- Implement root routing behavior: open the current sprint when set; otherwise show the sprint picker without selecting a sprint.
- Add frontend test setup and route-level skeleton tests using a mocked API; keep all pages as placeholders in this phase.
- Verify the frontend calls only the backend API and contains no database or integration credentials.

**Milestone M2 - Frontend shell ready**

- Vite serves the React shell; all specified routes render their placeholder states and unknown routes have a defined fallback.
- API client can reach the backend readiness endpoint and reports loading/unavailable states correctly.
- Route and accessibility smoke tests pass at the shell level; no feature calculations are implemented yet.

### Phase 3 - Feature Implementation (One Feature at a Time)

Implement each feature completely across domain logic, repository/API, UI, and tests before starting the next. Keep the slices small; do not build all backend features first and defer all frontend work.

1. **Sprint selection and overview (P1)**: list/current sprint selection; sprint summary, dates, issue-count and point progress, unestimated work, health, and no-data states. Add domain, API, UI, and acceptance tests.
2. **Status normalization and issue details (P1/P2)**: default sample mappings, nullable unmapped status behavior, issue list/detail, filtering by status/type/assignee, and source URL as escaped non-clickable text. Add mapping and filter tests.
3. **Risk analysis and drill-down (P1)**: blocked, overdue, scope-added, and capacity signals; consistent `asOf`; risk filters and metric/chart selection behavior. Test missing data, removed scope, and unmapped issues.
4. **Progress and burndown (P1)**: complete daily snapshots, baseline, actual and planned lines, issue-count/story-point toggle, gaps for missing observations, and textual chart alternative. Add snapshot and boundary tests.
5. **Historical-velocity forecast (P2)**: eligible historical sprint selection, median velocity/duration, forecast date, and unavailable/zero-remaining/unestimated states. Add deterministic calculation and API/UI tests.
6. **Refresh lifecycle (P2)**: load persisted data at startup; manual per-sprint sample reimport, transaction rollback, last-success timestamp, concurrent-refresh handling, and stale/failed UI states.
7. **Status mapping settings (P2)**: editable local mappings, validation, transactional re-normalization, duplicate rejection, and settings UI. Confirm the settings route remains local-only.

For each slice, use fixed fixtures and `asOf` dates, validate the feature against its independent acceptance scenarios, and keep contract tests between frontend, API, and database aligned.

**Milestone M3 - Feature slices complete**

- All seven specified workflows work against seeded PostgreSQL through the documented API.
- Every P1/P2 acceptance scenario has a passing test at the domain, API, and relevant UI boundary.
- Each slice preserves null/missing-value semantics, and no feature introduces external Jira/Confluence access or shared-network exposure.

### Phase 4 - Integration and Testing

**Work**

- Run a clean-machine flow: install from lockfile, start Compose DB, migrate, seed, start backend and frontend, and complete each user journey.
- Add end-to-end tests for sprint selection, summary, chart filters, risk drill-down, issue expansion, refresh, and status-mapping updates.
- Verify failed refresh rollback, unavailable DB/provider states, common `asOf` behavior, stale snapshots, and stable HTTP/error contracts.
- Run axe-core on primary routes with zero critical/serious violations; manually test keyboard access, focus, accessible chart alternatives, and status meaning without color.
- Check layouts at 768 px, 1024 px, and 1440 px, with no horizontal overlap.
- Measure maximum sample workload against API p95 <= 500 ms and usable dashboard render <= 2 seconds.
- Scan source, fixtures, lockfiles, logs, and built frontend output for credentials; verify all app/database listeners are loopback-only.
- Document startup, migration, seed, test, refresh, and destructive reset procedures. Record failures as release blockers rather than lowering criteria silently.

**Milestone M4 - Integrated prototype accepted**

- All specification success criteria pass against a clean local setup.
- The complete dashboard works with PostgreSQL and sample data and requires no Jira/Confluence credentials.
- No critical/serious accessibility violations, performance failures, leaked credentials, or non-loopback listeners remain.

## Verification Gates

1. **M1**: clean install, database health, migration/seed repeatability, schema constraints, API readiness, loopback binding.
2. **M2**: frontend route tests, mocked API states, shell-level accessibility and credential boundary.
3. **M3**: feature-by-feature domain/unit, API integration, and UI acceptance tests; do not advance a slice with failing tests.
4. **M4**: complete end-to-end suite, axe-core/manual keyboard checks, viewport, performance, clean setup, and secret scan.

## Dependencies and Risks

- **Docker engine prerequisite**: The last environment check found Docker Desktop installed but its daemon unavailable and WSL not installed. Resolve Docker/WSL startup before M1 can pass; do not substitute an in-memory database because PostgreSQL persistence is required.
- **Legacy documentation**: `project_spec.md` and `DATA_CONTRACT.md` still describe Streamlit/Python and pandas. Reconcile or retire them in Phase 1 to prevent conflicting contracts.
- **Historical data quality**: Burndown depends on daily snapshots and the sprint-start baseline. Missing fixture observations must display as gaps/unavailable rather than being synthesized.
- **Local-only security boundary**: No authentication is planned. Binding to loopback is a release requirement; shared deployment requires a separate security specification.

## Explicitly Excluded

Live Jira or Confluence integrations, OAuth/shared-user authentication, external navigation to Jira, writeback, real-time streaming, multi-team comparison, pagination, and shared deployment are not milestones in this plan. Each requires a separate specification before work begins.