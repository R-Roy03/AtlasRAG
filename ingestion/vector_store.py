import sys
import os
import shutil
import time
import streamlit as st

# --- 🟢 FIX 1: Syntax Error Fixed (Alag lines) ---
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass
# -----------------------------------------------

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

# --- 🟢 FIX 2: New Folder Name (Bypasses Read-Only Error) ---
# Purana 'chroma_db' use nahi karenge, naya banayenge
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PERSIST_DIRECTORY = os.path.join(BASE_DIR, "chroma_storage_v2")

def index_documents(chunks: list[Document]):
    if not chunks:
        return None

    # 1. Cleanup: Naye folder ko bhi fresh start denge
    if os.path.exists(PERSIST_DIRECTORY):
        try:
            shutil.rmtree(PERSIST_DIRECTORY)
            time.sleep(1)
        except Exception as e:
            print(f"Cleanup Warning: {e}")

    # 2. Status UI
    status = st.empty()
    status.text("🔄 Initializing Local Embeddings (HuggingFace)...")
    
    # 3. Initialize Embeddings (Local & Free)
    try:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    except Exception as e:
        st.error(f"❌ Failed to load local model: {e}")
        raise e

    print(f"💾 Indexing {len(chunks)} chunks into {PERSIST_DIRECTORY}...")
    status.text(f"💾 Creating New Index for {len(chunks)} chunks...")

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