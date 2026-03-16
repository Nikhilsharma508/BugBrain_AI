"""
ui/pages/main_pipeline_page.py — Core Triage Pipeline UI
----------------------------------------------------------
PURPOSE:
    Renders the form to accept bug reports and user reviews,
    triggers the orchestrator pipeline, and displays results.
"""

import streamlit as st
from src.agents.orchestrator import run_pipeline
from src.ui.components import result_display
import time


def render():
    st.header("Run Triage Pipeline")
    st.markdown("Submit a new bug report and an optional user review below to trigger the triage agents.")

    # Form inputs
    with st.form("triage_form"):
        bug_trace = st.text_area(
            "Bug Trace / Log Dump / Stack Trace",
            height=300,
            placeholder="Paste your raw crash logs or application errors here...",
            help="This is the raw technical output that needs parsing."
        )
        
        user_review = st.text_area(
            "User Review (Optional)",
            height=100,
            placeholder="User comments, steps they tried, or extra context like 'I clicked the button and it crashed'.",
            help="Optional natural language context."
        )
        
        submitted = st.form_submit_button("Run Analysis", type="primary")

    if submitted:
        if not bug_trace.strip():
            st.error("Please provide a Bug Trace to run the analysis.")
            return

        # Execute Pipeline
        with st.spinner("Agents are analyzing the logs and running triage..."):
            try:
                start_time = time.time()
                # UI strictly deals with presentation, passing raw data to LangGraph
                result = run_pipeline(bug_trace=bug_trace, user_review=user_review)
                duration = time.time() - start_time
                
                # Display Results via modular component
                result_display.render_triage_result(result, duration)

            except Exception as e:
                st.error(f"Pipeline execution failed: {str(e)}")
                st.exception(e)
