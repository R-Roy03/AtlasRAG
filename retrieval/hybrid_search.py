from retrieval.vector_search import VectorSearcher
from retrieval.keyword_search import KeywordSearcher

class HybridRetriever:
    # UPDATE: Folder name changed to './chromadb'
    def __init__(self, persist_dir="./chromadb"):
        self.vector_searcher = VectorSearcher(persist_dir)
        self.keyword_searcher = KeywordSearcher(persist_dir)

    def search(self, query):
        # 1. Get Results
        vector_results = self.vector_searcher.search(query, k=5)
        keyword_results = self.keyword_searcher.search(query, k=5)
        
        print(f"\n📊 Combining Results: {len(vector_results)} Vector + {len(keyword_results)} Keyword")
        
        # 2. Deduplication Logic
        final_docs = []
        seen_content = set()

        for doc, score in vector_results:
            if doc.page_content not in seen_content:
                final_docs.append(doc)
                seen_content.add(doc.page_content)

        for res in keyword_results:
            if res["content"] not in seen_content:
                from langchain_core.documents import Document
                doc = Document(page_content=res["content"], metadata=res["metadata"])
                final_docs.append(doc)
                seen_content.add(res["content"])
        
        return final_docs[:7]