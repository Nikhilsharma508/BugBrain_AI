# `src/agents/` — LangChain Agent Definitions

## Purpose

Contains the AI agent logic that powers the bug triage pipeline. Each agent handles one specific responsibility, following the **Single Responsibility Principle**.

## Files

| File | Description |
|------|-------------|
| `__init__.py` | Exports: `ExtractionAgent`, `TriageAgent`, `Orchestrator` |
| `extraction_agent.py` | Converts preprocessed text → structured JSON via LLM |
| `triage_agent.py` | Classifies severity (P1–P4) and assigns team ownership |
| `orchestrator.py` | End-to-end pipeline controller (the main entry point) |

## Pipeline Architecture

```
Orchestrator
  ├── TextCleaner + NoiseFilter + LogParser  (preprocessing)
  ├── ExtractionAgent                        (LLM extraction)
  ├── DuplicateDetection                     (RAG similarity)
  └── TriageAgent                            (classification)
```

## Key Design Decisions

1. **No hallucinated steps:** If the user didn't provide reproduction steps, the agent returns `"Steps not provided by user"` rather than guessing.
2. **Policy-driven classification:** Severity and team rules are loaded from YAML files in `src/policies/`, not hard-coded.
3. **Single entry point:** `Orchestrator.run_pipeline()` is the only function external code needs to call.
