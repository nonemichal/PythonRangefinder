import cv2

def open_cam():
    # Open the camera (0 is usually the default camera)
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Capture video in a loop
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        # Check if frame was read correctly
        if not ret:
            print("Error: Could not read frame.")
            break

        # Display the frame in a window
        cv2.imshow('Camera', frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()