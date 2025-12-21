from pypdf import PdfReader


def extract_text(pdf_path):
    reader = PdfReader(str(pdf_path))
    pages = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)

    return "\n".join(pages)
