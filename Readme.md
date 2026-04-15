# 🎓 AI-Based RAG Chatbot for College Information System

An intelligent chatbot that answers student queries about college policies, fees, admission, attendance, placements, and more — powered by Retrieval-Augmented Generation (RAG).

---

## 📌 What It Does

- Answers student questions instantly based on real college documents
- Uses OCR to read scanned PDF policies and manuals
- Retrieves the most relevant document chunks for each query
- Generates accurate, grounded answers using a Large Language Model (Groq / LLaMA 3)
- Shows source documents for every answer (transparent and trustworthy)
- Available 24/7 — no dependency on office staff

---

## 🧠 How It Works (RAG Pipeline)

```
Student Question
      ↓
Embed the question (HuggingFace MiniLM)
      ↓
Search FAISS vector store for relevant chunks
      ↓
Send chunks + question to LLM (Groq LLaMA 3)
      ↓
Return grounded answer + source documents
```

---

## 🗂️ Project Structure

```
RagChatBot/
├── documents/              # College PDF files (not committed to Git)
├── vectorstore/            # FAISS index (auto-generated, not committed)
├── frontend/
│   └── index.html          # Chat UI (open directly in browser)
├── ingest.py               # Phase 2: PDF ingestion + embedding pipeline
├── rag_chain.py            # Phase 3: RAG query chain
├── main.py                 # Phase 4: FastAPI backend server
├── .env                    # API keys (not committed to Git)
├── .gitignore
└── requirements.txt
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | Groq API (LLaMA 3 8B) |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` |
| Vector Database | FAISS (local, free) |
| OCR | Tesseract + pdf2image |
| Backend | FastAPI + Uvicorn |
| Frontend | Plain HTML + JavaScript |
| RAG Framework | LangChain |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/RagChatBot.git
cd RagChatBot
```

### 2. Create and activate virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install system dependencies

- **Tesseract OCR**: Download from https://github.com/UB-Mannheim/tesseract/wiki
- **Poppler** (Windows): Download from https://github.com/oschwartz10612/poppler-windows/releases

Update the paths in `ingest.py`:
```python
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH   = r"C:\Program Files\poppler\...\Library\bin"
```

### 5. Set up environment variables

Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free Groq API key at: https://console.groq.com

### 6. Add your college documents

Place your college PDF files inside the `documents/` folder.

### 7. Run the ingestion pipeline

```bash
python ingest.py
```

This scans all PDFs using OCR, generates embeddings, and saves the FAISS vector store. Run this once, and again whenever you add or update documents.

### 8. Test the RAG chain

```bash
python rag_chain.py
```

### 9. Start the backend server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 10. Open the chat UI

Open `frontend/index.html` directly in your browser and start asking questions.

---

## 🧪 Testing the API

Once the server is running, visit:

- `http://localhost:8000` — health check
- `http://localhost:8000/docs` — interactive Swagger UI to test queries

Example request:
```json
POST /ask
{
  "question": "What is the attendance policy?"
}
```

Example response:
```json
{
  "answer": "Students must maintain a minimum of 75% attendance...",
  "sources": ["Time & Attendance_Policy Lead.pdf"]
}
```

---

## 📄 Documents Supported

The chatbot is currently trained on the following college documents:

- Admission Policy
- Anti-Ragging Policy
- Disciplinary Procedure
- Exam Policy
- Internship Manual
- Placement Policy
- Time & Attendance Policy

To add more documents, place the PDFs in the `documents/` folder and re-run `python ingest.py`.

---

## 🔒 .gitignore

The following are excluded from version control:

```
.env
vectorstore/
documents/
venv/
__pycache__/
*.pyc
```

---

## 🛣️ Future Scope

- Voice-enabled chatbot interface
- Multi-language support (regional languages)
- WhatsApp integration
- Mobile app (Android / iOS)
- AI analytics dashboard for common queries
- ERP system integration for real-time data

---

## 📃 License

This project was developed as a student project for academic purposes.