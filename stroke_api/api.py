from fastapi import APIRouter, HTTPException
from .filters import filter_patient, stroke_data_df

router = APIRouter()


@router.get("/")
def read_root():
    """
    Route racine de l'API.

    Returns:
        dict: Message de bienvenue de l'API Stroke Prediction.
    """

    return {"message": "Bienvenue sur l'API Stroke Prediction !"}


@router.get("/patients/")
def get_patients(
    gender: str = None,
    stroke: int = None,
    min_age: int = None,
    max_age: int = None,
):
    """
    Récupère la liste des patients filtrée selon les critères fournis.

    Args:
        gender (str, optional): Filtrer par genre ("Male", "Female", etc.).
        stroke (int, optional): Filtrer par AVC (1 pour AVC, 0 sinon).
        min_age (int, optional): Âge minimum inclus pour le filtre.
        max_age (int, optional): Âge maximum inclus pour le filtre.

    Returns:
        list of dict or dict: Liste des patients correspondant aux filtres,
                              ou message si aucun patient n'est trouvé.

    Remarques :
    - Utilise la fonction `filter_patient` pour appliquer les filtres.
    """

    filtered = filter_patient(
        gender=gender,
        stroke=stroke,
        min_age=min_age,
        max_age=max_age,
    )
    if not filtered:
        return {"message": "Aucun patient trouvé."}
    return filtered


@router.get("/patients/{patient_id}")
def get_patient_by_id(patient_id: int):
    """
    Récupère un patient selon son ID.

    Args:
        patient_id (int): Identifiant unique du patient.

    Returns:
        dict: Dictionnaire représentant le patient correspondant à l'ID.

    Raises:
        HTTPException: Erreur 404 si aucun patient avec l'ID fourni n'est trouvé.

    Remarques :
    - Retourne le premier (et unique) enregistrement correspondant à l'ID.
    """

    patient = stroke_data_df[stroke_data_df["id"] == patient_id]
    if patient.empty:
        raise HTTPException(status_code=404, detail="Patient non trouvé")
    return patient.to_dict("records")[0]
    # Gérer le cas où l'id de patient passé en paramètre n'existe pas


@router.get("/stats/")
def get_stats():
    """
    Récupère les statistiques globales des patients.

    Returns:
        dict: Dictionnaire contenant les statistiques suivantes :
            - total_patients (int): Nombre total de patients
            - stroke_true (int): Nombre de patients ayant eu un AVC
            - stroke_false (int): Nombre de patients n'ayant pas eu d'AVC
            - gender_distribution (dict): Répartition des patients par genre
            - average_age (float): Âge moyen des patients, arrondi à 2 décimales

    Remarques :
    - Les calculs sont réalisés sur l'ensemble des patients présents dans `stroke_data_df`.
    """

    total = len(stroke_data_df)
    stroke_true = int(stroke_data_df["stroke"].sum())
    stroke_false = total - stroke_true
    gender_count = stroke_data_df["gender"].value_counts().to_dict()
    avg_age = float(stroke_data_df["age"].mean())

    return {
        "total_patients": total,
        "stroke_true": stroke_true,
        "stroke_false": stroke_false,
        "gender_distribution": gender_count,
        "average_age": round(avg_age, 2),
    }
