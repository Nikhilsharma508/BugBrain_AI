"""
src/schemas/bug_report.py — Bug Report Input Model
----------------------------------------------------
PURPOSE:
    Defines the input data model for a bug report.
    Maps to the columns in Data/bug_report.csv:
        - Id: report identifier
        - Bug Details: raw text of the bug report
        - User Review: optional user commentary (how it happened, context)

CONNECTS TO:
    - orchestrator.py reads CSV rows and creates BugReport instances
    - PipelineState carries these fields through the graph
"""

from pydantic import BaseModel, Field
from typing import Optional


class BugReport(BaseModel):
    """Input model representing a single bug report from the CSV."""

    id: int = Field(description="Bug report ID from the CSV")
    bug_trace: str = Field(description="Raw bug report text (Bug Details column)")
    user_review: Optional[str] = Field(
        default=None,
        description="Optional user commentary providing extra context (User Review column)",
    )
