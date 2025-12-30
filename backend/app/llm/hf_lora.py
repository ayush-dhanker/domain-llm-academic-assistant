from dataclasses import dataclass
from typing import Optional

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel


@dataclass
class HFLoRALLM:
    base_model_name: str
    adapter_path: str
    device: Optional[str] = None

    def __post_init__(self):
        adapter_path = str(self.adapter_path)  # ensure string

        # Force local adapter loading
        self.tokenizer = AutoTokenizer.from_pretrained(
            adapter_path,
            use_fast=True,
            local_files_only=True,
        )
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        if self.device is None:
            if torch.cuda.is_available():
                self.device = "cuda"
            elif torch.backends.mps.is_available():
                self.device = "mps"
            else:
                self.device = "cpu"

        dtype = torch.float16 if self.device in (
            "cuda", "mps") else torch.float32

        base = AutoModelForCausalLM.from_pretrained(
            self.base_model_name,
            torch_dtype=dtype,
            device_map="auto" if self.device == "cuda" else None,
        )

        # Force local adapter loading
        self.model = PeftModel.from_pretrained(
            base,
            adapter_path,
            local_files_only=True,
        )

        self.model.eval()
        self.model.config.use_cache = True

        if self.device != "cuda":
            self.model.to(self.device)

    @torch.inference_mode()
    def generate(self, prompt: str, max_new_tokens: int = 120) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        out = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            pad_token_id=self.tokenizer.eos_token_id,
            eos_token_id=self.tokenizer.eos_token_id,
        )
        return self.tokenizer.decode(out[0], skip_special_tokens=True)
