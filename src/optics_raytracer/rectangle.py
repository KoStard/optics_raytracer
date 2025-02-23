import numpy as np

from optics_raytracer.colored_object import ColoredObject
from .primitives import vector_dtype

rectangle_dtype = np.dtype([
    ('middle_point', *vector_dtype),
    ('normal', *vector_dtype),
    ('width', np.float32),
    ('height', np.float32),
    ('u_vector', *vector_dtype),
])

class Rectangle:
    """
    Wrapper class for rectangle_dtype numpy arrays with helper methods.
    """
    def __init__(self, rectangle_array: np.ndarray):
        if rectangle_array.dtype != rectangle_dtype:
            raise ValueError(f"Input array must have dtype {rectangle_dtype}")
        self.array = rectangle_array

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

    @staticmethod
    def build(
        middle_point: np.ndarray,
        normal: np.ndarray,
        width: float,
        height: float,
        u_vector: np.ndarray
    ) -> 'Rectangle':
        """
        Create a new Rectangle instance.
        
        Args:
            middle_point: Center point of the rectangle
            normal: Normal vector of the rectangle's plane
            width: Width of the rectangle
            height: Height of the rectangle
            u_vector: U vector defining the rectangle's horizontal axis
            
        Returns:
            New Rectangle instance
        """
        normal = normal / np.linalg.norm(normal)  # Normalize
        return Rectangle(np.array(
            (middle_point, normal, width, height, u_vector),
            dtype=rectangle_dtype
        ))
        
    @staticmethod
    def get_hits_mask(rectangle_array: np.ndarray, points_array: np.ndarray) -> np.ndarray:
        """
        Check which points lie within the rectangle.
        
        Args:
            rectangle_array: Rectangle numpy array with middle_point, normal, width, height and u_vector
            points_array: Array of points to check (Nx3)
            
        Returns:
            Boolean mask array indicating which points are inside the rectangle
        """
        middle_to_point_vector_array = points_array - rectangle_array['middle_point']

        # Get u and v projections
        u = rectangle_array['u_vector'][:, np.newaxis]
        v = np.cross(rectangle_array['normal'], rectangle_array['u_vector'])[:, np.newaxis]
        u_projection_vectors = np.matmul(np.matmul(u, u.T) / np.matmul(u.T, u), middle_to_point_vector_array.T).T
        v_projection_vectors = np.matmul(np.matmul(v, v.T) / np.matmul(v.T, v), middle_to_point_vector_array.T).T

        return np.logical_and(
            np.linalg.norm(u_projection_vectors, axis=1) <= rectangle_array['width'] / 2,
            np.linalg.norm(v_projection_vectors, axis=1) <= rectangle_array['height'] / 2
        )


class ColoredRectangle(ColoredObject):
    """
    A rectangle that can return colors for points that hit its surface.
    """
    def __init__(self, rectangle: Rectangle, color: np.ndarray):
        """
        Create a new ColoredRectangle.
        
        Args:
            rectangle: The rectangle geometry
            color: RGB color (3-element array) with values between 0 and 1
        """
        self.rectangle = rectangle
        self.color = color

    def get_colors(self, points: np.ndarray) -> np.ndarray:
        """
        Get colors for an array of points on its surface.
        
        Args:
            points: Array of points (Nx3)
            
        Returns:
            Array of colors (Nx3) in RGB format with values between 0 and 1
            Points that don't hit the rectangle will have color [0,0,0]
        """
        # Create empty array of black colors
        colors = np.zeros_like(points)
        
        # Set color for hit points
        colors[:] = self.color
        
        return colors
