import streamlit as st
from rag_backend import build_vector_db, query_rag

st.set_page_config(page_title="📑 Native RAG Chatbot", layout="wide")

st.title("📑 Native RAG Chatbot with Ollama + ChromaDB")

# Button to build database
if st.button("📥 Build Knowledge Base from PDFs"):
    with st.spinner("Building vector DB..."):
        chunks_added = build_vector_db("sample_pdfs")
    st.success(f"✅ Added {chunks_added} chunks from PDFs!")

# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask a question from your PDFs..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer, _ = query_rag(prompt)
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
