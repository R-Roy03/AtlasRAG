import streamlit as st
import os
import tempfile
import json
import time

# Fix for SQLite (Still good to keep)
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

# Local Imports
# Ensure sys path includes current dir
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ingestion.loader import load_documents
from ingestion.chunker import chunk_documents
from ingestion.vector_store import index_documents
from retrieval.hybrid_search import HybridRetriever
from inference.generator import LLMGenerator
from evaluation.metrics import AtlasEvaluator

st.set_page_config(page_title="AtlasRAG Enterprise", page_icon="🤖", layout="wide")

# --- SESSION STATE SETUP ---
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "chunks" not in st.session_state:
    st.session_state.chunks = []
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Knowledge Base")
    
    if st.session_state.vector_store is not None:
        st.success("🟢 System Ready (In-Memory)")
    else:
        st.warning("🔴 No Data Found")

    uploaded_files = st.file_uploader("📂 Upload PDFs", type=["pdf"], accept_multiple_files=True)
    
    if st.button("🚀 Update Knowledge Base", type="primary"):
        if not uploaded_files:
            st.warning("⚠️ Please upload a file first!")
        else:
            try:
                # 1. Save to Temp
                temp_dir = tempfile.mkdtemp()
                for uploaded_file in uploaded_files:
                    path = os.path.join(temp_dir, uploaded_file.name)
                    with open(path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                
                # 2. Process
                with st.spinner("Processing..."):
                    docs = load_documents(temp_dir)
                    chunks = chunk_documents(docs)
                    
                    # 3. Create In-Memory DB
                    vector_store = index_documents(chunks)
                    
                    # 4. Save to Session State (Critical for RAM mode)
                    st.session_state.vector_store = vector_store
                    st.session_state.chunks = chunks
                    
                st.success("✅ Updated!")
                time.sleep(1)
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error: {e}")

# --- MAIN CHAT ---
st.title("🤖 AtlasRAG Interface")

# Display History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Initialize System from Session State
retriever = None
if st.session_state.vector_store and st.session_state.chunks:
    retriever = HybridRetriever(st.session_state.vector_store, st.session_state.chunks)
    generator = LLMGenerator()
    evaluator = AtlasEvaluator()

if prompt := st.chat_input("Ask about your documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if not retriever:
        st.error("⚠️ Please upload and process documents first!")
    else:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Search & Generate
                    docs = retriever.search(prompt)
                    context = "\n".join([d.page_content for d in docs])
                    response = generator.generate(prompt, context)
                    
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    # Metrics
                    f_score, r_score = evaluator.evaluate(prompt, response, context)
                    c1, c2 = st.columns(2)
                    c1.progress(f_score, f"Faithfulness: {int(f_score*100)}%")
                    c2.progress(r_score, f"Relevance: {int(r_score*100)}%")
                    
                except Exception as e:
                    st.error(f"Error: {e}")