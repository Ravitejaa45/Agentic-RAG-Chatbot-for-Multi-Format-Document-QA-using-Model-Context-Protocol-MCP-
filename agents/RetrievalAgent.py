import faiss
import streamlit as st
import os
import hashlib
from dotenv import load_dotenv
from core.embedder import load_embedding_model
from core.mcp import create_mcp_message
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()

@st.cache_data(show_spinner=False)
def build_cached_index(docs_hash, docs, chunk_size, chunk_overlap, model_name="all-MiniLM-L6-v2"):
    model = load_embedding_model()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = []
    for doc in docs:
        chunks.extend(splitter.split_text(doc))

    embeddings = model.encode(chunks, convert_to_tensor=False)
    dim = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    return index, chunks


class RetrievalAgent:
    def __init__(self):
        self.model_name = "all-MiniLM-L6-v2"
        self.index = None
        self.text_chunks = []
        self.chunk_size = int(os.getenv("CHUNK_SIZE", 500))
        self.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", 100))

    def _hash_docs(self, docs):
        combined = "".join(docs)
        return hashlib.md5(combined.encode()).hexdigest()

    def build_index(self, docs):
        docs_hash = self._hash_docs(docs)
        self.index, self.text_chunks = build_cached_index(
            docs_hash, docs, self.chunk_size, self.chunk_overlap, self.model_name
        )

    def process(self, message):
        docs = message["payload"]["docs"]
        self.build_index(docs)
        return create_mcp_message(
            sender="RetrievalAgent",
            receiver="LLMResponseAgent",
            msg_type="CONTEXT_RESPONSE",
            trace_id=message["trace_id"],
            payload={"query": st.session_state.query}
        )

    def retrieve_top_chunks(self, query, top_k=4):
        embedder = load_embedding_model()
        q_embed = embedder.encode([query])
        D, I = self.index.search(q_embed, top_k)
        return [self.text_chunks[i] for i in I[0]]