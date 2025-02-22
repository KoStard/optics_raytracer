import numpy as np
from .primitives import vector_dtype

ray_dtype = np.dtype([
    ('origin', *vector_dtype),
    ('direction', *vector_dtype),
])

def get_ray_point_at_t(ray, t):
    return ray['origin'] + t * ray['direction']

def get_ray_points_array_at_t_array(rays, t_array):
    return rays['origin'] + t_array[:, np.newaxis] * rays['direction']
