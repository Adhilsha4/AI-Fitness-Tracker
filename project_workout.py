import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
import os
import datetime

# Streamlit UI
st.set_page_config("AI Fitness App")
st.title("AI Workout Tracker with Pose Detection")
st.image("Pushup.jpg")
user_name = st.text_input("Enter your name")
exercise_options = ["squat", "pushup", "shoulderpress", "lunge"]
selected_exercise = st.selectbox("Choose your exercise", exercise_options)
start_button = st.button("Start Workout")

if start_button and user_name:
    st.success("Workout started! A camera window will open.")

    # Voice Engine
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)

    def speak(text):
        engine.say(text)
        engine.runAndWait()

    # MediaPipe setup
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_drawing = mp.solutions.drawing_utils

    rep_count = 0
    direction = None
    goal_reps = 10
    halfway_announcement_done = False
    completion_announcement_done = False

    def calculate_angle(a, b, c):
        a, b, c = np.array(a), np.array(b), np.array(c)
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        return 360 - angle if angle > 180 else angle

    def get_landmark(lm, index, w, h):
        return [int(lm[index].x * w), int(lm[index].y * h)]

    # Start video capture
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            feedback = ""
            angle = 0

            if selected_exercise in ["squat", "lunge"]:
                hip = get_landmark(lm, mp_pose.PoseLandmark.RIGHT_HIP.value, w, h)
                knee = get_landmark(lm, mp_pose.PoseLandmark.RIGHT_KNEE.value, w, h)
                ankle = get_landmark(lm, mp_pose.PoseLandmark.RIGHT_ANKLE.value, w, h)
                angle = calculate_angle(hip, knee, ankle)

                if angle > 160:
                    feedback = "Stand Straight" if selected_exercise == "squat" else "Step Forward"
                    if direction == "down":
                        rep_count += 1
                        speak(str(rep_count))
                        direction = "up"
                        if rep_count % 5 == 0: speak("Good job")
                        if rep_count == goal_reps // 2 and not halfway_announcement_done:
                            speak("Halfway there")
                            halfway_announcement_done = True
                        if rep_count == goal_reps and not completion_announcement_done:
                            speak("Workout complete")
                            completion_announcement_done = True
                elif angle < 90:
                    feedback = "Go Lower" if selected_exercise == "squat" else "Bend Forward More"
                    direction = "down"
                else:
                    feedback = "Good Form"
                cv2.putText(frame, f"Knee Angle: {int(angle)}", tuple(knee), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

            elif selected_exercise == "pushup":
                shoulder = get_landmark(lm, mp_pose.PoseLandmark.RIGHT_SHOULDER.value, w, h)
                elbow = get_landmark(lm, mp_pose.PoseLandmark.RIGHT_ELBOW.value, w, h)
                wrist = get_landmark(lm, mp_pose.PoseLandmark.RIGHT_WRIST.value, w, h)
                angle = calculate_angle(shoulder, elbow, wrist)

                if angle > 160:
                    feedback = "Up Position"
                    if direction == "down":
                        rep_count += 1
                        speak(str(rep_count))
                        direction = "up"
                        if rep_count % 5 == 0: speak("Good job")
                        if rep_count == goal_reps // 2 and not halfway_announcement_done:
                            speak("Halfway there")
                            halfway_announcement_done = True
                        if rep_count == goal_reps and not completion_announcement_done:
                            speak("Workout complete")
                            completion_announcement_done = True
                elif angle < 90:
                    feedback = "Down Position"
                    direction = "down"
                else:
                    feedback = "Keep Going"
                cv2.putText(frame, f"Elbow Angle: {int(angle)}", tuple(elbow), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

            elif selected_exercise == "shoulderpress":
                hip = get_landmark(lm, mp_pose.PoseLandmark.RIGHT_HIP.value, w, h)
                shoulder = get_landmark(lm, mp_pose.PoseLandmark.RIGHT_SHOULDER.value, w, h)
                elbow = get_landmark(lm, mp_pose.PoseLandmark.RIGHT_ELBOW.value, w, h)
                angle = calculate_angle(hip, shoulder, elbow)

                if angle > 120:
                    feedback = "Lower Arm"
                    if direction == "up":
                        rep_count += 1
                        speak(str(rep_count))
                        direction = "down"
                        if rep_count % 5 == 0: speak("Good job")
                        if rep_count == goal_reps // 2 and not halfway_announcement_done:
                            speak("Halfway there")
                            halfway_announcement_done = True
                        if rep_count == goal_reps and not completion_announcement_done:
                            speak("Workout complete")
                            completion_announcement_done = True
                elif angle < 60:
                    feedback = "Raise Arm Up"
                    direction = "up"
                else:
                    feedback = "Mid Press"
                cv2.putText(frame, f"Shoulder Angle: {int(angle)}", tuple(shoulder), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

            cv2.putText(frame, f"{selected_exercise.upper()} ➤ {feedback}", (30, 50), 
                        cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"REPS: {rep_count}", (30, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
        else:
            cv2.putText(frame, "No pose detected", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("AI Trainer with Voice Feedback", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    # Create logs directory if not exists
    os.makedirs("user_logs", exist_ok=True)

    # Save summary to a user-specific CSV file
    timestamp = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    user_file = f"user_logs/{user_name.lower().replace(' ', '_')}_log.csv"
    file_exists = os.path.isfile(user_file)

    with open(user_file, "a") as f:
        if not file_exists:
            f.write("Timestamp,Exercise,Reps\n")
        f.write(f"{timestamp},{selected_exercise},{rep_count}\n")

    # Display summary in Streamlit
    st.subheader("🏁 Workout Summary")
    st.success(f"Name: {user_name}")
    st.info(f"Exercise: {selected_exercise.capitalize()}")
    st.success(f"Total Reps: {rep_count}")
    st.write("📝 Your workout has been saved successfully.")

elif start_button:
    st.warning("Please enter your name to begin.")
