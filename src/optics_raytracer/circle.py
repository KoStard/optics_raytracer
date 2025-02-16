from .surface import Surface
from .vec3 import Point3, Vec3


class Circle(Surface):
    def __init__(self, center: Point3, radius: float, normal: Vec3):
        super().__init__(center, normal)
        self.center = center
        self.radius = radius
        self.radius_squared = radius * radius
    
    def hit(self, ray, t_min=0, t_max=None):
        t = super().hit(ray, t_min, t_max)
        if t is None:
            return None
        P = ray.at(t)
        center_to_point = (P - self.center)
        distance_sqr = center_to_point.dot(center_to_point)
        if distance_sqr >= self.radius_squared:
            return None
        return t
