# `scripts/` — Utility Scripts

## Purpose
Standalone scripts for setup, data loading, and index building. These are run manually (not imported by the application).

## Files

| Script | Description | Run with |
|--------|-------------|----------|
| `build_vector_index.py` | Builds FAISS/ChromaDB index from historical data | `python scripts/build_vector_index.py` |
| `load_json_data.py` | Loads JSON data into the pipeline | `python scripts/load_json_data.py` |
