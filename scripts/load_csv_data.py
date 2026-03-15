# scripts/load_csv_data.py — CSV Data Loader
#
# PURPOSE:
#   Copies and prepares the source CSV data for pipeline use.
#   Reads from Data/bug_report.csv (original) and writes a
#   cleaned version to data/raw/ for the application to consume.
#
# WHAT IT DOES:
#   1. Reads Data/bug_report.csv
#   2. Validates the schema (Id, Bug Details columns)
#   3. Copies to data/raw/bug_report.csv
#   4. Prints basic stats (row count, sample)
#
# USAGE:
#   python scripts/load_csv_data.py
#
# TODO:
#   - Implement data loading and validation logic
#   - Add error handling for missing source file
#   - Print summary statistics

import pandas as pd
from pathlib import Path
