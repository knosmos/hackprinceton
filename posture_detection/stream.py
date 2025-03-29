import cv2
from posture_detection.features import *
from posture_detection.model import predict
import numpy as np

def show_posture_live():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            break
        
        ml_score = float(predict(np.array(parameterize_ml(frame)).reshape(1, -1)))
        posture_heuristic = parameterize_heuristics(frame)

        cv2.putText(frame, f"Posture: {posture_heuristic[0] - (35 if ml_score < 0.005 else (1 - ml_score) * 15):.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.putText(frame, f"shoulder_angle: {posture_heuristic[1]:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"head_tilt_angle: {posture_heuristic[2]:.2f}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"neck_tilt_angle: {posture_heuristic[3]:.2f}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"nose_eye_tilt_angle: {posture_heuristic[4]:.2f}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # cv2.putText(frame, f"ear_eye_right: {posture_heuristic[5]:.2f}", (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # cv2.putText(frame, f"ear_eye_left: {posture_heuristic[6]:.2f}", (10, 210), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"ml: {ml_score:.2f}", (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Posture Monitor', frame)

        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    show_posture_live()