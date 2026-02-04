import os
import sys

# Current folder ko path mein add karo
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ingestion.loader import load_documents
from ingestion.chunker import chunk_documents
from ingestion.vector_store import index_documents

def main():
    print("🚀 Starting Ingestion Pipeline...")

    # Paths set karo
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_FOLDER = os.path.join(BASE_DIR, "data")
    DB_PATH = os.path.join(BASE_DIR, "chromadb")

    # 1. Load
    docs = load_documents(DATA_FOLDER)
    if not docs:
        print("❌ Error: 'data' folder khali hai! PDF daalo.")
        return

    # 2. Chunk
    chunks = chunk_documents(docs)
    
    # 3. Embed & Store
    index_documents(chunks, persist_dir=DB_PATH)
    
    print("\n✅ Phase 1 Complete! Knowledge Base Ready.")

if __name__ == "__main__":
    main()