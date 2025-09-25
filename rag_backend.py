import os
import requests
from PyPDF2 import PdfReader
import chromadb
from chromadb.utils import embedding_functions

# ---------------- CONFIG ----------------
OLLAMA_URL = "http://localhost:11434"
GENERATION_MODEL = "deepseek-r1:8b"  # Generator model

# Persistent vector DB
chroma_client = chromadb.PersistentClient(path="./db")

# Use SentenceTransformers for embeddings (faster + higher quality)
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Create / load collection
collection = chroma_client.get_or_create_collection(
    name="pdf_chunks",
    embedding_function=embedding_fn
)

# ---------------- PDF LOADING ----------------
def load_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text.strip()

def load_pdfs_from_folder(folder):
    text = ""
    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            text += load_pdf_text(os.path.join(folder, file)) + "\n"
    return text.strip()

# ---------------- CHUNKING ----------------
def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

# ---------------- VECTOR DB BUILD ----------------
def build_vector_db(folder="sample_pdfs"):
    text = load_pdfs_from_folder(folder)
    chunks = chunk_text(text)
    for i, chunk in enumerate(chunks):
        collection.add(documents=[chunk], ids=[f"doc-{i}"])
    return len(chunks)

# ---------------- OLLAMA QUERY ----------------
def ask_ollama(prompt: str, context: str):
    url = f"{OLLAMA_URL}/api/generate"
    data = {
        "model": GENERATION_MODEL,
        "prompt": f"""
You are a helpful assistant. 
Answer strictly based on the provided context. 
If the context does not contain the answer, reply "I don’t know."

Context:
{context}

Question: {prompt}
Answer:""",
        "stream": False
    }
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json().get("response", "").strip()

# ---------------- RAG QUERY ----------------
def query_rag(user_question: str, n_results=3):
    results = collection.query(query_texts=[user_question], n_results=n_results)
    context = "\n".join([doc for docs in results["documents"] for doc in docs])
    answer = ask_ollama(user_question, context)
    return answer, context
