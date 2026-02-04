from rank_bm25 import BM25Okapi
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

class KeywordSearcher:
    # UPDATE: Folder name changed to './chromadb'
    def __init__(self, persist_dir="./chromadb"):
        api_key = os.getenv("GOOGLE_API_KEY")
        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=api_key)
        
        # Sahi folder se data load karo
        vector_store = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
        
        print("⚙️ Building Keyword Index (BM25)...")
        data = vector_store.get() # Data fetch karo
        self.docs = data['documents'] 
        self.metadatas = data['metadatas']
        
        # Agar DB khali hai to error roko
        if not self.docs:
            print("❌ Error: ChromaDB khali hai! 'python run_ingestion.py' dubara chalao.")
            self.corpus_size = 0
            self.bm25 = None
            return

        # Tokenize
        tokenized_corpus = [doc.lower().split() for doc in self.docs]
        self.bm25 = BM25Okapi(tokenized_corpus)

    def search(self, query, k=5):
        if not self.bm25: return [] # Safety check
        
        print(f"🔍 Keyword Searching for: '{query}'")
        tokenized_query = query.lower().split()
        
        scores = self.bm25.get_scores(tokenized_query)
        top_n = self.bm25.get_top_n(tokenized_query, self.docs, n=k)
        
        results = []
        for doc_text in top_n:
            idx = self.docs.index(doc_text)
            results.append({
                "content": doc_text,
                "metadata": self.metadatas[idx],
                "score": scores[idx]
            })
        return results