# Implement a python script, which creates a 1000x1000 png image as output
# The image has white background
# Vertical and horizontal through the middle goes 2 lines making a + through the image
# From the center, there are circles, with radius start from 20, until reaching the end of the image, with step of radius increase 20 pixels

import numpy as np
from PIL import Image, ImageDraw
import colorsys


def create_target_image(
    size=1000, output_path="target.png", line_thickness=2, circle_thickness=50, step=50
):
    """
    Create a target image with the following properties:
    - White background
    - Black cross through the middle
    - Concentric circles from the center with radius increasing by step px
    - Antialiased lines and circles
    - Distinct colors for each circle
    """
    # Create a white image with RGBA mode for antialiasing
    image = Image.new("RGBA", (size, size), color=(255, 255, 255, 255))

    # Create a drawing context with antialiasing
    draw = ImageDraw.Draw(image, "RGBA")

    # Find the center
    center = (size // 2, size // 2)

    # Draw concentric circles with different colors
    max_radius = int(np.sqrt(2) * size / 2)  # Maximum possible radius to reach corners
    radius = step

    while radius <= max_radius:
        # Calculate a color based on the radius
        # Use HSV color space for more distinct colors
        hue = (radius / max_radius) * 0.8  # Keep hue in a good range (0.0-0.8)
        rgb = colorsys.hsv_to_rgb(hue, 0.9, 0.9)  # High saturation and value

        # Convert to 8-bit RGB values
        color = tuple(int(c * 255) for c in rgb)

        # Draw circle with current radius and thicker line
        draw.ellipse(
            [
                (center[0] - radius, center[1] - radius),
                (center[0] + radius, center[1] + radius),
            ],
            outline=color,
            width=circle_thickness + 1,
        )
        radius += step

    # Draw the vertical and horizontal lines (the + sign)
    draw.line(
        [(center[0], 0), (center[0], size)], fill="black", width=line_thickness
    )  # Vertical
    draw.line(
        [(0, center[1]), (size, center[1])], fill="black", width=line_thickness
    )  # Horizontal

    # Save the image
    image.save(output_path)
    print(f"Image saved to {output_path}")


if __name__ == "__main__":
    create_target_image(output_path="experiments/assets/target.png")
