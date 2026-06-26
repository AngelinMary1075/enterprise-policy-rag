# src/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
import os

app = FastAPI(title="Enterprise Policy Intelligence Core API")

FAISS_DIR = "faiss_index"
if not os.path.exists(FAISS_DIR):
    raise RuntimeError("Physical FAISS index mapping missing. Execute src/ingest.py pipeline first.")

# Single instantiation cache for internal memory footprint reduction
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = FAISS.load_local(FAISS_DIR, embeddings, allow_dangerous_deserialization=True)
llm = Ollama(model="llama3", base_url="http://localhost:11434")

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_rag_engine(request: QueryRequest):
    try:
        # Step A: Perform semantic similarity index search
        docs = vector_store.similarity_search(request.question, k=3)
        
        # Step B: Construct analytical payloads and citations
        context_blocks = []
        citations = []
        for doc in docs:
            source = doc.metadata.get('source', 'Unknown File')
            owner = doc.metadata.get('owner', 'Unknown Operations')
            context_blocks.append(f"[Document: {os.path.basename(source)} | Governance: {owner}]\nContent: {doc.page_content}")
            citations.append({
                "source": os.path.basename(source),
                "page": doc.metadata.get('page', 0) + 1,
                "owner": owner,
                "effective_date": doc.metadata.get('effective_date', 'N/A')
            })
        
        context_str = "\n\n".join(context_blocks)
        
        # Step C: Prompt Engineering framing with corporate boundary constraints
        prompt = f"""You are an authoritative Enterprise Policy Intelligence Assistant. 
Answer the employee query explicitly utilizing only the verified organizational context provided below. 
If the text context does not explicitly yield facts to address the answer, strictly reply: 
"I am unable to verify that statement within current official company documentation." Do not generate external assumptions.

Context Reference Materials:
{context_str}

Employee Query: {request.question}
Authoritative Corporate Response:"""

        response = llm.invoke(prompt)
        
        return {
            "answer": response,
            "citations": citations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)