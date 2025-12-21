# import json
# from typing import List,Dict
# def write_chunks(chunks:List[Dict],output_path:str):
#     with open(output_path,'w',encoding="utf-8") as f:
#         for chunk in chunks:
#             f.write(json.dumps(chunk,ensure_ascii=False)+"\n")
from pathlib import Path
import json


def write_chunks(chunks, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
