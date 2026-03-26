# `src/duplicate_detection/` — RAG / Vector Similarity

## Purpose

Handles **duplicate bug detection** using vector embeddings and similarity search. Before creating a new ticket, the system checks if a similar bug has already been reported.

## How It Works

```
New Bug Report
    ↓
EmbeddingManager.embed_text()  →  [0.12, -0.45, 0.89, ...]
    ↓
VectorStoreManager.search()    →  Top-K similar reports
    ↓
SimilarityChecker.check()      →  DuplicateMatch (is_duplicate, score, matched_id)
```

## Files

| File | Description |
|------|-------------|
| `__init__.py` | Exports: `EmbeddingManager`, `VectorStoreManager`, `SimilarityChecker` |
| `embeddings.py` | Wrapper for OLLAMA embedding models |
| `vector_store.py` | FAISS or ChromaDB index operations (add, search, save) |
| `similarity.py` | High-level duplicate check API |

## Vector Store Location

Index files are stored in `data/vector_store/`. The index is built initially by `scripts/build_vector_index.py` and updated as new reports are processed.
