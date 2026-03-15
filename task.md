# AI Bug Triage System — Project Structure Generation

## Tasks
- [/] Plan the full project directory tree and document it in the implementation plan
- [ ] Create the top-level project files (`README.md`, `pyproject.toml`, `.env.example`, `.gitignore`, `Makefile`, etc.)
- [ ] Create `src/` core package structure with `__init__.py` and `config/` module
- [ ] Create `src/preprocessing/` module (log noise filtering, regex parsers)
- [ ] Create `src/agents/` module (extraction agent, triage agent, orchestrator)
- [ ] Create `src/prompts/` module (system/user prompt templates)
- [ ] Create `src/duplicate_detection/` module (embeddings, FAISS/Chroma, RAG)
- [ ] Create `src/schemas/` module (Pydantic models for structured output)
- [ ] Create `src/telemetry/` module (internal logging, latency, usage stats)
- [ ] Create `src/ui/` module (Streamlit app, pages, components)
- [ ] Create `data/` storage directories (raw, processed, vector_store, temp)
- [ ] Create `tests/` directory with unit and integration test stubs
- [ ] Create `docs/` directory (architecture diagram placeholder, API docs)
- [ ] Create `scripts/` directory (setup, data loading, index building)
- [ ] Create `notebooks/` directory (exploration / prototyping)
- [ ] Write README.md files in every folder
- [ ] Write the implementation plan and get user approval
