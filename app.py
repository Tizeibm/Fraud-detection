import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# Set page config
st.set_page_config(page_title="Fraud Detection System", layout="wide")

@st.cache_resource
def load_model():
    if os.path.exists('fraud_model.pkl'):
        return joblib.load('fraud_model.pkl')
    return None

@st.cache_data
def load_sample_data():
    # Load a small sample of the original data for simulation
    # We'll try to load the full dataset and sample from it
    try:
        df = pd.read_csv(r"C:\Users\FBI\Desktop\Fraud detection\archive (2)\creditcard.csv")
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def main():
    st.title("🛡️ Credit Card Fraud Detection System")
    
    model = load_model()
    if model is None:
        st.error("Model file 'fraud_model.pkl' not found. Please run 'fraud_detection_improved.py' first.")
        return

    data = load_sample_data()
    
    st.sidebar.header("Input Transaction Details")
    
    # Since the dataset has anonymized features V1-V28, manual input is difficult.
    # We will offer two modes: Manual (limited) and Simulation.
    
    mode = st.sidebar.radio("Choose Mode", ["Simulation (Random Sample)", "Manual Input (Advanced)"])
    
    input_data = None
    
    if mode == "Simulation (Random Sample)":
        st.info("Simulate a transaction by picking a random sample from the dataset.")
        if st.button("Load Random Transaction"):
            if data is not None:
                sample = data.sample(1)
                # Store the true class
                true_class = sample['Class'].values[0]
                # Drop class for prediction
                input_data = sample.drop('Class', axis=1)
                
                st.write("### Transaction Details")
                st.dataframe(input_data)
                st.write(f"**Actual Label:** {'Fraud' if true_class == 1 else 'Legitimate'}")
            else:
                st.error("Data not available.")
                
    elif mode == "Manual Input (Advanced)":
        st.warning("This mode requires values for all 30 features (Time, V1-V28, Amount).")
        # For simplicity, we can just ask for Time and Amount and fill V1-V28 with zeros (not accurate but functional for demo)
        # Or better, just use sliders for a few key features if we knew them.
        # Given the constraints, let's just show Time and Amount and random V's? No, that's bad.
        # Let's just allow pasting a CSV row.
        
        csv_input = st.text_area("Paste CSV row (Time, V1...V28, Amount)", "")
        if csv_input:
            try:
                # simple parsing
                values = [float(x) for x in csv_input.split(',')]
                if len(values) == 30:
                    input_data = pd.DataFrame([values], columns=data.columns[:-1]) # Exclude Class
                    st.write("### Transaction Details")
                    st.dataframe(input_data)
                else:
                    st.error(f"Expected 30 values, got {len(values)}")
            except Exception as e:
                st.error(f"Error parsing input: {e}")

    if input_data is not None:
        if st.button("Predict Fraud"):
            # Predict
            prediction = model.predict(input_data)[0]
            probability = model.predict_proba(input_data)[0][1]
            
            st.write("---")
            st.write("### Prediction Results")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if prediction == 1:
                    st.error("🚨 FRAUD DETECTED")
                else:
                    st.success("✅ LEGITIMATE TRANSACTION")
            
            with col2:
                st.metric("Fraud Probability", f"{probability:.2%}")
                
            # Explanation (simple feature importance if possible, or just context)
            if prediction == 1:
                st.warning("This transaction has been flagged as high risk.")
            
            # Threshold adjustment visualization
            st.write("---")
            st.write("#### Sensitivity Analysis")
            threshold = st.slider("Adjust Decision Threshold", 0.0, 1.0, 0.5, 0.01)
            custom_pred = 1 if probability >= threshold else 0
            
            if custom_pred == 1:
                st.write(f"At threshold {threshold}: **Fraud**")
            else:
                st.write(f"At threshold {threshold}: **Legitimate**")

if __name__ == "__main__":
    main()
