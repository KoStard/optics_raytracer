from .ray import Ray
from .vec3 import Point3


class ColoredObject:
    def __init__(self, color, object):
        self.color = color
        self.object = object
    
    def hit(self, ray):
        return self.object.hit(ray)
    
    def get_color(self, ray: Ray, point: Point3):
        return self.color