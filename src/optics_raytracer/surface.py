import numpy as np
from .primitives import vector_dtype

surface_dtype = np.dtype(
    [
        ("point", *vector_dtype),
        ("normal", *vector_dtype),
    ]
)


def get_surface_hit_ts(rays, surface_point, surface_normal, t_max=100000) -> np.ndarray:
    """
    Get the t of intersection of rays with a surface.
    surface_point - vec3
    surface_normal - vec3
    """
    P0 = surface_point
    n = surface_normal
    d_array = rays["direction"]
    O = rays["origin"]
    divisor = np.matvec(d_array, n)
    divisor[divisor == 0] = 1e-10
    t_array = np.matvec(P0 - O, n) / divisor
    t_array[t_array < 1e-6] = np.inf  # Negatives or at the beginning
    t_array[t_array > t_max] = np.inf
    return t_array


def get_surface_hit_ts_mask(hit_ts):
    return np.abs(hit_ts) < np.inf
