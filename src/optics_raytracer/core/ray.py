import numpy as np
from optics_raytracer.core.primitives import vector_dtype

ray_dtype = np.dtype(
    [
        ("origin", *vector_dtype),
        ("direction", *vector_dtype),
    ]
)


def get_ray_point_at_t(ray, t):
    return ray["origin"] + t * ray["direction"]


def get_ray_points_array_at_t_array(rays, t_array):
    return rays["origin"] + t_array[:, np.newaxis] * rays["direction"]


def build_rays(origins, directions):
    if origins.shape != directions.shape:
        raise ValueError("Origins and directions arrays must have the same shape.")

    rays = np.empty(
        origins.shape[:-1], dtype=ray_dtype
    )  # infer num rays from shape of input origins

    rays["origin"] = origins
    rays["direction"] = directions
    return rays
