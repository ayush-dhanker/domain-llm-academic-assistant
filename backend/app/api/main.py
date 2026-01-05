import time
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.api.schemas import QueryRequest, QueryResponse
from app.api.deps import get_rag
from app.api.logging_config import setup_logging

from dotenv import load_dotenv
load_dotenv()

setup_logging()
log = logging.getLogger("api")

app = FastAPI(title="Academic Regulations Assistant API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
def ready():
    try:
        _ = get_rag()
        return {"status": "ready"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


@app.post("/query", response_model=QueryResponse)
def query(payload: QueryRequest):
    start = time.time()
    try:
        rag = get_rag()

        if payload.top_k is None:
            result = rag.answer(payload.question)
        else:
            try:
                result = rag.answer(payload.question, top_k=payload.top_k)
            except TypeError:
                result = rag.answer(payload.question)

        answer = (result.get("answer") or "").strip()
        sources = result.get("sources") or []

        elapsed = time.time() - start
        log.info(
            f"Query handled in {elapsed:.2f}s | q='{payload.question[:60]}'")

        return {"answer": answer, "sources": sources}

    except Exception as e:
        log.exception("Query failed")
        raise HTTPException(status_code=500, detail=str(e))
