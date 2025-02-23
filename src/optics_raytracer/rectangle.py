import numpy as np
from .primitives import vector_dtype

rectangle_dtype = np.dtype([
    ('middle_point', *vector_dtype),
    ('normal', *vector_dtype),
    ('width', np.float64),
    ('height', np.float64),
    ('u_vector', *vector_dtype),
])

def build_rectangle(
    middle_point: np.ndarray,
    normal: np.ndarray,
    width: float,
    height: float,
    u_vector: np.ndarray
):
    """
    Create a rectangle numpy structured array.
    
    Args:
        middle_point: Center point of the rectangle
        normal: Normal vector of the rectangle's plane
        width: Width of the rectangle
        height: Height of the rectangle
        u_vector: U vector defining the rectangle's horizontal axis
        
    Returns:
        Numpy structured array representing the rectangle
    """
    normal = normal / np.linalg.norm(normal)  # Normalize
    return np.array(
        (middle_point, normal, width, height, u_vector),
        dtype=rectangle_dtype
    )

def get_rectangle_hits_mask(rectangle, points_array):
    middle_to_point_vector_array = points_array - rectangle['middle_point']

    # Get u and v projections
    u = rectangle['u_vector'][:, np.newaxis]
    v = np.cross(rectangle['normal'], rectangle['u_vector'])[:, np.newaxis]
    u_projection_vectors = np.matmul(np.matmul(u, u.T) / np.matmul(u.T, u), middle_to_point_vector_array.T).T
    v_projection_vectors = np.matmul(np.matmul(v, v.T) / np.matmul(v.T, v), middle_to_point_vector_array.T).T

    return np.logical_and(
        np.linalg.norm(u_projection_vectors, axis=1) <= rectangle['width'] / 2,
        np.linalg.norm(v_projection_vectors, axis=1) <= rectangle['height'] / 2
    )
