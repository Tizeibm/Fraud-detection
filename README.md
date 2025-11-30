![Python](https://img.shields.io/badge/Python-3.8-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68.1-blue)
![XGBoost](https://img.shields.io/badge/XGBoost-1.5.0-blue)

# Détection de Fraude Bancaire

## Description du Projet
L'application de détection de fraude bancaire permet d'analyser des transactions financières afin d'identifier des comportements suspects. Utilisant des techniques avancées de machine learning, cette application aide à prévenir les fraudes en temps réel. 

### Fonctionnalités Clés
- Détection automatique de fraudes à l'aide de modèles de machine learning.
- Interface de tableau de bord pour visualiser les résultats et les analyses.
- Support pour des ensembles de données réalistes pour l'entraînement et l'évaluation des modèles.

## Tech Stack

| Technologie      | Description                  |
|------------------|------------------------------|
| ![Python](https://img.shields.io/badge/Python-3.8-blue.svg) | Langage de programmation utilisé pour le développement. |
| ![FastAPI](https://img.shields.io/badge/FastAPI-0.68.1-blue) | Framework web pour créer des API rapidement et efficacement. |
| ![XGBoost](https://img.shields.io/badge/XGBoost-1.5.0-blue) | Bibliothèque de machine learning pour le modèle de détection de fraude. |

## Instructions d'Installation

### Prérequis
- Python 3.8 ou supérieur
- Pip (gestionnaire de paquets Python)

### Guide d'Installation
1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/Tizeibm/Fraud-detection.git
   cd Fraud-detection
   ```

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

### Configuration de l'Environnement
Aucune variable d'environnement spécifique n'a été détectée dans le code, mais assurez-vous que votre environnement Python est configuré correctement.

## Utilisation

### Lancer le Projet
Pour démarrer l'application FastAPI, exécutez le fichier `app_fastapi.py` :
```bash
python app_fastapi.py
```
L'application sera accessible à l'adresse `http://127.0.0.1:8000`.

### Exemples d'Utilisation
Vous pouvez interagir avec l'API via des requêtes HTTP. Par exemple, pour soumettre une transaction à analyser, utilisez un client HTTP comme `curl` ou Postman.

## Structure du Projet

Voici un aperçu de la structure du projet :

```
Fraud-detection/
├── app_fastapi.py          # Point d'entrée de l'application FastAPI
├── dashboard.py            # Script pour générer le tableau de bord
├── fraud_dataset_realistic_200k.csv  # Ensemble de données pour l'entraînement
├── fraud_model_xgboost.pkl # Modèle entraîné pour la détection de fraude
├── model_metadata.pkl      # Métadonnées du modèle
├── requirements.txt        # Liste des dépendances du projet
└── train_advanced.py       # Script pour entraîner le modèle
```

### Explication des Fichiers Principaux
- `app_fastapi.py` : Contient la logique principale de l'application et les routes de l'API.
- `dashboard.py` : Permet de visualiser les résultats de l'analyse.
- `fraud_dataset_realistic_200k.csv` : Fichier de données utilisé pour entraîner le modèle.
- `fraud_model_xgboost.pkl` : Fichier contenant le modèle de détection de fraude pré-entraîné.
- `requirements.txt` : Fichier listant toutes les bibliothèques nécessaires pour faire fonctionner l'application.

## Contribuer
Les contributions sont les bienvenues ! Pour contribuer, veuillez suivre ces étapes :
1. Fork ce dépôt.
2. Créez une nouvelle branche (`git checkout -b feature/YourFeature`).
3. Apportez vos modifications et validez-les (`git commit -m 'Ajout d'une nouvelle fonctionnalité'`).
4. Poussez vos changements (`git push origin feature/YourFeature`).
5. Ouvrez une Pull Request.

Merci de votre intérêt pour le projet de détection de fraude bancaire !
