import torch
from .torch_details import device

def build_pixelated_viewport(
    middle_point: torch.Tensor,
    normal: torch.Tensor,
    width: float,
    height: float,
    u_vector: torch.Tensor,
    pixel_columns: int,
    pixel_rows: int
):
    """
    Create a pixelated viewport numpy structured array.
    
    Args:
        middle_point: Center point of the viewport
        normal: Normal vector of the viewport plane
        width: Total width of the viewport
        height: Total height of the viewport
        u_vector: U vector defining the viewport's horizontal axis
        pixel_columns: Number of pixel columns
        pixel_rows: Number of pixel rows
        
    Returns:
        Numpy structured array representing the pixelated viewport
    """
    normal = normal / torch.linalg.norm(normal)  # Normalize
    return {
        'middle_point': middle_point, 
        'normal': normal, 
        'width': width, 
        'height': height, 
        'u_vector': u_vector, 
        'pixel_columns': pixel_columns, 
        'pixel_rows': pixel_rows
    }

def get_pixel_points(pixelated_viewport):
    """
    Returns height x width matrix of points, where each point is a pixel center.
    """
    u = pixelated_viewport['u_vector'][:, torch.newaxis]
    v = torch.linalg.cross(pixelated_viewport['normal'], pixelated_viewport['u_vector'])[:, torch.newaxis]

    u_step = pixelated_viewport['width'] / (pixelated_viewport['pixel_columns'] - 1) * u
    v_step = pixelated_viewport['height'] / (pixelated_viewport['pixel_rows'] - 1) * v

    u_steps = (torch.arange(pixelated_viewport['pixel_columns']).to(device) * u_step)
    v_steps = (torch.arange(pixelated_viewport['pixel_rows']).to(device) * v_step)

    u_steps = u_steps - u_step * (pixelated_viewport['pixel_columns'] - 1) / 2
    v_steps = v_steps - v_step * (pixelated_viewport['pixel_rows'] - 1) / 2
    
    x = torch.tile(u_steps.T, (pixelated_viewport['pixel_rows'], 1, 1))
    y = torch.tile(v_steps.T[:, torch.newaxis], (1, pixelated_viewport['pixel_columns'], 1))
    
    return pixelated_viewport['middle_point'][torch.newaxis, torch.newaxis, :] + x + y
