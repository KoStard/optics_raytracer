# Understand the impact of lens on slope https://physics.stackexchange.com/questions/690925/what-is-the-angle-of-a-ray-passing-through-a-thin-lens
# Build logic to go to the 2d plane of ray + norm, get slope, adjust, recreate the vector.

from .circle import Circle
from .ray import Ray
from .vec3 import Point3, Vec3


class Lens(Circle):
    def __init__(self, center: Point3, radius: float, normal: Vec3, focal_distance: float):
        super().__init__(center, radius, normal)
        self.focal_distance = focal_distance
    
    def hit(self, ray: Ray, t_min=0, t_max=None):
        t = super().hit(ray, t_min, t_max)
        if t is None:
            return None
        if t < 1e-6:
            return None
        return t
        
    
    def get_new_ray(self, ray: Ray, point: Point3) -> Ray:
        new_direction = ray.direction - (point - self.center) / self.focal_distance * (ray.direction.dot(self.normal))
        new_ray = Ray(point, new_direction)
        return new_ray