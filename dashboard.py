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

st.set_page_config(page_title="Fraud Detection Dashboard", layout="wide")

st.title("🛡️ Advanced Fraud Detection System")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Real-time Inference", "Model Insights"])

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

@st.cache_resource
def load_metadata():
    try:
        return joblib.load(MODEL_METADATA_PATH)
    except:
        return None

if page == "Overview":
    st.header("Dataset Overview")
    df = load_data()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Transactions", f"{len(df):,}")
    col2.metric("Fraud Cases", f"{df['label_is_fraud'].sum():,}")
    col3.metric("Fraud Rate", f"{df['label_is_fraud'].mean()*100:.2f}%")
    
    st.subheader("Fraud by Category")
    fig = px.bar(df.groupby('merchant_category')['label_is_fraud'].mean().reset_index(), 
                 x='merchant_category', y='label_is_fraud', 
                 title="Fraud Rate by Merchant Category")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Real-time Inference":
    st.header("Test Transaction")
    
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            amount = st.number_input("Amount", min_value=0.0, value=100.0)
            merchant_category = st.selectbox("Merchant Category", ["electronics", "travel", "grocery", "fashion", "entertainment"])
            transaction_hour = st.slider("Hour of Day", 0, 23, 12)
            is_foreign = st.selectbox("Is Foreign Transaction?", [0, 1])
            
        with col2:
            age = st.number_input("Customer Age", 18, 100, 30)
            device = st.selectbox("Device", ["mobile", "desktop", "tablet"])
            distance_from_home = st.number_input("Distance from Home (km)", 0.0, 10000.0, 10.0) # Placeholder if not in input
            
        # Hidden/Default fields for simplicity in this demo form
        # In a real app, these would be populated or computed
        submit = st.form_submit_button("Analyze Transaction")
        
        if submit:
            # Construct payload matching API expectation
            # Note: We need to match the exact schema of TransactionInput in app_fastapi.py
            # For this demo, we'll mock the missing fields with average/default values
            payload = {
                "transaction_hour": transaction_hour,
                "day_of_week": 0, # Default
                "age": age,
                "gender": "M", # Default
                "home_country": "US",
                "transaction_country": "US" if is_foreign == 0 else "FR",
                "merchant_category": merchant_category,
                "merchant_base_risk": 0.1, # Default
                "transaction_type": "online",
                "card_type": "Visa",
                "device": device,
                "amount": amount,
                "avg_30d_amount": 50.0, # Default
                "previous_transactions_24h": 1,
                "last_hour_transactions": 0,
                "balance": 1000.0,
                "ip_risk_score": 0.5,
                "is_foreign": is_foreign,
                "device_mismatch": 0,
                "location_change": 0,
                "amount_anomaly": 0.0,
                "hour_anomaly": 0
            }
            
            try:
                response = requests.post(API_URL, json=payload)
                if response.status_code == 200:
                    result = response.json()
                    st.success("Analysis Complete")
                    
                    col_res1, col_res2 = st.columns(2)
                    col_res1.metric("Fraud Probability", f"{result['fraud_probability']:.2%}")
                    col_res2.metric("Risk Level", result['risk_level'])
                    
                    if result['is_fraud']:
                        st.error("🚨 FRAUD DETECTED")
                    else:
                        st.success("✅ Transaction Safe")
                else:
                    st.error(f"API Error: {response.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}")
                st.info("Make sure the API is running: `uvicorn app_fastapi:app --reload`")

elif page == "Model Insights":
    st.header("Model Performance")
    metadata = load_metadata()
    if metadata:
        st.write(f"**Optimal Threshold:** {metadata.get('threshold', 'N/A')}")
        st.write(f"**Features Used:** {len(metadata.get('numerical_cols', [])) + len(metadata.get('categorical_cols', []))}")
    else:
        st.warning("Model metadata not found. Please train the model first.")
