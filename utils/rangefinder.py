# utils/rangefinder.py

from PIL import Image
import numpy as np
import cv2
from pathlib import Path
import os
import time

current_folder = Path(__file__).parent


def find_max_coordinates_convolution(image1_array, image2_array):
    # Użyj tylko czerwonego kanału
    image1_array = image1_array[:, :, 0]
    image2_array = image2_array[:, :, 0]

    # Oblicz różnicę, unikając zawijania
    red_channel = image2_array.astype(np.int16) - image1_array.astype(np.int16)
    red_channel[red_channel < 0] = 0  # Ustaw wszystkie wartości ujemne na 0
    red_channel = red_channel.astype(np.uint8)  # Konwertuj z powrotem na uint8

    # Zastosuj filtr uśredniający 3x3 (średnia ruchoma) w celu wygładzenia wyniku
    kernel = np.ones((6, 6), np.float32) / 9
    red_channel = cv2.filter2D(red_channel, -1, kernel)

    # Zainicjuj zmienne do przechowywania maksymalnej średniej intensywności i jej współrzędnych
    max_intensity = 0
    max_coordinates = (0, 0)

    # Iteruj przez kanał czerwony, przesuwając ramkę 9x9 po obrazie
    for i in range(red_channel.shape[0] - 8):  # Odejmij 8, aby dopasować ramkę 9x9
        for j in range(red_channel.shape[1] - 8):
            # Wyodrębnij bieżącą ramkę 9x9
            frame = red_channel[i : i + 9, j : j + 9]

            # Oblicz średnią intensywność bieżącej ramki
            mean_intensity = np.mean(frame)

            # Zaktualizuj max_intensity i max_coordinates, jeśli bieżąca średnia jest najwyższa dotychczas
            if mean_intensity > max_intensity:
                max_intensity = mean_intensity
                max_coordinates = (i + 5, j + 5)

    return max_coordinates, max_intensity, red_channel


def find_max_coordinates_sum(image1_array, image2_array):
    # Wytnij fragment o rozmiarach 190:250 dla x i wszystkie y (użyj tylko czerwonego kanału)
    image1_array_section = image1_array[190:250, :, 0]
    image2_array_section = image2_array[190:250, :, 0]

    # Oblicz różnicę, unikając zawijania
    red_channel = image2_array_section.astype(np.int16) - image1_array_section.astype(
        np.int16
    )
    red_channel[red_channel < 0] = 0  # Ustaw wszystkie wartości ujemne na 0
    red_channel = red_channel.astype(np.uint8)  # Konwertuj z powrotem na uint8

    # Stwórz zmienną red_sum, która będzie 1-wymiarową tablicą zsumowanych rzędów
    red_sum = np.sum(red_channel, axis=0)

    # Znajdź indeks(y) maksymalnej wartości
    max_indices = np.where(red_sum == np.max(red_sum))[0]

    # Jeśli jest więcej niż jedna maksymalna wartość, znajdź indeks uśredniony
    if len(max_indices) > 1:
        max_index = int(np.mean(max_indices))
    else:
        max_index = max_indices[0]

    # Stwórz nową tablicę o rozmiarze image1_array i wypełnij ją czarnym kolorem
    full_red_channel = np.zeros_like(image1_array[:, :, 0], dtype=np.uint8)

    # Wstaw wartości z red_channel do odpowiedniego paska
    full_red_channel[190:250, :] = red_channel

    return max_index, np.max(red_sum), full_red_channel


