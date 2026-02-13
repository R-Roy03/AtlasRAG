import sys
import os
import shutil
import time

# --- 🟢 FIX FOR CHROMA DB ON CLOUD ---
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass
# -------------------------------------

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

# Setup Vector Store Path (Use Absolute Path)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PERSIST_DIRECTORY = os.path.join(BASE_DIR, "chroma_db")

def index_documents(chunks: list[Document]):
    if not chunks:
        return None

    import streamlit as st
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key and hasattr(st, "secrets"):
        api_key = st.secrets.get("GOOGLE_API_KEY")

    # 🛑 DELETE OLD DB (Force Cleanup)
    if os.path.exists(PERSIST_DIRECTORY):
        try:
            shutil.rmtree(PERSIST_DIRECTORY)
            time.sleep(1)
        except Exception as e:
            print(f"Cleanup Error: {e}")

    # Initialize Embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        google_api_key=api_key
    )

    # Create New Vector Store
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )
    return vector_store