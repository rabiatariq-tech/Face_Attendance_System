import cv2
import face_recognition
import time

from face_utils import match_face
from attendance import mark_attendance

# =========================
# OPEN WEBCAM
# =========================

video = cv2.VideoCapture(0)

# =========================
# TIME CONTROL
# =========================

last_process_time = 0
process_interval = 3  # seconds

# =========================
# UI VARIABLES
# =========================

message = "Waiting for face..."
message_color = (255, 255, 255)

student_name = ""
student_roll = ""

display_until = 0

# =========================
# SMART SYSTEM VARIABLES
# =========================

# Prevent same person from being recognized repeatedly
recently_seen = {}

RECOGNITION_COOLDOWN = 8  # seconds

# Prevent false "Not a Student"
unknown_counter = 0
UNKNOWN_THRESHOLD = 3

# =========================
# MAIN LOOP
# =========================

while True:

    ret, frame = video.read()

    if not ret:
        break

    # Convert frame to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect face locations
    locations = face_recognition.face_locations(rgb)

    face_detected = len(locations) > 0

    current_time = time.time()

    # =========================
    # RUN RECOGNITION
    # =========================

    if face_detected and (current_time - last_process_time > process_interval):

        encodings = face_recognition.face_encodings(rgb)

        # =========================
        # NO FACE
        # =========================

        if len(encodings) == 0:

            message = "No Face Detected"
            message_color = (0, 0, 255)

            student_name = ""
            student_roll = ""

            display_until = time.time() + 2

        # =========================
        # MULTIPLE FACES
        # =========================

        elif len(encodings) > 1:

            message = "Multiple Faces Detected"
            message_color = (0, 255, 255)

            student_name = ""
            student_roll = ""

            display_until = time.time() + 2

        # =========================
        # SINGLE FACE
        # =========================

        else:

            encoding = encodings[0]

            name, roll_no, distance = match_face(encoding)

            # =========================
            # STUDENT FOUND
            # =========================

            if name:

                # Reset unknown counter
                unknown_counter = 0

                # Check if recently seen
                if roll_no in recently_seen:

                    time_since_seen = (
                        current_time - recently_seen[roll_no]
                    )

                    # Ignore repeated recognition
                    # Ignore repeated recognition
                    if time_since_seen < RECOGNITION_COOLDOWN:
                        last_process_time = current_time

                # Update recent recognition time
                recently_seen[roll_no] = current_time

                # Mark attendance
                status = mark_attendance(roll_no)

                # Attendance marked
                if status == "marked":

                    message = "Attendance Marked"
                    message_color = (0, 255, 0)

                # Already marked
                else:

                    message = "Attendance Already Marked"
                    message_color = (0, 255, 255)

                student_name = name
                student_roll = roll_no

                display_until = time.time() + 3

            # =========================
            # UNKNOWN PERSON
            # =========================

            else:

                unknown_counter += 1

                # Only show after multiple failures
                if unknown_counter >= UNKNOWN_THRESHOLD:

                    message = "Not a Registered Student"
                    message_color = (0, 0, 255)

                    student_name = ""
                    student_roll = ""

                    display_until = time.time() + 3

                    unknown_counter = 0

        # Update processing time
        last_process_time = current_time

    # =========================
    # RESET UI
    # =========================

    if time.time() > display_until:

        message = "Waiting for face..."
        message_color = (255, 255, 255)

        student_name = ""
        student_roll = ""

    # =========================
    # DRAW FACE BOXES
    # =========================

    for (top, right, bottom, left) in locations:

        cv2.rectangle(
            frame,
            (left, top),
            (right, bottom),
            message_color,
            3
        )

    # =========================
    # TOP UI PANEL
    # =========================

    cv2.rectangle(frame, (0, 0), (640, 130), (30, 30, 30), -1)

    # Title
    cv2.putText(
        frame,
        "Face Attendance System",
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    # Main message
    cv2.putText(
        frame,
        message,
        (20, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        message_color,
        2
    )

    # Student name
    cv2.putText(
        frame,
        f"Name: {student_name}",
        (20, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (220, 220, 220),
        1
    )

    # Roll number
    cv2.putText(
        frame,
        f"Roll No: {student_roll}",
        (320, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (220, 220, 220),
        1
    )

    # Exit instruction
    cv2.putText(
        frame,
        "Press Q or ESC to Exit",
        (360, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (180, 180, 180),
        1
    )

    # =========================
    # SHOW WINDOW
    # =========================

    cv2.imshow("Face Attendance System", frame)

    # =========================
    # EXIT CONTROLS
    # =========================

    key = cv2.waitKey(1)

    if key == ord('q') or key == 27:
        break

# =========================
# CLEANUP
# =========================

video.release()
cv2.destroyAllWindows()