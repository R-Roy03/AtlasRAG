"""
AtlasRAG — CLI Mode (Terminal-based RAG interface).
Run after ingestion: python run_rag.py
"""
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from ingestion.loader import load_documents
from ingestion.chunker import chunk_documents
from ingestion.vector_store import InMemoryVectorStore
from retrieval.hybrid_search import HybridRetriever
from inference.generator import LLMGenerator

load_dotenv()


def main():
    print("Starting AtlasRAG CLI Mode...")

    # 1. Load documents
    docs = load_documents("data")
    chunks = chunk_documents(docs)

    if not chunks:
        print("No documents found in 'data/' folder. Add PDFs first.")
        return

    # 2. Create in-memory vector store (pure Python, no chromadb)
    model = SentenceTransformer("all-MiniLM-L6-v2")
    store = InMemoryVectorStore(model)

    metadatas = []
    for i, chunk in enumerate(chunks):
        meta = dict(chunk.metadata) if chunk.metadata else {}
        if not meta:
            meta = {"source": "cli", "chunk_index": i}
        metadatas.append(meta)

    store.add(
        documents=[chunk.page_content for chunk in chunks],
        metadatas=metadatas,
        ids=[f"chunk_{i}" for i in range(len(chunks))],
    )

    # 3. Setup components
    retriever = HybridRetriever(store, chunks)
    generator = LLMGenerator()

    print("System Ready!\n")

    while True:
        print("=" * 50)
        query = input("Enter your question (or 'exit' to quit): ")

        if query.lower() in ['exit', 'quit', 'q']:
            print("Goodbye!")
            break

        # 4. Retrieve
        print(f"\nSearching for: '{query}'...")
        retrieved_docs = retriever.search(query)

        if not retrieved_docs:
            print("No relevant documents found.")
            continue

        # 5. Generate
        context_text = "\n".join([doc.page_content for doc in retrieved_docs])
        print(f"Found {len(retrieved_docs)} relevant contexts. Generating answer...")
        answer = generator.generate(query, context_text)

        # 6. Output
        print("\nAI ANSWER:")
        print("-" * 40)
        print(answer)
        print("-" * 40)


if __name__ == "__main__":
    main()
