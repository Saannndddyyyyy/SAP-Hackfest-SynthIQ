import random
import numpy as np
import pandas as pd

FIRST_NAMES = [
    "Arjun", "Meera", "Rahul", "Ananya", "Vikram",
    "Priya", "Karan", "Ishita", "Rohan", "Sneha",
    "Aditya", "Nisha", "Kabir", "Diya", "Aman",
    "Sara", "Dev", "Tanya", "Neil", "Aisha"
]

TRAITS = [
    "Price Sensitive",
    "Brand Loyal",
    "Impulse Buyer",
    "Research-Oriented",
    "Emotion-Driven",
    "Digital Native",
    "Value Seeker",
    "Trend Conscious",
    "Risk Averse",
    "Premium Aspirational"
]

def generate_personas(product_context, n_personas=30):

    personas = []

    for i in range(n_personas):

        age = random.randint(18, 60)
        income = random.randint(20000, 150000)
        trait = random.choice(TRAITS)
        name = random.choice(FIRST_NAMES) + " " + random.choice(["Sharma","Iyer","Khan","Das","Mehta"])

        purchase_prob = round(np.clip(np.random.normal(0.5, 0.2), 0, 1), 2)

        reaction = simulate_reaction(trait, purchase_prob, product_context)

        personas.append({
            "Name": name,
            "Age": age,
            "Income": income,
            "Dominant Trait": trait,
            "Purchase Probability": purchase_prob,
            "Reaction Summary": reaction
        })

    return pd.DataFrame(personas)


def simulate_reaction(trait, purchase_prob, context):

    if purchase_prob > 0.7:
        sentiment = "Highly Interested"
    elif purchase_prob > 0.4:
        sentiment = "Moderately Interested"
    else:
        sentiment = "Low Interest"

    return f"{sentiment}. Responds as a {trait} consumer towards {context}."