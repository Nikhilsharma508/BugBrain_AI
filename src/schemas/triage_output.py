"""
src/schemas/triage_output.py — Triage Result Output Model
----------------------------------------------------------
PURPOSE:
    Defines the structured JSON output the pipeline produces.
    This is the contract that the LLM must follow.
    Downstream tools (Jira, GitHub Issues, Streamlit UI) consume this.

OUTPUT FIELDS:
    - issue_summary: one-line technical summary
    - steps_to_reproduce: ordered list (or "Not provided by user")
    - technical_details: error info, environment, key stack frames
    - severity: P1/P2/P3/P4
    - suggested_owner: team name from policies

CONNECTS TO:
    - extraction_agent.py produces partial TriageResult (summary, steps, tech details)
    - triage_agent.py enriches it with severity + suggested_owner
    - orchestrator.py returns the final TriageResult
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class TechnicalDetails(BaseModel):
    """Technical information extracted from the bug report."""

    detected_error: str = Field(
        default="Not identified",
        description="Primary exception or error class name",
    )
    error_message: str = Field(
        default="Not identified",
        description="Error message or description",
    )
    environment: str = Field(
        default="Not identified",
        description="Platform, OS, or runtime environment mentioned",
    )
    key_stack_frames: List[str] = Field(
        default_factory=list,
        description="Most relevant stack trace lines (max 5)",
    )


class ExtractionResult(BaseModel):
    """Structured output of the bug extraction pipeline."""

    issue_summary: str = Field(
        description="One-line technical summary of the bug",
    )
    steps_to_reproduce: List[str] = Field(
        default_factory=lambda: ["Not provided by user"],
        description="Ordered reproduction steps. If not available, say 'Not provided by user'",
    )
    technical_details: TechnicalDetails = Field(
        default_factory=TechnicalDetails,
        description="Extracted technical information",
    )
    signals: dict = Field(
        default_factory=dict,
        description="Extracted log signals (exceptions, error messages, key stack frames, timestamps)",
    )

class ClassificationResult(BaseModel):
    """Structured output of the triage policy pipeline."""

    severity: str = Field(
        default="P3 (Medium)",
        description="Severity level: P1 (Critical), P2 (High), P3 (Medium), or P4 (Low)",
    )
    suggested_owner: str = Field(
        default="Platform-Team",
        description="Team name responsible for this bug",
    )

class TriageResult(BaseModel):
    """Final combined output containing both Extraction and Classification."""
    
    issue_summary: str = Field(description="One-line technical summary of the bug")
    steps_to_reproduce: List[str] = Field(description="Ordered reproduction steps")
    technical_details: TechnicalDetails = Field(description="Extracted technical information")
    severity: str = Field(description="Severity level")
    suggested_owner: str = Field(description="Team name responsible for this bug")
