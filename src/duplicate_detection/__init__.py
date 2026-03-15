# src/duplicate_detection — RAG / Vector Similarity
#
# This package handles duplicate bug detection using vector embeddings
# and similarity search against existing reports stored in FAISS or ChromaDB.
#
# Exports:
#   - EmbeddingManager: Wrapper for embedding model (OpenAI / HuggingFace)
#   - VectorStoreManager: FAISS or ChromaDB operations
#   - SimilarityChecker: Compare new report against existing tickets

from src.duplicate_detection.embeddings import EmbeddingManager
from src.duplicate_detection.vector_store import VectorStoreManager
from src.duplicate_detection.similarity import SimilarityChecker

__all__ = ["EmbeddingManager", "VectorStoreManager", "SimilarityChecker"]
