# 🩺 AI Clinical Decision Support System

**Hackathon MVP** - An intelligent healthcare application that assists doctors in analyzing patient data, predicting diseases, and suggesting treatment guidelines using Machine Learning.

---

## 🎯 Features

- **Disease Prediction** - Random Forest ML model predicting 5 diseases (Dengue, Flu, Pneumonia, Anemia, Hypertension)
- **Explainable AI** - Transparent reasoning for every prediction
- **Treatment Guidelines** - Rule-based, non-prescriptive care suggestions
- **PDF Reports** - Downloadable clinical reports
- **Responsive UI** - Clean, medical-themed interface

---

## 🚀 Quick Start
#### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### 2. Train the Model (First Time Only)
```bash
python model.py
```

#### 3. Start Backend Server
```bash
python app.py
```
Server will run at: `http://localhost:5000`

#### 4. Open Frontend
Open `frontend/index.html` in your web browser.

---

## 📁 Project Structure

```
BYTEQUEST/
├── frontend/
│   ├── index.html          # User interface
│   ├── style.css           # Styling
│   └── script.js           # Frontend logic
│
├── backend/
│   ├── app.py              # Flask API server
│   ├── model.py            # ML model (Random Forest)
│   ├── explainer.py        # AI explanations
│   ├── rules.py            # Treatment rules
│   ├── report.py           # PDF generator
│   ├── requirements.txt    # Dependencies
│   │
│   ├── models/             # Trained model files
│   └── outputs/reports/    # Generated PDFs
│
├── data/
│   └── clinical_data.csv   # Training dataset
│
├── start.bat               # One-click setup (Windows)
├── README.md               # This file
└── HACKATHON_SUMMARY.md    # Project presentation summary
```

---

## 🧪 Test Case

**Sample Patient Data:**
- Age: 28 years
- Gender: Female
- Symptoms: Fever ✓, Headache ✓
- BP: 112 mmHg
- SpO2: 98%
- Hemoglobin: 12.5 g/dL
- WBC: 4000/μL
- Platelet: 90,000/μL

**Expected Result:** Dengue (due to low platelet count)

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/predict` | POST | Get disease predictions |
| `/api/generate-report` | POST | Generate PDF report |
| `/api/model-info` | GET | Model information |
| `/api/diseases` | GET | Supported diseases |

---

## 🛠️ Tech Stack

- **Frontend:** HTML5, CSS3, JavaScript
- **Backend:** Python, Flask
- **ML Model:** scikit-learn (Random Forest)
- **PDF Generation:** fpdf
- **Data Processing:** Pandas, NumPy

---

## ⚖️ Disclaimer

This is a **decision support tool** for healthcare professionals. It is NOT a replacement for clinical judgment. Final diagnosis and treatment decisions must be made by licensed medical practitioners.

---

## 📝 License

Educational & Research Purposes Only

---

**Built for Hackathon 2026** 🚀
