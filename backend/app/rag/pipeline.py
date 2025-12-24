import re
from app.rag.retriever import Retriever
from app.rag.prompt import build_prompt


NUMBER_PATTERN = re.compile(r"\b(one|two|three|\d+)\b", re.IGNORECASE)


class RAGPipeline:
    def __init__(self, llm):
        self.retriever = Retriever()
        self.llm = llm

    def _has_explicit_number(self, retrieved_chunks):
        for r in retrieved_chunks:
            if NUMBER_PATTERN.search(r["content"]):
                return True
        return False

    def answer(self, question: str):
        retrieved = self.retriever.retrieve(question)

        # ✅ FACT GATE
        has_explicit_fact = self._has_explicit_number(retrieved)

        prompt = build_prompt(question, retrieved)
        response = self.llm.generate(prompt)

        if not has_explicit_fact:
            response = (
                "The regulations do not explicitly specify this."
            )

        return {
            "answer": response,
            "sources": [r["metadata"] for r in retrieved],
        }
