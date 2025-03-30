
import cv2
from flask import Flask, Response, render_template, jsonify, send_file
from display_logic import PostureTracker
from stream import generate_frames
import os

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
    image_path = tracker.plot_scores()
    if image_path is None:
        return "No data available", 404
    return send_file(image_path, mimetype='image/png')


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
    # Remove all saved images
    for file_name in os.listdir("static"):
        file_path = os.path.join("static", file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
    
    app.run(debug=True, use_reloader=False)