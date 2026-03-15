# src/schemas/triage_output.py — Triage Result Output Model
#
# PURPOSE:
#   Defines the structured JSON output that the system produces.
#   This is the contract that downstream tools (Jira, GitHub Issues) consume.
#
# FIELDS (from Problem Statement):
#   - issue_summary: str — One-line technical summary
#   - steps_to_reproduce: List[str] — Ordered reproduction steps
#   - technical_details: TechnicalDetails — Error info, environment
#   - severity: str — P1/P2/P3/P4 with description
#   - suggested_owner: str — Team name (e.g., "Payments-Backend-Team")
#   - duplicate_of: Optional[str] — ID of existing ticket if duplicate
#
# TODO:
#   - Define TriageResult and TechnicalDetails Pydantic models
#   - Add JSON serialisation helpers
#   - Add example() class method for documentation

from pydantic import BaseModel
from typing import Optional
