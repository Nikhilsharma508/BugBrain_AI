# `src/` — Production Source Code

This directory contains all production-grade Python source code for the AI Bug Triage System.

## Sub-packages

| Package | Purpose |
|---------|---------|
| `config/` | Centralised project settings via Pydantic `BaseSettings` |
| `preprocessing/` | Log noise filtering, regex parsing, text cleaning |
| `schemas/` | Pydantic data models for input/output contracts |
| `agents/` | LangChain agent definitions (extraction, triage, orchestrator) |
| `prompts/` | Prompt templates separated from agent logic |
| `duplicate_detection/` | Embeddings, FAISS/ChromaDB vector store, similarity search |
| `policies/` | Externalised business rules (severity, team routing) in YAML |
| `telemetry/` | Python logging, API latency tracking, cost metrics, audit trail |
| `ui/` | Streamlit application (pages + reusable components) |

## Design Principles

- **Separation of Concerns:** Each sub-package handles one responsibility.
- **Dependency Direction:** `ui → agents → preprocessing/schemas/duplicate_detection → config`
- **No Circular Imports:** Lower-level modules never import from higher-level ones.
