import cv2
import mediapipe as mp
import time
import pydirectinput  # Using pyDirectInput for keyboard input

# Define game control keys
BREAK_KEY = 'left'  # Key to apply brakes
GAS_KEY = 'right'   # Key to accelerate

time.sleep(2.0)
current_key = None  # Stores the currently pressed key

# Initialize MediaPipe utilities for drawing and hand tracking
mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands  # Hand tracking module

# List of finger tip IDs for gesture recognition
tipIds = [4, 8, 12, 16, 20]

# Start the webcam video capture
video = cv2.VideoCapture(0)

# Setup hand tracking with confidence level
with mp_hand.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8) as hands:
    while True:
        ret, image = video.read()  # Capture a frame
        if not ret:
            continue

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        lmList = []
        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                myHands = results.multi_hand_landmarks[0]
                for id, lm in enumerate(myHands.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                # Draw hand landmarks on screen
                mp_draw.draw_landmarks(image, hand_landmark, mp_hand.HAND_CONNECTIONS)

        fingers = [] # Stores the state of each finger (1 = extended, 0 = folded)
        if len(lmList) != 0:
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)  # Thumb extended
            else:
                fingers.append(0)  # Thumb folded

            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)   # Finger extended
                else:
                    fingers.append(0)   # Finger folded

            total = fingers.count(1)
            new_key = None  # Track which key should be pressed

            if total == 0:  # No fingers extended → Apply brakes
                cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, "BRAKE", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                new_key = BREAK_KEY

            elif total == 5:  # No fingers extended → Apply brakes
                cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, "GAS", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                new_key = GAS_KEY

            # If the new key is different from the currently pressed key, release the old key
            if new_key != current_key:
                if current_key is not None:
                    pydirectinput.keyUp(current_key)  # Release the old key
                if new_key is not None:
                    pydirectinput.keyDown(new_key)  # Press the new key
                current_key = new_key  # Update the current key

        cv2.imshow("Frame", image)

        # Press 'q' to exit the program
        k = cv2.waitKey(1)
        if k == ord('q'):
            break

# Cleanup
video.release()
cv2.destroyAllWindows()
