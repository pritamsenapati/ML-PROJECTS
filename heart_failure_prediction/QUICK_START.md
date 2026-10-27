# 🚀 CardioPredict - Quick Start Guide

## ⚡ 5-Minute Setup

### Step 1: Install Dependencies (2 min)
```powershell
cd "c:\Users\senap\OneDrive\Documents\Desktop\ML PROJECT\heart_failure_prediction"
pip install -r requirements.txt
```

### Step 2: Train Model (1 min)
```powershell
python train.py
```
You should see output like:
```
LogisticRegression accuracy: 0.8167
RandomForest accuracy: 0.7894
GradientBoosting accuracy: 0.8254
Best model: GradientBoosting with accuracy 0.8254
```

### Step 3: Run Enhanced App (1 min)
```powershell
python app_enhanced.py
```

### Step 4: Open Browser
Navigate to: **http://127.0.0.1:5000**

---

## 📖 Basic Usage

### 1️⃣ Create Your First Patient
- Click **👥 Patients** → **+ Add New Patient**
- Enter: Name, Age, Email, Phone
- Click **Create Patient**

### 2️⃣ Perform Risk Assessment
- Click **Assessment** (home page)
- Fill in all 12 clinical parameters
- Click **Analyze Risk**
- See prediction with contributing factors!

### 3️⃣ Track Patient History
- Go to **👥 Patients**
- Click on patient name
- See assessment history and risk trend chart

### 4️⃣ View Dashboard
- Click **📊 Dashboard**
- See overall statistics and recent assessments

---

## 🎯 What's New (Enhanced Version)

### ✨ New Features Added:

| Feature | Location | Purpose |
|---------|----------|---------|
| **Patient Management** | `/patients` | Store and manage patient records |
| **Assessment History** | `/patient/<id>` | Track all assessments for a patient |
| **Dashboard** | `/dashboard` | View analytics and statistics |
| **Risk Trends** | `/patient/<id>` | Chart showing risk over time |
| **PDF Export** | Patient details page | Download assessment reports |
| **Patient Search** | `/patients` | Find patients by name |
| **Responsive Navigation** | All pages | Professional multi-page interface |
| **Database Integration** | SQLite | Persistent data storage |

---

## 🔢 Example Patient Data

**Test values to try:**

```
Age: 60
Anaemia: No
Creatinine Phosphokinase: 400
Diabetes: No
Ejection Fraction: 40
High Blood Pressure: Yes
Platelets: 250000
Serum Creatinine: 1.8
Serum Sodium: 135
Sex: Male (1)
Smoking: No
Time: 200
```

Click **Analyze Risk** → You should see prediction + top 5 contributing factors!

---

## 📊 Dashboard Metrics

The dashboard shows:
- **Total Patients** - All registered patients
- **Total Assessments** - All risk assessments done
- **🔴 High Risk** - Count of high-risk patients
- **🟡 Moderate Risk** - Count of moderate-risk patients
- **🟢 Low Risk** - Count of low-risk patients
- **Average Risk Probability** - Mean risk across all assessments
- **Recent Assessments** - Last 5 assessments performed

---

## 🗄️ Database

The app automatically creates `heart_failure.db` with:
- **Patient Table** - Stores patient information
- **Assessment Table** - Stores all risk assessments

**No manual setup needed!**

---

## 📝 Common Tasks

### Export Assessment as PDF
1. Go to patient details page
2. Find assessment in history
3. Click **📥 Report** button
4. PDF downloads automatically

### Search for Patient
1. Go to **👥 Patients**
2. Type name in search box
3. Press Enter
4. Results filter in real-time

### View Risk Trend
1. Go to **👥 Patients**
2. Click patient name
3. See interactive chart of risk changes over time

---

## ⚙️ File Guide

| File | Purpose |
|------|---------|
| `app_enhanced.py` | Main application (START THIS) |
| `train.py` | ML model training script |
| `requirements.txt` | Python dependencies |
| `templates/` | HTML pages (6 files) |
| `static/style.css` | Styling |
| `static/script.js` | JavaScript logic |
| `model/best_model.joblib` | Trained ML model |

---

## 🎨 Interface Overview

### Navigation Bar
At the top of every page:
- **♥️ CardioPredict** - Logo/Home link
- **Assessment** - Prediction interface
- **📊 Dashboard** - Analytics
- **👥 Patients** - Patient management

### Color Scheme
- **🔴 High Risk** - Red (#e74c3c) - > 60% death probability
- **🟡 Moderate Risk** - Orange (#f39c12) - 30-60%
- **🟢 Low Risk** - Green (#27ae60) - < 30%

---

## ⚠️ Important Reminders

1. **This is for educational purposes only**
2. **Always consult healthcare professionals** for actual medical decisions
3. **Train the model first** (`python train.py`) before using app
4. **Close the app properly** - Use Ctrl+C in terminal

---

## 🐛 Quick Fixes

**App won't start?**
```powershell
# Clear old database
del heart_failure.db
# Reinstall dependencies  
pip install --upgrade -r requirements.txt
# Run again
python app_enhanced.py
```

**Port 5000 in use?**
Edit line in `app_enhanced.py`:
```python
if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Change to different port
```

---

## 📚 For Your Semester Project

### Key Points to Mention:

1. **Database-Driven System**
   - Uses SQLAlchemy ORM
   - Two-table relational design
   - Automatic schema creation

2. **Machine Learning Pipeline**
   - Data preprocessing with pandas
   - Model training with scikit-learn
   - Feature importance extraction

3. **Full-Stack Application**
   - Backend: Flask + Python
   - Frontend: HTML/CSS/JavaScript
   - Database: SQLite

4. **Professional Features**
   - Responsive UI design
   - Data visualization (Chart.js)
   - PDF report generation
   - Patient management system

---

## 🎓 Demo Scenario (For Presentation)

1. Show the Assessment page - "Fill in patient data"
2. Click Analyze - "See prediction and factors"
3. Go to Patients - "Patient records saved automatically"
4. Click on patient - "Full assessment history tracked"
5. Show Dashboard - "Overall analytics and statistics"
6. Export PDF - "Professional reports"

---

**Ready to use!** 🎉

For detailed documentation, see **README_ENHANCED.md**
