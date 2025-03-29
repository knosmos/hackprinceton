import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

# Load data
X = np.loadtxt("ml/features/X.txt")
Y = np.loadtxt("ml/features/Y.txt")

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Define neural net model
model = MLPClassifier(
    hidden_layer_sizes=(12, 8),
    activation='relu',
    solver='adam',
    max_iter=5000,
    random_state=42
)

# Fit model
model.fit(X_scaled, Y)

# Prediction function (returns probability of class 1)
def predict(features):
    features_scaled = scaler.transform(features)
    return model.predict_proba(features_scaled)[0][1]
