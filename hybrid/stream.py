import cv2
from hybrid.features import *
from hybrid.model import predict
import numpy as np

def show_posture_live():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        params = parameterize(frame)
        posture = float(predict(np.array(params[:]).reshape(1, -1)))

        cv2.putText(
            frame,
            f"Posture: {posture:.2f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
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