import torch
from .torch_details import device
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
        middle_point: torch.Tensor,
        normal: torch.Tensor,
        u_vector: torch.Tensor
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

    def get_colors(self, points: torch.Tensor) -> torch.Tensor:
        """
        Get colors for an array of points on its surface (assumes they are on the surface).
        
        Args:
            points: Array of points (Nx3)
            
        Returns:
            Array of colors (Nx3) in RGB format with values between 0 and 1
            Points that don't hit the image will have color [0,0,0]
        """
        # Create empty array of black colors
        colors = torch.zeros_like(points)

        # Get vectors from center to points
        center_to_points = points - self.rectangle.middle_point
        
        # Get u and v components
        u = self.rectangle.u_vector
        # Making negative, as y in image is supposed to be pointing "down"
        v = -torch.linalg.cross(self.rectangle.normal, u)
        
        u = u / torch.linalg.norm(u)
        v = v / torch.linalg.norm(v)
        
        # Calculate image coordinates (0-1 range)
        # TODO: Check if this is correct
        u_coords = torch.matmul(center_to_points, u.reshape(-1, 1)) / self.width + 0.5
        v_coords = torch.matmul(center_to_points, v.reshape(-1, 1)) / self.height + 0.5
        
        # Convert to pixel coordinates
        img_width, img_height = self.image.size
        x = torch.clip((u_coords * img_width).to(torch.int), 0, img_width - 1)
        y = torch.clip((v_coords * img_height).to(torch.int), 0, img_height - 1)
        
        # Get colors from image
        for i, (xi, yi) in enumerate(zip(x, y)):
            colors[i] = torch.tensor(self.image.getpixel((xi, yi))).to(device) / 255.0
                
        return colors
