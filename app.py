
import cv2
from flask import Flask, Response, render_template, jsonify
from display_logic import PostureTracker
from stream import generate_frames

cap = cv2.VideoCapture(0)

app = Flask(__name__)
tracker = PostureTracker(cap)


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(cap), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/step', methods=['GET'])
def step():
    result = tracker.step()
    return jsonify(result)


@app.route('/graph')
def graph():
    img = tracker.plot_scores()
    if img is None:
        return "No data available", 404
    return Response(img, mimetype='image/png')


@app.route('/since_sleep')
def since_sleep():
    seconds = tracker.since_sleep()

    hours = seconds // 3600
    seconds -= hours * 3600

    minutes = seconds // 60
    seconds -= minutes * 60

    return jsonify({
        'hours': hours,
        'minutes': minutes,
        'seconds': round(seconds)
    })


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)