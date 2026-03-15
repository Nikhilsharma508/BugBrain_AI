# `src/config/` — Centralised Configuration

## Purpose

Provides a **single source of truth** for all project settings. Uses Pydantic `BaseSettings` to:

- Read values from environment variables (`.env` file)
- Validate types and required fields at startup
- Provide IDE auto-completion for all config values

## Files

| File | Description |
|------|-------------|
| `__init__.py` | Exports the global `settings` instance |
| `settings.py` | `Settings` class definition (all env vars) |

## Usage

```python
from src.config import settings

api_key = settings.openai_api_key
model = settings.llm_model_name
```

## Configuration Source

All values come from the `.env` file at the project root. See `.env.example` for the full list of variables.
