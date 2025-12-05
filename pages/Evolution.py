import streamlit as st
import pandas as pd
import plotly.express as px


# --- Configuration de la page ---

st.set_page_config(
    page_title="Evolution des validations",
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
# 📈 Graphique 1 : Courbe par jour
# ================================
data_grouped_jour = (
    data.groupby("jour")["nb_vald"]
    .sum()
    .reset_index()
)

fig_jour = px.line(
    data_grouped_jour,
    x="jour",
    y="nb_vald",
    title="Évolution des validations par jour",
    labels={"jour": "Jour", "nb_vald": "Nombre de validations"},
    markers=True
)
st.plotly_chart(fig_jour, use_container_width=True)

# ================================
# 📈 Graphique 2 : Courbe cumulée des validations
# ================================
data_grouped_cumul = (
    data.groupby("jour")["nb_vald"]
    .sum()
    .cumsum()
    .reset_index()
)

fig_cumul = px.line(
    data_grouped_cumul,
    x="jour",
    y="nb_vald",
    title="Cumul des validations au fil du temps",
    labels={"jour": "Jour", "nb_vald": "Cumul des validations"},
    markers=True
)
st.plotly_chart(fig_cumul, use_container_width=True)
