# src/preprocessing — Log Noise Filtering & Text Cleaning
#
# This package contains all pre-processing logic that runs BEFORE the LLM.
# Its job is to trim ~95% of irrelevant content from raw bug reports.
#
# Exports:
#   - LogParser: Regex-based stack trace and error extractor
#   - NoiseFilter: Strips emotional language, memory dumps, hardware info
#   - TextCleaner: Unicode normalisation, whitespace cleanup

from src.preprocessing.log_parser import LogParser
from src.preprocessing.noise_filter import NoiseFilter
from src.preprocessing.text_cleaner import TextCleaner

__all__ = ["LogParser", "NoiseFilter", "TextCleaner"]
