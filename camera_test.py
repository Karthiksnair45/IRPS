import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=1)
detector = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

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

while True:
    ret, frame = cap.read()
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
            
            gesture = get_gesture(hand)
            cv2.putText(frame, gesture, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 3)

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()