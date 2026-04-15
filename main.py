from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from rag_chain import ask

app = FastAPI(title="College RAG Chatbot")

# Allow frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

@app.post("/ask")
def answer_question(body: Question):
    result = ask(body.question)
    return result

@app.get("/")
def health_check():
    return {"status": "College RAG Chatbot is running"}