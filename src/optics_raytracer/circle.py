import torch
from optics_raytracer.colored_object import ColoredObject


class Circle:
    def __init__(self, circle_data: dict):
        self.circle_data = circle_data

    @property
    def center(self) -> torch.Tensor:
        return self.circle_data['center']

    @property
    def normal(self) -> torch.Tensor:
        return self.circle_data['normal']

    @property
    def radius(self) -> float:
        return self.circle_data['radius']

    @staticmethod
    def build(center: torch.Tensor, radius: float, normal: torch.Tensor) -> 'Circle':
        """
        Create a new Circle instance.
        
        Args:
            center: 3D center point of the circle
            radius: Radius of the circle
            normal: Normal vector of the circle's plane
            
        Returns:
            New Circle instance
        """
        normal = normal / torch.linalg.norm(normal)  # Normalize
        return Circle({
            'center': center, 
            'normal': normal, 
            'radius': radius
        })

    @staticmethod
    def get_hits_mask(circle_data: dict, points_array: torch.Tensor) -> torch.Tensor:
        """
        Check which points lie within the circle. Assumes that it's already in the plane.
        
        Args:
            circle_data: Circle numpy array with center, normal and radius
            points_array: Array of points to check (Nx3)
            
        Returns:
            Boolean mask array indicating which points are inside the circle
        """
        # Vector from center to each point
        center_to_point = points_array - circle_data['center']
        
        # Then check if points are within radius
        within_radius = torch.linalg.norm(center_to_point, axis=1) <= circle_data['radius']
        
        return within_radius


class ColoredCircle(ColoredObject):
    """
    A circle that can return colors for points that hit its surface.
    """
    def __init__(self, circle: Circle, color: torch.Tensor):
        """
        Create a new ColoredCircle.
        
        Args:
            circle: The circle geometry
            color: RGB color (3-element array) with values between 0 and 1
        """
        self.circle = circle
        self.color = color

    def get_colors(self, points: torch.Tensor) -> torch.Tensor:
        """
        Get colors for an array of points on its surface.
        
        Args:
            points: Array of points (Nx3)
            
        Returns:
            Array of colors (Nx3) in RGB format with values between 0 and 1
            Points that don't hit the circle will have color [0,0,0]
        """
        # Create empty array of black colors
        colors = torch.zeros_like(points)
        
        # Get mask of points that hit the circle
        hits_mask = self.circle.get_hits_mask(self.circle.circle_data, points)
        
        # Set color for hit points
        colors[hits_mask] = self.color
        
        return colors
