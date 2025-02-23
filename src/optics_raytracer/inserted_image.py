import numpy as np
from PIL import Image
from .colored_object import ColoredObject
from .rectangle import Rectangle

class InsertedImage(ColoredObject):
    """
    A rectangular image that can be inserted into the scene and return colors for points that hit its surface.
    """
    def __init__(
        self, 
        image_path: str, 
        width: float, 
        height: float,
        middle_point: np.ndarray,
        normal: np.ndarray,
        u_vector: np.ndarray
    ):
        """
        Create a new InsertedImage.
        
        Args:
            image_path: Path to the image file
            width: Width of the image in the scene
            height: Height of the image in the scene
            middle_point: Center point of the image in 3D space
            normal: Normal vector of the image plane
            u_vector: Vector defining the horizontal axis of the image
        """
        # Load and convert image to RGB
        self.image = Image.open(image_path).convert('RGB')
        self.width = width
        self.height = height
        
        # Create a rectangle to represent the image plane
        self.rectangle = Rectangle.build(
            middle_point=middle_point,
            normal=normal,
            width=width,
            height=height,
            u_vector=u_vector
        )

    def get_colors(self, points: np.ndarray) -> np.ndarray:
        """
        Get colors for an array of points on its surface (assumes they are on the surface).
        
        Args:
            points: Array of points (Nx3)
            
        Returns:
            Array of colors (Nx3) in RGB format with values between 0 and 1
            Points that don't hit the image will have color [0,0,0]
        """
        # Create empty array of black colors
        colors = np.zeros_like(points)

        # Get vectors from center to points
        center_to_points = points - self.rectangle.middle_point
        
        # Get u and v components
        u = self.rectangle.u_vector
        v = np.cross(self.rectangle.normal, u)
        
        # Calculate image coordinates (0-1 range)
        u_coords = np.dot(center_to_points, u) / self.width + 0.5
        v_coords = np.dot(center_to_points, v) / self.height + 0.5
        
        # Convert to pixel coordinates
        img_width, img_height = self.image.size
        x = np.clip((u_coords * img_width).astype(int), 0, img_width - 1)
        y = np.clip((v_coords * img_height).astype(int), 0, img_height - 1)
        
        # Get colors from image
        for i, (xi, yi) in enumerate(zip(x, y)):
            colors[i] = np.array(self.image.getpixel((xi, yi))) / 255.0
                
        return colors
