import numpy as np
import math

class Exporter3D:
    def __init__(self):
        self.vertices = np.empty((0, 3), dtype=np.float32)
        self.lines = []
        self.vertex_to_index = {}

    def _add_vertex(self, point: np.ndarray):
        key = tuple(point)
        if key in self.vertex_to_index:
            return self.vertex_to_index[key]
        
        index = len(self.vertices) + 1
        self.vertices = np.vstack([self.vertices, point])
        self.vertex_to_index[key] = index
        return index

    def add_line(self, start: np.ndarray, end: np.ndarray, group="rays"):
        idx1 = self._add_vertex(start)
        idx2 = self._add_vertex(end)
        self.lines.append(([idx1, idx2], group))

    def add_circle(self, circle: np.ndarray, resolution=50):
        """Add a circle using circle_dtype"""
        normal = circle['normal']
        center = circle['center']
        radius = circle['radius']
        
        # Find orthogonal basis vectors
        if abs(normal[0]) < 0.9:
            arbitrary = np.array([1, 0, 0])
        else:
            arbitrary = np.array([0, 1, 0])
        tangent = np.cross(normal, arbitrary)
        tangent /= np.linalg.norm(tangent)
        binormal = np.cross(normal, tangent)
        
        # Generate circle points
        angles = np.linspace(0, 2 * math.pi, resolution)
        points = (
            center[np.newaxis, :] + 
            radius * np.cos(angles)[:, np.newaxis] * tangent[np.newaxis, :] +
            radius * np.sin(angles)[:, np.newaxis] * binormal[np.newaxis, :]
        )
        
        # Add lines for the circle
        start_idx = self._add_vertex(points[0])
        prev_idx = start_idx
        for pt in points[1:]:
            idx = self._add_vertex(pt)
            self.lines.append(([prev_idx, idx], "circles"))
            prev_idx = idx
        self.lines.append(([prev_idx, start_idx], "circles"))

    def add_rectangle(self, rectangle: np.ndarray):
        """Add a rectangle using rectangle_dtype"""
        center = rectangle['middle_point']
        u = rectangle['u_vector']
        v = np.cross(rectangle['normal'], u)
        width = rectangle['width']
        height = rectangle['height']
        
        # Calculate corner points
        p1 = center - u*(width/2) - v*(height/2)
        p2 = center + u*(width/2) - v*(height/2)
        p3 = center + u*(width/2) + v*(height/2)
        p4 = center - u*(width/2) + v*(height/2)
        
        # Add edges
        for start, end in [(p1, p2), (p2, p3), (p3, p4), (p4, p1)]:
            self.add_line(start, end, group="rectangles")
    
    def add_point(self, point: np.ndarray, group="hits", size=0.01):
        """Add a point as a small cross for visibility"""
        offsets = np.eye(3) * size
        for axis in range(3):
            self.add_line(point - offsets[axis], point + offsets[axis], group)
    
    def save_to_obj(self, output_path: str):
        # Define materials with colors and transparency
        rays_color = (1, 0, 0, 0.05)         # red, opaque
        materials = {
            "rays": rays_color,
            "rays/missed": rays_color,
            "rays/1_depth": rays_color,
            "rays/2_depth": rays_color,
            "rays/3_depth": rays_color,
            "rays/4_depth": rays_color,
            "rays/5_depth": rays_color,
            "rays/6_depth": rays_color,
            "rays/7_depth": rays_color,
            "rays/8_depth": rays_color,
            "rays/9_depth": rays_color,
            "circles": (0, 0, 1, 0.5),      # blue, semi-transparent
            "rectangles": (0, 1, 0, 0.5),   # green, semi-transparent
            "hits": (0, 0, 0, 1)            # black, opaque
        }
        
        with open(output_path, "w") as f:
            # Write vertices
            for v in self.vertices:
                f.write(f"v {v[0]} {v[1]} {v[2]}\n")
            
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
