from posture_detection.features import get_landmarks, calculate_heuristic_info, compute_ml_features_from_landmarks
from posture_detection.model import predict
import mediapipe as mp
import numpy as np

def calculate_posture_values(image):
    landmarks = get_landmarks(image)

    # No visibility
    if landmarks is None:
        return None 
    
    heuristics = calculate_heuristic_info(landmarks)
    features = compute_ml_features_from_landmarks(landmarks)

    # Start heuristic calculations
    score = 100

    # Min angle from x axis
    score -= 1.15 * max(heuristics["shoulder_angle"] - 3, 0)
    score -= 1.15 * max(heuristics["head_tilt_angle"] - 3, 0)

    # Neck to nose
    score -= 1.05 * max(heuristics["neck_tilt_angle"] - 5, 0)

    # Nose to center of eyes
    score -= 1.05 * max(heuristics["nose_eye_tilt_angle"] - 10, 0)

    # ML score
    ml_result = float(predict(np.array(features).reshape(1, -1)))

    if ml_result < 0.005:
        score -= 35
    elif ml_result < 0.01:
        score -= 29
    elif ml_result < 0.05:
        score -= 24
    elif ml_result < 0.1:
        score -= 19
    elif ml_result < 0.15:
        score -= 15
    else:
        score -= (1 - ml_result) * 15

    score = max(score, 0)

    # Return all results for easy debugging for now
    all_results = dict(heuristics)
    all_results["score"] = score
    all_results["ml"] = ml_result
    return all_results

