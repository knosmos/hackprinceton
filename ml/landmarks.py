import cv2
import mediapipe as mp

def get_landmarks(image_path):
    mp_pose = mp.solutions.pose

    with mp_pose.Pose(
            static_image_mode=True,
            model_complexity=1,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:

        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Image not found at path: {image_path}")

        # Convert the image to RGB.
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = pose.process(image_rgb)
        return results.pose_landmarks.landmark if results.pose_landmarks else None