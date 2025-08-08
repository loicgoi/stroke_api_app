import streamlit as st
import pandas as pd
from stroke_api.filters import filter_patient, get_stroke_data

st.set_page_config(page_title="Stroke Prediction App", layout="wide")


st.title("Stroke Prediction App")

accueil, donnees, viz, stats = st.tabs(["Accueil", "Données", "Visualisation", "Stats"])

with accueil:
    st.header("Bienvenue sur l'application Stroke Prediction")

with donnees:
    st.header("Données")

    @st.cache_data
    def load_data():
        return get_stroke_data()

    st.markdown(
        """Veuillez choisir vos critères de filtrage. Renseignez un ID de patient :"""
    )
    patient_id = st.text_input("ID de patient attendu", key="id", width=150)

    st.markdown("""Ou sélectionnez vos critères :""")

    col1, col2, col3 = st.columns(3)

    selected_gender = col1.selectbox(
        "Sélectionner un genre", ["Tous", "Male", "Female"], index=0
    )
    selected_stroke = col2.selectbox(
        "Sélectionner si AVC", ["Tous", "Oui", "Non"], index=0
    )
    selected_age = col3.slider(
        "Tranches d'âge des patients",
        min_value=0,
        max_value=100,
        value=(30, 70),
        step=1,
    )

    df = load_data()
    if patient_id:
        try:
            patient = df[df["id"] == int(patient_id)]
            if not patient.empty:
                st.dataframe(patient)
            else:
                st.warning("Aucun patient trouvé avec cet ID.")
        except ValueError:
            st.error("ID invalide. Veuillez entrer un nombre.")
    else:
        # Préparer les filtres
        gender = selected_gender if selected_gender != "Tous" else None
        stroke = {"Oui": 1, "Non": 0}.get(selected_stroke, None)
        min_age, max_age = selected_age  # <-- déballage du tuple

        filtered_data = filter_patient(
            gender=gender,
            stroke=stroke,
            min_age=min_age,
            max_age=max_age,
        )
        if filtered_data:
            st.dataframe(pd.DataFrame(filtered_data))
            st.markdown(f"**{len(filtered_data)} patients trouvés**")
        else:
            st.warning("Aucun patient ne correspond aux critères sélectionnés.")

with viz:
    st.header("Graphiques")

with stats:
    st.header("Stats")
