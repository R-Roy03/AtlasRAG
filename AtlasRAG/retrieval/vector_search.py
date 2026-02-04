import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

class VectorSearcher:
    # UPDATE: Folder name changed to './chromadb'
    def __init__(self, persist_dir="./chromadb"):
        api_key = os.getenv("GOOGLE_API_KEY")
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=api_key)
        
        # Load existing DB
        self.vector_store = Chroma(
            persist_directory=persist_dir,
            embedding_function=self.embeddings
        )

    def search(self, query, k=5):
        print(f"🔍 Vector Searching for: '{query}'")
        docs = self.vector_store.similarity_search_with_score(query, k=k)
        return docs