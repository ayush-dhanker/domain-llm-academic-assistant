# import pickle
# from app.utils import project_path
# from app.embeddings.embedder import Embedder


# class Retriever:
#     def __init__(self, top_k=3):
#         with open(project_path("data", "vector_store", "faiss_store.pkl"), "rb") as f:
#             self.store = pickle.load(f)
#         self.embedder = Embedder()
#         self.top_k = top_k

#     def retrieve(self, query: str):
#         query_embedding = self.embedder.embed_query(query)
#         results = self.store.search(query_embedding, top_k=self.top_k)
#         return results
import pickle
from app.utils import project_path
from app.embeddings.embedder import Embedder


class Retriever:
    def __init__(self, top_k=3):
        with open(project_path("data", "vector_store", "faiss_store.pkl"), "rb") as f:
            self.store = pickle.load(f)
        self.embedder = Embedder()
        self.top_k = top_k

    def retrieve(self, query: str, top_k: int = None):
        query_embedding = self.embedder.embed_query(query)
        k = top_k if top_k is not None else self.top_k
        results = self.store.search(query_embedding, top_k=k)
        return results
