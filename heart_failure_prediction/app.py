from pathlib import Path
import joblib
import pandas as pd
import numpy as np
from flask import Flask, jsonify, render_template, request
from sklearn.preprocessing import StandardScaler

APP_DIR = Path(__file__).parent
MODEL_DIR = APP_DIR / "model"

app = Flask(__name__)


def load_artifacts():
    model = joblib.load(MODEL_DIR / "best_model.joblib")
    columns = joblib.load(MODEL_DIR / "columns.joblib")
    return model, columns


def get_feature_importance(model, columns, df):
    """Extract feature importance from the model"""
    clf = model.named_steps['clf']
    
    importance_dict = {}
    
    # Get feature importance based on model type
    if hasattr(clf, 'feature_importances_'):
        # RandomForest or GradientBoosting
        importances = clf.feature_importances_
    elif hasattr(clf, 'coef_'):
        # LogisticRegression - use absolute coefficients
        importances = np.abs(clf.coef_[0])
    else:
        return {}
    
    # Map importances to column names
    for col, imp in zip(columns, importances):
        importance_dict[col] = float(imp)
    
    # Get top 5 features
    top_features = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Get actual values for top features
    result = {}
    for feature, importance in top_features:
        value = df[feature].iloc[0]
        result[feature] = {
            'importance': importance,
            'value': float(value),
            'display_name': feature.replace('_', ' ').title()
        }
    
    return result


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.json or request.form.to_dict()
    model, columns = load_artifacts()

    # Collect features in correct order
    values = []
    for c in columns:
        v = data.get(c)
        if v is None:
            return jsonify({"error": f"Missing feature {c}"}), 400
        values.append(float(v))

    df = pd.DataFrame([values], columns=columns)
    prob = model.predict_proba(df)[0, 1]
    pred = int(model.predict(df)[0])
    
    # Get feature importance
    top_features = get_feature_importance(model, columns, df)
    
    return jsonify({
        "prediction": pred, 
        "death_probability": float(prob),
        "top_factors": top_features
    })


if __name__ == "__main__":
    app.run(debug=True)
