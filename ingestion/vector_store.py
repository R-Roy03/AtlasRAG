import sys
import os

# --- 🟢 FIX FOR CHROMA DB ON STREAMLIT CLOUD ---
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass 

# -----------------------------------------------

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
import shutil
from dotenv import load_dotenv

load_dotenv()

# Setup Vector Store Path
PERSIST_DIRECTORY = "./chroma_db"

def index_documents(chunks: list[Document]):
    if not chunks:
        return

    import streamlit as st
    # 🟢 FORCE API KEY LOAD
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key and "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]

    # 🟢 USE EXACT MODEL NAME (No prefix)
    embeddings = GoogleGenerativeAIEmbeddings(
        model="text-embedding-004", 
        google_api_key=api_key,
        task_type="retrieval_document"
    )

    # Create Chroma Vector Store
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )
    
    print("✅ Documents indexed successfully!")
    return vector_store