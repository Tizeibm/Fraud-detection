import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, average_precision_score, precision_recall_curve, roc_auc_score
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuration
DATA_PATH = "fraud_dataset_realistic_200k.csv"
MODEL_PATH = "fraud_model_xgboost.pkl"
METADATA_PATH = "model_metadata.pkl"
RANDOM_STATE = 42

def load_data(path):
    print(f"Loading data from {path}...")
    df = pd.read_csv(path)
    # Convert transaction_time to datetime
    df['transaction_time'] = pd.to_datetime(df['transaction_time'])
    return df

def preprocess_data(df):
    print("Preprocessing data...")
    
    # Feature Engineering
    # Calculate hours since last transaction for each customer (if applicable, but we'll stick to provided features for now)
    # The dataset already has 'days_from_last' equivalent or similar in 'previous_transactions_24h' etc.
    
    # Drop identifiers and leakage/irrelevant columns
    drop_cols = ['transaction_id', 'customer_id', 'transaction_time', 'merchant_id'] 
    # merchant_id might be high cardinality, let's drop it for this iteration or use target encoding (omitted for simplicity)
    
    X = df.drop(columns=drop_cols + ['label_is_fraud'])
    y = df['label_is_fraud']
    
    # Identify categorical and numerical columns
    categorical_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()
    numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    
    print(f"Categorical columns: {categorical_cols}")
    print(f"Numerical columns: {numerical_cols}")
    
    return X, y, categorical_cols, numerical_cols

def build_pipeline(categorical_cols, numerical_cols):
    # Preprocessing for numerical data
    numeric_transformer = StandardScaler()

    # Preprocessing for categorical data
    categorical_transformer = OneHotEncoder(handle_unknown='ignore', sparse_output=False)

    # Bundle preprocessing for numerical and categorical data
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numerical_cols),
            ('cat', categorical_transformer, categorical_cols)
        ]
    )
    
    # XGBoost Classifier
    # scale_pos_weight is useful for imbalanced datasets
    clf = xgb.XGBClassifier(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        objective='binary:logistic',
        scale_pos_weight=10, # Adjust based on imbalance ratio
        random_state=RANDOM_STATE,
        n_jobs=-1,
        eval_metric='aucpr'
    )

    # Create pipeline
    pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                               ('classifier', clf)])
    
    return pipeline

def evaluate_model(pipeline, X_test, y_test):
    print("\nEvaluating model...")
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]
    
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    roc_auc = roc_auc_score(y_test, y_proba)
    pr_auc = average_precision_score(y_test, y_proba)
    
    print(f"\nROC-AUC: {roc_auc:.4f}")
    print(f"PR-AUC: {pr_auc:.4f}")
    
    return y_proba

def find_optimal_threshold(y_test, y_proba):
    precisions, recalls, thresholds = precision_recall_curve(y_test, y_proba)
    
    # Target 95% Recall (Catching most frauds)
    target_recall = 0.95
    optimal_threshold = 0.5
    
    for p, r, t in zip(precisions, recalls, thresholds):
        if r < target_recall:
            break
        optimal_threshold = t
        
    print(f"\nOptimal Threshold for {target_recall*100}% Recall: {optimal_threshold:.4f}")
    return optimal_threshold

def main():
    # 1. Load Data
    df = load_data(DATA_PATH)
    
    # 2. Preprocess
    X, y, cat_cols, num_cols = preprocess_data(df)
    
    # 3. Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y)
    
    # 4. Build Pipeline
    pipeline = build_pipeline(cat_cols, num_cols)
    
    # 5. Train
    print("Training XGBoost model...")
    pipeline.fit(X_train, y_train)
    
    # 6. Evaluate
    y_proba = evaluate_model(pipeline, X_test, y_test)
    
    # 7. Optimal Threshold
    threshold = find_optimal_threshold(y_test, y_proba)
    
    # 8. Save Model & Metadata
    print(f"Saving model to {MODEL_PATH}...")
    joblib.dump(pipeline, MODEL_PATH)
    
    metadata = {
        'categorical_cols': cat_cols,
        'numerical_cols': num_cols,
        'threshold': threshold
    }
    joblib.dump(metadata, METADATA_PATH)
    print("Training complete.")

if __name__ == "__main__":
    main()
