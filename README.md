# Agentic RAG Chatbot for Multi-Format Document QA using Model Context Protocol (MCP)

An intelligent document-driven Q&A chatbot designed to parse and reason over real-world business files using modular agents, semantic retrieval, and the blazing-fast LLaMA-3 hosted on Groq. It supports natural language queries on PDFs, Word docs, PPTs, CSV and Text - all processed through an **MCP-style agent messaging architecture**.

Powered by **Docling** for high-quality parsing and chunking, **FAISS** for vector search, and **SentenceTransformers** for embeddings - this system delivers explainable, reference-backed answers with minimal latency.

## What This Project Does

This application transforms unstructured business files into an **interactive Q&A interface** where users can:

- Upload documents in **PDF, DOCX, PPTX, CSV, TXT** formats.  
- Ask questions in **plain English** like *"What is Ravi's Educational Background?"*.  
- Get answers grounded in the actual content of the documents.  
- View the specific source text chunks used to generate the answer.
- Run everything locally through a clean **Streamlit interface**.

Under the hood, it simulates **agent-based communication** using a simplified **Model Context Protocol (MCP)**. Each specialized component (agent) handles a specific task such as:

- Parsing and extracting text from documents using **Docling**.
- Chunking and embedding text with **Sentence Transformers**.
- Performing semantic search via **FAISS**.
- Generating LLM responses using **LLaMA-3** through **Groq API**.
- Passing structured messages between agents using **traceable MCP format**.

This modular design makes the project easy to extend, debug, and integrate into more advanced RAG pipelines.

## Technical Stack Summary

| Layer             | Tools / Libraries                                      |
|------------------|--------------------------------------------------------|
| Document Parsing | **Docling** - for multi-format file parsing and markdown conversion. |
| Embeddings        | SentenceTransformers using the `all-MiniLM-L6-v2` model. |
| Vector Search     | FAISS – flat L2 distance index for similarity retrieval. |
| LLM Backend       | `llama3-8b-8192` via the Groq API  .                  |
| Agent Messaging   | Model Context Protocol (MCP) using UUID-based trace IDs. |
| Interface         | Streamlit – lightweight UI for local testing and interaction. |
| Secrets Management| `python-dotenv` for `.env` to securely handle environment variables. |

## Supported File Formats

This chatbot leverages **Docling** to convert a variety of document types into clean, structured Markdown while preserving semantic layout and text fidelity.

Supported formats:

- `.pdf` – Portable Document Format.
- `.docx` – Microsoft Word documents.
- `.pptx` – Microsoft PowerPoint presentations.
- `.csv` – Comma-Separated Values (tabular data).
- `.txt` – Plain text files.

## Why Docling?

**Docling** is a powerful, open-source library for document conversion that supports multi-format inputs and provides structured markdown output. Its hybrid chunking and linguistic awareness make it ideal for semantically chunked retrieval systems like this chatbot.

### Benefits

- Clean separation between document structure and content.  
- Handles tables, lists, sections, and formatting gracefully.  
- Integrates easily with embedding pipelines like Sentence Transformers and FAISS.  


## How It Works (Architecture Breakdown)

Each part of the flow is **isolated into agents**, and they communicate via structured messages using a custom version of **Model Context Protocol (MCP)**:

| Agent             | Role                                                                 |
|------------------|----------------------------------------------------------------------|
| IngestionAgent    | Converts uploaded files into clean Markdown using Docling.           |
| RetrievalAgent    | Splits text into chunks, generates embeddings, and builds FAISS index. |
| LLMResponseAgent  | Constructs prompts, retrieves relevant context, and queries LLaMA-3.   |
| MCP | Facilitates traceable message passing between agents.                 |


## Key Features

- **Semantic Search**: Uses embedding-based similarity instead of keyword matching.  
- **Chunk-Aware Indexing**: Dynamically splits documents using customizable token window sizes. 
- **LLM Integration**: Sends compressed context to LLaMA-3 (via Groq) for fast, fluent generation.  
- **Explainability**: Displays source chunks for full transparency.  
- **Stateless & Modular**: Stateless protocol between agents makes the pipeline extensible.  

## Project Structure

```text
agentic-rag-chatbot/
├── agents/
│   ├── IngestionAgent.py        
│   ├── RetrievalAgent.py        
│   └── LLMResponseAgent.py      
├── core/
│   ├── parser.py                
│   ├── embedder.py              
│   └── mcp.py                   
├── ui/
│   └── app.py                   
├── .env                        
├── requirements.txt             
└── README.md             
```

# Setup Instructions

## 1. Clone the repository

```bash
git clone <path to your chatbot .git>
cd agentic-rag-chatbot
```

## 2. Create & activate venv

```bash
python -m venv <env_name>
venv\Scripts\activate
```

## 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

## 4. Add your API keys in `.env`

```bash
GROQ_API_KEY=<your_groq_key>
CHUNK_SIZE=<your_chunk_size>
CHUNK_OVERLAP=<your_chunk_overlap>
```

## 5. Launch the chatbot

```bash
streamlit run ui/app.py
```

## Sample Use Case

1. **Upload Documents**  
   Upload files like `quarterly_report.pdf` and `team_kpi.csv` via the interface.

2. **Ask a Question**  
   Example: _"What KPIs were tracked in Q1?"_

3. **Behind the Scenes Workflow**  
   The chatbot performs the following steps:

   - Parses both files using **Docling**.
   - Splits content into logical chunks.
   - Embeds chunks and retrieves top relevant segments.
   - Queries **LLaMA-3** via **Groq** with the extracted context.
   - Returns a grounded answer along with source references.


## Future Plans

- **Fine-tuned LLM integration** for context-specific domains when users upload domain-specific documents.  
- Add **vision-based document understanding** for extracting insights from charts and images.  
- Enable **multi-turn conversation** with better dialogue memory and state tracking. 
- Support **persistent document indexing** using Qdrant or Chroma for long-term storage.

## Summary

This chatbot demonstrates a clean, modular, and scalable approach to RAG-based document QA - with a strong focus on **traceability**, **explainability**, and **format-agnostic parsing** powered by [Docling](https://docling-project.github.io/docling/). It supports multi-agent coordination using **Model Context Protocol (MCP)** for clear agent interaction and robust workflow orchestration.

Key highlights:

- **Docling-powered ingestion** to parse PDFs, DOCX, PPTX,  CSV, and TXT in a unified pipeline.  
- **MCP-based architecture** for structured communication between agents.  
- **Semantic vector retrieval** using sentence-transformer embeddings and FAISS.  
- **LLM response generation** with top-k document grounding.  
- **Developer-friendly and modular** - easy to plug in different embedding models or LLMs.


