from dataclasses import dataclass
from datetime import date
from typing import Literal, TypedDict

import pandas as pd


StatusCategory = Literal["To Do", "In Progress", "Done", "Blocked"]


class SprintRecord(TypedDict):
    sprint_id: str
    name: str
    start_date: date | None
    end_date: date | None
    capacity_points: float | None


class IssueRecord(TypedDict):
    issue_key: str
    summary: str
    issue_type: str
    status: StatusCategory
    assignee: str | None
    story_points: float | None
    due_date: date | None
    created_at: date | None
    resolved_at: date | None
    jira_url: str | None


class HistorySprintRecord(TypedDict):
    sprint_id: str
    name: str
    start_date: date | None
    end_date: date | None
    committed_points: float | None
    completed_points: float | None


@dataclass(frozen=True)
class SprintDataset:
    sprint: SprintRecord
    issues: pd.DataFrame
    history: pd.DataFrame