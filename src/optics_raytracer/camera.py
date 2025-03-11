from abc import ABC, abstractmethod
import torch

from optics_raytracer.export_3d import Exporter3D
from optics_raytracer.lens import Lens
from optics_raytracer.surface import get_surface_hit_ts, get_surface_hit_ts_mask

from .pixelated_viewport import get_pixel_points
from .size import FloatSize, IntegerSize
from .ray import build_rays, get_ray_points_array_at_t_array
from .torch_details import device

class Camera(ABC):
    @abstractmethod
    def get_output_image_initial_colors(self):
        pass
    
    @abstractmethod
    def get_rays(self, exporter: Exporter3D, ray_sampling_rate_for_3d_export: float):
        pass
    
    @abstractmethod
    def convert_ray_colors_to_pixel_colors(self, colors):
        pass
    
    @abstractmethod
    def get_image_size(self) -> IntegerSize:
        pass


class SimpleCamera(Camera):
    def __init__(self, camera_data: torch.Tensor):
        self.camera_data = camera_data

    @property
    def pixel_columns(self) -> int:
        return self.camera_data['pixel_columns']

    @property
    def pixel_rows(self) -> int:
        return self.camera_data['pixel_rows']
    
    @property
    def camera_center(self) -> torch.Tensor:
        return self.camera_data['camera_center']

    @staticmethod
    def build(
        camera_center: torch.Tensor,
        focal_distance: float,
        viewport_size: FloatSize,
        image_size: IntegerSize,
        viewport_u_vector: torch.Tensor,
        viewport_normal: torch.Tensor,
    ) -> 'Camera':
        """
        Create a new Camera instance.
        
        Args:
            camera_center: Center point of the camera
            focal_distance: Distance from camera to viewport
            viewport_size: Size of the viewport
            image_size: Size of the output image
            viewport_u_vector: U vector defining the viewport's horizontal axis
            viewport_normal: Normal vector of the viewport plane
            
        Returns:
            New Camera instance
        """
        viewport_normal = viewport_normal / torch.linalg.norm(viewport_normal)
        viewport_center = camera_center + focal_distance * viewport_normal
        return SimpleCamera({
            'middle_point': viewport_center,
            'normal': viewport_normal,
            'width': viewport_size.width,
            'height': viewport_size.height,
            'u_vector': viewport_u_vector,
            'pixel_columns': image_size.width,
            'pixel_rows': image_size.height,
            'camera_center': camera_center,
        })
    
    def get_output_image_initial_colors(self):
        """
        Get the initial colors for the output image.

        Returns:
            Array of colors (Nx3)
        """
        return torch.zeros((self.pixel_rows * self.pixel_columns, 3)).to(device)

    def get_rays(self, exporter: Exporter3D, ray_sampling_rate_for_3d_export: float):
        """
        Generate rays from the camera through each pixel and visualize in 3D.
        
        Args:
            exporter: 3D exporter instance
            ray_sampling_rate_for_3d_export: Fraction of rays to include in visualization
            
        Returns:
            dicts for the rays
        """
        # Get pixel points and directions
        pixel_points = get_pixel_points(self.camera_data)
        directions = pixel_points.reshape(-1, 3) - self.camera_center
        directions = directions / torch.linalg.norm(directions, axis=1, keepdims=True)
        
        # Build rays
        rays = build_rays(
            self.camera_center.tile(len(directions), 1),
            directions
        )
        
        # Add viewport rectangle to 3D visualization
        exporter.add_rectangle(self.camera_data)
        
        return rays
    
    def convert_ray_colors_to_pixel_colors(self, colors):
        # Returning as is, as one ray is for one pixel here
        return colors
    
    def get_image_size(self):
        return IntegerSize(self.camera_data['pixel_columns'], self.camera_data['pixel_rows'])


