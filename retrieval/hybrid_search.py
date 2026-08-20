import re

from rank_bm25 import BM25Okapi
from ingestion.loader import Document

# RRF damping constant. 60 is the value from the original Cormack et al.
# paper and the usual default; it keeps any single rank-1 hit from
# dominating the combined score.
RRF_K = 60

FUSION_MODES = ("rrf", "weighted", "interleave")


def tokenize(text: str) -> list[str]:
    """
    Lowercase and keep only runs of letters/digits.

    Plain text.split() left punctuation glued to words and was
    case-sensitive, so "XLOOKUP," never matched a query for "XLOOKUP"
    and "KUMAR" never matched "kumar". No stemming, no stopwords —
    normalisation only.
    """
    return re.findall(r"[a-z0-9]+", text.lower())


def min_max(scores: list[float]) -> list[float]:
    """
    Rescale scores onto [0, 1].

    Vector cosine similarities sit in a narrow band (roughly 0-0.7) while
    BM25 scores are unbounded and routinely reach 15+. Adding them raw
    would let BM25 drown out the vector signal entirely, so each list is
    rescaled against its own range before being combined.

    Trade-off worth knowing: this is per-query, so the best candidate
    always becomes 1.0 even when nothing matched well. RRF avoids that
    by ignoring scores and using ranks only.
    """
    if not scores:
        return []
    lo, hi = min(scores), max(scores)
    if hi == lo:
        return [1.0] * len(scores)
    return [(s - lo) / (hi - lo) for s in scores]


class HybridRetriever:
    def __init__(self, collection, chunks, fusion: str = "rrf"):
        """
        Initialize with a vector store (InMemoryVectorStore) and document chunks.
        Uses rank_bm25 directly for keyword search.

        fusion selects how the two result lists are combined:
          "rrf"        — reciprocal rank fusion (default)
          "weighted"   — min-max normalised score sum
          "interleave" — alternate vector/BM25 results (the original behaviour)
        """
        if fusion not in FUSION_MODES:
            raise ValueError(f"fusion must be one of {FUSION_MODES}, got {fusion!r}")

        self.collection = collection  # InMemoryVectorStore object
        self.chunks = chunks
        self.fusion = fusion

        # BM25 retriever (direct, no langchain dependency)
        self.corpus = [doc.page_content for doc in chunks]
        tokenized_corpus = [tokenize(text) for text in self.corpus]
        self.bm25 = BM25Okapi(tokenized_corpus)

    # ── Candidate generation ──────────────────────────────────────────
    # Each returns a list of (text, Document, score), best first.

    def _vector_candidates(self, query: str, n: int = 5):
        results = self.collection.query(query_texts=[query], n_results=n)
        if not results or not results["documents"]:
            return []

        texts = results["documents"][0]
        metas = results["metadatas"][0]
        scores = results.get("scores", [[]])[0]

        candidates = []
        for i, text in enumerate(texts):
            score = scores[i] if i < len(scores) else 0.0
            candidates.append((text, Document(text, metas[i] or {}), score))
        return candidates

    def _bm25_candidates(self, query: str, n: int = 5):
        scores = self.bm25.get_scores(tokenize(query))
        top_indices = sorted(
            range(len(scores)), key=lambda i: scores[i], reverse=True
        )[:n]
        return [
            (self.chunks[i].page_content, self.chunks[i], scores[i])
            for i in top_indices
            if scores[i] > 0
        ]

    # ── Fusion strategies ─────────────────────────────────────────────

    @staticmethod
    def _interleave(vector, bm25):
        """Alternate one vector result, one BM25 result, skipping duplicates.

        Note this ignores scores completely and always gives BM25's top hit
        position 2, even when BM25 found nothing relevant."""
        merged = []
        seen_content = set()

        max_len = max(len(vector), len(bm25)) if vector or bm25 else 0
        for i in range(max_len):
            for candidates in (vector, bm25):
                if i < len(candidates):
                    text, doc, _ = candidates[i]
                    if text not in seen_content:
                        merged.append(doc)
                        seen_content.add(text)
        return merged

    @staticmethod
    def _rrf(vector, bm25):
        """Reciprocal rank fusion: score = sum of 1 / (RRF_K + rank).

        Uses only positions, never raw scores, so the two incomparable
        score scales never have to be reconciled. A document found by
        both retrievers accumulates from both."""
        totals, docs = {}, {}
        for candidates in (vector, bm25):
            for rank, (text, doc, _) in enumerate(candidates, start=1):
                totals[text] = totals.get(text, 0.0) + 1.0 / (RRF_K + rank)
                docs.setdefault(text, doc)

        ranked = sorted(totals, key=totals.get, reverse=True)
        return [docs[text] for text in ranked]

    @staticmethod
    def _weighted(vector, bm25, alpha: float = 0.5):
        """Min-max normalise each score list, then add them.

        alpha weights the vector side; (1 - alpha) weights BM25."""
        totals, docs = {}, {}
        for candidates, weight in ((vector, alpha), (bm25, 1.0 - alpha)):
            normalised = min_max([score for _, _, score in candidates])
            for (text, doc, _), value in zip(candidates, normalised):
                totals[text] = totals.get(text, 0.0) + weight * value
                docs.setdefault(text, doc)

        ranked = sorted(totals, key=totals.get, reverse=True)
        return [docs[text] for text in ranked]

    # ── Public API ────────────────────────────────────────────────────

    def search(self, query: str, fusion: str = None):
        """
        Performs Hybrid Search (Vector + BM25) and returns the top results.
        Pass fusion to override the mode chosen at construction time.
        """
        mode = fusion or self.fusion
        vector = self._vector_candidates(query)
        bm25 = self._bm25_candidates(query)

        if mode == "rrf":
            merged = self._rrf(vector, bm25)
        elif mode == "weighted":
            merged = self._weighted(vector, bm25)
        elif mode == "interleave":
            merged = self._interleave(vector, bm25)
        else:
            raise ValueError(f"Unknown fusion mode: {mode!r}")

        return merged[:7]  # Return top 7 unique results
