import os
import time
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

def index_documents(chunks, persist_dir="./chroma_db"):
    print("💾 Creating Vector Store...")
    if not chunks: return None
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: API Key missing in .env")
        return None
    
    # UPDATE: Model change kiya hai 'embedding-001' -> 'text-embedding-004'
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=api_key)
    
    try:
        # Batch size limit handle karne ke liye (Enterprise Style)
        # Hum ChromaDB ko chunks de rahe hain, wo khud handle karega
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=persist_dir
        )
        print(f"   ✅ Stored {len(chunks)} chunks in ChromaDB at {persist_dir}")
        return vector_store
        
    except Exception as e:
        print(f"❌ Error in Vector Store: {e}")
        return None