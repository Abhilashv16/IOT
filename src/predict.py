import joblib

from features import extract_features_csi


model = joblib.load("models/model.pkl")

scaler = joblib.load("models/scaler.pkl")


def predict(csi):

    features = extract_features_csi(csi)

    features = scaler.transform([features])

    prediction = model.predict(features)[0]

    return prediction