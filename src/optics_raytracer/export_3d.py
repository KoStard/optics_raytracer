import numpy as np
import math
from .ray_group_namer import RayGroupNamer


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
        normal = circle["normal"]
        center = circle["center"]
        radius = circle["radius"]

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
            center[np.newaxis, :]
            + radius * np.cos(angles)[:, np.newaxis] * tangent[np.newaxis, :]
            + radius * np.sin(angles)[:, np.newaxis] * binormal[np.newaxis, :]
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
        center = rectangle["middle_point"]
        u = rectangle["u_vector"]
        v = np.cross(rectangle["normal"], u)
        width = rectangle["width"]
        height = rectangle["height"]

        # Calculate corner points
        p1 = center - u * (width / 2) - v * (height / 2)
        p2 = center + u * (width / 2) - v * (height / 2)
        p3 = center + u * (width / 2) + v * (height / 2)
        p4 = center - u * (width / 2) + v * (height / 2)

        # Add edges
        for start, end in [(p1, p2), (p2, p3), (p3, p4), (p4, p1)]:
            self.add_line(start, end, group="rectangles")

    def add_point(self, point: np.ndarray, group="hits", size=0.01):
        """Add a point as a small cross for visibility"""
        offsets = np.eye(3) * size
        for axis in range(3):
            self.add_line(point - offsets[axis], point + offsets[axis], group)

    def save_to_obj(self, output_path: str, output_mtl_path: str):
        # Define materials with colors and transparency
        rays_color = (1, 0, 0, 0.1)  # red, opaque
        
        # Generate distinct colors for different object/lens hits
        def generate_color(index, obj_type='lens'):
            # Simple pastel color generation with lower intensity
            # Use a different base hue for lenses vs objects
            base_r, base_g, base_b = (0.2, 0.3, 0.7) if obj_type == 'lens' else (0.7, 0.5, 0.2)
            
            # Vary the colors slightly based on index
            r = (base_r + index * 0.05) % 0.7
            g = (base_g + index * 0.07) % 0.7
            b = (base_b + index * 0.06) % 0.7
            
            # Lower alpha for less visual clutter
            alpha = 0.2
            
            return (r, g, b, alpha)
        
        materials = {
            "primary_rays": rays_color,
            "missed_rays": (0.1, 0.1, 0.1, 0.1),
            "lens_outlines": (0, 0.4, 0.8, 0.5),  # blue, semi-transparent
            "screen_outlines": (0, 0.6, 0.2, 0.5),  # green, semi-transparent
            "hit_points": (0, 0, 0, 1),  # black, opaque
        }
        
        # Add basic refraction depth materials
        for depth in range(1, 10):
            ordinal = RayGroupNamer.get_ordinal(depth)
            materials[f"{ordinal}_refraction"] = rays_color
        
        # Add materials for each lens and object dynamically
        # We don't know how many there will be, so we'll create materials for a reasonable number
        for hit_object_index in range(20):
            # Lens ray materials
            # Use the RayGroupNamer to generate consistent group names
            
            lens_color = generate_color(hit_object_index, 'lens')
            materials[RayGroupNamer.get_ray_group_name(None, "lens", hit_object_index)] = lens_color
            materials[RayGroupNamer.get_ray_group_name(1, "lens", hit_object_index)] = lens_color
            materials[RayGroupNamer.get_ray_group_name(2, "lens", hit_object_index)] = lens_color
            materials[RayGroupNamer.get_ray_group_name(3, "lens", hit_object_index)] = lens_color
            materials[RayGroupNamer.get_hit_point_group_name("lens", hit_object_index)] = lens_color
            
            # Object ray materials
            obj_color = generate_color(hit_object_index, 'object')
            materials[RayGroupNamer.get_ray_group_name(None, "object", hit_object_index)] = obj_color
            materials[RayGroupNamer.get_ray_group_name(1, "object", hit_object_index)] = obj_color
            materials[RayGroupNamer.get_ray_group_name(2, "object", hit_object_index)] = obj_color
            materials[RayGroupNamer.get_ray_group_name(3, "object", hit_object_index)] = obj_color
            materials[RayGroupNamer.get_hit_point_group_name("object", hit_object_index)] = obj_color

        # Create MTL file
        with open(output_mtl_path, "w") as mtl_file:
            # Write material definitions to the MTL file
            for material, (r, g, b, alpha) in materials.items():
                mtl_file.write(f"newmtl {material}\n")
                mtl_file.write(f"Kd {r} {g} {b}\n")
                mtl_file.write(f"d {alpha}\n\n")

        with open(output_path, "w") as f:
            # Reference the material library
            mtl_filename = output_mtl_path.split("/")[-1]
            f.write(f"mtllib {mtl_filename}\n\n")

            # Write vertices
            for v in self.vertices:
                f.write(f"v {v[0]} {v[1]} {v[2]}\n")

            # Write lines grouped
            current_group = None
            for line_entry in self.lines:
                line, group = line_entry
                if group != current_group:
                    f.write(f"g {group}\n")
                    f.write(f"usemtl {group}\n")
                    current_group = group
                f.write("l " + " ".join(str(idx) for idx in line) + "\n")
