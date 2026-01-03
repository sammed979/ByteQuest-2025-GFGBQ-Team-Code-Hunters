import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os

class ClinicalModel:
    def __init__(self):
        self.model = None
        self.label_encoder = None
        self.feature_names = None
        self.disease_info = {
            'Dengue': {
                'key_symptoms': ['High fever', 'Low platelet count', 'Headache'],
                'severity': 'Moderate to Severe'
            },
            'Flu': {
                'key_symptoms': ['Fever', 'Cough', 'Fatigue', 'Headache'],
                'severity': 'Mild to Moderate'
            },
            'Pneumonia': {
                'key_symptoms': ['High fever', 'Cough', 'Low SpO2', 'High WBC'],
                'severity': 'Severe'
            },
            'Anemia': {
                'key_symptoms': ['Fatigue', 'Low hemoglobin', 'Normal fever'],
                'severity': 'Mild to Moderate'
            },
            'Hypertension': {
                'key_symptoms': ['High BP', 'Headache', 'Normal temperature'],
                'severity': 'Chronic'
            }
        }
    
    def prepare_data(self, df):
        """Prepare dataset for training"""
        # Convert Yes/No to 1/0
        df['fever'] = df['fever'].map({'Yes': 1, 'No': 0})
        df['cough'] = df['cough'].map({'Yes': 1, 'No': 0})
        df['headache'] = df['headache'].map({'Yes': 1, 'No': 0})
        df['fatigue'] = df['fatigue'].map({'Yes': 1, 'No': 0})
        
        # Convert gender to numeric
        df['gender'] = df['gender'].map({'Male': 1, 'Female': 0})
        
        # Features and target
        feature_cols = ['age', 'gender', 'fever', 'cough', 'headache', 
                       'fatigue', 'bp_systolic', 'spo2', 'hemoglobin', 
                       'wbc', 'platelet']
        
        X = df[feature_cols]
        y = df['disease']
        
        self.feature_names = feature_cols
        
        return X, y
    
    def train(self, csv_path):
        """Train the Random Forest model"""
        print("[*] Loading dataset...")
        df = pd.read_csv(csv_path)
        
        print(f"[+] Dataset loaded: {len(df)} samples, {len(df['disease'].unique())} diseases")
        
        # Prepare data
        X, y = self.prepare_data(df)
        
        # Encode disease labels
        self.label_encoder = LabelEncoder()
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Split data (no stratification for small datasets)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=42
        )
        
        # Train Random Forest
        print("[*] Training Random Forest model...")
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=2,
            random_state=42,
            class_weight='balanced'  # Handle imbalanced data
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        train_acc = self.model.score(X_train, y_train)
        test_acc = self.model.score(X_test, y_test)
        
        print(f"[+] Training Accuracy: {train_acc*100:.2f}%")
        print(f"[+] Testing Accuracy: {test_acc*100:.2f}%")
        
        return train_acc, test_acc
    
    def predict(self, patient_data):
        """Make prediction with confidence scores"""
        if self.model is None:
            raise ValueError("Model not trained or loaded!")
        
        # Convert input to DataFrame
        input_df = pd.DataFrame([patient_data])
        
        # Get prediction probabilities
        probabilities = self.model.predict_proba(input_df)[0]
        
        # Get disease names and sort by probability
        diseases = self.label_encoder.classes_
        results = []
        
        for disease, prob in zip(diseases, probabilities):
            results.append({
                'disease': disease,
                'confidence': round(prob * 100, 2),
                'info': self.disease_info.get(disease, {})
            })
        
        # Sort by confidence (highest first)
        results = sorted(results, key=lambda x: x['confidence'], reverse=True)
        
        return results
    
    def get_feature_importance(self):
        """Get feature importance for explainability"""
        if self.model is None:
            return None
        
        importance = self.model.feature_importances_
        feature_imp = dict(zip(self.feature_names, importance))
        
        # Sort by importance
        sorted_features = sorted(feature_imp.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_features
    
    def save_model(self, model_dir='models'):
        """Save trained model"""
        os.makedirs(model_dir, exist_ok=True)
        
        joblib.dump(self.model, f'{model_dir}/trained_model.pkl')
        joblib.dump(self.label_encoder, f'{model_dir}/label_encoder.pkl')
        joblib.dump(self.feature_names, f'{model_dir}/feature_names.pkl')
        
        print(f"[+] Model saved to {model_dir}/")
    
    def load_model(self, model_dir='models'):
        """Load pre-trained model"""
        self.model = joblib.load(f'{model_dir}/trained_model.pkl')
        self.label_encoder = joblib.load(f'{model_dir}/label_encoder.pkl')
        self.feature_names = joblib.load(f'{model_dir}/feature_names.pkl')
        
        print("[+] Model loaded successfully!")


# Training script (run once)
if __name__ == "__main__":
    model = ClinicalModel()
    
    # Train model
    csv_path = '../data/clinical_data.csv'
    model.train(csv_path)
    
    # Save model
    model.save_model()
    
    # Test prediction
    test_patient = {
        'age': 45,
        'gender': 0,  # Female
        'fever': 1,
        'cough': 1,
        'headache': 1,
        'fatigue': 1,
        'bp_systolic': 135,
        'spo2': 96,
        'hemoglobin': 11.0,
        'wbc': 4800,
        'platelet': 230000
    }
    
    results = model.predict(test_patient)
    print("\n[*] Test Prediction:")
    for r in results[:3]:
        print(f"  {r['disease']}: {r['confidence']}%")