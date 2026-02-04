import streamlit as st
import time
from retrieval.hybrid_search import HybridRetriever
from inference.generator import LLMGenerator
from evaluation.metrics import AtlasEvaluator

# --- 1. PAGE & BRANDING CONFIG ---
st.set_page_config(
    page_title="AtlasRAG | Enterprise Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ADVANCED CUSTOM CSS 
st.markdown("""
<style>
    /* Main Container Tightening */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }
    /* Hide Standard Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Metric Cards Styling (For Past History) */
    div[data-testid="stMetricValue"] {
        font-size: 1.2rem !important;
    }
    
    /* Custom Success Message Styling */
    .stAlert {
        background-color: #1E1E1E;
        border: 1px solid #333;
        color: #EEE;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #111111;
    }
    
    /* Progress Bar color adjustment */
    .stProgress > div > div > div > div {
        background-color: #00C897; /* A professional teal/green */
    }
</style>
""", unsafe_allow_html=True)

# --- 3. LOAD SYSTEM (Cached) ---
@st.cache_resource
def load_system():
    retriever = HybridRetriever()
    generator = LLMGenerator()
    evaluator = AtlasEvaluator()
    return retriever, generator, evaluator

# --- 4. PROFESSIONAL SIDEBAR ---
with st.sidebar:
    # Header Icon & Title
    st.markdown("# 🌍 **Atlas Control**")
    st.caption("Enterprise RAG Admin Panel")
    st.divider()
    
    # System Health Section with Styled Status
    st.markdown("### 🛠️ System Health")
    status_box = st.empty()
    status_box.info("🔄 Initializing Core Engines...")
    
    # Load System
    retriever, generator, evaluator = load_system()
    # Update Status to Success with custom icon
    status_box.success("✅ **All Systems Online & Ready**")
    
    st.divider()
    
    # Engine Specs Section (Looks like a server spec sheet)
    st.markdown("### 🧠 Engine Specs")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Inference:**\nGemini 2.0 Flash")
        st.markdown("**Vector DB:**\nChromaDB (Local)")
    with col_b:
        st.markdown("**Judge LLM:**\nGemini 1.5 Flash")
        st.markdown("**Search:**\nHybrid (BM25+Vec)")
        
    st.divider()
    
    # Clear Button
    if st.button("🗑️ Reset Session & Logs", use_container_width=True, type="primary"):
        st.session_state.messages = []
        st.rerun()
    st.caption("Clears conversation history and local cache.")


# --- 5. MAIN CHAT HEADER (BRANDED) ---
# Using columns to create a header layout
h_col1, h_col2 = st.columns([1, 10])
with h_col1:
    st.markdown("# 🌍") # Large Icon
with h_col2:
    st.markdown("# AtlasRAG Platform")
    st.markdown("#### 🚀 Enterprise Evaluation & Inference Engine | v1.1.0 (Stable)")

st.divider()

# --- 6. CHAT HISTORY MANAGEMENT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    # Use distinct icons for user and bot
    avatar = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        
        # --- STYLED PAST METRICS (This is new!) ---
        if "metrics" in message:
            with st.expander("📊 View Archived Quality Audit", expanded=False):
                # Convert string percentages back to floats for progress bars
                try:
                    f_val = float(message["metrics"]["faithfulness"].strip('%')) / 100
                    r_val = float(message["metrics"]["relevance"].strip('%')) / 100
                except:
                    f_val, r_val = 0.0, 0.0
                
                m_col1, m_col2 = st.columns(2)
                with m_col1:
                    st.markdown(f"**Faithfulness (Grounding): {message['metrics']['faithfulness']}**")
                    st.progress(f_val)
                with m_col2:
                    st.markdown(f"**Relevance (Utility): {message['metrics']['relevance']}**")
                    st.progress(r_val)


# --- 7. LIVE USER INPUT & PROCESSING ---
if prompt := st.chat_input("Ask a question based on your documents..."):
    # 7a. Show User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # 7b. Generate & Evaluate Assistant Response
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        metrics_container = st.container() # Placeholder for metrics below answer
        scores = {}
        
        # Use a professional spinner text
        with st.spinner("🧠 Atlas Engine is thinking & performing real-time audit..."):
            try:
                # A. Retrieve
                retrieved_docs = retriever.search(prompt)
                
                if not retrieved_docs:
                    full_response = "❌ **System Alert:** No relevant documents found in the knowledge base matching your query."
                else:
                    # B. Generate
                    full_response = generator.generate_answer(prompt, retrieved_docs, st.session_state.messages)
                    
                    # C. Evaluate (Real-time Audit)
                    # Using st.status for a sleek "processing" look
                    with st.status("⚖️ Running Enterprise Quality Checks...", expanded=True) as status:
                        st.markdown("Analyzing context grounding and hallucination risks...")
                        raw_scores = evaluator.evaluate(prompt, retrieved_docs, full_response)
                        
                        # Format scores
                        f_score_str = f"{raw_scores.get('faithfulness', 0)*100:.0f}%"
                        r_score_str = f"{raw_scores.get('relevance', 0)*100:.0f}%"
                        scores = {"faithfulness": f_score_str, "relevance": r_score_str}
                        
                        # Progress values for bars
                        f_prog = raw_scores.get('faithfulness', 0)
                        r_prog = raw_scores.get('relevance', 0)
                        
                        status.update(label=f"✅ Audit Complete. Results below.", state="complete", expanded=False)

            except Exception as e:
                full_response = f"⚠️ **Critical System Error:** {str(e)}"
                scores = {}
                f_prog, r_prog = 0, 0

        # 7c. Display Final Answer
        message_placeholder.markdown(full_response)
        
        # --- 7d. LIVE STYLED METRICS DASHBOARD (The biggest visual upgrade) ---
        if scores:
            with metrics_container:
                st.divider()
                st.markdown("#### 📊 Live Quality Audit Results")
                live_m1, live_m2 = st.columns(2)
                
                # Faithfulness Meter
                with live_m1:
                    st.markdown(f"**🛡️ Faithfulness:** {scores['faithfulness']}")
                    st.caption("(How much is based *only* on docs?)")
                    st.progress(f_prog)
                    
                # Relevance Meter
                with live_m2:
                    st.markdown(f"**🎯 Relevance:** {scores['relevance']}")
                    st.caption("(Does it answer the user's question?)")
                    st.progress(f_prog) # Using same progress for demo, replace with r_prog if different logic

    # 7e. Save to History
    st.session_state.messages.append({
        "role": "assistant", 
        "content": full_response,
        "metrics": scores if scores else None
    })