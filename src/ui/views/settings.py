"""
src/ui/views/settings.py — Interactive Node-Based Settings
------------------------------------------------------------
PURPOSE:
    A futuristic, animated settings dashboard with interactive
    node-linked visualizations. Click nodes to expand their config panels.
    Handles session-based overrides for all system variables.
"""

import streamlit as st
import os

# ─────────────────────────────────────────────────────────────────────────────
# CSS INJECTION
# ─────────────────────────────────────────────────────────────────────────────
NODE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Space+Mono:wght@400;700&display=swap');

/* ── GLOBAL RESET ── */
*, *::before, *::after { box-sizing: border-box; }

.stApp { background: #050a14 !important; }
section[data-testid="stSidebar"] { background: #08101f !important; }
.main .block-container { padding-top: 2rem !important; max-width: 1100px !important; }

/* ── ANIMATED STAR BACKGROUND ── */
.node-bg {
    position: fixed; inset: 0; pointer-events: none; z-index: 0;
    background:
        radial-gradient(ellipse at 20% 50%, rgba(100,182,255,0.04) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 20%, rgba(168,85,247,0.04) 0%, transparent 50%),
        radial-gradient(ellipse at 60% 80%, rgba(6,182,212,0.04) 0%, transparent 50%);
}

/* ── HEADER ── */
.env-title {
    font-family: 'Orbitron', monospace;
    font-size: 2.6rem;
    font-weight: 900;
    text-align: center;
    letter-spacing: 8px;
    color: transparent;
    background: linear-gradient(135deg, #64b6ff 0%, #a855f7 50%, #06b6d4 100%);
    -webkit-background-clip: text;
    background-clip: text;
    text-shadow: none;
    margin-bottom: 0.3rem;
    animation: titlePulse 4s ease-in-out infinite;
}
@keyframes titlePulse {
    0%, 100% { filter: brightness(1); }
    50% { filter: brightness(1.25); }
}
.env-subtitle {
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    text-align: center;
    color: #4a6fa5;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 3rem;
}

/* ── NODE BUTTON ── */
.node-wrapper { position: relative; margin-bottom: 6px; }

.node-btn-llm, .node-btn-emb, .node-btn-vec, .node-btn-obs {
    font-family: 'Orbitron', monospace !important;
    font-size: 0.7rem !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    border-radius: 40px !important;
    border: none !important;
    padding: 10px 24px !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    position: relative !important;
    overflow: hidden !important;
    width: 100% !important;
}

/* LLM - Purple */
.node-btn-llm {
    background: linear-gradient(135deg, #2d1b4e, #4a1e8a) !important;
    color: #d8b4fe !important;
    box-shadow: 0 0 20px rgba(168,85,247,0.5), inset 0 1px 0 rgba(255,255,255,0.1) !important;
}
.node-btn-llm:hover { box-shadow: 0 0 35px rgba(168,85,247,0.8), inset 0 1px 0 rgba(255,255,255,0.2) !important; transform: translateY(-2px) !important; }

/* EMBEDDING - Cyan */
.node-btn-emb {
    background: linear-gradient(135deg, #0a2a35, #0e5a6e) !important;
    color: #67e8f9 !important;
    box-shadow: 0 0 20px rgba(6,182,212,0.5), inset 0 1px 0 rgba(255,255,255,0.1) !important;
}
.node-btn-emb:hover { box-shadow: 0 0 35px rgba(6,182,212,0.8) !important; transform: translateY(-2px) !important; }

/* VECTOR - Amber */
.node-btn-vec {
    background: linear-gradient(135deg, #2a1a00, #6b3a00) !important;
    color: #fcd34d !important;
    box-shadow: 0 0 20px rgba(245,158,11,0.5), inset 0 1px 0 rgba(255,255,255,0.1) !important;
}
.node-btn-vec:hover { box-shadow: 0 0 35px rgba(245,158,11,0.8) !important; transform: translateY(-2px) !important; }

/* OBSERVABILITY - Red */
.node-btn-obs {
    background: linear-gradient(135deg, #2a0a0a, #6b1414) !important;
    color: #fca5a5 !important;
    box-shadow: 0 0 20px rgba(239,68,68,0.5), inset 0 1px 0 rgba(255,255,255,0.1) !important;
}
.node-btn-obs:hover { box-shadow: 0 0 35px rgba(239,68,68,0.8) !important; transform: translateY(-2px) !important; }

/* ── CONNECTOR LINE ── */
.connector-line {
    width: 2px;
    background: linear-gradient(to bottom, rgba(100,150,220,0.6), rgba(100,150,220,0.0));
    margin: 0 auto 4px;
    border-radius: 2px;
    animation: lineFlow 2s ease-in-out infinite;
}
@keyframes lineFlow {
    0%, 100% { opacity: 0.4; }
    50% { opacity: 1; }
}

/* ── CONFIG PANEL ── */
.config-panel {
    background: rgba(8, 18, 35, 0.92);
    border-radius: 16px;
    padding: 20px 24px;
    margin-top: 4px;
    animation: panelIn 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
    position: relative;
    overflow: hidden;
}
.config-panel::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 16px;
    padding: 1px;
    background: linear-gradient(135deg, rgba(100,182,255,0.3), rgba(168,85,247,0.2), rgba(6,182,212,0.3));
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor; mask-composite: exclude;
    pointer-events: none;
}
@keyframes panelIn {
    from { opacity: 0; transform: translateY(-12px) scale(0.97); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
}

/* ── PANEL HEADERS ── */
.panel-header-llm  { color: #c084fc; font-family: 'Space Mono', monospace; font-size: 0.7rem; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 14px; font-weight: 700; }
.panel-header-emb  { color: #22d3ee; font-family: 'Space Mono', monospace; font-size: 0.7rem; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 14px; font-weight: 700; }
.panel-header-vec  { color: #fbbf24; font-family: 'Space Mono', monospace; font-size: 0.7rem; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 14px; font-weight: 700; }
.panel-header-obs  { color: #f87171; font-family: 'Space Mono', monospace; font-size: 0.7rem; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 14px; font-weight: 700; }

/* ── SUB-PROVIDER BADGE ── */
.provider-badge {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    font-weight: 700;
    padding: 4px 14px;
    border-radius: 20px;
    letter-spacing: 2px;
    margin-bottom: 14px;
    animation: badgePop 0.4s cubic-bezier(0.34,1.56,0.64,1);
}
@keyframes badgePop {
    from { transform: scale(0.7); opacity: 0; }
    to   { transform: scale(1); opacity: 1; }
}
.badge-gemini     { background: rgba(99,102,241,0.2); color: #a5b4fc; border: 1px solid rgba(99,102,241,0.5); }
.badge-azure      { background: rgba(59,130,246,0.2); color: #93c5fd; border: 1px solid rgba(59,130,246,0.5); }
.badge-ollama     { background: rgba(16,185,129,0.2); color: #6ee7b7; border: 1px solid rgba(16,185,129,0.5); }
.badge-openrouter { background: rgba(249,115,22,0.2); color: #fdba74; border: 1px solid rgba(249,115,22,0.5); }

/* ── DIVIDER ── */
.node-divider {
    height: 1px;
    background: linear-gradient(to right, transparent, rgba(100,150,220,0.3), transparent);
    margin: 14px 0;
}

/* ── STATUS TAG ── */
.status-tag {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: #2dff8f;
    letter-spacing: 1px;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    margin-top: 8px;
}
.status-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #2dff8f;
    animation: blink 1.5s ease-in-out infinite;
}
@keyframes blink {
    0%, 100% { opacity: 1; } 50% { opacity: 0.2; }
}

/* ── BULK OPERATIONS PANEL ── */
.bulk-panel {
    background: rgba(8, 18, 35, 0.85);
    border-radius: 16px;
    padding: 22px 26px;
    margin-top: 30px;
    border: 1px solid rgba(100, 150, 220, 0.15);
}
.bulk-title {
    font-family: 'Orbitron', monospace;
    font-size: 0.9rem;
    font-weight: 700;
    color: #64b6ff;
    letter-spacing: 3px;
    margin-bottom: 6px;
}
.bulk-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #3a5580;
    letter-spacing: 1px;
    margin-bottom: 16px;
}

/* ── FOOTER ── */
.node-footer {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: #1e3050;
    text-align: center;
    letter-spacing: 2px;
    margin-top: 30px;
    padding-bottom: 20px;
}

/* ── STREAMLIT WIDGET OVERRIDES ── */
div[data-testid="stSelectbox"] label,
div[data-testid="stTextInput"] label,
div[data-testid="stSlider"] label,
div[data-testid="stCheckbox"] label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.62rem !important;
    letter-spacing: 1.5px !important;
    color: #4a7aaa !important;
    text-transform: uppercase !important;
}

div[data-testid="stSelectbox"] > div > div,
div[data-testid="stTextInput"] > div > div > input {
    background: rgba(5, 15, 30, 0.8) !important;
    border: 1px solid rgba(100, 150, 220, 0.2) !important;
    border-radius: 8px !important;
    color: #c8dff8 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
}

div[data-testid="stSlider"] [role="slider"] {
    background: #64b6ff !important;
    box-shadow: 0 0 10px rgba(100, 182, 255, 0.7) !important;
}

/* Node column left layout */
.node-column { display: flex; flex-direction: column; gap: 8px; padding-top: 10px; }

/* Floating orbit animation for active node */
.active-node-glow {
    animation: nodeOrbit 3s ease-in-out infinite;
}
@keyframes nodeOrbit {
    0%, 100% { filter: brightness(1) drop-shadow(0 0 8px currentColor); }
    50% { filter: brightness(1.4) drop-shadow(0 0 18px currentColor); }
}
</style>
"""


def render():
    st.markdown(NODE_CSS, unsafe_allow_html=True)
    st.markdown("<div class='node-bg'></div>", unsafe_allow_html=True)

    # ── HEADER ────────────────────────────────────────────────────────────────
    st.markdown(
        "<div class='env-title'>ENVIRONMENT NODES</div>", unsafe_allow_html=True
    )
    st.markdown(
        "<div class='env-subtitle'>// configure system-wide variables interactively //</div>",
        unsafe_allow_html=True,
    )

    # ── SESSION STATE ─────────────────────────────────────────────────────────
    if "active_node" not in st.session_state:
        st.session_state.active_node = "llm"

    # ── TWO-COLUMN LAYOUT ─────────────────────────────────────────────────────
    left_col, right_col = st.columns([1, 2.4], gap="large")

    # ── LEFT: NODE SELECTOR COLUMN ────────────────────────────────────────────
    with left_col:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        nodes = [
            ("llm", "🧠", "LLM_PROVIDER", "node-btn-llm"),
            ("emb", "🧬", "EMBEDDING", "node-btn-emb"),
            ("vec", "📦", "VECTOR_STORE", "node-btn-vec"),
            ("obs", "🔭", "OBSERVABILITY", "node-btn-obs"),
        ]

        for node_id, icon, label, btn_class in nodes:
            is_active = st.session_state.active_node == node_id
            prefix = "▶ " if is_active else "   "
            if st.button(
                f"{icon}  {prefix}{label}",
                key=f"node_{node_id}",
                use_container_width=True,
            ):
                st.session_state.active_node = node_id
                st.rerun()

            # Connector line below active node
            if is_active:
                st.markdown(
                    "<div class='connector-line' style='height:28px'></div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        # Live indicator
        st.markdown(
            """
            <div class='status-tag'>
                <span class='status-dot'></span>SESSION ACTIVE
            </div>
        """,
            unsafe_allow_html=True,
        )

    # ── RIGHT: CONFIG PANEL ───────────────────────────────────────────────────
    with right_col:
        active = st.session_state.active_node

        # ── LLM NODE ──────────────────────────────────────────────────────────
        if active == "llm":
            st.markdown("<div class='config-panel'>", unsafe_allow_html=True)
            st.markdown(
                "<div class='panel-header-llm'>⬡ CORE LLM PARAMETERS</div>",
                unsafe_allow_html=True,
            )

            c1, c2 = st.columns(2)
            temp = c1.slider(
                "Temperature",
                0.0,
                1.0,
                float(os.getenv("LLM_TEMPERATURE", "0.0")),
                0.05,
            )
            tokens = c2.text_input(
                "Max Tokens", value=os.getenv("LLM_MAX_TOKENS", "None")
            )
            os.environ["LLM_TEMPERATURE"] = str(temp)
            os.environ["LLM_MAX_TOKENS"] = tokens

            st.markdown("<div class='node-divider'></div>", unsafe_allow_html=True)

            provider_options = ["ollama", "gemini", "azure", "openrouter"]
            base_model = st.selectbox(
                "LLM_BASE_MODEL",
                options=provider_options,
                index=provider_options.index(os.getenv("LLM_BASE_MODEL", "ollama")),
            )
            os.environ["LLM_BASE_MODEL"] = base_model

            st.markdown("<div class='node-divider'></div>", unsafe_allow_html=True)

            # Provider-specific pop-up
            BADGE = {
                "gemini": ("badge-gemini", "💎 GEMINI COMPONENTS"),
                "azure": ("badge-azure", "☁️ AZURE OPENAI COMPONENTS"),
                "ollama": ("badge-ollama", "🦙 OLLAMA COMPONENTS"),
                "openrouter": ("badge-openrouter", "🌐 OPENROUTER COMPONENTS"),
            }
            cls, label = BADGE[base_model]
            st.markdown(
                f"<div class='provider-badge {cls}'>{label}</div>",
                unsafe_allow_html=True,
            )

            if base_model == "gemini":
                gem_key = st.text_input(
                    "GEMINI_API_KEY",
                    value=os.getenv("GEMINI_API_KEY", ""),
                    type="password",
                )
                gem_mod = st.text_input(
                    "GEMINI_MODEL", value=os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
                )
                os.environ["GEMINI_API_KEY"] = gem_key
                os.environ["GEMINI_MODEL"] = gem_mod

            elif base_model == "azure":
                az_key = st.text_input(
                    "AZURE_OPENAI_API_KEY",
                    value=os.getenv("AZURE_OPENAI_API_KEY", ""),
                    type="password",
                )
                az_end = st.text_input(
                    "AZURE_OPENAI_ENDPOINT",
                    value=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
                )
                az_ver = st.text_input(
                    "AZURE_OPENAI_API_VERSION",
                    value=os.getenv("AZURE_OPENAI_API_VERSION", ""),
                )
                az_dep = st.text_input(
                    "AZURE_OPENAI_DEPLOYMENT",
                    value=os.getenv("AZURE_OPENAI_DEPLOYMENT", ""),
                )
                os.environ["AZURE_OPENAI_API_KEY"] = az_key
                os.environ["AZURE_OPENAI_ENDPOINT"] = az_end
                os.environ["AZURE_OPENAI_API_VERSION"] = az_ver
                os.environ["AZURE_OPENAI_DEPLOYMENT"] = az_dep

            elif base_model == "ollama":
                oll_mod = st.text_input(
                    "OLLAMA_MODEL",
                    value=os.getenv("OLLAMA_MODEL", "gpt-oss:120b-cloud"),
                )
                os.environ["OLLAMA_MODEL"] = oll_mod

            elif base_model == "openrouter":
                or_key = st.text_input(
                    "OPENROUTER_API_KEY",
                    value=os.getenv("OPENROUTER_API_KEY", ""),
                    type="password",
                )
                or_mod = st.text_input(
                    "OPENROUTER_MODEL",
                    value=os.getenv(
                        "OPENROUTER_MODEL", "meta-llama/llama-3-70b-instruct"
                    ),
                )
                os.environ["OPENROUTER_API_KEY"] = or_key
                os.environ["OPENROUTER_MODEL"] = or_mod

            st.markdown("</div>", unsafe_allow_html=True)

        # ── EMBEDDING NODE ────────────────────────────────────────────────────
        elif active == "emb":
            st.markdown("<div class='config-panel'>", unsafe_allow_html=True)
            st.markdown(
                "<div class='panel-header-emb'>⬡ EMBEDDING CONFIGURATION</div>",
                unsafe_allow_html=True,
            )

            emb_mod = st.text_input(
                "EMBEDDING_MODEL",
                value=os.getenv("EMBEDDING_MODEL", "qwen3-embedding:0.6b"),
            )
            os.environ["EMBEDDING_MODEL"] = emb_mod

            st.markdown("<div class='node-divider'></div>", unsafe_allow_html=True)
            st.markdown(
                "<div class='provider-badge badge-gemini'>📐 SIMILARITY PARAMETERS</div>",
                unsafe_allow_html=True,
            )

            emb_threshold = st.slider(
                "EMBEDDING_SIMILARITY_THRESHOLD",
                0.0,
                1.0,
                float(os.getenv("EMBEDDING_SIMILARITY_THRESHOLD", "0.2")),
                0.05,
            )
            os.environ["EMBEDDING_SIMILARITY_THRESHOLD"] = str(emb_threshold)

            st.markdown("</div>", unsafe_allow_html=True)

        # ── VECTOR STORE NODE ─────────────────────────────────────────────────
        elif active == "vec":
            st.markdown("<div class='config-panel'>", unsafe_allow_html=True)
            st.markdown(
                "<div class='panel-header-vec'>⬡ VECTOR STORE CONFIGURATION</div>",
                unsafe_allow_html=True,
            )

            v_type = st.selectbox(
                "VECTOR_STORE_TYPE",
                options=["faiss", "chromadb"],
                index=["faiss", "chromadb"].index(
                    os.getenv("VECTOR_STORE_TYPE", "faiss")
                ),
            )
            os.environ["VECTOR_STORE_TYPE"] = v_type

            st.markdown("<div class='node-divider'></div>", unsafe_allow_html=True)

            v_path = st.text_input(
                "VECTOR_STORE_PATH",
                value=os.getenv("VECTOR_STORE_PATH", "data/vector_store"),
            )
            os.environ["VECTOR_STORE_PATH"] = v_path

            st.markdown("</div>", unsafe_allow_html=True)

        # ── OBSERVABILITY NODE ────────────────────────────────────────────────
        elif active == "obs":
            st.markdown("<div class='config-panel'>", unsafe_allow_html=True)
            st.markdown(
                "<div class='panel-header-obs'>⬡ LOGGING & OBSERVABILITY</div>",
                unsafe_allow_html=True,
            )

            c1, c2 = st.columns(2)
            l_level = c1.selectbox(
                "LOG_LEVEL",
                ["DEBUG", "INFO", "WARNING", "ERROR"],
                index=["DEBUG", "INFO", "WARNING", "ERROR"].index(
                    os.getenv("LOG_LEVEL", "INFO")
                ),
            )
            l_path = c2.text_input(
                "LOG_FILE_PATH", value=os.getenv("LOG_FILE_PATH", "data/temp/app.log")
            )
            os.environ["LOG_LEVEL"] = l_level
            os.environ["LOG_FILE_PATH"] = l_path

            st.markdown("<div class='node-divider'></div>", unsafe_allow_html=True)
            st.markdown(
                "<div class='provider-badge' style='background:rgba(239,68,68,0.15);color:#fca5a5;border:1px solid rgba(239,68,68,0.4)'>🔗 LANGCHAIN TRACING</div>",
                unsafe_allow_html=True,
            )

            tracing = st.checkbox(
                "LANGCHAIN_TRACING_V2",
                value=os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true",
            )
            lc_proj = st.text_input(
                "LANGCHAIN_PROJECT",
                value=os.getenv("LANGCHAIN_PROJECT", "ai-bug-triage"),
            )
            lc_key = st.text_input(
                "LANGCHAIN_API_KEY",
                value=os.getenv("LANGCHAIN_API_KEY", ""),
                type="password",
            )
            os.environ["LANGCHAIN_TRACING_V2"] = str(tracing).lower()
            os.environ["LANGCHAIN_PROJECT"] = lc_proj
            os.environ["LANGCHAIN_API_KEY"] = lc_key

            st.markdown("</div>", unsafe_allow_html=True)

    # ── ADVANCED BULK OPERATIONS ──────────────────────────────────────────────
    st.markdown("<div class='bulk-panel'>", unsafe_allow_html=True)
    st.markdown(
        "<div class='bulk-title'>🛠 ADVANCED BULK OPERATIONS</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='bulk-sub'>// apply sweeping changes or export your session config //</div>",
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns([1.4, 1.4, 2])

    if c1.button(
        "💾  Apply Session Settings", type="primary", use_container_width=True
    ):
        # Update session state from environment variables
        st.session_state.LLM_BASE_MODEL = os.getenv("LLM_BASE_MODEL", "ollama")
        st.session_state.LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.0"))
        st.session_state.LLM_MAX_TOKENS = os.getenv("LLM_MAX_TOKENS", "None")
        st.session_state.EMBEDDING_MODEL = os.getenv(
            "EMBEDDING_MODEL", "qwen3-embedding:0.6b"
        )
        st.session_state.EMBEDDING_SIMILARITY_THRESHOLD = float(
            os.getenv("EMBEDDING_SIMILARITY_THRESHOLD", "0.2")
        )
        st.session_state.VECTOR_STORE_TYPE = os.getenv("VECTOR_STORE_TYPE", "faiss")
        st.session_state.VECTOR_STORE_PATH = os.getenv(
            "VECTOR_STORE_PATH", "data/vector_store"
        )
        st.session_state.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        st.session_state.LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "data/temp/app.log")
        st.session_state.LANGCHAIN_TRACING_V2 = os.getenv(
            "LANGCHAIN_TRACING_V2", "false"
        )
        st.session_state.LANGCHAIN_PROJECT = os.getenv(
            "LANGCHAIN_PROJECT", "ai-bug-triage"
        )
        st.session_state.LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY", "")
        st.success("✓ Session configurations applied.")
        st.balloons()
        # st.experimental_rerun() removed for Streamlit 1.55 compatibility

    if c2.button("📤  Export Config", use_container_width=True):
        config_str = f"""# Session Export — AI Bug Triage
LLM_BASE_MODEL={os.getenv('LLM_BASE_MODEL', 'ollama')}
LLM_TEMPERATURE={os.getenv('LLM_TEMPERATURE', '0.0')}
LLM_MAX_TOKENS={os.getenv('LLM_MAX_TOKENS', 'None')}
EMBEDDING_MODEL={os.getenv('EMBEDDING_MODEL', 'qwen3-embedding:0.6b')}
EMBEDDING_SIMILARITY_THRESHOLD={os.getenv('EMBEDDING_SIMILARITY_THRESHOLD', '0.2')}
VECTOR_STORE_TYPE={os.getenv('VECTOR_STORE_TYPE', 'faiss')}
VECTOR_STORE_PATH={os.getenv('VECTOR_STORE_PATH', 'data/vector_store')}
LOG_LEVEL={os.getenv('LOG_LEVEL', 'INFO')}
LOG_FILE_PATH={os.getenv('LOG_FILE_PATH', 'data/temp/app.log')}
LANGCHAIN_TRACING_V2={os.getenv('LANGCHAIN_TRACING_V2', 'false')}
LANGCHAIN_PROJECT={os.getenv('LANGCHAIN_PROJECT', 'ai-bug-triage')}"""
        st.code(config_str, language="bash")
        st.toast("Config string generated!", icon="📋")

    c3.file_uploader(
        "Import .env File", type=["env", "txt"], label_visibility="collapsed"
    )

    # Add a button to clear cache
    if st.button("🧹 Clear Cache", use_container_width=True):
        # Clear session state keys related to config
        keys_to_clear = [
            "LLM_BASE_MODEL",
            "LLM_TEMPERATURE",
            "LLM_MAX_TOKENS",
            "EMBEDDING_MODEL",
            "EMBEDDING_SIMILARITY_THRESHOLD",
            "VECTOR_STORE_TYPE",
            "VECTOR_STORE_PATH",
            "LOG_LEVEL",
            "LOG_FILE_PATH",
            "LANGCHAIN_TRACING_V2",
            "LANGCHAIN_PROJECT",
            "LANGCHAIN_API_KEY",
        ]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        st.success("Cache cleared.")
        # st.experimental_rerun() removed for Streamlit 1.55 compatibility
    st.markdown("</div>", unsafe_allow_html=True)

    # ── FOOTER ────────────────────────────────────────────────────────────────
    st.markdown(
        "<div class='node-footer'>⚡ SESSION-SCOPED // CHANGES RESET ON APP RESTART // ALL VARS ARE TEMPORARY</div>",
        unsafe_allow_html=True,
    )
