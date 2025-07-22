import streamlit as st
from agents.IngestionAgent import IngestionAgent
from agents.RetrievalAgent import RetrievalAgent
from agents.LLMResponseAgent import LLMResponseAgent

st.title("Agentic Q&A Document Chatbot")

uploaded_files = st.file_uploader(
    "Upload documents",
    accept_multiple_files=True,
    type=["pdf", "pptx", "csv", "docx", "txt"]
)

query = st.text_input("Ask a question:")

if 'query' not in st.session_state:
    st.session_state.query = ""

if st.button("Submit") and uploaded_files and query:
    st.session_state.query = query

    ingestion = IngestionAgent()
    retrieval = RetrievalAgent()
    llm = LLMResponseAgent(retrieval)

    msg1 = ingestion.process(uploaded_files)
    msg2 = retrieval.process(msg1)
    final_msg = llm.process(msg2)

    st.subheader("Answer")
    st.write(final_msg["payload"]["answer"])

    st.subheader("Source Chunks")
    for i, chunk in enumerate(final_msg["payload"]["sources"]):
        st.markdown(f"**Chunk {i+1}:** {chunk}")