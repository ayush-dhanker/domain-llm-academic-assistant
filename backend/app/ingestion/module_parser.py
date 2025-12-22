# parsing module catalog
import re
from typing import List, Dict

MODULE_PATTERN = re.compile(
    r"(Module\s+Name\s*:\s*.+)"
)


def parse_modules(text: str) -> List[Dict]:

    matches = list(MODULE_PATTERN.finditer(text))
    modules = []

    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

        module_block = text[start:end].strip()
        module_name = match.group().replace("Module Name:", "").strip()

        modules.append({
            "module_name": module_name,
            "body": module_block
        })

    return modules


# removes table
def strip_module_toc(text: str) -> str:

    marker = "Modulbezeichnung:"
    idx = text.find(marker)
    if idx == -1:
        raise ValueError("Could not find start of module catalog body")
    return text[idx:]


def chunk_module(module):
    fields = module["body"].split("\n\n")
    chunks = []

    for field in fields:
        field = field.strip()
        if not field:
            continue

        chunks.append({
            "content": field,
            "metadata": {
                "doc_type": "ModuleCatalog",
                "module_name": module["module_name"],
            }
        })

    return chunks
