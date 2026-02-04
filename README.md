# 🌍 AtlasRAG Platform
### Enterprise-Grade Evaluation & Inference Engine

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/Orchestration-LangChain-green)](https://www.langchain.com/)
[![Gemini](https://img.shields.io/badge/AI-Gemini%202.0-purple)](https://deepmind.google/technologies/gemini/)

**AtlasRAG** is not just a chatbot; it is a self-correcting **Knowledge Intelligence System** designed to solve the biggest problem in enterprise GenAI: **Reliability.**

Unlike standard RAG implementations, AtlasRAG includes an internal **"Evaluation Engine" (LLM-as-a-Judge)** that audits every generated response for hallucinations (Faithfulness) and utility (Relevance) in real-time.

---

## 🚀 Key Features

### ⚖️ Self-Correcting Architecture
Every response is mathematically scored before being presented to the user.
- **Faithfulness Score:** Checks if the answer is grounded *strictly* in the retrieved documents.
- **Relevance Score:** Verifies if the answer actually addresses the user's query.

### 🔍 Hybrid Search Engine
Combines the best of both retrieval worlds:
- **Vector Search (ChromaDB):** For semantic understanding and conceptual matching.
- **Keyword Search (Rank-BM25):** For exact matching of domain-specific jargon and technical terms.

### 📊 Observability & Audit Trails
Treats AI as a production component, not a black box.
- Logs every interaction, latency, token usage, and quality score to `logs/query_logs.csv` for analytics.

### 🔒 Local-First Privacy
- Documents are processed and stored locally using **ChromaDB**. Your private data never leaves the ingestion pipeline.

---

## 🛠️ Tech Stack

| Component | Technology | Reasoning |
| :--- | :--- | :--- |
| **LLM (Inference)** | **Gemini 2.0 Flash Lite** | Low-latency reasoning with high context window. |
| **LLM (Judge)** | **Gemini 1.5 Flash** | Independent audit model for unbiased scoring. |
| **Orchestration** | **LangChain** | Robust chain-of-thought workflows. |
| **Vector Store** | **ChromaDB** | Local, privacy-focused vector database. |
| **Search Algo** | **BM25 + Vector** | Hybrid retrieval for maximum recall. |
| **Frontend** | **Streamlit** | Interactive UI with real-time metric dashboards. |

---

## ⚙️ Installation & Setup

Follow these steps to run AtlasRAG locally:

### 1. Clone the Repository
```bash
git clone [https://github.com/R-Roy03/AtlasRAG-Enterprise-Architecture.git](https://github.com/R-Roy03/AtlasRAG-Enterprise-Architecture.git)
cd AtlasRAG