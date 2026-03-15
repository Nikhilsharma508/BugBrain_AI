# `scripts/` — Utility Scripts

## Purpose
Standalone scripts for setup, data loading, and index building. These are run manually (not imported by the application).

## Files

| Script | Description | Run with |
|--------|-------------|----------|
| `setup_env.sh` | Creates virtualenv and installs dependencies | `bash scripts/setup_env.sh` |
| `load_csv_data.py` | Copies and prepares CSV data for the pipeline | `python scripts/load_csv_data.py` |
| `build_vector_index.py` | Builds FAISS/ChromaDB index from historical data | `python scripts/build_vector_index.py` |
