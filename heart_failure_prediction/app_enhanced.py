from pathlib import Path
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
from flask import Flask, jsonify, render_template, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

APP_DIR = Path(__file__).parent
MODEL_DIR = APP_DIR / "model"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{APP_DIR / "heart_failure.db"}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ======================== DATABASE MODELS ========================

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    assessments = db.relationship('Assessment', backref='patient', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Patient {self.name}>'


class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    
    # Patient data
    age = db.Column(db.Float)
    anaemia = db.Column(db.Integer)
    creatinine_phosphokinase = db.Column(db.Float)
    diabetes = db.Column(db.Integer)
    ejection_fraction = db.Column(db.Float)
    high_blood_pressure = db.Column(db.Integer)
    platelets = db.Column(db.Float)
    serum_creatinine = db.Column(db.Float)
    serum_sodium = db.Column(db.Float)
    sex = db.Column(db.Integer)
    smoking = db.Column(db.Integer)
    time = db.Column(db.Float)
    
    # Prediction results
    prediction = db.Column(db.Integer)
    death_probability = db.Column(db.Float)
    risk_level = db.Column(db.String(20))
    top_factors = db.Column(db.Text)  # JSON stored as text
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Assessment {self.patient_id} - {self.risk_level}>'


# ======================== HELPER FUNCTIONS ========================

def load_artifacts():
    model = joblib.load(MODEL_DIR / "best_model.joblib")
    columns = joblib.load(MODEL_DIR / "columns.joblib")
    return model, columns


def get_feature_importance(model, columns, df):
    """Extract feature importance from the model"""
    clf = model.named_steps['clf']
    
    importance_dict = {}
    
    if hasattr(clf, 'feature_importances_'):
        importances = clf.feature_importances_
    elif hasattr(clf, 'coef_'):
        importances = np.abs(clf.coef_[0])
    else:
        return {}
    
    for col, imp in zip(columns, importances):
        importance_dict[col] = float(imp)
    
    top_features = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)[:5]
    
    result = {}
    for feature, importance in top_features:
        value = df[feature].iloc[0]
        result[feature] = {
            'importance': importance,
            'value': float(value),
            'display_name': feature.replace('_', ' ').title()
        }
    
    return result


def get_risk_level(probability):
    """Determine risk level from probability"""
    if probability > 0.6:
        return 'High Risk'
    elif probability > 0.3:
        return 'Moderate Risk'
    else:
        return 'Low Risk'


# ======================== ROUTES ========================

@app.route("/")
def index():
    """Home page - Assessment interface"""
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    """Dashboard with analytics"""
    total_patients = Patient.query.count()
    total_assessments = Assessment.query.count()
    
    high_risk_count = Assessment.query.filter_by(risk_level='High Risk').count()
    moderate_risk_count = Assessment.query.filter_by(risk_level='Moderate Risk').count()
    low_risk_count = Assessment.query.filter_by(risk_level='Low Risk').count()
    
    avg_risk_prob = db.session.query(db.func.avg(Assessment.death_probability)).scalar()
    avg_risk_prob = round(avg_risk_prob * 100, 2) if avg_risk_prob else 0
    
    recent_assessments = Assessment.query.order_by(Assessment.created_at.desc()).limit(5).all()
    
    stats = {
        'total_patients': total_patients,
        'total_assessments': total_assessments,
        'high_risk': high_risk_count,
        'moderate_risk': moderate_risk_count,
        'low_risk': low_risk_count,
        'avg_risk_probability': avg_risk_prob,
        'recent_assessments': recent_assessments
    }
    
    return render_template("dashboard.html", stats=stats)


