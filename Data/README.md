# `data/` — Runtime Data Storage

## Purpose
Organises all data used and produced by the application at runtime. Separated from the original `Data/` folder which contains the immutable source CSV.

## Sub-directories

| Folder | Purpose | Git-tracked? |
|--------|---------|--------------|
| `raw/` | Copies of source data used by the pipeline | Yes (small files) |
| `processed/` | Cleaned/transformed outputs from preprocessing | No (generated) |
| `vector_store/` | FAISS/ChromaDB index files for duplicate detection | No (generated) |
| `temp/` | Ephemeral scratch files, logs, metrics JSONL | No (temporary) |
