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

from src.ui.views import main_pipeline_page, Dashboard


def main():
    st.set_page_config(
        page_title="AI Bug Triage",
        page_icon="🐛",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # ---------------------------------------------------------
    # GLOBAL AESTHETICS (Clean Dark Tech Glassmorphism)
    # ---------------------------------------------------------
    st.markdown(
        """
        <style>

            /* ── Dark gradient background ── */
            .stApp {
                background: linear-gradient(135deg, #1a2847 0%, #0f1923 50%, #162a4a 100%) !important;
                background-attachment: fixed !important;
            }

            /* ── Transparent Streamlit chrome ── */
            [data-testid="stHeader"], [data-testid="stToolbar"] {
                background: transparent !important;
                backdrop-filter: none !important;
            }
            [data-testid="stAppViewContainer"] {
                background: transparent !important;
            }
            

            /* ── Sidebar — Dark Frosted Glass ── */
            [data-testid="stSidebar"] {
                background: rgba(15, 25, 40, 0.95) !important;
                backdrop-filter: blur(15px) !important;
                -webkit-backdrop-filter: blur(15px) !important;
                border-right: 2px solid rgba(100, 150, 220, 0.3);
            }
            [data-testid="stSidebar"] * {
                color: #e0e6ff !important;
            }

            /* ══════════════════════════════════════════════════
               GLASS CARD — the single source of truth
               Applied ONLY via <div class="glass-card">
            ══════════════════════════════════════════════════ */
            .glass-card {
                background: rgba(20, 35, 60, 0.75) !important;
                border-radius: 16px !important;
                backdrop-filter: blur(12px) !important;
                -webkit-backdrop-filter: blur(12px) !important;
                border: 1.5px solid rgba(100, 150, 220, 0.35) !important;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6),
                            inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
                padding: 1.5rem !important;
                margin-bottom: 1rem !important;
                color: #f0f4ff !important;
                transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
            }
            .glass-card:hover {
                border-color: rgba(100, 180, 255, 0.55) !important;
                box-shadow: 0 12px 48px rgba(100, 150, 220, 0.35),
                            inset 0 1px 0 rgba(255, 255, 255, 0.12) !important;
            }
            /* Ensure text inside glass cards is always light */
            .glass-card h1, .glass-card h2, .glass-card h3, .glass-card h4,
            .glass-card p, .glass-card label, .glass-card span {
                color: #f0f4ff !important;
            }

            /* ══════════════════════════════════════════════════
               Glass on st.form() — works natively via DOM wrapper
            ══════════════════════════════════════════════════ */
            [data-testid="stForm"] {
                background: rgba(20, 35, 60, 0.75) !important;
                border-radius: 16px !important;
                backdrop-filter: blur(12px) !important;
                -webkit-backdrop-filter: blur(12px) !important;
                border: 1.5px solid rgba(100, 150, 220, 0.35) !important;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6),
                            inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
                padding: 1.5rem !important;
                margin-bottom: 1rem !important;
                transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
            }
            [data-testid="stForm"]:hover {
                border-color: rgba(100, 180, 255, 0.55) !important;
                box-shadow: 0 12px 48px rgba(100, 150, 220, 0.35),
                            inset 0 1px 0 rgba(255, 255, 255, 0.12) !important;
            }

            /* ══════════════════════════════════════════════════
               Glass on st.container(border=True)
               → targets [data-testid="stVerticalBlockBorderWrapper"]
               Only applies to the OUTER (top-level) containers,
               not to nested ones (e.g., the inner placeholder divs).
            ══════════════════════════════════════════════════ */
            [data-testid="stVerticalBlockBorderWrapper"] {
                background: rgba(20, 35, 60, 0.75) !important;
                border-radius: 16px !important;
                backdrop-filter: blur(12px) !important;
                -webkit-backdrop-filter: blur(12px) !important;
                border: 1.5px solid rgba(100, 150, 220, 0.35) !important;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6),
                            inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
                padding: 1.2rem !important;
                margin-bottom: 1rem !important;
                transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
            }
            [data-testid="stVerticalBlockBorderWrapper"]:hover {
                border-color: rgba(100, 180, 255, 0.55) !important;
                box-shadow: 0 12px 48px rgba(100, 150, 220, 0.35),
                            inset 0 1px 0 rgba(255, 255, 255, 0.12) !important;
            }
            /* Remove double-glass on nested border-wrappers */
            [data-testid="stVerticalBlockBorderWrapper"]
            [data-testid="stVerticalBlockBorderWrapper"] {
                background: rgba(10, 20, 40, 0.5) !important;
                border: 1px solid rgba(100, 150, 220, 0.2) !important;
                box-shadow: none !important;
                backdrop-filter: none !important;
                -webkit-backdrop-filter: none !important;
            }

            /* ── Input fields ── */
            .stTextArea textarea, .stTextInput input {
                background: rgba(10, 20, 35, 0.6) !important;
                color: #f0f4ff !important;
                border: 1.5px solid rgba(100, 150, 220, 0.3) !important;
                border-radius: 10px !important;
            }
            .stTextArea textarea:focus, .stTextInput input:focus {
                border-color: #64b6ff !important;
                box-shadow: 0 0 15px rgba(100, 182, 255, 0.6) !important;
                background: rgba(10, 20, 35, 0.8) !important;
            }

            /* ── Buttons ── */
            .stButton > button {
                background: linear-gradient(135deg, #64b6ff 0%, #4a90e2 100%) !important;
                color: #ffffff !important;
                border-radius: 12px !important;
                border: 2px solid #64b6ff !important;
                font-weight: 800 !important;
                transition: all 0.3s ease !important;
                padding: 0.7rem 1.4rem !important;
                font-size: 1rem !important;
            }
            .stButton > button:hover {
                background: linear-gradient(135deg, #82c3ff 0%, #6db3ff 100%) !important;
                transform: scale(1.05);
                box-shadow: 0 6px 20px rgba(100, 182, 255, 0.7) !important;
                border: 2px solid #82c3ff !important;
            }

            /* ── Metrics ── */
            [data-testid="stMetricValue"] {
                color: #64b6ff !important;
                font-size: 2.2rem !important;
                font-weight: 900 !important;
                text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
            }
            [data-testid="stMetricLabel"] {
                color: #b0c4de !important;
                font-weight: 700 !important;
                font-size: 1rem !important;
            }

            /* ── Expanders ── */
            [data-testid="stExpander"] {
                background: rgba(15, 28, 50, 0.7) !important;
                border: 2px solid rgba(100, 150, 220, 0.3) !important;
                border-radius: 12px !important;
            }
            [data-testid="stExpander"] * {
                color: #f0f4ff !important;
            }

            /* ── Code blocks ── */
            pre {
                background: rgba(10, 20, 35, 0.8) !important;
                border: 1px solid rgba(100, 150, 220, 0.2) !important;
                border-radius: 10px !important;
                color: #64d9ff !important;
            }

            /* ── Success/Error/Info boxes ── */
            .stSuccess {
                background: rgba(34, 139, 34, 0.2) !important;
                border: 2px solid #64d9ff !important;
                color: #90ee90 !important;
                border-radius: 12px !important;
            }
            .stError {
                background: rgba(178, 34, 34, 0.2) !important;
                border: 2px solid #ff6b6b !important;
                color: #ff9999 !important;
                border-radius: 12px !important;
            }
            .stInfo {
                background: rgba(70, 130, 180, 0.2) !important;
                border: 2px solid #64b6ff !important;
                color: #add8e6 !important;
                border-radius: 12px !important;
            }

            /* ── Top glow line on glass cards ── */
            .glass-card::before {
                content: '';
                position: absolute;
                top: 0; left: 10%; right: 10%;
                height: 1px;
                background: linear-gradient(90deg, transparent, rgba(100, 182, 255, 0.4), transparent);
                pointer-events: none;
            }
            .glass-card { position: relative; overflow: hidden; }

            /* ── Markdown text defaults ── */
            .stMarkdown, .stMarkdown p, .stMarkdown li {
                color: #e0e6ff !important;
            }
            
        </style>
    """,
        unsafe_allow_html=True,
    )

    st.sidebar.title("🐛 AI Bug Triage System")
    st.sidebar.markdown(
        "Welcome to the **uc20_bug_report_summarizer** interactive interface. "
        "This tool uses an LLM-driven LangGraph pipeline to extract, parse, "
        "and triage incoming software bug reports."
    )

    # Navigation
    page = st.sidebar.radio(
        "Navigation", ["Run Triage Pipeline", "Dashboard"]
    )

    if page == "Run Triage Pipeline":
        main_pipeline_page.render()
    elif page == "Dashboard":
        Dashboard.render()
    else:
        st.info("Feature under construction.")


if __name__ == "__main__":
    main()
