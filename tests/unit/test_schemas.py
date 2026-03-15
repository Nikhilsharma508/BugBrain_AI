# tests/unit/test_schemas.py — Unit Tests for Pydantic Models
#
# PURPOSE:
#   Tests the Pydantic data models in src/schemas/
#
# TEST CASES (planned):
#   - test_bug_report_valid: Creates a valid BugReport instance
#   - test_bug_report_missing_required: Raises ValidationError for missing fields
#   - test_triage_result_serialisation: Serialises TriageResult to JSON correctly
#   - test_duplicate_match_defaults: Checks default values
#
# TODO:
#   - Write test functions for each model
#   - Test edge cases (empty strings, None values)

import pytest
