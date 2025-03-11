from PIL import Image
import numpy as np

class ImageSaver:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.pixels = None
        self.image = None
    
    def write_pixels(self, pixel_colors: np.ndarray):
        self.pixels = pixel_colors.astype('uint8')

    def save(self, filename: str):
        # Save image with format determined by extension
        self.image = Image.fromarray(self.pixels, mode='RGB')
        self.image.save(filename)
