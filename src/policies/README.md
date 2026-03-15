# `src/policies/` — Externalised Business Rules

## Purpose

Stores **business rules as YAML configuration** instead of hard-coding them in Python. This means:

- **Product Managers** can edit severity rules without touching code
- **Team routing** can be updated without a code deployment
- Rules are version-controlled and easy to review in pull requests

## Files

| File | Description |
|------|-------------|
| `severity_policy.yaml` | P1–P4 severity definitions, conditions, and response times |
| `team_routing.yaml` | Maps components/keywords to responsible teams |
| `README.md` | This file |

## How They're Used

1. The `TriageAgent` loads these YAML files at startup
2. The rules are injected into the LLM prompt as context
3. The LLM classifies the bug based on these rules (not its own judgment)

## Editing Rules

Simply open the YAML file, modify the conditions or keywords, and save. No Python changes needed. The next time the Streamlit app restarts, it picks up the updated rules.
