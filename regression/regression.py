import os
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Define exponential decay function
def exponential_func(x, a, b):
    return a * np.exp(-b * x)

# Get the current script's directory
current_path = os.path.dirname(os.path.abspath(__file__))

# Construct the path to data.csv
data_file = os.path.join(current_path, 'data.csv')

# Load data from CSV
data = pd.read_csv(data_file)

# Extract x (pixel) and y (distance)
x = data['pixel'].values
y = data['distance'].values

# Normalize x for better numerical stability
x_normalized = x / max(x)

# Fit the data with initial guesses
initial_guesses = [300, 0.01]  # Adjust these values as needed
params, covariance = curve_fit(exponential_func, x_normalized, y, p0=initial_guesses)

# Extract fitted parameters
a, b = params
print(f"Fitted equation: y = {a:.4f} * exp(-{b:.4f} * x)")

# Generate points for the fitted curve
x_fit = np.linspace(min(x), max(x), 500)
y_fit = exponential_func(x_fit / max(x), a, b)

# Plot the data and the fit
plt.scatter(x, y, label='Data')
plt.plot(x_fit, y_fit, color='red', label='Fitted function')
plt.xlabel('Pixel')
plt.ylabel('Distance')
plt.legend()
plt.title('Exponential Fit')
plt.show()
