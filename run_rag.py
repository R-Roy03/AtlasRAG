from retrieval.hybrid_search import HybridRetriever
from inference.generator import LLMGenerator

def main():
    # 1. Setup
    print("🚀 Starting Enterprise RAG System...")
    retriever = HybridRetriever()
    generator = LLMGenerator()
    
    while True:
        print("\n" + "="*50)
        query = input("❓ Enter your question (or 'exit' to quit): ")
        
        if query.lower() in ['exit', 'quit', 'q']:
            print("👋 Goodbye!")
            break
            
        # 2. Retrieve (Dhoondo)
        print(f"\n🔍 Searching knowledge base for: '{query}'...")
        retrieved_docs = retriever.search(query)
        
        if not retrieved_docs:
            print("❌ No relevant documents found.")
            continue
            
        # 3. Generate (Socho aur Likho)
        print(f"📄 Found {len(retrieved_docs)} relevant contexts. Sending to LLM...")
        answer = generator.generate_answer(query, retrieved_docs)
        
        # 4. Output
        print("\n🤖 AI ANSWER:")
        print("-" * 20)
        print(answer)
        print("-" * 20)

if __name__ == "__main__":
    main()