import sys
import os
import shutil
import time
import streamlit as st

# --- 🟢 CRITICAL FIX FOR CHROMA DB ON CLOUD ---
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

    # 1. API Key Load
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key and hasattr(st, "secrets"):
        api_key = st.secrets.get("GOOGLE_API_KEY")
    
    if not api_key:
        st.error("❌ Google API Key not found!")
        return None

    # 2. Cleanup Old Database (Fresh Start)
    if os.path.exists(PERSIST_DIRECTORY):
        try:
            shutil.rmtree(PERSIST_DIRECTORY)
            time.sleep(1)
        except Exception as e:
            print(f"Cleanup Warning: {e}")

    # 3. 🟢 MULTI-MODEL STRATEGY (Jo chal jaye wo sahi)
    # List of models to try in order of preference
    # Note: 'task_type' hata diya hai taaki compatibility badh jaye
    models_to_try = [
        "models/text-embedding-004",  # New Standard
        "models/embedding-001",       # Old Reliable
        "text-embedding-004",         # No Prefix
        "embedding-001"               # No Prefix
    ]

    vector_store = None
    last_error = None

    status_text = st.empty()

    for model_name in models_to_try:
        try:
            print(f"🔄 Trying model: {model_name}...")
            status_text.text(f"🔄 Trying embedding model: {model_name}...")
            
            # Initialize Embeddings (Simple Config)
            embeddings = GoogleGenerativeAIEmbeddings(
                model=model_name,
                google_api_key=api_key
                # 🛑 REMOVED 'task_type' to prevent API version conflicts
            )

            # Create Vector Store
            vector_store = Chroma.from_documents(
                documents=chunks,
                embedding=embeddings,
                persist_directory=PERSIST_DIRECTORY
            )
            
            print(f"✅ Success with {model_name}!")
            status_text.text(f"✅ Success! Using {model_name}")
            return vector_store # Loop yahi khatam, humein winner mil gaya

        except Exception as e:
            print(f"❌ Failed {model_name}: {e}")
            last_error = e
            continue # Agla model try karo

    # Agar hum yahan pahunche, matlab sab fail ho gaye
    st.error("❌ All Embedding Models Failed.")
    st.error(f"Last Error: {str(last_error)}")
    st.info("💡 Tip: Check if 'Generative AI API' is enabled in your Google Cloud Console.")
    raise last_error