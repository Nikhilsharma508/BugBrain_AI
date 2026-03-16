"""
src/duplicate_detection/vector_store.py — FAISS / ChromaDB Operations
----------------------------------------------------------------------
WHAT IT CAN DO (when implemented):
    - Create and load FAISS indexes (file-based, fast, zero setup)
    - Create and load ChromaDB collections (persistent, metadata support)
    - Add new report embeddings to the store
    - Search for top-K similar reports by vector similarity
    - Save/load index to/from data/vector_store/
    - Auto-create index on first run (handles empty store gracefully)

CONNECTS TO:
    - similarity.py uses search() to find similar reports
    - embeddings.py provides the vectors to store
    - scripts/build_vector_index.py builds the initial index from CSV
    - config/settings.py provides vector_store_type and vector_store_path
"""
