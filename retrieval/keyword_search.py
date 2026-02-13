import os
from rank_bm25 import BM25Okapi
from langchain_chroma import Chroma  # Updated import
from langchain_google_genai import GoogleGenerativeAIEmbeddings

class KeywordSearcher:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            print("❌ API Key missing")
            return

        # 1. Setup correct embedding model (Same as ingestion)
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001", 
            google_api_key=self.api_key
        )

        # 2. Load Documents from ChromaDB to build BM25 Index
        # extract all documents from DB and making BM25 index
        if os.path.exists("./chroma_db"):
            self.vector_store = Chroma(
                persist_directory="./chroma_db",
                embedding_function=self.embeddings
            )
            
            # Fetch all documents (Limit 100 for speed, can be increased)
            # Note: Production mein hum documents alag store karte hain, 
            # par abhi ke liye vector store se nikal rahe hain.
            try:
                # Dummy search to get docs (Workaround since Chroma doesn't have 'get_all')
                results = self.vector_store.similarity_search("dummy", k=50) 
                self.documents = [doc.page_content for doc in results]
                
                # 3. Create BM25 Index
                tokenized_corpus = [doc.split(" ") for doc in self.documents]
                self.bm25 = BM25Okapi(tokenized_corpus)
                print(f"✅ BM25 Index Built with {len(self.documents)} docs")
            except Exception as e:
                print(f"⚠️ BM25 Build Error: {e}")
                self.bm25 = None
        else:
            print("❌ ChromaDB not found for Keyword Search")
            self.bm25 = None

    def search(self, query, k=3):
        if not self.bm25:
            return []
        
        tokenized_query = query.split(" ")
        # Get top-k text results
        results = self.bm25.get_top_n(tokenized_query, self.documents, n=k)
        return results