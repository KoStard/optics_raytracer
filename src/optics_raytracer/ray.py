from .vec3 import Vec3, Point3

class Ray:
    def __init__(self, origin: Point3 = None, direction: Vec3 = None):
        self._origin = origin
        self._direction = direction
    
    @property
    def origin(self):
        return self._origin

    @property
    def direction(self):
        return self._direction
    
    def at(self, t: float):
        return self._origin + t * self._direction

    def __str__(self):
        return f"{self._origin} + t * {self._direction}"
    
    def __repr__(self):
        return f"ray(origin={repr(self._origin)}, direction={repr(self._direction)})"
