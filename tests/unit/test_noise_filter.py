# tests/unit/test_noise_filter.py — Unit Tests for NoiseFilter
#
# PURPOSE:
#   Tests the noise filtering functions in src/preprocessing/noise_filter.py
#
# TEST CASES (planned):
#   - test_remove_memory_addresses: Strips 0x... address ranges
#   - test_remove_hardware_info: Removes USB device listings
#   - test_preserve_stack_traces: Keeps Java/Python stack traces intact
#   - test_remove_emotional_language: Strips non-technical content
#   - test_real_sample_data: Tests against actual bug_report.csv entries
#
# TODO:
#   - Write test functions
#   - Create fixtures with sample noise data

import pytest
