"""
src/preprocessing — Text Preprocessing Pipeline
-------------------------------------------------
Chains: clean → filter_noise → extract_signals

USAGE:
    from src.preprocessing import run_preprocessing
    result = run_preprocessing(bug_trace)
    # result = {"cleaned_text": "...", "signals": {...}}
"""

from src.preprocessing.text_cleaner import clean
from src.preprocessing.noise_filter import filter_noise

def run_preprocessing(bug_trace: str) -> dict:
    """Run the full preprocessing pipeline on raw bug report text.

    Returns:
        dict with:
            - cleaned_text: str (noise-filtered text)
            - signals: dict (extracted exceptions, stack frames, etc.)
    """
    # Step 1: Normalise whitespace and line endings
    text = clean(bug_trace)

    # Step 2: Remove non-diagnostic noise
    text = filter_noise(text)

    return {
        "cleaned_text": text,
    }


__all__ = ["run_preprocessing", "clean", "filter_noise"]
