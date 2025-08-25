import streamlit as st
from components.description_variables import show_description


def accueil():
    """
    Affiche la page d'accueil de l'application Stroke Prediction.

    Fonctionnalités principales :
    - Affiche un en-tête de bienvenue.
    - Fournit un texte introductif expliquant l'objectif de l'application :
        explorer les données patients, visualiser les statistiques clés et comprendre
        les facteurs associés aux AVC.
    - Propose un bouton "Description des variables" :
        - Lorsqu'il est cliqué, appelle la fonction `show_description()` pour afficher
          les détails des variables des patients.

    Remarques :
    - La fonction ne prend pas d'arguments et ne retourne aucune valeur.
    - Elle repose sur Streamlit pour l'affichage interactif.
    """

    st.header("Bienvenue sur l'application Stroke Prediction")
    st.markdown(
        "Explorez les données des patients, visualisez les statistiques clés et comprenez les facteurs associés aux AVC."
    )
    if st.button("Description des variables"):
        show_description()
