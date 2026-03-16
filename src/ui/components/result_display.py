"""
ui/components/result_display.py — Reusable Result Drawer
----------------------------------------------------------
PURPOSE:
    Encapsulate the Streamlit UI code required to display the `TriageResult`
    so that it can be reused across different pages (e.g. main page or history).
"""

import streamlit as st
from src.schemas.triage_output import TriageResult


def render_triage_result(result: TriageResult, duration_sec: float = None):
    """
    Renders a TriageResult object beautifully in Streamlit.
    """
    
    # Top Level Metrics
    st.write("---")
    st.subheader("📊 Analysis Complete")
    
    if duration_sec is not None:
        st.caption(f"Pipeline executed in {duration_sec:.2f} seconds.")

    col1, col2 = st.columns(2)
    
    with col1:
        # Style severity based on level
        severity_color = "normal"
        if "P1" in result.severity:
            severity_color = "red"
        elif "P2" in result.severity:
            severity_color = "orange"
        elif "P3" in result.severity:
            severity_color = "blue"
            
        st.metric("Assigned Severity", result.severity, delta_color=severity_color)
        
    with col2:
        st.metric("Suggested Owner Team", result.suggested_owner)

    # Issue Summary
    st.info(f"**Issue Summary:** {result.issue_summary}")

    # Two-column layout for details
    detail_col1, detail_col2 = st.columns([1, 1])

    with detail_col1:
        st.markdown("### 📝 Steps to Reproduce")
        if not result.steps_to_reproduce or result.steps_to_reproduce == ["Not provided by user"]:
            st.warning("No reproduction steps could be extracted from the user report.")
        else:
            for i, step in enumerate(result.steps_to_reproduce, 1):
                st.markdown(f"{i}. {step}")

    with detail_col2:
        st.markdown("### ⚙️ Technical Details")
        st.markdown(f"**Detected Error:** `{result.technical_details.detected_error}`")
        st.markdown(f"**Environment:** {result.technical_details.environment}")
        st.markdown(f"**Error Message:** {result.technical_details.error_message}")
        
    # Stack Trace Expander
    if hasattr(result.technical_details, 'key_stack_frames') and result.technical_details.key_stack_frames:
        with st.expander("🔍 View Key Stack Frames"):
            for frame in result.technical_details.key_stack_frames:
                st.code(frame, language="java") # Default to java/text highlighting
