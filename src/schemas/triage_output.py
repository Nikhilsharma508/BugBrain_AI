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
        description="The specific error message or description accompanying the error",
    )
    environment: str = Field(
        default="Not identified",
        description="The platform, OS, browser, or runtime environment mentioned where the bug occurred",
    )
    timestamp: str = Field(
        default="Not identified",
        description="The exact date/time the error occurred, extracted directly from the logs or report",
    )
    key_stack_frames: List[str] = Field(
        default_factory=list,
        description="The most relevant stack trace lines pointing to the failure origin",
    )


class ExtractionResult(BaseModel):
    """Structured output of the bug extraction pipeline."""

    issue_summary: str = Field(
        description="Start with 'Error' or 'Warning: <ExceptionType>' followed by a concise, natural summary of what failed, why it failed, and when it occurs."
    )

    steps_to_reproduce: List[str] = Field(
        default_factory=lambda: ["Not provided by user"],
        description="Ordered, step-by-step actions required to reproduce the bug. Reconstruct these from the user narrative if possible. If completely missing, output ['Not provided by user'].",
    )
    user_impact_assessment: str = Field(
        default="Unknown",
        description="A short summary of how many users this affects and how severely it blocks their workflows, based purely on the text.",
    )
    technical_details: TechnicalDetails = Field(
        default_factory=TechnicalDetails,
        description="Detailed technical information including errors, stack traces, and environment variables.",
    )


class ClassificationResult(BaseModel):
    """Structured output of the triage policy pipeline."""

    model_config = {"extra": "ignore"}

    triage_reasoning: str = Field(
        description="Step-by-step logical justification for the chosen severity and owner, referencing specific policies.",
    )
    severity: str = Field(
        default="P3 (Medium)",
        description="The assigned severity level based strictly on the provided policy: P1 (Critical), P2 (High), P3 (Medium), P4 (Low), or N/A (Not Related).",
    )
    suggested_owner: str = Field(
        default="Platform-Team",
        description="The engineering team responsible for addressing this bug, based strictly on the provided routing keywords or Out-of-Scope.",
    )


class TriageResult(BaseModel):
    """Final combined output containing both Extraction and Classification."""

    issue_summary: str = Field(
        description="One line formatted as 'Error: <ExceptionType> <technical summary>', describing the bug, its cause, and when it occurs."
    )
    steps_to_reproduce: List[str] = Field(description="Ordered reproduction steps")
    user_impact_assessment: str = Field(description="Assessment of user impact")
    technical_details: TechnicalDetails = Field(
        description="Extracted technical information"
    )
    triage_reasoning: str = Field(description="Justification for the triage decision")
    severity: str = Field(description="Severity level")
    suggested_owner: str = Field(description="Team name responsible for this bug")
