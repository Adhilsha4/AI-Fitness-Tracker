# 🏋️‍♀️ AI Workout Tracker with Pose Detection

An AI-powered fitness app built using **Python**, **OpenCV**, **MediaPipe**, **Streamlit**, and **Text-to-Speech** that counts your workout repetitions using real-time pose detection and provides **voice feedback**. It supports multiple exercises and stores a personalized workout log for each user.

---

## 🚀 Features

- 👤 **User Input**: Name entry and exercise selection from dropdown.
- 📸 **Pose Detection**: Real-time camera tracking using MediaPipe.
- 🎯 **Repetition Counter**: Counts reps based on body joint angles.
- 🔈 **Voice Feedback**: Announces rep count, motivation, and completion status.
- 💾 **Workout Logging**: Saves user-specific workout logs to a CSV file.
- 📊 **Workout Summary**: Displays total reps after session ends.
- 🧠 **Multiple Exercises**: Supports:
  - Squats
  - Pushups
  - Lunges
  - Shoulder Press

---

## 🧰 Tech Stack

- **Python**
- **Streamlit** – For interactive web UI
- **OpenCV** – For webcam frame capture and display
- **MediaPipe** – For pose estimation
- **NumPy** – For vector and angle calculations
- **pyttsx3** – For offline text-to-speech
- **OS & DateTime** – For logging and timestamping sessions

---

## 📸 How It Works

1. User inputs their name and selects an exercise.
2. On clicking **Start Workout**, webcam opens and tracks the user’s body.
3. The app calculates joint angles to detect movement patterns.
4. Voice feedback gives:
   - Rep count
   - “Good job” messages
   - “Halfway there” cue
   - “Workout complete” when done
5. Reps are saved in a per-user CSV log with timestamp.
6. A summary is shown in Streamlit after the session.

---

## 🧪 Setup Instructions

### ✅ Prerequisites

Install the required Python libraries:

```bash
pip install streamlit opencv-python mediapipe numpy pyttsx3
```

### ▶️ Run the App
```bash
streamlit run project_workout.py
```

### 🗃️ Project Structure
```bash
AI-Workout-Tracker/
│
├── Pushup.jpg                     # Header image for UI
├── your_app_filename.py          # Main application file
└── user_logs/                    # Folder containing user CSV workout logs
    └── john_doe_log.csv          # Example log file
```


