import streamlit as st
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from ingestion.loader import Document


def index_documents(chunks: list[Document]):
    """
    Creates an In-Memory Vector Store using ChromaDB directly.
    """
    if not chunks:
        return None

    status = st.empty()
    status.text("🔄 Initializing In-Memory Embeddings...")

    try:
        ef = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

        client = chromadb.EphemeralClient()  # In-memory, no tenant issues

        # Remove old collection if it exists
        try:
            client.delete_collection("atlas_docs")
        except Exception:
            pass

        status.text("🧠 Building vector index...")
        collection = client.create_collection("atlas_docs", embedding_function=ef)

        status.text(f"💾 Indexing {len(chunks)} chunks in RAM...")
        print(f"Indexing {len(chunks)} chunks in RAM...")

        # ChromaDB 1.5+ rejects empty metadata dicts — ensure each has at least one key
        metadatas = []
        for i, chunk in enumerate(chunks):
            meta = dict(chunk.metadata) if chunk.metadata else {}
            if not meta:
                meta = {"source": "uploaded", "chunk_index": i}
            metadatas.append(meta)

        collection.add(
            documents=[chunk.page_content for chunk in chunks],
            metadatas=metadatas,
            ids=[f"chunk_{i}" for i in range(len(chunks))],
        )

        status.text(f"✅ {len(chunks)} chunks indexed successfully!")
        print(f"Indexed {len(chunks)} chunks in RAM")

        # Store client ref on collection so it doesn't get garbage collected
        collection._atlas_client = client
        return collection

    except Exception as e:
        status.error(f"❌ RAM Indexing Failed: {e}")
        print(f"Vector Store Error: {e}")
        import traceback
        traceback.print_exc()
        return None
