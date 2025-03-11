from abc import ABC, abstractmethod
import torch

class ColoredObject(ABC):
    """
    Abstract base class for objects that can return colors for given points.
    """
    @abstractmethod
    def get_colors(self, points: torch.Tensor) -> torch.Tensor:
        """
        Get colors for an array of points on its surface.
        
        Args:
            points: Array of points (Nx3)
            
        Returns:
            Array of colors (Nx3) in RGB format with values between 0 and 1
        """
        pass
