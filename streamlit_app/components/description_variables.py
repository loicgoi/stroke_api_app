import streamlit as st


def show_description():
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
