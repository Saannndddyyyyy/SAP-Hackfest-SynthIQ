# population_model.py

import random

FIRST_NAMES = ["Tanya", "Keshav", "Gopi", "Aditi", "Rohan", "Neha", "Vikram", "Priya", "Arjun", "Sanya"]
LAST_NAMES = ["Sharma", "Singh", "Pramod", "Mehra", "Gupta", "Kapoor", "Reddy", "Patel"]

def generate_realistic_persona():
    """
    Generates a single human-like persona with realistic demographics and Big Five traits.
    """
    name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    age = random.randint(20, 65)  # realistic adult range
    income = random.randint(15000, 100000)  # monthly income in INR

    # Big Five: realistic ranges, rounded to 2 decimals
    big_five = {
        'Openness': round(random.uniform(0.4, 0.9), 2),
        'Conscientiousness': round(random.uniform(0.3, 0.9), 2),
        'Extraversion': round(random.uniform(0.2, 0.9), 2),
        'Agreeableness': round(random.uniform(0.3, 0.9), 2),
        'Neuroticism': round(random.uniform(0.2, 0.8), 2)
    }

    return {"name": name, "age": age, "income": income, "big_five": big_five}

def generate_population(n_agents=15):
    """
    Generates a list of n_agents human-like personas.
    """
    return [generate_realistic_persona() for _ in range(n_agents)]