import math
from .circle import Circle
from .vec3 import Point3, Vec3

class Exporter3D:
    def __init__(self):
        self.vertices = []
        self.lines = []
        self.points = []
        self.vertex_to_index = {}

    def _add_vertex(self, point: Vec3):
        key = (point.x, point.y, point.z)
        if key in self.vertex_to_index:
            return self.vertex_to_index[key]
        index = len(self.vertices) + 1
        self.vertices.append(point)
        self.vertex_to_index[key] = index
        return index

    def add_line(self, start: Point3, end: Point3, group="rays"):
        idx1 = self._add_vertex(start)
        idx2 = self._add_vertex(end)
        self.lines.append(([idx1, idx2], group))

    def add_circle(self, circle: Circle, resolution=50):
        # Use the circle's normal to define the circle's plane
        normal = circle.normal.unit_vector
        # Choose an arbitrary vector not parallel to the normal
        if abs(normal.x) < 0.9:
            arbitrary = Vec3(1, 0, 0)
        else:
            arbitrary = Vec3(0, 1, 0)
        tangent = normal.cross(arbitrary).unit_vector
        binormal = normal.cross(tangent).unit_vector

        points = []
        for i in range(resolution):
            angle = 2 * math.pi * i / resolution
            offset = tangent * (circle.radius * math.cos(angle)) + binormal * (circle.radius * math.sin(angle))
            pt = circle.center + offset
            points.append(pt)
        # Add lines for the closed loop with group "circles"
        start_idx = self._add_vertex(points[0])
        prev_idx = start_idx
        for pt in points[1:]:
            idx = self._add_vertex(pt)
            self.lines.append(([prev_idx, idx], "circles"))
            prev_idx = idx
        self.lines.append(([prev_idx, start_idx], "circles"))

    def add_rectangle(self, rectangle):
        # Assumes rectangle has attributes left_top, u, v, width, and height.
        lt = rectangle.left_top
        u = rectangle.u
        v = rectangle.v
        p1 = lt
        p2 = lt + u * rectangle.width
        p3 = p2 + v * rectangle.height
        p4 = lt + v * rectangle.height
        for start, end in [(p1, p2), (p2, p3), (p3, p4), (p4, p1)]:
            self.add_line(start, end, group="rectangles")
    
    def add_point(self, point: Point3, group="hits", size=0.01):
        """Add a point as a small cross for visibility"""
        # Create a small cross using 3 perpendicular lines
        offset_x = Vec3(size, 0, 0)
        offset_y = Vec3(0, size, 0)
        offset_z = Vec3(0, 0, size)
        
        # X-axis line
        self.add_line(point - offset_x, point + offset_x, group)
        # Y-axis line
        self.add_line(point - offset_y, point + offset_y, group)
        # Z-axis line
        self.add_line(point - offset_z, point + offset_z, group)
    
    def save_to_obj(self, output_path: str):
        # Define materials with colors and transparency
        materials = {
            "rays": (1, 0, 0, 1),         # red, opaque
            "circles": (0, 0, 1, 0.5),      # blue, semi-transparent
            "rectangles": (0, 1, 0, 0.5),   # green, semi-transparent
            "hits": (0, 0, 0, 1)            # yellow, opaque
        }
        
        with open(output_path, "w") as f:
            # Write vertices
            for v in self.vertices:
                f.write(f"v {v.x} {v.y} {v.z}\n")
            
            # Write materials directly in the OBJ file
            f.write("\n# Material definitions\n")
            for material, (r, g, b, alpha) in materials.items():
                f.write(f"newmtl {material}\n")
                f.write(f"Kd {r} {g} {b}\n")
                f.write(f"d {alpha}\n\n")
            
            # Write lines grouped
            current_group = None
            for line_entry in self.lines:
                line, group = line_entry
                if group != current_group:
                    f.write(f"g {group}\n")
                    f.write(f"usemtl {group}\n")
                    current_group = group
                f.write("l " + " ".join(str(idx) for idx in line) + "\n")
            
            # Points are now represented as small spheres (circles)
