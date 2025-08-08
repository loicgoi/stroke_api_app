import streamlit as st
import pandas as pd
import requests
import plotly.express as px
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

tab1, tab2, tab3, tab4 = st.tabs(["Accueil", "Données", "Visualisations", "Statistiques" ])

with tab1 :
    st.markdown (("Bienvenue sur l’application de visualisation des données AVC. Cette application vous permet d’explorer les données des patients, visualiser les statistiques clés, et comprendre les facteurs associés aux AVC."))


def get_patients_data ():
    requests.get("http://localhosts:8000/filter_patient/") 
    return pd.DataFrame(response.json())

with tab2:
    st.header("Données des patients")

    # Appelle de l'API
    df = get_filter_patient_data ()

    # Filtrage des données :
    genre = st.selectbox("Genre", ["All"] + df("gender").unique().tolist())
    AVC = st.selectbox("AVC", ["All", 0, 1])
    age_max = st.slider("age_max", int(df["age"].min()), int(df["age"].max()), 60)

    # Application des filtrages
    if genre != "All":
        df = df(df("gender") == genre)
    if AVC != "All":
        df = df(df("stroke") == AVC)
    df= df(df("age") == age_max)

    # Affichage
    st.dataframe(df)


with tab3:
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
        text=stroke_by_gender["stroke"].round(1)  # afficher les % sur les barres
    )
    fig1.update_traces(textposition="outside")
    st.plotly_chart(fig1)

    # Graphique en barres : nombre d'AVC par tranche d'âge
    fig2 = px.bar(
        df.groupby("age")["stroke"].sum().reset_index(),
        x="age",
        y="stroke",
        title="Nombre d'AVC par âge",
        labels={"age": "Âge", "stroke": "Nombre d'AVC"},
        color="stroke"
    )
    st.plotly_chart(fig2)


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
            "stroke": "AVC (0 = Non, 1 = Oui)"
        },
        title="Âge moyen selon hypertension et AVC"
    )
    st.plotly_chart(fig3)

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
            "stroke": "AVC (0 = Non, 1 = Oui)"
        },
    title="Âge moyen selon hypertension et AVC"
    )
    st.plotly_chart(fig4)

    # Taux d'AVC selon heart_disease et smoking_status
    rate_data = df.groupby(["heart_disease", "smoking_status"])["stroke"].mean().reset_index()
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
            "heart_disease": "Maladie cardiaque (0=Non, 1=Oui)"
        },
        title="Taux d'AVC (%) selon maladie cardiaque et tabagisme",
        text=rate_data["stroke"].round(1)
    )
    fig5.update_traces(textposition="outside")
    st.plotly_chart(fig5)


st.markdown("""
    **Graphique 1 :** affiche le nombre d'AVC par âge, ce qui permet de repérer les tranches d'âges les plus touchées.
    
    **Graphique 2 :** montre la proportion globale des personnes ayant eu un AVC (1) ou non (0).
            
    **Graphique 3 :**
    """)




