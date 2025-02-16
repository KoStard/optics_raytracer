from .pixelated_viewport import PixelatedViewport
from .ray import Ray
from .vec3 import Color3, Point3


class InsertedImage(PixelatedViewport):
    def __init__(self, left_top, width, height, u_vector, normal, image):
        super().__init__(left_top, width, height, u_vector, normal, image.width, image.height)
        self.image = image
    
    def get_color(self, ray: Ray, point: Point3) -> Color3:
        column, row = self.convert_point_to_pixel(point)
        raw_color = self.image.getpixel((column, row))
        return Color3(raw_color[0] / 255, raw_color[1] / 255, raw_color[2] / 255)
