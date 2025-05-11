import numpy as np

from optics_raytracer.core.ray import build_rays
from optics_raytracer.geometry.circle import circle_dtype

lens_dtype = np.dtype(
    [
        *circle_dtype.descr,  # Inherit circle fields
        ("focal_distance", np.float32),  # Focal distance of the lens
    ]
)


class Lens:
    """
    Wrapper class for lens_dtype numpy arrays with helper methods.
    """

    def __init__(self, lens_array: np.ndarray):
        if lens_array.dtype != lens_dtype:
            raise ValueError(f"Input array must have dtype {lens_dtype}")
        self.array = lens_array

    @property
    def center(self) -> np.ndarray:
        return self.array["center"]

    @property
    def normal(self) -> np.ndarray:
        return self.array["normal"]

    @property
    def focal_distance(self) -> float:
        return self.array["focal_distance"]

    @staticmethod
    def build(
        center: np.ndarray, radius: float, normal: np.ndarray, focal_distance: float
    ) -> "Lens":
        """
        Create a new Lens instance.

        Args:
            center: 3D center point of the lens
            radius: Radius of the lens
            normal: Normal vector of the lens surface
            focal_distance: Focal distance of the lens

        Returns:
            New Lens instance
        """
        normal = normal / np.linalg.norm(normal)  # Normalize
        return Lens(
            np.array((center, normal, radius, focal_distance), dtype=lens_dtype)
        )

    def get_new_rays(
        self, hitting_rays: np.ndarray, hit_points: np.ndarray
    ) -> np.ndarray:
        """
        Calculate new ray directions after refraction through the lens.

        Args:
            hitting_rays: Array of incoming rays (ray_dtype)
            hit_points: Array of hit points on lens surface (Nx3)

        Returns:
            Array of refracted rays (ray_dtype)
        """
        # Working based on this idea:
        # - parallel rays meet at the focal distance
        # - the ray passing through the center of the lens doesn't change direction
        # - so the ray from the hit point goes to the point where the parallel ray going through the center of the lens would hit the focal plane
        # - if we make a vector from the point where the original ray would hit the focal plane if it didn't change direction, we'll see that this vector is exactly and always self.center - hit_point
        # - the rest is just getting the vector from hit_point to the point where the original ray would hit the focal plane, adding the self.center - hit_point vector, and we have the new direction
        # - then we need to normalize it
        # - we also swap for cases when the normal is in the direction of the ray origin
        normal_away_from_origin = np.matvec(hitting_rays["direction"], self.normal) > 0
        scale = self.focal_distance / np.matvec(hitting_rays["direction"], self.normal)
        new_directions = hitting_rays["direction"] * scale[:, np.newaxis] + (
            self.center - hit_points
        )
        # The issue arises here
        new_directions = new_directions / np.linalg.norm(
            new_directions, axis=1, keepdims=True
        )
        new_directions[~normal_away_from_origin] *= -1
        if self.focal_distance < 0:
            new_directions *= -1
        return build_rays(hit_points, new_directions)
