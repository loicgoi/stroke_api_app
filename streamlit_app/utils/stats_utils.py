import pandas as pd


def get_global_stats(patients_all):
    """
    Calcule et retourne des statistiques globales à partir d'une liste de patients.

    Cette fonction analyse les données d'une liste de patients et calcule :
    - le nombre total de patients,
    - le nombre d'hommes et de femmes,
    - le nombre de patients ayant eu un AVC et ceux n'en ayant pas eu,
    - l'âge moyen des patients.

    Parameters
    ----------
    patients_all : list of dict
        Liste de dictionnaires représentant les patients. Chaque dictionnaire doit
        contenir au moins les clés `"age"`, `"gender"` et `"stroke"`.

    Returns
    -------
    pd.DataFrame
        DataFrame Pandas contenant les statistiques globales avec deux colonnes :
        `"Statistique"` et `"Valeur"`.

    Examples
    --------
    >>> patients = [
    ...     {"age": 60, "gender": "Male", "stroke": 1},
    ...     {"age": 45, "gender": "Female", "stroke": 0}
    ... ]
    >>> get_global_stats(patients)
                Statistique  Valeur
    0       Total patients    2
    1                Hommes    1
    2               Femmes    1
    3     Patients avec AVC    1
    4  Patients sans AVC    1
    5             Âge moyen   52.5
    """
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
