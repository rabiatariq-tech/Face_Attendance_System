import face_recognition
from database import insert_student, find_student_by_roll

name = input("Enter name: ")
roll_no = input("Enter roll number: ")
image_path = input("Enter image path: ")

# check duplicate
if find_student_by_roll(roll_no):
    print("Student already exists!")
    exit()

image = face_recognition.load_image_file(image_path)
encodings = face_recognition.face_encodings(image)

if len(encodings) == 0:
    print("No face found!")
    exit()

if len(encodings) > 1:
    print("Multiple faces found!")
    exit()

encoding = encodings[0].tolist()

data = {
    "name": name,
    "roll_no": roll_no,
    "encoding": encoding,
    "last_attendance": None
}

insert_student(data)

print("Student added successfully!")