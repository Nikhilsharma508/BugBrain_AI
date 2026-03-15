# AI Bug Triage System — Industrial-Grade Project Structure

## Goal
Generate a complete, production-ready directory tree inside **UC20 - Bug Report Summarizer & Triage Assistant/** with `README.md` files in every folder, covering: preprocessing, extraction agents, duplicate detection (RAG), internal telemetry, Streamlit UI, schemas, data storage, tests, docs, and utility scripts.

## Concerns, Suggestions & Decisions

> [!IMPORTANT]
> **Before I build, here are my recommendations and a few questions:**

### Suggestions I will include
| # | Suggestion | Why |
|---|-----------|-----|
| 1 | **`src/schemas/`** (Pydantic models) | Decouples the JSON contract from agent logic. Every downstream consumer imports from here. |
| 2 | **`src/policies/`** (severity rules YAML) | Externalises the P1-P4 severity policy so PMs can edit it without touching Python. |
| 3 | **`pyproject.toml`** over `setup.py` | Modern Python packaging standard (PEP 621). |
| 4 | **`Makefile`** with common targets | `make install`, `make test`, `make run-ui` — one-liner dev experience. |
| 5 | **`.env.example`** | Documents every env var (API keys, model names) without leaking secrets. |
| 6 | **`scripts/build_vector_index.py`** | One-shot script to ingest historical CSV into FAISS/ChromaDB so the app boots with a warm index. |
| 7 | **`notebooks/`** | Exploration and quick prototyping — keeps experiments separate from production code. |

### Things you could introduce later
- **FastAPI gateway** in `src/api/` if you want a REST layer in front of the Streamlit UI.
- **Docker + docker-compose** for reproducible deployments.
- **CI/CD configs** (`.github/workflows/`) once you push to GitHub.
- **LangSmith / LangFuse** integration in `src/telemetry/` for production-grade LLM observability.
- **Cost tracker module** to estimate OpenAI token spend per request (required by submission guidelines).

---

## Proposed Directory Tree

```
UC20 - Bug Report Summarizer & Triage Assistant/
│
├── README.md                         # Project-level overview, setup instructions
├── pyproject.toml                    # Dependencies, build config (PEP 621)
├── requirements.txt                  # Pinned pip dependencies (alternate install)
├── .env.example                      # Template for environment variables
├── .gitignore                        # Python / data / IDE ignores
├── Makefile                          # Common dev commands
├── Problem Statement.md              # [EXISTING] — untouched
├── temp.ipynb                        # [EXISTING] — untouched
│
├── src/                              # ── All production source code ──
│   ├── __init__.py
│   ├── README.md
│   │
│   ├── config/                       # Centralised configuration
│   │   ├── __init__.py
│   │   ├── settings.py               # Pydantic BaseSettings (reads .env)
│   │   └── README.md
│   │
│   ├── preprocessing/                # Log noise trimming (regex, heuristics)
│   │   ├── __init__.py
│   │   ├── log_parser.py             # Regex-based stack trace extractor
│   │   ├── noise_filter.py           # Strips emotional language, memory dumps, etc.
│   │   ├── text_cleaner.py           # Unicode, whitespace normalisation
│   │   └── README.md
│   │
│   ├── schemas/                      # Pydantic data models
│   │   ├── __init__.py
│   │   ├── bug_report.py             # BugReport input model
│   │   ├── triage_output.py          # TriageResult output model (JSON contract)
│   │   ├── duplicate_result.py       # DuplicateMatch model
│   │   └── README.md
│   │
│   ├── agents/                       # LangChain agent definitions
│   │   ├── __init__.py
│   │   ├── extraction_agent.py       # Raw text → structured JSON
│   │   ├── triage_agent.py           # Severity + owner classification
│   │   ├── orchestrator.py           # End-to-end pipeline controller
│   │   └── README.md
│   │
│   ├── prompts/                      # Prompt templates (system + user)
│   │   ├── __init__.py
│   │   ├── extraction_prompts.py     # Prompts for the extraction agent
│   │   ├── triage_prompts.py         # Prompts for severity / owner classification
│   │   ├── summarisation_prompts.py  # Prompts for log summarisation
│   │   └── README.md
│   │
│   ├── duplicate_detection/          # RAG / vector similarity
│   │   ├── __init__.py
│   │   ├── embeddings.py             # Embedding wrapper (OpenAI / HuggingFace)
│   │   ├── vector_store.py           # FAISS or ChromaDB operations
│   │   ├── similarity.py             # Compare new report vs. existing tickets
│   │   └── README.md
│   │
│   ├── policies/                     # Externalised business rules
│   │   ├── severity_policy.yaml      # P1–P4 thresholds and rules
│   │   ├── team_routing.yaml         # Component → Team mapping
│   │   └── README.md
│   │
│   ├── telemetry/                    # Internal monitoring & audit
│   │   ├── __init__.py
│   │   ├── logger.py                 # Structured Python logging setup
│   │   ├── metrics.py                # Latency, token usage, error counters
│   │   ├── audit_trail.py            # Per-request audit log writer
│   │   └── README.md
│   │
│   └── ui/                           # Streamlit application
│       ├── __init__.py
│       ├── app.py                    # Main Streamlit entry point
│       ├── pages/
│       │   ├── __init__.py
│       │   ├── submit_report.py      # Bug report submission form
│       │   ├── triage_dashboard.py   # Results & history dashboard
│       │   └── README.md
│       ├── components/
│       │   ├── __init__.py
│       │   ├── report_card.py        # Reusable result card widget
│       │   ├── severity_badge.py     # Colour-coded severity pill
│       │   └── README.md
│       └── README.md
│
├── data/                             # ── Data storage ──
│   ├── README.md
│   ├── raw/                          # Immutable source files
│   │   └── README.md                 # (bug_report.csv lives next door in Data/)
│   ├── processed/                    # Cleaned / transformed outputs
│   │   └── README.md
│   ├── vector_store/                 # FAISS / ChromaDB index files
│   │   └── README.md
│   └── temp/                         # Ephemeral scratch files
│       └── README.md
│
├── Data/                             # [EXISTING] — untouched (original CSV)
│   └── bug_report.csv
│
├── Validation Data/                  # [EXISTING] — untouched
│   └── Validation Input.md
│
├── tests/                            # ── Test suite ──
│   ├── __init__.py
│   ├── README.md
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_log_parser.py
│   │   ├── test_noise_filter.py
│   │   ├── test_schemas.py
│   │   └── README.md
│   └── integration/
│       ├── __init__.py
│       ├── test_extraction_pipeline.py
│       ├── test_duplicate_detection.py
│       └── README.md
│
├── docs/                             # ── Documentation ──
│   ├── README.md
│   ├── architecture.md               # High-level architecture description
│   └── api_reference.md              # Module-level API docs
│
├── scripts/                          # ── Utility scripts ──
│   ├── README.md
│   ├── setup_env.sh                  # Virtualenv + pip install automation
│   ├── load_csv_data.py              # Ingest raw CSV into data/processed/
│   └── build_vector_index.py         # Build FAISS/ChromaDB index from historical data
│
└── notebooks/                        # ── Exploration & prototyping ──
    ├── README.md
    └── 01_eda_bug_reports.ipynb      # Starter EDA notebook
```

## What I will create (summary)

### Top-level files
- `README.md` — project overview, quick-start, architecture summary
- `pyproject.toml` — dependencies and project metadata
- `requirements.txt` — pinned dependencies
- `.env.example` — env var template
- `.gitignore` — Python/data ignores
- `Makefile` — dev commands

### Source modules (`src/`)
| Module | Purpose |
|--------|---------|
| `config/` | Centralised settings via Pydantic `BaseSettings` |
| `preprocessing/` | Regex log parsing, noise filtering, text cleaning |
| `schemas/` | Pydantic models for input/output contracts |
| `agents/` | LangChain extraction + triage agents + orchestrator |
| `prompts/` | All prompt templates isolated from logic |
| `duplicate_detection/` | Embeddings + FAISS/ChromaDB + similarity search |
| `policies/` | Severity rules + team routing as YAML config |
| `telemetry/` | Python logging, latency/token metrics, audit trail |
| `ui/` | Streamlit app with pages and reusable components |

### Data, Tests, Docs, Scripts, Notebooks
- `data/` — `raw/`, `processed/`, `vector_store/`, `temp/`
- `tests/` — `unit/` and `integration/` with stub test files
- `docs/` — architecture and API reference placeholders
- `scripts/` — environment setup, CSV loader, index builder
- `notebooks/` — starter EDA notebook

## Verification Plan

### Automated
```bash
# 1. Verify all required directories exist
find "UC20 - Bug Report Summarizer & Triage Assistant/src" -type d | sort

# 2. Verify every folder has a README.md
find "UC20 - Bug Report Summarizer & Triage Assistant" -type d -exec sh -c \
  'test -f "$1/README.md" && echo "✅ $1" || echo "❌ MISSING: $1"' _ {} \;

# 3. Verify Python package structure
find "UC20 - Bug Report Summarizer & Triage Assistant/src" -name "__init__.py" | sort
```

### Manual
- Open the project in VS Code / PyCharm and visually confirm the tree matches the plan above.
- Confirm that existing files (`Problem Statement.md`, [Data/bug_report.csv](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/Data/bug_report.csv), `Validation Data/Validation Input.md`, [temp.ipynb](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/temp.ipynb)) have NOT been modified.
