# import re
# from app.rag.retriever import Retriever
# from app.rag.prompt import build_prompt


# NUMBER_PATTERN = re.compile(r"\b(one|two|three|\d+)\b", re.IGNORECASE)


# class RAGPipeline:
#     def __init__(self, llm):
#         self.retriever = Retriever()
#         self.llm = llm

#     def _has_explicit_number(self, retrieved_chunks):
#         for r in retrieved_chunks:
#             if NUMBER_PATTERN.search(r["content"]):
#                 return True
#         return False

#     def answer(self, question: str):
#         retrieved = self.retriever.retrieve(question)

#         # ✅ FACT GATE
#         has_explicit_fact = self._has_explicit_number(retrieved)

#         prompt = build_prompt(question, retrieved)
#         response = self.llm.generate(prompt)

#         if not has_explicit_fact:
#             response = (
#                 "The regulations do not explicitly specify this."
#             )

#         return {
#             "answer": response,
#             "sources": [r["metadata"] for r in retrieved],
#         }
# ---after fine tune---
import re
from app.rag.retriever import Retriever
from app.rag.prompt import build_prompt

POLICY_SIGNAL = re.compile(
    r"\b(must|shall|may|is permitted|is not permitted|requires|required|deadline|within|no later than|at most)\b",
    re.IGNORECASE,
)

NUMBER_SIGNAL = re.compile(r"\b(one|two|three|four|five|\d+)\b", re.IGNORECASE)


class RAGPipeline:
    def __init__(self, llm, retriever=None):
        self.retriever = retriever or Retriever()
        self.llm = llm

    def _concat_context(self, retrieved_chunks) -> str:
        return "\n".join([(r.get("content") or "") for r in retrieved_chunks])

    def _is_answerable(self, question: str, retrieved_chunks) -> bool:
        """
        Better gate than 'number only':
        - If no meaningful context -> not answerable
        - If question asks 'how many / number / times' -> require number in context
        - Otherwise require policy-like language in context
        """
        context = self._concat_context(retrieved_chunks).strip()
        if len(context) < 40:
            return False

        q = question.lower()
        asks_for_number = any(
            w in q for w in ["how many", "number", "times", "maximum", "at most"])

        if asks_for_number:
            return bool(NUMBER_SIGNAL.search(context))

        return bool(POLICY_SIGNAL.search(context))

    def answer(self, question: str, top_k: int = 4):
        retrieved = self.retriever.retrieve(question, top_k=top_k)

        
        if not self._is_answerable(question, retrieved):
            return {
                "answer": "The regulations do not explicitly specify this.",
                "sources": [r.get("metadata", {}) for r in retrieved],
            }

        prompt = build_prompt(question, retrieved)

        full_text = self.llm.generate(prompt, max_new_tokens=180)

  
        response = full_text.split("[ASSISTANT]")[-1].strip()

        if not response:
            response = "The regulations do not explicitly specify this."

        return {
            "answer": response,
            "sources": [r.get("metadata", {}) for r in retrieved],
        }
