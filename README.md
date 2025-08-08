Stroke data project
===================

Ce projet contient les fichiers nécessaires au brief Stroke data - Développement d'une API REST et visualisation.


Voici un exemple clair et structuré de `README.md` pour ton projet dans VSCode, basé sur tout ce que tu as partagé :

---

#  Stroke Prediction Dataset - API REST avec FastAPI

## Objectif du projet

Développer une API REST permettant d'exposer les données patients d’un dataset médical afin qu’elles soient consultables par d’autres équipes (médecins, data scientists, analystes, etc.).

---

## Dataset utilisé

* **Source** : [Kaggle - Stroke Prediction Dataset]
* **Description** : Informations médicales et sociales sur des patients, avec comme objectif de prédire les risques d’AVC (stroke).

###  Colonnes du dataset

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

📥 **Télécharger les données** et les placer dans le dossier `data/`.

---

##  Prétraitement des données

### Étapes réalisées :

* Suppression des doublons
* Traitement des valeurs manquantes dans la colonne `bmi` via médiane conditionnelle (par genre, âge, résidence, etc.)
* Correction des valeurs aberrantes (incohérentes) :

  * `work_type` pour les < 18 ans → `children`
  * `smoking_status` inconnu :

    * < 18 ans → `never smoked`
    * ≥ 18 ans → `not specified`
* Détection des outliers :

  * `avg_glucose_level` < 50 ou > 280
  * `bmi` < 10 ou > 80
* Sauvegarde des données nettoyées au format **Parquet** dans `data/stroke_data.parquet`

### Pourquoi Parquet ?

* Format compressé, léger, optimisé pour le Big Data
* Conserve les types de données
* Très utile pour des traitements performants sur gros volumes

## Fonctionnalités de l’API REST

Développée avec **FastAPI** + **Uvicorn**

| Méthode | Endpoint                                      | Description                                                               |
| ------: | --------------------------------------------- | ------------------------------------------------------------------------- |
|   `GET` | `/patients/{id}`                              | Retourne les infos d’un patient par son `id`                              |
|   `GET` | `/patients?stroke=1&gender=Female&max_age=60` | Filtre les patients par critères                                          |
|   `GET` | `/stats/`                                     | Statistiques globales : âge moyen, taux d’AVC, répartition hommes/femmes… |

Documentation interactive générée automatiquement par Swagger UI :
Accès via [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

##  Outils utilisés

| Outil       | Description                                                   |
| ----------- | ------------------------------------------------------------- |
| **FastAPI** | Framework Python pour API REST, rapide et typé                |
| **Uvicorn** | Serveur ASGI pour exécuter FastAPI                            |
| **Swagger** | Documentation interactive générée automatiquement par FastAPI |
| **Pandas**  | Manipulation des données pour le prétraitement                |
| **Poetry**  | Gestionnaire d'environnement Python + dépendances             |

---

##  Lancer le projet

```bash
poetry run fastapi dev stroke_api/main.py
```

📍 Accès à la documentation Swagger UI :
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

##  Fonctions de filtrage

```python
from typing import Optional

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

---

## Tâches restantes (à suivre sur GitHub Issues)

* [ ] Ajouter la route `/patients/{id}`
* [ ] Ajouter la route `/stats/` avec calculs :

  * âge moyen
  * taux d’AVC
  * répartition par genre
* [ ] Gérer les erreurs (404 si patient non trouvé, etc.)
* [ ] Ajouter des tests unitaires
* [ ] Créer un `Dockerfile` pour containeriser l’API
* [ ] Créer des branches par feature (`feature/route-stats`, `feature/id-route`, etc.)

---

##  Quelques définitions

### 🔁 Qu’est-ce qu’une API REST ?

* Une **API (Application Programming Interface)** permet à des logiciels de communiquer.
* **REST (Representational State Transfer)** est un style d’architecture d’API.

###  Principes REST

* Protocole HTTP (`GET`, `POST`, `PUT`, `DELETE`)
* Représentations en JSON
* URLs claires pour accéder aux ressources
* Stateless : aucune mémoire des requêtes précédentes
* Codes HTTP (200, 404, etc.) pour indiquer le résultat

---

##  Structure du projet

```
stroke_api/
│
├── data/
│   └── stroke_data.parquet          # Données prétraitées
├─API_tuto.ipnyb                     # Exécutions des fontions 
├── filters.py                       # Fonctions de filtrage
├── main.py                          # Fichier principal FastAPI
├── utils.py                         # Fonctions utilitaires (si besoin)
├── README.md                        # Explications des requetes qui sont réalisé
```

---

##  Contribution

* Forker ce repo
* Créer une branche : `feature/<nom>`
* Créer une issue correspondante
* Soumettre une Pull Request claire

