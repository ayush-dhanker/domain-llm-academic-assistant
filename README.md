# domain-llm-academic-assistant
A domain-specific LLM assistant that answers official academic & examination regulation questions accurately using fine-tuning + RAG.

Model

Base LLM: TinyLlama/TinyLlama-1.1B-Chat-v1.0

Fine-tune: LoRA adapter trained on OVGU regulations (data/finetuning/regulations-lora-adapter)

Inference: local (MPS on Mac / CPU fallback)

RAG

Vector store: FAISS pickle (data/vector_store/faiss_store.pkl)

Retriever: sentence-transformer embeddings

Response: answer + source metadata