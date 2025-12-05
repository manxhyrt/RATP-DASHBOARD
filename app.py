import streamlit as st
import pandas as pd
import plotly.express as px

# ================================
# 🚇 Dashboard RATP - 1er trimestre
# ================================

# --- Configuration de la page ---

st.set_page_config(
    page_title="Dashboard RATP",
    layout="wide"   # 👈 permet d'utiliser toute la largeur de la page
)


# --- Titre principal en couleur ---
st.markdown(
    "<h1 style='color:#06B59C;'>📊 Dashboard RATP - Validations des titres de transport (1er trimestre)</h1>",
    unsafe_allow_html=True
)


# --- Chargement des données ---
data = pd.read_csv(
    "validations-reseau-ferre-nombre-validations-par-jour-1er-trimestre.csv",
    sep=";"
)

# Conversion des dates
data["jour"] = pd.to_datetime(data["jour"], dayfirst=True)

# =================================
# --- Filtres ---  MENU
# =================================

# --- Logo dans la sidebar ---
st.sidebar.image("ratp-logo.png", use_container_width=True)  # 👈 ton fichier logo

st.sidebar.header("Filtres")

mois = st.sidebar.selectbox("Choisir un mois", sorted(data["Mois"].unique()))

# --- Application des filtres ---
data_filtered = data[data["Mois"] == mois]

st.subheader("📂 Données filtrées")

st.dataframe(data_filtered, use_container_width=True)


# ================================
# 🚇 KPI en haut du dashboard
# ================================
col1, col2 = st.columns(2)


# Nombre de stations uniques
nb_stations = data["libelle_arret"].nunique()

# Nombre total de validations
nb_validations = data["nb_vald"].sum()

# --- Mise en page en colonnes ---
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
        <div style="background-color:#06B59C; padding:20px; border-radius:10px; text-align:center">
            <h3 style="color:white;">Nombre de stations</h3>
            <h2 style="color:white; font-size:36px;">{nb_stations}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div style="background-color:#00319C; padding:20px; border-radius:10px; text-align:center">
            <h3 style="color:white;">Nombre total de validations</h3>
            <h2 style="color:white; font-size:36px;">{nb_validations:,}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )


# ================================
# 🚉 Graphique 1 : Top 10 des arrêts
# ================================
data_grouped_arret = (
    data.groupby("libelle_arret")["nb_vald"]
    .sum()
    .reset_index()
    .sort_values(by="nb_vald", ascending=False)
    .head(10)
)

fig_arret = px.bar(
    data_grouped_arret,
    x="libelle_arret",
    y="nb_vald",
    title="Top 10 des arrêts les plus validés",
    labels={"libelle_arret": "Arrêt", "nb_vald": "Nombre de validations"},
    color="nb_vald",
    color_continuous_scale="Blues"
)
st.plotly_chart(fig_arret, use_container_width=True)
