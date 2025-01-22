# utils/cam.py
#
# Opis: Plik zawiera klasy i funkcje do obsługi kamery oraz przechwytywania obrazów.
# Autorzy: Michał Miler, Magdalena Różycka, Szymon Kosz
# Data: 22.01.2025

import cv2
from pathlib import Path

# Uzyskaj ścieżkę do bieżącego folderu
current_folder = Path(__file__).parent


class Camera:
    def __init__(self):
        # Zainicjuj bieżącą klatkę jako None
        self.current_frame = None

        # Otwórz kamerę za pomocą OpenCV (0 odnosi się do domyślnej kamery)
        self.cap = cv2.VideoCapture(0)

    def start_opencv_window(self):
        # Ciągłe przechwytywanie klatek z kamery
        while True:
            # Odczytaj klatkę z kamery
            ret, frame = self.cap.read()
            if not ret:
                # Jeśli przechwycenie klatki się nie powiedzie, pomiń tę iterację
                continue

            # Wyświetl przechwyconą klatkę w oknie OpenCV
            cv2.imshow("Camera", frame)

            # Zaktualizuj bieżącą klatkę do najnowszej przechwyconej klatki
            self.current_frame = frame

            # Wyjdź z pętli, jeśli naciśnięto klawisz 'q' lub zamknięto okno
            if (
                cv2.waitKey(1) & 0xFF == ord("q")
                or cv2.getWindowProperty("Camera", cv2.WND_PROP_VISIBLE) < 1
            ):
                break

        # Zwolnij kamerę i zamknij okna OpenCV po zakończeniu
        self.cap.release()
        cv2.destroyAllWindows()

    def get_current_frame(self):
        # Zwróć najnowszą przechwyconą klatkę
        return self.current_frame

    def save_frame(self, index):
        # Zapisz bieżącą klatkę do pliku PNG
        if self.current_frame is not None:
            # Zapisz obraz jako "captured_frame.png" w bieżącym katalogu
            cv2.imwrite(
                current_folder / ".." / "photos" / f"captured_frame_{index}.png",
                self.current_frame,
            )
            print(f"Klatka zapisana jako 'captured_frame_{index}.png'")
        else:
            print("Brak dostępnej klatki do zapisania.")
