import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


DATA_PATH = Path(__file__).parent / "heart_failure_clinical_records_dataset.csv"
MODEL_DIR = Path(__file__).parent / "model"
MODEL_DIR.mkdir(exist_ok=True)


def load_data(path=DATA_PATH):
    df = pd.read_csv(path)
    return df


def prepare(df):
    df = df.copy()
    y = df.pop("DEATH_EVENT")
    X = df
    return X, y


def train_and_select(X_train, y_train, X_val, y_val):
    candidates = {
        "LogisticRegression": LogisticRegression(max_iter=1000),
        "RandomForest": RandomForestClassifier(n_estimators=200, random_state=0),
        "GradientBoosting": GradientBoostingClassifier(n_estimators=200, random_state=0),
    }

    results = {}
    best_name = None
    best_score = -1
    best_pipeline = None

    for name, clf in candidates.items():
        pipe = Pipeline([("scaler", StandardScaler()), ("clf", clf)])
        pipe.fit(X_train, y_train)
        score = pipe.score(X_val, y_val)
        results[name] = float(score)
        print(f"{name} accuracy: {score:.4f}")
        if score > best_score:
            best_score = score
            best_name = name
            best_pipeline = pipe

    return best_name, best_pipeline, results


def main():
    df = load_data()
    X, y = prepare(df)
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    best_name, best_pipeline, results = train_and_select(X_train, y_train, X_val, y_val)

    print(f"Best model: {best_name} with accuracy {results[best_name]:.4f}")

    # Save model, feature names and metrics
    joblib.dump(best_pipeline, MODEL_DIR / "best_model.joblib")
    joblib.dump(list(X.columns), MODEL_DIR / "columns.joblib")

    with open(MODEL_DIR / "metrics.json", "w") as f:
        json.dump({"best": best_name, "scores": results}, f, indent=2)


if __name__ == "__main__":
    main()
