import numpy as np

def synthesize_intelligence(responses):

    positive = sum(["buy" in r.lower() for r in responses])
    acceptance_rate = positive / len(responses) * 100

    summary = f"""
AI Market Intelligence Summary

• Simulated Participants: {len(responses)}
• Estimated Purchase Acceptance: {round(acceptance_rate,1)}%

Strategic Insight:
Acceptance below 40% indicates repositioning required.
Above 65% suggests strong product-market fit.
"""

    return summary