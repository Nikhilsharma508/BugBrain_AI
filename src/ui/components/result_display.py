"""
ui/components/result_display.py — Reusable Result Drawer
----------------------------------------------------------
PURPOSE:
    Encapsulate the Streamlit UI code required to display the `TriageResult`.
"""

import streamlit as st
from src.schemas.triage_output import TriageResult


def get_severity_style(severity: str):
    """Return HTML/CSS styling based on severity level."""
    if "P1" in severity:
        return "#ff6b6b"  # "🔴 Critical"
    elif "P2" in severity:
        return "#ff9800"  # "🟠 High"
    elif "P3" in severity:
        return "#ffc107"  # "🟡 Medium"
    else:
        return "#4caf50"  # "🟢 Low"


def render_triage_result(result: TriageResult, duration_sec: float = 0.0):
    """
    Renders a TriageResult object beautifully in Streamlit with enhanced styling.
    """

    # Title
    st.markdown(
        "<h3 style='color: #64b6ff; text-align: center; font-weight: 900; margin-top: 0;'>FINAL TRIAGE REPORT</h3>",
        unsafe_allow_html=True,
    )

    if duration_sec is not None:
        st.markdown(
            f"<p style='text-align: center; color: #b0c4de; font-size: 0.9rem;'>✅ Pipeline executed in {duration_sec:.2f} seconds</p>",
            unsafe_allow_html=True,
        )

    # Get severity styling
    severity_bg = get_severity_style(result.severity)

    # Header Section: Severity & Owner
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
            <div style='background: rgba({int(severity_bg[1:3], 16)}, {int(severity_bg[3:5], 16)}, {int(severity_bg[5:7], 16)}, 0.15); 
                        border: 2px solid {severity_bg}; 
                        border-radius: 20px; 
                        padding: 1rem; 
                        text-align: center;'>
                <p style='color: {severity_bg}; font-weight: 900; font-size: 1.5rem; margin: 0.5rem 0;'>{result.severity}</p>
                <p style='color: #b0c4de; font-size: 0.85rem; margin: 0;'>Assigned Severity</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div style='background: rgba(100, 182, 255, 0.15); 
                        border: 2px solid #64b6ff; 
                        border-radius: 20px; 
                        padding: 1rem; 
                        text-align: center;'>
                <p style='color: #64b6ff; font-weight: 900; font-size: 1.5rem; margin: 0.5rem 0;'>{result.suggested_owner}</p>
                <p style='color: #b0c4de; font-size: 0.85rem; margin: 0;'>Suggested Owner</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        "<hr style='border: 1px solid rgba(100, 150, 220, 0.3);'>",
        unsafe_allow_html=True,
    )

    # Issue Summary
    st.markdown(
        "<h4 style='color: #64d9ff; font-weight: 800; margin-bottom: 0.5rem;'>📝 Issue Summary</h4>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='color: #e0e6ff; line-height: 1.6; font-size: 1rem;'>{result.issue_summary}</p>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<hr style='border: 1px solid rgba(100, 150, 220, 0.2);'>",
        unsafe_allow_html=True,
    )

    # Steps to Reproduce
    st.markdown(
        "<h4 style='color: #64d9ff; font-weight: 800; margin-bottom: 0.5rem;'>🔧 Steps to Reproduce</h4>",
        unsafe_allow_html=True,
    )
    if not result.steps_to_reproduce or result.steps_to_reproduce == [
        "Not provided by user"
    ]:
        st.info("⚠️ No reproduction steps could be extracted from the user report.")
    else:
        steps_html = ""
        for i, step in enumerate(result.steps_to_reproduce, 1):
            steps_html += f"<p style='color: #e0e6ff; margin: 0.5rem 0;'><strong style='color: #64b6ff;'>{i}.</strong> {step}</p>"
        st.markdown(
            f"<div style='color: #e0e6ff;'>{steps_html}</div>", unsafe_allow_html=True
        )

    st.markdown(
        "<hr style='border: 1px solid rgba(100, 150, 220, 0.2);'>",
        unsafe_allow_html=True,
    )

    # Technical Details
    st.markdown(
        "<h4 style='color: #64d9ff; font-weight: 800; margin-bottom: 0.5rem;'>⚙️ Technical Details</h4>",
        unsafe_allow_html=True,
    )

    tech_html = f"""
    <div style='background: rgba(20, 35, 60, 0.6); border-left: 4px solid #64b6ff; border-radius: 8px; padding: 1rem;'>
        <p style='color: #b0c4de; margin: 0.5rem 0;'><strong>Detected Error:</strong> <span style='color: #64d9ff;'>{result.technical_details.detected_error}</span></p>
        <p style='color: #b0c4de; margin: 0.5rem 0;'><strong>Environment:</strong> <span style='color: #64d9ff;'>{result.technical_details.environment}</span></p>
        <p style='color: #b0c4de; margin: 0.5rem 0;'><strong>Error Message:</strong><br/><span style='color: #e0e6ff; font-family: monospace;'>{result.technical_details.error_message}</span></p>
    </div>
    """
    st.markdown(tech_html, unsafe_allow_html=True)

    # Stack Trace Expander
    if (
        hasattr(result.technical_details, "key_stack_frames")
        and result.technical_details.key_stack_frames
    ):
        with st.expander("🔍 View Key Stack Frames", expanded=False):
            for i, frame in enumerate(result.technical_details.key_stack_frames, 1):
                st.markdown(
                    f"<p style='color: #64d9ff; font-weight: 700;'>Frame {i}</p>",
                    unsafe_allow_html=True,
                )
                st.code(frame, language="java")
