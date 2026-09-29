---
agent: agent
---
Implement the burndown data-model backlog task using `./instructions/implement-burndown-model.agent.md`.

Use Approach 2: Iterative Reread. Work one file at a time, and for each pass:

1. Read the entire file and the directly relevant contract or specification before changing it.
2. Make the smallest focused change in that file only.
3. Run the narrowest relevant check immediately after the change.
4. Reread the changed file and compare it with the requirements and test result.
5. Record the file, change, check, and any remaining issue before moving to the next file.

Start with `burndown.py`, then add or update `tests/test_burndown.py`. Do not change the dashboard, shared contract, or unrelated files unless a concrete requirement demands it. Continue through the implementation and focused validation without waiting for approval between files. If a check fails, repair that file and rerun the same check before proceeding. Do not mark the backlog task complete unless its focused tests pass.

At the end, report `Implemented`, `Files`, `Validation`, and `Remaining`, including each file's check result and any unresolved assumptions.