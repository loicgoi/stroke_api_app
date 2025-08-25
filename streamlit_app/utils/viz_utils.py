import plotly.express as px
from collections import Counter


def plot_taux_avc(patients):
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
