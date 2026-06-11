from rank_bm25 import BM25Okapi
from ingestion.loader import Document


class HybridRetriever:
    def __init__(self, collection, chunks):
        """
        Initialize with a ChromaDB Collection and document chunks.
        Uses rank_bm25 directly for keyword search.
        """
        self.collection = collection  # chromadb Collection object
        self.chunks = chunks

        # BM25 retriever (direct, no langchain dependency)
        self.corpus = [doc.page_content for doc in chunks]
        tokenized_corpus = [text.split() for text in self.corpus]
        self.bm25 = BM25Okapi(tokenized_corpus)

    def search(self, query: str):
        """
        Performs Hybrid Search (Vector + BM25) and deduplicates results.
        """
        # 1. Vector search via ChromaDB
        results = self.collection.query(query_texts=[query], n_results=5)
        vector_docs = []
        if results and results["documents"]:
            for doc_text, metadata in zip(
                results["documents"][0], results["metadatas"][0]
            ):
                vector_docs.append(
                    Document(page_content=doc_text, metadata=metadata or {})
                )

        # 2. BM25 search
        tokenized_query = query.split()
        bm25_scores = self.bm25.get_scores(tokenized_query)
        top_indices = sorted(
            range(len(bm25_scores)), key=lambda i: bm25_scores[i], reverse=True
        )[:5]
        bm25_docs = [self.chunks[i] for i in top_indices if bm25_scores[i] > 0]

        # 3. Combine and Deduplicate (interleaved)
        all_docs = []
        seen_content = set()

        max_len = max(len(vector_docs), len(bm25_docs)) if vector_docs or bm25_docs else 0
        for i in range(max_len):
            if i < len(vector_docs):
                doc = vector_docs[i]
                if doc.page_content not in seen_content:
                    all_docs.append(doc)
                    seen_content.add(doc.page_content)

            if i < len(bm25_docs):
                doc = bm25_docs[i]
                if doc.page_content not in seen_content:
                    all_docs.append(doc)
                    seen_content.add(doc.page_content)

        return all_docs[:7]  # Return top 7 unique results
