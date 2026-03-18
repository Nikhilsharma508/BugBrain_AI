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

import streamlit as st


def render_report_card(result, expanded=True):
    """
    Renders a triage result as a visually attractive card with all key information.

    Args:
        result: TriageResult object
        expanded: Whether to show all details or collapsed view
    """

    # Determine severity color
    if "P1" in result.severity:
        severity_color, border_color = "#ff6b6b", "#ffaaaa"
    elif "P2" in result.severity:
        severity_color, border_color = "#ff9800", "#ffb84d"
    elif "P3" in result.severity:
        severity_color, border_color = "#ffc107", "#ffe082"
    else:
        severity_color, border_color = "#4caf50", "#81c784"

    # Card header
    card_html = f"""
    <div style='
        background: rgba(20, 35, 60, 0.8);
        border: 2px solid {severity_color};
        border-radius: 12px;
        padding: 1.2rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
    '>
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;'>
            <h5 style='color: #64b6ff; font-weight: 900; margin: 0;'>Report Card</h5>
            <div style='
                display: inline-block;
                background: {severity_color}33;
                border: 2px solid {severity_color};
                border-radius: 20px;
                padding: 0.3rem 0.8rem;
                color: {severity_color};
                font-weight: 900;
                font-size: 0.75rem;
            '>
                {result.severity}
            </div>
        </div>
        
        <p style='color: #e0e6ff; margin: 0.5rem 0; font-size: 0.95rem;'><strong>Summary:</strong></p>
        <p style='color: #b0c4de; margin: 0.5rem 0; line-height: 1.4;'>{result.issue_summary[:150]}...</p>
        
        <div style='display: flex; gap: 1rem; margin-top: 1rem;'>
            <div style='flex: 1;'>
                <p style='color: #b0c4de; font-size: 0.8rem; margin: 0;'>Owner</p>
                <p style='color: #64b6ff; font-weight: 700; margin: 0;'>{result.suggested_owner}</p>
            </div>
            <div style='flex: 1;'>
                <p style='color: #b0c4de; font-size: 0.8rem; margin: 0;'>Environment</p>
                <p style='color: #64d9ff; font-weight: 700; margin: 0;'>{result.technical_details.environment}</p>
            </div>
        </div>
    </div>
    """

    st.markdown(card_html, unsafe_allow_html=True)
