# 🎓 AI-Based Real-Time Face Attendance System

## 📌 Project Overview

This project is an AI-powered real-time face attendance system developed using Python, OpenCV, Flask, MongoDB, and the `face_recognition` library.

The system captures live webcam video, detects and recognizes student faces, and automatically marks attendance in real time.

The project was designed as a standalone portfolio project to demonstrate skills in:

- Computer Vision
- Face Recognition
- Real-Time Systems
- Flask Backend Development
- MongoDB Integration
- Frontend UI Development

---

# 🚀 Features

✅ Real-Time Face Recognition  
✅ Live Webcam Attendance System  
✅ MongoDB Database Integration  
✅ One-Shot Learning Approach  
✅ Duplicate Attendance Prevention  
✅ Unknown Person Detection  
✅ Professional Web-Based UI  
✅ Student Information Panel  
✅ Flask Backend Server  
✅ OpenCV Face Detection  
✅ Face Encoding Matching  

---

# 🧠 System Workflow

```text
Student shows face to webcam
            ↓
OpenCV captures frame
            ↓
face_recognition detects face
            ↓
Face encoding generated
            ↓
Encoding compared with MongoDB encodings
            ↓
Student identified
            ↓
Attendance marked
            ↓
UI updated in real time
```

---

# 🏗️ Project Structure

```text
face-attendance-system/
│
├── app.py
├── add_student.py
├── face_utils.py
├── database.py
├── attendance.py
├── requirements.txt
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
└── README.md
```

---

# ⚙️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core Programming |
| OpenCV | Webcam & Image Processing |
| face_recognition | Face Recognition |
| dlib | Facial Feature Extraction |
| Flask | Backend Web Server |
| MongoDB Atlas | Cloud Database |
| HTML/CSS/JS | Frontend UI |

---

# 🧠 Why face_recognition + dlib?

The `face_recognition` library internally uses `dlib`.

### dlib provides:
- Face landmark detection
- Deep learning face embeddings
- 128-dimensional face encodings

### face_recognition provides:
- Easy-to-use wrapper around dlib
- Simple APIs for detection and matching

This combination was selected because:
- Lightweight
- Fast on CPU
- Beginner-friendly
- Excellent for real-time attendance systems

---

# 🎯 One-Shot Learning Concept

The system follows a one-shot learning approach.

This means:
- Only one image per student is required
- The system generates a unique face encoding
- Future recognition is based on encoding similarity

---

# 🧮 Face Recognition Logic

1. Detect face from webcam frame
2. Convert BGR image → RGB
3. Generate face encoding
4. Fetch stored encodings from MongoDB
5. Compute Euclidean distance
6. Find best match
7. If distance < threshold:
   - Student recognized
8. Else:
   - Unknown person

---

# ⚡ Performance Optimization

To reduce CPU usage:

```python
if face_detected:
    if time_passed:
        run_recognition()
```

### Optimizations Used:
- Recognition every few seconds
- Cooldown system
- Unknown face threshold
- Single-face validation

---

# 🎨 UI Features

✅ Modern Dashboard  
✅ Webcam Feed  
✅ Student Information Panel  
✅ Attendance Status Display  
✅ Responsive Layout  

---

# 📦 Attendance Responses

## Attendance Marked

```json
{
  "name": "Rabia Tariq",
  "roll_no": "CS-101",
  "status": "Attendance Marked"
}
```

## Already Marked

```json
{
  "name": "Rabia Tariq",
  "roll_no": "CS-101",
  "status": "Attendance Already Marked"
}
```

## Unknown Person

```json
{
  "status": "Not a Registered Student"
}
```

---

# ▶️ How To Run

## 1. Install dependencies

```bash
pip install -r requirements.txt
```

## 2. Start the project

```bash
python app.py
```

## 3. Open browser

```text
http://127.0.0.1:5000
```

---

# 🔥 Future Improvements

- Admin dashboard
- Attendance history
- CSV export
- Email notifications
- Anti-spoofing detection
- Multi-camera support
- React frontend
- Cloud deployment

---


