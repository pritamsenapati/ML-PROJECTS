# ♥️ CardioPredict - Heart Failure Risk Assessment System

## 📋 Project Overview

**CardioPredict** is a comprehensive machine learning-based web application for predicting heart failure risk in patients. Built as a 3rd semester mini project, it combines predictive analytics with a complete patient management system.

### Key Features
- **AI-Powered Risk Assessment** - Real-time prediction using trained ML models (Random Forest, Gradient Boosting, Logistic Regression)
- **Patient Management System** - Create, store, and manage patient records
- **Assessment History Tracking** - View complete history of risk assessments for each patient
- **Interactive Dashboard** - Real-time statistics and analytics
- **Risk Visualization** - Charts showing risk trends over time
- **Report Generation** - Export assessments as PDF reports
- **Patient Search** - Find patients by name with pagination
- **Contributing Factors Analysis** - Understand which clinical parameters drove the prediction

---

## 🏥 Clinical Parameters Analyzed

1. **Age** - Patient age in years
2. **Anaemia** - Binary indicator (0/1)
3. **Creatinine Phosphokinase** - CPK levels in U/L
4. **Diabetes** - Binary indicator (0/1)
5. **Ejection Fraction** - Percentage of blood pumped (%)
6. **High Blood Pressure** - Binary indicator (0/1)
7. **Platelets** - Platelet count
8. **Serum Creatinine** - Creatinine levels in mg/dL
9. **Serum Sodium** - Sodium levels in mEq/L
10. **Sex** - Binary indicator (0/1)
11. **Smoking** - Binary indicator (0/1)
12. **Time** - Follow-up period in days

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Step 1: Clone/Download Project
```bash
cd c:\Users\senap\OneDrive\Documents\Desktop\ML PROJECT\heart_failure_prediction
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Train the Model (First Time Only)
```bash
python train.py
```
This creates the ML model in the `model/` directory.

### Step 4: Run the Enhanced Application
```bash
python app_enhanced.py
```

### Step 5: Access the Application
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 📱 Application Structure

### Pages

#### 1. **Assessment Page** (`/`)
- Input patient clinical data
- Get real-time risk prediction
- View contributing factors
- Option to save assessment to patient record

#### 2. **Dashboard** (`/dashboard`)
- View overall statistics
  - Total patients
  - Total assessments
  - Risk distribution (High/Moderate/Low)
  - Average risk probability
- Recent assessments overview
- Quick analytics

#### 3. **Patients** (`/patients`)
- List all patients with search functionality
- Pagination support
- Filter by patient name
- Quick links to view patient details

#### 4. **Patient Details** (`/patient/<id>`)
- Complete patient information
- Assessment history
- Risk probability trend chart
- Export reports as PDF

#### 5. **New Patient** (`/patient/new`)
- Create new patient records
- Store basic information (name, age, email, phone)

---

## 🗄️ Database Schema

### Patient Table
```
id (Primary Key)
name (String)
age (Integer)
email (String)
phone (String)
created_at (DateTime)
updated_at (DateTime)
```

### Assessment Table
```
id (Primary Key)
patient_id (Foreign Key)
age, anaemia, creatinine_phosphokinase, ... (Clinical Data)
prediction (Integer: 0 or 1)
death_probability (Float: 0.0-1.0)
risk_level (String: Low/Moderate/High Risk)
top_factors (Text: JSON format)
created_at (DateTime)
```

---

## 🔍 Key Features Explained

### 1. **Risk Prediction**
- Uses trained machine learning models
- Returns prediction (Yes/No) and probability percentage
- Categorizes into risk levels:
  - **🟢 Low Risk**: < 30% death probability
  - **🟡 Moderate Risk**: 30-60% death probability  
  - **🔴 High Risk**: > 60% death probability

### 2. **Contributing Factors**
After prediction, the system displays:
- Top 5 clinical factors that influenced the prediction
- Patient's actual values for each factor
- Influence percentage for each factor
- Visual importance bars

### 3. **Risk Trend Analysis**
- Interactive chart showing risk probability over time
- Helps track patient health progression
- Identifies improving or deteriorating trends

### 4. **PDF Report Export**
- Professional report generation
- Includes:
  - Patient information
  - Assessment date
  - Risk level and probability
  - Clinical parameters table
  - Medical disclaimer

---

## 📊 API Endpoints

### Assessment API
```
POST /predict
```
**Request Body:**
```json
{
  "age": 60,
  "anaemia": 0,
  "creatinine_phosphokinase": 400,
  "diabetes": 0,
  "ejection_fraction": 40,
  "high_blood_pressure": 1,
  "platelets": 250000,
  "serum_creatinine": 1.8,
  "serum_sodium": 135,
  "sex": 1,
  "smoking": 0,
  "time": 200,
  "patient_id": 1
}
```

**Response:**
```json
{
  "prediction": 1,
  "death_probability": 0.85,
  "risk_level": "High Risk",
  "top_factors": {
    "ejection_fraction": {
      "importance": 0.25,
      "value": 40,
      "display_name": "Ejection Fraction"
    },
    ...
  }
}
```

### Risk History API
```
GET /api/patient/<patient_id>/risk-history
```

---

## 🧠 Machine Learning Models

The project trains and evaluates three models:

1. **Logistic Regression**
   - Simple, interpretable baseline
   - Fast predictions

2. **Random Forest**
   - Ensemble learning approach
   - Good feature importance extraction
   - Handles non-linear relationships

3. **Gradient Boosting**
   - Sequential error correction
   - High accuracy potential
   - Complex decision boundaries

**Best model is automatically selected** based on validation accuracy and used for predictions.

---

## 📈 Usage Example

### Scenario: Assessing a New Patient

1. **Create Patient Record**
   - Navigate to "Patients" → "+ Add New Patient"
   - Enter: John Doe, Age 65
   - Click "Create Patient"

2. **Perform Risk Assessment**
   - Go to "Assessment" page
   - Fill in clinical parameters from patient's lab results
   - Click "Analyze Risk"

3. **Review Results**
   - See risk level and probability
   - Review contributing factors
   - Understand which clinical parameters are concerning

4. **Track Progress**
   - Go to patient details page
   - See "Assessment History" with all past assessments
   - Watch risk trend chart
   - Export reports for medical record

---

## ⚠️ Important Disclaimers

- This tool is **for educational and clinical decision support ONLY**
- **NOT a substitute** for professional medical diagnosis
- Always consult qualified healthcare professionals
- Used trained on historical data - predictions may have limitations
- Regular model retraining recommended for production use

---

## 📁 Project Structure

```
heart_failure_prediction/
├── app.py                          # Original simple app
├── app_enhanced.py                 # Enhanced version with DB
├── train.py                        # ML model training script
├── requirements.txt                # Python dependencies
├── heart_failure.db               # SQLite database (auto-created)
├── heart_failure_clinical_records_dataset.csv  # Training data
│
├── model/
│   ├── best_model.joblib         # Trained ML model
│   ├── columns.joblib            # Feature column names
│   └── metrics.json              # Training metrics
│
├── templates/
│   ├── layout.html               # Base template with navigation
│   ├── index.html                # Assessment page
│   ├── dashboard.html            # Analytics dashboard
│   ├── patients.html             # Patients listing
│   ├── patient_detail.html       # Patient details & history
│   └── new_patient.html          # New patient form
│
├── static/
│   ├── style.css                 # Main stylesheet
│   └── script.js                 # Frontend JavaScript
│
└── README.md                      # This file
```

---

## 🔧 Technology Stack

- **Backend**: Flask, Flask-SQLAlchemy
- **Database**: SQLite3
- **ML**: scikit-learn, pandas, numpy
- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Chart.js
- **PDF Export**: ReportLab
- **Python Version**: 3.8+

---

## 🎓 Academic Merit

This project demonstrates:

✅ **Full-Stack Development**
- Backend: REST APIs, Database design, ORM
- Frontend: Responsive UI, JavaScript interactivity

✅ **Machine Learning**
- Model training and evaluation
- Feature importance analysis
- Model comparison and selection

✅ **Software Engineering**
- Project structure and organization
- Database design and relationships
- Error handling and validation
- Code documentation

✅ **Data Visualization** 
- Dashboard analytics
- Interactive charts
- Professional report generation

---

## 📝 How to Use as Semester Project

### Presentation Points

1. **Problem Statement**
   - Heart failure prediction is critical for patient care
   - Need for accessible risk assessment tool

2. **Solution Approach**
   - ML-based prediction system
   - Complete patient management system
   - Professional UI/UX design

3. **Technical Implementation**
   - Database design and relationships
   - ML pipeline and model evaluation
   - Web application architecture
   - Feature importance analysis

4. **Results & Testing**
   - Model accuracy metrics
   - Sample predictions with explanations
   - Dashboard statistics
   - Report generation

5. **Future Enhancements**
   - User authentication system
   - Multi-user support
   - Real-time monitoring alerts
   - Mobile application
   - Integration with hospital systems

---

## 🐛 Troubleshooting

### Issue: "Module not found" error
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Database errors
**Solution:** Delete `heart_failure.db` and restart the app:
```bash
# Remove old database
del heart_failure.db
# Run app to recreate
python app_enhanced.py
```

### Issue: Port 5000 already in use
**Solution:** Change port in app_enhanced.py:
```python
app.run(debug=True, port=5001)
```

---

## 📞 Support

For questions or issues:
1. Check the code comments
2. Review the documentation above
3. Verify all dependencies are installed
4. Ensure database is properly created

---

## 📜 License

This project is for educational purposes.

---

**Last Updated**: February 2026  
**Version**: 2.0 (Enhanced)  
**Status**: Ready for 3rd Semester Mini Project Submission
