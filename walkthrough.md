# AI Bug Triage System — Project Structure Walkthrough

## What Was Created

**86 files** across **25 directories** — a complete industrial-grade project skeleton.

### Top-Level Files (6)
- [README.md](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/README.md), [pyproject.toml](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/pyproject.toml), [requirements.txt](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/requirements.txt), [.env.example](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/.env.example), [.gitignore](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/.gitignore), [Makefile](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/Makefile)
- [guide.md](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/guide.md) — full setup & development guide (answers all your questions)

### `src/` — 9 Sub-Modules (37 Python files + 10 READMEs)

| Module | Files | Purpose |
|--------|-------|---------|
| `config/` | [settings.py](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/src/config/settings.py) | Pydantic BaseSettings for env vars |
| `preprocessing/` | [log_parser.py](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/tests/unit/test_log_parser.py), [noise_filter.py](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/tests/unit/test_noise_filter.py), [text_cleaner.py](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/src/preprocessing/text_cleaner.py) | Trim 95% log noise |
| `schemas/` | [bug_report.py](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/src/schemas/bug_report.py), [triage_output.py](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/src/schemas/triage_output.py), [duplicate_result.py](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/src/schemas/duplicate_result.py) | Pydantic data contracts |
| `agents/` | [extraction_agent.py](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/src/agents/extraction_agent.py), [triage_agent.py](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/src/agents/triage_agent.py), [orchestrator.py](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/src/agents/orchestrator.py) | LangChain agents + pipeline |
| `prompts/` | [extraction_prompts.py](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/src/prompts/extraction_prompts.py), [triage_prompts.py](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/src/prompts/triage_prompts.py), [summarisation_prompts.py](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/src/prompts/summarisation_prompts.py) | Prompt templates |
| `duplicate_detection/` | [embeddings.py](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/src/duplicate_detection/embeddings.py), [vector_store.py](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/src/duplicate_detection/vector_store.py), [similarity.py](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/src/duplicate_detection/similarity.py) | RAG + FAISS/ChromaDB |
| `policies/` | [severity_policy.yaml](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/src/policies/severity_policy.yaml), [team_routing.yaml](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/src/policies/team_routing.yaml) | Editable business rules |
| `telemetry/` | [logger.py](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/src/telemetry/logger.py), [metrics.py](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/src/telemetry/metrics.py), [audit_trail.py](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/src/telemetry/audit_trail.py) | Logging, cost tracking |
| `ui/` | [app.py](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/src/ui/app.py), `pages/`, `components/` | Streamlit app |

### Supporting Directories
- `Data/` — original CSV + new `raw/`, `processed/`, `vector_store/`, `temp/` sub-dirs
- `tests/` — `unit/` (3 tests) + `integration/` (2 tests)
- `docs/` — [architecture.md](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/docs/architecture.md), [api_reference.md](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/docs/api_reference.md)
- `scripts/` — [setup_env.sh](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/scripts/setup_env.sh), [load_csv_data.py](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/scripts/load_csv_data.py), [build_vector_index.py](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/scripts/build_vector_index.py)
- `notebooks/` — [01_eda_bug_reports.ipynb](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/notebooks/01_eda_bug_reports.ipynb)

## Verification Results

```
✅ 25 directories exist
✅ 24 README.md files (every dir except Validation Data/ which is untouched)
✅ 45 Python files with imports + comments (no implementation code)
✅ Original files untouched (Problem Statement.md, bug_report.csv, Validation Input.md, temp.ipynb)
```

## Next Steps
1. Read [guide.md](file:///Users/nike/Documents/Data%20Science%20Work/Project/UC20%20-%20Bug%20Report%20Summarizer%20&%20Triage%20Assistant/guide.md) for the full initial setup walkthrough
2. Run `git init` and make your first commit
3. Create virtual env and install dependencies
4. Start implementing modules (begin with `src/preprocessing/`)
