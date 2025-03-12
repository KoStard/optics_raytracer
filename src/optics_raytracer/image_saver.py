from PIL import Image
import torch

class ImageSaver:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.pixels = None
        self.image = None
    
    def write_pixels(self, pixel_colors: torch.Tensor):
        self.pixels = pixel_colors.cpu().numpy().astype('uint8')

    def save(self, filename: str):
        # Save image with format determined by extension
        self.image = Image.fromarray(self.pixels, mode='RGB')
        self.image.save(filename)