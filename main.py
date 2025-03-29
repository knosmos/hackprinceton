import time
import cv2
from ui.connect import write_num, reconnect
from posture_detection.calculate_posture import calculate_posture_values

# Display constants
DISPLAY_SLEEP = 1
DISPLAY_AWAKE = 2
DISPLAY_POSTURE = 3
DISPLAY_GRASS = 4
DISPLAY_DEAD = 5

# Time stuff in seconds
CONSECUTIVE_BAD_POSTURE = 5
CONSECUTIVE_DEAD = 30
ALL_UNDER_CUTOFF = 71.25
AVERAGE_CUTOFF = 62.5
TOUCH_GRASS = 60

def main():
    time_at_last_away = time.time()
    cap = cv2.VideoCapture(0)

    recent_scores = []

    while True:
        try:
            time.sleep(0.4)
            # Read in screenshot from camera
            ret, frame = cap.read()

            if not ret:
                continue
            
            # Calculate information
            current_time = time.time()
            time_elapsed = current_time - time_at_last_away
            posture_results = calculate_posture_values(frame)

            # You are away
            if posture_results is None:
                time_at_last_away = time.time()
                write_num(DISPLAY_SLEEP)
                continue
            
            # Otherwise, force touch grass (override everything else)
            if time_elapsed >= TOUCH_GRASS:
                write_num(DISPLAY_GRASS)
                continue
                
            # Update recent scores
            recent_scores.append((current_time, posture_results["score"]))
            
            while recent_scores[0][0] < current_time - max(CONSECUTIVE_DEAD, CONSECUTIVE_BAD_POSTURE):
                recent_scores.pop(0)
            
            # If we just started, don't do anything
            if current_time < max(CONSECUTIVE_DEAD, CONSECUTIVE_BAD_POSTURE):
                write_num(DISPLAY_SLEEP)
                continue

            # Calculate necessary sliding window posture information
            dead_avg = 0
            dead_cnt = 0
            posture_avg = 0
            posture_cnt = 0

            for t, val in recent_scores:
                if current_time - t <= CONSECUTIVE_DEAD:
                    dead_avg += val
                    dead_cnt += 1
                if current_time - t <= CONSECUTIVE_BAD_POSTURE:
                    posture_avg += val
                    posture_cnt += 1

            dead_avg /= dead_cnt
            posture_avg /= posture_cnt

            print(f"posture_avg: {posture_avg}, dead_avg: {dead_avg}")

            # Dead
            if time_elapsed >= CONSECUTIVE_DEAD and dead_avg <= ALL_UNDER_CUTOFF:
                write_num(DISPLAY_DEAD)
                continue

            # Bad posture
            if time_elapsed >= CONSECUTIVE_BAD_POSTURE and posture_avg <= ALL_UNDER_CUTOFF:
                write_num(DISPLAY_POSTURE)
                continue
            
            # Otherwise, awake
            write_num(DISPLAY_AWAKE)

        except:
            reconnect()
            print("reconnecting...")
            time_at_last_away = time.time()


if __name__ == "__main__":
    main()