import torch
from optics_raytracer.ray import build_rays


class Lens:
    def __init__(self, lens_data: dict):
        self.lens_data = lens_data
        
    @property
    def center(self) -> torch.Tensor:
        return self.lens_data['center']
    
    @property
    def normal(self) -> torch.Tensor:
        return self.lens_data['normal']
    
    @property
    def focal_distance(self) -> float:
        return self.lens_data['focal_distance']

    @staticmethod
    def build(center: torch.Tensor, radius: float, normal: torch.Tensor, focal_distance: float) -> 'Lens':
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
        normal = normal / torch.linalg.norm(normal)  # Normalize
        return Lens({
            'center': center, 
            'normal': normal, 
            'radius': radius, 
            'focal_distance': focal_distance
        })

    def get_new_rays(self, hitting_rays: torch.Tensor, hit_points: torch.Tensor) -> torch.Tensor:
        """
        Calculate new ray directions after refraction through the lens.
        
        Args:
            hitting_rays: Array of incoming rays
            hit_points: Array of hit points on lens surface (Nx3)
            
        Returns:
            Array of refracted rays
        """
        # Working based on this idea:
        # - parallel rays meet at the focal distance
        # - the ray passing through the center of the lens doesn't change direction
        # - so the ray from the hit point goes to the point where the parallel ray going through the center of the lens would hit the focal plane
        # - if we make a vector from the point where the original ray would hit the focal plane if it didn't change direction, we'll see that this vector is exactly and always self.center - hit_point
        # - the rest is just getting the vector from hit_point to the point where the original ray would hit the focal plane, adding the self.center - hit_point vector, and we have the new direction
        # - then we need to normalize it
        # - we also swap for cases when the normal is in the direction of the ray origin
        normal_away_from_origin = torch.matmul(hitting_rays['direction'], self.normal) > 0
        scale = self.focal_distance / torch.matmul(hitting_rays['direction'], self.normal)
        new_directions = hitting_rays['direction'] * scale[:, torch.newaxis] + (self.center - hit_points)
        # The issue arises here
        new_directions = new_directions / torch.linalg.norm(new_directions, axis=1, keepdims=True)
        new_directions[~normal_away_from_origin] *= -1
        if self.focal_distance < 0:
            new_directions *= -1
        return build_rays(hit_points, new_directions)
