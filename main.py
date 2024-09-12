import cv2
import mediapipe as mp
import pyautogui

# Initialize webcam
cap = cv2.VideoCapture(0)

# Initialize MediaPipe hand detector and drawing utilities
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

# Get screen dimensions
screen_width, screen_height = pyautogui.size()

# Variables to store coordinates
index_y = 0
thumb_y = 0
middle_y = 0
scroll_started = False

while True:
    # Read frame from webcam
    _, frame = cap.read()
    frame_height, frame_width, _ = frame.shape

    # Convert frame to RGB for MediaPipe processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    # If hands are detected
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark

            # Initialize variables for landmark positions
            index_x = index_y = 0
            thumb_x = thumb_y = 0
            middle_x = middle_y = 0

            # Iterate through landmarks to find specific points
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                # Index finger tip
                if id == 8:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255), thickness=-1)
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y
                    pyautogui.moveTo(index_x, index_y)

                # Thumb tip
                if id == 4:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 0), thickness=-1)
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y

                # Middle finger tip
                if id == 12:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 0, 255), thickness=-1)
                    middle_x = screen_width / frame_width * x
                    middle_y = screen_height / frame_height * y

            # Click action if thumb and index finger tips are close
            if abs(index_y - thumb_y) < 20:
                pyautogui.click()
                pyautogui.sleep(1)

            # Scroll when index finger and middle finger are joined
            if abs(index_x - middle_x) < 20 and abs(index_y - middle_y) < 20:
                scroll_started = True
                # Scroll up if the joined fingers move upwards
                if index_y < frame_height / 2:
                    pyautogui.scroll(110)  # Scroll up
                # Scroll down if the joined fingers move downwards
                elif index_y > frame_height / 2:
                    pyautogui.scroll(-110)  # Scroll down
            else:
                scroll_started = False

    # Display the frame
    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)

# Release resources
cap.release()
cv2.destroyAllWindows()
