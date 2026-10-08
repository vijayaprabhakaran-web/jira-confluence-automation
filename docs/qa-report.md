# QA Report

**Application:** Sprint Atlas | Progress Dashboard

**Date:** 2026-10-08

**Environment:** Chrome; frontend at `http://127.0.0.1:5173/`, backend at `http://127.0.0.1:3001`, PostgreSQL at `127.0.0.1:5432`
**Overall status:** Partial pass. The Status mapping UI flow passes. The sprint overview does not expose sprint selection, and two other views remain placeholders.

## Pages Tested

- **Sprint overview** (`/`): Loaded successfully. Summary metrics and issue panels showed placeholders and "No sprint selected"; there is no sprint selector. [Screenshot](qa-sprint-overview.png)
- **Progress analysis** (`/sprints/current/progress`): Loaded successfully, but the content is a placeholder saying "Select a sprint to load this view." [Screenshot](qa-progress-analysis.png)
- **Risks and issues** (`/sprints/current/issues`): Loaded successfully, but the content is a placeholder saying "Select a sprint to load this view." [Screenshot](qa-risks-and-issues.png)
- **Status mapping** (`/settings/status-mappings`): Initially rendered a placeholder. After the fix, it loads four mappings and provides editable source-status fields, normalized-status selectors, add/remove controls, and a save action. [Desktop screenshot](qa-status-mapping.png); [mobile screenshot](qa-status-mapping-mobile.png).

Shared navigation, the API connection indicator, and the **Check connection** button were visible across the pages.

## Interactive Tests

- Opened each primary navigation route and confirmed its rendered state.
- Clicked **Check connection**; the page continued to show **API connected**.
- On Status mapping, verified four existing rows load, added a temporary source status, selected **In Progress**, and clicked **Save mappings**. The UI displayed "Status mappings saved." A follow-up API read confirmed the test mapping persisted.
- Removed the temporary row, clicked **Save mappings** again, then reloaded the page. The original four mappings were present and the test row was absent.
- Separately submitted a temporary mapping through the API and restored the original set afterward.
- Added a blank row and submitted it; the form rejected it with "Enter a source status for every row."
- Added a source status differing from an existing value only by case (`blocked` vs `Blocked`) and submitted it; the form rejected it as a duplicate.
- Simulated a transient failure on the mapping-load request; the page displayed "Failed to fetch" and **Retry**. Clicking **Retry** successfully loaded all four mappings.
- Emulated a 390x844 mobile viewport. The document width remained 390px with no horizontal overflow; the 12 form controls had no overlapping bounding boxes.
- Re-read the mappings after the negative and retry tests: four original entries remained and no temporary test entry remained.

## Additional Test Cases (Executed)

| ID | Test | Expected result | Result |
| --- | --- | --- | --- |
| QA-01 | Submit a blank source-status row | Inline validation blocks save | Pass; "Enter a source status for every row." |
| QA-02 | Submit a duplicate source status with different casing | Duplicate validation blocks save | Pass; "blocked" is identified as a duplicate of "Blocked." |
| QA-03 | Fail the initial mapping GET, then retry | Error state is shown and retry reloads mappings | Pass; retry loaded all four mappings. Failure was injected in Chrome; backend was not stopped. |
| QA-04 | Inspect the form at 390x844 | No horizontal overflow or control overlap | Pass; document width 390px, zero overlapping controls. [Screenshot](qa-status-mapping-mobile.png) |
| QA-05 | Check persisted data after tests | Original four mappings remain, test rows absent | Pass; API returned four mappings and no test entry. |

## Bugs Found

Severity uses Blocker / High / Medium / Low. Screenshots show the current state; the pre-fix Status mapping placeholder was observed during the session but was not archived as a PNG.

- **High - Sprint dashboard cannot select or load a sprint.** `GET /api/v1/sprints` returns four sample sprints, but the overview makes no request for them and shows no selector. Its metrics and work panels stay empty. Evidence: [Sprint overview screenshot](qa-sprint-overview.png).
- **High - Progress analysis and Risks and issues are unimplemented placeholders.** Both routes instruct the user to select a sprint but expose no selector or data controls. Evidence: [Progress analysis](qa-progress-analysis.png) and [Risks and issues](qa-risks-and-issues.png).
- **High - Status mapping had no UI to edit or submit mappings.** The route initially displayed a generic placeholder despite a working backend endpoint. Fixed during this session. Evidence of the corrected page: [Status mapping after fix](qa-status-mapping.png). No pre-fix screenshot was saved.

## Fixes Applied

- Replaced the Status mapping placeholder with an editor that loads and saves through the existing API, supports add/edit/remove, offers the four normalized statuses, validates empty and duplicate source statuses, reports save/load errors, and provides a retry action. Added responsive styling.
- Added the frontend API client calls for `GET` and `PUT /api/v1/status-mappings` and mounted the editor on `/settings/status-mappings`.
- **Commit reference:** No commit was created. These changes are uncommitted in the working tree; there is no fix commit SHA. Current `HEAD` at review time: `0151d46` (`docs: add reports and prototype planning specs`), which does not contain this fix.

## Current Status

- **Passing:** Frontend build; browser status-mapping add/edit/select/save/remove/reload flow; empty and case-insensitive duplicate validation; injected mapping-load failure and retry; mobile overflow/overlap check; database-backed health check; frontend home response; sprint-list and status-mapping API reads; clean browser console; editor diagnostics; `git diff --check`.
- **Known issues:** Sprint overview still cannot select a sprint or consume the available sprint list. Progress analysis and Risks and issues remain placeholders. These prevent a full dashboard workflow despite the Status mapping fix.
- **Not exercised:** A real backend outage/HTTP 5xx and touch interactions on a physical mobile device. No frontend automated test suite was run; verification used the production build and Chrome interaction checks.
