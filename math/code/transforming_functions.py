import numpy as np
import matplotlib.pyplot as plt
import keyboard
import random

# Create a range of x values
x = np.linspace(-10, 10, 400)

# Define a function to plot and apply translations, mirroring, or flipping
def plot_and_transform(transform_type, h_translation, v_translation, mirror=False):
    # Create the original absolute function f(x) = |x|
    y_original = np.abs(x)

    if transform_type == 't' or transform_type == 'm':
        # Apply horizontal and vertical translations
        y_transformed = np.abs(x - h_translation) + v_translation
        if mirror:
            # Apply mirroring
            y_transformed = -y_transformed
        title = f"Absolute Function with h_translation={h_translation:.2f}, v_translation={v_translation:.2f}"
    elif transform_type == 'f':
        # Apply flipping
        y_transformed = -y_original
        title = "Flipped Absolute Function"

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(x, y_original, label="Original Absolute Function $|x|$", color='b')
    plt.plot(x, y_transformed, label="Transformed Function", color='r')

    # Add labels and legend
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()

    # Display the plot
    plt.title(title)
    plt.grid(True)
    plt.show()

# Count how many times the transformation has been applied
transform_count = 0

# Apply transformations 15 times
while transform_count < 15:
    # Randomly choose between 't' for translation, 'm' for mirroring, or 'f' for flipping
    transform_type = random.choice(['t', 'm', 'f'])

    if transform_type == 't' or transform_type == 'm':
        # Apply translations
        h_translation = np.random.uniform(-5.0, 5.0)  # Horizontal translation amount
        v_translation = np.random.uniform(-5.0, 5.0)  # Vertical translation amount
    else:
        # No translations for flipping
        h_translation = v_translation = None

    if transform_type == 'm':
        # Apply mirroring
        mirror = True
    else:
        mirror = False

    plot_and_transform(transform_type, h_translation, v_translation, mirror=mirror)
    transform_count += 1

print("Transformations completed.")
