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

        self.title("DALMIERZ")
        self.geometry("800x600")

        self.background_image = Image.open("laser2.jpg")
        self.background_image = self.background_image.resize((800, 600), Image.Resampling.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Ustawienie tła
        self.background_label = Label(self, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

        # Ustawienia siatki
        self.grid_columnconfigure(0, weight=1, minsize=120)
        self.grid_columnconfigure(1, weight=1, minsize=120)
        self.grid_columnconfigure(2, weight=1, minsize=120)
        self.grid_rowconfigure(1, weight=1, minsize=150)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=0)

        self.title_label = Label(self, text="DALMIERZ", font=("Courier New", 14, "bold"))
        self.title_label.grid(row=0, column=1, pady=10)

        #okna
        self.window1 = Label(self, text="", bg="gray", relief="solid", bd=2, highlightbackground="white",
                             width=12, height=6)
        self.window1.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.window2 = Label(self, text="", bg="gray", relief="solid", bd=2, highlightbackground="white",
                             width=12, height=6)
        self.window2.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        self.window3 = Label(self, text="", bg="gray", relief="solid", bd=2, highlightbackground="white",
                             width=12, height=6)
        self.window3.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")

        #przyciski
        self.button1 = tk.Button(self, text="", command=self.update_frame, relief="groove", bg="black",
                                 width=10)
        self.button1.grid(row=2, column=0, pady=20, padx=5, sticky="ew")

        self.button2 = tk.Button(self, text="", command=self.update_frame, relief="groove", bg="black",
                                 width=10)
        self.button2.grid(row=2, column=1, pady=20, padx=5, sticky="ew")

        self.button3 = tk.Button(self, text="", command=self.update_frame, relief="groove", bg="black",
                                 width=10)
        self.button3.grid(row=2, column=2, pady=20, padx=5, sticky="ew")


        self.distance_label = Label(self, text="Odległość [m]:", font=("Courier New", 12, "bold"), bg= "black", fg="white", padx=5)
        self.distance_label.grid(row=3, column=1, pady=(5, 0), sticky="n")

        #pole wynikowe
        self.distance_value = Label(self, text="", relief="solid", bg="white", bd=2, highlightbackground="white")
        self.distance_value.grid(row=4, column=1, pady=(0, 20), ipadx=70, ipady=5, sticky="n")

        self.label = Label(self)
        self.camera = Camera()
        self.thread = threading.Thread(target=self.camera.start_opencv_window)
        self.thread.daemon = True
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
