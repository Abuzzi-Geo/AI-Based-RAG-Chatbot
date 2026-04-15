import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Load the saved vector store
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.load_local(
    "vectorstore/",
    embeddings,
    allow_dangerous_deserialization=True
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Load Groq LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

# Prompt
prompt_template = """You are a helpful college information assistant.
Use only the information below to answer the student's question.
If the answer is not in the context, say "I don't have that information. Please contact the college office."

Context:
{context}

Question: {question}

Answer:"""

prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

# Build RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt},
    return_source_documents=True
)

def ask(question: str) -> dict:
    result = qa_chain.invoke({"query": question})
    return {
        "answer": result["result"],
        "sources": [doc.metadata.get("source", "unknown") for doc in result["source_documents"]]
    }

# Quick test
if __name__ == "__main__":
    q = "What is the admission policy?"
    print(f"Question: {q}")
    response = ask(q)
    print(f"Answer: {response['answer']}")
    print(f"Sources: {response['sources']}")