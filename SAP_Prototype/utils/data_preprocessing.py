import pandas as pd
from datetime import datetime


def load_and_engineer_features(filepath):

    df = pd.read_excel(filepath)

    # -----------------------------
    # Basic Cleaning
    # -----------------------------
    df = df.drop_duplicates()
    df = df.dropna(subset=["Income"])
    df = df.drop(columns=["Z_CostContact", "Z_Revenue", "ID"], errors="ignore")

    # -----------------------------
    # Feature Engineering
    # -----------------------------

    current_year = datetime.now().year
    df["Age"] = current_year - df["Year_Birth"]

    spend_cols = [
        "MntWines", "MntFruits", "MntMeatProducts",
        "MntFishProducts", "MntSweetProducts", "MntGoldProds"
    ]
    df["Total_Spend"] = df[spend_cols].sum(axis=1)

    purchase_cols = [
        "NumWebPurchases",
        "NumCatalogPurchases",
        "NumStorePurchases"
    ]
    df["Total_Purchases"] = df[purchase_cols].sum(axis=1)

    df["Web_Purchase_Ratio"] = (
        df["NumWebPurchases"] / (df["Total_Purchases"] + 1)
    )

    campaign_cols = [
        "AcceptedCmp1", "AcceptedCmp2", "AcceptedCmp3",
        "AcceptedCmp4", "AcceptedCmp5", "Response"
    ]
    df["Campaign_Response_Score"] = df[campaign_cols].sum(axis=1)

    df["Engagement_Score"] = 1 / (df["Recency"] + 1)

    df["Spend_to_Income_Ratio"] = df["Total_Spend"] / (df["Income"] + 1)

    model_features = [
        "Age",
        "Income",
        "Total_Spend",
        "Total_Purchases",
        "Web_Purchase_Ratio",
        "Campaign_Response_Score",
        "Engagement_Score",
        "Spend_to_Income_Ratio"
    ]

    df_model = df[model_features]

    return df, df_model