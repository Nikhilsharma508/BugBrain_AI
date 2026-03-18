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

import streamlit as st


def render_severity_badge(severity: str):
    """
    Renders a colour-coded severity badge with bright, highly visible styling.

    Args:
        severity: Severity string (e.g., "P1 (Critical)", "P2 (High)", "P3 (Medium)", "P4 (Low)")
    """
    # Map severity to colors
    colors = {
        "P1": ("#ff6b6b", "#ffaaaa", "🔴 CRITICAL"),
        "P2": ("#ff9800", "#ffb84d", "🟠 HIGH"),
        "P3": ("#ffc107", "#ffe082", "🟡 MEDIUM"),
        "P4": ("#4caf50", "#81c784", "🟢 LOW"),
    }

    # Extract priority level
    priority = severity.split()[0] if severity else "P3"
    bg_color, border_color, label = colors.get(priority, colors["P3"])

    badge_html = f"""
    <div style='
        display: inline-block;
        background: {bg_color}33;
        border: 2px solid {bg_color};
        border-radius: 20px;
        padding: 0.4rem 1rem;
        font-weight: 900;
        font-size: 0.85rem;
        color: {bg_color};
        text-align: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    '>
        {label}
    </div>
    """
    st.markdown(badge_html, unsafe_allow_html=True)
