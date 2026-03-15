# src/preprocessing/text_cleaner.py — Text Normalisation Utilities
#
# PURPOSE:
#   Handles low-level text normalisation tasks:
#     - Unicode character normalisation (e.g., ¬Æ → proper characters)
#     - Whitespace collapsing (multiple spaces/newlines → single)
#     - Tab-to-space conversion
#     - Trimming leading/trailing whitespace per line
#     - Removing null bytes and control characters
#
# APPROACH:
#   Pure string operations — no ML or regex complexity.
#   Runs as the first step in the preprocessing pipeline.
#
# KEY CLASS:
#   TextCleaner — Main class with methods like:
#     - clean(raw_text) → str
#     - normalise_unicode(text) → str
#     - collapse_whitespace(text) → str
#     - truncate(text, max_chars) → str
#
# TODO:
#   - Implement each normalisation method
#   - Add character encoding detection (chardet)
#   - Add max token/character limit enforcement

import re
import unicodedata
from typing import Optional
