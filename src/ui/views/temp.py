"""
src/ui/views/Dashboard.py — Analytics Dashboard
------------------------------------------------------------
PURPOSE:
    Provides visualizations and key metrics from triaged bug reports.
    Uses data from processed_bug_reports.json and processed_bug_report.csv.
"""

import streamlit as st
import pandas as pd
import json
import yaml
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
JSON_PATH = PROJECT_ROOT / "Data" / "processed" / "processed_bug_reports.json"
POLICIES_DIR = PROJECT_ROOT / "src" / "policies"


def load_policies():
    """Loads severity and team definitions from YAML files."""
    severities = ["P1_Critical", "P2_High", "P3_Medium", "P4_Low"]
    teams = ["Platform-Team"]

    sev_path = POLICIES_DIR / "severity_policy.yaml"
    team_path = POLICIES_DIR / "team_routing.yaml"

    if sev_path.exists():
        with open(sev_path, "r") as f:
            sev_data = yaml.safe_load(f)
            if "severity_levels" in sev_data:
                severities = [
                    v.get("label", k) for k, v in sev_data["severity_levels"].items()
                ]

    if team_path.exists():
        with open(team_path, "r") as f:
            team_data = yaml.safe_load(f)
            if "teams" in team_data:
                teams = list(team_data["teams"].keys())

    return severities, teams


def load_data():
    """Loads triaged bug data from JSON."""
    if not JSON_PATH.exists():
        return pd.DataFrame()

    try:
        with open(JSON_PATH, "r") as f:
            data = json.load(f)

        flat_data = []
        for bug_id, details in data.items():
            row = {
                "Id": int(bug_id),
                "Severity": details.get("severity", "Unknown"),
                "Owner": details.get("suggested_owner", "Unassigned"),
                "Summary": details.get("issue_summary", ""),
                "Error": details.get("technical_details", {}).get(
                    "detected_error", "N/A"
                ),
                "Timestamp": details.get("technical_details", {}).get(
                    "timestamp", "N/A"
                ),
            }
            flat_data.append(row)

        return pd.DataFrame(flat_data)
    except Exception as e:
        st.error(f"Error loading JSON data: {e}")
        return pd.DataFrame()


