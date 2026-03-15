# src/duplicate_detection/vector_store.py — FAISS / ChromaDB Operations
#
# PURPOSE:
#   Manages the vector database that stores embeddings of all existing
#   bug reports. Supports both FAISS (file-based) and ChromaDB (persistent).
#
# KEY CLASS:
#   VectorStoreManager — with methods like:
#     - initialise() → Load or create the vector index
#     - add_report(report_id: str, text: str) → Add new report embedding
#     - search(query_text: str, top_k: int) → List of similar reports
#     - save() → Persist the index to disk
#
# TODO:
#   - Implement FAISS backend (load/save from data/vector_store/)
#   - Implement ChromaDB backend as alternative
#   - Add factory method to switch between backends via config
#   - Handle index not found (first run) gracefully

from typing import Optional
