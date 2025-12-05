import streamlit as st
import pandas as pd
import plotly.express as px


# --- Configuration de la page ---

st.set_page_config(
    page_title="Répartition des validations",
    layout="wide"   # 👈 permet d'utiliser toute la largeur de la page
)


# --- Titre principal en couleur ---
st.markdown(
    "<h1 style='color:#06B59C;'>Evolution des validations (1er trimestre)</h1>",
    unsafe_allow_html=True
)

# --- Chargement des données ---
data = pd.read_csv(
    "validations-reseau-ferre-nombre-validations-par-jour-1er-trimestre.csv",
    sep=";"
)

# Conversion des dates
data["jour"] = pd.to_datetime(data["jour"], dayfirst=True)


# --- Logo dans la sidebar ---
st.sidebar.image("ratp-logo.png", use_container_width=True)  # 👈 ton fichier logo

st.sidebar.header("Filtres")

mois = st.sidebar.selectbox("Choisir un mois", sorted(data["Mois"].unique()))

# --- Application des filtres ---
data_filtered = data[data["Mois"] == mois]


# ================================
# 🎟️ Graphique 1 : Répartition par catégorie de titre
# ================================
data_grouped_cat = (
    data.groupby("categorie_titre")["nb_vald"]
    .sum()
    .reset_index()
)

fig_cat = px.pie(
    data_grouped_cat,
    names="categorie_titre",
    values="nb_vald",
    title="Répartition des validations par catégorie de titre",
    hole=0.4  # donut chart
)
st.plotly_chart(fig_cat, use_container_width=True)

# ================================
# 📊 Graphique 2 : Barres par mois et catégorie
# ================================
data_grouped_mois = (
    data.groupby(["Mois", "categorie_titre"])["nb_vald"]
    .sum()
    .reset_index()
)
# --- Préparer les données en pourcentage ---
data_grouped_mois_pct = (
    data_grouped_mois
    .groupby("Mois")
    .apply(lambda d: d.assign(pct = d["nb_vald"] / d["nb_vald"].sum() * 100))
    .reset_index(drop=True)
)

# --- Graphique en 100% ---
fig_mois_pct = px.bar(
    data_grouped_mois_pct,
    x="Mois",
    y="pct",
    color="categorie_titre",
    title="Répartition en % des validations par mois et par catégorie",
    labels={"pct": "Part (%)", "Mois": "Mois"},
    text_auto=".1f"  # affiche les % sur les barres
)

# Barres empilées en 100%
fig_mois_pct.update_layout(barmode="stack", yaxis=dict(ticksuffix="%"))

st.plotly_chart(fig_mois_pct, use_container_width=True)