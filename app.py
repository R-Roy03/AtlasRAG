import sys
import os
import streamlit as st
import time
import json
import tempfile
import shutil

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Local Imports
from ingestion.loader import load_documents
from ingestion.chunker import chunk_documents
from ingestion.vector_store import index_documents
from retrieval.hybrid_search import HybridRetriever
from inference.generator import LLMGenerator
from evaluation.metrics import AtlasEvaluator

# ══════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════
st.set_page_config(
    page_title="AtlasRAG — Enterprise AI",
    page_icon="assets/atlas_icon.svg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════
# PREMIUM CSS INJECTION
# ══════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&family=Share+Tech+Mono&display=swap');

/* ── CSS Variables ── */
:root {
    --bg-primary: #0B0F19;
    --bg-secondary: #111827;
    --bg-card: rgba(17, 24, 39, 0.7);
    --bg-glass: rgba(255, 255, 255, 0.03);
    --border-glass: rgba(255, 255, 255, 0.08);
    --accent-primary: #6C63FF;
    --accent-secondary: #A78BFA;
    --accent-glow: rgba(108, 99, 255, 0.15);
    --accent-gradient: linear-gradient(135deg, #6C63FF 0%, #A78BFA 50%, #C084FC 100%);
    --success: #34D399;
    --success-glow: rgba(52, 211, 153, 0.15);
    --warning: #FBBF24;
    --error: #F87171;
    --text-primary: #F1F5F9;
    --text-secondary: #94A3B8;
    --text-muted: #64748B;
    --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
}

/* ── Global Reset ── */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-sans) !important;
}

/* ── Hide Streamlit Defaults ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] {
    background: transparent !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb {
    background: var(--accent-primary);
    border-radius: 3px;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F1629 0%, #111827 100%) !important;
    border-right: 1px solid var(--border-glass) !important;
}

[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    font-family: var(--font-sans) !important;
    font-weight: 700 !important;
}

/* ── Sidebar Buttons ── */
[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-family: var(--font-sans) !important;
    padding: 0.6rem 1.2rem !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    border: 1px solid var(--border-glass) !important;
}

[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: var(--accent-gradient) !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 4px 15px var(--accent-glow) !important;
}

[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(108, 99, 255, 0.3) !important;
}

[data-testid="stSidebar"] .stButton > button:not([kind="primary"]) {
    background: var(--bg-glass) !important;
    color: var(--text-secondary) !important;
}

[data-testid="stSidebar"] .stButton > button:not([kind="primary"]):hover {
    background: rgba(255, 255, 255, 0.08) !important;
    color: var(--text-primary) !important;
    border-color: var(--accent-primary) !important;
}

