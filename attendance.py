from datetime import datetime, timedelta
from database import find_student_by_roll, update_attendance

COOLDOWN_MINUTES = 2

def mark_attendance(roll_no):

    student = find_student_by_roll(roll_no)

    last_attendance = student.get("last_attendance")

    current_time = datetime.now()

    # If attendance already exists
    if last_attendance:

        # Convert string to datetime
        last_time = datetime.fromisoformat(last_attendance)

        # Check time difference
        if current_time - last_time < timedelta(minutes=COOLDOWN_MINUTES):
            return "already_marked"

    # Update attendance time
    update_attendance(roll_no, current_time.isoformat())

    return "marked"