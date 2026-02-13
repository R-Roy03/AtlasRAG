import sys
import os
import shutil
import time

# --- 🟢 CRITICAL FIX: FORCE PYSQLITE3 FOR CHROMA DB ---
# Ye code sabse upar hona chahiye taaki purana SQLite load na ho
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass
# ------------------------------------------------------

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# --- 🟢 PATH SETUP: Use Absolute Paths to avoid Permission Errors ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PERSIST_DIRECTORY = os.path.join(BASE_DIR, "chroma_db")

def index_documents(chunks: list[Document]):
    """
    Creates a vector store from document chunks.
    """
    if not chunks:
        print("⚠️ No chunks to index.")
        return None

    # 1. API Key Load (Environment or Streamlit Secrets)
    import streamlit as st
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key and hasattr(st, "secrets"):
        api_key = st.secrets.get("GOOGLE_API_KEY")
    
    if not api_key:
        raise ValueError("❌ GOOGLE_API_KEY not found! Check .env or Streamlit Secrets.")

    # 2. Cleanup Old Database (Safe Delete)
    if os.path.exists(PERSIST_DIRECTORY):
        try:
            shutil.rmtree(PERSIST_DIRECTORY)
            print("🧹 Old database removed successfully.")
            time.sleep(1) # Thoda wait karo taaki system file release kar de
        except Exception as e:
            print(f"⚠️ Warning: Could not delete old DB: {e}")

    # 3. Initialize Embeddings (Stable Model)