from .vec3 import Point3, Vec3


class Surface:
    def __init__(self, point: Point3, normal: Vec3):
        self.point = point
        self.normal = normal.unit_vector
    
    def __repr__(self):
        return f"Surface({repr(self.point)}, {repr(self.normal)})"

    def hit(self, ray, t_min=0, t_max=None):
        if self.ray_is_parallel(ray):
            return None
        t = (self.point - ray.origin).dot(self.normal) / ray.direction.dot(self.normal)
        if t < t_min:
            return None
        if t_max is not None and t > t_max:
            return None
        return t

    def ray_is_parallel(self, ray):
        return ray.direction.dot(self.normal) <= 1e-5
