import os
import logging
from functools import lru_cache
from pathlib import Path

from app.utils import project_path
from app.llm.hf_lora import HFLoRALLM
from app.rag.pipeline import RAGPipeline

log = logging.getLogger("deps")


@lru_cache(maxsize=1)
def get_rag() -> RAGPipeline:
    base_model = os.getenv("BASE_MODEL", "TinyLlama/TinyLlama-1.1B-Chat-v1.0")

    adapter_path = os.getenv(
        "ADAPTER_PATH",
        str(project_path("data", "finetuning", "regulations-lora-adapter")),
    )

    device = os.getenv("LLM_DEVICE", "mps")

    # Validate adapter folder exists
    ap = Path(adapter_path)
    if not ap.exists():
        raise RuntimeError(f"Adapter path not found: {adapter_path}")

    log.info(
        f"Loading LLM base={base_model} adapter={adapter_path} device={device}")

    llm = HFLoRALLM(
        base_model_name=base_model,
        adapter_path=adapter_path,
        device=device,
    )

    rag = RAGPipeline(llm)
    log.info("RAG pipeline ready.")
    return rag
