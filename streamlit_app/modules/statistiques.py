import streamlit as st
import pandas as pd
from stroke_api.filters import filter_patient
from modules.config import API_URL


def fetch_stats():
    """
    Récupère les statistiques depuis l'API et retourne les données au format JSON.

    Effectue une requête GET vers l'endpoint `/stats/` de l'API définie par `API_URL`.
    Si la requête est réussie, la réponse est convertie en dictionnaire Python via `response.json()`.
    En cas d'erreur (connexion, statut HTTP invalide, etc.), un message d'erreur est affiché
    dans Streamlit et la fonction retourne `None`.

    Returns
    -------
    dict | None
        Un dictionnaire contenant les statistiques si la requête réussit,
        sinon `None` en cas d'erreur.
    """
    try:
        response = requests.get(f"{API_URL}/stats/")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erreur API : {e}")
        return None


def statistiques():
    """
    Affiche les statistiques globales des patients dans l'application Streamlit.

    Fonctionnalités principales :
    - Récupère tous les patients via la fonction `filter_patient()`.
    - Calcule et affiche :
        - Le nombre total de patients
        - Le nombre d'hommes et de femmes
        - Le nombre de patients ayant eu un AVC
        - Le nombre de patients n'ayant pas eu d'AVC
        - L'âge moyen des patients
    - Affiche les statistiques sous forme de tableau Streamlit (`st.dataframe`).

    Remarques :
    - La fonction ne prend pas d'arguments et ne retourne pas de valeur.
    - Les calculs sont réalisés sur l'ensemble des patients sans filtrage préalable.
    - Les genres sont considérés comme "male" ou "female" (insensible à la casse).
    """

    st.header("Statistiques")
    patients_all = filter_patient()
    total_patients = len(patients_all)

    # Compteurs AVC
    stroke_true = sum(p["stroke"] for p in patients_all)
    stroke_false = total_patients - stroke_true

    # Âge moyen
    avg_age = (
        round(sum(p["age"] for p in patients_all) / total_patients, 2)
        if total_patients
        else 0
    )

    # Compteurs par genre
    nb_hommes = sum(1 for p in patients_all if p["gender"].lower() == "male")
    nb_femmes = sum(1 for p in patients_all if p["gender"].lower() == "female")

    rows = [
        ("Total patients", total_patients),
        ("Hommes", nb_hommes),
        ("Femmes", nb_femmes),
        ("Patients avec AVC", stroke_true),
        ("Patients sans AVC", stroke_false),
        ("Âge moyen", avg_age),
    ]

    stats_df = pd.DataFrame(rows, columns=["Statistique", "Valeur"])
    st.dataframe(stats_df)
