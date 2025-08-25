import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
from stroke_api.filters import filter_patient

st.set_page_config(page_title="Stroke Prediction App", layout="wide")

# --- Onglets ---
st.title("Stroke Prediction App")
accueil, donnees, viz, stats = st.tabs(
    ["Accueil", "Données", "Visualisation", "Statistiques"]
)

# --- Accueil ---
with accueil:
    st.header("Bienvenue sur l'application Stroke Prediction")
    st.markdown(
        "Explorez les données des patients, visualisez les statistiques clés et comprenez les facteurs associés aux AVC."
    )

    if st.button("Description des variables"):
        st.markdown(
            """
- **gender** : Genre du patient (Male, Female, Other)
- **age** : Âge en années
- **hypertension** : 1 = hypertension, 0 = non
- **heart_disease** : 1 = maladie cardiaque, 0 = non
- **ever_married** : Marié ou non
- **work_type** : Type d’emploi
- **Residence_type** : Urbain ou rural
- **avg_glucose_level** : Niveau moyen de glucose
- **bmi** : Indice de masse corporelle
- **smoking_status** : Habitudes tabagiques
- **stroke** : 1 = AVC, 0 = non
"""
        )

# --- Données ---
with donnees:
    st.header("Données")

    patient_id = st.text_input("ID de patient", key="id", placeholder="Ex : 9032")
    col1, col2, col3 = st.columns(3)
    selected_gender = col1.selectbox(
        "Sélectionner un genre", ["Tous", "Male", "Female"]
    )
    selected_stroke = col2.selectbox("Sélectionner si AVC", ["Tous", "Oui", "Non"])
    selected_age = col3.slider("Tranche d'âge", 0, 100, (30, 70))

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


# --- Fonctions cache pour graphiques ---
@st.cache_data
def calc_taux_avc(patients):
    compteur, total = {}, {}
    for p in patients:
        g = p.get("gender", "Unknown")
        compteur[g] = compteur.get(g, 0) + p.get("stroke", 0)
        total[g] = total.get(g, 0) + 1
    return {g: compteur[g] / total[g] * 100 for g in compteur}


@st.cache_data
def calc_avc_par_age(patients):
    return Counter(p["age"] for p in patients if p.get("stroke") == 1)


@st.cache_data
def calc_avc_par_imc(patients):
    def imc_bin(bmi):
        if bmi < 18.5:
            return "Maigreur"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Surpoids"
        elif bmi < 35:
            return "Obésité modérée"
        else:
            return "Obésité sévère"

    return Counter(imc_bin(p.get("bmi", 0)) for p in patients if p.get("stroke") == 1)


@st.cache_data
def calc_avc_maladie_tabac(patients):
    rate_data = {}
    for p in patients:
        key = (p.get("heart_disease", 0), p.get("smoking_status", "Unknown"))
        if key not in rate_data:
            rate_data[key] = {"stroke_sum": 0, "count": 0}
        rate_data[key]["stroke_sum"] += p.get("stroke", 0)
        rate_data[key]["count"] += 1
    return [
        {
            "heart_disease": k[0],
            "smoking_status": k[1],
            "stroke": v["stroke_sum"] / v["count"] * 100,
        }
        for k, v in rate_data.items()
    ]


# --- Visualisations ---
with viz:
    st.header("Visualisations")

    if not patients_data:
        st.info("Aucune donnée disponible pour les graphiques.")
    else:
        # Taux d'AVC par genre
        taux_avc = calc_taux_avc(patients_data)
        fig1 = px.bar(
            x=list(taux_avc.keys()),
            y=list(taux_avc.values()),
            labels={"x": "Genre", "y": "Taux d'AVC (%)"},
            text=[round(v, 1) for v in taux_avc.values()],
            title="Taux d'AVC par genre",
        )
        fig1.update_traces(textposition="outside")
        st.plotly_chart(fig1)

        # Nombre d'AVC par tranche d'âge
        age_count = calc_avc_par_age(patients_data)
        fig2 = px.bar(
            x=list(age_count.keys()),
            y=list(age_count.values()),
            labels={"x": "Âge", "y": "Nombre d'AVC"},
            title="Nombre d'AVC par âge",
        )
        st.plotly_chart(fig2)

        # Répartition des AVC selon IMC
        imc_count = calc_avc_par_imc(patients_data)
        fig3 = px.pie(
            names=list(imc_count.keys()),
            values=list(imc_count.values()),
            title="Répartition des AVC selon IMC",
            hole=0.1,
            color=list(imc_count.keys()),
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        st.plotly_chart(fig3)

        # AVC selon maladie cardiaque et tabagisme
        rate_list = calc_avc_maladie_tabac(patients_data)
        fig4 = px.bar(
            rate_list,
            x="smoking_status",
            y="stroke",
            color="heart_disease",
            barmode="group",
            text=[round(d["stroke"], 1) for d in rate_list],
            labels={
                "stroke": "Taux d'AVC (%)",
                "smoking_status": "Statut fumeur",
                "heart_disease": "Maladie cardiaque",
            },
        )
        fig4.update_traces(textposition="outside")
        st.plotly_chart(fig4)

# --- Statistiques ---
with stats:
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
