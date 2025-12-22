from sentence_transformers import SentenceTransformer


class Embedder:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_texts(self, texts):
        return self.model.encode(
            texts,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

    def embed_query(self, query: str):
        return self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )[0]
