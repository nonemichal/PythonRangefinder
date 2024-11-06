# utils/gui.py

import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import threading
import cv2


class CameraGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set up the GUI window title
        self.title("Camera Frame Display")

        # Label to display the current image frame
        self.label = Label(self)
        self.label.pack()

        # Button that updates the displayed frame when clicked
        self.update_button = tk.Button(
            self, text="Update Frame", command=self.update_frame
        )
        self.update_button.pack()

        # Variable to hold the current frame from OpenCV
        self.current_frame = None

        # Start a background thread to continuously capture and display the OpenCV window
        self.thread = threading.Thread(target=self.show_opencv_window)
        self.thread.daemon = True  # Ensure thread exits when the main program exits
        self.thread.start()

    def show_opencv_window(self):
        # Open the camera using OpenCV
        cap = cv2.VideoCapture(0)
        while True:
            # Capture a frame from the camera
            ret, frame = cap.read()
            if not ret:
                continue

            # Display the captured frame using OpenCV
            cv2.imshow("Camera", frame)

            # Update the current frame to be used by Tkinter
            self.current_frame = frame

            # Break the loop if 'q' key is pressed in the OpenCV window
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Release the camera and close OpenCV windows
        cap.release()
        cv2.destroyAllWindows()

    def update_frame(self):
        # Update the Tkinter GUI with the current frame
        if self.current_frame is not None:
            # Convert the OpenCV frame to a format Tkinter can display
            image = Image.fromarray(cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB))
            photo: ImageTk.PhotoImage = ImageTk.PhotoImage(
                image=image
            )  # Type annotation for the photo

            # Update the label with the new image
            self.label.config(image=photo) # type: ignore
            self.label.image = photo # type: ignore
