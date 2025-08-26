import streamlit as st
from modules import accueil, donnees, visualisations, statistiques

st.set_page_config(page_title="Stroke Prediction App", layout="wide")

st.sidebar.title("Menu")
page = st.sidebar.radio("", ["Accueil", "Données", "Visualisation", "Statistiques"])

st.sidebar.markdown("---")
st.sidebar.info("Stroke Prediction App")

st.title("Stroke Prediction App")

if page == "Accueil":
    accueil.accueil()
elif page == "Données":
    donnees.donnees()
elif page == "Visualisation":
    visualisations.visualisations()
elif page == "Statistiques":
    statistiques.statistiques()
