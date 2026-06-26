# src/ingest.py
import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from database import get_metadata, init_db

DATA_DIR = "data/raw_pdfs"
FAISS_DIR = "faiss_index"

def build_vector_store():
    init_db() 
    
    if not os.path.exists(DATA_DIR) or not os.listdir(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
        print(f"Please add template PDF files to '{DATA_DIR}' and re-run ingestion.")
        return

    print("Parsing raw enterprise PDFs...")
    loader = PyPDFDirectoryLoader(DATA_DIR)
    documents = loader.load()
    
    print("Enriching document chunks with SQL metadata tags...")
    for doc in documents:
        filename = os.path.basename(doc.metadata.get('source', ''))
        meta = get_metadata(filename)
        doc.metadata.update(meta) # Hybrid integration: merging metadata payload

    print("Splitting text into semantic sub-chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    chunks = text_splitter.split_documents(documents)

    print("Generating local text embeddings (all-MiniLM-L6-v2)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    print("Building and saving local FAISS physical matrix...")
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(FAISS_DIR)
    print(f"Success! FAISS indices securely persisted to '{FAISS_DIR}'")

if __name__ == "__main__":
    build_vector_store()