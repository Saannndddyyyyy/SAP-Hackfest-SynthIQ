import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


# -------------------------------------------------
# LAYER 1 — HIGH-RESOLUTION AUTO CLUSTERING
# -------------------------------------------------

def auto_cluster(df_model, min_clusters=30):

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df_model)

    n_samples = len(df_model)

    # Ensure we don’t exceed sample size
    n_clusters = min(min_clusters, max(2, n_samples // 2))

    model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = model.fit_predict(scaled_data)

    df_clustered = df_model.copy()
    df_clustered["Cluster"] = clusters

    return df_clustered, n_clusters


# -------------------------------------------------
# LAYER 2 — MACRO PERSONA CREATION
# -------------------------------------------------

def generate_macro_personas(df_clustered):

    global_means = df_clustered.drop(columns=["Cluster"]).mean()
    cluster_means = df_clustered.groupby("Cluster").mean()

    persona_map = {}

    for cluster_id in cluster_means.index:

        deviations = cluster_means.loc[cluster_id] - global_means
        dominant = deviations.abs().sort_values(ascending=False).head(2).index.tolist()

        name = " & ".join(dominant).replace("_", " ")
        persona_map[cluster_id] = f"High {name}"

    df_clustered["Macro_Persona"] = df_clustered["Cluster"].map(persona_map)

    return df_clustered


# -------------------------------------------------
# LAYER 3 — LLM-STYLE NARRATIVE GENERATOR
# -------------------------------------------------

def generate_llm_narratives(df_clustered):

    global_means = df_clustered.drop(columns=["Cluster", "Macro_Persona"]).mean()
    global_std = df_clustered.drop(columns=["Cluster", "Macro_Persona"]).std()

    narratives = {}

    cluster_means = df_clustered.groupby("Macro_Persona").mean()

    for persona in cluster_means.index:

        row = cluster_means.loc[persona]
        z_scores = (row - global_means) / (global_std + 1e-6)

        dominant = z_scores.abs().sort_values(ascending=False).head(3).index.tolist()

        traits_text = ", ".join([d.replace("_", " ") for d in dominant])

        narrative = f"""
This segment is characterized by elevated {traits_text}.
Customers in this group demonstrate statistically significant behavioral deviation 
from the overall market baseline. 

They exhibit structured purchasing patterns and measurable engagement signals. 
Strategically, this segment represents a differentiated behavioral archetype 
requiring targeted positioning and customized value propositions.
"""

        narratives[persona] = narrative.strip()

    return narratives