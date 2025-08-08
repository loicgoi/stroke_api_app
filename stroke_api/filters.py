from typing import Optional
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "stroke_data.parquet"

stroke_data_df = pd.read_parquet(DATA_PATH)


def get_stroke_data() -> pd.DataFrame:
    return stroke_data_df.copy()


# --- filtres existants ---


def filtred_stroke(df: pd.DataFrame, stroke: int) -> pd.DataFrame:
    return df[df["stroke"] == stroke] if "stroke" in df.columns else df


def filtred_gender(df: pd.DataFrame, gender: str) -> pd.DataFrame:
    return (
        df[df["gender"].str.lower() == gender.lower()] if "gender" in df.columns else df
    )


def filtered_age_range(df: pd.DataFrame, min_age: int, max_age: int) -> pd.DataFrame:
    if "age" in df.columns:
        mask = (df["age"] >= min_age) & (df["age"] <= max_age)
        return df.loc[mask].copy()
    return df


# --- fonction principale appelée par Streamlit et l'API ---


def filter_patient(
    gender: Optional[str] = None,
    stroke: Optional[int] = None,
    min_age: Optional[int] = None,
    max_age: Optional[int] = None,
) -> list[dict]:
    df = stroke_data_df.copy()

    if gender is not None:
        df = filtred_gender(df, gender)
    if stroke is not None:
        df = filtred_stroke(df, stroke)
    if min_age is not None and max_age is not None:
        df = filtered_age_range(df, min_age, max_age)

    return df.to_dict("records")
