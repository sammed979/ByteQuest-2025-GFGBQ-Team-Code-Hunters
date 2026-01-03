from fpdf import FPDF
from datetime import datetime
import os

class ClinicalReport(FPDF):
    def header(self):
        """Report header"""
        self.set_font('Arial', 'B', 16)
        self.set_text_color(0, 102, 204)
        self.cell(0, 10, 'AI CLINICAL DECISION SUPPORT REPORT', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.set_text_color(128, 128, 128)
        self.cell(0, 5, 'AI-Assisted Diagnostic Analysis', 0, 1, 'C')
        self.ln(5)
        self.set_draw_color(0, 102, 204)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)
    
    def footer(self):
        """Report footer"""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

class ReportGenerator:
    def __init__(self):
        self.output_dir = 'outputs/reports'
        os.makedirs(self.output_dir, exist_ok=True)
    
    def sanitize_text(self, text):
        """Remove emojis and special Unicode characters that fpdf can't handle"""
        if not isinstance(text, str):
            return str(text)
        
        # Replace common emojis with text equivalents
        replacements = {
            '⚠️': '[!]',
            '⚠': '[!]',
            '✅': '[+]',
            '❌': '[x]',
            '🔬': '',
            '🩺': '',
            '💊': '',
            '🏥': '',
            '📊': '',
            '🥗': '',
            '🏃': '',
            '🚨': '[!]',
            '➕': '+',
            '✓': '[+]',
            '•': '-',
            '₂': '2',
            'μ': 'u',
        }
        
        for emoji, replacement in replacements.items():
            text = text.replace(emoji, replacement)
        
        # Remove any remaining non-ASCII characters
        text = text.encode('ascii', 'ignore').decode('ascii')
        
        return text
    
    def generate_report(self, patient_data, predictions, explanation, treatment_plan):
        """Generate comprehensive clinical PDF report"""
        
        pdf = ClinicalReport()
        pdf.add_page()
        
        # Report metadata
        report_id = f"CDSS-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        timestamp = datetime.now().strftime('%B %d, %Y at %I:%M %p')
        
        # === SECTION 1: Report Information ===
        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 8, 'Report Information', 0, 1, 'L')
        pdf.set_draw_color(200, 200, 200)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)
        
        pdf.set_font('Arial', '', 10)
        pdf.cell(50, 6, f'Report ID: {report_id}', 0, 1)
        pdf.cell(50, 6, f'Generated: {timestamp}', 0, 1)
        pdf.ln(5)
        
        # === SECTION 2: Patient Information ===
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, 'Patient Information', 0, 1, 'L')
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)
        
        pdf.set_font('Arial', '', 10)
        # Patient Name
        patient_name = self.sanitize_text(patient_data.get('patient_name', 'N/A'))
        pdf.cell(0, 6, f"Patient Name: {patient_name}", 0, 1)
        
        # Age and Gender
        gender_text = 'Male' if patient_data.get('gender') == 1 else 'Female'
        pdf.cell(50, 6, f"Age: {patient_data.get('age', 'N/A')} years", 0, 0)
        pdf.cell(50, 6, f"Gender: {gender_text}", 0, 1)
        pdf.ln(3)
        
        # === SECTION 3: Clinical Findings ===
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, 'Clinical Findings', 0, 1, 'L')
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)
        
        # Symptoms
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 6, 'Symptoms:', 0, 1)
        pdf.set_font('Arial', '', 9)
        
        symptoms = []
        if patient_data.get('fever') == 1: symptoms.append('Fever')
        if patient_data.get('cough') == 1: symptoms.append('Cough')
        if patient_data.get('headache') == 1: symptoms.append('Headache')
        if patient_data.get('fatigue') == 1: symptoms.append('Fatigue')
        
        symptom_text = ', '.join(symptoms) if symptoms else 'None reported'
        pdf.multi_cell(0, 5, f"  {symptom_text}")
        pdf.ln(2)
        
        # Vitals
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 6, 'Vital Signs:', 0, 1)
        pdf.set_font('Arial', '', 9)
        pdf.cell(95, 5, f"  Blood Pressure: {patient_data.get('bp_systolic', 'N/A')} mmHg (systolic)", 0, 0)
        pdf.cell(95, 5, f"  SpO2: {patient_data.get('spo2', 'N/A')}%", 0, 1)
        pdf.ln(2)
        
        # Lab values
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 6, 'Laboratory Values:', 0, 1)
        pdf.set_font('Arial', '', 9)
        pdf.cell(95, 5, f"  Hemoglobin: {patient_data.get('hemoglobin', 'N/A')} g/dL", 0, 0)
        pdf.cell(95, 5, f"  WBC Count: {patient_data.get('wbc', 'N/A')}/uL", 0, 1)
        pdf.cell(95, 5, f"  Platelet Count: {patient_data.get('platelet', 'N/A')}/uL", 0, 1)
        pdf.ln(5)
        
        # === SECTION 4: AI Analysis Results ===
        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(204, 0, 0)
        pdf.cell(0, 8, 'AI-Powered Diagnostic Analysis', 0, 1, 'L')
        pdf.set_text_color(0, 0, 0)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)
        
        # Top predictions
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 6, 'Predicted Conditions (Ranked by Confidence):', 0, 1)
        pdf.ln(2)
        
        for i, pred in enumerate(predictions[:3], 1):
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(10, 6, f"{i}.", 0, 0)
            pdf.cell(100, 6, self.sanitize_text(pred['disease']), 0, 0)
            
            # Color code based on confidence
            if pred['confidence'] > 60:
                pdf.set_text_color(0, 150, 0)  # Green
            elif pred['confidence'] > 40:
                pdf.set_text_color(255, 140, 0)  # Orange
            else:
                pdf.set_text_color(128, 128, 128)  # Gray
            
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, f"{pred['confidence']}% confidence", 0, 1)
            pdf.set_text_color(0, 0, 0)
        
        pdf.ln(3)
        
        # === SECTION 5: Clinical Reasoning ===
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, 'Clinical Reasoning', 0, 1, 'L')
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)
        
        pdf.set_font('Arial', '', 9)
        pdf.multi_cell(0, 5, self.sanitize_text(explanation.get('summary', 'Analysis complete.')))
        pdf.ln(2)
        
        if explanation.get('reasoning'):
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, 'Key Diagnostic Factors:', 0, 1)
            pdf.set_font('Arial', '', 9)
            for reason in explanation['reasoning']:
                pdf.cell(5, 5, '', 0, 0)
                pdf.multi_cell(0, 5, self.sanitize_text(f"- {reason}"))
        
        pdf.ln(3)
        
        # Red flags
        if explanation.get('red_flags'):
            pdf.set_font('Arial', 'B', 10)
            pdf.set_text_color(204, 0, 0)
            pdf.cell(0, 6, 'WARNING SIGNS DETECTED:', 0, 1)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('Arial', '', 9)
            for flag in explanation['red_flags']:
                pdf.cell(5, 5, '', 0, 0)
                pdf.multi_cell(0, 5, self.sanitize_text(flag))
            pdf.ln(2)
        
        # === SECTION 6: Treatment Support ===
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(0, 102, 0)
        pdf.cell(0, 8, 'Treatment Support Guidelines', 0, 1, 'L')
        pdf.set_text_color(0, 0, 0)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)
        
        # Disclaimer first
        pdf.set_fill_color(255, 250, 205)
        pdf.set_font('Arial', 'B', 9)
        pdf.cell(0, 6, 'IMPORTANT DISCLAIMER:', 0, 1, 'L', True)
        pdf.set_font('Arial', '', 8)
        for disc in treatment_plan.get('disclaimer', []):
            pdf.cell(5, 5, '', 0, 0)
            pdf.multi_cell(0, 4, self.sanitize_text(disc))
        pdf.ln(3)
        
        # Treatment categories
        categories = [
            ('immediate_care', 'Immediate Care Measures'),
            ('symptomatic_relief', 'Symptomatic Relief'),
            ('monitoring', 'Monitoring Requirements'),
            ('dietary', 'Dietary Recommendations')
        ]
        
        for key, title in categories:
            if treatment_plan.get(key):
                pdf.set_font('Arial', 'B', 10)
                pdf.cell(0, 6, title + ':', 0, 1)
                pdf.set_font('Arial', '', 9)
                for item in treatment_plan[key]:
                    pdf.cell(5, 5, '', 0, 0)
                    pdf.multi_cell(0, 5, self.sanitize_text(f"- {item}"))
                pdf.ln(2)
        
        # Red flags
        if treatment_plan.get('red_flags'):
            pdf.set_font('Arial', 'B', 10)
            pdf.set_text_color(204, 0, 0)
            pdf.cell(0, 6, 'RED FLAG SYMPTOMS:', 0, 1)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('Arial', '', 9)
            for flag in treatment_plan['red_flags']:
                pdf.cell(5, 5, '', 0, 0)
                pdf.multi_cell(0, 5, self.sanitize_text(flag))
        
        # === FINAL DISCLAIMER ===
        pdf.ln(8)
        pdf.set_fill_color(240, 240, 240)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 6, 'IMPORTANT MEDICAL DISCLAIMER', 0, 1, 'C', True)
        pdf.set_font('Arial', '', 8)
        pdf.multi_cell(0, 4, 
            'This report is generated by an AI-powered Clinical Decision Support System. '
            'It is intended to ASSIST healthcare professionals, NOT replace clinical judgment. '
            'All diagnostic and treatment decisions must be made by qualified medical practitioners '
            'after thorough clinical evaluation. This system does not provide medical advice, '
            'diagnosis, or treatment. Always consult with a licensed healthcare provider.')
        
        # Signature section
        pdf.ln(10)
        pdf.set_font('Arial', '', 9)
        pdf.cell(95, 6, 'Reviewed by: _______________________', 0, 0)
        pdf.cell(95, 6, 'Date: _______________________', 0, 1)
        pdf.ln(5)
        pdf.cell(95, 6, 'Physician Signature: _______________________', 0, 1)
        
        # Save PDF
        filename = f"{report_id}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        pdf.output(filepath)
        
        return filepath, filename