def calculate_distance(path1, path2, method="sum"):
    # Załaduj dwa obrazy
    image1 = Image.open(path1)
    image2 = Image.open(path2)

    # Upewnij się, że oba obrazy mają ten sam rozmiar i tryb (RGB)
    image1 = image1.convert("RGB")
    image2 = image2.convert("RGB")

    # Konwertuj obrazy na tablice NumPy
    image1_array = np.array(image1, dtype=np.uint8)
    image2_array = np.array(image2, dtype=np.uint8)

    if method == "convolution":
        # Znajdź współrzędne maksymalnej intensywności metodą konwolucji
        max_coordinates, max_intensity, red_channel = find_max_coordinates_convolution(
            image1_array, image2_array
        )
    elif method == "sum":
        # Znajdź współrzędne maksymalnej intensywności metodą sumowania
        max_index, max_intensity, red_channel = find_max_coordinates_sum(
            image1_array, image2_array
        )
        max_coordinates = (0, int(max_index))  # Ustaw współrzędne na podstawie indeksu

    # Konwertuj wygładzony wynik z powrotem na obraz PIL
    result_image = Image.fromarray(red_channel)

    # Zapisz wynik jako obraz PNG
    result_image.save(current_folder / ".." / "photos" / "result_image.png")
    print("Obraz wynikowy zapisany jako result_image.png")
    print("Najwyższa średnia intensywność czerwieni:", max_intensity)
    print("Współrzędne ramki o najwyższej intensywności:", max_coordinates)

    # Na podstawie dopasowania jest liczona rzeczywista odległość
    distance = max_coordinates[1]
    distance = (
        7.223e-14 * distance**6
        - 1.721e-10 * distance**5
        + 1.647e-07 * distance**4
        - 8.111e-05 * distance**3
        + 0.02198 * distance**2
        - 3.343 * distance
        + 289.5
    )
    distance = f"{distance:.2f}"

    # Wyświetl rzeczywistą odległość w cm
    print("Rzeczywista odległość:", distance, "cm")

    return distance, max_coordinates, max_intensity


def process_all_pairs(folder_path):
    folder = Path(folder_path)
    image_files = sorted(folder.glob("*.png"))

    # Tworzenie par obrazów
    image_pairs = [
        (str(image_files[i]), str(image_files[i + 1]))
        for i in range(0, len(image_files), 2)
    ]

    total_time_conv = 0
    total_time_sum = 0
    num_pairs = 0

    # Przetwarzanie każdej pary obrazów
    for path1, path2 in image_pairs:
        if os.path.exists(path1) and os.path.exists(path2):
            print(f"\n\nPrzetwarzanie pary: {path1} i {path2}")

            # Oblicz dystans metodą konwolucji
            print("METODA KONWOLUCJI")
            start_time_conv = time.time()
            distance_conv, max_coordinates_conv, max_intensity_conv = (
                calculate_distance(path1, path2, method="convolution")
            )
            end_time_conv = time.time()
            time_conv = end_time_conv - start_time_conv
            total_time_conv += time_conv

            # Oblicz dystans metodą sumowania
            print("METODA SUMOWANIA")
            start_time_sum = time.time()
            distance_sum, max_coordinates_sum, max_intensity_sum = calculate_distance(
                path1, path2, method="sum"
            )
            end_time_sum = time.time()
            time_sum = end_time_sum - start_time_sum
            total_time_sum += time_sum

            num_pairs += 1

            # Wydrukuj czas wykonywania obu metod
            print(f"Czas wykonywania metody konwolucji: {time_conv:.4f} sekund")
            print(f"Czas wykonywania metody sumowania: {time_sum:.4f} sekund")
        else:
            print(f"Brakujące pliki: {path1} lub {path2}")

    # Oblicz i wyświetl średni czas wykonywania obu metod
    if num_pairs > 0:
        avg_time_conv = total_time_conv / num_pairs
        avg_time_sum = total_time_sum / num_pairs
        print(f"\n\nŚredni czas wykonywania metody konwolucji: {avg_time_conv:.4f} sekund")
        print(f"Średni czas wykonywania metody sumowania: {avg_time_sum:.4f} sekund")

    # Usuń plik result_image.png, jeśli istnieje
    result_image_path = folder / "result_image.png"

    if result_image_path.exists():
        os.remove(result_image_path)
        print(f"Plik {result_image_path} został usunięty.")
    else:
        print(f"Plik {result_image_path} nie istnieje.")


if __name__ == "__main__":
    # Ścieżka do folderu z obrazami
    input_folder = current_folder / ".." / "photos"
    process_all_pairs(input_folder)
