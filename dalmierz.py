# main.py

from utils.gui import GUI


def main():
    # Utwórz instancję klasy CameraGUI
    app = GUI()
    app.mainloop()  # Uruchom pętlę zdarzeń Tkinter, aby wyświetlić GUI


if __name__ == "__main__":
    # Wykonaj funkcję main, jeśli ten plik jest uruchamiany bezpośrednio
    main()
