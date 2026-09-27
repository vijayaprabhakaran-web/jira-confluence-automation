# Engineering Status Report

**Project:** Jira Sprint Progress Dashboard
**Report owner:** Product Engineering Team
**Reporting period:** September 21 - September 25, 2026
**Overall status:** Amber

## Highlights
- Agreed on the first-release scope for a desktop-first dashboard covering one team's current and historical sprints.
- Documented how issue-count progress, story-point progress, unestimated work, and risk signals should be presented.

## Delivery Updates
- **Requirements baseline:** Complete. The initial specification covers sprint summary, progress analysis, risk analysis, issue details, filtering, and accessibility requirements.
- **Sample data and calculation rules:** In progress. The data set and calculation behavior are being shaped to include unestimated, blocked, overdue, and added-after-start issues.
- **Dashboard prototype:** Not started. Implementation is planned after the sample-data contract and calculation tests are agreed.

## Risks and Dependencies
- **Velocity forecast depends on representative historical sprint data:** Without enough completed sprint history, the forecast could be misleading. The team will label forecasts as unavailable when evidence is insufficient and include this case in test data. **Owner:** Data and calculations lead.
- **Decision needed:** Confirm which workflow statuses map to To Do, In Progress, Done, and Blocked before connecting live Jira data. **Decision-maker:** Scrum master. **Needed by:** October 2, 2026.

## Focus for Next Week
- Finalize the normalized sample-data contract, including optional story points, due dates, and issue creation dates.
- Implement and test progress and risk calculations using representative sprint scenarios.
- Build the first dashboard view with sprint summary metrics and a readable issue list.