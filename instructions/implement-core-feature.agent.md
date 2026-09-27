---
name: Implement Core Feature
description: "Implement Jira Sprint Progress Dashboard core features from the backlog with focused tests and validation."
user-invocable: true
---
- Use this instruction for requests to implement unchecked items under `## Core Features` in `backlog.md`.
- Input format:
  + Name the backlog item or describe the required behavior; optionally provide acceptance criteria, priority, and constraints.
  + If asked generally to implement core features, choose the smallest coherent next unchecked item in backlog order and honor its dependencies.
- Processing steps:
  + Read the relevant backlog item, `project_spec.md`, `DATA_CONTRACT.md`, `data_contract.py`, and nearby implementation and tests.
  + Confirm the behavior and the cheapest focused validation before editing.
  + Implement the smallest complete feature slice; keep calculations independent of Streamlit and data-source adapters.
  + Add or update focused tests for expected behavior and relevant edge cases, then run them.
  + Mark a backlog item complete only after implementation and focused validation pass.
- Output format:
  + Return concise Markdown bullets for `Implemented`, `Files`, `Validation`, and `Remaining`.
  + Identify any incomplete work or failed checks; do not claim a feature is complete unless its acceptance criteria are verified.
- Constraints:
  + Treat `project_spec.md` and the shared data contract as authoritative; preserve nullable estimates and actual sprint dates.
  + Keep the sample-data MVP usable without Jira credentials; do not start Jira Cloud integration unless explicitly requested.
  + Preserve accessibility requirements, including keyboard operation and status cues that do not rely on color alone.
  + Avoid unrelated refactors and do not mark follow-on backlog items complete without implementing them.