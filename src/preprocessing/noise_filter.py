# src/preprocessing/noise_filter.py — Strips Irrelevant Content
#
# PURPOSE:
#   Removes non-technical noise from raw bug reports before LLM processing:
#     - Emotional language ("I was having a great day until...")
#     - Hardware inventory dumps (USB devices, memory modules, etc.)
#     - Memory address ranges (0x92950000 - 0x92b7bfff ...)
#     - Repetitive library/JAR file listings
#     - System framework paths that don't contribute to the error
#
# APPROACH:
#   Combines regex patterns with heuristic rules to identify and remove
#   noise sections while preserving technical content (stack traces,
#   error messages, steps to reproduce).
#
# KEY CLASS:
#   NoiseFilter — Main class with methods like:
#     - filter(raw_text) → str  (cleaned text)
#     - remove_memory_dumps(text) → str
#     - remove_hardware_info(text) → str
#     - remove_emotional_language(text) → str
#
# TODO:
#   - Define noise patterns based on sample data analysis
#   - Implement section-level filtering (keep stack trace sections)
#   - Add configurable aggressiveness level
#   - Handle edge case: user description mixed with log output

import re
from typing import Optional