class EyeCamera(Camera):
    """
    Camera that simulates an eye with a lens, generating multiple rays per pixel
    that distribute across the lens surface.
    
    We have the viewport in the back, with the pixels as usual.
    Then we have a lens in the front (like with eye).
    On the lens we have `number_of_circles` virtual circles with radiuses equally breaking the lens radius, with biggest one matching the lens radius.
    Then on each virtual circle, we have `rays_per_circle` virtual points, equally breaking the circle.
    For each pixel in the viewport, we create rays to the each virtual point.
    We run these rays through the lens and return the rays leaving the lens as output of get_rays.
    """
    def __init__(self, camera_data: torch.Tensor, lens: Lens):
        self.camera_data = camera_data
        self.lens = lens

    @staticmethod
    def build(
        viewport_center: torch.Tensor,
        lens_distance: float,
        lens_radius: float,
        number_of_circles: int,
        rays_per_circle: int,
        viewport_size: FloatSize,
        image_size: IntegerSize,
        viewport_u_vector: torch.Tensor,
        viewport_normal: torch.Tensor,
        lens_focal_distance: float,
    ) -> 'EyeCamera':
        """
        Create a new EyeCamera instance.
        
        Args:
            viewport_center: Center point of the viewport
            lens_distance: Distance from viewport to lens
            lens_radius: Radius of the lens
            number_of_circles: Number of concentric circles on lens
            rays_per_circle: Number of rays per circle
            viewport_size: Size of the viewport
            image_size: Size of the output image
            viewport_u_vector: U vector defining the viewport's horizontal axis
            viewport_normal: Normal vector of the viewport plane
            
        Returns:
            New EyeCamera instance
        """
        viewport_normal = viewport_normal / torch.linalg.norm(viewport_normal)
        # Create the lens
        lens_center = viewport_center + lens_distance * viewport_normal
        lens = Lens.build(
            center=lens_center,
            radius=lens_radius,
            normal=viewport_normal,
            focal_distance=lens_focal_distance
        )
        
        return EyeCamera({
            'middle_point': viewport_center,
            'normal': viewport_normal,
            'width': viewport_size.width,
            'height': viewport_size.height,
            'u_vector': viewport_u_vector,
            'pixel_columns': image_size.width,
            'pixel_rows': image_size.height,
            'lens_distance': lens_distance,
            'lens_radius': lens_radius,
            'number_of_circles': number_of_circles,
            'rays_per_circle': rays_per_circle,
        }, lens)
    
    @property
    def viewport_center(self) -> torch.Tensor:
        return self.camera_data['middle_point']
    
    @property
    def pixel_columns(self) -> int:
        return self.camera_data['pixel_columns']

    @property
    def pixel_rows(self) -> int:
        return self.camera_data['pixel_rows']
    
    def get_output_image_initial_colors(self):
        """
        Get the initial colors for the output image.

        Returns:
            Array of colors (Nx3)
        """
        return torch.zeros((self.pixel_rows * self.pixel_columns, 3)).to(device)

    def get_rays(self, exporter: Exporter3D, ray_sampling_rate_for_3d_export: float):
        """
        Generate multiple rays per pixel that distribute across the lens surface and visualize in 3D.
        
        Args:
            exporter: 3D exporter instance
            ray_sampling_rate_for_3d_export: Fraction of rays to include in visualization
            
        Returns:
            Array of rays where each pixel has number_of_circles * rays_per_circle rays
        """
        # Add viewport and lens to 3D visualization
        exporter.add_rectangle(self.camera_data)
        exporter.add_circle(self.lens.lens_data)
        # Get pixel points on the viewport
        pixel_points = get_pixel_points(self.camera_data)
        pixel_points = pixel_points.reshape(-1, 3)
        
        # Calculate lens center position
        lens_center = self.viewport_center + self.camera_data['lens_distance'] * self.camera_data['normal']
        
        # Generate circles on the lens
        num_circles = self.camera_data['number_of_circles']
        rays_per_circle = self.camera_data['rays_per_circle']
        lens_radius = self.camera_data['lens_radius']
        
        # Generate points on each circle
        all_lens_points = []
        for circle_idx in range(num_circles):
            # Calculate radius for this circle
            r = lens_radius * (circle_idx + 1) / num_circles
            
            # Generate equally spaced points on this circle
            angles = torch.linspace(0.0, 2 * torch.pi, rays_per_circle + 1)[:-1]
            circle_points = torch.zeros((rays_per_circle, 3)).to(device)
            circle_points[:, 0] = r * torch.cos(angles)
            circle_points[:, 1] = r * torch.sin(angles)
            
            # Transform points to lens plane
            u = self.camera_data['u_vector']
            v = torch.linalg.cross(self.camera_data['normal'], u)
            transform = torch.column_stack([u, v, self.camera_data['normal']])
            circle_points = lens_center + torch.matmul(circle_points, transform.T)
            
            all_lens_points.append(circle_points)
        
        # Flatten all lens points
        all_lens_points = torch.concatenate(all_lens_points)
        
        # Create rays from each pixel to each lens point
        origins = torch.repeat_interleave(pixel_points, len(all_lens_points), axis=0)
        directions = torch.tile(all_lens_points, (len(pixel_points), 1)) - origins
        directions = directions / torch.linalg.norm(directions, axis=1)[:, torch.newaxis]
        
        
        # Create initial rays to lens
        rays_to_lens = build_rays(origins, directions)
        
        # Calculate hit points on lens
        lens_ts = get_surface_hit_ts(rays_to_lens, self.lens.center, self.lens.normal)
        hit_mask = get_surface_hit_ts_mask(lens_ts)
        hit_rays = build_rays(rays_to_lens['origin'][hit_mask], rays_to_lens['direction'][hit_mask])
        hit_points = get_ray_points_array_at_t_array(hit_rays, lens_ts[hit_mask])
        
        # Get refracted rays through lens
        refracted_rays = self.lens.get_new_rays(hit_rays, hit_points)
        
        # Sample rays for visualization
        tracing_mask = (torch.rand(len(hit_points)) <= ray_sampling_rate_for_3d_export)
        hit_and_tracing_rays = build_rays(hit_rays['origin'][tracing_mask], hit_rays['direction'][tracing_mask])
        for hit_and_tracing_rays_origin, hit_point in zip(hit_and_tracing_rays['origin'], hit_points[tracing_mask]):
            exporter.add_line(hit_and_tracing_rays_origin, hit_point, group="camera_rays")
            exporter.add_point(hit_point, group="lens_hits")
            
        return refracted_rays

    def get_image_size(self):
        return IntegerSize(self.camera_data['pixel_columns'], self.camera_data['pixel_rows'])

    def convert_ray_colors_to_pixel_colors(self, colors):
        """
        Convert the colors of the rays to the colors of the pixels.

        Args:
            colors: Array of colors (Nx3) for the rays

        Returns:
            Array of colors (Nx3) for the pixels
        """
        # Average the colors for each pixel
        pixel_colors = colors.reshape(self.pixel_rows * self.pixel_columns, self.camera_data['number_of_circles'] * self.camera_data['rays_per_circle'], 3).mean(axis=1)
        return pixel_colors
