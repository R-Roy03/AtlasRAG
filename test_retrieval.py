"""
AtlasRAG — CI-friendly test suite.
Tests core library imports and module structure without requiring API keys or local files.
"""


def test_core_retrieval_imports():
    """Verify all core retrieval libraries are installed and importable."""
    from rank_bm25 import BM25Okapi
    import numpy as np
    from ingestion.loader import Document
    assert BM25Okapi is not None
    assert np is not None
    assert Document is not None


def test_ingestion_modules():
    """Verify ingestion package structure is correct."""
    from ingestion.loader import load_documents
    from ingestion.chunker import chunk_documents
    assert callable(load_documents)
    assert callable(chunk_documents)


def test_vector_store_module():
    """Verify vector_store module is importable."""
    from ingestion.vector_store import index_documents, InMemoryVectorStore
    assert callable(index_documents)
    assert InMemoryVectorStore is not None


def test_inference_module():
    """Verify inference module is importable."""
    from inference.generator import LLMGenerator
    assert LLMGenerator is not None


def test_evaluation_module():
    """Verify evaluation module is importable."""
    from evaluation.metrics import AtlasEvaluator
    assert AtlasEvaluator is not None


def test_hybrid_search_class():
    """Verify HybridRetriever class exists and has search method."""
    from retrieval.hybrid_search import HybridRetriever
    assert hasattr(HybridRetriever, 'search')


def test_chunker_empty_input():
    """Chunker should return empty list for empty input."""
    from ingestion.chunker import chunk_documents
    result = chunk_documents([])
    assert result == []


def test_bm25_basic():
    """BM25 index creation and scoring works correctly."""
    from rank_bm25 import BM25Okapi
    corpus = [
        "the quick brown fox jumps over the fence".split(),
        "the lazy dog sleeps in the sun all day".split(),
        "a cat sat on the mat near the door".split(),
        "birds fly high in the blue sky above".split(),
    ]
    bm25 = BM25Okapi(corpus)
    scores = bm25.get_scores("quick brown fox".split())
    assert len(scores) == len(corpus)
    # First doc contains all query terms, should score highest
    assert scores[0] == max(scores)


def test_document_class():
    """Verify our custom Document class works correctly."""
    from ingestion.loader import Document
    doc = Document(page_content="Hello world", metadata={"source": "test.pdf"})
    assert doc.page_content == "Hello world"
    assert doc.metadata["source"] == "test.pdf"


def test_in_memory_vector_store():
    """Verify InMemoryVectorStore can index and query documents."""
    from sentence_transformers import SentenceTransformer
    from ingestion.vector_store import InMemoryVectorStore

    model = SentenceTransformer("all-MiniLM-L6-v2")
    store = InMemoryVectorStore(model)

    store.add(
        documents=["Python is a programming language", "The sun is a star"],
        metadatas=[{"source": "a"}, {"source": "b"}],
        ids=["0", "1"],
    )

    results = store.query(query_texts=["What is Python?"], n_results=1)
    assert len(results["documents"]) == 1
    assert len(results["documents"][0]) == 1
    assert "Python" in results["documents"][0][0]
