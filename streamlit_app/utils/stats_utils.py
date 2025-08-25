import pandas as pd


def get_global_stats(patients_all):
    total_patients = len(patients_all)
    stroke_true = sum(p["stroke"] for p in patients_all)
    stroke_false = total_patients - stroke_true
    avg_age = (
        round(sum(p["age"] for p in patients_all) / total_patients, 2)
        if total_patients
        else 0
    )
    nb_hommes = sum(1 for p in patients_all if p["gender"].lower() == "male")
    nb_femmes = sum(1 for p in patients_all if p["gender"].lower() == "female")

    rows = [
        ("Total patients", total_patients),
        ("Hommes", nb_hommes),
        ("Femmes", nb_femmes),
        ("Patients avec AVC", stroke_true),
        ("Patients sans AVC", stroke_false),
        ("Âge moyen", avg_age),
    ]
    return pd.DataFrame(rows, columns=["Statistique", "Valeur"])
