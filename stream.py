import cv2
from posture_detection.calculate_posture import calculate_posture_values

def generate_frames(cap):
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        posture_heuristic = calculate_posture_values(frame)

        if posture_heuristic:
            cv2.putText(frame, f"posture: {posture_heuristic['score']:.2f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"shoulder_angle: {posture_heuristic['shoulder_angle']:.2f}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"head_tilt_angle: {posture_heuristic['head_tilt_angle']:.2f}", (10, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"neck_tilt_angle: {posture_heuristic['neck_tilt_angle']:.2f}", (10, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"nose_eye_tilt_angle: {posture_heuristic['nose_eye_tilt_angle']:.2f}", (10, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"ml: {posture_heuristic['ml']:.2f}", (10, 180),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Posture: NA", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Encode frame as JPEG.
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame_bytes = buffer.tobytes()

        # Yield frame in byte format.
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')