from flask import Flask, Response, render_template, request, jsonify
import cv2
import numpy as np
import face_recognition
import mysql.connector
from datetime import datetime
import threading
import time

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root@123",
        database="face_db",
        autocommit=True
    )

db_init = get_db()
cur_init = db_init.cursor()
cur_init.execute("SELECT name, image FROM faces")
rows = cur_init.fetchall()
cur_init.close()
db_init.close()

known_encodings = []
known_names = []

for name, blob in rows:
    img = cv2.imdecode(np.frombuffer(blob, np.uint8), cv2.IMREAD_COLOR)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    enc = face_recognition.face_encodings(rgb)
    if enc:
        known_encodings.append(enc[0])
        known_names.append(name)

print("Faces loaded:", known_names)

camera = None
current_frame = None
active = False
detected_today = set()

ALL_DAYS = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]


def camera_loop():
    global camera, current_frame, active

    while True:
        if not active or camera is None:
            time.sleep(0.1)
            continue

        ret, frame = camera.read()
        if not ret:
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        locations = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, locations)

        for (top, right, bottom, left), face_enc in zip(locations, encodings):
            matches = face_recognition.compare_faces(
                known_encodings, face_enc, tolerance=0.6
            )
            name = "Unknown"

            if True in matches:
                idx = matches.index(True)
                name = known_names[idx]

                if name not in detected_today:
                    day = datetime.now().strftime("%A")
                    db = get_db()
                    cur = db.cursor()
                    cur.execute(
                        "INSERT IGNORE INTO weekly_attendance (name, day) VALUES (%s,%s)",
                        (name, day)
                    )
                    cur.close()
                    db.close()
                    detected_today.add(name)

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        current_frame = frame

threading.Thread(target=camera_loop, daemon=True).start()


def gen_frames():
    global current_frame
    while True:
        if current_frame is not None:
            ret, buffer = cv2.imencode('.jpg', current_frame)
            if ret:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' +
                       buffer.tobytes() + b'\r\n')
        time.sleep(0.05)


@app.route('/')
def home():
    return render_template('index.html')  

@app.route('/video')
def video():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start', methods=['POST'])
def start():
    global active, camera, current_frame, detected_today
    detected_today.clear()
    if camera is None:
        camera = cv2.VideoCapture(0)
        time.sleep(0.5)
    active = True
    current_frame = None
    return jsonify(ok=True)

@app.route('/stop', methods=['POST'])
def stop():
    global active, camera, current_frame
    active = False
    current_frame = None
    if camera is not None:
        camera.release()
        camera = None
    return jsonify(ok=True)

@app.route('/week')
def week():
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT day, GROUP_CONCAT(name)
        FROM weekly_attendance
        GROUP BY day
    """)
    rows = cur.fetchall()
    cur.close()
    db.close()

    data = {day: [] for day in ALL_DAYS}
    for day, names in rows:
        if day in data and names:
            data[day] = names.split(',')

    return jsonify(data)

@app.route('/rate', methods=['POST'])
def rate():
    r = request.json['rating']
    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO feedback (rating) VALUES (%s)", (r,))
    cur.close()
    db.close()
    return jsonify(ok=True)

@app.route('/feedback_avg')
def feedback_avg():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT AVG(rating) FROM feedback")
    avg = cur.fetchone()[0]
    cur.close()
    db.close()

    if avg is None:
        avg = 0
    return jsonify(avg=round(float(avg), 2))


if __name__ == '__main__':
    print("Server running at http://localhost:5000")
    app.run(debug=False)