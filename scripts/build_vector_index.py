# scripts/build_vector_index.py — Vector Index Builder
#
# PURPOSE:
#   One-shot script to build the FAISS/ChromaDB vector index from
#   historical bug report data. This ensures the app boots with a
#   "warm" index for duplicate detection.
#
# WHAT IT DOES:
#   1. Reads processed bug report data from data/raw/
#   2. Generates embeddings for each report
#   3. Stores embeddings in FAISS or ChromaDB index
#   4. Saves the index to data/vector_store/
#
# USAGE:
#   python scripts/build_vector_index.py
#
# PREREQUISITES:
#   - Run scripts/load_csv_data.py first
#   - OPENAI_API_KEY must be set in .env
#
# TODO:
#   - Load data from data/raw/
#   - Use EmbeddingManager to generate embeddings
#   - Use VectorStoreManager to build and save the index
#   - Add progress bar for large datasets

from pathlib import Path
