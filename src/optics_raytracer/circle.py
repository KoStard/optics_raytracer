import numpy as np

from optics_raytracer.colored_object import ColoredObject
from .primitives import vector_dtype

circle_dtype = np.dtype(
    [
        ("center", *vector_dtype),  # Center point of the circle
        ("normal", *vector_dtype),  # Normal vector of the circle's plane
        ("radius", np.float32),  # Radius of the circle
    ]
)


class Circle:
    """
    Wrapper class for circle_dtype numpy arrays with helper methods.
    """

    def __init__(self, circle_array: np.ndarray):
        if circle_array.dtype != circle_dtype:
            raise ValueError(f"Input array must have dtype {circle_dtype}")
        self.array = circle_array

    @property
    def center(self) -> np.ndarray:
        return self.array["center"]

    @property
    def normal(self) -> np.ndarray:
        return self.array["normal"]

    @property
    def radius(self) -> float:
        return self.array["radius"]

    @staticmethod
    def build(center: np.ndarray, radius: float, normal: np.ndarray) -> "Circle":
        """
        Create a new Circle instance.

        Args:
            center: 3D center point of the circle
            radius: Radius of the circle
            normal: Normal vector of the circle's plane

        Returns:
            New Circle instance
        """
        normal = normal / np.linalg.norm(normal)  # Normalize
        return Circle(np.array((center, normal, radius), dtype=circle_dtype))

    @staticmethod
    def get_hits_mask(circle_array: np.ndarray, points_array: np.ndarray) -> np.ndarray:
        """
        Check which points lie within the circle. Assumes that it's already in the plane.

        Args:
            circle_array: Circle numpy array with center, normal and radius
            points_array: Array of points to check (Nx3)

        Returns:
            Boolean mask array indicating which points are inside the circle
        """
        # Vector from center to each point
        center_to_point = points_array - circle_array["center"]

        # Then check if points are within radius
        within_radius = (
            np.linalg.norm(center_to_point, axis=1) <= circle_array["radius"]
        )

        return within_radius


class ColoredCircle(ColoredObject):
    """
    A circle that can return colors for points that hit its surface.
    """

    def __init__(self, circle: Circle, color: np.ndarray):
        """
        Create a new ColoredCircle.

        Args:
            circle: The circle geometry
            color: RGB color (3-element array) with values between 0 and 1
        """
        self.circle = circle
        self.color = color

    def get_colors(self, points: np.ndarray) -> np.ndarray:
        """
        Get colors for an array of points on its surface.

        Args:
            points: Array of points (Nx3)

        Returns:
            Array of colors (Nx3) in RGB format with values between 0 and 1
            Points that don't hit the circle will have color [0,0,0]
        """
        # Create empty array of black colors
        colors = np.zeros_like(points)

        # Get mask of points that hit the circle
        hits_mask = self.circle.get_hits_mask(self.circle.array, points)

        # Set color for hit points
        colors[hits_mask] = self.color

        return colors
