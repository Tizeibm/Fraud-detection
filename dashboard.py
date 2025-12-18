import streamlit as st
import pandas as pd
import requests
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Configuration
API_URL = "http://localhost:8000/predict"
DATA_PATH = "fraud_dataset_realistic_200k.csv"
MODEL_METADATA_PATH = "model_metadata.pkl"

st.set_page_config(page_title="Détection de Fraude Bancaire", layout="wide")

st.title("🛡️ Système Détection de Fraude")

# Barre latérale
st.sidebar.header("Navigation")
page = st.sidebar.radio("Aller à", ["Vue d'ensemble", "Inférence Temps Réel", "Performance du Modèle"])

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

@st.cache_resource
def load_metadata():
    try:
        return joblib.load(MODEL_METADATA_PATH)
    except:
        return None

if page == "Vue d'ensemble":
    st.header("Aperçu du Dataset")
    df = load_data()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total des Transactions", f"{len(df):,}")
    col2.metric("Cas de Fraude", f"{df['label_is_fraud'].sum():,}")
    col3.metric("Taux de Fraude", f"{df['label_is_fraud'].mean()*100:.2f}%")

    st.subheader("Fraude par Catégorie")
    fig = px.bar(df.groupby('merchant_category')['label_is_fraud'].mean().reset_index(),
                 x='merchant_category', y='label_is_fraud',
                 title="Taux de Fraude par Catégorie de Marchand")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Inférence Temps Réel":
    st.header("Tester une Transaction")

    with st.form("prediction_form"):
        col1, col2 = st.columns(2)

        with col1:
            amount = st.number_input("Montant", min_value=0.0, value=100.0)
            merchant_category = st.selectbox("Catégorie du Marchand", ["electronics", "travel", "grocery", "fashion", "entertainment"])
            transaction_hour = st.slider("Heure de la Journée", 0, 23, 12)
            is_foreign = st.selectbox("Transaction à l'Étranger ?", ['Oui', 'Non'])
            if is_foreign == 'Oui':
                is_foreign = 1
            else:
                is_foreign = 0
            card_type = st.selectbox("Type de carte", ['Visa', 'Mastercard', 'Amex', 'Discover'])
            

        with col2:
            age = st.number_input("Âge du Client", 18, 100, 30)
            device = st.selectbox("Appareil", ["mobile", "desktop", "tablet"])
            balance = st.number_input("Solde compte", 0.0, 100000.0, 2000.0)
            #transaction_type = st.selectbox("Type de transaction", ['En ligne', 'Bancaire'])
            #if transaction_type == 'En ligne':
            #    transaction_type = "online"
            #else:
            #    transaction_type = "in_store"
        # Champs cachés/par défaut pour simplifier ce formulaire de démo
        # Dans une vraie application, ces valeurs seraient calculées ou récupérées
            last_transaction_hour = st.number_input("Nombre de transcation il y a une heure", 0, 10000, 0)
            previous_transactions_24h = st.number_input("Nombre de transcation il y a 24H", 0, 10000, 0)

        submit = st.form_submit_button("Analyser la Transaction")

        if submit:
            # Construction de la requête correspondant aux attentes de l'API
            # Note : Nous devons correspondre au schéma exact de TransactionInput dans app_fastapi.py
            # Pour cette démo, nous simulons les champs manquants avec des valeurs moyennes/par défaut
            payload = {
                "transaction_hour": transaction_hour,
                "day_of_week": 0, # Par défaut
                "age": age,
                "gender": "M", # Par défaut
                "home_country": "US",
                "transaction_country": "CMR" if is_foreign == 0 else "US",
                "merchant_category": merchant_category,
                "merchant_base_risk": 0.1, # Par défaut
                "transaction_type": 'online',
                "card_type": card_type,
                "device": device,
                "amount": amount,
                "avg_30d_amount": 100.0, # Par défaut
                "previous_transactions_24h": previous_transactions_24h,
                "last_hour_transactions": last_transaction_hour,
                "balance": balance,
                "ip_risk_score": 0.5,
                "is_foreign": is_foreign,
                "device_mismatch": 0,
                "location_change": 0,
                "amount_anomaly": 0.3,
                "hour_anomaly": 0
            }

            try:
                response = requests.post(API_URL, json=payload)
                if response.status_code == 200:
                    result = response.json()
                    st.success("Analyse Terminée")

                    col_res1, col_res2 = st.columns(2)
                    col_res1.metric("Probabilité de Fraude", f"{result['fraud_probability']:.2%}")
                    col_res2.metric("Niveau de Risque", result['risk_level'])

                    if result['is_fraud']:
                        st.error("🚨 FRAUDE DÉTECTÉE")
                    else:
                        st.success("✅ Transaction Sûre")

                    #Raisons
                    st.subheader("Raisons principales de la decision")

                    reason_df = pd.DataFrame(result["reasons"])
                    reason_df["impact_abs"] = reason_df["impact"].abs()

                    fig = px.bar(
                        reason_df,
                        x="impact_abs",
                        y="feature",
                        orientation="h",
                        color="direction",
                        title="Facteurs influençant la decision"
                    )

                    st.plotly_chart(fig, use_container_width=True)

                    for r in result["reasons"]:
                        st.write(
                            f"- **{r['feature']}** →"
                            f"{'augmente' if r['direction']=='increase_risk' else 'réduit'} le risque"
                            f"(impact = {abs(r['impact'])})"
                        )
                else:
                    st.error(f"Erreur API : {response.text}")
            except Exception as e:
                st.error(f"Erreur de Connexion : {e}")
                st.info("Assurez-vous que l'API est en cours d'exécution : `uvicorn app_fastapi:app --reload`")

elif page == "Performance du Modèle":
    st.header("Performance du Modèle")
    metadata = load_metadata()
    if metadata:
        st.write(f"**Seuil Optimal :** {metadata.get('threshold', 'N/A')}")
        st.write(f"**Features Utilisées :** {len(metadata.get('numerical_cols', [])) + len(metadata.get('categorical_cols', []))}")
    else:
        st.warning("Métadonnées du modèle introuvables. Veuillez d'abord entraîner le modèle.")
