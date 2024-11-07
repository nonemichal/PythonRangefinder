# utils/gui.py

import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import threading
import cv2
from utils.cam import Camera


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set up the GUI window title
        self.title("RangeFinder")

        # Label to display the current image frame
        self.label = Label(self)
        self.label.pack()

        # Button that updates the displayed frame when clicked
        self.update_button = tk.Button(
            self, text="Update Frame", command=self.update_frame
        )
        self.update_button.pack()

        # Button to save the current frame to a file
        self.save_button = tk.Button(self, text="Save Frame", command=self.save_frame)
        self.save_button.pack()

        # Create an instance of the Camera class
        self.camera = Camera()

        # Start a background thread to continuously capture frames from the camera
        self.thread = threading.Thread(target=self.camera.start_opencv_window)
        self.thread.daemon = True  # Ensure thread exits when the main program exits
        self.thread.start()

    def update_frame(self):
        # Get the current frame from the Camera instance
        self.current_frame = self.camera.get_current_frame()

        # Update the Tkinter GUI with the current frame
        if self.current_frame is not None:
            # Convert the OpenCV frame to a format Tkinter can display
            image = Image.fromarray(cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB))
            photo = ImageTk.PhotoImage(image=image)

            # Update the label with the new image
            self.label.config(image=photo)  # type: ignore
            self.label.image = photo  # type: ignore

    def save_frame(self):
        # Save the current frame to a PNG file
        if self.current_frame is not None:
            # Save the image as "captured_frame.png" in the current directory
            cv2.imwrite("captured_frame.png", self.current_frame)
            print("Frame saved as 'captured_frame.png'")
        else:
            print("No frame available to save.")
