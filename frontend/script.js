// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// Global variable to store analysis results
let currentAnalysisData = null;

// DOM Elements
const patientForm = document.getElementById('patientForm');
const loadingIndicator = document.getElementById('loadingIndicator');
const resultsSection = document.getElementById('resultsSection');
const predictionsContainer = document.getElementById('predictionsContainer');
const explanationContainer = document.getElementById('explanationContainer');
const treatmentContainer = document.getElementById('treatmentContainer');
const downloadReportBtn = document.getElementById('downloadReportBtn');
const newAnalysisBtn = document.getElementById('newAnalysisBtn');

// Event Listeners
patientForm.addEventListener('submit', handleFormSubmit);
downloadReportBtn.addEventListener('click', downloadReport);
newAnalysisBtn.addEventListener('click', resetForm);

// Form Submit Handler
async function handleFormSubmit(e) {
    e.preventDefault();

    // Collect form data
    const formData = new FormData(patientForm);
    const patientData = {
        patient_name: formData.get('patient_name'),
        age: parseInt(formData.get('age')),
        gender: formData.get('gender'),
        fever: formData.get('fever') ? 1 : 0,
        cough: formData.get('cough') ? 1 : 0,
        headache: formData.get('headache') ? 1 : 0,
        fatigue: formData.get('fatigue') ? 1 : 0,
        bp_systolic: parseInt(formData.get('bp_systolic')),
        spo2: parseInt(formData.get('spo2')),
        hemoglobin: parseFloat(formData.get('hemoglobin')),
        wbc: parseInt(formData.get('wbc')),
        platelet: parseInt(formData.get('platelet'))
    };

    // Validate data
    if (!validatePatientData(patientData)) {
        alert('Please check all input values are within valid ranges');
        return;
    }

    // Show loading, hide results
    loadingIndicator.style.display = 'block';
    resultsSection.style.display = 'none';

    try {
        // Call prediction API
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(patientData)
        });

        if (!response.ok) {
            throw new Error('API request failed');
        }

        const data = await response.json();

        if (data.success) {
            currentAnalysisData = {
                patient_data: patientData,
                predictions: data.predictions,
                explanation: data.explanation,
                treatment: data.treatment
            };

            displayResults(data);
        } else {
            throw new Error(data.error || 'Analysis failed');
        }

    } catch (error) {
        console.error('Error:', error);
        if (error.message === 'Failed to fetch') {
            alert('Network Error: Unable to connect to backend server. Please ensure the server is running on ' + API_BASE_URL);
        } else {
            alert(error.message || 'Error analyzing patient data.');
        }
    } finally {
        loadingIndicator.style.display = 'none';
    }
}

// Validate Patient Data
function validatePatientData(data) {
    if (isNaN(data.age) || data.age < 1 || data.age > 120) return false;
    if (isNaN(data.bp_systolic) || data.bp_systolic < 50 || data.bp_systolic > 250) return false;
    if (isNaN(data.spo2) || data.spo2 < 50 || data.spo2 > 100) return false;
    if (isNaN(data.hemoglobin) || data.hemoglobin < 5 || data.hemoglobin > 20) return false;
    if (isNaN(data.wbc) || data.wbc < 1000 || data.wbc > 50000) return false;
    if (isNaN(data.platelet) || data.platelet < 10000 || data.platelet > 600000) return false;
    return true;
}

