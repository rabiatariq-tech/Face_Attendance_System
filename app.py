from flask import Flask, render_template, Response, jsonify

import cv2
import face_recognition
import time

from face_utils import match_face
from attendance import mark_attendance

# =========================
# FLASK APP
# =========================

app = Flask(__name__)

# =========================
# OPEN WEBCAM
# =========================

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# =========================
# GLOBAL VARIABLES
# =========================

message = "Waiting for face..."
message_color = (255, 255, 255)

student_name = ""
student_roll = ""

# Real-time UI data
current_student = {
    "name": "Waiting...",
    "roll": "Waiting...",
    "status": "Waiting for face..."
}

# =========================
# PERFORMANCE CONTROL
# =========================

last_process_time = 0
process_interval = 3

# =========================
# SMART RECOGNITION
# =========================

recently_seen = {}

RECOGNITION_COOLDOWN = 8

unknown_counter = 0
UNKNOWN_THRESHOLD = 3

# =========================
# VIDEO GENERATOR
# =========================

def generate_frames():

    global message
    global message_color
    global student_name
    global student_roll
    global last_process_time
    global unknown_counter

    while True:

        success, frame = camera.read()

        if not success:
            break

        # =========================
        # CONVERT TO RGB
        # =========================

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # =========================
        # DETECT FACES
        # =========================

        locations = face_recognition.face_locations(rgb)

        current_time = time.time()

        # =========================
        # RUN RECOGNITION
        # =========================

        if len(locations) > 0 and (
            current_time - last_process_time > process_interval
        ):

            encodings = face_recognition.face_encodings(
                rgb,
                locations
            )

            # =========================
            # SINGLE FACE ONLY
            # =========================

            if len(encodings) == 1:

                encoding = encodings[0]

                name, roll_no, distance = match_face(
                    encoding
                )

                # =========================
                # STUDENT FOUND
                # =========================

                if name:

                    unknown_counter = 0

                    # Cooldown logic
                    if roll_no in recently_seen:

                        time_since_seen = (
                            current_time
                            - recently_seen[roll_no]
                        )

                        if (
                            time_since_seen
                            < RECOGNITION_COOLDOWN
                        ):
                            pass

                    recently_seen[roll_no] = current_time

                    # =========================
                    # MARK ATTENDANCE
                    # =========================

                    status = mark_attendance(
                        roll_no
                    )

                    if status == "marked":

                        message = "Attendance Marked"

                        message_color = (
                            0,
                            255,
                            0
                        )

                    else:

                        message = (
                            "Attendance Already Marked"
                        )

                        message_color = (
                            0,
                            255,
                            255
                        )

                    student_name = name
                    student_roll = roll_no

                    # =========================
                    # UPDATE UI DATA
                    # =========================

                    current_student["name"] = (
                        name
                    )

                    current_student["roll"] = (
                        roll_no
                    )

                    current_student["status"] = (
                        message
                    )

                # =========================
                # UNKNOWN PERSON
                # =========================

                else:

                    unknown_counter += 1

                    if (
                        unknown_counter
                        >= UNKNOWN_THRESHOLD
                    ):

                        message = (
                            "Not a Registered Student"
                        )

                        message_color = (
                            0,
                            0,
                            255
                        )

                        student_name = ""
                        student_roll = ""

                        current_student["name"] = (
                            "Unknown"
                        )

                        current_student["roll"] = (
                            "N/A"
                        )

                        current_student["status"] = (
                            message
                        )

                        unknown_counter = 0

            # =========================
            # MULTIPLE FACES
            # =========================

            elif len(encodings) > 1:

                message = "Multiple Faces Detected"

                message_color = (
                    0,
                    255,
                    255
                )

                current_student["name"] = (
                    "Multiple Faces"
                )

                current_student["roll"] = (
                    "N/A"
                )

                current_student["status"] = (
                    message
                )

            last_process_time = current_time

        # =========================
        # WAITING STATE
        # =========================

        if len(locations) == 0:

            current_student["name"] = (
                "Waiting..."
            )

            current_student["roll"] = (
                "Waiting..."
            )

            current_student["status"] = (
                "Waiting for face..."
            )

        # =========================
        # DRAW FACE BOXES
        # =========================

        for (
            top,
            right,
            bottom,
            left
        ) in locations:

            cv2.rectangle(
                frame,
                (left, top),
                (right, bottom),
                message_color,
                3
            )

        # =========================
        # CONVERT FRAME
        # =========================

        ret, buffer = cv2.imencode(
            '.jpg',
            frame
        )

        frame = buffer.tobytes()

        # =========================
        # STREAM FRAME
        # =========================

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'
            + frame +
            b'\r\n'
        )

# =========================
# ROUTES
# =========================

@app.route('/')
def index():

    return render_template(
        'index.html'
    )

@app.route('/video_feed')
def video_feed():

    return Response(
        generate_frames(),
        mimetype=(
            'multipart/x-mixed-replace; boundary=frame'
        )
    )

@app.route('/student_info')
def student_info():

    return jsonify(current_student)

# =========================
# RUN APP
# =========================

if __name__ == '__main__':

    print(
        "Flask server starting..."
    )

    app.run(debug=True, use_reloader=False)