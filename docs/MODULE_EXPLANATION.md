# Module Explanations

### 1. Ingestion Layer
Responsible for loading PDFs using `PyPDFLoader` and splitting text into optimized chunks via `RecursiveCharacterTextSplitter`.

### 2. Hybrid Retrieval
Combines semantic search (Vector) and keyword matching (BM25) to ensure high recall for both conceptual and specific term queries.

### 3. Inference Engine
Uses Google Gemini 2.5 Flash to generate responses based strictly on the retrieved context.

### 4. Evaluation Engine (Self-Correction)
Implements 'LLM-as-a-Judge' to score responses. It checks if the answer is grounded in the source (Faithfulness) and if it actually answers the user (Relevance).