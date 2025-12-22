from app.ingestion.pdf_loader import extract_text
from app.ingestion.spo_parser import (
    parse_spo,
    chunk_spo_section,
    strip_spo_toc,
)
from app.ingestion.module_parser import (
    parse_modules,
    chunk_module,
    strip_module_toc,
)
from app.ingestion.chunk_writer import write_chunks
from app.utils import project_path

MAX_WORDS = 400


def run():
    all_chunks = []

    # ---------- SPO ----------
    spo_path = project_path(
        "data", "raw_pdfs", "SPO_Master_2021_04_08_Courtesy_Translation.pdf"
    )
    spo_text = extract_text(spo_path)
    spo_text = strip_spo_toc(spo_text)
    spo_sections = parse_spo(spo_text)

    for section in spo_sections:
        for chunk in chunk_spo_section(section):
            if not chunk["content"].strip():
                continue
            if len(chunk["content"].split()) > MAX_WORDS:  # ✅ FIX 3
                continue
            all_chunks.append(chunk)

    # ---------- MODULE CATALOG ----------
    module_path = project_path(
        "data", "raw_pdfs", "Modulkatalog_2024_Sommersemester.pdf"
    )
    module_text = extract_text(module_path)
    module_text = strip_module_toc(module_text)
    modules = parse_modules(module_text)

    for module in modules:
        chunk = chunk_module(module)
        if not chunk["content"].strip():
            continue
        if len(chunk["content"].split()) > MAX_WORDS:      # ✅ FIX 3
            continue
        all_chunks.append(chunk)

    output_path = project_path("data", "processed", "chunks.jsonl")
    write_chunks(all_chunks, output_path)


if __name__ == "__main__":
    run()
