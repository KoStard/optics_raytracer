from PIL import Image

class ImageSaver:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # Create empty image in RGB mode
        self.image = Image.new('RGB', (width, height))
        self.pixels = self.image.load()
        self.current_x = 0
        self.current_y = 0
    
    def add_pixel(self, color):
        # Convert color to 8-bit RGB values
        r = int(255.999 * color[0])
        g = int(255.999 * color[1])
        b = int(255.999 * color[2])
        
        # Set pixel and move to next position
        self.pixels[self.current_x, self.current_y] = (r, g, b)
        
        # Update position
        self.current_x += 1
        if self.current_x >= self.width:
            self.current_x = 0
            self.current_y += 1

    def save(self, filename: str):
        # Save image with format determined by extension
        self.image.save(filename)