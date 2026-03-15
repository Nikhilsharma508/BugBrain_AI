# src/ui/pages/submit_report.py — Bug Report Submission Form
#
# PURPOSE:
#   Streamlit page where users paste or upload a raw bug report.
#   Calls the Orchestrator pipeline and displays the structured result.
#
# UI ELEMENTS (planned):
#   - Text area for pasting raw bug report
#   - File upload button for CSV/text files
#   - "Analyse" button to trigger the pipeline
#   - Results display: JSON output, severity badge, team assignment
#   - Duplicate warning if a similar report exists
#
# TODO:
#   - Build the input form with st.text_area and st.file_uploader
#   - Connect to Orchestrator.run_pipeline()
#   - Display results using components from src/ui/components/
#   - Add loading spinner during processing

import streamlit as st
