# utils/gui.py

import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import threading
import cv2
from utils.cam import Camera
from utils.rangefinder import calculate_distance
from pathlib import Path

# Uzyskaj ścieżkę do bieżącego folderu
current_folder = Path(__file__).parent


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.camera = Camera()
        self.label = Label(self)

        self.title("DALMIERZ")
        self.geometry("900x600")

        self.background_image = Image.open("laser2.jpg")
        self.background_image = self.background_image.resize(
            (900, 600), Image.Resampling.LANCZOS
        )
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

        self.title_label = Label(
            self, text="DALMIERZ", font=("Courier New", 14, "bold")
        )
        self.title_label.grid(row=0, column=1, pady=10)

        # okna
        self.window1 = Label(
            self,
            text="",
            bg="gray",
            relief="solid",
            bd=2,
            highlightbackground="white",
            width=12,
            height=6,
        )
        self.window1.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.window2 = Label(
            self,
            text="",
            bg="gray",
            relief="solid",
            bd=2,
            highlightbackground="white",
            width=12,
            height=6,
        )
        self.window2.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        self.window3 = Label(
            self,
            text="",
            bg="gray",
            relief="solid",
            bd=2,
            highlightbackground="white",
            width=12,
            height=6,
        )
        self.window3.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")

        # przyciski
        self.button1 = tk.Button(
            self,
            text="Zrób zdjęcie bez lasera",
            command=lambda: self.capture_and_display(1),
            relief="groove",
            bg="#4f4f4f",
            fg="white",
            width=10,
        )
        self.button1.grid(row=2, column=0, pady=20, padx=5, sticky="ew")

        self.button2 = tk.Button(
            self,
            text="Zrób zdjęcie z laserem",
            command=lambda: self.capture_and_display(2),
            relief="groove",
            bg="#4f4f4f",
            fg="white",
            width=10,
        )
        self.button2.grid(row=2, column=1, pady=20, padx=5, sticky="ew")

        self.button3 = tk.Button(
            self,
            text="Wylicz odleglość",
            command=self.calculate_and_display,
            relief="groove",
            bg="#4f4f4f",
            fg="white",
            width=10,
        )
        self.button3.grid(row=2, column=2, pady=20, padx=5, sticky="ew")

        self.distance_label = Label(
            self,
            text="Odległość [cm]:",
            font=("Courier New", 12, "bold"),
            bg="black",
            fg="white",
            padx=5,
        )
        self.distance_label.grid(row=3, column=1, pady=(5, 0), sticky="n")

        # pole wynikowe
        self.distance_value = Label(
            self, text="", relief="solid", bg="white", bd=2, highlightbackground="white"
        )
        self.distance_value.grid(
            row=4, column=1, pady=(0, 20), ipadx=70, ipady=5, sticky="n"
        )

        self.thread = threading.Thread(target=self.camera.start_opencv_window)
        self.thread.daemon = True
        self.thread.start()

    def update_frame(self):
        # Pobierz bieżącą klatkę z instancji Camera
        self.current_frame = self.camera.get_current_frame()

        # Zaktualizuj GUI Tkinter bieżącą klatką
        if self.current_frame is not None:
            # Konwertuj klatkę OpenCV na format, który może wyświetlić Tkinter
            image = Image.fromarray(cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB))
            photo = ImageTk.PhotoImage(image=image)

            # Zaktualizuj etykietę nowym obrazem
            self.label.config(image=photo)
            self.label.image = photo

    # Przechwyć bieżącą klatkę i wyświetl ją na etykiecie
    def capture_and_display(self, index):
        self.camera.save_frame(index)

        image_path = current_folder / ".." / "photos" / f"captured_frame_{index}.png"
        self.display_image(image_path, index)

    # Oblicz odległość, wyświetl wynik i obraz różnicowy
    def calculate_and_display(self):
        image_path1 = current_folder / ".." / "photos" / "captured_frame_1.png"
        image_path2 = current_folder / ".." / "photos" / "captured_frame_2.png"

        distance, max_coordinates, max_intensity = calculate_distance(image_path1, image_path2)
        self.distance_value.config(text=distance)

        image_path = current_folder / ".." / "photos" / "result_image.png"
        self.display_image(image_path, 3)

    # Wyświetl obraz na jednej z 3 etykiet
    def display_image(self, image_path, index):
        img = Image.open(image_path)
        img = img.resize((250, 250))
        img = ImageTk.PhotoImage(img)

        if index == 1:
            self.window1.config(image=img)
            self.window1.image = img
        if index == 2:
            self.window2.config(image=img)
            self.window2.image = img
        if index == 3:
            self.window3.config(image=img)
            self.window3.image = img
