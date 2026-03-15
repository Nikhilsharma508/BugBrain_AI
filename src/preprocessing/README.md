# `src/preprocessing/` — Log Noise Filtering & Text Cleaning

## Purpose

This module contains all pre-processing logic that runs **before** the bug report is sent to the LLM. Its primary job is to **trim ~95% of irrelevant noise** so the AI can focus on what matters.

## Why is this needed?

Looking at the sample data (`Data/bug_report.csv`), raw bug reports contain:
- Thousands of lines of memory address ranges (`0x92950000 - 0x92b7bfff ...`)
- JAR file listings and library paths
- Hardware inventory (USB devices, memory modules)
- Emotional user descriptions mixed with technical data

Without preprocessing, we'd waste **tokens and money** sending all this noise to the LLM.

## Files

| File | Description |
|------|-------------|
| `__init__.py` | Package exports: `LogParser`, `NoiseFilter`, `TextCleaner` |
| `log_parser.py` | Regex-based extraction of stack traces, error codes, file paths |
| `noise_filter.py` | Removes emotional language, hardware dumps, memory addresses |
| `text_cleaner.py` | Unicode normalisation, whitespace cleanup, truncation |

## Pipeline Order

```
Raw Text → TextCleaner → NoiseFilter → LogParser → Clean Output
```

The clean output is then passed to the extraction agent in `src/agents/`.
