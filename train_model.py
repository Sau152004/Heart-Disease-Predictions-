"""
Heart Disease Model Training Script
This script trains a machine learning model for heart disease prediction
and saves it for use with the Flask web application.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_explore_data(file_path):
    """Load and explore the heart disease dataset"""
    print("Loading dataset...")
    
    try:
        # Try to load the CSV file
        df = pd.read_csv(file_path)
        print(f"✅ Dataset loaded successfully!")
        print(f"Shape: {df.shape}")
        
        # Display basic information
        print("\n📊 Dataset Info:")
        print(df.info())
        
        print("\n📈 Statistical Summary:")
        print(df.describe())
        
        print("\n🎯 Target Distribution:")
        print(df['target'].value_counts())
        
        # Check for missing values
        print("\n❓ Missing Values:")
        print(df.isnull().sum())
        
        return df
        
    except FileNotFoundError:
        print(f"❌ Error: Could not find file '{file_path}'")
        print("Please ensure your CSV file is in the same directory as this script.")
        return None
    except Exception as e:
        print(f"❌ Error loading dataset: {str(e)}")
        return None

def preprocess_data(df):
    """Preprocess the data for training"""
    print("\n🔧 Preprocessing data...")
    
    # Make a copy to avoid modifying original data
    df_processed = df.copy()
    
    # Handle missing values if any
    df_processed = df_processed.dropna()
    
    # Ensure target column exists and is properly named
    if 'target' not in df_processed.columns:
        # Common alternative names for target column
        target_alternatives = ['num', 'heart_disease', 'diagnosis', 'class']
        for alt in target_alternatives:
            if alt in df_processed.columns:
                df_processed['target'] = df_processed[alt]
                break
    
    # Separate features and target
    if 'target' in df_processed.columns:
        X = df_processed.drop('target', axis=1)
        y = df_processed['target']
    else:
        print("❌ Error: No target column found!")
        print("Available columns:", df_processed.columns.tolist())
        return None, None
    
    # Ensure target is binary (0 and 1)
    y = y.map({0: 0, 1: 1, 2: 1, 3: 1, 4: 1})  # Convert multi-class to binary
    
    print(f"✅ Features shape: {X.shape}")
    print(f"✅ Target shape: {y.shape}")
    print(f"✅ Target distribution: {y.value_counts().to_dict()}")
    
    return X, y

def train_models(X_train, X_test, y_train, y_test):
    """Train and compare different models"""
    print("\n🤖 Training models...")
    
    # Scale features for some models
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Define models to compare
    models = {
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'SVM': SVC(kernel='rbf', random_state=42, probability=True)
    }
    
    results = {}
    
    # Train and evaluate each model
    for name, model in models.items():
        print(f"\nTraining {name}...")
        
        # Use scaled data for Logistic Regression and SVM
        if name in ['Logistic Regression', 'SVM']:
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
            y_proba = model.predict_proba(X_test_scaled)[:, 1]
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_proba = model.predict_proba(X_test)[:, 1]
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        auc_score = roc_auc_score(y_test, y_proba)
        
        # Cross-validation score
        if name in ['Logistic Regression', 'SVM']:
            cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5)
        else:
            cv_scores = cross_val_score(model, X_train, y_train, cv=5)
        
        results[name] = {
            'model': model,
            'accuracy': accuracy,
            'auc_score': auc_score,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'scaler': scaler if name in ['Logistic Regression', 'SVM'] else None
        }
        
        print(f"✅ {name} - Accuracy: {accuracy:.4f}, AUC: {auc_score:.4f}, CV: {cv_scores.mean():.4f} (±{cv_scores.std():.4f})")
    
    return results

def select_best_model(results):
    """Select the best performing model"""
    print("\n🏆 Model Selection:")
    
    # Sort models by AUC score
    sorted_models = sorted(results.items(), key=lambda x: x[1]['auc_score'], reverse=True)
    
    print("\nModel Rankings (by AUC Score):")
    for i, (name, metrics) in enumerate(sorted_models, 1):
        print(f"{i}. {name}: AUC={metrics['auc_score']:.4f}, Accuracy={metrics['accuracy']:.4f}")
    
    # Select best model
    best_model_name, best_metrics = sorted_models[0]
    best_model = best_metrics['model']
    best_scaler = best_metrics['scaler']
    
    print(f"\n🥇 Best Model: {best_model_name}")
    print(f"   AUC Score: {best_metrics['auc_score']:.4f}")
    print(f"   Accuracy: {best_metrics['accuracy']:.4f}")
    print(f"   CV Score: {best_metrics['cv_mean']:.4f} (±{best_metrics['cv_std']:.4f})")
    
    return best_model, best_scaler, best_model_name

def save_model(model, scaler, model_name, filename='heart_disease_model.pkl'):
    """Save the trained model and scaler"""
    print(f"\n💾 Saving model to {filename}...")
    
    try:
        # Create a dictionary to store model and metadata
        model_data = {
            'model': model,
            'scaler': scaler,
            'model_name': model_name,
            'feature_names': [
                'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
                'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
            ],
            'target_names': ['No Risk', 'Risk']
        }
        
        joblib.dump(model_data, filename)
        print(f"✅ Model saved successfully as {filename}")
        
        # Also save just the model for simpler loading
        joblib.dump(model, filename.replace('.pkl', '_simple.pkl'))
        print(f"✅ Simple model saved as {filename.replace('.pkl', '_simple.pkl')}")
        
    except Exception as e:
        print(f"❌ Error saving model: {str(e)}")

def main():
    """Main training pipeline"""
    print("🫀 Heart Disease Prediction Model Training")
    print("=" * 50)
    
    # Load data (adjust filename as needed)
    data_file = input("Enter the path to your heart disease CSV file (or press Enter for 'heart.csv'): ").strip()
    if not data_file:
        data_file = 'heart.csv'
    
    df = load_and_explore_data(data_file)
    if df is None:
        return
    
    # Preprocess data
    X, y = preprocess_data(df)
    if X is None or y is None:
        return
    
    # Split data
    print("\n✂️ Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    
    # Train models
    results = train_models(X_train, X_test, y_train, y_test)
    
    # Select best model
    best_model, best_scaler, model_name = select_best_model(results)
    
    # Save model
    save_model(best_model, best_scaler, model_name)
    
    print("\n🎉 Training completed successfully!")
    print("\nNext steps:")
    print("1. Run 'python app.py' to start the Flask server")
    print("2. Open your browser to http://localhost:5000")
    print("3. Fill in the form to make predictions!")

if __name__ == "__main__":
    main()