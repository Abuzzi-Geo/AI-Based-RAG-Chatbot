from dotenv import load_dotenv
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

load_dotenv()

print("Testing embeddings (runs locally, no API needed)...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector = embeddings.embed_query("What is the college fee?")
print(f"Embeddings working! Vector length: {len(vector)}")

print("\nTesting Groq LLM...")
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
response = llm.invoke("Say hello in one sentence.")
print(f"Groq LLM working! Response: {response.content}")

print("\nPhase 1 complete! You are ready for Phase 2.")