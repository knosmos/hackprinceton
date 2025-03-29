import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose

pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    enable_segmentation=False,
)

def get_all_landmarks_path(image_path):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)
    return results.pose_landmarks.landmark if results.pose_landmarks else None

def get_all_landmarks_frame(frame):
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)
    return results.pose_landmarks.landmark if results.pose_landmarks else None
 
def parameterize(image):
    if (type(image) == str):
        landmarks = get_all_landmarks_path(image)
    else:
        landmarks = get_all_landmarks_frame(image)

    features = []

    for i in range(13):
        features.append(landmarks[i].x)
        features.append(landmarks[i].y)
    
    return features