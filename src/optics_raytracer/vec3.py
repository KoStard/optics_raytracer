class Vec3:
    def __init__(self, e0=None, e1=None, e2=None):
        if e0 is None and e1 is None and e2 is None:
            self.e = [0, 0, 0]
        else:
            self.e = [e0, e1, e2]
    
    @property
    def x(self):
        return self.e[0]
    
    @property
    def y(self):
        return self.e[1]
    
    @property
    def z(self):
        return self.e[2]
    
    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def __getitem__(self, i):
        return self.e[i]
    
    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, other):
        if isinstance(other, Vec3):
            # Hadamard product (or element-wise product)
            return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            return Vec3(self.x * other, self.y * other, self.z * other)
    
    def __rmul__(self, other):
        return self * other
    
    def __truediv__(self, other):
        return Vec3(self.x / other, self.y / other, self.z / other)
    
    @property
    def length(self):
        return self.length_squared ** 0.5
    
    def __str__(self):
        return f"{self.x} {self.y} {self.z}"
    
    def __repr__(self):
        return f"vec3({self.x}, {self.y}, {self.z})"
    
    @property
    def length_squared(self):
        return self.x * self.x + self.y * self.y + self.z * self.z
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other):
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    @property
    def unit_vector(self):
        return self / self.length

class Point3(Vec3):
    def __repr__(self):
        return f"point3({self.x}, {self.y}, {self.z})"

class Color3(Vec3):
    
    def __repr__(self):
        return f"color3({self.x}, {self.y}, {self.z})"