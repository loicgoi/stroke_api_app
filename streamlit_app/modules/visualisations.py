import streamlit as st
import plotly.express as px
from collections import Counter


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


def visualisations():
    st.header("Visualisations")

    patients_data = st.session_state.get("patients_data", [])

    if not patients_data:
        st.info("Veuillez d'abord sélectionner des patients dans l'onglet Données.")
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

        # Nombre d'AVC par âge
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
