# src/ui/components/severity_badge.py — Colour-Coded Severity Pill
#
# PURPOSE:
#   A small Streamlit component that renders a colour-coded badge
#   based on the severity level:
#     - P1 (Critical) → Red
#     - P2 (High)     → Orange
#     - P3 (Medium)   → Yellow
#     - P4 (Low)      → Green
#
# USAGE:
#   from src.ui.components.severity_badge import render_severity_badge
#   render_severity_badge("P1 (Critical)")
#
# TODO:
#   - Implement render_severity_badge(severity: str)
#   - Use st.markdown with inline CSS for colour styling

import streamlit as st
