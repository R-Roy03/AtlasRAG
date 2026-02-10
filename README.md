# 🌍 AtlasRAG Platform
### Enterprise-Grade Evaluation & Inference Engine

**AtlasRAG** is not just a chatbot; it is a self-correcting **Knowledge Intelligence System** designed to solve the biggest problem in enterprise GenAI: **Reliability**.

Unlike standard RAG implementations, AtlasRAG includes an internal **"Evaluation Engine" (LLM-as-a-Judge)** that audits every generated response for hallucinations (**Faithfulness**) and utility (**Relevance**) in real-time.

---

## 🚀 Key Features

### ⚖️ Self-Correcting Architecture
Every response is mathematically scored before being presented to the user.
- **Faithfulness Score:** Checks if the answer is grounded *strictly* in the retrieved documents.
- **Relevance Score:** Verifies if the answer actually addresses the user's query.

### 🔍 Hybrid Search Engine
Combines the best of both retrieval worlds for maximum accuracy:
- **Vector Search (ChromaDB):** For semantic understanding and conceptual matching.
- **Keyword Search (Rank-BM25):** For exact matching of domain-specific jargon and technical terms.

### 🧠 Dynamic Knowledge Base
- **User-Controlled Chunking:** Adjust chunk sizes (500-2000 tokens) via the UI to optimize for precision or context.
- **Live Ingestion:** Upload PDF documents directly through the sidebar. The system automatically handles chunking, embedding, and indexing in real-time.
- **Persistent Storage:** Knowledge is stored locally in `chroma_db`, ensuring data persists even after restarts.

### 💾 Smart Chat Management
- **Chat History:** Automatically saves your conversation context.
- **Export & Clear:** Download your full chat history as JSON or clear it with a single click to start fresh.

## 🏗️ System Architecture

![AtlasRAG Architecture](assets/architecture_diagram.png)

> **Flow:** The system ingests PDFs into a vector store. When a user queries, we perform a **Hybrid Search** (Vector + BM25) to retrieve context. The LLM generates an answer, which is then auditted by an **Evaluation Judge** before being shown to the user.

---

## 🛠️ Tech Stack

| Component | Technology | Reasoning |
| :--- | :--- | :--- |
| **LLM (Inference)** | **Gemini 2.5 Flash** | Latest high-speed model for reasoning & generation. |
| **LLM (Judge)** | **Gemini 2.5 Flash** | Same high-tier model used for unbiased self-evaluation. |
| **Orchestration** | **LangChain** | Robust chain-of-thought workflows. |
| **Vector Store** | **ChromaDB** | Local, privacy-focused vector database. |
| **Search Algo** | **BM25 + Vector** | Hybrid retrieval for maximum recall. |
| **Frontend** | **Streamlit** | Interactive UI with real-time metric dashboards & controls. |

---

## ⚙️ Installation & Setup

Follow these steps to run AtlasRAG locally:

### 1. Clone the Repository
```bash
git clone https://github.com/R-Roy03/AtlasRAG.git
cd AtlasRAG

```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

```

### 3. Install Dependencies (Version Locked)
```bash
pip install -r requirements.txt

```

### 4. Set Up API Key
1. Create a `.env` file in the root folder.
2. Add your Google API key:
```env
GOOGLE_API_KEY="your_actual_api_key_here"

```


### 5. Run the Application
```bash
python -m streamlit run app.py

```
---

## 🛡️ Future-Proofing
This project includes a frozen requirements.txt to ensure stability. If you return to this project after weeks or months, simply run pip install -r requirements.txt to restore the exact working environment.

---
*Built with ❤️ by Rakesh Raushan