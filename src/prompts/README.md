# `src/prompts/` — Prompt Templates

## Purpose

Stores all LLM prompt templates **separate from agent logic**. This separation means you can iterate on prompts without touching Python code, and prompts can be versioned/reviewed independently.

## Files

| File | Description |
|------|-------------|
| `__init__.py` | Exports all prompt constants |
| `extraction_prompts.py` | System + user prompts for the extraction agent |
| `triage_prompts.py` | System + user prompts for severity/team classification |
| `summarisation_prompts.py` | System prompt for log summarisation (overflow handler) |

## Design Principles

1. **Prompts are constants** — defined as Python strings for easy import
2. **Placeholders use `{variable_name}`** — compatible with LangChain's `ChatPromptTemplate`
3. **System prompts define role + rules**, user prompts inject the actual data
4. **Anti-hallucination rules** are embedded in the extraction prompt
