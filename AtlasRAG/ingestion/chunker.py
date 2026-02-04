# UPDATE: Import path fix kiya gaya hai
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_documents(documents, chunk_size=1000, chunk_overlap=200):
    print("✂️ Chunking documents...")
    if not documents:
        return []
        
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = splitter.split_documents(documents)
    print(f"   🧩 Created {len(chunks)} chunks.")
    return chunks