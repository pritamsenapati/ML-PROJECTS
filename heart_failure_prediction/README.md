# Heart Failure Prediction

Files added:

- `train.py` - trains multiple classifiers and saves the best model to `model/best_model.joblib`
- `app.py` - Flask app that serves the frontend and prediction endpoint
- `templates/index.html` - frontend form
- `static/style.css` and `static/script.js` - frontend assets
- `requirements.txt` - Python dependencies

Quick start:

1. Install dependencies:

```
pip install -r requirements.txt
```

2. Train the model (from this folder):

```
python train.py
```

3. Run the web app:

```
python app.py
```

4. Open http://127.0.0.1:5000/ in your browser.
