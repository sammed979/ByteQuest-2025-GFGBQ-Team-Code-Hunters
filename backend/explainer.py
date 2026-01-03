class ClinicalExplainer:
    """Generates human-readable explanations for AI predictions"""
    
    def __init__(self):
        # Clinical thresholds
        self.thresholds = {
            'fever_temp': 99.0,
            'high_bp': 140,
            'low_spo2': 95,
            'low_hb_male': 13.5,
            'low_hb_female': 12.0,
            'high_wbc': 11000,
            'low_platelet': 150000
        }
    
    def analyze_vitals(self, patient_data):
        """Analyze patient vitals and return abnormalities"""
        findings = []
        red_flags = []
        
        # Temperature analysis
        if patient_data.get('fever') == 1:
            findings.append("Fever present")
            if patient_data.get('temp', 100) > 102:
                red_flags.append("High grade fever (>102°F)")
        
        # Blood pressure
        bp = patient_data.get('bp_systolic', 120)
        if bp >= 140:
            findings.append(f"Elevated blood pressure ({bp} mmHg)")
            if bp >= 180:
                red_flags.append("⚠️ Critically high BP - immediate attention needed")
        elif bp < 90:
            findings.append(f"Low blood pressure ({bp} mmHg)")
            red_flags.append("⚠️ Hypotension detected")
        
        # Oxygen saturation
        spo2 = patient_data.get('spo2', 98)
        if spo2 < 95:
            findings.append(f"Low oxygen saturation ({spo2}%)")
            if spo2 < 90:
                red_flags.append("⚠️ Critical hypoxia - oxygen support needed")
        
        # Hemoglobin
        hb = patient_data.get('hemoglobin', 13)
        gender = patient_data.get('gender', 1)
        threshold = self.thresholds['low_hb_male'] if gender == 1 else self.thresholds['low_hb_female']
        
        if hb < threshold:
            findings.append(f"Low hemoglobin ({hb} g/dL)")
        
        # White blood cells
        wbc = patient_data.get('wbc', 7000)
        if wbc > 11000:
            findings.append(f"Elevated WBC count ({wbc}/μL) - suggests infection")
        elif wbc < 4000:
            findings.append(f"Low WBC count ({wbc}/μL)")
        
        # Platelets
        platelet = patient_data.get('platelet', 200000)
        if platelet < 150000:
            findings.append(f"Low platelet count ({platelet}/μL)")
            if platelet < 50000:
                red_flags.append("⚠️ Severe thrombocytopenia - bleeding risk")
        
        return findings, red_flags
    
    def explain_prediction(self, top_disease, confidence, patient_data, feature_importance):
        """Generate detailed explanation for the prediction"""
        
        findings, red_flags = self.analyze_vitals(patient_data)
        
        explanation = {
            'summary': f"Based on clinical analysis, {top_disease} is predicted with {confidence}% confidence.",
            'key_findings': findings,
            'red_flags': red_flags,
            'reasoning': []
        }
        
        # Disease-specific reasoning
        if top_disease == 'Dengue':
            reasoning = []
            if patient_data.get('fever') == 1:
                reasoning.append("Fever is a hallmark symptom of dengue")
            if patient_data.get('platelet', 200000) < 150000:
                reasoning.append("Thrombocytopenia (low platelets) strongly indicates dengue")
            if patient_data.get('headache') == 1:
                reasoning.append("Severe headache is common in dengue fever")
            if patient_data.get('wbc', 7000) < 5000:
                reasoning.append("Leukopenia supports viral infection (dengue)")
            
            explanation['reasoning'] = reasoning
        
        elif top_disease == 'Pneumonia':
            reasoning = []
            if patient_data.get('fever') == 1 and patient_data.get('cough') == 1:
                reasoning.append("Fever with cough suggests respiratory infection")
            if patient_data.get('spo2', 98) < 95:
                reasoning.append("Low oxygen saturation indicates compromised lung function")
            if patient_data.get('wbc', 7000) > 11000:
                reasoning.append("Elevated WBC count suggests bacterial infection")
            
            explanation['reasoning'] = reasoning
        
        elif top_disease == 'Flu':
            reasoning = []
            if patient_data.get('fever') == 1:
                reasoning.append("Fever is typical of influenza")
            if patient_data.get('cough') == 1 and patient_data.get('fatigue') == 1:
                reasoning.append("Cough and fatigue are classic flu symptoms")
            if patient_data.get('platelet', 200000) >= 150000:
                reasoning.append("Normal platelet count rules out dengue, supports flu")
            
            explanation['reasoning'] = reasoning
        
        elif top_disease == 'Anemia':
            reasoning = []
            hb = patient_data.get('hemoglobin', 13)
            if hb < 12:
                reasoning.append(f"Hemoglobin level ({hb} g/dL) is below normal range")
            if patient_data.get('fatigue') == 1:
                reasoning.append("Fatigue is a primary symptom of anemia")
            if patient_data.get('fever') == 0:
                reasoning.append("Absence of fever suggests non-infectious cause")
            
            explanation['reasoning'] = reasoning
        
        elif top_disease == 'Hypertension':
            reasoning = []
            bp = patient_data.get('bp_systolic', 120)
            if bp >= 140:
                reasoning.append(f"Systolic BP ({bp} mmHg) exceeds hypertension threshold")
            if patient_data.get('headache') == 1:
                reasoning.append("Headache can be associated with high blood pressure")
            if patient_data.get('age', 30) > 40:
                reasoning.append("Age is a risk factor for hypertension")
            
            explanation['reasoning'] = reasoning
        
        # Top influential features
        if feature_importance:
            top_features = feature_importance[:3]
            explanation['top_factors'] = [
                f"{feat.replace('_', ' ').title()}: {imp*100:.1f}% importance" 
                for feat, imp in top_features
            ]
        
        return explanation
    
    def generate_differential_diagnosis(self, predictions):
        """Generate differential diagnosis explanation"""
        differential = {
            'primary': predictions[0],
            'alternatives': predictions[1:3],
            'reasoning': []
        }
        
        primary = predictions[0]
        if len(predictions) > 1:
            second = predictions[1]
            conf_diff = primary['confidence'] - second['confidence']
            
            if conf_diff > 30:
                differential['reasoning'].append(
                    f"{primary['disease']} is significantly more likely than {second['disease']} "
                    f"(confidence difference: {conf_diff:.1f}%)"
                )
            elif conf_diff < 10:
                differential['reasoning'].append(
                    f"Close differential between {primary['disease']} and {second['disease']}. "
                    "Further diagnostic tests recommended."
                )
        
        return differential