// Display Results
function displayResults(data) {
    // Display predictions
    displayPredictions(data.predictions);

    // Display explanation
    displayExplanation(data.explanation);

    // Display treatment
    displayTreatment(data.treatment, data.warnings);

    // Show results section
    resultsSection.style.display = 'block';

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Display Predictions
function displayPredictions(predictions) {
    let html = '';

    predictions.forEach((pred, index) => {
        const rank = index + 1;
        const confidenceClass = getConfidenceClass(pred.confidence);

        html += `
            <div class="prediction-item rank-${rank}">
                <div>
                    <div style="font-size: 14px; color: #6c757d; margin-bottom: 5px;">
                        ${rank === 1 ? '🎯 Primary Diagnosis' : `Alternative ${rank}`}
                    </div>
                    <div class="prediction-name">${pred.disease}</div>
                </div>
                <div class="confidence-badge ${confidenceClass}">
                    ${pred.confidence}%
                </div>
            </div>
        `;
    });

    predictionsContainer.innerHTML = html;
}

// Get Confidence Class
function getConfidenceClass(confidence) {
    if (confidence >= 60) return 'confidence-high';
    if (confidence >= 40) return 'confidence-medium';
    return 'confidence-low';
}

// Display Explanation
function displayExplanation(explanation) {
    let html = `
        <div class="explanation-summary">
            <strong>Summary:</strong>
            <p>${explanation.summary}</p>
        </div>
    `;

    // Key findings
    if (explanation.key_findings && explanation.key_findings.length > 0) {
        html += `
            <h4 style="margin-top: 25px; color: #0066cc;">Clinical Findings:</h4>
            <ul class="findings-list">
                ${explanation.key_findings.map(finding => `<li>✓ ${finding}</li>`).join('')}
            </ul>
        `;
    }

    // Reasoning
    if (explanation.reasoning && explanation.reasoning.length > 0) {
        html += `
            <h4 style="margin-top: 25px; color: #0066cc;">Diagnostic Reasoning:</h4>
            <ul class="reasoning-list">
                ${explanation.reasoning.map(reason => `<li>• ${reason}</li>`).join('')}
            </ul>
        `;
    }

    // Red flags
    if (explanation.red_flags && explanation.red_flags.length > 0) {
        html += `
            <h4 style="margin-top: 25px; color: #dc3545;">⚠️ Warning Signs:</h4>
            ${explanation.red_flags.map(flag => `<div class="red-flag-item">${flag}</div>`).join('')}
        `;
    }

    explanationContainer.innerHTML = html;
}

// Display Treatment
function displayTreatment(treatment, warnings) {
    let html = '';

    // Warnings first
    if (warnings && warnings.length > 0) {
        html += `
            <div style="background: #fff5f5; border: 2px solid #dc3545; border-radius: 8px; padding: 15px; margin-bottom: 20px;">
                <strong style="color: #dc3545;">⚠️ Clinical Warnings:</strong>
                ${warnings.map(w => `<div style="margin-top: 8px;">• ${w}</div>`).join('')}
            </div>
        `;
    }

    // Treatment categories
    const categories = [
        { key: 'immediate_care', title: '🚨 Immediate Care Measures', icon: '🏥' },
        { key: 'symptomatic_relief', title: '💊 Symptomatic Relief', icon: '💊' },
        { key: 'monitoring', title: '📊 Monitoring Requirements', icon: '📊' },
        { key: 'dietary', title: '🥗 Dietary Recommendations', icon: '🥗' },
        { key: 'lifestyle', title: '🏃 Lifestyle Modifications', icon: '🏃' }
    ];

    categories.forEach(cat => {
        if (treatment[cat.key] && treatment[cat.key].length > 0) {
            html += `
                <div class="treatment-category">
                    <h4>${cat.icon} ${cat.title}</h4>
                    <ul class="treatment-list">
                        ${treatment[cat.key].map(item => `<li>${item}</li>`).join('')}
                    </ul>
                </div>
            `;
        }
    });

    // Red flags
    if (treatment.red_flags && treatment.red_flags.length > 0) {
        html += `
            <div class="treatment-category">
                <h4 style="color: #dc3545;">⚠️ Red Flag Symptoms</h4>
                ${treatment.red_flags.map(flag => `<div class="red-flag-item">${flag}</div>`).join('')}
            </div>
        `;
    }

    treatmentContainer.innerHTML = html;
}

// Download Report
async function downloadReport() {
    if (!currentAnalysisData) {
        alert('No analysis data available to download');
        return;
    }

    try {
        downloadReportBtn.disabled = true;
        downloadReportBtn.innerHTML = '<span class="btn-icon">⏳</span> Generating PDF...';

        const response = await fetch(`${API_BASE_URL}/generate-report`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(currentAnalysisData)
        });

        if (!response.ok) {
            throw new Error('Failed to generate report');
        }

        // Download the PDF
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `clinical-report-${Date.now()}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        // Show success message
        alert('Clinical report downloaded successfully!');

    } catch (error) {
        console.error('Error:', error);
        alert('Error generating PDF report. Please try again.');
    } finally {
        downloadReportBtn.disabled = false;
        downloadReportBtn.innerHTML = '<span class="btn-icon">📄</span> Download Clinical Report (PDF)';
    }
}

// Reset Form
function resetForm() {
    patientForm.reset();
    resultsSection.style.display = 'none';
    currentAnalysisData = null;
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Form validation on input
patientForm.addEventListener('input', (e) => {
    const input = e.target;
    if (input.type === 'number') {
        const min = parseInt(input.min);
        const max = parseInt(input.max);
        const value = parseFloat(input.value);

        if (value < min || value > max) {
            input.style.borderColor = '#dc3545';
        } else {
            input.style.borderColor = '#28a745';
        }
    }
});

// Console log for debugging
console.log('🚀 AI Clinical Decision Support System Frontend Loaded');
console.log('📡 API Base URL:', API_BASE_URL);