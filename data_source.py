from datetime import date, timedelta

import pandas as pd

from data_contract import SprintDataset


def load_sample_data(today: date | None = None) -> SprintDataset:
    dashboard_date = today or date.today()
    sprint_start = dashboard_date - timedelta(days=7)
    sprint_end = dashboard_date + timedelta(days=7)

    def sprint_day(offset: int) -> date:
        return sprint_start + timedelta(days=offset)

    def dashboard_day(offset: int) -> date:
        return dashboard_date + timedelta(days=offset)

    issue_rows = [
        ("PROJ-101", "Account recovery flow", "Story", "Done", "Mina Patel", 5, 2, -6, -2),
        ("PROJ-102", "Audit event schema", "Task", "Done", "Jordan Lee", 3, None, -6, -1),
        ("PROJ-103", "Mobile session refresh", "Story", "In Progress", "Sam Rivera", 8, 1, -5, None),
        ("PROJ-104", "Fix duplicate notifications", "Bug", "Blocked", "Mina Patel", 3, -2, -5, None),
        ("PROJ-105", "Admin export permissions", "Story", "In Progress", "Alex Chen", 5, 5, -4, None),
        ("PROJ-106", "Document API limits", "Task", "To Do", "Jordan Lee", 2, None, -4, None),
        ("PROJ-107", "Search index tuning", "Task", "Done", "Sam Rivera", 3, None, -3, -1),
        ("PROJ-108", "Workspace invite controls", "Story", "In Progress", "Alex Chen", 8, 6, -3, None),
        ("PROJ-109", "Correct timezone display", "Bug", "To Do", "Mina Patel", None, None, -2, None),
        ("PROJ-110", "Bulk member updates", "Story", "In Progress", "Jordan Lee", 5, 3, -2, None),
        ("PROJ-111", "Usage report filters", "Story", "To Do", "Sam Rivera", 8, 8, -1, None),
        ("PROJ-112", "Retry failed webhooks", "Task", "Blocked", "Alex Chen", 3, -1, -1, None),
        ("PROJ-113", "Account lockout message", "Bug", "Done", "Mina Patel", 2, None, 0, -3),
        ("PROJ-114", "Add team activity view", "Story", "In Progress", "Jordan Lee", 5, 4, 2, None),
        ("PROJ-115", "Webhook delivery metrics", "Task", "To Do", "Sam Rivera", None, 9, 3, None),
        ("PROJ-116", "Refresh token rotation", "Story", "To Do", "Alex Chen", 8, 7, 4, None),
        ("PROJ-117", "Clarify billing error copy", "Bug", "In Progress", "Mina Patel", 2, 2, 5, None),
        ("PROJ-118", "Remove deprecated setting", "Task", "To Do", "Jordan Lee", None, None, 6, None),
    ]

    issues = pd.DataFrame(
        [
            {
                "issue_key": key,
                "summary": summary,
                "issue_type": issue_type,
                "status": status,
                "assignee": assignee,
                "story_points": points,
                "due_date": dashboard_day(due_offset) if due_offset is not None else None,
                "created_at": sprint_day(created_offset),
                "resolved_at": dashboard_day(resolved_offset) if resolved_offset is not None else None,
                "jira_url": f"https://example.atlassian.net/browse/{key}",
            }
            for key, summary, issue_type, status, assignee, points, due_offset, created_offset, resolved_offset in issue_rows
        ]
    )

    history = pd.DataFrame(
        [
            {
                "sprint_id": f"sprint-{number}",
                "name": f"Platform Sprint {number}",
                "start_date": sprint_start - timedelta(days=14 * (4 - number)),
                "end_date": sprint_start - timedelta(days=14 * (3 - number)) - timedelta(days=1),
                "committed_points": committed,
                "completed_points": completed,
            }
            for number, committed, completed in [(21, 48, 44), (22, 52, 50), (23, 46, 38)]
        ]
    )

    sprint = {
        "sprint_id": "sprint-24",
        "name": "Platform Sprint 24",
        "start_date": sprint_start,
        "end_date": sprint_end,
        "capacity_points": 50,
    }
    return SprintDataset(sprint=sprint, issues=issues, history=history)