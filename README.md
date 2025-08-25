# Stroke Prediction Dataset - API REST avec FastAPI

## Objectif du projet

Développer une API REST permettant d'exposer les données patients d’un dataset médical afin qu’elles soient consultables par d’autres équipes (médecins, data scientists, analystes, etc.).

---

## Dataset utilisé

- **Source** : [Kaggle - Stroke Prediction Dataset](https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset)
- **Description** : Informations médicales et sociales sur des patients, avec comme objectif de prédire les risques d’AVC (stroke).

### Colonnes du dataset

| Colonne             | Description                                      |
| ------------------- | ------------------------------------------------ |
| `id`                | Identifiant unique du patient                    |
| `gender`            | Sexe du patient                                  |
| `age`               | Âge du patient                                   |
| `hypertension`      | Présence d’hypertension (0 = Non, 1 = Oui)       |
| `heart_disease`     | Présence de maladie cardiaque (0 = Non, 1 = Oui) |
| `ever_married`      | Statut marital                                   |
| `work_type`         | Type d’emploi                                    |
| `Residence_type`    | Milieu de vie : Urbain ou Rural                  |
| `avg_glucose_level` | Moyenne du taux de glucose                       |
| `bmi`               | Indice de masse corporelle                       |
| `smoking_status`    | Statut tabagique                                 |
| `stroke`            | Présence d’AVC (0 = Non, 1 = Oui)                |

**Télécharger les données** et les placer dans le dossier `data/`.

---

## Prétraitement des données

### Étapes réalisées

- Suppression des doublons
- Traitement des valeurs manquantes dans la colonne `bmi` via médiane conditionnelle
- Correction des valeurs aberrantes :
  - `work_type` pour les < 18 ans → `children`
  - `smoking_status` inconnu :
    - < 18 ans → `never smoked`
    - ≥ 18 ans → `not specified`
- Détection des outliers :
  - `avg_glucose_level` < 50 ou > 280
  - `bmi` < 10 ou > 80
- Sauvegarde des données nettoyées au format **Parquet** dans `data/stroke_data.parquet`

### Pourquoi Parquet ?

- Format compressé, léger et optimisé pour le Big Data
- Conserve les types de données
- Très performant pour des traitements sur gros volumes

---

## Fonctionnalités de l’API REST

Développée avec **FastAPI** + **Uvicorn**

| Méthode | Endpoint                                      | Description                                                              |
| ------- | --------------------------------------------- | ------------------------------------------------------------------------ |
| `GET`   | `/patients/{id}`                              | Retourne les infos d’un patient par son `id`                             |
| `GET`   | `/patients?stroke=1&gender=Female&max_age=60` | Filtre les patients par critères                                         |
| `GET`   | `/stats/`                                     | Statistiques globales : âge moyen, taux d’AVC, répartition hommes/femmes |

Documentation interactive générée automatiquement par Swagger UI :  
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Outils utilisés

| Outil       | Description                                       |
| ----------- | ------------------------------------------------- |
| **FastAPI** | Framework Python pour API REST, rapide et typé    |
| **Uvicorn** | Serveur ASGI pour exécuter FastAPI                |
| **Swagger** | Documentation interactive générée automatiquement |
| **Pandas**  | Manipulation des données pour le prétraitement    |
| **Poetry**  | Gestionnaire d'environnement Python + dépendances |

---

## Lancer le projet

```bash
poetry install
poetry run uvicorn stroke_api.main:app --reload

Fonctions de filtrage (exemple)
from typing import Optional
```

```python
def filter_patient(
    gender: Optional[str] = None,
    stroke: Optional[int] = None,
    max_age: Optional[int] = None
) -> list[dict]:
    df = stroke_data_df.copy()
    if gender is not None:
        df = df[df['gender'].str.lower() == gender.lower()]
    if stroke is not None:
        df = df[df['stroke'] == stroke]
    if max_age is not None:
        df = df[df['age'] <= max_age]
    return df.to_dict('records')
```

Tâches restantes

- [ ] Ajouter la route `/patients/{id}`
- [ ] Gérer les erreurs (404 si patient non trouvé, etc.)
- [ ] Ajouter des tests unitaires
- [ ] Créer un Dockerfile pour containeriser l’API

```markdown
Structure du projet
├── .gitignore
├── poetry.lock
├── pyproject.toml
├── README.md
├── data
│ ├── stroke_data.parquet
│ └── healthcare-dataset-stroke-data.csv
├── streamlit_app
│ ├── __init__.py
│ ├── app.py
│ ├── utils
│ │ ├── data_utils.py
│ │ ├── viz_utils.py
│ │ └── stats_utils.py
│ ├── modules
│ │ ├── visualisations.py
│ │ ├── statistiques.py
│ │ ├── accueil.py
│ │ ├── config.py
│ │ └── donnees.py
│ ├── .streamlit
│ │ └── config.toml
│ └── components
│ └── description_variables.py
└── stroke_api
├── api.py
├── main.py
├── __init__.py
├── filters.py
└── API_tuto.ipynb
```

Contribution

- Forker ce repo

- Créer une branche : feature/<nom>

- Créer une issue correspondante

- Soumettre une Pull Request claire

```

```
