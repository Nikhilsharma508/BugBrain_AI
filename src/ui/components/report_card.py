# src/ui/components/report_card.py — Reusable Result Card Widget
#
# PURPOSE:
#   A Streamlit component that renders a triage result as a visual card.
#   Displays: summary, severity badge, team, steps to reproduce, and
#   duplicate warning (if applicable).
#
# USAGE:
#   from src.ui.components.report_card import render_report_card
#   render_report_card(triage_result)
#
# TODO:
#   - Implement render_report_card(result: TriageResult)
#   - Use st.container() for card layout
#   - Include expandable sections for technical details

import streamlit as st