@app.route("/patients")
def patients_list():
    """List all patients"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = Patient.query
    if search:
        query = query.filter(Patient.name.ilike(f'%{search}%'))
    
    patients = query.order_by(Patient.created_at.desc()).paginate(page=page, per_page=10)
    
    return render_template("patients.html", patients=patients, search=search)


@app.route("/patient/<int:patient_id>")
def patient_detail(patient_id):
    """View patient details and assessment history"""
    patient = Patient.query.get_or_404(patient_id)
    assessments = Assessment.query.filter_by(patient_id=patient_id).order_by(Assessment.created_at.desc()).all()
    
    return render_template("patient_detail.html", patient=patient, assessments=assessments)


@app.route("/patient/new", methods=['GET', 'POST'])
def new_patient():
    """Create new patient"""
    if request.method == 'POST':
        patient = Patient(
            name=request.form.get('name'),
            age=request.form.get('age'),
            email=request.form.get('email'),
            phone=request.form.get('phone')
        )
        db.session.add(patient)
        db.session.commit()
        return redirect(url_for('patient_detail', patient_id=patient.id))
    
    return render_template("new_patient.html")


@app.route("/predict", methods=["POST"])
def predict():
    """Make prediction and save assessment"""
    data = request.json or request.form.to_dict()
    patient_id = data.get('patient_id')
    
    model, columns = load_artifacts()

    values = []
    for c in columns:
        v = data.get(c)
        if v is None:
            return jsonify({"error": f"Missing feature {c}"}), 400
        values.append(float(v))

    df = pd.DataFrame([values], columns=columns)
    prob = model.predict_proba(df)[0, 1]
    pred = int(model.predict(df)[0])
    risk_level = get_risk_level(prob)
    
    top_factors = get_feature_importance(model, columns, df)
    
    # Save assessment to database if patient_id provided
    if patient_id:
        patient = Patient.query.get(patient_id)
        if patient:
            assessment = Assessment(
                patient_id=patient_id,
                age=float(data.get('age')),
                anaemia=int(data.get('anaemia')),
                creatinine_phosphokinase=float(data.get('creatinine_phosphokinase')),
                diabetes=int(data.get('diabetes')),
                ejection_fraction=float(data.get('ejection_fraction')),
                high_blood_pressure=int(data.get('high_blood_pressure')),
                platelets=float(data.get('platelets')),
                serum_creatinine=float(data.get('serum_creatinine')),
                serum_sodium=float(data.get('serum_sodium')),
                sex=int(data.get('sex')),
                smoking=int(data.get('smoking')),
                time=float(data.get('time')),
                prediction=pred,
                death_probability=prob,
                risk_level=risk_level,
                top_factors=str(top_factors)
            )
            db.session.add(assessment)
            db.session.commit()
    
    return jsonify({
        "prediction": pred, 
        "death_probability": float(prob),
        "risk_level": risk_level,
        "top_factors": top_factors
    })


@app.route("/export/<int:assessment_id>")
def export_assessment(assessment_id):
    """Export assessment as PDF"""
    assessment = Assessment.query.get_or_404(assessment_id)
    patient = assessment.patient
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e3c72'),
        spaceAfter=30,
        alignment=1
    )
    
    # Title
    elements.append(Paragraph("CardioPredict - Assessment Report", title_style))
    elements.append(Spacer(1, 12))
    
    # Patient Info
    elements.append(Paragraph(f"<b>Patient Name:</b> {patient.name}", styles['Normal']))
    elements.append(Paragraph(f"<b>Assessment Date:</b> {assessment.created_at.strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Results
    risk_color = '#e74c3c' if assessment.risk_level == 'High Risk' else '#f39c12' if assessment.risk_level == 'Moderate Risk' else '#27ae60'
    elements.append(Paragraph(f"<b><font color='{risk_color}'>Risk Level: {assessment.risk_level}</font></b>", styles['Heading2']))
    elements.append(Paragraph(f"<b>Death Probability:</b> {assessment.death_probability*100:.2f}%", styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Patient Data Table
    data = [
        ['Clinical Parameter', 'Value'],
        ['Age', f"{assessment.age}"],
        ['Ejection Fraction', f"{assessment.ejection_fraction}%"],
        ['Serum Creatinine', f"{assessment.serum_creatinine} mg/dL"],
        ['Serum Sodium', f"{assessment.serum_sodium} mEq/L"],
        ['Creatinine Phosphokinase', f"{assessment.creatinine_phosphokinase} U/L"],
        ['Platelets', f"{assessment.platelets:,.0f}"],
    ]
    
    t = Table(data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(t)
    
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("<i>This assessment is for clinical decision support only. Always consult with qualified healthcare professionals.</i>", styles['Normal']))
    
    doc.build(elements)
    buffer.seek(0)
    
    return send_file(buffer, mimetype='application/pdf', as_attachment=True, download_name=f'assessment_{assessment_id}.pdf')


@app.route("/api/patient/<int:patient_id>/risk-history")
def risk_history_api(patient_id):
    """API endpoint for patient risk history"""
    assessments = Assessment.query.filter_by(patient_id=patient_id).order_by(Assessment.created_at).all()
    
    data = {
        'dates': [a.created_at.strftime('%Y-%m-%d %H:%M') for a in assessments],
        'probabilities': [a.death_probability * 100 for a in assessments],
        'risk_levels': [a.risk_level for a in assessments]
    }
    
    return jsonify(data)


# ======================== INITIALIZATION ========================

@app.before_request
def create_tables():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
