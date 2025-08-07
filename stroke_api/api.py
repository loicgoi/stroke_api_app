from fastapi import APIRouter, HTTPException
from .filters import filter_patient, stroke_data_df

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API Stroke Prediction !"}

# TODO décommenter et compléter
@router.get("/patients/")
def get_patients(gender: str = None, stroke: int = None, max_age: float = None):
    filtered_df = filter_patient(stroke = stroke, gender = gender, max_age = max_age)
    if not filtered_df:
        return{"message": "Aucun patient trouvé."}
    return filtered_df

# # TODO décommenter et compléter
@router.get("/patients/{patient_id}")
def get_patient_by_id(patient_id: int):
    patient = stroke_data_df[stroke_data_df['id'] == patient_id]
    if patient.empty:
        raise HTTPException(status_code=404, detail='Patient non trouvé')
    return patient.to_dict("records")[0]
    # Gérer le cas où l'id de patient passé en paramètre n'existe pas


# TODO Ajout de la route stats
@router.get("/stats/")
def get_stats():
    total = len(stroke_data_df)
    stroke_true = int(stroke_data_df['stroke'].sum())
    stroke_false = total - stroke_true
    gender_count = stroke_data_df['gender'].value_counts().to_dict()
    avg_age = float(stroke_data_df['age'].mean())

    return {
        "total_patients": total,
        "stroke_true": stroke_true,
        "stroke_false": stroke_false,
        "gender_distribution": gender_count,
        "average_age": round(avg_age, 2)
    }
