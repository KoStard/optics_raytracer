import torch
from optics_raytracer.colored_object import ColoredObject

class Rectangle:
    def __init__(self, rectangle_data: dict):
        self.rectangle_data = rectangle_data

    @property
    def middle_point(self) -> torch.Tensor:
        return self.rectangle_data['middle_point']

    @property
    def normal(self) -> torch.Tensor:
        return self.rectangle_data['normal']

    @property
    def width(self) -> float:
        return self.rectangle_data['width']

    @property
    def height(self) -> float:
        return self.rectangle_data['height']

    @property
    def u_vector(self) -> torch.Tensor:
        return self.rectangle_data['u_vector']

    @staticmethod
    def build(
        middle_point: torch.Tensor,
        normal: torch.Tensor,
        width: float,
        height: float,
        u_vector: torch.Tensor
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
        normal = normal / torch.linalg.norm(normal)  # Normalize
        return Rectangle(
            {
                "middle_point": middle_point,
                "normal": normal,
                "width": width,
                "height": height,
                "u_vector": u_vector,
            }
        )
        
    @staticmethod
    def get_hits_mask(rectangle_array: torch.Tensor, points_array: torch.Tensor) -> torch.Tensor:
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
        u = rectangle_array['u_vector'][:, torch.newaxis]
        v = torch.linalg.cross(rectangle_array['normal'], rectangle_array['u_vector'])[:, torch.newaxis]
        u_projection_vectors = torch.matmul(torch.matmul(u, u.T) / torch.matmul(u.T, u), middle_to_point_vector_array.T).T
        v_projection_vectors = torch.matmul(torch.matmul(v, v.T) / torch.matmul(v.T, v), middle_to_point_vector_array.T).T

        return torch.logical_and(
            torch.linalg.norm(u_projection_vectors, axis=1) <= rectangle_array['width'] / 2,
            torch.linalg.norm(v_projection_vectors, axis=1) <= rectangle_array['height'] / 2
        )


class ColoredRectangle(ColoredObject):
    """
    A rectangle that can return colors for points that hit its surface.
    """
    def __init__(self, rectangle: Rectangle, color: torch.Tensor):
        """
        Create a new ColoredRectangle.
        
        Args:
            rectangle: The rectangle geometry
            color: RGB color (3-element array) with values between 0 and 1
        """
        self.rectangle = rectangle
        self.color = color

    def get_colors(self, points: torch.Tensor) -> torch.Tensor:
        """
        Get colors for an array of points on its surface.
        
        Args:
            points: Array of points (Nx3)
            
        Returns:
            Array of colors (Nx3) in RGB format with values between 0 and 1
            Points that don't hit the rectangle will have color [0,0,0]
        """
        # Create empty array of black colors
        colors = torch.zeros_like(points)
        
        # Set color for hit points
        colors[:] = self.color
        
        return colors
