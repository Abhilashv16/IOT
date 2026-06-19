import os
import csv
import json
import pandas as pd

from features import extract_features_csi



def parse_csi_line(line):

    if "CSI_DATA" not in line:
        return None

    try:
        _, rest = line.split("CSI_DATA,", 1)

        row = next(csv.reader([rest]))

        csi = json.loads(row[-1])

        if len(csi) != 128:
            return None

        return csi

    except:
        return None


def map_csi_label(label_num):

    if label_num in [0, 1]:
        return 0
    else:
        return 1



def load_csi_dataset(base_path="data/raw"):

    X = []
    y = []

    if not os.path.exists(base_path):
        return X, y

    for person in os.listdir(base_path):

        person_path = os.path.join(base_path, person)

        if not os.path.isdir(person_path):
            continue

        for label_folder in os.listdir(person_path):

            label_path = os.path.join(person_path, label_folder)

            if not os.path.isdir(label_path):
                continue

            try:
                label_num = int(label_folder.split("_")[-1])

            except:
                continue

            final_label = map_csi_label(label_num)

            for file in os.listdir(label_path):

                if not file.endswith(".data"):
                    continue

                file_path = os.path.join(label_path, file)

                try:
                    with open(file_path, "r") as f:

                        for line in f:

                            csi = parse_csi_line(line)

                            if csi is None:
                                continue

                            features = extract_features_csi(csi)

                            X.append(features)
                            y.append(final_label)

                except:
                    continue

    return X, y


def load_live_csv(csv_path="logs/live_predict.csv"):

    X = []
    y = []

    if not os.path.exists(csv_path):

        print("live_predict.csv not found")

        return X, y

    try:

        df = pd.read_csv(csv_path)

        print("Live CSV rows:", len(df))

        required_cols = [
            "rssi",
            "mean",
            "std",
            "max",
            "min",
            "prediction"
        ]

        for col in required_cols:

            if col not in df.columns:

                print("Missing column:", col)

                return X, y

        for _, row in df.iterrows():

            features = [
                row["rssi"],
                row["mean"],
                row["std"],
                row["max"],
                row["min"],
                row["mean"] - row["min"],
                row["max"] - row["mean"],
                row["std"] ** 2,
                abs(row["max"] - row["min"])
            ]

            label = 0 if row["prediction"] == "OBJECT" else 1

            X.append(features)
            y.append(label)

    except Exception as e:

        print("CSV ERROR:", e)

    return X, y


def load_dataset():

    X_csi, y_csi = load_csi_dataset()

    X_live, y_live = load_live_csv()

    print("CSI samples:", len(X_csi))
    print("Live samples:", len(X_live))

    X = X_csi + X_live
    y = y_csi + y_live

    return X, y