# utils/cam.py

import cv2


class Camera:
    def __init__(self):
        # Initialize the current frame to None
        self.current_frame = None

        # Open the camera using OpenCV (0 refers to the default camera)
        self.cap = cv2.VideoCapture(0)

    def start_opencv_window(self):
        # Continuously capture frames from the camera
        while True:
            # Read a frame from the camera
            ret, frame = self.cap.read()
            if not ret:
                # If frame capture fails, skip this iteration
                continue

            # Display the captured frame in an OpenCV window
            cv2.imshow("Camera", frame)

            # Update the current frame to the latest captured frame
            self.current_frame = frame

            # Exit the loop if the 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Release the camera and close OpenCV windows when done
        self.cap.release()
        cv2.destroyAllWindows()

    def get_current_frame(self):
        # Return the most recent captured frame
        return self.current_frame
