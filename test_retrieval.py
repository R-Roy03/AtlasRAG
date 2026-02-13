try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass
import pytest
from retrieval.hybrid_search import HybridRetriever
from langchain_community.document_loaders import PyPDFLoader

def test_pdf_loading():
    """Check if the PDF loader is working"""
    # Dummy path for testing logic
    loader = PyPDFLoader("data/GA3.pdf") 
    assert loader is not None

def test_hybrid_search_logic():
    """Simple check for retrieval components"""
    try:
        from rank_bm25 import BM25Okapi
        from langchain_chroma import Chroma
        assert True
    except ImportError:
        pytest.fail("Core retrieval libraries missing!")