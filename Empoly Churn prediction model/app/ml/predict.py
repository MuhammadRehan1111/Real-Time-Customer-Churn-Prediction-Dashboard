import pickle
import pandas as pd

with open("app/ml/model.pkl", "rb") as f:
    model = pickle.load(f)

def predict_customer(data: dict):
    df = pd.DataFrame([data])

    prob = model.predict_proba(df)[0][1]
    pred = model.predict(df)[0]

    return {
        "prediction": "Yes" if pred == 1 else "No",
        "probability": float(prob)
    }