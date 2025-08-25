import streamlit as st
from stroke_api.filters import filter_patient


@st.cache_data
def get_patients(gender=None, stroke=None, min_age=0, max_age=100):
    return filter_patient(
        gender=gender, stroke=stroke, min_age=min_age, max_age=max_age
    )
