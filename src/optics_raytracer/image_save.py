from .vec3 import Color3


class ImageSaver:
    # PPM
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.buffer = [
            f"""P3
{width} {height}
255"""]
    
    def add_pixel(self, color: Color3):
        self.buffer.append(self._serialize_color(color))
    
    def _serialize_color(self, color: Color3):
        red = int(255.999 * color.x)
        green = int(255.999 * color.y)
        blue = int(255.999 * color.z)
        return f"{red} {green} {blue}"

    def save(self, filename: str):
        with open(filename, 'w') as f:
            f.write('\n'.join(self.buffer))
