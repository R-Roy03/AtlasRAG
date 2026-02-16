from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document

class HybridRetriever:
    def __init__(self, vector_store, chunks):
        """
        Initialize with the In-Memory Vector Store and Chunks.
        """
        self.vector_store = vector_store
        self.chunks = chunks
        
        # Initialize Retrievers
        self.vector_retriever = vector_store.as_retriever(search_kwargs={"k": 5})
        self.bm25_retriever = BM25Retriever.from_documents(chunks)
        self.bm25_retriever.k = 5

    def search(self, query: str):
        """
        Performs Hybrid Search (Vector + BM25) and deduplicates results.
        """
        # 1. Get results from both
        vector_docs = self.vector_retriever.invoke(query)
        bm25_docs = self.bm25_retriever.invoke(query)

        # 2. Combine and Deduplicate
        all_docs = []
        seen_content = set()
        
        # Interleave results (Vector, Keyword, Vector, Keyword...)
        max_len = max(len(vector_docs), len(bm25_docs))
        for i in range(max_len):
            if i < len(vector_docs):
                doc = vector_docs[i]
                if doc.page_content not in seen_content:
                    all_docs.append(doc)
                    seen_content.add(doc.page_content)
            
            if i < len(bm25_docs):
                doc = bm25_docs[i]
                if doc.page_content not in seen_content:
                    all_docs.append(doc)
                    seen_content.add(doc.page_content)
        
        return all_docs[:7] # Return top 7 unique results