# Instructions Catalog

Use this catalog to select the project workflow instruction matching the request. Load the linked instruction completely when its keywords match.

- [`./creating-instructions.agent.md`](./creating-instructions.agent.md) — create and maintain project instructions and their routing.
  + Keywords: instructions, instruction setup, Copilot configuration, prompt wrapper
- [`./implement-core-feature.agent.md`](./implement-core-feature.agent.md) — implement a focused Jira dashboard core feature from the backlog and validate it.
  + Keywords: implement feature, core feature, dashboard, backlog
  + Target: `backlog.md`, `project_spec.md`, `DATA_CONTRACT.md`
- [`./calculate-compound-interest.agent.md`](./calculate-compound-interest.agent.md) — calculate compound interest with the project CLI and present its output.
  + Keywords: compound interest, interest calculation, final amount, interest earned
  + Target: `tools/compound_interest.py`
- [`./use-calculate-sprint-work.agent.md`](./use-calculate-sprint-work.agent.md) — use the sprint-work CLI to report supplied sprint totals and missing metrics.
  + Keywords: sprint work, committed points, completed points, unestimated issues
  + Target: `tools/calculate_sprint_work.py`
- [`./create-status-report.agent.md`](./create-status-report.agent.md) — generate concise weekly status reports from provided project facts.
  + Keywords: status report, weekly report, team update
  + Target: `reports/**/*.md`, `backlog.md`, `TODO.md`