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
    st.markdown (("Bienvenue sur l’application de visualisation des données AVC. "
    "Cette application vous permet d’explorer les données des patients, visualiser les statistiques clés, et comprendre les facteurs associés aux AVC."))

# Explication des variables
    if st.button("Description des variables"):
        st.markdown("""
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
    """)


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
    st.header("Visualisations")

    #  Graphique 1 : Le taux d'AVC par genre
    stroke_by_gender = df.groupby("gender")["stroke"].mean().reset_index()
    stroke_by_gender["stroke"] *= 100  # conversion en %
    fig1 = px.bar(
        stroke_by_gender,
        x="gender",
        y="stroke",
        labels={"stroke": "Taux d'AVC (%)", "gender": "Genre"},
        title="Graphique 1 : Montre le taux d'AVC en fonction du genre.",
        text=stroke_by_gender["stroke"].round(1)  # afficher les % sur les barres
    )
    fig1.update_traces(textposition="outside", marker_line_width=0)
    st.plotly_chart(fig1)
    st.markdown("Graphique 1: On remarque avec ce graphe que les hommes sont subgé a etre touche par l'AVC que les femmes." \
    "Hommes : 51%  -  Femmes : 47%" )

    # Graphique 2 : Nombre d'AVC par tranche d'âge
    fig2 = px.bar(
        df.groupby("age")["stroke"].sum().reset_index(),
        x="age",
        y="stroke",
        title="Graphique 2 : Le nombre d'AVC par tranche d'âge.",
        labels={"age": "Âge", "stroke": "Nombre d'AVC"},
        color="stroke"
    )
    fig2.update_layout(bargap=0.2)  # réduire l'espace entre les barres
    st.plotly_chart(fig2)
    st.markdown("Graphique 2: Le calcul de la répartition du nombre d'AVC par tranche d'age montre que les personnes ages a partir de 80 ans ont souvent des crises d'AVC")
    


    # Graphique 3 : Lien entre hypertension, âge moyen et AVC
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
        title="Graphique 3 : Âge moyen selon hypertension et AVC."
    )
    st.plotly_chart(fig3)
    # st.markdown("Graphique 3: " ICI A COMPLETE



    # Graphique 4 : Répartition des AVC selon les tranches de BMI
    df["bmi_bin"] = pd.cut(
        df["bmi"],
        bins=[0, 18.5, 25, 30, 35, df["bmi"].max()],
        labels=["Maigreur", "Normal", "Surpoids", "Obésité modérée", "Obésité sévère"]
    )
    df_bmi_stroke = df[df["stroke"] == 1]
    fig4 = px.pie(
        df_bmi_stroke,
        names="bmi_bin",
        title="Répartition des AVC selon les tranches de BMI",
        hole=0.1,  
        color="bmi_bin",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig4)



    # Graphique 5 : Taux d'AVC selon maladie cardiaque et tabagisme
    rate_data = df.groupby(["heart_disease", "smoking_status"])["stroke"].mean().reset_index()
    rate_data["stroke"] *= 100  # en %

    fig5 = px.bar(
        rate_data,
        x="smoking_status",
        y="stroke",
        color="heart_disease",
        barmode="group",
        labels={
            "stroke": "Taux d'AVC (%)",
            "smoking_status": "Statut de fumeur",
            "heart_disease": "Maladie cardiaque (0 = Non, 1 = Oui)"
        },
        title="Graphique 5 : Taux d'AVC (%) selon maladie cardiaque et tabagisme.",
        text=rate_data["stroke"].round(1)
    )
    fig5.update_traces(textposition="outside")
    st.plotly_chart(fig5)


with stats:
    st.header("Stats")






