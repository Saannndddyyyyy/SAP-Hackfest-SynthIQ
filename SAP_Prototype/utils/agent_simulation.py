import requests
import streamlit as st

def simulate_agent_response_local(persona, context):

    prompt = f"""
You are a consumer with:
Age: {persona['age']}
Income: {persona['income']}
Traits: {persona['big_five']}

Product Context:
{context}

Respond naturally in human style:
- Emotional reaction
- Likes
- Concerns
- Purchase likelihood
"""

    HF_TOKEN = st.secrets["HF_TOKEN"]
    API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": prompt}

    res = requests.post(API_URL, json=payload, headers=headers)
    return res.json()[0]["generated_text"]