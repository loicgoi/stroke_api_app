import streamlit as st
from modules import accueil, donnees, visualisations, statistiques

st.set_page_config(page_title="Stroke Prediction App", layout="wide")

st.title("Stroke Prediction App")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Accueil", "Données", "Visualisation", "Statistiques"]
)

with tab1:
    accueil.accueil()

with tab2:
    donnees.donnees()

with tab3:
    visualisations.visualisations()

with tab4:
    statistiques.statistiques()