/* ── Download Button ── */
[data-testid="stSidebar"] .stDownloadButton > button {
    width: 100% !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-family: var(--font-sans) !important;
    background: var(--bg-glass) !important;
    color: var(--text-secondary) !important;
    border: 1px solid var(--border-glass) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

[data-testid="stSidebar"] .stDownloadButton > button:hover {
    background: rgba(255, 255, 255, 0.08) !important;
    color: var(--text-primary) !important;
    border-color: var(--accent-primary) !important;
}

/* ── File Uploader ── */
[data-testid="stFileUploader"] {
    border-radius: 16px !important;
}

[data-testid="stFileUploader"] > div {
    background: var(--bg-glass) !important;
    border: 2px dashed rgba(108, 99, 255, 0.3) !important;
    border-radius: 16px !important;
    transition: all 0.3s ease !important;
}

[data-testid="stFileUploader"] > div:hover {
    border-color: var(--accent-primary) !important;
    background: var(--accent-glow) !important;
}

/* ── Slider ── */
[data-testid="stSlider"] > div > div > div {
    background: var(--accent-gradient) !important;
}

/* ── Chat Messages ── */
[data-testid="stChatMessage"] {
    background: var(--bg-glass) !important;
    border: 1px solid var(--border-glass) !important;
    border-radius: 16px !important;
    padding: 1.2rem !important;
    margin-bottom: 1rem !important;
    backdrop-filter: blur(10px) !important;
    -webkit-backdrop-filter: blur(10px) !important;
    transition: all 0.3s ease !important;
}

[data-testid="stChatMessage"]:hover {
    border-color: rgba(108, 99, 255, 0.2) !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
}

/* ── Chat Input ── */
[data-testid="stChatInput"] {
    border-radius: 50px !important;
}

[data-testid="stChatInput"] > div {
    background: var(--bg-secondary) !important;
    border: 1px solid transparent !important;
    border-radius: 50px !important;
    background-image: linear-gradient(var(--bg-secondary), var(--bg-secondary)),
                      linear-gradient(135deg, #5CE1E6 0%, #6C63FF 50%, #A78BFA 100%) !important;
    background-origin: border-box !important;
    background-clip: padding-box, border-box !important;
    box-shadow: 0 4px 25px rgba(108, 99, 255, 0.12),
                0 0 40px rgba(92, 225, 230, 0.06) !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

[data-testid="stChatInput"] > div:focus-within {
    box-shadow: 0 4px 30px rgba(108, 99, 255, 0.25),
                0 0 60px rgba(92, 225, 230, 0.1),
                inset 0 0 20px rgba(108, 99, 255, 0.03) !important;
    transform: translateY(-1px) !important;
}

[data-testid="stChatInput"] textarea {
    border-radius: 50px !important;
}

[data-testid="stChatInput"] textarea {
    font-family: var(--font-sans) !important;
    color: var(--text-primary) !important;
}

/* ── Progress Bars ── */
[data-testid="stProgress"] > div > div > div {
    background: var(--accent-gradient) !important;
    border-radius: 8px !important;
}

/* ── Alerts ── */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: 1px solid var(--border-glass) !important;
    font-family: var(--font-sans) !important;
}

/* ── Divider ── */
hr {
    border-color: var(--border-glass) !important;
    margin: 1.5rem 0 !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: var(--bg-glass) !important;
    border: 1px solid var(--border-glass) !important;
    border-radius: 12px !important;
}

/* ── Metric Cards ── */
[data-testid="stMetric"] {
    background: var(--bg-glass) !important;
    border: 1px solid var(--border-glass) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}

/* ══ CUSTOM CLASSES ══ */

/* Hero Header */
.hero-container {
    text-align: center !important;
    padding: 2rem 1rem 1.5rem;
    margin-bottom: 1rem;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
}

.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(108, 99, 255, 0.15), rgba(167, 139, 250, 0.15));
    border: 1px solid rgba(108, 99, 255, 0.25);
    border-radius: 100px;
    padding: 0.35rem 1rem;
    font-size: 0.75rem;
    font-weight: 600;
    color: #A78BFA;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 1rem;
    font-family: var(--font-sans);
}

.hero-title {
    font-family: var(--font-sans) !important;
    font-size: 2.8rem !important;
    font-weight: 900 !important;
    background: linear-gradient(135deg, #F1F5F9 0%, #6C63FF 45%, #A78BFA 70%, #C084FC 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.15 !important;
    margin: 0 0 0.5rem 0 !important;
    padding: 0 !important;
}

.hero-subtitle {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.95rem;
    color: var(--text-secondary);
    font-weight: 400;
    line-height: 1.7;
    max-width: 650px;
    width: 100%;
    margin: 0 auto !important;
    text-align: center !important;
    letter-spacing: 0.01em;
    display: block !important;
}

/* Typewriter character animation */
.tw-char {
    opacity: 0;
    display: inline;
    animation: charAppear 0.05s forwards;
}

@keyframes charAppear {
    to { opacity: 1; }
}

.tw-cursor {
    display: inline-block;
    width: 2px;
    height: 1.1em;
    background: #5CE1E6;
    margin-left: 2px;
    vertical-align: text-bottom;
    animation: cursorBlink 0.8s step-end 5, cursorFade 0.3s ease 4.5s forwards;
}

@keyframes cursorBlink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
}

@keyframes cursorFade {
    to { opacity: 0; visibility: hidden; }
}

