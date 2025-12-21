import re
from typing import List, Dict

SECTION_PATTERN = re.compile(
    r"(§\s*\d+\s+[A-Za-z].+?)\n"
)

PARA_PATTERN = re.compile(
    r"\(\d+\)"
)


def strip_spo_toc(text: str) -> str:
    """
    Removes table of contents by cutting everything
    before the first real § section with body text.
    """
    marker = "§ 1"
    idx = text.find(marker)
    if idx == -1:
        raise ValueError("Could not find start of SPO body")
    return text[idx:]


def parse_spo(text: str) -> List[Dict]:

    matches = list(SECTION_PATTERN.finditer(text))
    sections = []

    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

        section_title = match.group().strip()
        section_body = text[start:end].replace(section_title, "").strip()

        sections.append({
            "section": section_title,
            "body": section_body
        })

    return sections


def chunk_spo_section(section):
    parts = PARA_PATTERN.split(section["body"])
    paras = PARA_PATTERN.findall(section["body"])

    chunks = []

    for i, text in enumerate(parts):
        text = text.strip()
        if not text:
            continue

        para_id = paras[i - 1] if i > 0 else None

        chunks.append({
            "content": text,
            "metadata": {
                "doc_type": "SPO",
                "section": section["section"],
                "paragraph": para_id,
            }
        })

    return chunks
