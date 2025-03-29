from posture_detection.features import compute_ml_features_from_image
import os
import numpy as np

DATA_PATH = "posture_detection/images"
FEATURE_PATH = "posture_detection/features"
X = []
Y = []

for img_name in os.listdir(DATA_PATH):
    if img_name[-3 :] == "txt":
        continue

    img_path = os.path.join(DATA_PATH, img_name)
    out_path = DATA_PATH + "/out_" + img_name[4:7] + ".txt"

    # Handle input
    X.append(compute_ml_features_from_image(img_path))

    # Handle output
    with open(out_path, "r") as f:
        Y.append(int(f.read().strip()))


if __name__ == "__main__":
    X = np.array(X)
    Y = np.array(Y)

    np.savetxt(os.path.join(FEATURE_PATH, "X.txt"), X)
    np.savetxt(os.path.join(FEATURE_PATH, "Y.txt"), Y)