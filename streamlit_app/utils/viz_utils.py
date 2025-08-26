import plotly.express as px
from collections import Counter


def plot_taux_avc(patients) -> px.fig:
    """
    Crée un graphique en barres représentant le taux d'AVC par genre.

    Args:
        patients (list of dict): Liste de dictionnaires représentant les patients.
            Chaque dictionnaire peut contenir les clés "gender" et "stroke".

    Returns:
        plotly.fig: Figure Plotly sous forme de bar chart, avec :
            - x : genres ("Male", "Female", "Unknown", etc.)
            - y : taux d'AVC (%) pour chaque genre
            - texte : pourcentage arrondi affiché sur chaque barre
            - titre : "Taux d'AVC par genre"

    Remarques :
    - Si le genre d'un patient n'est pas renseigné, "Unknown" est utilisé.
    - Le taux d'AVC est calculé comme (nombre d'AVC / nombre total de patients du genre) * 100.
    - La fonction ne modifie pas `st.session_state`; elle se contente de renvoyer la figure Plotly.
    """

    compteur, total = {}, {}
    for p in patients:
        g = p.get("gender", "Unknown")
        compteur[g] = compteur.get(g, 0) + p.get("stroke", 0)
        total[g] = total.get(g, 0) + 1
    taux = {g: compteur[g] / total[g] * 100 for g in compteur}
    return px.bar(
        x=list(taux.keys()),
        y=list(taux.values()),
        labels={"x": "Genre", "y": "Taux d'AVC (%)"},
        text=[round(v, 1) for v in taux.values()],
        title="Taux d'AVC par genre",
    )
