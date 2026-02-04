import os
from langchain_community.document_loaders import PyPDFLoader
# UPDATE: 'langchain.schema' ki jagah 'langchain_core.documents' use hoga
from langchain_core.documents import Document 

def load_documents(folder_path: str) -> list[Document]:
    documents = []
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return []
    
    print(f"📂 Loading PDFs from: {folder_path}...")
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            try:
                loader = PyPDFLoader(os.path.join(folder_path, filename))
                documents.extend(loader.load())
                print(f"   ✅ Loaded: {filename}")
            except Exception as e:
                print(f"   ❌ Error: {filename} - {e}")
    return documents