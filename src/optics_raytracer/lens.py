import numpy as np

from optics_raytracer.ray import build_rays
from .circle import circle_dtype

lens_dtype = np.dtype([
    *circle_dtype.descr,  # Inherit circle fields
    ('focal_distance', np.float32),  # Focal distance of the lens
])

class Lens:
    """
    Wrapper class for lens_dtype numpy arrays with helper methods.
    """
    def __init__(self, lens_array: np.ndarray):
        if lens_array.dtype != lens_dtype:
            raise ValueError(f"Input array must have dtype {lens_dtype}")
        self.array = lens_array
        
    @property
    def center(self) -> np.ndarray:
        return self.array['center']
    
    @property
    def normal(self) -> np.ndarray:
        return self.array['normal']
    
    @property
    def focal_distance(self) -> float:
        return self.array['focal_distance']

    @staticmethod
    def build(center: np.ndarray, radius: float, normal: np.ndarray, focal_distance: float) -> 'Lens':
        """
        Create a new Lens instance.
        
        Args:
            center: 3D center point of the lens
            radius: Radius of the lens
            normal: Normal vector of the lens surface
            focal_distance: Focal distance of the lens
            
        Returns:
            New Lens instance
        """
        normal = normal / np.linalg.norm(normal)  # Normalize
        return Lens(np.array(
            (center, normal, radius, focal_distance),
            dtype=lens_dtype
        ))

    def get_new_rays(self, hitting_rays: np.ndarray, hit_points: np.ndarray) -> np.ndarray:
        """
        Calculate new ray directions after refraction through the lens.
        
        Args:
            hitting_rays: Array of incoming rays (ray_dtype)
            hit_points: Array of hit points on lens surface (Nx3)
            
        Returns:
            Array of refracted rays (ray_dtype)
        """
        # Need proof if this works, as it's a faster algorithm
        # # Vector from lens center to hit points
        # center_to_point = hit_points - self.center
        
        # # Scale by focal distance and ray normal component
        # # TODO fix cases when normal is pointing the other direction
        # scale = np.matvec(hitting_rays['direction'], self.normal) / self.focal_distance
        # direction_change = center_to_point * scale[:, np.newaxis]
        
        # # Calculate new directions
        # new_directions = hitting_rays['direction'] - direction_change
        # new_directions = new_directions / np.linalg.norm(new_directions)
        
        # # Build new rays
        # return build_rays(hit_points, new_directions)
        
        def rows_dot(m1, m2):
            return np.einsum('ij,ij->i', m1, m2)
        
        normal_away_from_origin = np.matvec(hitting_rays['direction'], self.normal) > 0
        normals = np.full((len(hitting_rays), 3), self.normal)
        normals[~normal_away_from_origin] = -self.normal
        scale = ((rows_dot(hitting_rays['origin'] - self.center, normals) + self.focal_distance) / rows_dot(hitting_rays['direction'], normals))
        new_directions = self.center - hitting_rays['origin'] + hitting_rays['direction'] * scale[:, np.newaxis]
        new_directions = new_directions / np.linalg.norm(new_directions)
        if self.focal_distance < 0:
            new_directions = -new_directions
        return build_rays(hit_points, new_directions)
