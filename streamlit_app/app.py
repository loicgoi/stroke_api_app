import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import pandas as pd
from stroke_api.filters import filter_patient, get_stroke_data

st.set_page_config(page_title="Stroke Prediction App", layout="wide")

# Configuration url
API_BASE = "http://localhost:8000"
PATIENTS_URL = f"{API_BASE}/patients"
STATS_URL = f"{API_BASE}/stats"


# Fonctions mise en cache des données
@st.cache_data
def query_patients(params: dict) -> pd.DataFrame:
    """Interroge l'endpoint /patients/ avec filtres."""
    try:
        response = requests.get(PATIENTS_URL, params=params, timeout=10)
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur API /patients : {e}")
        return pd.DataFrame()


@st.cache_data
def query_stats() -> dict:
    """Interroge l'endpoint /stats/."""
    try:
        response = requests.get(STATS_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur API /stats : {e}")
        return {}


# Onglets
st.title("Stroke Prediction App")
accueil, donnees, viz, stats = st.tabs(
    ["Accueil", "Données", "Visualisation", "Statistiques"]
)

# Accueil
with accueil:
    st.title("Détection des AVC")

    st.markdown(
        """
    Bienvenue dans l'application de détection des AVC (Accidents Vasculaires Cérébraux).

    ---
    
    ### Navigation :
    - **Données** : explorez les patients et appliquez des filtres.
    - **Statistiques** : consultez les chiffres globaux.
    - **(À venir) Prédictions** : prédisez le risque d’AVC.

    ---
    
    ### Données utilisées :
    Jeu de données public sur les AVC incluant :
    - Âge, sexe, antécédents médicaux,
    - Statut AVC (oui/non).

    Données exposées via une API FastAPI.

    ---
    
    Projet réalisé dans le cadre de la formation *Développeur en Intelligence Artificielle* (Simplon, 2025–2026).
    
    Technologies : Python · FastAPI · Pandas · Streamlit · REST API
    """
    )

# Tableau de données filtrables
with donnees:
    st.header("Données")

    # --- Filtres ---
    patient_id = st.text_input(
        "ID de patient attendu",
        key="id",
        placeholder="Ex : 9032",
        help="Laissez vide pour filtrer par critères",
    )

    col1, col2, col3 = st.columns(3)
    selected_gender = col1.selectbox(
        "Sélectionner un genre", ["Tous", "Male", "Female"], index=0
    )
    selected_stroke = col2.selectbox(
        "Sélectionner si AVC", ["Tous", "Oui", "Non"], index=0
    )
    selected_age = col3.slider("Tranches d'âge", 0, 100, (30, 70), 1)

    # --- Construction params ---
    params = {}
    if selected_gender != "Tous":
        params["gender"] = selected_gender
    if selected_stroke != "Tous":
        params["stroke"] = {"Oui": 1, "Non": 0}[selected_stroke]
    params["min_age"], params["max_age"] = selected_age

    # --- Requête par ID ou par filtres ---
    if patient_id:
        try:
            resp = requests.get(f"{PATIENTS_URL}/{int(patient_id)}", timeout=10)
            resp.raise_for_status()
            st.dataframe(pd.DataFrame([resp.json()]))
        except ValueError:
            st.error("ID invalide.")
        except requests.exceptions.HTTPError as e:
            st.warning(
                "Patient non trouvé." if resp.status_code == 404 else f"Erreur : {e}"
            )
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur de connexion : {e}")
    else:
        df = query_patients(params)
        if df.empty:
            st.warning("Aucun patient ne correspond aux critères.")
        else:
            st.dataframe(df)
            st.markdown(f"**{len(df)} patients trouvés**")

# Graphiques
with viz:
    st.header("Visualisations")

    # Le taux d'AVC par genre
    stroke_by_gender = df.groupby("gender")["stroke"].mean().reset_index()
    stroke_by_gender["stroke"] = stroke_by_gender["stroke"] * 100  # conversion en %
    fig1 = px.bar(
        stroke_by_gender,
        x="gender",
        y="stroke",
        labels={"stroke": "Taux d'AVC (%)", "gender": "Genre"},
        title="Taux d'AVC en fonction du genre",
        text=stroke_by_gender["stroke"].round(1),  # afficher les % sur les barres
    )
    fig1.update_traces(textposition="outside")
    st.plotly_chart(fig1, key="fig1")

    # Graphique en barres : nombre d'AVC par tranche d'âge
    fig2 = px.bar(
        df.groupby("age")["stroke"].sum().reset_index(),
        x="age",
        y="stroke",
        title="Nombre d'AVC par âge",
        labels={"age": "Âge", "stroke": "Nombre d'AVC"},
        color="stroke",
    )
    fig2.update_traces(width=0.8)
    st.plotly_chart(fig2, key="fig2")

    #  Lien entre hypertension, âge moyen et AVC
    fig3 = px.bar(
        df.groupby(["hypertension", "stroke"])["age"].mean().reset_index(),
        x="hypertension",
        y="age",
        color="stroke",
        barmode="group",
        labels={
            "hypertension": "Hypertension (0 = Non, 1 = Oui)",
            "age": "Âge moyen",
            "stroke": "AVC (0 = Non, 1 = Oui)",
        },
        title="Âge moyen selon hypertension et AVC",
    )
    st.plotly_chart(fig3, key="fig3")

    # Le lien entre hypertension, âge moyen et AVC
    fig4 = px.bar(
        df.groupby(["hypertension", "stroke"])["age"].mean().reset_index(),
        x="hypertension",
        y="age",
        color="stroke",
        barmode="group",
        labels={
            "hypertension": "Hypertension (0 = Non, 1 = Oui)",
            "age": "Âge moyen",
            "stroke": "AVC (0 = Non, 1 = Oui)",
        },
        title="Âge moyen selon hypertension et AVC",
    )
    st.plotly_chart(fig4, key="fig4")

    # Taux d'AVC selon heart_disease et smoking_status
    rate_data = (
        df.groupby(["heart_disease", "smoking_status"])["stroke"].mean().reset_index()
    )
    rate_data["stroke"] = rate_data["stroke"] * 100  # en %

    fig5 = px.bar(
        rate_data,
        x="smoking_status",
        y="stroke",
        color="heart_disease",
        barmode="group",
        labels={
            "stroke": "Taux d'AVC (%)",
            "smoking_status": "Statut de fumeur",
            "heart_disease": "Maladie cardiaque (0=Non, 1=Oui)",
        },
        title="Taux d'AVC (%) selon maladie cardiaque et tabagisme",
        text=rate_data["stroke"].round(1),
    )
    fig5.update_traces(textposition="outside")
    st.plotly_chart(fig5, key="fig5")

    st.markdown("**Graphique 5 :** Taux d'AVC selon heart_disease et smoking_status")

st.markdown(
    """
    **Graphique 1 :** affiche le nombre d'AVC par âge, ce qui permet de repérer les tranches d'âges les plus touchées.
    
    **Graphique 2 :** montre la proportion globale des personnes ayant eu un AVC (1) ou non (0).
            
    **Graphique 3 :**
    """
)

# Statistique
with stats:
    st.header("Statistiques")
    data = query_stats()
    if not data:
        st.stop()

    gender = data.pop("gender_distribution", {})
    flat = {**data, **gender}
    labels = {
        "total_patients": "Total patients",
        "stroke_true": "Patients avec AVC",
        "stroke_false": "Patients sans AVC",
        "average_age": "Âge moyen",
        "Male": "Hommes",
        "Female": "Femmes",
    }
    rows = [
        (labels.get(k, k), round(v, 2) if isinstance(v, float) else v)
        for k, v in flat.items()
    ]
    st.dataframe(pd.DataFrame(rows, columns=["Statistique", "Valeur"]))
