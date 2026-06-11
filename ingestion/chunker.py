from ingestion.loader import Document


def chunk_documents(documents: list[Document], chunk_size=1000, chunk_overlap=200) -> list[Document]:
    """
    Splits documents into smaller chunks using recursive character splitting.
    No langchain dependency — pure Python implementation.
    """
    print(f"Chunking documents with Size: {chunk_size} & Overlap: {chunk_overlap}...")
    if not documents:
        return []

    separators = ["\n\n", "\n", ". ", " ", ""]
    chunks = []

    for doc in documents:
        text = doc.page_content
        split_texts = _recursive_split(text, separators, chunk_size)

        for piece in split_texts:
            piece = piece.strip()
            if piece:
                chunks.append(Document(
                    page_content=piece,
                    metadata=dict(doc.metadata),
                ))

    # Apply overlap by merging short chunks and creating overlapping windows
    if chunk_overlap > 0 and len(chunks) > 1:
        overlapped = []
        for i, chunk in enumerate(chunks):
            if i > 0 and len(chunk.page_content) < chunk_size:
                # Prepend overlap from previous chunk
                prev_text = chunks[i - 1].page_content
                overlap_text = prev_text[-chunk_overlap:] if len(prev_text) > chunk_overlap else prev_text
                merged = overlap_text + " " + chunk.page_content
                if len(merged) <= chunk_size + chunk_overlap:
                    chunk = Document(page_content=merged, metadata=dict(chunk.metadata))
            overlapped.append(chunk)
        chunks = overlapped

    print(f"   Created {len(chunks)} chunks.")
    return chunks


def _recursive_split(text: str, separators: list[str], chunk_size: int) -> list[str]:
    """Recursively split text by trying each separator in order."""
    if len(text) <= chunk_size:
        return [text]

    # Find the best separator
    separator = separators[-1]  # fallback: split by character
    for sep in separators:
        if sep in text:
            separator = sep
            break

    parts = text.split(separator)
    results = []
    current = ""

    for part in parts:
        candidate = current + separator + part if current else part
        if len(candidate) <= chunk_size:
            current = candidate
        else:
            if current:
                results.append(current)
            # If this single part is too long, recursively split with next separator
            if len(part) > chunk_size and separators.index(separator) < len(separators) - 1:
                remaining_seps = separators[separators.index(separator) + 1:]
                results.extend(_recursive_split(part, remaining_seps, chunk_size))
            else:
                current = part
                continue
            current = ""

    if current:
        results.append(current)

    return results