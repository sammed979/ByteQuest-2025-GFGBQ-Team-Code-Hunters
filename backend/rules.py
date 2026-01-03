class TreatmentRules:
    """
    Rule-based treatment suggestions (NON-PRESCRIPTIVE)
    These are standard care guidelines only
    """
    
    def __init__(self):
        self.treatment_database = {
            'Dengue': {
                'immediate_care': [
                    'Ensure adequate hydration (oral or IV fluids)',
                    'Monitor vital signs every 4-6 hours',
                    'Complete bed rest recommended'
                ],
                'symptomatic_relief': [
                    'Antipyretics for fever (paracetamol class)',
                    'Avoid NSAIDs (aspirin, ibuprofen) - bleeding risk',
                    'Cool sponging for fever management'
                ],
                'monitoring': [
                    'Daily platelet count monitoring',
                    'Watch for warning signs: abdominal pain, persistent vomiting, bleeding',
                    'Hematocrit levels to detect plasma leakage'
                ],
                'dietary': [
                    'High-fluid diet (coconut water, ORS)',
                    'Easily digestible foods',
                    'Papaya leaf extract (traditional support)'
                ],
                'red_flags': [
                    '⚠️ If platelet count drops below 50,000/μL - immediate hospitalization',
                    '⚠️ Any bleeding manifestation - seek emergency care',
                    '⚠️ Severe abdominal pain - possible plasma leakage'
                ]
            },
            
            'Flu': {
                'immediate_care': [
                    'Rest and isolate to prevent spread',
                    'Maintain good hydration',
                    'Monitor temperature regularly'
                ],
                'symptomatic_relief': [
                    'Antipyretics for fever (paracetamol)',
                    'Cough suppressants if needed',
                    'Saline gargles for throat irritation'
                ],
                'monitoring': [
                    'Watch for breathing difficulty',
                    'Monitor for secondary bacterial infection',
                    'Recovery typically within 7-10 days'
                ],
                'dietary': [
                    'Warm fluids (soups, herbal tea)',
                    'Vitamin C rich foods',
                    'Light, nutritious meals'
                ],
                'red_flags': [
                    '⚠️ Difficulty breathing or chest pain - seek immediate care',
                    '⚠️ Fever persisting beyond 5 days',
                    '⚠️ Confusion or altered mental state'
                ]
            },
            
            'Pneumonia': {
                'immediate_care': [
                    '⚠️ REQUIRES MEDICAL ATTENTION - DO NOT SELF-TREAT',
                    'Oxygen therapy if SpO2 < 94%',
                    'Hospital admission may be required'
                ],
                'symptomatic_relief': [
                    'Antipyretics for fever',
                    'Adequate pain management',
                    'Breathing exercises as advised'
                ],
                'monitoring': [
                    'Continuous oxygen saturation monitoring',
                    'Chest X-ray for extent of infection',
                    'Culture and sensitivity tests for targeted therapy'
                ],
                'dietary': [
                    'High-calorie, high-protein diet',
                    'Adequate hydration',
                    'Small frequent meals if breathlessness'
                ],
                'red_flags': [
                    '⚠️ SpO2 below 90% - EMERGENCY',
                    '⚠️ Rapid breathing or chest retractions',
                    '⚠️ Confusion or drowsiness - ICU care may be needed'
                ]
            },
            
            'Anemia': {
                'immediate_care': [
                    'Identify underlying cause (blood loss, nutritional, chronic disease)',
                    'Complete blood count (CBC) with peripheral smear',
                    'Iron studies, B12, folate levels'
                ],
                'symptomatic_relief': [
                    'Iron supplementation (if iron-deficiency confirmed)',
                    'Gradual increase in physical activity',
                    'Avoid strenuous exercise initially'
                ],
                'monitoring': [
                    'Repeat hemoglobin after 4-6 weeks of treatment',
                    'Monitor for treatment response',
                    'Watch for signs of heart strain if severe anemia'
                ],
                'dietary': [
                    'Iron-rich foods (spinach, red meat, lentils)',
                    'Vitamin C to enhance iron absorption',
                    'Avoid tea/coffee with meals (inhibits iron absorption)'
                ],
                'red_flags': [
                    '⚠️ Hemoglobin < 7 g/dL - may require transfusion',
                    '⚠️ Chest pain or palpitations - cardiac evaluation needed',
                    '⚠️ Unexplained weight loss or night sweats - rule out malignancy'
                ]
            },
            
            'Hypertension': {
                'immediate_care': [
                    'Blood pressure monitoring 2-3 times daily',
                    'Lifestyle modification counseling',
                    'Risk assessment for cardiovascular disease'
                ],
                'symptomatic_relief': [
                    'Stress reduction techniques',
                    'Adequate sleep (7-8 hours)',
                    'Headache management with simple analgesics'
                ],
                'monitoring': [
                    'Home BP monitoring log',
                    'Kidney function tests (creatinine, BUN)',
                    'ECG and echocardiography if chronic',
                    'Fundoscopy to check for hypertensive retinopathy'
                ],
                'dietary': [
                    'DASH diet (low sodium, high potassium)',
                    'Limit salt intake to <5g/day',
                    'Reduce caffeine and alcohol',
                    'Increase fruits and vegetables'
                ],
                'lifestyle': [
                    'Regular aerobic exercise (30 min, 5 days/week)',
                    'Weight reduction if overweight',
                    'Smoking cessation',
                    'Stress management (yoga, meditation)'
                ],
                'red_flags': [
                    '⚠️ BP > 180/120 - Hypertensive emergency',
                    '⚠️ Chest pain, vision changes, or severe headache - immediate care',
                    '⚠️ Shortness of breath - possible heart failure'
                ]
            }
        }
    
    def get_treatment_plan(self, disease, severity='moderate'):
        """Get treatment suggestions for a disease"""
        if disease not in self.treatment_database:
            return {
                'message': 'Treatment guidelines not available for this condition',
                'recommendation': 'Please consult with a specialist for proper evaluation'
            }
        
        plan = self.treatment_database[disease].copy()
        
        # Add disclaimer
        plan['disclaimer'] = [
            '⚠️ IMPORTANT: These are general supportive care guidelines only',
            '✋ NOT a prescription - Doctor review required',
            '👨‍⚕️ Final treatment decisions must be made by the attending physician',
            '📞 Seek immediate medical attention for red flag symptoms'
        ]
        
        return plan
    
    def check_drug_interactions(self, disease, patient_data):
        """Check for potential contraindications"""
        warnings = []
        
        # Age-based warnings
        age = patient_data.get('age', 30)
        if age < 12:
            warnings.append('⚠️ Pediatric patient - dosage adjustments required')
        elif age > 65:
            warnings.append('⚠️ Elderly patient - monitor for adverse effects')
        
        # Condition-based warnings
        if disease == 'Dengue':
            if patient_data.get('platelet', 200000) < 50000:
                warnings.append('⚠️ CRITICAL: Severe thrombocytopenia - hospitalization required')
        
        if disease == 'Pneumonia':
            if patient_data.get('spo2', 98) < 90:
                warnings.append('⚠️ EMERGENCY: Severe hypoxia - ICU care needed')
        
        # BP warnings
        bp = patient_data.get('bp_systolic', 120)
        if bp < 90:
            warnings.append('⚠️ Hypotension present - avoid certain medications')
        elif bp > 180:
            warnings.append('⚠️ Severe hypertension - urgent medical evaluation')
        
        return warnings
    
    def generate_follow_up_plan(self, disease):
        """Generate follow-up schedule"""
        follow_up = {
            'Dengue': {
                'immediate': 'Daily monitoring until platelet count normalizes',
                'short_term': 'Review after 7 days with repeat CBC',
                'long_term': 'No specific follow-up if recovered'
            },
            'Flu': {
                'immediate': 'Self-monitoring at home',
                'short_term': 'Review if symptoms persist beyond 7 days',
                'long_term': 'Consider annual flu vaccination'
            },
            'Pneumonia': {
                'immediate': 'Daily clinical assessment',
                'short_term': 'Repeat chest X-ray after 6 weeks',
                'long_term': 'Pneumococcal vaccination if eligible'
            },
            'Anemia': {
                'immediate': 'Identify cause with investigations',
                'short_term': 'Repeat hemoglobin after 4-6 weeks',
                'long_term': 'Monitor every 3 months until normalized'
            },
            'Hypertension': {
                'immediate': 'Weekly BP monitoring',
                'short_term': 'Review after 2-4 weeks',
                'long_term': 'Regular 3-monthly check-ups'
            }
        }
        
        return follow_up.get(disease, {
            'immediate': 'Clinical judgment required',
            'short_term': 'Follow-up as per doctor\'s advice',
            'long_term': 'Regular health monitoring'
        })