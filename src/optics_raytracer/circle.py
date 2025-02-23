import numpy as np
from .surface import surface_dtype
from .primitives import vector_dtype

circle_dtype = np.dtype([
    ('center', *vector_dtype),      # Center point of the circle
    ('normal', *vector_dtype),      # Normal vector of the circle's plane
    ('radius', np.float64),         # Radius of the circle
])

def build_circle(center: np.ndarray, radius: float, normal: np.ndarray):
    """
    Create a circle numpy structured array.
    
    Args:
        center: 3D center point of the circle
        radius: Radius of the circle
        normal: Normal vector of the circle's plane
        
    Returns:
        Numpy structured array representing the circle
    """
    normal = normal / np.linalg.norm(normal)  # Normalize
    return np.array(
        (center, normal, radius),
        dtype=circle_dtype
    )

def get_hits_mask(circle, points_array):
    """
    Check which points lie within the circle. Assumes that it's already in the plane.
    
    Args:
        circle: Circle object with center, normal and radius
        points_array: Array of points to check (Nx3)
        
    Returns:
        Boolean mask array indicating which points are inside the circle
    """
    # Vector from center to each point
    center_to_point = points_array - circle['center']
    
    # Then check if points are within radius
    within_radius = np.linalg.norm(center_to_point, axis=1) <= circle['radius']
    
    return within_radius
