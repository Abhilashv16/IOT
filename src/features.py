import numpy as np


def extract_features_csi(csi):

    csi = np.array(csi)

    features = [
        np.mean(csi),
        np.std(csi),
        np.max(csi),
        np.min(csi),
        np.median(csi),
        np.percentile(csi, 25),
        np.percentile(csi, 75),
        np.var(csi),
        np.mean(np.abs(np.diff(csi)))
    ]

    return features