# main.py
#
# Opis: Plik zawiera główną funkcję programu, która uruchamia GUI aplikacji.
# Autorzy: Michał Miler, Magdalena Różycka, Szymon Kosz
# Data: 22.01.2025

from utils.gui import GUI


# Główna funkcja programu
def main():
    # Utwórz instancję klasy CameraGUI
    app = GUI()
    app.mainloop()  # Uruchom pętlę zdarzeń Tkinter, aby wyświetlić GUI


if __name__ == "__main__":
    # Wykonaj funkcję main, jeśli ten plik jest uruchamiany bezpośrednio
    main()
