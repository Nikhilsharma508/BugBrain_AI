"""
src/duplicate_detection/embeddings.py — Embedding Model Wrapper
-----------------------------------------------------------------
WHAT IT CAN DO (when implemented):
    - Generate text embeddings using OpenAI (text-embedding-3-small)
    - Generate embeddings using HuggingFace sentence-transformers (free, local)
    - Batch embedding for processing multiple reports at once
    - Caching: avoid re-embedding the same text twice
    - Configurable model selection via settings

CONNECTS TO:
    - similarity.py calls embed_text() to vectorise new reports
    - vector_store.py stores the resulting vectors
    - config/settings.py provides embedding_model_name
"""
