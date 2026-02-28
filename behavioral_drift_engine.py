import pandas as pd
import numpy as np
import os
import random

# ─────────────────────────────────────────────────────────────
# 1. BASELINE STATIC PERSONAS
# ─────────────────────────────────────────────────────────────

CLUSTER_PERSONAS = pd.DataFrame({
    "Cluster": ["C1", "C2", "C3", "C4", "C5"],
    "Label": [
        "Conservative Low-Income",
        "Young Mid-Spender",
        "Affluent High-Spender",
        "Cautious Saver",
        "Premium Power-Buyer"
    ],
    "Income": [28000, 52000, 88000, 45000, 130000],
    "TotalSpent": [210, 780, 1850, 430, 2950],
    "Age": [55, 32, 44, 48, 39],
    "risk_tolerance": [0.20, 0.55, 0.70, 0.35, 0.85],
    "spending_propensity": [0.25, 0.60, 0.75, 0.40, 0.90],
    "default_prob": [0.18, 0.10, 0.05, 0.12, 0.03]
})

SENSITIVITY = {
    "C1": dict(alpha=0.030, beta=0.025, gamma=0.020),
    "C2": dict(alpha=0.020, beta=0.018, gamma=0.015),
    "C3": dict(alpha=0.012, beta=0.010, gamma=0.008),
    "C4": dict(alpha=0.022, beta=0.020, gamma=0.017),
    "C5": dict(alpha=0.008, beta=0.007, gamma=0.005),
}

# ─────────────────────────────────────────────────────────────
# 2. SHOCK DEFINITIONS
# ─────────────────────────────────────────────────────────────

PERSONAL_SHOCKS = {
    "Career Setback": (-0.15, -0.20, +0.10),
    "Health Crisis": (-0.10, -0.30, +0.15),
    "Family Transition": (+0.05, +0.10, -0.02),
    "Major Windfall": (+0.20, +0.25, -0.05),
    "Digital Fatigue": (-0.05, -0.10, 0.00),
    "Social Influence (FOMO)": (+0.10, +0.20, +0.05),
    "Ethical Awakening": (0.00, -0.15, 0.00),
    "Educational Achievement": (+0.15, +0.10, -0.05),
    "Relocation": (-0.05, -0.05, +0.02),
    "Relationship Change": (-0.10, -0.10, +0.08)
}

PRODUCT_SETBACKS = {
    "Price Hike": (0.00, -0.25, 0.00),
    "Feature Obsolescence": (-0.10, -0.15, 0.00),
    "Service Instability": (-0.20, -0.10, 0.00),
    "Support Friction": (-0.15, -0.05, 0.00)
}

# ─────────────────────────────────────────────────────────────
# 3. CORE ENGINE
# ─────────────────────────────────────────────────────────────

def calculate_fsi(inflation, interest_rate, unemployment, gdp_growth):
    raw_fsi = (0.4 * inflation) + (0.3 * interest_rate) + (0.3 * unemployment)
    gdp_bonus = max(0, gdp_growth - 6.0)
    dampening = 1 - (0.015 * gdp_bonus)
    return raw_fsi * dampening

def predict_purchase_probability(income, total_spent, risk_tolerance, fsi):
    raw_score = (0.25 * (income / 130000) * 100) + \
                (0.35 * (total_spent / 2950) * 100) + \
                (0.30 * risk_tolerance * 100) - \
                (0.10 * (fsi / 10.0) * 100)
    return round(float(np.clip(100 / (1 + np.exp(-0.07 * (raw_score - 50))), 0, 100)), 2)

def run_simulation(macro_signals=None, manual_product_setback=None, num_samples=10):
    """
    Runs simulation where:
    - Macro (FSI) is Manual (via macro_signals)
    - Product Setback is Manual (via manual_product_setback)
    - Personal Shocks are Random
    """
    fsi = 0
    if macro_signals:
        fsi = calculate_fsi(macro_signals["inflation"], macro_signals["interest_rate"], 
                            macro_signals["unemployment"], macro_signals["gdp_growth"])
    
    ps_r, ps_s, ps_d = (0, 0, 0)
    if manual_product_setback and manual_product_setback in PRODUCT_SETBACKS:
        ps_r, ps_s, ps_d = PRODUCT_SETBACKS[manual_product_setback]

    all_results = []
    for _, persona in CLUSTER_PERSONAS.iterrows():
        cluster = persona["Cluster"]
        coeffs = SENSITIVITY[cluster]
        
        for i in range(num_samples):
            # Baseline + Macro + Manual Product Setback
            r = persona["risk_tolerance"] - (coeffs["alpha"] * fsi) + ps_r
            s = persona["spending_propensity"] - (coeffs["beta"] * fsi) + ps_s
            d = persona["default_prob"] + (coeffs["gamma"] * fsi) + ps_d
            
            # Random Personal Shock
            shock_name = "None"
            if random.random() < 0.3: # 30% chance
                shock_name = random.choice(list(PERSONAL_SHOCKS.keys()))
                r_i, s_i, d_i = PERSONAL_SHOCKS[shock_name]
                r += r_i; s += s_i; d += d_i
            
            r, s, d = np.clip([r, s, d], 0.0, 1.0)
            
            prob_before = predict_purchase_probability(persona["Income"], persona["TotalSpent"], persona["risk_tolerance"], 0)
            prob_after = predict_purchase_probability(persona["Income"], persona["TotalSpent"], r, fsi)
            
            all_results.append({
                "Sample_ID": f"{cluster}_{i}",
                "Cluster": cluster,
                "Macro_FSI": round(fsi, 2),
                "Product_Setback": manual_product_setback if manual_product_setback else "None",
                "Personal_Shock": shock_name,
                "Prob_Before (%)": prob_before,
                "Prob_After (%)": prob_after,
                "Delta": round(prob_after - prob_before, 2)
            })
            
    return pd.DataFrame(all_results)

if __name__ == "__main__":
    # Example: Manually trigger Macro Stress AND a Product Price Hike
    MACRO_STATE = {"inflation": 4.0, "interest_rate": 6.0, "unemployment": 5.5, "gdp_growth": 5.0}
    PRODUCT_ISSUE = "Price Hike"
    
    print(f"\n[Trigger] Macro Stress (Manual): {MACRO_STATE}")
    print(f"[Trigger] Product Setback (Manual): {PRODUCT_ISSUE}")
    print(f"[Engine] Randomizing Personal Shocks per individual...")
    
    df = run_simulation(macro_signals=MACRO_STATE, manual_product_setback=PRODUCT_ISSUE, num_samples=5)
    
    print("\n=== SAMPLE RESULTS (First 10) ===")
    print(df.head(10)[["Sample_ID", "Personal_Shock", "Prob_After (%)", "Delta"]].to_string(index=False))
    
    summary = df.groupby("Cluster")["Delta"].mean().round(2)
    print("\n=== AVERAGE DRIFT PER CLUSTER ===")
    print(summary)
