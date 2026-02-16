import streamlit as st
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

def index_documents(chunks: list[Document]):
    """
    Creates an In-Memory Vector Store.
    """
    if not chunks:
        return None

    status = st.empty()
    status.text("🔄 Initializing In-Memory Embeddings...")
    
    try:
        # Use Local Embeddings
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        status.text(f"💾 Indexing {len(chunks)} chunks in RAM...")
        print(f"💾 Indexing {len(chunks)} chunks in RAM...")

        # 🟢 Create In-Memory Vector Store (No directory = RAM)
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings
        )
        
        status.text("✅ Success! Knowledge Base Ready in RAM.")
        print("✅ Success! Database created in RAM.")
        return vector_store
        
    except Exception as e:
        st.error(f"❌ RAM Indexing Failed: {str(e)}")
        raise e