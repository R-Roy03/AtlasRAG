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

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Setup Vector Store Path
PERSIST_DIRECTORY = "./chroma_db"

def index_documents(chunks: list[Document]):
    """
    Creates a vector store from document chunks.
    """
    if not chunks:
        return

    # Initialize Embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

    # Create Chroma Vector Store
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )
    
    print("✅ Documents indexed successfully!")
    return vector_store