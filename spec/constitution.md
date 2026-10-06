# Project Constitution

This constitution sets the engineering principles for the Jira and Confluence automation project. Feature specifications and implementation plans must follow it or explicitly propose an amendment.

## Core Principles

### I. Specify Before Building

Every feature must have a reviewed specification describing user value, scope, acceptance criteria, important data cases, and failure behavior before implementation begins. Plans and tasks must trace back to that specification. Do not silently expand scope.

### II. Secure Integrations by Default

Jira, Confluence, database, and other service credentials must remain server-side and come from environment configuration or an approved secret store. Never commit, expose to the browser, or write credentials to logs. Use the least API permissions necessary, and treat issue and page content as internal data.

### III. Make Automation Explicit and Safe

Integrations are read-only unless a feature specification explicitly authorizes a write operation. For authorized writes, validate inputs, make retries safe where possible, and record an auditable outcome. Bulk or destructive actions require a preview and explicit confirmation. Never hide partial failures or report success when an external change is uncertain.

### IV. Preserve Contracts and Provider Boundaries

Sample data, Jira, and Confluence adapters must be separate from domain calculations and application workflows. They must map external data to documented internal contracts. Normalize workflow states through configuration rather than embedding provider-specific status names in calculations. Preserve missing values as missing; do not silently coerce unknown or unestimated data to zero.

### V. Keep the Approved Stack and Boundaries

- Frontend: React 18 with Vite.
- Backend: Node.js with Express.
- Database: PostgreSQL 15, run through Docker Compose for local development.
- The browser communicates with application services through the backend API; it must not connect directly to PostgreSQL or call Jira/Confluence with privileged credentials.

Technology changes require an explicit design decision and updates to affected specifications. The current `project_spec.md` still describes a Streamlit/Python implementation; reconcile it with this stack before implementation rather than maintaining two competing architectures.

### VI. Protect Data Integrity

Validate external input at system boundaries and enforce important invariants in both application logic and the database where appropriate. Use versioned database migrations. Keep date-only values distinct from timestamps, and preserve documented nullability and meaning across API, application, and database layers.

### VII. Design for Reliable External Services

Handle pagination, rate limits, timeouts, authentication failures, and upstream outages explicitly. Retry only transient failures and only when repeating the operation is safe. Return clear errors and freshness information; do not silently substitute stale, partial, or fabricated data.

### VIII. Verify Behavior at Each Boundary

Test domain calculations independently, API behavior at route and service boundaries, and persistence against PostgreSQL 15. Mock or contract-test Jira and Confluence integrations so tests do not require live credentials. A feature is complete only when its acceptance criteria and relevant tests pass.

### IX. Make the Interface Accessible

Target WCAG 2.1 AA. Core workflows must support keyboard use, readable contrast, clear labels, and status indicators that do not rely on color alone. Keep the desktop-first layout usable at tablet widths without overlapping content.

## Governance

Before implementation, check the feature specification and plan against each relevant principle. When requirements conflict with this constitution or existing project documents, resolve the conflict explicitly before coding. Amend this constitution through a reviewed change and update dependent specifications when principles or the approved stack change.