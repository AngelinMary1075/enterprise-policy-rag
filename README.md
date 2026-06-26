# Enterprise Policy Intelligence Assistant (RAG)

An intelligent, context-aware Retrieval-Augmented Generation (RAG) pipeline designed to bridge the gap between structured organizational data and unstructured corporate documents. This application unifies SQLite relational employee records with PDF-based documents (such as candidate resumes) into a localized, ultra-secure vector ecosystem, completely decoupled from external third-party cloud API dependencies.

## Key Features

* **Structured Data Extraction:** Parses employee profiles, salaries, roles, and expertise from a local SQLite engine.
* **Dynamic Unstructured Parsing:** Automatically scans local directories to read, split, and chunk multi-page PDF documents.
* **Unified Vector Indexing:** Blends multi-source operational streams into a singular local FAISS vector store using highly accurate open-source embeddings.
* **100% Local Intelligence:** Leverages Ollama (llama3) locally to synthesize document context and format professional, conversational responses.
* **Modular Multi-Tier Architecture:** Built with a blazing-fast FastAPI backend service coupled with an intuitive Streamlit interactive dashboard.

## Tech Stack & Core Dependencies

* **Frontend Dashboard:** Streamlit
* **API Service Layer:** FastAPI (Uvicorn server)
* **Orchestration Framework:** LangChain / LangChain-Ollama / LangChain-Community
* **Vector Store:** Facebook AI Similarity Search (FAISS)
* **Embedding Model:** sentence-transformers/all-MiniLM-L6-v2 (Local HuggingFace model)
* Local Inference Engine:  Ollama (llama3)
* **Relational Store:** SQLite3

## System Prerequisites

* **Python 3.10** or higher installed on your host system.
* **Ollama** installed and configured locally.

## Installation & Environment Configuration

### Step 1: Environment Files

Create a file named `.env` in the root backend directory to contain localized development configs:

```text
OLLAMA_BASE_URL=http://localhost:11434
FASTAPI_PORT=8000

```

### Step 2: Initialize Ollama

Ensure Ollama is actively running on your local daemon and pull the target Large Language Model model:

```bash
ollama run llama3

```

### Step 3: Install Package Dependencies

Open your choice of terminal, navigate to the backend directory, activate your isolation virtual environment, and install the required modules:

```bash
pip install -r requirements.txt

```

### Step 4: Database Initializer Setup

Run your initialization script to spin up the local SQLite instance and inject dummy structural corporate data:

```bash
python src/database.py

```

## Running the Complete Framework

To boot up the complete framework, run the backend API service alongside the user interface client across distinct terminal lines.

### Terminal Line 1: Ingestion & Vector Build Execution

Process your raw policy and resume documents into mathematical coordinates before querying:

```bash
python src/ingest.py

```

### Terminal Line 2: Boot the FastAPI Core Backend Microservice

```bash
uvicorn src.main:app --port 8000 --reload

```

### Terminal Line 3: Launch the Interactive Streamlit UI Client

```bash
streamlit run src/app.py

```

## End-to-End Operational Workflow

1. **Ingestion Execution:** Log into your Streamlit interface, access the document interface section, and drop a target file (e.g., a technical resume PDF) into the processing pane.
2. **Knowledge Synthesis:** Press "Process & Learn Document". The system executes `rag_engine.py`, reads the data, and outputs a confirmation reading "Unified multi-source vector database successfully built!" onto your FastAPI tracking log.
3. **Contextual Inquiries:** Enter human-readable analytical inquiries directly into the conversational layout box (e.g., "What equipment am I entitled to as a Tier 1 Full-Remote employee?"). The RAG pipeline matches the similarity indices, packages a structured payload prompt context, and returns stylized, bulleted layouts back to the browser panel instantly.
