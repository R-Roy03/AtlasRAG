"""
AtlasRAG — Retrieval Evaluation Harness.

Measures retrieval quality on the real PDFs in data/, using the real chunker,
the real vector store, and the real HybridRetriever. Compares three modes:

    vector-only  — embeddings + cosine similarity
    bm25-only    — keyword scoring
    hybrid       — production HybridRetriever.search() (rank interleaving)

Reports Recall@1/3/5 and MRR@5, overall and split by query type.

Run:  python -m evaluation.retrieval_eval
"""
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ingestion.loader import load_documents
from ingestion.chunker import chunk_documents
from ingestion.vector_store import index_documents
from retrieval.hybrid_search import HybridRetriever

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
GROUND_TRUTH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ground_truth.json")
K_VALUES = (1, 3, 5)
MAX_K = max(K_VALUES)


def _normalize(text: str) -> str:
    """Collapse all whitespace. PDF extraction inserts stray newlines, so
    snippet matching has to be whitespace-insensitive to be reliable."""
    return " ".join(text.split())


def resolve_ground_truth(questions, chunks):
    """
    Turn each question's answer_snippet into the set of chunk indices that
    contain it. Chunks overlap, so a snippet can legitimately land in more
    than one chunk — any of them counts as a correct retrieval.
    Exits loudly if a snippet resolves to nothing.
    """
    normalized_chunks = [_normalize(c.page_content) for c in chunks]
    resolved, unresolved = [], []

    for q in questions:
        snippet = _normalize(q["answer_snippet"])
        relevant = {i for i, text in enumerate(normalized_chunks) if snippet in text}
        if not relevant:
            unresolved.append(q)
        else:
            resolved.append({**q, "relevant": relevant})

    if unresolved:
        print("\nERROR: these answer_snippets matched no chunk:")
        for q in unresolved:
            print(f"   {q['id']}: {q['answer_snippet']!r}")
        print("\nThe documents in data/ or the chunking settings have changed.")
        print("Fix ground_truth.json before trusting any numbers.")
        sys.exit(1)

    return resolved


def build_content_index(chunks):
    """Map normalized chunk text -> set of chunk indices, so retrieved
    Documents (which are rebuilt objects, not the originals) can be
    matched back to their position in the corpus."""
    index = {}
    for i, c in enumerate(chunks):
        index.setdefault(_normalize(c.page_content), set()).add(i)
    return index


# ── The three retrieval modes ────────────────────────────────────────────
# hybrid calls production code directly. The two baselines reach into the
# same index objects the retriever holds, so the only thing that differs
# between the three arms is how results are combined.

def retrieve_hybrid(retriever, query):
    return [d.page_content for d in retriever.search(query)]


def retrieve_vector(retriever, query):
    results = retriever.collection.query(query_texts=[query], n_results=MAX_K)
    if not results or not results["documents"]:
        return []
    return list(results["documents"][0])


def retrieve_bm25(retriever, query):
    scores = retriever.bm25.get_scores(query.split())
    ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    return [retriever.corpus[i] for i in ranked[:MAX_K] if scores[i] > 0]


MODES = {
    "vector-only": retrieve_vector,
    "bm25-only": retrieve_bm25,
    "hybrid": retrieve_hybrid,
}


def first_hit_rank(retrieved_texts, relevant, content_index):
    """1-based rank of the first retrieved chunk that is in the relevant
    set, or None if there is no hit inside the top MAX_K."""
    for rank, text in enumerate(retrieved_texts[:MAX_K], start=1):
        if content_index.get(_normalize(text), set()) & relevant:
            return rank
    return None


def score(questions, retriever, content_index, mode_fn):
    """Returns {recall@1, recall@3, recall@5, mrr} plus per-question ranks."""
    ranks = []
    for q in questions:
        retrieved = mode_fn(retriever, q["question"])
        ranks.append(first_hit_rank(retrieved, q["relevant"], content_index))

    n = len(ranks)
    metrics = {f"Recall@{k}": sum(1 for r in ranks if r is not None and r <= k) / n
               for k in K_VALUES}
    metrics["MRR@5"] = sum(1 / r for r in ranks if r is not None) / n
    return metrics, ranks


def print_table(title, results, n):
    print(f"\n{title}  (n={n})")
    print("-" * 62)
    header = f"{'mode':<14}" + "".join(f"{m:>11}" for m in results["hybrid"])
    print(header)
    for mode in ("vector-only", "bm25-only", "hybrid"):
        row = f"{mode:<14}" + "".join(f"{v:>11.3f}" for v in results[mode].values())
        print(row)


def print_delta(results):
    print(f"{'hybrid vs vector-only':<14}", end="")
    for metric in results["hybrid"]:
        base = results["vector-only"][metric]
        delta = results["hybrid"][metric] - base
        pct = f"{delta / base * 100:+.1f}%" if base > 0 else "  n/a"
        print(f"{pct:>11}", end="")
    print()


def main():
    print("=" * 62)
    print("AtlasRAG — Retrieval Evaluation")
    print("=" * 62)

    docs = load_documents(DATA_DIR)
    if not docs:
        print(f"\nNo PDFs found in {DATA_DIR}. Add documents and re-run.")
        sys.exit(1)

    chunks = chunk_documents(docs)
    store = index_documents(chunks, show_ui=False)
    if store is None:
        print("\nIndexing failed.")
        sys.exit(1)

    retriever = HybridRetriever(store, chunks)
    content_index = build_content_index(chunks)

    with open(GROUND_TRUTH, encoding="utf-8") as f:
        questions = resolve_ground_truth(json.load(f)["questions"], chunks)

    sources = sorted({d.metadata.get("source", "?") for d in docs})
    print(f"\nCorpus:    {len(sources)} PDFs -> {len(chunks)} chunks")
    print(f"Questions: {len(questions)}")

    all_results = {}
    for mode, fn in MODES.items():
        all_results[mode] = score(questions, retriever, content_index, fn)

    overall = {m: all_results[m][0] for m in MODES}
    print_table("OVERALL", overall, len(questions))
    print_delta(overall)

    for qtype in ("semantic", "exact_keyword"):
        subset = [q for q in questions if q["type"] == qtype]
        by_type = {m: score(subset, retriever, content_index, MODES[m])[0] for m in MODES}
        print_table(f"{qtype.upper().replace('_', ' ')} QUERIES", by_type, len(subset))
        print_delta(by_type)

    print("\n" + "-" * 62)
    print(f"Caveat: {len(questions)} questions over {len(chunks)} chunks from one")
    print("person's document set, authored by the same person who built the")
    print("system. Indicative of relative ordering, not a general benchmark.")
    print("-" * 62)


if __name__ == "__main__":
    main()
