import faiss
import numpy as np


class VectorStore:
    def __init__(self, dim: int):
        self.index = faiss.IndexFlatIP(dim)
        self.metadata = []

    def add(self, embeddings: np.ndarray, metadatas: list):
        self.index.add(embeddings)
        self.metadata.extend(metadatas)

    def search(self, query_embedding, top_k=5):
        scores, indices = self.index.search(
            query_embedding.reshape(1, -1), top_k
        )

        results = []
        for score, idx in zip(scores[0], indices[0]):
            results.append({
                "score": float(score),
                "metadata": self.metadata[idx],
            })

        return results
