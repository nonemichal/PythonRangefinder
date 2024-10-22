# Triangulation-based Rangefinder Project

## Description

This is a project for a **rangefinder** that calculates distance using the triangulation method. The program responsible for camera handling is located in `cam/cam.py`, while the main execution program is in `dalmierz.py`. The camera opens and displays live video in a window. You can terminate the camera feed by pressing the `q` key.

## Important Notes

- This project requires **Python 3.13**. You can download it from the official website [Python.org](https://www.python.org/downloads/).
- During installation, make sure that **Python is added to your PATH**. This option can be selected during the Python installer setup process.

## Installation

Follow these steps to set up the project:

### Step 1: Install Python

If Python is not yet installed on your system:
1. Download the **Python 3.13** installer from [Python.org](https://www.python.org/downloads/).
2. During the installation process, **make sure to check the box** that says **"Add Python to PATH"** before clicking "Install Now."
3. Complete the installation and verify that Python is correctly installed by opening a Command Prompt (cmd) or terminal and typing:

```bash
python --version
```

You should see something like:

```bash
Python 3.13.x
```

### Step 2: Set Up the Project

1. Open Command Prompt (cmd) or terminal.
2. Navigate to the directory where you want to create the project:

```bash
cd C:\path\to\your\project
```

3. Create a virtual environment in this directory:

```bash
python -m venv venv
```

### Step 3: Activate the Virtual Environment

To activate the virtual environment:

```bash
venv\Scripts\activate
```

You will know the environment is active when you see `(venv)` at the beginning of your command line.

### Step 4: Install Required Libraries

Install the necessary dependencies (such as OpenCV) by running the following command:

```bash
pip install -r requirements.txt
```

This will install all the required libraries needed for the project to function.

### Step 5: Run the Program

**If you are already in the project directory and venv is already activated, you can skip to point 4 and run the program directly.**

1. Open Command Prompt (cmd) or your terminal.
2. Navigate to the project directory (where you saved `dalmierz.py`) using:

```bash
cd C:\path\to\your\project
```

3. Activate the virtual environment by typing:

```bash
venv\Scripts\activate
```

4. Run the main program (dalmierz.py) by entering:

```bash
python dalmierz.py
```

After executing this command, the camera feed will open, and the program will begin calculating distances using triangulation.

### Step 6: Termination and Deactivation

To stop the program, press the `q` key while the camera window is open. After finishing work on the project, you can deactivate the virtual environment by typing:

```bash
deactivate
```

This will return you to the normal system environment.

## How to Update `requirements.txt`

If you install any new libraries during development, update the requirements.txt file to keep track of the dependencies:

```bash
pip freeze > requirements.txt
```
This ensures that all the necessary packages are listed for easy installation by others.