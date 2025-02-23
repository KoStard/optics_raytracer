import numpy as np

from optics_raytracer.ray import build_rays
from .circle import circle_dtype

lens_dtype = np.dtype([
    *circle_dtype.descr,  # Inherit circle fields
    ('focal_distance', np.float64),  # Focal distance of the lens
])

def build_lens(center: np.ndarray, radius: float, normal: np.ndarray, focal_distance: float):
    """
    Create a lens numpy structured array.
    
    Args:
        center: 3D center point of the lens
        radius: Radius of the lens
        normal: Normal vector of the lens surface
        focal_distance: Focal distance of the lens
        
    Returns:
        Numpy structured array representing the lens
    """
    normal = normal / np.linalg.norm(normal)  # Normalize
    return np.array(
        (center, normal, radius, focal_distance),
        dtype=lens_dtype
    )

def get_new_rays_from_lens(lens, hitting_rays, hit_points):
    """
    Calculate new ray directions after refraction through the lens.
    
    Args:
        lens: Lens object (lens_dtype)
        hitting_rays: Array of incoming rays (ray_dtype)
        hit_points: Array of hit points on lens surface (Nx3)
        
    Returns:
        Array of refracted rays (ray_dtype)
    """
    # Vector from lens center to hit points
    center_to_point = hit_points - lens['center']
    
    # Scale by focal distance and ray normal component
    scale = np.matvec(hitting_rays['direction'], lens['normal']) / lens['focal_distance']
    direction_change = center_to_point * scale[:, np.newaxis]
    
    # Calculate new directions
    new_directions = hitting_rays['direction'] - direction_change
    new_directions = new_directions / np.linalg.norm(new_directions)
    
    # Build new rays
    return build_rays(hit_points, new_directions)
