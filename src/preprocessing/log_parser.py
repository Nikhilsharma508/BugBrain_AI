# src/preprocessing/log_parser.py — Regex-Based Stack Trace Extractor
#
# PURPOSE:
#   Extracts meaningful technical signals from raw bug report text:
#     - Java/Python stack traces
#     - Error codes and exception names
#     - File paths and line numbers
#     - Timestamps and log levels
#
# APPROACH:
#   Uses compiled regex patterns to identify and extract structured
#   information from thousands of lines of noisy log output.
#   This ensures the LLM only sees the relevant ~5% of the log.
#
# KEY CLASS:
#   LogParser — Main class with methods like:
#     - extract_stack_traces(raw_text) → List[str]
#     - extract_error_codes(raw_text) → List[str]
#     - extract_file_references(raw_text) → List[dict]
#     - parse(raw_text) → dict  (combined extraction)
#
# TODO:
#   - Define regex patterns for Java, Python, and generic stack traces
#   - Handle multi-line stack trace continuation
#   - Add extraction for memory addresses (0x...) and filter them out
#   - Return structured dict with extracted signals

import re
from typing import Optional
