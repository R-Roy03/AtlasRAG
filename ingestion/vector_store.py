import sys
import os
import shutil
import time
import tempfile # <--- New Import
import streamlit as st

# --- Syntax Fix ---
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass
# ------------------

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

# --- 🟢 NUCLEAR FIX: Use System Temp Directory ---
# /tmp folder hamesha writable hota hai
TEMP_DIR = tempfile.gettempdir()
PERSIST_DIRECTORY = os.path.join(TEMP_DIR, "chroma_db_final")

def index_documents(chunks: list[Document]):
    if not chunks:
        return None

    # 1. Cleanup
    if os.path.exists(PERSIST_DIRECTORY):
        try:
            shutil.rmtree(PERSIST_DIRECTORY)
            time.sleep(1)
        except Exception as e:
            print(f"Cleanup Warning: {e}")

    # 2. Status UI
    status = st.empty()
    status.text("🔄 Initializing Local Embeddings (HuggingFace)...")
    
    # 3. Initialize Embeddings
    try:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    except Exception as e:
        st.error(f"❌ Failed to load local model: {e}")
        raise e

    print(f"💾 Indexing {len(chunks)} chunks into {PERSIST_DIRECTORY}...")
    status.text(f"💾 Creating Index in Temp Storage ({len(chunks)} chunks)...")

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