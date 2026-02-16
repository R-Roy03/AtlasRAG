import sys
import os
import shutil
import time
import streamlit as st

# ---  CRITICAL FIX FOR CHROMA DB ON CLOUD ---
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass
# ----------------------------------------------

from langchain_chroma import Chroma
# 🟢 LOCAL EMBEDDINGS (No API Key needed for this part)
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

# Setup Vector Store Path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PERSIST_DIRECTORY = os.path.join(BASE_DIR, "chroma_db")

def index_documents(chunks: list[Document]):
    if not chunks:
        return None

    # 1. Cleanup Old Database (Fresh Start)
    if os.path.exists(PERSIST_DIRECTORY):
        try:
            shutil.rmtree(PERSIST_DIRECTORY)
            time.sleep(1)
        except Exception as e:
            print(f"Cleanup Warning: {e}")

    # 2. Status Update
    status = st.empty()
    status.text("🔄 Initializing Local Embeddings (HuggingFace)...")
    
    # 3. Initialize Local Embeddings
    # Model: all-MiniLM-L6-v2 (Industry Standard for RAG)
    try:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    except Exception as e:
        st.error(f"❌ Failed to load local model: {e}")
        raise e

    print(f"💾 Indexing {len(chunks)} chunks...")
    status.text(f"💾 Creating Index for {len(chunks)} chunks...")

    # 4. Create Vector Store
    try:
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=PERSIST_DIRECTORY
        )
        status.text("✅ Success! Knowledge Base Updated.")
        print("✅ Success! Database updated locally.")
        time.sleep(1)
        status.empty()
        return vector_store
        
    except Exception as e:
        st.error(f"❌ Database Creation Failed: {str(e)}")
        raise e