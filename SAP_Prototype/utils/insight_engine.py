def generate_insights(df):

    acceptance_rate = (df["Purchase Probability"] > 0.6).mean() * 100
    avg_income = df["Income"].mean()
    top_trait = df["Dominant Trait"].value_counts().idxmax()

    insights = f"""
Market Simulation Summary:

• Estimated Acceptance Rate: {round(acceptance_rate,1)}%
• Average Income of Simulated Group: {round(avg_income)}
• Dominant Consumer Archetype: {top_trait}

Strategic Recommendation:
Focus messaging around the dominant archetype while optimizing pricing sensitivity levers.
"""

    return insights