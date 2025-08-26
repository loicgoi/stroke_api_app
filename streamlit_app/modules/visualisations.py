import streamlit as st
import plotly.express as px
from collections import Counter


@st.cache_data
def calc_taux_avc(patients) -> dict:
    """
    Calcule le taux d'AVC par genre à partir d'une liste de patients.

    Args:
        patients (list of dict): Liste de dictionnaires représentant les patients.
            Chaque dictionnaire peut contenir les clés "gender" et "stroke".

    Returns:
        dict: Un dictionnaire où chaque clé est un genre ("Male", "Female", etc.)
              et chaque valeur est le pourcentage de patients ayant eu un AVC pour ce genre.

    Remarques :
    - La fonction utilise le caching de Streamlit (@st.cache_data) pour optimiser les performances.
    - Si le genre d'un patient n'est pas renseigné, "Unknown" est utilisé.
    """

    compteur, total = {}, {}
    for p in patients:
        g = p.get("gender", "Unknown")
        compteur[g] = compteur.get(g, 0) + p.get("stroke", 0)
        total[g] = total.get(g, 0) + 1
    return {g: compteur[g] / total[g] * 100 for g in compteur}


@st.cache_data
def calc_avc_par_age(patients) -> Counter:
    """
    Compte le nombre de patients ayant eu un AVC par âge.

    Args:
        patients (list of dict): Liste de dictionnaires représentant les patients.
            Chaque dictionnaire doit contenir les clés "age" et "stroke".

    Returns:
        collections.Counter: Compteur des AVC par âge, uniquement pour les patients
                             ayant eu un AVC (stroke == 1).

    Remarques :
    - Les âges des patients sans AVC sont ignorés.
    - La fonction utilise le caching de Streamlit (@st.cache_data) pour optimiser les performances.
    """
    return Counter(p["age"] for p in patients if p.get("stroke") == 1)


@st.cache_data
def calc_avc_par_imc(patients) -> Counter:
    """
    Compte le nombre de patients ayant eu un AVC selon les catégories d'IMC.

    Args:
        patients (list of dict): Liste de dictionnaires représentant les patients.
            Chaque dictionnaire doit contenir les clés "bmi" et "stroke".

    Returns:
        collections.Counter: Compteur des AVC par catégorie d'IMC :
            - "Maigreur" : IMC < 18.5
            - "Normal" : 18.5 <= IMC < 25
            - "Surpoids" : 25 <= IMC < 30
            - "Obésité modérée" : 30 <= IMC < 35
            - "Obésité sévère" : IMC >= 35

    Remarques :
    - Seuls les patients ayant eu un AVC (stroke == 1) sont comptés.
    - La fonction utilise le caching de Streamlit (@st.cache_data) pour optimiser les performances.
    """

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
def calc_avc_maladie_tabac(patients) -> int:
    """
    Calcule le taux d'AVC en fonction de la présence de maladie cardiaque et du statut tabagique.

    Args:
        patients (list of dict): Liste de dictionnaires représentant les patients.
            Chaque dictionnaire peut contenir les clés "heart_disease", "smoking_status" et "stroke".

    Returns:
        list of dict: Liste de dictionnaires avec les clés suivantes :
            - "heart_disease" : 0 ou 1
            - "smoking_status" : statut du patient ("Unknown" si non renseigné)
            - "stroke" : pourcentage de patients ayant eu un AVC dans ce groupe

    Remarques :
    - Les résultats sont regroupés par combinaison (maladie cardiaque, statut tabac).
    - La fonction utilise le caching de Streamlit (@st.cache_data) pour optimiser les performances.
    """

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


