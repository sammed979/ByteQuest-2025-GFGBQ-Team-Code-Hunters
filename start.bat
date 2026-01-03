@echo off
echo Starting AI Clinical Decision Support System...
echo.

echo [1/3] Installing Python dependencies...
cd backend
pip install -r requirements.txt

echo.
echo [2/3] Training ML model...
python model.py

echo.
echo [3/3] Starting Flask server...
echo Server will be available at: http://localhost:5000
echo Open frontend/index.html in your browser
echo.
python app.py

pause