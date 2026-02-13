import sys
import os
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


import streamlit as st
import time
import shutil
import json  # <-- New Import for saving history
from ingestion.loader import load_documents
from ingestion.chunker import chunk_documents
from ingestion.vector_store import index_documents
from retrieval.hybrid_search import HybridRetriever
from inference.generator import LLMGenerator
from evaluation.metrics import AtlasEvaluator

# Page Config
st.set_page_config(page_title="AtlasRAG Enterprise", page_icon="🤖", layout="wide")

# --- 1. SIDEBAR: CONTROL PANEL ---
with st.sidebar:
    st.title("⚙️ Knowledge Base")
    
    # Status Indicator
    if os.path.exists("./chroma_db"):
        st.success("🟢 System Ready")
    else:
        st.warning("🔴 No Data Found")

    chunk_size = st.slider(
        "📏 Chunk Size (Tokens)", 
        min_value=500, max_value=2000, value=1000, step=100
    )
    
    uploaded_files = st.file_uploader(
        "📂 Upload New PDFs", 
        type=["pdf"], 
        accept_multiple_files=True
    )
    
    if st.button("🚀 Update Knowledge Base", type="primary"):
        if not uploaded_files:
            st.warning("⚠️ Pehle koi file upload karein!")
        else:
            progress_bar = st.progress(0, text="Starting ingestion...")
            
            data_folder = "data"
            if not os.path.exists(data_folder):
                os.makedirs(data_folder)
            
            for uploaded_file in uploaded_files:
                file_path = os.path.join(data_folder, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
            
            progress_bar.progress(20, text="🧹 Cleaning old database...")
            
            if os.path.exists("chroma_db"):
                try:
                    shutil.rmtree("chroma_db")
                except:
                    pass
            
            try:
                progress_bar.progress(40, text="📄 Loading Documents...")
                docs = load_documents(data_folder)
                
                progress_bar.progress(60, text="✂️ Chunking Content...")
                chunks = chunk_documents(docs, chunk_size=chunk_size)
                
                progress_bar.progress(80, text="💾 Indexing Vector DB...")
                index_documents(chunks)
                
                progress_bar.progress(100, text="✅ Done!")
                time.sleep(0.5)
                progress_bar.empty()
                
                st.success("✅ PDF Uploaded Successfully!")
                st.info("💡 You can now ask questions from this PDF.")
                
                st.cache_resource.clear()
                time.sleep(2)
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error: {e}")

    # --- NEW FEATURE: CHAT HISTORY CONTROLS ---
    st.divider()
    st.subheader("💬 Chat Controls")
    
    # Download Button logic
    if "messages" in st.session_state and st.session_state.messages:
        # Chat ko text format mein convert karte hain
        chat_str = json.dumps(st.session_state.messages, indent=2)
        
        st.download_button(
            label="📥 Download Chat History",
            data=chat_str,
            file_name="atlas_chat_history.json",
            mime="application/json",
            help="Save your conversation to a file."
        )
    
    # Clear Button logic
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- 2. MAIN CHAT INTERFACE ---

st.title("🤖 AtlasRAG Interface")
st.caption(f"Enterprise System Active | Model: Gemini 2.5 Flash")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. LOAD SYSTEM (Cached) ---
@st.cache_resource
def load_system():
    if not os.path.exists("./chroma_db"):
        return None, None, None
    
    retriever = HybridRetriever()
    generator = LLMGenerator()
    evaluator = AtlasEvaluator()
    return retriever, generator, evaluator

retriever, generator, evaluator = load_system()

if not retriever:
    st.info("👈 Please upload a PDF in the sidebar to start!")
    st.stop()

# --- 4. CHAT LOGIC ---
if prompt := st.chat_input("Ask a question based on your documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        with st.spinner("🧠 Thinking..."):
            context_docs = retriever.search(prompt)
            context_text = "\n".join([doc.page_content for doc in context_docs])
            
            response = generator.generate(prompt, context_text)
            
            faith_score, rel_score = evaluator.evaluate(prompt, response, context_text)
            
            message_placeholder.markdown(response)
            
            col1, col2 = st.columns(2)
            with col1:
                st.progress(faith_score, text=f"🛡️ Faithfulness: {int(faith_score*100)}%")
            with col2:
                st.progress(rel_score, text=f"🎯 Relevance: {int(rel_score*100)}%")

    st.session_state.messages.append({"role": "assistant", "content": response})