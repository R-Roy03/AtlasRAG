import sys
import os

# --- 🟢 FIX FOR SQLITE ---
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass
# -----------------------

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import time
import json
import shutil
from ingestion.loader import load_documents
from ingestion.chunker import chunk_documents
from ingestion.vector_store import index_documents
from retrieval.hybrid_search import HybridRetriever
from inference.generator import LLMGenerator
from evaluation.metrics import AtlasEvaluator

st.set_page_config(page_title="AtlasRAG Enterprise", page_icon="🤖", layout="wide")

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(BASE_DIR, "chroma_db")

with st.sidebar:
    st.title("⚙️ Knowledge Base")
    
    # Status Check
    if os.path.exists(DB_PATH) and os.listdir(DB_PATH):
        st.success("🟢 System Ready")
    else:
        st.warning("🔴 No Data Found")

    chunk_size = st.slider("📏 Chunk Size", 500, 2000, 1000)
    uploaded_files = st.file_uploader("📂 Upload PDFs", type=["pdf"], accept_multiple_files=True)
    
    if st.button("🚀 Update Knowledge Base", type="primary"):
        if not uploaded_files:
            st.error("Please upload a file!")
        else:
            progress = st.progress(0, text="Starting...")
            try:
                # 1. Clean Data Folder
                if os.path.exists(DATA_FOLDER):
                    shutil.rmtree(DATA_FOLDER)
                os.makedirs(DATA_FOLDER)
                
                # 2. Save Files
                for uploaded_file in uploaded_files:
                    with open(os.path.join(DATA_FOLDER, uploaded_file.name), "wb") as f:
                        f.write(uploaded_file.getbuffer())
                
                progress.progress(40, text="Processing...")
                
                # 3. Pipeline
                docs = load_documents(DATA_FOLDER)
                chunks = chunk_documents(docs, chunk_size=chunk_size)
                index_documents(chunks)
                
                progress.progress(100, text="Done!")
                st.success("Updated! Reloading...")
                time.sleep(2)
                st.rerun()
                
            except Exception as e:
                st.error(f"Error: {e}")

# Chat UI
st.title("🤖 AtlasRAG Interface")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Load System
@st.cache_resource
def load_system():
    if not os.path.exists(DB_PATH): return None, None, None
    try:
        return HybridRetriever(), LLMGenerator(), AtlasEvaluator()
    except: return None, None, None

retriever, generator, evaluator = load_system()

if prompt := st.chat_input("Ask about your PDF..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    if retriever:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                docs = retriever.search(prompt)
                ctx = "\n".join([d.page_content for d in docs])
                res = generator.generate(prompt, ctx)
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
    else:
        st.error("Please upload a document first!")