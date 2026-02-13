# 🌍 AtlasRAG Platform

![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)
![AI](https://img.shields.io/badge/Gen_AI-Gemini_2.5-orange?style=for-the-badge&logo=google&logoColor=white)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/Framework-LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![ChromaDB](https://img.shields.io/badge/Vector_DB-Chroma-purple?style=for-the-badge)

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

![AtlasRAG Architecture](assets/atlasrag_architecture.png)

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
## 🏆 Competitive Advantage (Why AtlasRAG?)

| Feature | Standard RAG ❌ | AtlasRAG (Your Project) ✅ |
| :--- | :---: | :---: |
| **Search Type** | Vector Only (Similarity) | **Hybrid (Vector + Keyword)** |
| **Accuracy** | Prone to Hallucinations | **High (Self-Correction)** |
| **Evaluation** | None (Blind Trust) | **LLM-as-a-Judge (Faithfulness Check)** |
| **Privacy** | Cloud Vector DB | **Local ChromaDB (Privacy First)** |
| **Cost** | High (OpenAI) | **Optimized (Gemini Flash)** |

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
## 🚀 Usage Guide

1. **Environment Setup**: Ensure your virtual environment is active: `venv\Scripts\activate`.
2. **Run App**: Launch the interface using `streamlit run app.py`.
3. **Ingest Data**: 
   - Drag and drop your PDFs into the sidebar.
   - Click **"Update Knowledge Base"** to trigger chunking and embedding.
4. **Interactive Chat**: Ask questions based on your documents. The system will provide answers along with **Faithfulness** and **Relevance** scores.

## 📖 Usage Examples

### Sample Scenario: Basic Electrical Engineering
**User Query:** *"Explain Kirchhoff's Current Law (KCL) with an example."*

**AtlasRAG Output:**
> "Kirchhoff's Current Law (KCL) states that the algebraic sum of the currents meeting at a junction in an electric circuit is equal to zero.
> **Example:** In a junction with entering currents I1, I3 and leaving currents I2, I4: I1 + I3 = I2 + I4."

**Evaluation Scores:**
- ✅ **Faithfulness:** 100% (Grounded in module-1 notes)
- ✅ **Relevance:** 100% (Directly answers the definition and example request)

## 📂 Project Structure
- `app.py`: Main Streamlit interface and application logic.
- `retriever.py`: Logic for Hybrid Search (BM25 + ChromaDB).
- `evaluator.py`: LLM-as-a-Judge implementation for answer auditing.
- `assets/`: Contains architecture diagrams and images.
```
---

```

## 🛡️ Future-Proofing
This project includes a frozen requirements.txt to ensure stability. If you return to this project after weeks or months, simply run pip install -r requirements.txt to restore the exact working environment.

---

## 📜 License

This project is licensed under the MIT License.

---

## 👤 Author

**Rakesh Raushan**
---
*Built with ❤️ by Rakesh Raushan*