# src/schemas/bug_report.py — Bug Report Input Model
#
# PURPOSE:
#   Defines the Pydantic model for a raw bug report as it enters the system.
#   Validates and structures the input data before it hits the preprocessing pipeline.
#
# FIELDS (planned):
#   - id: Optional[int] — Report ID from CSV or database
#   - raw_text: str — The full unstructured bug report text
#   - source: Optional[str] — Where the report came from (email, Jira, form)
#   - submitted_at: Optional[datetime] — Timestamp of submission
#
# TODO:
#   - Define the BugReport Pydantic model with field validators
#   - Add a from_csv_row() class method for loading from the CSV data

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
