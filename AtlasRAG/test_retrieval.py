from retrieval.hybrid_search import HybridRetriever

def main():
    print("🚀 Initializing Hybrid Search Engine...")
    retriever = HybridRetriever()
    
    # 1. Test Query (Apne PDF se related koi sawal socho)
    # Example: Agar tumhara PDF "Generative AI" par hai:
    query = "Explain Generative AI" 
    
    print("\n❓ User Query:", query)
    results = retriever.search(query)

    print("\n✅ Found Relevant Contexts:")
    for i, doc in enumerate(results):
        print(f"\n--- Result {i+1} ---")
        print(f"📄 Content: {doc.page_content[:200]}...") # Sirf first 200 chars dikhayenge
        print(f"📂 Source: {doc.metadata.get('source', 'Unknown')}")

if __name__ == "__main__":
    main()