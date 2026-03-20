"""
ui/pages/main_pipeline_page.py — Core Triage Pipeline UI
----------------------------------------------------------
PURPOSE:
    Renders the form to accept bug reports and user reviews,
    triggers the orchestrator pipeline, and displays results in a 3-column layout.
"""

import streamlit as st
import time
import json
import os
import pandas as pd
from pathlib import Path
from src.agents.orchestrator import run_pipeline
from src.ui.components import result_display
from src.duplicate_detection.similarity import EMBEDDING_SIMILARITY_THRESHOLD
from src.duplicate_detection.vector_store import add_reports_to_index

# Absolute paths for data
project_root = Path(__file__).resolve().parent.parent.parent.parent
raw_dir = project_root / "Data" / "raw"
csv_path = raw_dir / "processed_bug_report.csv"
processed_dir = project_root / "Data" / "processed"


def get_next_id() -> str:
    """Gets the next incremented ID from the CSV."""
    if not csv_path.exists():
        return "1"
    try:
        df = pd.read_csv(csv_path)
        if df.empty:
            return "1"
        max_id = 0
        for val in df["Id"].dropna():
            try:
                current_id = int(float(val))
                if current_id > max_id:
                    max_id = current_id
            except (ValueError, TypeError):
                pass
        return str(max_id + 1)
    except Exception:
        import uuid
        return str(uuid.uuid4())[:8]


