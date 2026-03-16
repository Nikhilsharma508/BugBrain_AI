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

import streamlit as st
import sys
from pathlib import Path

# Add project root to python path to ensure imports work from anywhere
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.ui.pages import main_pipeline_page

def main():
    st.set_page_config(
        page_title="AI Bug Triage",
        page_icon="🐛",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.sidebar.title("🐛 AI Bug Triage System")
    st.sidebar.markdown(
        "Welcome to the **uc20_bug_report_summarizer** interactive interface. "
        "This tool uses an LLM-driven LangGraph pipeline to extract, parse, "
        "and triage incoming software bug reports."
    )
    
    # Navigation
    page = st.sidebar.radio(
        "Navigation", 
        ["Run Triage Pipeline", "Settings (Coming Soon)", "History (Coming Soon)"]
    )

    if page == "Run Triage Pipeline":
        main_pipeline_page.render()
    else:
        st.info("Feature under construction.")

if __name__ == "__main__":
    main()