def visualisations():
    """
    Affiche les visualisations statistiques des données patients dans l'application Streamlit.

    Fonctionnalités principales :
    - Vérifie que des patients ont été sélectionnés dans `st.session_state["patients_data"]`.
    - Crée quatre visualisations avec Plotly :
        1. Taux d'AVC par genre (bar chart)
        2. Nombre d'AVC par âge (bar chart)
        3. Répartition des AVC selon les catégories d'IMC (pie chart)
        4. Taux d'AVC selon la présence de maladie cardiaque et le statut tabagique (bar chart groupé)
    - Affiche les graphiques directement dans l'application Streamlit.
    - Si aucun patient n'est sélectionné, affiche un message d'information.

    Remarques :
    - Les calculs utilisent les fonctions `calc_taux_avc`, `calc_avc_par_age`,
      `calc_avc_par_imc` et `calc_avc_maladie_tabac` avec caching pour optimiser les performances.
    - Les graphiques sont interactifs grâce à Plotly.
    """

    st.header("Visualisations")
    patients_data = st.session_state.get("patients_data", [])
    if not patients_data:
        st.info("Veuillez d'abord sélectionner des patients dans l'onglet Données.")
        return

    # --- 1. Taux d'AVC par genre (bar chart horizontal)
    taux_avc = calc_taux_avc(patients_data)
    fig1 = px.bar(
        {"Genre": list(taux_avc.keys()), "Taux d'AVC (%)": list(taux_avc.values())},
        x="Taux d'AVC (%)",
        y="Genre",
        orientation="h",
        text=[round(v, 1) for v in taux_avc.values()],
        title="Taux d'AVC par genre",
    )
    fig1.update_traces(textposition="outside")
    st.plotly_chart(fig1)

    # --- 2. Nombre d'AVC par âge (histogramme)
    ages = [p["age"] for p in patients_data if p.get("stroke") == 1]
    fig2 = px.histogram(
        ages,
        nbins=20,
        labels={"value": "Âge", "count": "Nombre d'AVC"},
        title="Distribution des AVC par âge",
    )
    st.plotly_chart(fig2)

    # --- 3. Répartition des AVC selon IMC (bar chart)
    imc_count = calc_avc_par_imc(patients_data)
    fig3 = px.bar(
        {
            "Catégorie IMC": list(imc_count.keys()),
            "Nombre d'AVC": list(imc_count.values()),
        },
        x="Catégorie IMC",
        y="Nombre d'AVC",
        text=[v for v in imc_count.values()],
        title="Répartition des AVC selon IMC",
        color="Catégorie IMC",
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig3.update_traces(textposition="outside")
    st.plotly_chart(fig3)

    # --- 4. AVC selon maladie cardiaque et tabac (heatmap)
    rate_list = calc_avc_maladie_tabac(patients_data)

    # Préparer les axes et la matrice des valeurs
    smoking_statuses = sorted(list(set(d["smoking_status"] for d in rate_list)))
    heart_diseases = [0, 1]  # 0 = pas de maladie cardiaque, 1 = maladie cardiaque
    z_matrix = []

    for hd in heart_diseases:
        row = []
        for ss in smoking_statuses:
            # Chercher le taux correspondant
            val = next(
                (
                    d["stroke"]
                    for d in rate_list
                    if d["heart_disease"] == hd and d["smoking_status"] == ss
                ),
                0,
            )
            row.append(val)
        z_matrix.append(row)

    fig4 = px.imshow(
        z_matrix,
        x=smoking_statuses,
        y=["Sans maladie cardiaque", "Avec maladie cardiaque"],
        labels={
            "x": "Statut fumeur",
            "y": "Maladie cardiaque",
            "color": "Taux d'AVC (%)",
        },
        color_continuous_scale="Reds",
        text_auto=True,
        title="Taux d'AVC selon maladie cardiaque et statut tabac",
    )

    st.plotly_chart(fig4)

    # --- 5. Scatter IMC vs Âge pour AVC avec 2 couleurs distinctes
    scatter_data = [p for p in patients_data if p.get("stroke") == 1]
    fig5 = px.scatter(
        scatter_data,
        x="age",
        y="bmi",
        color="gender",
        color_discrete_map={"Male": "blue", "Female": "red", "Unknown": "gray"},
        labels={"age": "Âge", "bmi": "IMC", "gender": "Genre"},
        title="IMC vs Âge des patients ayant eu un AVC",
        hover_data=["stroke"],
    )
    st.plotly_chart(fig5)
