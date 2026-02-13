import sys
import os

# --- 🟢 CRITICAL FIX: FORCE PYSQLITE3 ---
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass
# ----------------------------------------

# --- 🟢 PATH FIX: Allow importing from local folders ---
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import time
import json
import shutil

# Local Imports
from ingestion.loader import load_documents
from ingestion.chunker import chunk_documents
from ingestion.vector_store import index_documents
from retrieval.hybrid_search import HybridRetriever
from inference.generator import LLMGenerator
from evaluation.metrics import AtlasEvaluator

# Page Config
st.set_page_config(page_title="AtlasRAG Enterprise", page_icon="🤖", layout="wide")

# Setup Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(BASE_DIR, "chroma_db")

# --- 1. SIDEBAR: CONTROL PANEL ---
with st.sidebar:
    st.title("⚙️ Knowledge Base")
    
    # Status Indicator
    if os.path.exists(DB_PATH) and os.listdir(DB_PATH):
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
            st.warning("⚠️ Please upload a file first!")
        else:
            status_text = st.empty()
            progress_bar = st.progress(0)
            
            try:
                # Step 1: Save Files
                status_text.text("📂 Saving files...")
                if os.path.exists(DATA_FOLDER):
                    shutil.rmtree(DATA_FOLDER)
                os.makedirs(DATA_FOLDER)
                
                for uploaded_file in uploaded_files:
                    file_path = os.path.join(DATA_FOLDER, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                progress_bar.progress(20)

                # Step 2: Load
                status_text.text("📄 Loading Documents...")
                docs = load_documents(DATA_FOLDER)
                progress_bar.progress(40)

                # Step 3: Chunk
                status_text.text("✂️ Chunking Content...")
                chunks = chunk_documents(docs, chunk_size=chunk_size)
                progress_bar.progress(60)

                # Step 4: Index (Database Creation)
                status_text.text("💾 Creating Vector Database...")
                index_documents(chunks)
                progress_bar.progress(100)
                
                status_text.text("✅ Done!")
                st.success("Knowledge Base Updated Successfully!")
                time.sleep(2)
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                # Print to logs for debugging
                print(f"Error Traceback: {e}")

    # Chat History Controls
    st.divider()
    st.subheader("💬 Chat Controls")
    
    if "messages" in st.session_state and st.session_state.messages:
        chat_str = json.dumps(st.session_state.messages, indent=2)
        st.download_button(
            label="📥 Download Chat",
            data=chat_str,
            file_name="chat_history.json",
            mime="application/json"
        )
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# --- 2. MAIN CHAT INTERFACE ---
st.title("🤖 AtlasRAG Interface")
st.caption("Enterprise System Active | Model: Gemini 2.5 Flash")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. LOAD SYSTEM (Cached) ---
@st.cache_resource
def load_system():
    # Only load if DB exists
    if not os.path.exists(DB_PATH):
        return None, None, None
    
    try:
        retriever = HybridRetriever()
        generator = LLMGenerator()
        evaluator = AtlasEvaluator()
        return retriever, generator, evaluator
    except Exception as e:
        return None, None, None

retriever, generator, evaluator = load_system()

# --- 4. CHAT LOGIC ---
if prompt := st.chat_input("Ask a question based on your documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if not retriever:
        st.error("⚠️ Knowledge Base not found. Please upload PDFs first!")
    else:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            with st.spinner("🧠 Thinking..."):
                try:
                    # Retrieve
                    context_docs = retriever.search(prompt)
                    context_text = "\n".join([doc.page_content for doc in context_docs])
                    
                    # Generate
                    response = generator.generate(prompt, context_text)
                    
                    # Evaluate
                    faith_score, rel_score = evaluator.evaluate(prompt, response, context_text)
                    
                    # Display
                    message_placeholder.markdown(response)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.progress(faith_score, text=f"🛡️ Faithfulness: {int(faith_score*100)}%")
                    with col2:
                        st.progress(rel_score, text=f"🎯 Relevance: {int(rel_score*100)}%")
                        
                    st.session_state.messages.append({"role": "assistant", "content": response})
                
                except Exception as e:
                    st.error(f"❌ Error during generation: {e}")