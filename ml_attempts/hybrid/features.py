import cv2
import mediapipe as mp
import numpy as np
import math

mp_pose = mp.solutions.pose

pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    enable_segmentation=False,
    min_detection_confidence=0,
    min_tracking_confidence=0
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


def angle(l1, l2):
    dx = l2.x - l1.x
    dy = l2.y - l1.y
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
    return angle_deg


def eval_horiz(angle):
    angle = abs(angle) % 180
    return min(angle, abs(180 - angle))


def eval_vert(angle):
    angle = abs(angle) % 180
    return abs(90 - angle)


def parameterize(image):
    # Path
    if isinstance(image, str):
        landmarks = get_all_landmarks_path(image)
    # Frame
    elif isinstance(image, np.ndarray):
        landmarks = get_all_landmarks_frame(image)
    # Unrecognized
    else:
        raise TypeError("Unrecognized image path")

    # Get relevant information
    left_shoulder = landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value]
    right_shoulder = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value]
    left_eye = landmarks[mp.solutions.pose.PoseLandmark.LEFT_EYE.value]
    right_eye = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_EYE.value]
    nose = landmarks[mp.solutions.pose.PoseLandmark.NOSE.value]

    # Min angle from x axis
    shoulder_angle = eval_horiz(angle(left_shoulder, right_shoulder))
    head_tilt_angle = eval_horiz(angle(left_eye, right_eye))

    # How far nose is from middle of shoulders (x direcction)
    shoulder_width = abs(right_shoulder.x - left_shoulder.x)
    shoulder_midpoint_x = (left_shoulder.x + right_shoulder.x) / 2
    nose_offset = abs(nose.x - shoulder_midpoint_x) / shoulder_width

    # Neck to nose
    shoulder_midpoint_y = (left_shoulder.y + right_shoulder.y) / 2
    dx_neck = nose.x - shoulder_midpoint_x
    dy_neck = nose.y - shoulder_midpoint_y
    neck_tilt_angle = eval_vert(math.degrees(math.atan2(dy_neck, dx_neck)))

    # Nose to center of eyes
    eyes_midpoint_x = (left_eye.x + right_eye.x) / 2
    eyes_midpoint_y = (left_eye.y + right_eye.y) / 2
    dx_nose_eye = eyes_midpoint_x - nose.x
    dy_nose_eye = eyes_midpoint_y - nose.y
    nose_eye_tilt = eval_vert(math.degrees(math.atan2(dy_nose_eye, dx_nose_eye)))
    

    # print(right_shoulder.x - left_shoulder.x, right_shoulder.y - left_shoulder.y)
    return [shoulder_angle, head_tilt_angle, neck_tilt_angle, nose_eye_tilt, nose_offset]
    """
    angles = []
    test = [left_shoulder, right_shoulder, left_eye, right_eye, nose]
    for i in range(len(test)):
        for j in range(i + 1, len(test)):
            angles.append(angle(test[i], test[j]))
    return angles"""