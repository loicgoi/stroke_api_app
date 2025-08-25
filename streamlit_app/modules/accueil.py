import streamlit as st
from components.description_variables import show_description


def accueil():
    st.header("Bienvenue sur l'application Stroke Prediction")
    st.markdown(
        "Explorez les données des patients, visualisez les statistiques clés et comprenez les facteurs associés aux AVC."
    )
    if st.button("Description des variables"):
        show_description()
