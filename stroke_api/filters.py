from typing import Optional
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "stroke_data.parquet"

stroke_data_df = pd.read_parquet(DATA_PATH)


def get_stroke_data() -> pd.DataFrame:
    """
    Retourne une copie du DataFrame contenant les données des patients.

    Returns:
        pd.DataFrame: DataFrame complet des patients, prêt à être utilisé
                      ou filtré sans modifier l'original.
    """
    return stroke_data_df.copy()


def filtred_stroke(df: pd.DataFrame, stroke: int) -> pd.DataFrame:
    """
    Filtre un DataFrame selon la colonne 'stroke'.

    Args:
        df (pd.DataFrame): DataFrame des patients.
        stroke (int): Valeur du champ 'stroke' à filtrer (1 pour AVC, 0 sinon).

    Returns:
        pd.DataFrame: DataFrame filtré contenant uniquement les lignes avec
                      la valeur de 'stroke' spécifiée. Si la colonne n'existe
                      pas, renvoie le DataFrame inchangé.
    """

    return df[df["stroke"] == stroke] if "stroke" in df.columns else df


def filtred_gender(df: pd.DataFrame, gender: str) -> pd.DataFrame:
    """
    Filtre un DataFrame selon la colonne 'gender'.

    Args:
        df (pd.DataFrame): DataFrame des patients.
        gender (str): Genre à filtrer ("Male", "Female", etc.).

    Returns:
        pd.DataFrame: DataFrame filtré contenant uniquement les lignes
                      correspondant au genre spécifié. Si la colonne n'existe
                      pas, renvoie le DataFrame inchangé.
    """
    return (
        df[df["gender"].str.lower() == gender.lower()] if "gender" in df.columns else df
    )


def filtered_age_range(df: pd.DataFrame, min_age: int, max_age: int) -> pd.DataFrame:
    """
    Filtre un DataFrame pour ne conserver que les patients dont l'âge
    se situe dans une plage donnée.

    Args:
        df (pd.DataFrame): DataFrame des patients.
        min_age (int): Âge minimum inclus.
        max_age (int): Âge maximum inclus.

    Returns:
        pd.DataFrame: DataFrame filtré contenant uniquement les patients
                      dont l'âge est compris entre min_age et max_age.
                      Si la colonne 'age' n'existe pas, renvoie le DataFrame inchangé.
    """

    if "age" in df.columns:
        mask = (df["age"] >= min_age) & (df["age"] <= max_age)
        return df.loc[mask].copy()
    return df


def filter_patient(
    gender: Optional[str] = None,
    stroke: Optional[int] = None,
    min_age: Optional[int] = None,
    max_age: Optional[int] = None,
) -> list[dict]:
    """
    Filtre les patients selon plusieurs critères et retourne la liste des résultats.

    Args:
        gender (str, optional): Genre à filtrer ("Male", "Female", etc.).
        stroke (int, optional): Filtre AVC (1 pour AVC, 0 sinon).
        min_age (int, optional): Âge minimum inclus pour le filtre.
        max_age (int, optional): Âge maximum inclus pour le filtre.

    Returns:
        list of dict: Liste de dictionnaires représentant les patients filtrés,
                      chaque dictionnaire correspondant à une ligne du DataFrame.

    Remarques :
    - Les filtres sont appliqués uniquement si les valeurs correspondantes sont fournies.
    - Utilise les fonctions `filtred_gender`, `filtred_stroke` et `filtered_age_range`.
    - Le DataFrame original `stroke_data_df` n'est jamais modifié.
    """

    df = stroke_data_df.copy()

    if gender is not None:
        df = filtred_gender(df, gender)
    if stroke is not None:
        df = filtred_stroke(df, stroke)
    if min_age is not None and max_age is not None:
        df = filtered_age_range(df, min_age, max_age)

    return df.to_dict("records")
