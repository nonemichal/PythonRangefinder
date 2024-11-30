from PIL import Image
import numpy as np
import cv2

# Load the two images
image1 = Image.open("o2.png")
image2 = Image.open("o1.png")

# Ensure both images have the same size and mode (RGB)
image1 = image1.convert("RGB")
image2 = image2.convert("RGB")

# Convert images to NumPy arrays
image1_array = np.array(image1, dtype=np.uint8)
image2_array = np.array(image2, dtype=np.uint8)

# Calculate the difference, avoiding wrap-around
result_array = image2_array.astype(np.int16) - image1_array.astype(np.int16)
result_array[result_array < 0] = 0  # Set any negative values to 0
result_array = result_array.astype(np.uint8)  # Convert back to uint8

red_channel = result_array[:, :, 0] # Red color only

# Apply a 3x3 averaging filter (moving average) to smooth the result
# Kernel for averaging
kernel = np.ones((6, 6), np.float32) / 9
red_channel = cv2.filter2D(red_channel, -1, kernel)

# Initialize variables to store the maximum average intensity and its coordinates
max_intensity = 0
max_coordinates = (0, 0)

# Iterate over the red channel, moving the 9x9 frame across the image
for i in range(red_channel.shape[0] - 8):  # Subtract 8 to fit a 9x9 frame
    for j in range(red_channel.shape[1] - 8):
        # Extract the current 9x9 frame
        frame = red_channel[i:i+9, j:j+9]
        
        # Calculate the mean intensity of the current frame
        mean_intensity = np.mean(frame)
        
        # Update max_intensity and max_coordinates if the current mean is the highest found so far
        if mean_intensity > max_intensity:
            max_intensity = mean_intensity
            max_coordinates = (i + 5, j + 5)

# Convert the smoothed result back to a PIL Image
result_image = Image.fromarray(red_channel)

# Save the result as a PNG image
result_image.save("result_image_smoothed.png")
print("Result image saved as result_image_smoothed.png")
print("Highest average red intensity:", max_intensity)
print("Coordinates of the frame with highest intensity:", max_coordinates)