/* Status Pills */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border-radius: 100px;
    font-size: 0.8rem;
    font-weight: 600;
    font-family: var(--font-sans);
    letter-spacing: 0.02em;
}

.status-ready {
    background: linear-gradient(135deg, rgba(52, 211, 153, 0.1), rgba(52, 211, 153, 0.05));
    border: 1px solid rgba(52, 211, 153, 0.25);
    color: #34D399;
}

.status-offline {
    background: linear-gradient(135deg, rgba(251, 191, 36, 0.1), rgba(251, 191, 36, 0.05));
    border: 1px solid rgba(251, 191, 36, 0.25);
    color: #FBBF24;
}

/* Pulse Animation for Status Dot */
.pulse-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    display: inline-block;
    animation: pulse 2s infinite;
}

.pulse-dot.green {
    background: #34D399;
    box-shadow: 0 0 8px rgba(52, 211, 153, 0.6);
}

.pulse-dot.amber {
    background: #FBBF24;
    box-shadow: 0 0 8px rgba(251, 191, 36, 0.6);
}

@keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.3); opacity: 0.7; }
}

/* Metric Gauge Cards */
.metric-card {
    background: var(--bg-glass);
    border: 1px solid var(--border-glass);
    border-radius: 16px;
    padding: 1.2rem;
    text-align: center;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
}

.metric-card:hover {
    border-color: rgba(108, 99, 255, 0.3);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
    transform: translateY(-2px);
}

.metric-label {
    font-family: var(--font-sans);
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.5rem;
}

.metric-value {
    font-family: var(--font-mono);
    font-size: 2rem;
    font-weight: 700;
    margin: 0.3rem 0;
}

