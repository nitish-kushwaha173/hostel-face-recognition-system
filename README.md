# Hostel Mess Face Detector

## 📌 Project Overview

Hostel Mess Face Detector is an AI-based face recognition system designed for hostel mess attendance management. The system detects and recognizes hostel students using computer vision technology. When a registered student is identified, their name, date, and time are automatically stored as a daily entry.

---

## 🚀 Features

* Real-time face detection
* Face recognition for registered hostel students
* Automatic daily attendance entry
* Unknown face detection
* Prevents duplicate entries for the same day
* Stores date and time of entry
* Simple and user-friendly system

---

## 🛠️ Technologies Used

* Python
* OpenCV
* face_recognition Library
* NumPy
* Flask (Optional for Web Dashboard)
* MySQL / MongoDB

---

## 📂 Project Structure

```bash
Hostel-Mess-Face-Detector/
│── dataset/
│── images/
│── attendance/
│── main.py
│── app.py
│── requirements.txt
│── README.md
```

---

## ⚙️ Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/hostel-mess-face-detector.git
cd hostel-mess-face-detector
```

### Install Dependencies

```bash
pip install opencv-python
pip install face-recognition
pip install numpy
```

---

## ▶️ Run the Project

```bash
python main.py
```

If using Flask:

```bash
python app.py
```

---

## 🧠 Working Process

1. The camera captures faces in real time.
2. The system detects the face using OpenCV.
3. The detected face is compared with stored student data.
4. If the student is recognized:

   * Their name is identified.
   * Attendance with date and time is stored.
5. Unknown faces are ignored or marked.

---

## 📌 Example Entry

```text
Name: Nitish Kumar
Date: 2026-05-30
Time: 08:15 AM
```

---

## 🔥 Future Improvements

* Admin dashboard
* Email/SMS alerts
* Cloud database support
* Live monitoring system
* Mobile app integration

---

## 👨‍💻 Author

Nitish Kumar

---

## 📜 License

This project is for educational purposes.
