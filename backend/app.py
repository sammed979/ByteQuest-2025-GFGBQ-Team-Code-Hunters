from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from model import ClinicalModel
from explainer import ClinicalExplainer
from rules import TreatmentRules
from report import ReportGenerator
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend connection

# Initialize components
clinical_model = ClinicalModel()
explainer = ClinicalExplainer()
treatment_rules = TreatmentRules()
report_gen = ReportGenerator()

# Load pre-trained model
try:
    clinical_model.load_model('models')
    print("[+] Model loaded successfully!")
except Exception as e:
    print(f"[!] Model not found. Please train the model first: {e}")

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'message': 'AI Clinical Decision Support System API',
        'version': '1.0.0'
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    """Main prediction endpoint"""
    try:
        # Get patient data from request
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['patient_name', 'age', 'gender', 'fever', 'cough', 'headache', 
                          'fatigue', 'bp_systolic', 'spo2', 'hemoglobin', 
                          'wbc', 'platelet']
        
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Convert gender to numeric
        if isinstance(data['gender'], str):
            data['gender'] = 1 if data['gender'].lower() == 'male' else 0
        
        # Extract only the features needed for the model (exclude patient_name)
        model_features = {
            'age': data['age'],
            'gender': data['gender'],
            'fever': data['fever'],
            'cough': data['cough'],
            'headache': data['headache'],
            'fatigue': data['fatigue'],
            'bp_systolic': data['bp_systolic'],
            'spo2': data['spo2'],
            'hemoglobin': data['hemoglobin'],
            'wbc': data['wbc'],
            'platelet': data['platelet']
        }
        
        # Get predictions
        predictions = clinical_model.predict(model_features)
        
        # Get feature importance
        feature_importance = clinical_model.get_feature_importance()
        
        # Generate explanation
        top_disease = predictions[0]['disease']
        top_confidence = predictions[0]['confidence']
        explanation = explainer.explain_prediction(
            top_disease, top_confidence, data, feature_importance
        )
        
        # Get treatment suggestions
        treatment_plan = treatment_rules.get_treatment_plan(top_disease)
        
        # Check for warnings
        warnings = treatment_rules.check_drug_interactions(top_disease, data)
        
        # Get follow-up plan
        follow_up = treatment_rules.generate_follow_up_plan(top_disease)
        
        # Prepare response
        response = {
            'success': True,
            'predictions': predictions[:3],  # Top 3 predictions
            'explanation': explanation,
            'treatment': treatment_plan,
            'warnings': warnings,
            'follow_up': follow_up,
            'patient_summary': {
                'age': data['age'],
                'gender': 'Male' if data['gender'] == 1 else 'Female',
                'symptoms_count': sum([
                    data['fever'], data['cough'], 
                    data['headache'], data['fatigue']
                ])
            }
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/generate-report', methods=['POST'])
def generate_report():
    """Generate and download PDF report"""
    try:
        data = request.get_json()
        
        # Extract components
        patient_data = data.get('patient_data', {})
        predictions = data.get('predictions', [])
        explanation = data.get('explanation', {})
        treatment = data.get('treatment', {})
        
        # Generate PDF
        filepath, filename = report_gen.generate_report(
            patient_data, predictions, explanation, treatment
        )
        
        # Send file
        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
    
    except Exception as e:
        import traceback
        print(f"[ERROR] PDF Generation failed: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/model-info', methods=['GET'])
def model_info():
    """Get model information and statistics"""
    try:
        feature_importance = clinical_model.get_feature_importance()
        
        return jsonify({
            'success': True,
            'model_type': 'Random Forest Classifier',
            'features': clinical_model.feature_names,
            'diseases': list(clinical_model.label_encoder.classes_),
            'feature_importance': [
                {'feature': feat, 'importance': round(imp * 100, 2)}
                for feat, imp in feature_importance
            ]
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/diseases', methods=['GET'])
def get_diseases():
    """Get list of supported diseases with info"""
    diseases_info = []
    
    for disease in clinical_model.disease_info.keys():
        info = clinical_model.disease_info[disease]
        diseases_info.append({
            'name': disease,
            'key_symptoms': info['key_symptoms'],
            'severity': info['severity']
        })
    
    return jsonify({
        'success': True,
        'diseases': diseases_info
    })

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs('models', exist_ok=True)
    os.makedirs('outputs/reports', exist_ok=True)
    
    print("[*] Starting AI Clinical Decision Support System...")
    print("[*] API running at: http://localhost:5000")
    print("[*] Endpoints:")
    print("   POST /api/predict - Get disease predictions")
    print("   POST /api/generate-report - Generate PDF report")
    print("   GET  /api/model-info - Model information")
    print("   GET  /api/diseases - Supported diseases")
    
    app.run(debug=True, host='0.0.0.0', port=5000)