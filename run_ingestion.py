import os
import shutil
# Ab hum Classes nahi, Functions import kar rahe hain
from ingestion.loader import load_documents
from ingestion.chunker import chunk_documents
from ingestion.vector_store import index_documents

def main():
    print("🚀 Starting Ingestion Process...")

    # 1. Clean Slate: Purana DB uda do taaki fresh start ho
    if os.path.exists("chroma_db"):
        try:
            shutil.rmtree("chroma_db")
            print("🗑️  Old database removed for fresh start.")
        except Exception as e:
            print(f"⚠️ Could not delete old DB: {e}")

    # 2. Load Data
    data_folder = "data"
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
        print(f"⚠️ '{data_folder}' folder created. Please put PDFs inside!")
        return

    docs = load_documents(data_folder)

    if not docs:
        print("❌ No Documents found! Add PDFs to 'data' folder.")
        return

    # 3. Chunk Data
    # Aapke chunker.py mein function ka naam 'chunk_documents' hai
    chunks = chunk_documents(docs)

    # 4. Index & Store
    # Aapke vector_store.py mein function ka naam 'index_documents' hai
    index_documents(chunks)

    print("\n✅ Ingestion Complete! Now run 'streamlit run app.py'")

if __name__ == "__main__":
    main()
