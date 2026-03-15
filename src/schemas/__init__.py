# src/schemas — Pydantic Data Models
#
# This package defines the data contracts for the entire project.
# Every structured input/output flows through models defined here.
#
# Exports:
#   - BugReport: Input model for raw bug report data
#   - TriageResult: Output model (JSON contract for Jira/GitHub Issues)
#   - DuplicateMatch: Model for duplicate detection results

from src.schemas.bug_report import BugReport
from src.schemas.triage_output import TriageResult
from src.schemas.duplicate_result import DuplicateMatch

__all__ = ["BugReport", "TriageResult", "DuplicateMatch"]
