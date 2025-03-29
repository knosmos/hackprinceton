import cv2
from posture_detection.calculate_posture import calculate_posture_values
import numpy as np

def show_posture_live():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            break
        
        posture_heuristic = calculate_posture_values(frame)

        if posture_heuristic:
            cv2.putText(frame, f"Posture: {posture_heuristic["score"]:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"shoulder_angle: {posture_heuristic["shoulder_angle"]:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"head_tilt_angle: {posture_heuristic["head_tilt_angle"]:.2f}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"neck_tilt_angle: {posture_heuristic["neck_tilt_angle"]:.2f}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"nose_eye_tilt_angle: {posture_heuristic["nose_eye_tilt_angle"]:.2f}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"ml: {posture_heuristic["ml"]:.2f}", (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, f"Posture: NA", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Posture Monitor', frame)

        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    show_posture_live()