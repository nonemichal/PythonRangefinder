# main.py

from utils.gui import GUI


def main():
    # Create an instance of the CameraGUI class
    app = GUI()
    app.mainloop()  # Run the Tkinter event loop to display the GUI


if __name__ == "__main__":
    # Execute the main function if this file is run directly
    main()
