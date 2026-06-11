import os
from pypdf import PdfReader


class Document:
    """Simple document class — no langchain dependency."""
    def __init__(self, page_content: str, metadata: dict = None):
        self.page_content = page_content
        self.metadata = metadata or {}


def load_documents(folder_path: str) -> list[Document]:
    documents = []
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return []

    print(f"Loading PDFs from: {folder_path}...")
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            try:
                filepath = os.path.join(folder_path, filename)
                reader = PdfReader(filepath)
                for i, page in enumerate(reader.pages):
                    text = page.extract_text() or ""
                    if text.strip():
                        documents.append(Document(
                            page_content=text,
                            metadata={"source": filename, "page": i + 1},
                        ))
                print(f"   Loaded: {filename} ({len(reader.pages)} pages)")
            except Exception as e:
                print(f"   Error: {filename} - {e}")
    return documents