def render():
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&family=Exo+2:wght@300;400;700;900&display=swap');

            /* ── Global Reset & Background ── */
            html, body, [data-testid="stApp"] {
                background: #060d1a !important;
                font-family: 'Exo 2', sans-serif !important;
            }

            /* Animated grid background */
            [data-testid="stApp"]::before {
                content: '';
                position: fixed;
                inset: 0;
                background-image:
                    linear-gradient(rgba(100, 182, 255, 0.04) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(100, 182, 255, 0.04) 1px, transparent 1px);
                background-size: 48px 48px;
                pointer-events: none;
                z-index: 0;
            }

            /* Ambient glow orbs */
            [data-testid="stApp"]::after {
                content: '';
                position: fixed;
                top: -200px;
                left: -200px;
                width: 700px;
                height: 700px;
                background: radial-gradient(circle, rgba(100, 130, 255, 0.08) 0%, transparent 70%);
                pointer-events: none;
                z-index: 0;
                animation: orb-drift 18s ease-in-out infinite alternate;
            }

            @keyframes orb-drift {
                0%   { transform: translate(0, 0) scale(1); }
                100% { transform: translate(300px, 200px) scale(1.3); }
            }

            /* ── Universal Glass Card ── */
            /* Applied to Streamlit structural wrappers */
            [data-testid="stVerticalBlockBorderWrapper"],
            [data-testid="stForm"],
            .glass-card {
                background: rgba(12, 24, 48, 0.75) !important;
                border-radius: 16px !important;
                backdrop-filter: blur(14px) !important;
                -webkit-backdrop-filter: blur(14px) !important;
                border: 1.5px solid rgba(100, 150, 220, 0.35) !important;
                box-shadow:
                    0 8px 32px rgba(0, 0, 0, 0.6),
                    inset 0 1px 0 rgba(255, 255, 255, 0.07) !important;
                padding: 1.5rem !important;
                margin-bottom: 1.25rem !important;
                transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
                position: relative;
                overflow: hidden;
            }

            [data-testid="stVerticalBlockBorderWrapper"]::before,
            .glass-card::before {
                content: '';
                position: absolute;
                top: 0; left: 0; right: 0;
                height: 1px;
                background: linear-gradient(90deg, transparent, rgba(100, 182, 255, 0.5), transparent);
                pointer-events: none;
            }

            [data-testid="stVerticalBlockBorderWrapper"]:hover,
            [data-testid="stForm"]:hover,
            .glass-card:hover {
                border-color: rgba(100, 180, 255, 0.6) !important;
                box-shadow:
                    0 12px 48px rgba(40, 100, 200, 0.35),
                    inset 0 1px 0 rgba(255, 255, 255, 0.12) !important;
            }

            /* ── Columns: wrap each column content in glass ── */
            [data-testid="stHorizontalBlock"] > div > [data-testid="stVerticalBlock"] {
                background: rgba(12, 24, 48, 0.75) !important;
                border-radius: 16px !important;
                border: 1.5px solid rgba(100, 150, 220, 0.3) !important;
                box-shadow: 0 6px 24px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255,255,255,0.06) !important;
                backdrop-filter: blur(12px) !important;
                -webkit-backdrop-filter: blur(12px) !important;
                padding: 1.25rem 1.25rem 1rem !important;
                transition: border-color 0.3s, box-shadow 0.3s !important;
                overflow: hidden;
                position: relative;
            }

            [data-testid="stHorizontalBlock"] > div > [data-testid="stVerticalBlock"]:hover {
                border-color: rgba(100, 180, 255, 0.55) !important;
                box-shadow: 0 10px 36px rgba(40, 100, 200, 0.3), inset 0 1px 0 rgba(255,255,255,0.1) !important;
            }

            /* Top shimmer line on column cards */
            [data-testid="stHorizontalBlock"] > div > [data-testid="stVerticalBlock"]::before {
                content: '';
                position: absolute;
                top: 0; left: 0; right: 0;
                height: 1px;
                background: linear-gradient(90deg, transparent, rgba(100, 182, 255, 0.45), transparent);
            }

            /* ── DataFrame / Table Glass ── */
            [data-testid="stDataFrame"],
            .stDataFrame,
            [data-testid="stDataFrameResizable"] {
                background: rgba(10, 20, 42, 0.85) !important;
                border-radius: 12px !important;
                border: 1.5px solid rgba(100, 150, 220, 0.3) !important;
                overflow: hidden !important;
                backdrop-filter: blur(10px) !important;
            }

            /* ── Bar Chart containers ── */
            [data-testid="stArrowVegaLiteChart"],
            [data-testid="stVegaLiteChart"] {
                background: transparent !important;
                border-radius: 10px !important;
                overflow: hidden !important;
            }

            /* ── Metric Card (custom HTML) ── */
            .metric-card {
                background: rgba(10, 22, 46, 0.85);
                border: 1.5px solid rgba(100, 150, 220, 0.35);
                border-radius: 16px;
                padding: 1.6rem 1rem;
                text-align: center;
                transition: all 0.35s ease;
                margin-bottom: 0;
                position: relative;
                overflow: hidden;
                backdrop-filter: blur(14px);
                -webkit-backdrop-filter: blur(14px);
                box-shadow: 0 6px 28px rgba(0,0,0,0.55), inset 0 1px 0 rgba(255,255,255,0.07);
            }

            .metric-card::before {
                content: '';
                position: absolute;
                top: 0; left: 0; right: 0;
                height: 1px;
                background: linear-gradient(90deg, transparent, rgba(100, 182, 255, 0.5), transparent);
            }

            .metric-card:hover {
                border-color: rgba(100, 182, 255, 0.65);
                box-shadow: 0 10px 40px rgba(40, 120, 220, 0.35), inset 0 1px 0 rgba(255,255,255,0.12);
                transform: translateY(-4px);
            }

            .metric-val {
                color: #64b6ff;
                font-size: 2.4rem;
                font-weight: 900;
                font-family: 'Exo 2', sans-serif;
                line-height: 1.1;
                letter-spacing: -0.5px;
            }

            .metric-lab {
                color: #8ab0d8;
                font-size: 0.72rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 2px;
                margin-top: 6px;
                font-family: 'Share Tech Mono', monospace;
            }

            .metric-icon {
                font-size: 1.4rem;
                margin-bottom: 6px;
                display: block;
                opacity: 0.85;
            }

            /* ── Section Headers ── */
            .section-header {
                font-family: 'Rajdhani', sans-serif;
                font-size: 1.05rem;
                font-weight: 700;
                color: #90c4f0;
                text-transform: uppercase;
                letter-spacing: 2.5px;
                margin-bottom: 0.75rem;
                display: flex;
                align-items: center;
                gap: 8px;
            }

            .section-header::after {
                content: '';
                flex: 1;
                height: 1px;
                background: linear-gradient(90deg, rgba(100, 182, 255, 0.4), transparent);
                margin-left: 8px;
            }

            /* ── Page Title ── */
            .dash-title {
                text-align: center;
                font-family: 'Exo 2', sans-serif;
                font-weight: 900;
                font-size: 2.8rem;
                background: linear-gradient(135deg, #64b6ff 0%, #a78bfa 50%, #60efff 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                letter-spacing: -1px;
                margin-bottom: 4px;
            }

            .dash-sub {
                text-align: center;
                color: #5a7a9e;
                font-family: 'Share Tech Mono', monospace;
                font-size: 0.78rem;
                letter-spacing: 4px;
                margin-bottom: 2.5rem;
            }

            /* ── Status Badge ── */
            .status-dot {
                display: inline-block;
                width: 8px; height: 8px;
                background: #22dd88;
                border-radius: 50%;
                margin-right: 6px;
                animation: pulse-dot 2s ease-in-out infinite;
                vertical-align: middle;
            }

            @keyframes pulse-dot {
                0%, 100% { box-shadow: 0 0 0 0 rgba(34,221,136,0.6); }
                50%       { box-shadow: 0 0 0 5px rgba(34,221,136,0); }
            }

            /* ── Divider ── */
            hr {
                border-color: rgba(100, 150, 220, 0.2) !important;
                margin: 2rem 0 !important;
            }

            /* ── Caption / Footer ── */
            .stCaption, [data-testid="stCaptionContainer"] {
                color: #3d5a7a !important;
                font-family: 'Share Tech Mono', monospace !important;
                font-size: 0.72rem !important;
                letter-spacing: 1px !important;
                text-align: center !important;
            }

            /* ── Scrollbar ── */
            ::-webkit-scrollbar { width: 5px; height: 5px; }
            ::-webkit-scrollbar-track { background: rgba(0,0,0,0.3); border-radius: 10px; }
            ::-webkit-scrollbar-thumb { background: rgba(100, 182, 255, 0.35); border-radius: 10px; }
            ::-webkit-scrollbar-thumb:hover { background: rgba(100, 182, 255, 0.55); }

            /* ── Ensure text stays readable in all wrapped blocks ── */
            [data-testid="stVerticalBlock"] p,
            [data-testid="stVerticalBlock"] span,
            [data-testid="stVerticalBlock"] label,
            [data-testid="stVerticalBlock"] div {
                color: #d0e4ff;
            }

            /* Remove default block padding that breaks glass wrap */
            [data-testid="stMainBlockContainer"] {
                padding-top: 2rem !important;
            }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # ── Header ──
    st.markdown(
        "<div class='dash-title'>📊 TRIAGE ANALYTICS</div>", unsafe_allow_html=True
    )
    st.markdown(
        "<div class='dash-sub'>REAL-TIME SYSTEM PERFORMANCE DASHBOARD</div>",
        unsafe_allow_html=True,
    )

    df = load_data()
    all_severities, all_teams = load_policies()

    if df.empty:
        st.markdown(
            """
            <div class='glass-card' style='text-align:center; padding: 3rem;'>
                <div style='font-size:3rem;'>🛰️</div>
                <h3 style='color:#64b6ff; font-family: Rajdhani, sans-serif; letter-spacing:2px;'>NO DATA FOUND</h3>
                <p style='color:#5a7a9e; font-family: Share Tech Mono, monospace; font-size:0.85rem;'>
                    Run the triage pipeline to generate analytics.
                </p>
            </div>
        """,
            unsafe_allow_html=True,
        )
        return

    # ── TOP METRICS ──
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown(
            f"""
            <div class='metric-card'>
                <span class='metric-icon'>🗂️</span>
                <div class='metric-val'>{len(df)}</div>
                <div class='metric-lab'>Reports Handled</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with m2:
        top_sev = df["Severity"].mode()[0] if not df["Severity"].empty else "N/A"
        st.markdown(
            f"""
            <div class='metric-card'>
                <span class='metric-icon'>🔴</span>
                <div class='metric-val' style='color:#ff8080; font-size:1.7rem;'>{top_sev}</div>
                <div class='metric-lab'>Main Impact</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with m3:
        top_owner = df["Owner"].mode()[0] if not df["Owner"].empty else "N/A"
        st.markdown(
            f"""
            <div class='metric-card'>
                <span class='metric-icon'>👤</span>
                <div class='metric-val' style='color:#7eff9e; font-size:1.7rem;'>{top_owner.split('-')[0]}</div>
                <div class='metric-lab'>Lead Assignee</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with m4:
        avg_char = int(df["Summary"].str.len().mean()) if not df["Summary"].empty else 0
        st.markdown(
            f"""
            <div class='metric-card'>
                <span class='metric-icon'>✏️</span>
                <div class='metric-val' style='color:#64d9ff;'>{avg_char}</div>
                <div class='metric-lab'>Avg Summary Len</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # ── CHARTS ──
    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            "<div class='section-header'>⚡ Severity Spread</div>",
            unsafe_allow_html=True,
        )
        sev_counts = (
            df["Severity"]
            .value_counts()
            .reindex(all_severities, fill_value=0)
            .reset_index()
        )
        sev_counts.columns = ["Severity", "Reports"]
        st.bar_chart(sev_counts.set_index("Severity"), color="#64b6ff", height=260)

    with c2:
        st.markdown(
            "<div class='section-header'>🛠️ Team Load</div>", unsafe_allow_html=True
        )
        team_counts = (
            df["Owner"].value_counts().reindex(all_teams, fill_value=0).reset_index()
        )
        team_counts.columns = ["Team", "Reports"]
        st.bar_chart(team_counts.set_index("Team"), color="#a855f7", height=260)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # ── ERROR PATTERN ANALYSIS ──
    st.markdown(
        "<div class='section-header'>🧬 Error Pattern Recognition</div>",
        unsafe_allow_html=True,
    )
    error_df = df["Error"].value_counts().reset_index()
    error_df.columns = ["Error Type", "Frequency"]
    st.dataframe(error_df, use_container_width=True, hide_index=True, height=240)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # ── RAW CLASSIFICATIONS TABLE ──
    st.markdown(
        "<div class='section-header'>📋 Recent Classifications</div>",
        unsafe_allow_html=True,
    )
    st.dataframe(
        df[["Id", "Severity", "Owner", "Summary", "Timestamp"]].sort_values(
            "Id", ascending=True
        ),
        use_container_width=True,
        hide_index=True,
    )

    # ── Footer ──
    st.markdown("---")
    st.caption(
        "⬤ Data sync: ONLINE  ·  Source: processed_bug_reports.json  ·  Auto-refresh enabled"
    )
