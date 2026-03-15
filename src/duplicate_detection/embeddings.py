# src/duplicate_detection/embeddings.py — Embedding Model Wrapper
#
# PURPOSE:
#   Provides a unified interface for generating text embeddings.
#   Supports OpenAI embeddings and can be extended to HuggingFace models.
#   Used to convert bug report summaries into vectors for similarity search.
#
# KEY CLASS:
#   EmbeddingManager — with methods like:
#     - embed_text(text: str) → List[float]
#     - embed_batch(texts: List[str]) → List[List[float]]
#
# TODO:
#   - Initialise embedding model from settings
#   - Implement embed_text() and embed_batch()
#   - Add caching to avoid re-embedding the same text

from langchain_openai import OpenAIEmbeddings
from typing import Optional
