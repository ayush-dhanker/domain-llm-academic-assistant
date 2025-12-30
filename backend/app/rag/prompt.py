# SYSTEM_PROMPT = """
# You are an academic regulations assistant.

# YOUR TASK:
# Answer the question using ONLY the information explicitly stated in the provided context.

# MANDATORY RULES:
# 1. You MUST NOT use any knowledge outside the provided context.
# 2. You MUST NOT infer, assume, interpret, or imply information.
# 3. You MAY state numbers, limits, or permissions ONLY IF they appear explicitly
#    and verbatim in the provided text.
# 4. If the context explicitly states a number or rule, quote it accurately.
# 5. If the context does NOT explicitly state the requested information, you MUST say:
#    "The regulations do not explicitly specify this."
# 6. If multiple sections are provided, treat each section independently.
#    Do NOT combine sections into conclusions or totals.
# 7. You MUST cite the relevant section (§) and paragraph for every statement.

# FORBIDDEN BEHAVIOR:
# - No speculation
# - No assumptions
# - No implications
# - No advice
# - No summarization beyond the text
# - Do NOT use words such as:
#   "implied", "assumed", "might", "could", "therefore", "however", "overall"

# RESPONSE STYLE:
# - Formal
# - Precise
# - Regulation-faithful

# OUTPUT FORMAT:
# - Each statement must be on its own line.
# - Each line must begin with:
#   "According to §X (Y), it states that ..."
# - Include ONLY information that directly answers the question.
# """


# def build_prompt(question: str, retrieved_chunks: list) -> str:
#     # Sort by relevance
#     retrieved_chunks = sorted(
#         retrieved_chunks,
#         key=lambda r: r.get("score", 0),
#         reverse=True
#     )

#     context_blocks = []

#     for r in retrieved_chunks:
#         meta = r["metadata"]

#         header = f"[Source: {meta.get('section', meta.get('module_name', 'Unknown'))}"
#         if "paragraph" in meta:
#             header += f" {meta['paragraph']}"
#         header += "]"

#         context_blocks.append(
#             f"{header}\n--- BEGIN SOURCE TEXT ---\n{r['content']}\n--- END SOURCE TEXT ---"
#         )

#     context = "\n\n".join(context_blocks)

#     return f"""{SYSTEM_PROMPT}

# Context:
# {context}

# Question:
# {question}

# Answer (use only the text above):
# """

# --above in before stage---
# after fine tuning---
def build_prompt(question: str, retrieved_chunks: list) -> str:
    context_blocks = []
    for r in sorted(retrieved_chunks, key=lambda x: x.get("score", 0), reverse=True):
        meta = r.get("metadata", {}) or {}
        section = meta.get("section") or meta.get("module_name") or "Unknown"
        paragraph = meta.get("paragraph")
        header = f"[Source: {section}" + \
            (f" {paragraph}]" if paragraph else "]")
        context_blocks.append(f"{header}\n{r.get('content','')}".strip())

    context = "\n\n".join(context_blocks)

    SYSTEM_PROMPT = (
        "You are an academic regulations assistant.\n"
        "RULES:\n"
        "- Answer ONLY using the provided context.\n"
        "- Do NOT infer, assume, or add information.\n"
        "- If the context does not explicitly specify the answer, say: "
        "\"The regulations do not explicitly specify this.\""
    )

    return f"""<s>[SYSTEM]
{SYSTEM_PROMPT}
[/SYSTEM]
[USER]
Context:
{context}

Question:
{question}
[/USER]
[ASSISTANT]
"""
