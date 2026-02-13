import sys
import os
import shutil
import time
import google.generativeai as genai  # <-- New Import

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

# Setup Vector Store Path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PERSIST_DIRECTORY = os.path.join(BASE_DIR, "chroma_db")

def index_documents(chunks: list[Document]):
    if not chunks:
        return None

    import streamlit as st
    
    # 1. Get API Key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key and hasattr(st, "secrets"):
        api_key = st.secrets.get("GOOGLE_API_KEY")
    
    if not api_key:
        st.error("❌ Google API Key not found!")
        return None

    # 2. Configure GenAI explicitly (Fixes 404 issues)
    genai.configure(api_key=api_key)

    # 3. Clean Old DB
    if os.path.exists(PERSIST_DIRECTORY):
        try:
            shutil.rmtree(PERSIST_DIRECTORY)
            time.sleep(1)
        except Exception as e:
            print(f"Cleanup Warning: {e}")

    # 4. Initialize Embeddings (NO PREFIX 'models/')
    # Ye library khud 'models/' jod leti hai, isliye hum sirf naam denge
    embeddings = GoogleGenerativeAIEmbeddings(
        model="text-embedding-004", 
        google_api_key=api_key,
        task_type="retrieval_document"
    )

    print(f"💾 Indexing {len(chunks)} chunks...")

    try:
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=PERSIST_DIRECTORY
        )
        print("✅ Success! Database updated.")
        return vector_store
        
    except Exception as e:
        # 🛑 Debugging Block: Agar fail hua to available models list karo
        print(f"❌ Error Detail: {e}")
        st.error(f"Embedding Failed. Error: {str(e)}")
        
        try:
            st.warning("🔍 Listing available models in logs...")
            for m in genai.list_models():
                if 'embedContent' in m.supported_generation_methods:
                    print(f"Available Model: {m.name}")
        except:
            pass
        raise e