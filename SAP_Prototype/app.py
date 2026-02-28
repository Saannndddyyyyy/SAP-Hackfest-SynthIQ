import streamlit as st
import re
import pandas as pd
import altair as alt
from utils.population_model import generate_population
from utils.local_llm_engine import load_model, generate_response

st.set_page_config(layout="wide")
st.title("🧠 GPU Synthetic Market Intelligence Lab")

# -------------------------
# Inputs
# -------------------------
product_context = st.text_area(
    "Describe your product & marketing visual",
    height=200
)

n_agents = st.slider("Number of Participants", 5, 30, 15)

# -------------------------
# Load Model Once
# -------------------------
tokenizer, model, device = load_model()  # cached, loaded only once per session

# -------------------------
# Run Simulation
# -------------------------
if st.button("Run Focus Group Simulation"):

    personas = generate_population(n_agents)

    responses = []
    purchase_scores = []

    progress = st.progress(0)
    progress_text = st.empty()

    for i, persona in enumerate(personas):

        progress_text.text(f"Processing {persona['name']} ({i+1}/{n_agents})")

        # -------------------------
        # Clean, human-like prompt
        # -------------------------
        prompt = f"""
        You are {persona['name']}, a {persona['age']}-year-old consumer with a monthly income of {persona['income']} INR.
        Your personality traits are:
        Openness: {persona['big_five']['Openness']}, 
        Conscientiousness: {persona['big_five']['Conscientiousness']}, 
        Extraversion: {persona['big_five']['Extraversion']}, 
        Agreeableness: {persona['big_five']['Agreeableness']}, 
        Neuroticism: {persona['big_five']['Neuroticism']}.

        You are evaluating this product:
        {product_context}

        Respond naturally as this persona, expressing:
        - Your emotions about the product
        - What you like about it
        - Any concerns or hesitations
        - Whether you would buy it

        Write in a conversational, human-like style.
        End your response with "Purchase Likelihood: XX%".
        """


        # -------------------------
        # Generate response
        # -------------------------
        response = generate_response(prompt, tokenizer, model, device)
        responses.append((persona["name"], response))

        # Extract Purchase Likelihood
        match = re.search(r'(\d+)\s*%', response)
        if match:
            purchase_scores.append(int(match.group(1)))
        else:
            purchase_scores.append(0)

        progress.progress((i+1)/n_agents)

    st.success("Simulation Complete")

    # -------------------------
    # Metrics
    # -------------------------
    avg_score = sum(purchase_scores) / len(purchase_scores)

    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Purchase Likelihood", f"{round(avg_score,1)}%")
    col2.metric("High Intent (>70%)", sum([x > 70 for x in purchase_scores]))
    col3.metric("Low Intent (<40%)", sum([x < 40 for x in purchase_scores]))

    # -------------------------
    # Participant Verbatims
    # -------------------------
    st.subheader("🗣 Participant Verbatims")
    for name, r in responses:
        with st.expander(f"{name} – Product Context"):
            st.write("**Product Description:**")
            st.write(product_context)
            st.write("**Response:**")
            st.write(r)

    # -------------------------
    # Visualize Purchase Likelihood
    # -------------------------
    st.subheader("📊 Purchase Likelihood Distribution")
    df = pd.DataFrame({
        "Name": [p['name'] for p in personas],
        "Purchase Likelihood": purchase_scores
    })

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Name', sort=None),
        y='Purchase Likelihood',
        color=alt.condition(
            alt.datum['Purchase Likelihood'] > 70,
            alt.value('green'),
            alt.value('red')
        )
    )

    st.altair_chart(chart, use_container_width=True)