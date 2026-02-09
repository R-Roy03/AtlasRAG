from retrieval.vector_search import VectorSearcher
from retrieval.keyword_search import KeywordSearcher

class HybridRetriever:
    def __init__(self):
        # FIX: We are not passing arguments
        # Kyunki VectorSearcher aur KeywordSearcher apne aap path handle kar rahe hain
        self.vector_searcher = VectorSearcher()
        self.keyword_searcher = KeywordSearcher()
    
    def search(self, query, k=3):
        """
        1. Get Vector Results (Semantic)
        2. Get Keyword Results (Exact Match)
        3. Combine & Remove Duplicates (Reranking logic simplified)
        """
        print(f"🔍 Hybrid Searching for: '{query}'")
        
        # 1. Vector Search
        vector_docs = self.vector_searcher.search(query, k=k)
        
        # 2. Keyword Search
        keyword_docs = self.keyword_searcher.search(query, k=k)
        
        # 3. Combine Results (Simple Set Logic to remove duplicates)
        # Note: Production mein hum Reranker Model use karte hain
        combined_results = []
        seen_content = set()

        # Add Vector Results First (High Priority)
        for doc in vector_docs:
            if doc.page_content not in seen_content:
                combined_results.append(doc)
                seen_content.add(doc.page_content)

        # Add Keyword Results if unique
        for doc_content in keyword_docs:
            if doc_content not in seen_content:
                # Wrap text in a dummy object to match format
                class DummyDoc:
                    def __init__(self, content):
                        self.page_content = content
                        self.metadata = {"source": "keyword_search"}
                
                combined_results.append(DummyDoc(doc_content))
                seen_content.add(doc_content)
        
        print(f"📊 Combining Results: {len(vector_docs)} Vector + {len(keyword_docs)} Keyword")
        return combined_results