# 📄 Document Q&A AI Backend (FastAPI + RAG + OpenAI)

A **production-minded AI backend** that ingests documents, builds vector embeddings, and answers user questions using Retrieval-Augmented Generation (RAG).

This project demonstrates how to design and build a **real-world AI system** with clean architecture, scalability considerations, and modern backend engineering practices.

---

## 🚀 Features

* 📥 Document ingestion (sync + background)
* 🔎 Semantic search using vector embeddings (Qdrant)
* 🤖 AI-powered answers using OpenAI
* ⚡ Redis caching for fast repeated queries
* 📡 Streaming responses (ChatGPT-style)
* 🔐 API key authentication
* 🔁 Retry + timeout handling for external APIs
* 🧠 Reranking + filtering for better retrieval quality
* 📦 Fully containerized with Docker Compose
* 🧱 Clean, enterprise-style architecture

---

## 🏗️ Architecture Overview

```text
Client
  ↓
FastAPI API
  ↓
Auth (API Key)
  ↓
Service Layer
  ├─ Redis Cache
  ├─ Retriever (Qdrant)
  │     ├─ Embeddings (OpenAI)
  │     ├─ Vector Search
  │     └─ Reranking
  └─ OpenAI (Answer Generation)
  ↓
Response (JSON or Streaming)
```

---

## 📂 Project Structure

```text
app/
├── main.py
├── api/
│   └── routers/
│       ├── ask_router.py
│       ├── ingest_router.py
│       └── health_router.py
├── schemas/
├── services/
├── providers/
├── retrieval/
├── cache/
└── core/

Dockerfile
docker-compose.yml
requirements.txt
.env
```

---

## ⚙️ Setup & Run

### 1️⃣ Clone the repo

```bash
git clone https://github.com/E-Asrar-Haghighi/Document-Q-A-AI-Backend-FastAPI-RAG-OpenAI- document-qa-ai
cd document-qa-ai
```

---

### 2️⃣ Create `.env`

```env
OPENAI_API_KEY=your_openai_key
APP_API_KEY=my-super-secret-api-key

OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

REDIS_HOST=redis
QDRANT_HOST=qdrant

PROVIDER_TIMEOUT_SECONDS=20
PROVIDER_MAX_RETRIES=2
PROVIDER_RETRY_DELAY_SECONDS=1.0

RETRIEVAL_TOP_K=3
RETRIEVAL_MIN_SCORE=0.20

```

---

### 3️⃣ Run with Docker

```bash
docker compose up --build
```

---

### 4️⃣ Open API docs

```text
http://localhost:8000/docs
```

---

## 🔐 Authentication

All main endpoints require an API key:

```text
X-API-Key: my-super-secret-api-key
```

---

## 📌 API Endpoints

### 🔹 Health

```http
GET /health
```

---

### 🔹 Ingest Document (Sync)

```http
POST /ingest
```

```json
{
  "document_id": "doc-1",
  "text": "Artificial intelligence helps automate tasks..."
}
```

---

### 🔹 Ingest Document (Background)

```http
POST /ingest-background
```

Returns immediately:

```json
{
  "message": "Document ingestion started in background.",
  "status": "accepted"
}
```

---

### 🔹 Ask Question

```http
POST /ask
```

```json
{
  "question": "What helps automate tasks?"
}
```

Response:

```json
{
  "answer": "...",
  "sources": [...]
}
```

---

### 🔹 Streaming Ask (Chat-style)

```http
POST /ask-stream
```

Returns streamed text response.

---

## 🧠 How It Works

### 1. Ingestion

* Split document into chunks
* Generate embeddings via OpenAI
* Store vectors in Qdrant

---

### 2. Retrieval

* Embed user question
* Search similar chunks in Qdrant
* Filter low-quality results
* Deduplicate + rerank

---

### 3. Answer Generation

* Build grounded context
* Send to OpenAI
* Return structured response

---

### 4. Caching

* Redis stores previous answers
* Reduces cost and latency

---

## 🧪 Example Flow

```text
1. POST /ingest
2. POST /ask
3. Cache hit on repeated queries
4. Streaming via /ask-stream
```

---

## 🧰 Tech Stack

* FastAPI
* OpenAI API (Chat + Embeddings)
* Qdrant (Vector DB)
* Redis (Caching)
* Docker & Docker Compose

---

## ⚡ Production Features

* Structured logging
* Centralized error handling
* Retry + timeout logic
* API key authentication
* Background processing
* Streaming responses

---

## 🧩 Future Improvements

* JWT authentication
* Job tracking for background ingestion
* Persistent metadata DB (Postgres)
* Advanced reranking models
* UI (React frontend)
* Observability (Prometheus, Grafana)

---

## 💡 What This Project Demonstrates

* Building a **real RAG system**
* Designing **clean backend architecture**
* Integrating AI into production-style APIs
* Handling **latency, failures, and scaling concerns**
* Writing **maintainable and modular code**

---

## 👨‍💻 Author

Ebrahim Asrarhaghighi
AI Engineer & Data Scientist
