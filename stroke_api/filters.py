from typing import Optional
from pathlib import Path
import pandas as pd

# Chemin absolu depuis la racine du projet
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "stroke_data.parquet"

stroke_data_df = pd.read_parquet(DATA_PATH)

# Tester l'app avec :
# poetry run fastapi dev stroke_api/main.py
# http://127.0.0.1:8000/docs : utiliser la fonctionnalité Try it out pour tester les routes

# Ajout des fonctions de filtrage des données cf notebook 1
# Ensuite faire appel à ces fonctions dans le fichier api.py où sont définies les routes.

# Filtrer le dataframe pour ne garder que les patients pour lesquels "stroke=1"
def filtred_stroke(df, stroke):
    if 'stroke' in df.columns:
        return df.loc[df['stroke'] == stroke]
    else:
        return df


# Filtrer les données pour ne garder que les patients pour lesquels "gender="male"
def filtred_gender(df, gender):
    if 'gender' in df.columns:
        return df.loc[df['gender'].str.lower() == gender.lower()]
    else:
        return df


# Filtrer les données pour ne garder que les patients tels que "age <= max_age"
def filtred_max_age(df, max_age):
    if 'age' in df.columns:
        return df.loc[df['age'] <= max_age]
    else:
        return df 


def filter_patient(
    gender: Optional[str] = None, 
    stroke: Optional[int] = None, 
    max_age: Optional[int] = None
) -> list[dict]:
    
    df_filtered = stroke_data_df.copy()

    if gender is not None:
        df_filtered = filtred_gender(df_filtered, gender)
    if stroke is not None:
        df_filtered = filtred_stroke(df_filtered, stroke)
    if max_age is not None:
        df_filtered = filtred_max_age(df_filtered, max_age)
    if df_filtered.empty:
        print("Aucun patient ne correspond aux critères sélectionnés.")
    return df_filtered.to_dict('records')

# Ajouter les fonctions de filtrage pour les autres routes.

