# AI Knowledge Assistant

A local Retrieval-Augmented Generation (RAG) based AI Knowledge Assistant that can ingest company knowledge documents, generate embeddings, perform semantic search, and answer questions using a local Large Language Model (LLM).

This project simulates an enterprise internal knowledge assistant similar to systems built using Azure OpenAI or AWS Bedrock architectures.

---

# Features

- Local AI-powered knowledge assistant
- RAG (Retrieval-Augmented Generation) pipeline
- Semantic document retrieval using embeddings
- Local LLM integration using Ollama
- Supports multiple document types:
  - Markdown (.md)
  - Text (.txt)
  - PDF (.pdf)
  - DOCX (.docx)
  - CSV (.csv)
- Chroma vector database for semantic search
- FastAPI backend
- Streamlit chat interface
- Citations for retrieved answers
- Query latency tracking
- Persistent local vector storage

---

# Tech Stack

| Layer | Technology |
|---|---|
| LLM | Ollama + Qwen2.5 |
| Embeddings | Sentence Transformers |
| Vector Database | ChromaDB |
| Backend API | FastAPI |
| Frontend UI | Streamlit |
| Parsing | PyPDF, python-docx, pandas |
| Language | Python |

---

# Project Architecture

```text
Documents
   ↓
Ingestion Pipeline
   ↓
Text Cleaning
   ↓
Chunking
   ↓
Embeddings
   ↓
Chroma Vector Database
   ↓
Retriever
   ↓
RAG Pipeline
   ↓
Ollama LLM
   ↓
FastAPI Backend
   ↓
Streamlit UI
```

---

# Folder Structure

```text
ai-knowledge-assistant/
│
├── api/
│   └── main.py
│
├── core/
│   ├── ingest.py
│   ├── embed.py
│   ├── retriever.py
│   ├── rag.py
│   └── utils.py
│
├── ui/
│   └── app.py
│
├── tools/
│   └── synth_data.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── chroma_db/
│
├── logs/
│
├── requirements.txt
├── README.md
└── .env
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone <your-github-repo-url>
cd ai-knowledge-assistant
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Install Ollama

Download and install Ollama:

https://ollama.com/

Pull the model:

```bash
ollama pull qwen2.5:3b
```

Verify installation:

```bash
ollama list
```

---

# Running the Project

## Step 1 — Generate Synthetic Documents

```bash
python tools/synth_data.py
```

---

## Step 2 — Run Ingestion Pipeline

```bash
python core/ingest.py
```

---

## Step 3 — Generate Embeddings

```bash
python core/embed.py
```

---

## Step 4 — Start FastAPI Backend

```bash
uvicorn api.main:app --reload
```

API Docs:

```text
http://127.0.0.1:8000/docs
```

---

## Step 5 — Start Streamlit UI

Open a new terminal:

```bash
streamlit run ui/app.py
```

UI URL:

```text
http://localhost:8501
```

---

# Example Questions

```text
What is FloCard?
How does employee onboarding work?
What are the security policies?
How are backups handled?
What is the deployment process?
```

---

# API Example

## POST /ask

Request:

```json
{
  "question": "What is FloCard?"
}
```

Response:

```json
{
  "question": "What is FloCard?",
  "answer": "FloCard is a digital business card platform...",
  "citations": [
    "flocard_overview.md"
  ],
  "latency_seconds": 1.42
}
```

---

# Supported File Types

| File Type | Supported |
|---|---|
| Markdown (.md) | Yes |
| Text (.txt) | Yes |
| PDF (.pdf) | Yes |
| DOCX (.docx) | Yes |
| CSV (.csv) | Yes |

---

# Future Improvements

- Better chunking strategies
- Hybrid retrieval
- Reranking models
- Docker deployment
- Authentication system
- Evaluation dashboard
- Export to Word/Excel
- Streaming responses

---

# Learning Outcomes

This project demonstrates:

- RAG architecture understanding
- Embeddings and semantic search
- Vector database integration
- Local LLM deployment
- FastAPI backend development
- Streamlit frontend development
- AI system design
- Enterprise AI workflow concepts

---

# Demo Flow

1. Generate synthetic documents
2. Run ingestion pipeline
3. Generate embeddings
4. Start FastAPI backend
5. Launch Streamlit UI
6. Ask questions
7. Observe citations and latency

---

# Author

Uditnarayan Routray

B.Tech 2025 Graduate

AI Knowledge Assistant Project