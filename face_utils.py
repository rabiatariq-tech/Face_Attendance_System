import face_recognition
import numpy as np
from config import THRESHOLD
from database import get_all_students

def encode_image(image):
    encodings = face_recognition.face_encodings(image)
    if len(encodings) == 0:
        return None
    return encodings[0]

def match_face(encoding):
    students = get_all_students()

    if len(students) == 0:
        return None, None, None

    known_encodings = []
    student_info = []

    for student in students:
        known_encodings.append(np.array(student["encoding"]))
        student_info.append(student)

    distances = face_recognition.face_distance(known_encodings, encoding)

    best_index = np.argmin(distances)
    best_distance = distances[best_index]

    if best_distance < THRESHOLD:
        student = student_info[best_index]
        return student["name"], student["roll_no"], best_distance

    return None, None, best_distance