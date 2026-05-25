import tkinter as tk
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import random
from PIL import Image, ImageTk

# --- Setup MediaPipe ---
base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=1)
detector = vision.HandLandmarker.create_from_options(options)

# --- Setup Camera ---
cap = cv2.VideoCapture(0)

# --- Game State ---
player_score = 0
cpu_score = 0
countdown = None
current_gesture = "unknown"

def get_gesture(hand):
    tips = [8, 12, 16, 20]
    knuckles = [6, 10, 14, 18]
    fingers_up = []
    for tip, knuckle in zip(tips, knuckles):
        if hand[tip].y < hand[knuckle].y:
            fingers_up.append(1)
        else:
            fingers_up.append(0)
    if fingers_up == [0, 0, 0, 0]:
        return "rock"
    elif fingers_up == [1, 1, 1, 1]:
        return "paper"
    elif fingers_up == [1, 1, 0, 0]:
        return "scissor"
    else:
        return "unknown"

def determine_result(player, cpu):
    if player == cpu:
        return "DRAW"
    elif (player == "rock" and cpu == "scissor") or \
         (player == "paper" and cpu == "rock") or \
         (player == "scissor" and cpu == "paper"):
        return "YOU WIN!"
    else:
        return "YOU LOSE!"

def play_round():
    global player_score, cpu_score
    play_btn.config(state="disabled")
    run_countdown(3)

def run_countdown(count):
    if count > 0:
        countdown_label.config(text=str(count))
        root.after(1000, lambda: run_countdown(count - 1))
    else:
        countdown_label.config(text="GO!")
        root.after(500, reveal_result)

def reveal_result():
    global player_score, cpu_score
    countdown_label.config(text="")
    print("Gesture at reveal:", current_gesture)
    
    player = current_gesture
    cpu = random.choice(['rock', 'paper', 'scissor'])
    result = determine_result(player, cpu)

    if result == "YOU WIN!":
        player_score += 1
        result_label.config(fg="#00ff88")
    elif result == "YOU LOSE!":
        cpu_score += 1
        result_label.config(fg="#ff4444")
    else:
        result_label.config(fg="#ffff00")

    your_label.config(text=f"You:  {player}")
    cpu_label.config(text=f"CPU:  {cpu}")
    result_label.config(text=result)
    score_label.config(text=f"Score  {player_score} - {cpu_score}")
    play_btn.config(state="normal")

def update_camera():
    global current_gesture
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = detector.detect(mp_image)

    if result.hand_landmarks:
        for hand in result.hand_landmarks:
            for landmark in hand:
                x = int(landmark.x * w)
                y = int(landmark.y * h)
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
            current_gesture = get_gesture(hand)
            cv2.putText(frame, current_gesture, (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 136), 2)
    else:
        current_gesture = "unknown"

    display = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(display)
    img = img.resize((500, 400))
    imgtk = ImageTk.PhotoImage(image=img)
    camera_label.imgtk = imgtk
    camera_label.configure(image=imgtk)
    root.after(10, update_camera)

# --- Window Setup ---
root = tk.Tk()
root.title("IRPS - Interactive Rock Paper Scissors")
root.configure(bg="#0a0a0a")
root.geometry("900x600")
root.resizable(False, False)

# --- Title ---
title = tk.Label(root, text="IRPS", font=("Courier New", 28, "bold"), 
                 bg="#0a0a0a", fg="#00ff88")
title.pack(pady=10)

# --- Main Frame ---
main_frame = tk.Frame(root, bg="#0a0a0a")
main_frame.pack(fill="both", expand=True, padx=10, pady=5)

# --- Left Panel (Camera) ---
left_panel = tk.Frame(main_frame, bg="#0a0a0a")
left_panel.pack(side="left", padx=10)

camera_label = tk.Label(left_panel, bg="#0a0a0a")
camera_label.pack()

countdown_label = tk.Label(left_panel, text="", font=("Courier New", 60, "bold"),
                           bg="#0a0a0a", fg="#ff4444")
countdown_label.pack()

# --- Right Panel (Game Info) ---
right_panel = tk.Frame(main_frame, bg="#111111", bd=2, relief="groove")
right_panel.pack(side="right", padx=10, fill="both", expand=True)

your_label = tk.Label(right_panel, text="You: -", font=("Courier New", 18),
                      bg="#111111", fg="#ffffff")
your_label.pack(pady=10)

cpu_label = tk.Label(right_panel, text="CPU: -", font=("Courier New", 18),
                     bg="#111111", fg="#ffffff")
cpu_label.pack(pady=10)

result_label = tk.Label(right_panel, text="", font=("Courier New", 22, "bold"),
                        bg="#111111", fg="#00ff88")
result_label.pack(pady=10)

score_label = tk.Label(right_panel, text="Score  0 - 0", font=("Courier New", 16),
                       bg="#111111", fg="#aaaaaa")
score_label.pack(pady=10)

play_btn = tk.Button(right_panel, text="PLAY", font=("Courier New", 16, "bold"),
                     bg="#00ff88", fg="#0a0a0a", padx=20, pady=10,
                     relief="flat", cursor="hand2", command=play_round)
play_btn.pack(pady=20)

update_camera()
root.mainloop()

options_list = ['rock', 'paper', 'scissor']