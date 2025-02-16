from .ray import Ray
from .surface import Surface
from .vec3 import Point3, Vec3


class Rectangle(Surface):
    def __init__(self, left_top: Point3, width: float, height: float, u_vector: Vec3, normal: Vec3):
        super().__init__(left_top, normal)
        self.left_top = left_top
        self.u = u_vector.unit_vector # x
        self.v = normal.cross(u_vector).unit_vector # y
        self.width = width
        self.height = height
        self.middle_point = self.left_top + self.u * width / 2 + self.v * height / 2
    
    def hit(self, ray: Ray, t_min=0, t_max=None):
        t = super().hit(ray, t_min, t_max)
        if t is None:
            return None
        P = ray.at(t)
        if abs(P.x - self.middle_point.x) >= self.width / 2 or abs(P.y - self.middle_point.y) >= self.height / 2:
            return None
        return t
