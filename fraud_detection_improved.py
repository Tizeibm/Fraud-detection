import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_curve

def load_data():
    df = pd.read_csv(r"C:\Users\FBI\Desktop\Fraud detection\archive (2)\creditcard.csv")
    return df

def train_and_evaluate():
    df = load_data()
    
    X = df.drop('Class', axis=1)
    y = df['Class']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Create pipeline with RandomForest
    # RandomForest often handles imbalanced data better than LogReg, especially with class_weight='balanced'
    # We increase n_jobs to -1 to use all cores
    pipeline = Pipeline(steps=[
        ('scaler', StandardScaler()),
        ('rf', RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42, n_jobs=-1))
    ])
    
    # Train
    print("Training Random Forest Classifier...")
    pipeline.fit(X_train, y_train)
    
    # Predict
    y_pred = pipeline.predict(X_test)
    
    # Evaluate
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Check if we can improve by adjusting threshold
    # (RandomForest output probabilities)
    y_proba = pipeline.predict_proba(X_test)[:, 1]
    
    # Let's find a threshold that gives high recall but maybe better precision
    precisions, recalls, thresholds = precision_recall_curve(y_test, y_proba)
    
    # Find threshold for 0.90 recall
    target_recall = 0.90
    # We want the highest precision for at least target_recall
    # Iterate and find
    best_threshold = 0.5
    for p, r, t in zip(precisions, recalls, thresholds):
        if r >= target_recall:
            best_threshold = t
        else:
            break # Recalls are descending
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_curve

def load_data():
    df = pd.read_csv(r"C:\Users\FBI\Desktop\Fraud detection\archive (2)\creditcard.csv")
    return df

def train_and_evaluate():
    df = load_data()
    
    X = df.drop('Class', axis=1)
    y = df['Class']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Create pipeline with RandomForest
    # RandomForest often handles imbalanced data better than LogReg, especially with class_weight='balanced'
    # We increase n_jobs to -1 to use all cores
    pipeline = Pipeline(steps=[
        ('scaler', StandardScaler()),
        ('rf', RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42, n_jobs=-1))
    ])
    
    # Train
    print("Training Random Forest Classifier...")
    pipeline.fit(X_train, y_train)
    
    # Predict
    y_pred = pipeline.predict(X_test)
    
    # Evaluate
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Check if we can improve by adjusting threshold
    # (RandomForest output probabilities)
    y_proba = pipeline.predict_proba(X_test)[:, 1]
    
    # Let's find a threshold that gives high recall but maybe better precision
    precisions, recalls, thresholds = precision_recall_curve(y_test, y_proba)
    
    # Find threshold for 0.90 recall
    target_recall = 0.90
    # We want the highest precision for at least target_recall
    # Iterate and find
    best_threshold = 0.5
    for p, r, t in zip(precisions, recalls, thresholds):
        if r >= target_recall:
            best_threshold = t
        else:
            break # Recalls are descending
            
    print(f"\nThreshold for >= {target_recall} recall: {best_threshold}")
    y_pred_new = (y_proba >= best_threshold).astype(int)
    
    print("New Confusion Matrix (Adjusted Threshold):")
    print(confusion_matrix(y_test, y_pred_new))
    print("\nNew Classification Report (Adjusted Threshold):")
    print(classification_report(y_test, y_pred_new))

    # Save the model
    import joblib
    model_filename = 'fraud_model.pkl'
    joblib.dump(pipeline, model_filename)
    print(f"\nModel saved to {model_filename}")

if __name__ == "__main__":
    train_and_evaluate()
