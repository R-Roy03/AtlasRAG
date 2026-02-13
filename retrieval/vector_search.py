import os
import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

# FIX: Class ka naam wapas 'VectorSearcher' kar diya (for no error in future)
class VectorSearcher:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            st.error("❌ Google API Key not found! Check .env file.")
            return

        # 1. Embedding Model (Must match Ingestion!)
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001", 
            google_api_key=self.api_key
        )

        # 2. Connect to Database (compulsery to tell the address!)
        if os.path.exists("./chroma_db"):
            self.vector_store = Chroma(
                persist_directory="./chroma_db",  
                embedding_function=self.embeddings
            )
        else:
            st.error("❌ Error: 'chroma_db' folder nahi mila! Please run 'python run_ingestion.py' first.")
            self.vector_store = None

    def search(self, query, k=3):
        """
        Semantic Search using Vector Database
        """
        if not self.vector_store:
            return []
            
        try:
            # Similarity Search
            results = self.vector_store.similarity_search(query, k=k)
            return results
        except Exception as e:
            st.error(f"❌ Search Error: {e}")
            return []