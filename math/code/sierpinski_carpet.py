import numpy as np
import matplotlib.pyplot as plt

def draw_carpet(x, y, size, depth, canvas):
    if depth == 0:
        canvas[x:x+size, y:y+size] = 1
    else:
        new_size = size // 3
        new_depth = depth - 1

        for i in range(3):
            for j in range(3):
                if i == 1 and j == 1:
                    continue  # Skip the center square
                new_x = x + i * new_size
                new_y = y + j * new_size
                draw_carpet(new_x, new_y, new_size, new_depth, canvas)

def plot_carpet(size, depth):
    # Create a canvas to draw the carpet on
    canvas = np.zeros((size, size), dtype=np.uint8)

    # Draw the Sierpinski Carpet
    draw_carpet(0, 0, size, depth, canvas)

    # Display the carpet using matplotlib
    plt.imshow(canvas, cmap='binary')
    plt.axis('off')
    plt.show()

# Test the script
plot_carpet(243, 4)  # Size: 243 pixels, Depth: 5

