import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import streamlit as st
from peft import PeftModel  # if you plan to add LoRA fine-tuning

MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"

@st.cache_resource
def load_model():
    """
    Load a 4-bit quantized Mistral instruct-tuned model for local generation.
    Supports GPU if available.
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.pad_token = tokenizer.eos_token

    # Load 4-bit quantized model
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        device_map="auto" if device=="cuda" else None,
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True
    )

    model.eval()
    return tokenizer, model, device

def generate_response(prompt, tokenizer, model, device, max_tokens=250):
    """
    Generates human-like persona response.
    """
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=0.85,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)