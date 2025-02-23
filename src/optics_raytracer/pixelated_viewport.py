import numpy as np
from .primitives import vector_dtype

pixelated_viewport_dtype = np.dtype([
    ('middle_point', *vector_dtype),
    ('normal', *vector_dtype),
    ('width', np.float64),
    ('height', np.float64),
    ('u_vector', *vector_dtype),
    ('pixel_columns', np.int64),
    ('pixel_rows', np.int64),
])

def get_pixel_points(pixelated_viewport):
    """
    Returns height x width matrix of points, where each point is a pixel center.
    """
    u = pixelated_viewport['u_vector'][:, np.newaxis]
    v = np.cross(pixelated_viewport['normal'], pixelated_viewport['u_vector'])[:, np.newaxis]

    u_step = pixelated_viewport['width'] / (pixelated_viewport['pixel_columns'] - 1) * u
    v_step = pixelated_viewport['height'] / (pixelated_viewport['pixel_rows'] - 1) * v

    u_steps = (np.arange(pixelated_viewport['pixel_columns']) * u_step)
    v_steps = (np.arange(pixelated_viewport['pixel_rows']) * v_step)

    u_steps = u_steps - u_step * (pixelated_viewport['pixel_columns'] - 1) / 2
    v_steps = v_steps - v_step * (pixelated_viewport['pixel_rows'] - 1) / 2
    
    x = np.tile(u_steps.T, (pixelated_viewport['pixel_rows'], 1, 1))
    y = np.tile(v_steps.T[:, np.newaxis], (1, pixelated_viewport['pixel_columns'], 1))
    
    return pixelated_viewport['middle_point'][np.newaxis, np.newaxis, :] + x + y
