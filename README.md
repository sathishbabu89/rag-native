
```markdown
# 📑 Native RAG Chatbot with Ollama + ChromaDB + Streamlit

This project is a **Retrieval-Augmented Generation (RAG)** chatbot that runs **entirely on your local machine**.  
It lets you upload or place PDFs in a folder, then ask natural language questions about them.  
The system retrieves relevant chunks from your documents and uses an Ollama LLM to generate answers.

---

## ✨ Features
- ✅ **Dual-Model RAG** → Embeddings via `sentence-transformers`, generation via `deepseek-r1:8b` on Ollama  
- ✅ **Persistent ChromaDB** → Save & reuse embeddings without re-indexing each run  
- ✅ **Multi-PDF Support** → Drop multiple PDFs into a folder  
- ✅ **Web Chat UI** → Built with Streamlit  
- ✅ **Lightweight & Local** → No external API required  

---

## 📂 Project Structure
```

rag-native/
│── app.py              # Streamlit UI
│── rag\_backend.py      # Core RAG logic
│── requirements.txt    # Dependencies
│── sample\_pdfs/        # Place your PDFs here
│── db/                 # Persistent ChromaDB (auto-created)

````

---

## 🚀 Getting Started

### 1. Install Ollama
Download Ollama for your OS: [https://ollama.com/download](https://ollama.com/download)

Start Ollama (it runs on `http://localhost:11434` by default).

### 2. Pull the LLM Model
```bash
ollama pull deepseek-r1:8b
````

### 3. Clone this Repository

```bash
git clone https://github.com/<your-username>/rag-native.git
cd rag-native
```

### 4. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Add Your PDFs

Place your documents in the `sample_pdfs/` folder.

### 7. Run the App

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🧑‍💻 Usage

1. Click **📥 Build Knowledge Base from PDFs** to index your documents.
2. Ask questions in the chat box.
3. The bot will answer using only the retrieved context from your PDFs.
4. Type new questions and continue chatting!

---

## ⚠️ Limitations

* If your PDFs are scanned images, text extraction may fail (consider OCR preprocessing).
* The current embedding model is `all-MiniLM-L6-v2` for speed; swap it for larger models if needed.
* Ollama must be running locally with the `deepseek-r1:8b` model pulled.

---

## 🛠️ Tech Stack

* [Ollama](https://ollama.com/) → Local LLM hosting
* [ChromaDB](https://www.trychroma.com/) → Vector store
* [SentenceTransformers](https://www.sbert.net/) → Embeddings
* [Streamlit](https://streamlit.io/) → Chat UI

---

## 📌 Roadmap

* [ ] File upload directly from Streamlit UI
* [ ] Support for multiple vector DB backends (Pinecone, Weaviate)
* [ ] Docker container for easier deployment

---

## 📜 License

MIT License. Free to use and modify.
