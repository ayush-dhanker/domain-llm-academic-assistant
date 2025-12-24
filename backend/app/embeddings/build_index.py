import json
from app.embeddings.embedder import Embedder
from app.embeddings.vector_store import VectorStore
from app.utils import project_path
import pickle


def load_chunks():
    path = project_path("data", "processed", "chunks.jsonl")
    chunks = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            chunks.append(json.loads(line))

    return chunks


def build():
    chunks = load_chunks()
    texts = [c["content"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]

    embedder = Embedder()
    embeddings = embedder.embed_texts(texts)

    store = VectorStore(dim=embeddings.shape[1])
    # store.add(embeddings, metadatas)
    store.add(embeddings, chunks)

    out_path = project_path("data", "vector_store", "faiss_store.pkl")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "wb") as f:
        pickle.dump(store, f)


if __name__ == "__main__":
    build()
