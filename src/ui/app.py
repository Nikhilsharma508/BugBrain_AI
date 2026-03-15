# src/ui/app.py — Main Streamlit Entry Point
#
# PURPOSE:
#   This is the main entry point for the Streamlit web application.
#   It sets up the page configuration, navigation sidebar, and
#   routes to the appropriate page based on user selection.
#
# RUN:
#   streamlit run src/ui/app.py
#   or: make run-ui
#
# PAGES:
#   - Submit Report: Paste or upload a bug report for triage
#   - Triage Dashboard: View past results, metrics, and audit history
#
# TODO:
#   - Set up Streamlit page config (title, icon, layout)
#   - Build sidebar navigation
#   - Import and render pages
#   - Add session state management

import streamlit as st
