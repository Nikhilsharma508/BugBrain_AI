# `src/schemas/` — Pydantic Data Models

## Purpose

Defines the **data contracts** for the entire project using Pydantic v2 models. Every structured input and output flows through models defined here.

This ensures:
- Type safety and validation at runtime
- Consistent JSON serialisation
- Auto-generated documentation
- Decoupled contracts — agents, UI, and API all import from here

## Files

| File | Description |
|------|-------------|
| `__init__.py` | Package exports: `BugReport`, `TriageResult`, `DuplicateMatch` |
| `bug_report.py` | Input model for raw bug report data |
| `triage_output.py` | Output model matching the Jira/GitHub JSON contract |
| `duplicate_result.py` | Result model for duplicate detection comparisons |

## Output Contract (from Problem Statement)

```json
{
  "issue_summary": "...",
  "steps_to_reproduce": ["..."],
  "technical_details": {"detected_error": "...", "environment": "..."},
  "severity": "P1 (Critical - Revenue Impacting)",
  "suggested_owner": "Payments-Backend-Team"
}
```
