"""
src/preprocessing/text_cleaner.py — Basic Text Normalisation
-------------------------------------------------------------
PURPOSE:
    First step in the preprocessing pipeline.
    Normalises raw text so downstream modules get consistent input.

WHAT IT DOES:
    - Strips leading/trailing whitespace
    - Collapses multiple blank lines into one
    - Normalises line endings (\\r\\n → \\n)
    - Removes null bytes and control characters

CAPABILITIES (can be extended later):
    - Unicode normalisation (NFC/NFKD)
    - Encoding detection and conversion
    - HTML entity decoding
    - Markdown stripping

CONNECTS TO:
    preprocessing/__init__.py → run_preprocessing() calls clean() first
"""

import re


import re

def clean(text: str) -> str:
    """Normalise raw text: fix line endings, collapse whitespace, strip edges."""
    if not text:
        return ""

    # Normalise line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove null bytes and control chars (keep newlines and tabs)
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)

    # COLLAPSE ESCAPED QUOTES:
    # Replaces any sequence of 2+ double-quotes with a single double-quote.
    # Handles "", """, """", etc., which are common CSV-export artifacts.
    text = re.sub(r'"{2,}', '"', text)

    # Collapse multiple tabs into a single space (logs often use tabs for padding)
    text = re.sub(r"\t+", " ", text)

    # Collapse 3+ consecutive newlines into 2 (keeps paragraph structure)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Strip leading/trailing whitespace
    return text.strip()

if __name__ == "__main__":
    print("--- TEXT CLEANER TEST ---")
    # Test varying levels of quote escaping and whitespace
    dirty = '""ts""\n\n\n\t\t(Initializer.java:52)\n""""at org.eclipse""""\n"""Root Cause"""'
    cleaned = clean(dirty)
    print(f"Cleaned Output:\n{cleaned}")
    
    # Verification
    assert '""' not in cleaned
    assert '\t' not in cleaned