from app.rag.pipeline import RAGPipeline
from app.llm.hf_lora import HFLoRALLM
from app.utils import project_path


def main():
    BASE_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    # ADAPTER_PATH = project_path("finetuning", "regulations-lora-adapter")
    ADAPTER_PATH = project_path(
        "data", "finetuning", "regulations-lora-adapter")

    print("Adapter path:", ADAPTER_PATH)
    print("Adapter exists:", ADAPTER_PATH.exists())

    llm = HFLoRALLM(
        base_model_name=BASE_MODEL,
        adapter_path=str(ADAPTER_PATH),
        device="mps",
    )

    rag = RAGPipeline(llm)

    q = "What is the standard duration of the Master’s program?"
    result = rag.answer(q)

    print("\nQUESTION:", q)
    print("\nANSWER:\n", result["answer"])
    print("\nSOURCES:")
    for s in result["sources"]:
        print("-", s)


if __name__ == "__main__":
    main()
