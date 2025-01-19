# utils/rangefinder.py

from PIL import Image
import numpy as np
import cv2
from pathlib import Path

def calculate_distance():
    # Uzyskaj ścieżkę do bieżącego folderu
    current_folder = Path(__file__).parent

    # Załaduj dwa obrazy
    image1 = Image.open(current_folder / '..' / 'photos' / 'captured_frame_1.png')
    image2 = Image.open(current_folder / '..' / 'photos' / 'captured_frame_2.png')

    # Upewnij się, że oba obrazy mają ten sam rozmiar i tryb (RGB)
    image1 = image1.convert("RGB")
    image2 = image2.convert("RGB")

    # Konwertuj obrazy na tablice NumPy
    image1_array = np.array(image1, dtype=np.uint8)
    image2_array = np.array(image2, dtype=np.uint8)

    image1_array = image1_array[:, :, 0] # Tylko czerwony kolor
    image2_array = image2_array[:, :, 0] # Tylko czerwony kolor

    # Oblicz różnicę, unikając zawijania
    red_channel = image2_array.astype(np.int16) - image1_array.astype(np.int16)
    red_channel[red_channel < 0] = 0  # Ustaw wszystkie wartości ujemne na 0
    red_channel = red_channel.astype(np.uint8)  # Konwertuj z powrotem na uint8

    # Zastosuj filtr uśredniający 3x3 (średnia ruchoma) w celu wygładzenia wyniku
    # Kernel do uśredniania
    kernel = np.ones((6, 6), np.float32) / 9
    red_channel = cv2.filter2D(red_channel, -1, kernel)

    # Zainicjuj zmienne do przechowywania maksymalnej średniej intensywności i jej współrzędnych
    max_intensity = 0
    max_coordinates = (0, 0)

    # Iteruj przez kanał czerwony, przesuwając ramkę 9x9 po obrazie
    for i in range(red_channel.shape[0] - 8):  # Odejmij 8, aby dopasować ramkę 9x9
        for j in range(red_channel.shape[1] - 8):
            # Wyodrębnij bieżącą ramkę 9x9
            frame = red_channel[i:i+9, j:j+9]

            # Oblicz średnią intensywność bieżącej ramki
            mean_intensity = np.mean(frame)

            # Zaktualizuj max_intensity i max_coordinates, jeśli bieżąca średnia jest najwyższa dotychczas
            if mean_intensity > max_intensity:
                max_intensity = mean_intensity
                max_coordinates = (i + 5, j + 5)

    # Konwertuj wygładzony wynik z powrotem na obraz PIL
    result_image = Image.fromarray(red_channel)

    # Zapisz wynik jako obraz PNG
    result_image.save(current_folder / '..' / 'photos' / 'result_image_smoothed.png')
    print("Obraz wynikowy zapisany jako result_image_smoothed.png")
    print("Najwyższa średnia intensywność czerwieni:", max_intensity)
    print("Współrzędne ramki o najwyższej intensywności:", max_coordinates)

    distance = max_coordinates[1]
    distance = f"{(170.3363 * np.exp(-0.005 * distance)):.2f}"

    return distance