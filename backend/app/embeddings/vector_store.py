import faiss


class VectorStore:
    def __init__(self, dim: int):
        self.index = faiss.IndexFlatIP(dim)
        self.documents = []

    def add(self, embeddings, documents):
        self.index.add(embeddings)
        self.documents.extend(documents)

    def search(self, query_embedding, top_k=5):
        scores, indices = self.index.search(
            query_embedding.reshape(1, -1), top_k
        )

        results = []
        for score, idx in zip(scores[0], indices[0]):
            doc = self.documents[idx]
            results.append({
                "score": float(score),
                "content": doc["content"],
                "metadata": doc["metadata"],
            })

        return results