.metric-value.faith { color: #34D399; }
.metric-value.rel { color: #6C63FF; }

.metric-bar {
    width: 100%;
    height: 6px;
    background: rgba(255, 255, 255, 0.06);
    border-radius: 3px;
    overflow: hidden;
    margin-top: 0.8rem;
}

.metric-bar-fill {
    height: 100%;
    border-radius: 3px;
    transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
}

.metric-bar-fill.faith {
    background: linear-gradient(90deg, #059669, #34D399);
}

.metric-bar-fill.rel {
    background: var(--accent-gradient);
}

/* Sidebar Section Header */
.sidebar-section {
    font-family: var(--font-sans);
    font-size: 0.7rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin: 1.5rem 0 0.8rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid var(--border-glass);
}

/* Sidebar Logo */
.sidebar-logo {
    font-family: var(--font-sans);
    font-size: 1.5rem;
    font-weight: 800;
    background: var(--accent-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem;
}

.sidebar-version {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    color: var(--text-muted);
}

/* Source Badge */
.source-badge {
    display: inline-block;
    background: rgba(108, 99, 255, 0.1);
    border: 1px solid rgba(108, 99, 255, 0.2);
    border-radius: 8px;
    padding: 0.2rem 0.6rem;
    font-size: 0.7rem;
    font-weight: 500;
    color: var(--accent-secondary);
    font-family: var(--font-mono);
    margin: 0.2rem;
}

/* Footer */
.app-footer {
    text-align: center;
    padding: 2rem 1rem 1rem;
    border-top: 1px solid var(--border-glass);
    margin-top: 3rem;
}

.footer-text {
    font-family: var(--font-sans);
    font-size: 0.75rem;
    color: var(--text-muted);
}

.footer-link {
    color: var(--accent-secondary);
    text-decoration: none;
    font-weight: 500;
    transition: color 0.2s;
}

.footer-link:hover {
    color: var(--accent-primary);
}

/* Typing animation */
@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
}

.typing-cursor {
    display: inline-block;
    width: 2px;
    height: 1em;
    background: var(--accent-primary);
    margin-left: 2px;
    animation: blink 1s step-end infinite;
}

/* Empty state */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: var(--text-muted);
}

.empty-state-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    opacity: 0.5;
}

.empty-state-title {
    font-family: var(--font-sans);
    font-size: 1.2rem;
    font-weight: 600;
    color: var(--text-secondary);
    margin-bottom: 0.5rem;
}

.empty-state-desc {
    font-family: var(--font-sans);
    font-size: 0.9rem;
    color: var(--text-muted);
    max-width: 400px;
    margin: 0 auto;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "chunks" not in st.session_state:
    st.session_state.chunks = []
if "messages" not in st.session_state:
    st.session_state.messages = []

# ══════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════
with st.sidebar:
    # Logo
    st.markdown("""
    <div style="padding: 0.5rem 0 0.5rem;">
        <div class="sidebar-logo" style="display: flex; align-items: center; gap: 0.5rem;">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="28" height="28">
                <defs><linearGradient id="sg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#5CE1E6"/><stop offset="100%" stop-color="#8B9CF7"/></linearGradient></defs>
                <circle cx="256" cy="270" r="85" fill="none" stroke="url(#sg)" stroke-width="16"/>
                <circle cx="256" cy="270" r="16" fill="url(#sg)"/>
                <line x1="190" y1="205" x2="130" y2="130" stroke="url(#sg)" stroke-width="12" stroke-linecap="round"/>
                <circle cx="115" cy="115" r="45" fill="none" stroke="#5CE1E6" stroke-width="14"/>
                <circle cx="115" cy="115" r="12" fill="#7BB8F5"/>
                <line x1="320" y1="205" x2="385" y2="140" stroke="url(#sg)" stroke-width="12" stroke-linecap="round"/>
                <circle cx="395" cy="130" r="22" fill="none" stroke="url(#sg)" stroke-width="10"/>
                <circle cx="395" cy="130" r="7" fill="url(#sg)"/>
                <line x1="320" y1="335" x2="385" y2="390" stroke="url(#sg)" stroke-width="12" stroke-linecap="round"/>
                <circle cx="395" cy="400" r="22" fill="none" stroke="url(#sg)" stroke-width="10"/>
                <circle cx="395" cy="400" r="7" fill="url(#sg)"/>
                <line x1="190" y1="340" x2="120" y2="410" stroke="url(#sg)" stroke-width="12" stroke-linecap="round"/>
                <circle cx="110" cy="420" r="18" fill="none" stroke="#5CE1E6" stroke-width="10"/>
                <circle cx="110" cy="420" r="6" fill="#5CE1E6"/>
            </svg>
            <span>AtlasRAG</span>
        </div>
        <div class="sidebar-version">v2.0 · Enterprise Edition</div>
    </div>
    """, unsafe_allow_html=True)

    # Status Indicator
    if st.session_state.vector_store is not None:
        st.markdown("""
        <div class="status-pill status-ready">
            <span class="pulse-dot green"></span>
            Knowledge Base Active
        </div>
        """, unsafe_allow_html=True)
        chunk_count = len(st.session_state.chunks)
        st.markdown(f"""
        <div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--text-muted);
                    padding: 0.3rem 0 0 1rem;">
            {chunk_count} chunks indexed in memory
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="status-pill status-offline">
            <span class="pulse-dot amber"></span>
            No Knowledge Base
        </div>
        """, unsafe_allow_html=True)

    # ── Data Ingestion Section ──
    st.markdown('<div class="sidebar-section">📂 Data Ingestion</div>', unsafe_allow_html=True)

    chunk_size = st.slider(
        "Chunk Size (tokens)",
        min_value=500, max_value=2000, value=1000, step=100,
        help="Smaller chunks = more precise. Larger chunks = more context."
    )

    uploaded_files = st.file_uploader(
        "Drop your PDFs here",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    if uploaded_files:
        st.markdown(f"""
        <div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--accent-secondary);
                    padding: 0.3rem 0;">
            📎 {len(uploaded_files)} file{'s' if len(uploaded_files) > 1 else ''} selected
        </div>
        """, unsafe_allow_html=True)

    if st.button("🚀 Update Knowledge Base", type="primary", use_container_width=True):
        if not uploaded_files:
            st.warning("⚠️ Upload at least one PDF first.")
        else:
            status_text = st.empty()
            progress_bar = st.progress(0)

            temp_dir = None
            try:
                # 1. Save to temp
                temp_dir = tempfile.mkdtemp()
                status_text.text("📂 Preparing files...")
                for uploaded_file in uploaded_files:
                    path = os.path.join(temp_dir, uploaded_file.name)
                    with open(path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                progress_bar.progress(20)

                # 2. Load
                status_text.text("📄 Parsing documents...")
                docs = load_documents(temp_dir)
                progress_bar.progress(40)

                # 3. Chunk
                status_text.text(f"✂️ Chunking ({chunk_size} tokens)...")
                chunks = chunk_documents(docs, chunk_size=chunk_size)
                progress_bar.progress(60)

                # 4. Index
                status_text.text("🧠 Building vector index...")
                vector_store = index_documents(chunks)

                # 5. Save state
                st.session_state.vector_store = vector_store
                st.session_state.chunks = chunks

                progress_bar.progress(100)
                status_text.text("✅ Knowledge Base Ready!")
                st.success(f"Indexed {len(chunks)} chunks from {len(uploaded_files)} files.")
                time.sleep(1.5)
                st.rerun()

            except Exception as e:
                st.error(f"❌ Ingestion failed: {e}")
            finally:
                # Cleanup temp directory
                if temp_dir and os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir, ignore_errors=True)

    # ── Chat Controls ──
    st.markdown('<div class="sidebar-section">💬 Chat Controls</div>', unsafe_allow_html=True)

    if st.session_state.messages:
        chat_json = json.dumps(st.session_state.messages, indent=2, ensure_ascii=False)
        st.download_button(
            label="📥 Export Chat History",
            data=chat_json,
            file_name="atlasrag_chat.json",
            mime="application/json",
            use_container_width=True
        )

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    # ── Model Info ──
    st.markdown('<div class="sidebar-section">⚡ Model Info</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family: var(--font-sans); font-size: 0.8rem; color: var(--text-muted); line-height: 1.8;">
        <div><span style="color: var(--text-secondary);">Inference:</span> Gemini 2.5 Flash</div>
        <div><span style="color: var(--text-secondary);">Judge:</span> Gemini 2.5 Flash</div>
        <div><span style="color: var(--text-secondary);">Embeddings:</span> MiniLM-L6-v2</div>
        <div><span style="color: var(--text-secondary);">Search:</span> Vector + BM25</div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════════════════════

# Hero Header — build typewriter subtitle
_tw_text = "Self-correcting AI that audits every response for hallucinations and relevance — powered by Hybrid Search and LLM-as-a-Judge evaluation."
_tw_chars = ""
for _i, _c in enumerate(_tw_text):
    _delay = _i * 0.03
    _ch = "&nbsp;" if _c == " " else _c.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    _tw_chars += f'<span class="tw-char" style="animation-delay:{_delay:.2f}s">{_ch}</span>'
_tw_chars += '<span class="tw-cursor"></span>'

st.markdown(f"""
<div class="hero-container">
    <div class="hero-badge">✦ Enterprise Knowledge Intelligence</div>
    <h1 class="hero-title">AtlasRAG</h1>
    <p class="hero-subtitle">{_tw_chars}</p>
</div>
""", unsafe_allow_html=True)

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Show empty state if no messages and no knowledge base
if not st.session_state.messages and st.session_state.vector_store is None:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">📄</div>
        <div class="empty-state-title">Upload documents to get started</div>
        <div class="empty-state-desc">
            Drop your PDF files in the sidebar, click "Update Knowledge Base",
            then ask questions about your documents.
        </div>
    </div>
    """, unsafe_allow_html=True)
elif not st.session_state.messages and st.session_state.vector_store is not None:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">💬</div>
        <div class="empty-state-title">Knowledge Base is ready</div>
        <div class="empty-state-desc">
            Your documents have been indexed. Ask a question below to start
            a conversation with your data.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Initialize Retriever
retriever = None
if st.session_state.vector_store and st.session_state.chunks:
    try:
        retriever = HybridRetriever(st.session_state.vector_store, st.session_state.chunks)
        generator = LLMGenerator()
        evaluator = AtlasEvaluator()
    except Exception as e:
        st.error(f"⚠️ System initialization error: {e}")

# ══════════════════════════════════════════════════════
# CHAT LOGIC
# ══════════════════════════════════════════════════════
if prompt := st.chat_input("Ask a question about your documents..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if not retriever:
        with st.chat_message("assistant"):
            st.markdown("⚠️ **Knowledge Base not loaded.** Upload PDFs and click *Update Knowledge Base* in the sidebar to get started.")
            st.session_state.messages.append({
                "role": "assistant",
                "content": "⚠️ **Knowledge Base not loaded.** Upload PDFs and click *Update Knowledge Base* in the sidebar to get started."
            })
    else:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()

            with st.spinner(""):
                # Show thinking state
                message_placeholder.markdown("*Searching knowledge base...*")

                try:
                    # 1. Retrieve
                    context_docs = retriever.search(prompt)

                    if not context_docs:
                        response = "I couldn't find relevant information in the uploaded documents for this query. Try rephrasing or uploading more relevant documents."
                        faith_score, rel_score = 0.0, 0.0
                    else:
                        context_text = "\n".join([doc.page_content for doc in context_docs])

                        # 2. Generate
                        message_placeholder.markdown("*Generating response...*")
                        response = generator.generate(prompt, context_text)

                        # 3. Evaluate
                        message_placeholder.markdown("*Evaluating response quality...*")
                        faith_score, rel_score = evaluator.evaluate(prompt, response, context_text)

                    # 4. Display Response
                    message_placeholder.markdown(response)

                    # 5. Display Metric Cards
                    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

                    col1, col2, col3 = st.columns([1, 1, 1])

                    with col1:
                        faith_pct = int(faith_score * 100)
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">🛡️ Faithfulness</div>
                            <div class="metric-value faith">{faith_pct}%</div>
                            <div class="metric-bar">
                                <div class="metric-bar-fill faith" style="width: {faith_pct}%;"></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        rel_pct = int(rel_score * 100)
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">🎯 Relevance</div>
                            <div class="metric-value rel">{rel_pct}%</div>
                            <div class="metric-bar">
                                <div class="metric-bar-fill rel" style="width: {rel_pct}%;"></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    with col3:
                        src_count = len(context_docs) if context_docs else 0
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">📚 Sources Used</div>
                            <div class="metric-value" style="color: var(--accent-secondary);">{src_count}</div>
                            <div style="margin-top: 0.5rem;">
                                {"".join([f'<span class="source-badge">Chunk {i+1}</span>' for i in range(min(src_count, 5))])}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    # 6. Source Documents Expander
                    if context_docs:
                        with st.expander(f"📖 View Source Context ({len(context_docs)} chunks)", expanded=False):
                            for i, doc in enumerate(context_docs):
                                source = doc.metadata.get("source", "Unknown")
                                page = doc.metadata.get("page", "?")
                                st.markdown(f"**Chunk {i+1}** · `{os.path.basename(source)}` · Page {page}")
                                st.markdown(f"> {doc.page_content[:300]}{'...' if len(doc.page_content) > 300 else ''}")
                                if i < len(context_docs) - 1:
                                    st.divider()

                    st.session_state.messages.append({"role": "assistant", "content": response})

                except Exception as e:
                    st.error(f"❌ Generation error: {e}")

# ══════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════
st.markdown("""
<div class="app-footer">
    <div class="footer-text">
        Built with 🖤 by <a class="footer-link" href="https://github.com/R-Roy03" target="_blank">Rakesh Raushan</a>
        &nbsp;·&nbsp;
        <a class="footer-link" href="https://github.com/R-Roy03/AtlasRAG" target="_blank">GitHub</a>
        &nbsp;·&nbsp;
        Powered by Gemini 2.5 Flash &amp; Sentence-Transformers
    </div>
</div>
""", unsafe_allow_html=True)
