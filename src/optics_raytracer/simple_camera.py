import numpy as np

from .pixelated_viewport import get_pixel_points
from .primitives import vector_dtype
from .size import FloatSize, IntegerSize
from .ray import build_rays

simple_camera_viewport_dtype = np.dtype(
    [
        ("middle_point", *vector_dtype),
        ("normal", *vector_dtype),
        ("width", np.float64),
        ("height", np.float64),
        ("u_vector", *vector_dtype),
        ("pixel_columns", np.int64),
        ("pixel_rows", np.int64),
        ("camera_center", *vector_dtype),
    ]
)


def build_camera(
    camera_center: np.ndarray,
    focal_distance: float,
    viewport_size: FloatSize,
    image_size: IntegerSize,
    viewport_u_vector: np.ndarray,
    viewport_normal: np.ndarray,
):
    viewport_normal = viewport_normal / np.linalg.norm(viewport_normal)
    viewport_center = camera_center + focal_distance * viewport_normal
    return np.array(
        (
            viewport_center,
            viewport_normal,
            viewport_size.width,
            viewport_size.height,
            viewport_u_vector,
            image_size.width,
            image_size.height,
            camera_center,
        ),
        dtype=simple_camera_viewport_dtype,
    )

def get_rays(simple_camera_viewport):
    pixel_points = get_pixel_points(simple_camera_viewport)
    directions = pixel_points.reshape(-1, 3) - simple_camera_viewport['camera_center']
    return build_rays(
        np.full_like(directions, simple_camera_viewport['camera_center']),
        directions
    )
