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
import altair as alt

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
JSON_PATH = PROJECT_ROOT / "Data" / "processed" / "processed_bug_reports.json"
POLICIES_DIR = PROJECT_ROOT / "src" / "policies"


def load_policies():
    """Loads severity and team definitions from YAML files."""
    severities = ["P1_Critical", "P2_High", "P3_Medium", "P4_Low"]
    teams = ["Platform-Team"]  # Default

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

        # Flatten JSON structure for DataFrame
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
            .metric-card {
                background: rgba(15, 28, 50, 0.7);
                border: 2px solid rgba(100, 150, 220, 0.3);
                border-radius: 12px;
                padding: 1.5rem;
                text-align: center;
                transition: all 0.3s ease;
                margin-bottom: 20px;
            }
            .metric-card:hover {
                border-color: #64b6ff;
                box-shadow: 0 4px 15px rgba(100, 182, 255, 0.2);
                transform: translateY(-5px);
            }
            .metric-val {
                color: #64b6ff;
                font-size: 2.5rem;
                font-weight: 800;
            }
            .metric-lab {
                color: #b0c4de;
                font-size: 0.9rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 1px;
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
            [data-testid="stHorizontalBlock"] > div > [data-testid="stVerticalBlock"]::before {
                content: '';
                position: absolute;
                top: 0; left: 0; right: 0;
                height: 1px;
                background: linear-gradient(90deg, transparent, rgba(100, 182, 255, 0.45), transparent);
            }
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
            .stDataFrame div {
                background-color: transparent !important;
            }
        </style>
        <link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&display=swap" rel="stylesheet">
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<h1 style='text-align: center; color: #64b6ff; margin-bottom: 0px; font-weight: 900; font-size: 3rem;'>📊 TRIAGE ANALYTICS</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; color: #b0c4de; margin-bottom: 3rem; font-size: 1.1rem;'>// REAL-TIME SYSTEM PERFORMANCE DASHBOARD //</p>",
        unsafe_allow_html=True,
    )

    df = load_data()
    all_severities, all_teams = load_policies()

    if df.empty:
        st.markdown(
            "<div class='metric-card' style='text-align: center;'><h3>No Data Found</h3><p>Run the triage pipeline to generate analytics.</p></div>",
            unsafe_allow_html=True,
        )
        return

    # --- TOP METRICS ---
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown(
            f"""<div class='metric-card'><div class='metric-val'>{len(df)}</div><div class='metric-lab'>Reports handled</div></div>""",
            unsafe_allow_html=True,
        )

    with m2:
        top_sev = df["Severity"].mode()[0] if not df["Severity"].empty else "N/A"
        st.markdown(
            f"""<div class='metric-card'><div class='metric-val' style='color: #ff9999;'>{top_sev}</div><div class='metric-lab'>Main Impact</div></div>""",
            unsafe_allow_html=True,
        )

    with m3:
        top_owner = df["Owner"].mode()[0] if not df["Owner"].empty else "N/A"
        st.markdown(
            f"""<div class='metric-card'><div class='metric-val' style='color: #99ff99;'>{top_owner.split('-')[0]}</div><div class='metric-lab'>Lead Assignee</div></div>""",
            unsafe_allow_html=True,
        )

    with m4:
        avg_char = int(df["Summary"].str.len().mean()) if not df["Summary"].empty else 0
        st.markdown(
            f"""<div class='metric-card'><div class='metric-val' style='color: #64d9ff;'>{avg_char}</div><div class='metric-lab'>Avg Length</div></div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # --- CHARTS ---
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

        max_val = sev_counts["Reports"].max()
        y_max = max_val + 2

        chart1 = (
            alt.Chart(sev_counts)
            .mark_bar(size=55)
            .encode(
                x=alt.X("Severity:N", title="Severity"),
                y=alt.Y(
                    "Reports:Q", title="Reports", scale=alt.Scale(domain=[0, y_max])
                ),
                color=alt.value("#64b6ff"),
            )
            .properties(height=320)
            .configure_view(fill="transparent")
            .configure(background="transparent")
        )

        st.altair_chart(chart1, use_container_width=True)

    with c2:
        st.markdown(
            "<div class='section-header'>🛠️ Team Load</div>", unsafe_allow_html=True
        )

        team_counts = (
            df["Owner"].value_counts().reindex(all_teams, fill_value=0).reset_index()
        )
        team_counts.columns = ["Team", "Reports"]

        max_val2 = team_counts["Reports"].max()
        y_max2 = max_val2 + 2

        chart2 = (
            alt.Chart(team_counts)
            .mark_bar(size=55)
            .encode(
                x=alt.X("Team:N", sort="-y", title="Team"),
                y=alt.Y(
                    "Reports:Q", title="Reports", scale=alt.Scale(domain=[0, y_max2])
                ),
                color=alt.value("#a855f7"),
            )
            .properties(height=320)
            .configure_view(fill="transparent")  # removes black background
            .configure(background="transparent")  # makes full chart transparent
        )

        st.altair_chart(chart2, use_container_width=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # --- PATTERN ANALYSIS ---# --- PATTERN ANALYSIS ---
    st.markdown("### 🧬 ERROR PATTERN RECOGNITION")

    error_df = df["Error"].value_counts().reset_index()
    error_df.columns = ["Error Type", "Frequency"]

    styled_error_df = error_df.style.set_properties(
        **{"background-color": "transparent", "color": "white", "border-color": "#333"}
    )

    st.dataframe(styled_error_df, use_container_width=True, hide_index=True, height=250)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # --- RAW DATA TABLE ---
    st.markdown("### 📋 RECENT CLASSIFICATIONS")

    raw_df = df[["Id", "Severity", "Owner", "Summary", "Timestamp"]].sort_values(
        "Id", ascending=True
    )

    styled_raw_df = raw_df.style.set_properties(
        **{"background-color": "transparent", "color": "white", "border-color": "#333"}
    )

    st.dataframe(styled_raw_df, use_container_width=True, hide_index=True)

    # Footer
    st.markdown("---")
    st.caption("Data synchronize status: ONLINE | Source: processed_bug_reports.json")
