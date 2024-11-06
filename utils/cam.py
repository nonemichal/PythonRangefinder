# utils/cam.py

import cv2


def open_cam():
    # Open the camera (0 is usually the default camera)
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None

    # Read a single frame from the camera
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        cap.release()
        return None

    # Release the camera after capturing the frame
    cap.release()
    return frame
