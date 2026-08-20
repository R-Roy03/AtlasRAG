"""
AtlasRAG — Pure-Python In-Memory Vector Store.
No chromadb, no protobuf, no gRPC — zero dependency crashes.
Uses sentence-transformers + numpy for embeddings and cosine similarity.
"""
import streamlit as st
import numpy as np
from sentence_transformers import SentenceTransformer
from ingestion.loader import Document


class InMemoryVectorStore:
    """
    Lightweight vector store using numpy cosine similarity.
    Drop-in replacement for chromadb Collection — same query() interface.
    """

    def __init__(self, model):
        self.model = model
        self.documents = []
        self.metadatas = []
        self.ids = []
        self.embeddings = None

    def add(self, documents, metadatas, ids):
        """Add documents with their embeddings."""
        self.documents = list(documents)
        self.metadatas = list(metadatas)
        self.ids = list(ids)
        # Encode all documents and L2-normalize for cosine similarity
        raw = self.model.encode(documents, show_progress_bar=False)
        norms = np.linalg.norm(raw, axis=1, keepdims=True)
        norms[norms == 0] = 1  # avoid division by zero
        self.embeddings = raw / norms

    def query(self, query_texts, n_results=5):
        """
        Semantic search via cosine similarity.
        Returns dict with 'documents' and 'metadatas' keys
        (same format as chromadb Collection.query).
        """
        if self.embeddings is None or len(self.documents) == 0:
            return {"documents": [[]], "metadatas": [[]]}

        # Encode and normalize query
        q_raw = self.model.encode(query_texts, show_progress_bar=False)
        q_norm = np.linalg.norm(q_raw, axis=1, keepdims=True)
        q_norm[q_norm == 0] = 1
        q_emb = q_raw / q_norm

        # Cosine similarity = dot product of normalized vectors
        similarities = np.dot(self.embeddings, q_emb.T)

        all_docs = []
        all_metas = []

        for col in range(similarities.shape[1]):
            scores = similarities[:, col]
            top_k = min(n_results, len(scores))
            top_indices = np.argsort(scores)[::-1][:top_k]

            all_docs.append([self.documents[i] for i in top_indices])
            all_metas.append([self.metadatas[i] for i in top_indices])

        return {"documents": all_docs, "metadatas": all_metas}


def index_documents(chunks: list[Document], show_ui: bool = True):
    """
    Creates an In-Memory Vector Store using sentence-transformers + numpy.
    Returns an InMemoryVectorStore with the same query() interface as chromadb.

    show_ui=False skips all Streamlit writes so this can run headless
    (e.g. from the retrieval eval harness).
    """
    if not chunks:
        return None

    status = st.empty() if show_ui else None
    if status:
        status.text("Initializing In-Memory Embeddings...")

    try:
        model = SentenceTransformer("all-MiniLM-L6-v2")
        store = InMemoryVectorStore(model)

        if status:
            status.text("Building vector index...")

        # Ensure each chunk has non-empty metadata (defensive)
        metadatas = []
        for i, chunk in enumerate(chunks):
            meta = dict(chunk.metadata) if chunk.metadata else {}
            if not meta:
                meta = {"source": "uploaded", "chunk_index": i}
            metadatas.append(meta)

        if status:
            status.text(f"Indexing {len(chunks)} chunks in RAM...")
        print(f"Indexing {len(chunks)} chunks in RAM...")

        store.add(
            documents=[chunk.page_content for chunk in chunks],
            metadatas=metadatas,
            ids=[f"chunk_{i}" for i in range(len(chunks))],
        )

        if status:
            status.text(f"{len(chunks)} chunks indexed successfully!")
        print(f"Indexed {len(chunks)} chunks in RAM")

        return store

    except Exception as e:
        if status:
            status.error(f"RAM Indexing Failed: {e}")
        print(f"Vector Store Error: {e}")
        import traceback
        traceback.print_exc()
        return None
