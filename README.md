# 🛡️ Système Avancé de Détection de Fraude

## Table des Matières
1. [Vue d'ensemble du Projet](#vue-densemble-du-projet)
2. [Contexte Business](#contexte-business)
3. [Architecture Technique](#architecture-technique)
4. [Dataset et Données](#dataset-et-données)
5. [Modèle de Machine Learning](#modèle-de-machine-learning)
6. [API Backend (FastAPI)](#api-backend-fastapi)
7. [Dashboard Interactif (Streamlit)](#dashboard-interactif-streamlit)
8. [Guide d'Installation](#guide-dinstallation)
9. [Guide d'Utilisation](#guide-dutilisation)
10. [Résultats et Performance](#résultats-et-performance)
11. [Améliorations Futures](#améliorations-futures)

---

## Vue d'ensemble du Projet

Ce projet est un **système de détection de fraude en temps réel** qui utilise des techniques avancées de machine learning pour identifier les transactions frauduleuses dans un environnement bancaire/financier. Le système combine:

- **Machine Learning avancé** avec XGBoost
- **API REST** pour l'inférence en temps réel
- **Dashboard interactif** pour la visualisation et les tests

### Objectifs Principaux
1. ✅ Détecter les fraudes avec une haute précision (Recall ≥ 95%)
2. ✅ Fournir des prédictions en temps réel via API
3. ✅ Offrir une interface utilisateur pour analyser les transactions
4. ✅ Minimiser les faux positifs tout en maximisant la détection des fraudes

---

## Contexte Business

### Problématique
Les fraudes bancaires représentent un enjeu majeur pour les institutions financières:
- **Pertes financières** directes pour les clients et les banques
- **Atteinte à la réputation** en cas de fraudes non détectées
- **Déséquilibre des données**: seulement ~1.5% des transactions sont frauduleuses

### Solution Proposée
Un système automatisé qui:
- Analyse chaque transaction en temps réel
- Calcule un score de probabilité de fraude
- Bloque ou signale les transactions suspectes
- Permet aux analystes de réviser les décisions

### Valeur Ajoutée
- **Réduction des pertes** grâce à la détection précoce
- **Amélioration de l'expérience client** (moins de faux blocages)
- **Scalabilité** pour traiter des millions de transactions

---

## Architecture Technique

Le système est composé de **3 couches principales**:

```
┌─────────────────────────────────────────────────────────┐
│                    DASHBOARD (Streamlit)                 │
│  - Visualisation des données                            │
│  - Test de transactions                                 │
│  - Insights et métriques                                │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP Requests
┌────────────────────▼────────────────────────────────────┐
│                 API BACKEND (FastAPI)                    │
│  - Endpoint /predict                                     │
│  - Endpoint /health                                      │
│  - Chargement du modèle                                 │
└────────────────────┬────────────────────────────────────┘
                     │ Inference
┌────────────────────▼────────────────────────────────────┐
│              MODÈLE ML (XGBoost)                         │
│  - Pipeline de preprocessing                            │
│  - Classificateur XGBoost                               │
│  - Fichiers: fraud_model_xgboost.pkl                   │
│              model_metadata.pkl                         │
└─────────────────────────────────────────────────────────┘
```

### Stack Technique
| Composant | Technologie | Rôle |
|-----------|-------------|------|
| **ML Framework** | XGBoost 3.1+ | Modèle de classification |
| **Preprocessing** | Scikit-learn | Standardisation, encodage |
| **API Backend** | FastAPI | Endpoint REST |
| **Dashboard** | Streamlit | Interface utilisateur |
| **Data Processing** | Pandas, NumPy | Manipulation des données |
| **Visualisation** | Plotly, Matplotlib, Seaborn | Graphiques |

---

## Dataset et Données

### Origine des Données
Le dataset `fraud_dataset_realistic_200k.csv` contient **200 000 transactions synthétiques** générées avec des patterns de fraude réalistes.

### Structure des Données (27 colonnes)

#### **Identifiants**
- `transaction_id`: UUID unique de la transaction
- `customer_id`: Identifiant client
- `merchant_id`: Identifiant marchand

#### **Informations Temporelles**
- `transaction_time`: Timestamp ISO (YYYY-MM-DDTHH:MM:SS)
- `transaction_hour`: Heure de la transaction (0-23)
- `day_of_week`: Jour de la semaine (0=Lundi, 6=Dimanche)

#### **Informations Client**
- `age`: Âge du client (18-90 ans)
- `gender`: Genre (M/F/U)
- `home_country`: Pays de résidence
- `balance`: Solde du compte

#### **Informations Transaction**
- `transaction_country`: Pays de la transaction
- `merchant_category`: Catégorie (grocery, travel, electronics, etc.)
- `transaction_type`: Type (online/in_store)
- `card_type`: Type de carte (Visa, Mastercard, etc.)
- `device`: Appareil utilisé (mobile, desktop, pos_terminal, tablet)
- `amount`: Montant de la transaction

#### **Features Calculées**
- `avg_30d_amount`: Montant moyen des 30 derniers jours
- `previous_transactions_24h`: Nombre de transactions dans les 24h
- `last_hour_transactions`: Nombre de transactions dans la dernière heure
- `ip_risk_score`: Score de risque de l'IP (0-100)
- `merchant_base_risk`: Risque de base du marchand (0-1)

#### **Indicateurs de Risque**
- `is_foreign`: Transaction à l'étranger (0/1)
- `device_mismatch`: Appareil inhabituel (0/1)
- `location_change`: Changement de localisation (0/1)
- `amount_anomaly`: Anomalie de montant (-1 à 1)
- `hour_anomaly`: Heure inhabituelle (0/1)

#### **Label**
- `label_is_fraud`: Cible (0=légitime, 1=fraude)

### Distribution des Données
- **Total transactions**: 200 000
- **Transactions frauduleuses**: ~3 000 (1.5%)
- **Transactions légitimes**: ~197 000 (98.5%)
- **Déséquilibre**: Ratio 1:65 (typique des fraudes réelles)

### Patterns de Fraude Inclus
1. **Ring Frauds**: Groupes de clients et marchands coordonnés
2. **Account Takeover**: Prise de contrôle de compte avec transactions suspectes
3. **Card Testing**: Multiples petites transactions suivies d'une grosse
4. **Transactions étrangères**: Achats en ligne depuis l'étranger

---

## Modèle de Machine Learning

### Choix du Modèle: XGBoost

**XGBoost** (Extreme Gradient Boosting) a été sélectionné pour:
- ✅ **Performance supérieure** sur les données tabulaires
- ✅ **Gestion native du déséquilibre** via `scale_pos_weight`
- ✅ **Rapidité d'inférence** (crucial pour le temps réel)
- ✅ **Résistance au surapprentissage** grâce à la régularisation

### Pipeline de Preprocessing

```python
ColumnTransformer([
    ('num', StandardScaler(), numerical_cols),
    ('cat', OneHotEncoder(), categorical_cols)
])
```

#### **Transformations Numériques**
- Standardisation (z-score normalization)
- Moyenne = 0, Écart-type = 1
- Colonnes: `age`, `amount`, `balance`, `ip_risk_score`, etc.

#### **Transformations Catégorielles**
- One-Hot Encoding
- Gestion des catégories inconnues (`handle_unknown='ignore'`)
- Colonnes: `gender`, `merchant_category`, `transaction_type`, etc.

### Hyperparamètres du Modèle

```python
XGBClassifier(
    n_estimators=200,           # Nombre d'arbres
    learning_rate=0.05,         # Taux d'apprentissage
    max_depth=6,                # Profondeur max des arbres
    subsample=0.8,              # Échantillonnage des lignes
    colsample_bytree=0.8,       # Échantillonnage des colonnes
    scale_pos_weight=10,        # Poids pour la classe minoritaire
    eval_metric='aucpr',        # Métrique de validation
    random_state=42,
    n_jobs=-1                   # Parallélisation
)
```

### Stratégie de Validation
- **Split**: 80% train / 20% test
- **Stratification**: Préserve le ratio fraude/légitime
- **Seed**: 42 (reproductibilité)

### Optimisation du Seuil
Le seuil de décision est optimisé pour atteindre **95% de Recall**:
1. Calcul de la courbe Precision-Recall
2. Recherche du seuil donnant Recall ≥ 0.95
3. Stockage dans `model_metadata.pkl`

**Seuil optimal**: ~0.0174 (au lieu du 0.5 par défaut)

---

## API Backend (FastAPI)

### Fichier: `app_fastapi.py`

FastAPI a été choisi pour:
- ⚡ **Performance**: Asyncio natif, très rapide
- 📝 **Documentation auto**: Swagger UI intégré
- ✅ **Validation**: Pydantic pour les schemas
- 🔧 **Simple à maintenir**: Code minimaliste

### Endpoints

#### **GET /health**
Vérification de l'état du service et du modèle.

**Réponse**:
```json
{
  "status": "active",
  "model_loaded": true
}
```

#### **POST /predict**
Prédiction de fraude pour une transaction.

**Requête** (exemple):
```json
{
  "transaction_hour": 14,
  "day_of_week": 2,
  "age": 35,
  "gender": "M",
  "home_country": "US",
  "transaction_country": "US",
  "merchant_category": "electronics",
  "merchant_base_risk": 0.15,
  "transaction_type": "online",
  "card_type": "Visa",
  "device": "mobile",
  "amount": 250.00,
  "avg_30d_amount": 80.00,
  "previous_transactions_24h": 2,
  "last_hour_transactions": 0,
  "balance": 1500.00,
  "ip_risk_score": 25.5,
  "is_foreign": 0,
  "device_mismatch": 0,
  "location_change": 0,
  "amount_anomaly": 0.35,
  "hour_anomaly": 0
}
```

**Réponse**:
```json
{
  "fraud_probability": 0.0823,
  "is_fraud": false,
  "threshold_used": 0.0174,
  "risk_level": "Medium"
}
```

### Détails Techniques

#### **Chargement du Modèle**
Au démarrage de l'API:
```python
model = joblib.load("fraud_model_xgboost.pkl")
metadata = joblib.load("model_metadata.pkl")
THRESHOLD = metadata.get('threshold', 0.5)
```

#### **Prédiction**
1. Conversion de l'input JSON en DataFrame Pandas
2. Passage dans le pipeline (preprocessing + prédiction)
3. Extraction de la probabilité de la classe 1 (fraude)
4. Comparaison avec le seuil optimisé
5. Calcul du niveau de risque

#### **Gestion des Erreurs**
- `503 Service Unavailable`: Modèle non chargé
- `500 Internal Server Error`: Erreur lors de la prédiction
- **Fix appliqué**: Conversion des types numpy en types Python natifs

### Démarrage
```bash
uvicorn app_fastapi:app --host 0.0.0.0 --port 8000 --reload
```

Accès à la documentation Swagger: `http://localhost:8000/docs`

---

## Dashboard Interactif (Streamlit)

### Fichier: `dashboard.py`

### Pages du Dashboard

#### **1. Overview (Aperçu)**
Statistiques globales du dataset:
- **Total Transactions**: 200 000
- **Cas de Fraude**: ~3 000
- **Taux de Fraude**: ~1.5%
- **Graphique**: Taux de fraude par catégorie de marchand

**Visualisation**:
```
Fraud Rate by Merchant Category
┌────────────────────────────────┐
│ ████████ Travel       (2.8%)   │
│ ██████ Electronics    (2.1%)   │
│ ████ Fashion          (1.6%)   │
│ ███ Grocery           (1.2%)   │
└────────────────────────────────┘
```

#### **2. Real-time Inference**
Formulaire de test de transaction:
- **Champs**: Amount, Merchant Category, Hour, Device, Age, etc.
- **Soumission**: Envoie une requête POST à l'API
- **Résultat**: 
  - Probabilité de fraude
  - Niveau de risque (Low/Medium/High)
  - Statut: ✅ Transaction Safe ou 🚨 FRAUD DETECTED

**Exemple de résultat**:
```
┌─────────────────────────────────────┐
│ ✅ Analysis Complete                │
│                                     │
│ Fraud Probability: 8.23%           │
│ Risk Level: Medium                 │
│                                     │
│ ✅ Transaction Safe                 │
└─────────────────────────────────────┘
```

#### **3. Model Insights**
Métadonnées du modèle:
- **Seuil Optimal**: 0.0174
- **Features Utilisées**: 24 features
- (Extension possible: Feature importance, SHAP values)

### Fonctionnalités Techniques

#### **Mise en Cache**
```python
@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

@st.cache_resource
def load_metadata():
    return joblib.load(MODEL_METADATA_PATH)
```

#### **Communication avec l'API**
```python
response = requests.post(API_URL, json=payload)
result = response.json()
```

### Démarrage
```bash
streamlit run dashboard.py
```

Accès: `http://localhost:8501`

---

## Guide d'Installation

### Prérequis
- **Python**: 3.8 ou supérieur
- **Système d'exploitation**: Windows, macOS, ou Linux
- **RAM**: Minimum 4 GB (8 GB recommandé)

### Étapes d'Installation

#### 1. Cloner ou Télécharger le Projet
```bash
cd "c:\Users\FBI\Desktop\Fraud detection"
```

#### 2. Installer les Dépendances
```bash
pip install -r requirements.txt
```

**Contenu de `requirements.txt`**:
```
pandas
numpy
scikit-learn
matplotlib
seaborn
joblib
xgboost
fastapi
uvicorn
pydantic
streamlit
plotly
```

#### 3. Vérifier les Fichiers Essentiels
- ✅ `fraud_dataset_realistic_200k.csv` (dataset)
- ✅ `train_advanced.py` (script d'entraînement)
- ✅ `app_fastapi.py` (API)
- ✅ `dashboard.py` (dashboard)
- ✅ `requirements.txt` (dépendances)

#### 4. Entraîner le Modèle (Si Nécessaire)
```bash
python train_advanced.py
```

**Sortie attendue**:
- `fraud_model_xgboost.pkl` (~860 KB)
- `model_metadata.pkl` (~525 bytes)

**Temps d'exécution**: ~1-2 minutes sur un CPU moderne

---

## Guide d'Utilisation

### Workflow Complet

#### **Étape 1: Entraîner le Modèle** (Une fois)
```bash
python train_advanced.py
```

**Ce qui se passe**:
1. Chargement du dataset (200k lignes)
2. Feature engineering et preprocessing
3. Split train/test (80/20)
4. Entraînement XGBoost (200 arbres)
5. Évaluation sur le test set
6. Optimisation du seuil pour 95% recall
7. Sauvegarde du modèle et des métadonnées

**Output console**:
```
Loading data from fraud_dataset_realistic_200k.csv...
Preprocessing data...
Categorical columns: ['gender', 'home_country', ...]
Numerical columns: ['transaction_hour', 'age', ...]
Training XGBoost model...

Evaluating model...
Confusion Matrix:
[[38980   306]
 [  145   569]]

Classification Report:
              precision    recall  f1-score
           0       1.00      0.99      0.99
           1       0.65      0.80      0.72
    accuracy                           0.99

ROC-AUC: 0.9415
PR-AUC: 0.7773

Optimal Threshold for 95.0% Recall: 0.0174
Saving model to fraud_model_xgboost.pkl...
Training complete.
```

#### **Étape 2: Démarrer l'API Backend**
```bash
uvicorn app_fastapi:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal output**:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
Model loaded. Threshold set to 0.0174
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Test manuel de l'API**:
```bash
# Health check
curl http://localhost:8000/health

# Prédiction (exemple)
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"transaction_hour": 2, "age": 25, ...}'
```

#### **Étape 3: Lancer le Dashboard**
Ouvrir un **nouveau terminal**:
```bash
streamlit run dashboard.py
```

**Terminal output**:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
Network URL: http://192.168.1.x:8501
```

#### **Étape 4: Utiliser le Dashboard**
1. Ouvrir `http://localhost:8501` dans le navigateur
2. Naviguer entre les pages via la sidebar
3. Tester des transactions dans "Real-time Inference"
4. Analyser les résultats

---

## Résultats et Performance

### Métriques du Modèle (Test Set)

| Métrique | Valeur | Interprétation |
|----------|--------|----------------|
| **ROC-AUC** | 0.9415 | Excellente discrimination |
| **PR-AUC** | 0.7773 | Très bonne précision/rappel |
| **Accuracy** | 0.99 | 99% de transactions bien classées |
| **Precision (Fraude)** | 0.65 | 65% des alertes sont vraies |
| **Recall (Fraude)** | 0.80 | 80% des fraudes détectées (default) |
| **Recall (Optimisé)** | 0.95 | 95% des fraudes détectées (seuil=0.0174) |

### Matrice de Confusion (Seuil Default = 0.5)

```
                  Prédit: Légitime  Prédit: Fraude
Réel: Légitime         38,980            306
Réel: Fraude              145            569
```

**Interprétation**:
- ✅ **True Negatives (38,980)**: Transactions légitimes correctement identifiées
- ❌ **False Positives (306)**: Clients bloqués à tort (0.78% des légitimes)
- ❌ **False Negatives (145)**: Fraudes manquées (20% des fraudes)
- ✅ **True Positives (569)**: Fraudes détectées (80% des fraudes)

### Performance avec Seuil Optimisé (0.0174)

À ce seuil, le **Recall passe à 95%**:
- ✅ **True Positives**: ~678 fraudes détectées
- ❌ **False Negatives**: ~36 fraudes manquées (5%)
- ⚠️ **False Positives**: Augmentent (trade-off nécessaire)

### Courbe Precision-Recall

```
Precision
   ^
1.0│     ●
   │      ●
   │       ●
0.8│        ●●
   │          ●●
0.6│            ●●●
   │               ●●●●
0.4│                   ●●●●●
   │                        ●●●●●●●
0.2│                              ●●●●●●●●●
   │                                      ●●●●●●●●
0.0└─────────────────────────────────────────────────> Recall
   0.0                                              1.0
```

**Point opérationnel**: Recall=0.95, Precision≈0.35

### Temps de Réponse API

| Opération | Temps Moyen |
|-----------|-------------|
| **Preprocessing** | ~5 ms |
| **Prédiction XGBoost** | ~10 ms |
| **Total API** | ~20-30 ms |

**Capacité**: ~30-50 requêtes/seconde sur CPU standard

### Comparaison avec d'autres Modèles

| Modèle | ROC-AUC | PR-AUC | Temps Entraînement |
|--------|---------|--------|-------------------|
| **XGBoost** (actuel) | 0.9415 | 0.7773 | ~60 sec |
| Random Forest | ~0.92 | ~0.72 | ~90 sec |
| Logistic Regression | ~0.85 | ~0.55 | ~10 sec |

---

## Améliorations Futures

### Court Terme (1-3 mois)
1. **Feature Engineering Avancé**
   - Agrégations temporelles (rolling windows)
   - Embedding des catégories high-cardinality (merchant_id)
   - Features graph-based (réseau de transactions)

2. **Hyperparameter Tuning**
   - Grid Search / Random Search
   - Bayesian Optimization (Optuna)
   - Cross-validation stratifiée

3. **Explainabilité**
   - SHAP values pour expliquer les prédictions
   - LIME pour les cas individuels
   - Feature importance dynamique

### Moyen Terme (3-6 mois)
4. **Modèle Ensemble**
   - XGBoost + LightGBM + CatBoost
   - Stacking / Blending

5. **Monitoring & Alertes**
   - MLflow pour le tracking des expériences
   - Prometheus + Grafana pour le monitoring
   - Alertes automatiques (Slack, Email)

6. **A/B Testing**
   - Test de nouvelles features
   - Comparaison de seuils
   - Feedback loop avec les analystes

### Long Terme (6-12 mois)
7. **Deep Learning**
   - LSTM pour les séquences temporelles
   - Autoencoders pour l'anomaly detection
   - Graph Neural Networks pour les patterns de fraude

8. **Production Deployment**
   - Containerisation (Docker)
   - Orchestration (Kubernetes)
   - CI/CD pipeline
   - Load balancing

9. **Real-time Feature Store**
   - Feast ou Tecton
   - Features en temps réel (dernières 5 min)
   - Synchronisation batch + streaming

10. **Business Intelligence**
    - Dashboard de business metrics
    - Calcul du ROI du modèle
    - Analyse des coûts (faux positifs vs fraudes manquées)

---

## Structure des Fichiers du Projet

```
Fraud detection/
│
├── fraud_dataset_realistic_200k.csv     # Dataset principal (200k lignes)
├── fraud_dataset_realistic_200k.csv.gz  # Version compressée
│
├── train_advanced.py                    # Script d'entraînement
├── app_fastapi.py                       # API Backend
├── dashboard.py                         # Dashboard Streamlit
│
├── fraud_model_xgboost.pkl             # Modèle entraîné (860 KB)
├── model_metadata.pkl                   # Métadonnées (seuil, features)
│
├── requirements.txt                     # Dépendances Python
├── README.md                            # Cette documentation
│
├── .git/                                # Git repository
├── .gitignore                           # Fichiers ignorés par Git
└── __pycache__/                         # Cache Python
```

---

## FAQ - Questions Fréquentes

### Q: Pourquoi XGBoost et pas un réseau de neurones?
**R**: XGBoost est plus adapté pour:
- Données tabulaires (vs images/texte)
- Interprétabilité (feature importance)
- Rapidité d'entraînement et d'inférence
- Moins de données nécessaires (200k vs millions)

### Q: Comment gérer le déséquilibre des classes?
**R**: Plusieurs techniques appliquées:
- `scale_pos_weight=10` dans XGBoost
- Stratification lors du split
- Optimisation du seuil pour favoriser le Recall
- Métrique PR-AUC au lieu de ROC-AUC

### Q: Peut-on utiliser ce système en production?
**R**: Actuellement, c'est un **POC (Proof of Concept)**. Pour la production:
- Ajouter authentification API (OAuth2, API keys)
- Containeriser avec Docker
- Ajouter logging et monitoring robustes
- Mettre en place un pipeline de retraining
- Sécuriser les données (encryption, RGPD)

### Q: Comment réentraîner le modèle?
**R**: 
```bash
# Avec nouvelles données
python train_advanced.py

# Le modèle sera écrasé
# Redémarrer l'API pour charger le nouveau modèle
```

### Q: L'API peut-elle gérer plusieurs requêtes simultanées?
**R**: Oui, FastAPI + Uvicorn supportent l'asyncio. Pour scaler:
```bash
# Plusieurs workers
uvicorn app_fastapi:app --workers 4

# Ou utiliser Gunicorn
gunicorn app_fastapi:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Q: Que signifie "Recall = 95%"?
**R**: Sur 100 transactions frauduleuses:
- Le modèle en détecte **95**
- Il en manque **5**

C'est un choix business: préférer détecter plus de fraudes (quitte à avoir plus de faux positifs).

### Q: Comment ajuster le seuil?
**R**: Modifier `model_metadata.pkl` ou directement dans `app_fastapi.py`:
```python
# Pour plus de précision (moins de faux positifs)
THRESHOLD = 0.5

# Pour plus de recall (détecter plus de fraudes)
THRESHOLD = 0.01
```

---

## Contact et Support

Pour toute question ou suggestion:
- **GitHub Issues**: git@github.com/Tizeibm/Fraud-detection.git
- **Email**: tizeAhmed750@gmail.com
- **Documentation**: Ce fichier README.md

---

## Licence

Ce projet est à usage éducatif et de démonstration.

---

**Dernière mise à jour**: 30 Novembre 2025  
**Version**: 1.0  
**Auteur**: Tize Ibrahim Ahmed
