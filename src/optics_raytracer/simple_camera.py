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

class Camera:
    """
    Wrapper class for simple_camera_viewport_dtype numpy arrays with helper methods.
    """
    def __init__(self, camera_array: np.ndarray):
        if camera_array.dtype != simple_camera_viewport_dtype:
            raise ValueError(f"Input array must have dtype {simple_camera_viewport_dtype}")
        self.array = camera_array

    @property
    def middle_point(self) -> np.ndarray:
        return self.array['middle_point']

    @property
    def normal(self) -> np.ndarray:
        return self.array['normal']

    @property
    def width(self) -> float:
        return self.array['width']

    @property
    def height(self) -> float:
        return self.array['height']

    @property
    def u_vector(self) -> np.ndarray:
        return self.array['u_vector']

    @property
    def pixel_columns(self) -> int:
        return self.array['pixel_columns']

    @property
    def pixel_rows(self) -> int:
        return self.array['pixel_rows']

    @property
    def camera_center(self) -> np.ndarray:
        return self.array['camera_center']

    @staticmethod
    def build(
        camera_center: np.ndarray,
        focal_distance: float,
        viewport_size: FloatSize,
        image_size: IntegerSize,
        viewport_u_vector: np.ndarray,
        viewport_normal: np.ndarray,
    ) -> 'Camera':
        """
        Create a new Camera instance.
        
        Args:
            camera_center: Center point of the camera
            focal_distance: Distance from camera to viewport
            viewport_size: Size of the viewport
            image_size: Size of the output image
            viewport_u_vector: U vector defining the viewport's horizontal axis
            viewport_normal: Normal vector of the viewport plane
            
        Returns:
            New Camera instance
        """
        viewport_normal = viewport_normal / np.linalg.norm(viewport_normal)
        viewport_center = camera_center + focal_distance * viewport_normal
        camera_array = np.array(
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
        return Camera(camera_array)
    
    def get_output_image_initial_colors(self):
        """
        Get the initial colors for the output image.

        Returns:
            Array of colors (Nx3)
        """
        return np.zeros((self.pixel_rows * self.pixel_columns, 3))

    def get_rays(self):
        """
        Generate rays from the camera through each pixel.
        
        Returns:
            Array of rays (ray_dtype)
        """
        pixel_points = get_pixel_points(self.array)
        directions = pixel_points.reshape(-1, 3) - self.camera_center
        return build_rays(
            np.full_like(directions, self.camera_center),
            directions
        )
