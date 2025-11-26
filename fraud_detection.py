import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix

def load_data():
    # Use the path found in the notebook
    df = pd.read_csv(r"C:\Users\FBI\Desktop\Fraud detection\archive (2)\creditcard.csv")
    return df

def train_and_evaluate():
    df = load_data()
    
    # Basic preprocessing as seen in the notebook (implied)
    # The notebook didn't show explicit splitting code in the snippets I read, 
    # but it used X_train, X_test, y_train, y_test.
    # I will assume a standard split.
    
    X = df.drop('Class', axis=1)
    y = df['Class']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Create pipeline
    pipeline = Pipeline(steps=[
        ('scaler', StandardScaler()),
        ('logreg', LogisticRegression(class_weight='balanced', max_iter=1000))
    ])
    
    # Train
    print("Training Logistic Regression...")
    pipeline.fit(X_train, y_train)
    
    # Predict
    y_pred = pipeline.predict(X_test)
    
    # Evaluate
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    train_and_evaluate()
