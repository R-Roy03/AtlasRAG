from langchain_text_splitters import RecursiveCharacterTextSplitter

# UPDATE: Added 'chunk_size' argument taaki app.py se control kar sakein
def chunk_documents(documents, chunk_size=1000, chunk_overlap=200):
    print(f"✂️ Chunking documents with Size: {chunk_size} & Overlap: {chunk_overlap}...")
    if not documents:
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = splitter.split_documents(documents)
    print(f"   🧩 Created {len(chunks)} chunks.")
    return chunks