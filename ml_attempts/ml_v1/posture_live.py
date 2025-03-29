import cv2
from ml.landmarks import parameterize
from ml.regression import predict
import numpy as np

def show_posture_live():
    cap = cv2.VideoCapture(0)  # Open webcam

    while True:
        ret, frame = cap.read()

        if not ret:
            break
        
        # Get posture score
        posture = float(predict(np.array(parameterize(frame)).reshape(1, -1)))

        # Draw posture score on the frame
        cv2.putText(
            frame,
            f"Posture: {posture:.2f}",
            (10, 30),  # Top-left corner
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),  # Green text
            2
        )

        cv2.imshow('Posture Monitor', frame)

        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    show_posture_live()