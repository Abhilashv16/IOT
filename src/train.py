import os
import joblib
import lightgbm as lgb

from sklearn.model_selection import train_test_split

from preprocess import scale_features
from load_data import load_dataset


def train():

    print("Loading datasets...")

    X, y = load_dataset()

    print("Total samples:", len(X))
    print("Labels:", set(y))

    if len(X) == 0:

        print("No data found")

        return

    # =====================================
    # SCALE
    # =====================================

    X, scaler = scale_features(X)

    # =====================================
    # SPLIT
    # =====================================

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    # =====================================
    # MODEL
    # =====================================

    model = lgb.LGBMClassifier(
        n_estimators=300,
        learning_rate=0.03
    )

    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)

    print("Accuracy:", accuracy * 100, "%")

    # =====================================
    # SAVE
    # =====================================

    os.makedirs("models", exist_ok=True)

    joblib.dump(model, "models/model.pkl")
    joblib.dump(scaler, "models/scaler.pkl")

    print("Model saved")


if __name__ == "__main__":
    train()