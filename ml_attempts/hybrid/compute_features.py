from hybrid.features import parameterize
import os
import numpy as np

DATA_PATH = "hybrid/images"
FEATURE_PATH = "hybrid/features"
X = []
Y = []

for img_name in os.listdir(DATA_PATH):
    if img_name[-3 :] == "txt":
        continue

    img_path = os.path.join(DATA_PATH, img_name)
    out_path = DATA_PATH + "/out_" + img_name[4:7] + ".txt"

    # Handle input
    X.append(parameterize(img_path))

    # Handle output
    with open(out_path, "r") as f:
        Y.append(int(f.read().strip()))


if __name__ == "__main__":
    X = np.array(X)
    Y = np.array(Y)

    np.savetxt(os.path.join(FEATURE_PATH, "X.txt"), X)
    np.savetxt(os.path.join(FEATURE_PATH, "Y.txt"), Y)