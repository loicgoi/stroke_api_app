import streamlit as st
from stroke_api.filters import filter_patient
from modules.config import API_URL


def fetch_patients(gender=None, stroke=None, min_age=0, max_age=100):
    params = {
        "gender": gender,
        "stroke": stroke,
        "min_age": min_age,
        "max_age": max_age,
    }
    try:
        response = requests.get(f"{API_URL}/patients/", params=params)
        response.raise_for_status()
        data = response.json()
        if "message" in data:
            return []
        return data
    except Exception as e:
        st.error(f"Erreur API : {e}")
        return []


def fetch_patient_by_id(patient_id):
    try:
        response = requests.get(f"{API_URL}/patients/{patient_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            st.warning("Patient non trouvé.")
        else:
            st.error(f"Erreur API : {e}")
        return None
    except Exception as e:
        st.error(f"Erreur API : {e}")
        return None


def donnees():
    """
    Affiche et gère l'interface de sélection des données patients dans l'application Streamlit.

    Fonctionnalités principales :
    - Affiche un en-tête "Données".
    - Permet de filtrer les patients selon plusieurs critères :
        - ID du patient (champ texte)
        - Genre ("Tous", "Male", "Female")
        - Présence d'AVC ("Tous", "Oui", "Non")
        - Tranche d'âge (slider)
    - Bouton de réinitialisation ("Réinitialiser les filtres") qui supprime les filtres et recharge la page.
    - Filtre les données des patients à partir de la fonction `filter_patient()` selon les critères sélectionnés.
    - Affiche les résultats filtrés dans un tableau Streamlit (`st.dataframe`) et le nombre de patients trouvés.
    - Gère les erreurs :
        - ID patient non valide
        - Aucun patient correspondant aux critères
    - Sauvegarde les résultats filtrés dans `st.session_state["patients_data"]` pour utilisation dans d'autres pages de l'application.

    Remarques :
    - Les filtres "Tous" correspondent à l'absence de filtrage pour ce critère.
    - La fonction repose sur `st.session_state` pour conserver les sélections entre les rechargements de la page.
    """

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
