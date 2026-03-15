# Architecture — AI Bug Triage System

## High-Level Data Flow

```
┌─────────────────┐
│  Raw Bug Report  │  (email, Jira, CSV, user paste)
└────────┬────────┘
         ▼
┌─────────────────┐
│  Preprocessing   │  TextCleaner → NoiseFilter → LogParser
│  (src/preprocessing)
└────────┬────────┘
         ▼
┌─────────────────┐
│ Extraction Agent │  LangChain LLM → Structured JSON
│  (src/agents)    │  Uses prompts from src/prompts/
└────────┬────────┘
         ▼
┌─────────────────┐
│ Duplicate Check  │  Embed → FAISS/ChromaDB search → DuplicateMatch
│  (src/duplicate) │
└────────┬────────┘
         ▼
┌─────────────────┐
│  Triage Agent    │  Severity (P1–P4) + Team routing
│  (src/agents)    │  Uses policies from src/policies/
└────────┬────────┘
         ▼
┌─────────────────┐
│  Structured Out  │  JSON → Jira / GitHub Issues / Dashboard
│  (src/schemas)   │
└─────────────────┘
```

## Module Dependency Graph

```
ui → agents → preprocessing
              schemas
              duplicate_detection
              prompts
              policies
     telemetry (cross-cutting)
     config (foundation)
```

## Technology Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Vector DB | FAISS (default) / ChromaDB | FAISS is fast and file-based; ChromaDB for persistence |
| LLM | OpenAI GPT-4o-mini | Cost-efficient with structured output support |
| Embeddings | text-embedding-3-small | OpenAI's latest compact embedding model |
| UI | Streamlit | Rapid prototyping, Python-native |
| Data models | Pydantic v2 | Runtime validation + JSON serialisation |
| Config | YAML + .env | Policies in YAML (PM-editable), secrets in .env |

## TODO
- Add architecture diagram image (draw.io or Mermaid)
- Add sequence diagram for the request lifecycle
- Add deployment architecture (when Docker is added)