def render():
    st.markdown(
        "<h1 style='text-align: center; color: #64b6ff; margin-bottom: 0; font-weight: 900; font-size: 2.5rem;'>🚀 Run Triage Pipeline</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; color: #b0c4de; margin-bottom: 2rem; font-size: 1rem;'>Submit a bug report and optional review to trigger the triage agents</p>",
        unsafe_allow_html=True,
    )

    # 3-column layout
    col_left, col_mid, col_right = st.columns([1.2, 1.2, 1.2], gap="large")

    with col_left:
        # st.form gets glass from global CSS targeting [data-testid="stForm"]
        with st.form("triage_form"):
            st.markdown(
                "<h3 style='color: #64b6ff; font-weight: 900; margin-top: 0;'>📋 Submit New Report</h3>",
                unsafe_allow_html=True,
            )
            bug_trace = st.text_area(
                "Bug Trace / Log Dump / Stack Trace",
                height=250,
                placeholder="Paste your raw crash logs or application errors here...",
                help="This is the raw technical output that needs parsing.",
            )
            user_review = st.text_area(
                "User Review (Optional)",
                height=100,
                placeholder="User comments, steps they tried, or extra context...",
                help="Optional natural language context.",
            )
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button(
                "🔍 Run Analysis", type="primary", use_container_width=True
            )

    # ── Pipeline Live Status — st.container(border=True) gets glass from global CSS ──
    status_container = col_left.container(border=True)
    # ── Final Triage Report ──
    report_container = col_mid.container(border=True)
    # ── RAG Similarity Search ──
    rag_container = col_right.container(border=True)

    # Initialize UI state
    has_result = "last_result" in st.session_state

    with status_container:
        st.markdown(
            "<h4 style='color: #64d9ff; font-weight: 900; margin-top: 0;'>⚙️ Pipeline Live Status</h4>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='color: #b0c4de; font-size: 0.9rem; margin-bottom: 1rem;'>4 key architecture stages:</p>",
            unsafe_allow_html=True,
        )
        status_slots = {
            "preprocess": st.empty(),
            "extract": st.empty(),
            "duplicate_detection": st.empty(),
            "triage": st.empty(),
        }

    def render_status_item(
        slot, stage_name, description, is_complete=False, is_active=False
    ):
        icon = "✅" if is_complete else ("🔄" if is_active else "⏳")
        border_color = (
            "#64d9ff"
            if is_complete
            else ("#ffc107" if is_active else "rgba(100, 150, 220, 0.3)")
        )
        bg_color = (
            "rgba(50, 100, 80, 0.3)"
            if is_complete
            else ("rgba(150, 100, 20, 0.2)" if is_active else "rgba(10, 20, 35, 0.5)")
        )
        text_color = (
            "#64d9ff" if is_complete else ("#ffc107" if is_active else "#b0c4de")
        )
        slot.markdown(
            f"""
             <div style='background: {bg_color}; border-left: 4px solid {border_color}; border-radius: 8px; padding: 0.8rem; margin-bottom: 0.5rem;'>
                 <p style='color: {text_color}; font-weight: 800; margin: 0; font-size: 0.95rem;'>{icon} {stage_name}</p>
                 <p style='color: #b0c4de; margin: 0.3rem 0 0 0; font-size: 0.85rem; white-space: pre-wrap;'>{description.replace('✅ ', '')}</p>
             </div>
             """,
            unsafe_allow_html=True,
        )

    # Initial render of status slots
    if not submitted:
        if has_result:
            similar_reports = st.session_state["last_similar"]
            render_status_item(
                status_slots["preprocess"],
                "Preprocessing",
                "[Filter] Stripped emotion, memory dumps.\n[Logger] Logged regex rules applied.",
                True,
            )
            render_status_item(
                status_slots["extract"],
                "Extraction",
                "[LangChain] Extracting structured JSON.\nSummary created.",
                True,
            )
            render_status_item(
                status_slots["duplicate_detection"],
                "Duplicate Detection",
                f"[FAISS] Vector similarity search initiated.\nThreshold: {int(EMBEDDING_SIMILARITY_THRESHOLD * 100)}%. Matched: {len(similar_reports)}",
                True,
            )
            render_status_item(
                status_slots["triage"],
                "Triage",
                "[Policy] Severity rules applied.\nRouting suggested.",
                True,
            )
        else:
            render_status_item(
                status_slots["preprocess"], "Preprocessing", "Waiting for input...", False
            )
            render_status_item(
                status_slots["extract"], "Extraction", "Waiting for input...", False
            )
            render_status_item(
                status_slots["duplicate_detection"],
                "Duplicate Detection",
                "Waiting for input...",
                False,
            )
            render_status_item(
                status_slots["triage"], "Triage", "Waiting for input...", False
            )

    if submitted:
        if not bug_trace.strip():
            st.error("Please provide a Bug Trace to run the analysis.")
            return

        has_result = False
        render_status_item(
            status_slots["preprocess"], "Preprocessing", "Processing incoming text...", False, True
        )
        render_status_item(
            status_slots["extract"], "Extraction", "Waiting for input...", False, False
        )
        render_status_item(
            status_slots["duplicate_detection"], "Duplicate Detection", "Waiting for input...", False, False
        )
        render_status_item(
            status_slots["triage"], "Triage", "Waiting for input...", False, False
        )

        try:
            start_time = time.time()
            for event in run_pipeline(bug_trace=bug_trace, user_review=user_review):
                node = event.get("node_name")

                if node == "preprocess":
                    render_status_item(
                        status_slots["preprocess"],
                        "Preprocessing",
                        "[Filter] Stripped emotion, memory dumps.\n[Logger] Logged regex rules applied.",
                        True,
                    )
                    render_status_item(
                        status_slots["extract"], "Extraction", "Calling LLM for extraction...", False, True
                    )

                elif node == "extract":
                    render_status_item(
                        status_slots["extract"],
                        "Extraction",
                        "[LangChain] Extracting structured JSON.\nSummary created.",
                        True,
                    )
                    render_status_item(
                        status_slots["duplicate_detection"],
                        "Duplicate Detection",
                        "Searching FAISS vector DB...",
                        False,
                        True,
                    )

                elif node == "duplicate_detection":
                    state = event.get("current_state", {})
                    sim = state.get("similar_reports", [])
                    render_status_item(
                        status_slots["duplicate_detection"],
                        "Duplicate Detection",
                        f"[FAISS] Vector similarity search finished.\nThreshold: {int(EMBEDDING_SIMILARITY_THRESHOLD * 100)}%. Matched: {len(sim)}",
                        True,
                    )
                    render_status_item(
                        status_slots["triage"], "Triage", "Applying severity policies...", False, True
                    )

                elif node == "triage":
                    render_status_item(
                        status_slots["triage"],
                        "Triage",
                        "[Policy] Severity rules applied.\nRouting suggested.",
                        True,
                    )

                elif node == "error":
                    st.error("Pipeline encountered an error.")
                    break

                elif node == "completed":
                    duration = time.time() - start_time
                    result = event.get("final_triage_result")
                    similar_reports = event.get("similar_reports", [])

                    tech_details_dict = (
                        result.technical_details.model_dump()
                        if hasattr(result.technical_details, "model_dump")
                        else result.technical_details
                    )
                    combined_text = f"""
                    User Review: {user_review}
                    Issue Summary: {result.issue_summary}
                    Steps to Reproduce: {', '.join(result.steps_to_reproduce)}
                    User Impact: {result.user_impact_assessment}
                    Technical Details: {json.dumps(tech_details_dict)}
                    """

                    st.session_state["last_result"] = result
                    st.session_state["last_bug_trace"] = bug_trace
                    st.session_state["last_user_review"] = user_review
                    st.session_state["last_duration"] = duration
                    st.session_state["last_similar"] = similar_reports
                    st.session_state["last_combined_text"] = combined_text

                    has_result = True
                    break

        except Exception as e:
            st.error(f"Pipeline execution failed: {str(e)}")
            st.exception(e)
            return

    # ── Middle Column: Final Triage Report ──
    with report_container:
        if has_result:
            result = st.session_state["last_result"]
            duration = st.session_state["last_duration"]
            result_display.render_triage_result(result, duration)

            if st.button(
                "✅ Ready to Commit",
                type="primary",
                use_container_width=True,
                key="commit_btn",
            ):
                with st.spinner("Committing to standard dataset & vector store..."):
                    try:
                        new_id = get_next_id()
                        bug_trace = st.session_state["last_bug_trace"]
                        user_review = st.session_state["last_user_review"]

                        if csv_path.exists():
                            df = pd.read_csv(csv_path)
                            for col in ["Id", "Bug Details", "User Review"]:
                                if col not in df.columns:
                                    df[col] = ""
                        else:
                            os.makedirs(raw_dir, exist_ok=True)
                            df = pd.DataFrame(columns=["Id", "Bug Details", "User Review"])

                        df["Id"] = (
                            pd.to_numeric(df["Id"], errors="coerce")
                            .fillna(0)
                            .astype("int64")
                        )

                        new_row = pd.DataFrame(
                            [{
                                "Id": int(new_id),
                                "Bug Details": str(bug_trace) if bug_trace else "",
                                "User Review": (
                                    str(user_review) if user_review else "No user review provided"
                                ),
                            }]
                        )
                        df = pd.concat([df, new_row], ignore_index=True)
                        df = df[["Id", "Bug Details", "User Review"]]
                        df.to_csv(csv_path, index=False)

                        os.makedirs(processed_dir, exist_ok=True)
                        json_path = processed_dir / "processed_bug_reports.json"
                        processed_data = {}
                        if json_path.exists():
                            with open(json_path, "r", encoding="utf-8") as f:
                                processed_data = json.load(f)
                        processed_data[new_id] = json.loads(result.model_dump_json())
                        with open(json_path, "w", encoding="utf-8") as f:
                            json.dump(processed_data, f, indent=2)

                        combined_text = st.session_state["last_combined_text"]
                        metadata = {
                            "id": new_id,
                            "issue_summary": result.issue_summary,
                            "steps": ", ".join(result.steps_to_reproduce),
                            "severity": result.severity,
                            "team": result.suggested_owner,
                        }
                        add_reports_to_index([combined_text], [metadata])

                        st.success(f"Successfully committed Bug Report #{new_id}!")
                        del st.session_state["last_result"]

                    except Exception as e:
                        st.error(f"Commit failed: {e}")
        else:
            st.markdown(
                "<h3 style='text-align: center; color: #64b6ff; font-weight: 900;'>FINAL TRIAGE REPORT</h3>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<p style='text-align: center; color: #b0c4de;'>Submit a report to see the analysis</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                """
                <div style='display: flex; justify-content: space-between; gap: 1rem; margin: 1.5rem 0;'>
                    <div style='flex: 1; text-align: center; padding: 1.5rem; background: rgba(10, 20, 35, 0.4); border: 2px solid rgba(100, 150, 220, 0.3); border-radius: 12px;'>
                        <p style='color: #b0c4de; margin: 0; font-size: 0.9rem; font-weight: 700;'>Assigned Severity</p>
                        <h2 style='color: rgba(100, 150, 220, 0.5); margin: 0.5rem 0 0 0;'>--</h2>
                    </div>
                    <div style='flex: 1; text-align: center; padding: 1.5rem; background: rgba(10, 20, 35, 0.4); border: 2px solid rgba(100, 150, 220, 0.3); border-radius: 12px;'>
                        <p style='color: #b0c4de; margin: 0; font-size: 0.9rem; font-weight: 700;'>Suggested Owner</p>
                        <h2 style='color: rgba(100, 150, 220, 0.5); margin: 0.5rem 0 0 0;'>--</h2>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("---")
            st.markdown("#### 📝 Issue Summary\n*Awaiting input...*")
            st.markdown("#### 🔧 Steps to Reproduce\n*Awaiting input...*")

    # ── Right Column: RAG Similarity Search ──
    with rag_container:
        st.markdown(
            "<h4 style='color: #64d9ff; font-weight: 900; margin-top: 0;'>🔍 RAG Similarity Search</h4>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='color: #b0c4de; font-size: 0.85rem;'>(FAISS/ChromaDB)</p>",
            unsafe_allow_html=True,
        )

        if has_result:
            similar_reports = st.session_state["last_similar"]
            if not similar_reports:
                st.info("ℹ️ No similar reports found above the threshold.")
            else:
                for i, rep in enumerate(similar_reports):
                    score_pct = rep.get("similarity_score", 0) * 100
                    if score_pct >= 90:
                        score_color = "#ff6b6b"
                    elif score_pct >= 75:
                        score_color = "#ff9800"
                    else:
                        score_color = "#ffc107"

                    with st.expander(
                        f"🔗 POTENTIAL DUPLICATE {i+1} — Match: {score_pct:.1f}%",
                        expanded=(i == 0),
                    ):
                        st.markdown(
                            f"<div style='background: rgba(100, 182, 255, 0.15); border-left: 4px solid {score_color}; border-radius: 8px; padding: 1rem;'>"
                            f"<p style='color: {score_color}; font-weight: 900; margin: 0;'>Similarity: {score_pct:.2f}%</p>"
                            f"</div>",
                            unsafe_allow_html=True,
                        )
                        st.markdown(
                            f"<p style='color: #b0c4de; font-size: 0.9rem; margin-top: 0.5rem;'><strong>ID:</strong> <span style='color: #64b6ff;'>{rep.get('id')}</span></p>"
                            f"<p style='color: #e0e6ff; margin: 0.3rem 0;'><strong>Summary:</strong> {rep.get('summary')}</p>"
                            f"<p style='color: #b0c4de; margin: 0.3rem 0;'><strong>Steps:</strong> {rep.get('steps')}</p>"
                            f"<p style='color: #b0c4de; margin: 0.3rem 0;'><strong>Severity:</strong> <span style='color: #ff9800; font-weight: 700;'>{rep.get('severity')}</span></p>"
                            f"<p style='color: #b0c4de; margin: 0.3rem 0;'><strong>Team:</strong> <span style='color: #64d9ff;'>{rep.get('team')}</span></p>",
                            unsafe_allow_html=True,
                        )
        else:
            st.info("ℹ️ Submit a report to search for similar historical issues.")
