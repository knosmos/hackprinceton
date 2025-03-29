import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

# Load data
X = np.loadtxt("hybrid/features/X.txt")
Y = np.loadtxt("hybrid/features/Y.txt")

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Define neural net model
model = MLPClassifier(
    hidden_layer_sizes=(8),
    activation='relu',
    solver='adam',
    max_iter=5000,
    random_state=42
)

# Fit model
model.fit(X_scaled, Y)

# Prediction (in probabilities)
def predict(features):
    features_scaled = scaler.transform(features)
    return model.predict_proba(features_scaled)[0][1]