import streamlit as st
from stroke_api.filters import filter_patient


@st.cache_data
def get_patients(gender=None, stroke=None, min_age=0, max_age=100):
    """
    Récupère et filtre les patients en utilisant la fonction `filter_patient` avec mise en cache.

    Cette fonction agit comme un wrapper autour de `filter_patient` et applique les filtres
    sur le genre, la présence d'AVC et la tranche d'âge.
    Les résultats sont mis en cache par Streamlit pour améliorer les performances et éviter
    des appels répétitifs coûteux.

    Parameters
    ----------
    gender : str, optional
        Sexe des patients à filtrer (`"Male"`, `"Female"`, `"Other"`).
        Par défaut : `None` (pas de filtre).
    stroke : int | bool, optional
        Indicateur de présence d'AVC (`1` ou `True` = AVC, `0` ou `False` = pas d'AVC).
        Par défaut : `None` (pas de filtre).
    min_age : int, optional
        Âge minimum des patients à récupérer.
        Par défaut : `0`.
    max_age : int, optional
        Âge maximum des patients à récupérer.
        Par défaut : `100`.

    Returns
    -------
    list
        Liste de dictionnaires représentant les patients filtrés.

    Notes
    -----
    - La mise en cache `@st.cache_data` permet de réutiliser les résultats précédemment calculés
      tant que les paramètres n'ont pas changé.
    """
    return filter_patient(
        gender=gender, stroke=stroke, min_age=min_age, max_age=max_age
    )
