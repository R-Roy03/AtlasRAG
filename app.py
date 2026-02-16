import sys
import os
import streamlit as st
import time
import json
import tempfile
import shutil

# --- 🟢 FIX 1: FORCE PYSQLITE3 ---
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass
# ---------------------------------

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Local Imports
from ingestion.loader import load_documents
from ingestion.chunker import chunk_documents
from ingestion.vector_store import index_documents
from retrieval.hybrid_search import HybridRetriever
from inference.generator import LLMGenerator
from evaluation.metrics import AtlasEvaluator

# Page Config
st.set_page_config(page_title="AtlasRAG Enterprise", page_icon="🤖", layout="wide")

# --- SESSION STATE SETUP ---
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "chunks" not in st.session_state:
    st.session_state.chunks = []
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 1. SIDEBAR: CONTROL PANEL ---
with st.sidebar:
    st.title("⚙️ Knowledge Base")
    
    # Status Indicator
    if st.session_state.vector_store is not None:
        st.success("🟢 System Ready (RAM)")
    else:
        st.warning("🔴 No Data Found")

    # Feature 1: Chunk Size Slider
    chunk_size = st.slider(
        "📏 Chunk Size (Tokens)", 
        min_value=500, max_value=2000, value=1000, step=100
    )
    
    # Upload Section
    uploaded_files = st.file_uploader(
        "📂 Upload PDFs", 
        type=["pdf"], 
        accept_multiple_files=True
    )
    
    # Update Button
    if st.button("🚀 Update Knowledge Base", type="primary"):
        if not uploaded_files:
            st.warning("⚠️ Please upload a file first!")
        else:
            status_text = st.empty()
            progress_bar = st.progress(0)
            
            try:
                # 1. Create Temp Directory
                temp_dir = tempfile.mkdtemp()
                status_text.text("📂 Saving files to Temp...")
                
                # 2. Save Files
                for uploaded_file in uploaded_files:
                    path = os.path.join(temp_dir, uploaded_file.name)
                    with open(path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                progress_bar.progress(20)
                
                # 3. Load Documents
                status_text.text("📄 Parsing Documents...")
                docs = load_documents(temp_dir)
                progress_bar.progress(40)
                
                # 4. Chunk Documents (Using Slider Value)
                status_text.text(f"✂️ Chunking with size {chunk_size}...")
                # Note: Ensure your chunk_documents function accepts chunk_size
                chunks = chunk_documents(docs, chunk_size=chunk_size) 
                progress_bar.progress(60)
                
                # 5. Index (In-Memory)
                status_text.text("💾 Indexing in RAM...")
                vector_store = index_documents(chunks)
                
                # 6. Save to Session State
                st.session_state.vector_store = vector_store
                st.session_state.chunks = chunks
                
                progress_bar.progress(100)
                status_text.text("✅ Done!")
                st.success("Knowledge Base Updated!")
                time.sleep(1)
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error: {e}")
                print(f"Error: {e}")

    # Feature 2 & 3: Chat Controls
    st.divider()
    st.subheader("💬 Chat Controls")
    
    # Download Chat
    if st.session_state.messages:
        chat_str = json.dumps(st.session_state.messages, indent=2)
        st.download_button(
            label="📥 Download Chat",
            data=chat_str,
            file_name="chat_history.json",
            mime="application/json"
        )
    
    # Clear Chat
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# --- 2. MAIN CHAT INTERFACE ---
st.title("🤖 AtlasRAG Interface")
st.caption("Enterprise System Active | Model: Gemini 2.5 Flash")

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Initialize System Logic
retriever = None
if st.session_state.vector_store and st.session_state.chunks:
    try:
        retriever = HybridRetriever(st.session_state.vector_store, st.session_state.chunks)
        generator = LLMGenerator()
        evaluator = AtlasEvaluator()
    except Exception as e:
        st.error(f"System Load Error: {e}")

# --- 3. CHAT LOGIC ---
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
                    
                    if not context_docs:
                        response = "I couldn't find relevant information in the uploaded documents."
                        faith_score, rel_score = 0.0, 0.0
                    else:
                        context_text = "\n".join([doc.page_content for doc in context_docs])
                        
                        # Generate
                        response = generator.generate(prompt, context_text)
                        
                        # Evaluate
                        faith_score, rel_score = evaluator.evaluate(prompt, response, context_text)
                    
                    # Display Response
                    message_placeholder.markdown(response)
                    
                    # Display Metrics
                    col1, col2 = st.columns(2)
                    with col1:
                        st.progress(faith_score, text=f"🛡️ Faithfulness: {int(faith_score*100)}%")
                    with col2:
                        st.progress(rel_score, text=f"🎯 Relevance: {int(rel_score*100)}%")
                        
                    st.session_state.messages.append({"role": "assistant", "content": response})
                
                except Exception as e:
                    st.error(f"❌ Error during generation: {e}")