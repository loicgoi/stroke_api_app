import streamlit as st
from stroke_api.filters import filter_patient


def donnees():
    st.header("Données")

    # --- Bouton Reset ---
    if st.button("Réinitialiser les filtres"):
        for key in [
            "patient_id",
            "selected_gender",
            "selected_stroke",
            "selected_age",
            "patients_data",
        ]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()  # recharge la page avec valeurs par défaut

    # ID du patient
    patient_id = st.text_input(
        "ID de patient",
        key="patient_id",  # clé explicite
        value=st.session_state.get("patient_id", ""),  # garder la saisie précédente
        placeholder="Ex : 9032",
    )

    col1, col2, col3 = st.columns(3)

    selected_gender = col1.selectbox(
        "Sélectionner un genre",
        ["Tous", "Male", "Female"],
        key="selected_gender",
        index=["Tous", "Male", "Female"].index(
            st.session_state.get("selected_gender", "Tous")
        ),
    )

    selected_stroke = col2.selectbox(
        "Sélectionner si AVC",
        ["Tous", "Oui", "Non"],
        key="selected_stroke",
        index=["Tous", "Oui", "Non"].index(
            st.session_state.get("selected_stroke", "Tous")
        ),
    )

    selected_age = col3.slider(
        "Tranche d'âge",
        0,
        100,
        st.session_state.get("selected_age", (30, 70)),  # valeur précédente ou défaut
        key="selected_age",
    )

    # Conversion en filtres
    gender = None if selected_gender == "Tous" else selected_gender
    stroke = (
        None if selected_stroke == "Tous" else {"Oui": 1, "Non": 0}[selected_stroke]
    )
    min_age, max_age = selected_age

    # --- Récupération des patients filtrés ---
    if patient_id:
        try:
            patient_id_int = int(patient_id)
            patients_data = [
                p for p in filter_patient() if p.get("id") == patient_id_int
            ]
            if not patients_data:
                st.warning("Patient non trouvé.")
        except ValueError:
            st.error("ID invalide.")
            patients_data = []
    else:
        patients_data = filter_patient(
            gender=gender, stroke=stroke, min_age=min_age, max_age=max_age
        )

    if not patients_data:
        st.warning("Aucun patient ne correspond aux critères.")
    else:
        st.dataframe(patients_data)
        st.markdown(f"**{len(patients_data)} patients trouvés**")

    # Sauvegarde pour les autres pages
    st.session_state["patients_data"] = patients_data
