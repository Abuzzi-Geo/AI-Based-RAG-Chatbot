import os
import pytesseract
from pdf2image import convert_from_path
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# ── Set your paths here ─────────────────────────────────────────
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH   = r"C:\Program Files\poppler\poppler-25.12.0\Library\bin"
DATA_FOLDER    = "documents"        # ← make sure your PDFs are inside this folder
# ────────────────────────────────────────────────────────────────

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def extract_text_from_pdf(pdf_path):
    print(f"  OCR scanning: {os.path.basename(pdf_path)}")
    pages = convert_from_path(pdf_path, dpi=200, poppler_path=POPPLER_PATH)
    texts = []
    for i, page in enumerate(pages):
        text = pytesseract.image_to_string(page)
        if text.strip():
            texts.append(Document(
                page_content=text,
                metadata={"source": pdf_path, "page": i + 1}
            ))
    return texts

# 1. Load all PDFs
print("Loading documents with OCR...")
all_docs = []
pdf_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".pdf")]

if not pdf_files:
    print(f"ERROR: No PDFs found in '{DATA_FOLDER}/' folder.")
    exit(1)

print(f"Found {len(pdf_files)} PDF(s): {pdf_files}")

for pdf_file in pdf_files:
    docs = extract_text_from_pdf(os.path.join(DATA_FOLDER, pdf_file))
    all_docs.extend(docs)
    print(f"  → Extracted {len(docs)} pages of text")

print(f"\nTotal pages with text: {len(all_docs)}")

# 2. Chunk
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(all_docs)
print(f"Created {len(chunks)} chunks")

if len(chunks) == 0:
    print("ERROR: Still 0 chunks. OCR may have failed. Check Tesseract path.")
    exit(1)

# 3. Embed
print("Generating embeddings...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 4. Store
print("Storing in FAISS...")
os.makedirs("vectorstore", exist_ok=True)
vectorstore = FAISS.from_documents(chunks, embeddings)
vectorstore.save_local("vectorstore/")
print("\nDone! Vector store saved to vectorstore/")