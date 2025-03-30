import time
import matplotlib.pyplot as plt
from posture_detection.calculate_posture import calculate_posture_values
from ui.connect import write_num, reconnect
from io import BytesIO

# Constants
DISPLAY_SLEEP = 1
DISPLAY_AWAKE = 2
DISPLAY_POSTURE = 3
DISPLAY_GRASS = 4
DISPLAY_DEAD = 5

CONSECUTIVE_BAD_POSTURE = 5
CONSECUTIVE_DEAD = 30
ALL_UNDER_CUTOFF = 71.25
AVERAGE_CUTOFF = 62.5
TOUCH_GRASS = 3600

class PostureTracker:
    def __init__(self, cap):
        self.cap = cap
        self.recent_scores = []
        self.time_at_last_away = time.time()
        self.latest_status = "sleep"
        self.starting_time = time.time()

    def step(self):
        try:
            ret, frame = self.cap.read()
            if not ret:
                return {"status": "camera_error", "score": None}

            current_time = time.time()
            time_elapsed = current_time - self.time_at_last_away
            posture_results = calculate_posture_values(frame)

            if posture_results is None:
                self.time_at_last_away = current_time
                write_num(DISPLAY_SLEEP)
                self.latest_status = "sleep"
                return {"status": "sleep", "score": None}

            if time_elapsed >= TOUCH_GRASS:
                write_num(DISPLAY_GRASS)
                self.latest_status = "grass"
                return {"status": "grass", "score": posture_results["score"]}

            self.recent_scores.append((current_time, posture_results["score"]))

            self.recent_scores = [
                (t, s) for t, s in self.recent_scores
                if t >= current_time - max(CONSECUTIVE_DEAD, CONSECUTIVE_BAD_POSTURE)
            ]

            dead_avg = self._average(current_time, CONSECUTIVE_DEAD)
            posture_avg = self._average(current_time, CONSECUTIVE_BAD_POSTURE)

            if time_elapsed >= CONSECUTIVE_DEAD and dead_avg <= ALL_UNDER_CUTOFF:
                write_num(DISPLAY_DEAD)
                self.latest_status = "dead"
            elif time_elapsed >= CONSECUTIVE_BAD_POSTURE and posture_avg <= ALL_UNDER_CUTOFF:
                write_num(DISPLAY_POSTURE)
                self.latest_status = "posture"
            else:
                write_num(DISPLAY_AWAKE)
                self.latest_status = "awake"

            return {"status": self.latest_status, "score": posture_results["score"]}

        except Exception as e:
            reconnect()
            self.time_at_last_away = time.time()
            return {"status": "error", "message": str(e)}

    def _average(self, current_time, window):
        scores = [s for t, s in self.recent_scores if current_time - t <= window]
        return sum(scores) / len(scores) if scores else 0
    
    def plot_scores(self):
        if not self.recent_scores:
            return None

        # Get values
        times, scores = zip(*self.recent_scores)
        times = [t - self.starting_time for t in times]

        # Plot
        plt.figure()
        plt.style.use('ggplot')
        plt.plot(times, scores, marker='o')

        plt.xlabel('Time (s)')
        plt.ylabel('Posture Score')

        plt.ylim(-3.3, 103.3)

        plt.title('Recent Posture Scores')

        # BytesIO buffer
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf.getvalue()

    def since_sleep(self):
        return time.time() - self.time_at_last_away