from abc import ABC, abstractmethod
import numpy as np

from optics_raytracer.export_3d import Exporter3D
from optics_raytracer.lens import Lens
from optics_raytracer.surface import get_surface_hit_ts, get_surface_hit_ts_mask

from .pixelated_viewport import get_pixel_points, pixelated_viewport_dtype
from .primitives import vector_dtype
from .size import FloatSize, IntegerSize
from .ray import build_rays, get_ray_points_array_at_t_array

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

simple_camera_viewport_dtype = np.dtype(
    [
        *pixelated_viewport_dtype.descr,
        ("camera_center", *vector_dtype),
    ]
)

class SimpleCamera(Camera):
    """
    Wrapper class for simple_camera_viewport_dtype numpy arrays with helper methods.
    """
    def __init__(self, camera_array: np.ndarray):
        if camera_array.dtype != simple_camera_viewport_dtype:
            raise ValueError(f"Input array must have dtype {simple_camera_viewport_dtype}")
        self.array = camera_array

    @property
    def pixel_columns(self) -> int:
        return self.array['pixel_columns']

    @property
    def pixel_rows(self) -> int:
        return self.array['pixel_rows']
    
    @property
    def camera_center(self) -> np.ndarray:
        return self.array['camera_center']

    @staticmethod
    def build(
        camera_center: np.ndarray,
        focal_distance: float,
        viewport_size: FloatSize,
        image_size: IntegerSize,
        viewport_u_vector: np.ndarray,
        viewport_normal: np.ndarray,
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
        viewport_normal = viewport_normal / np.linalg.norm(viewport_normal)
        viewport_center = camera_center + focal_distance * viewport_normal
        camera_array = np.array(
            (
                viewport_center,
                viewport_normal,
                viewport_size.width,
                viewport_size.height,
                viewport_u_vector,
                image_size.width,
                image_size.height,
                camera_center,
            ),
            dtype=simple_camera_viewport_dtype,
        )
        return SimpleCamera(camera_array)
    
    def get_output_image_initial_colors(self):
        """
        Get the initial colors for the output image.

        Returns:
            Array of colors (Nx3)
        """
        return np.zeros((self.pixel_rows * self.pixel_columns, 3))

    def get_rays(self, exporter: Exporter3D, ray_sampling_rate_for_3d_export: float):
        """
        Generate rays from the camera through each pixel and visualize in 3D.
        
        Args:
            exporter: 3D exporter instance
            ray_sampling_rate_for_3d_export: Fraction of rays to include in visualization
            
        Returns:
            Array of rays (ray_dtype)
        """
        # Get pixel points and directions
        pixel_points = get_pixel_points(self.array)
        directions = pixel_points.reshape(-1, 3) - self.camera_center
        directions = directions / np.linalg.norm(directions, axis=1, keepdims=True)
        
        # Build rays
        rays = build_rays(
            np.full_like(directions, self.camera_center),
            directions
        )
        
        # Add viewport rectangle to 3D visualization
        exporter.add_rectangle(self.array)
        
        return rays
    
    def convert_ray_colors_to_pixel_colors(self, colors):
        # Returning as is, as one ray is for one pixel here
        return colors
    
    def get_image_size(self):
        return IntegerSize(self.array['pixel_columns'], self.array['pixel_rows'])

eye_camera_viewport_dtype = np.dtype(
    [
        *pixelated_viewport_dtype.descr,
        ("lens_distance", np.float32),
        ("lens_radius", np.float32),
        ("number_of_circles", np.int32),
        ("rays_per_circle", np.int32),
    ]
)

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
    def __init__(self, camera_array: np.ndarray, lens: Lens):
        if camera_array.dtype != eye_camera_viewport_dtype:
            raise ValueError(f"Input array must have dtype {eye_camera_viewport_dtype}")
        self.array = camera_array
        self.lens = lens

    @staticmethod
    def build(
        viewport_center: np.ndarray,
        lens_distance: float,
        lens_radius: float,
        number_of_circles: int,
        rays_per_circle: int,
        viewport_size: FloatSize,
        image_size: IntegerSize,
        viewport_u_vector: np.ndarray,
        viewport_normal: np.ndarray,
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
        viewport_normal = viewport_normal / np.linalg.norm(viewport_normal)
        camera_array = np.array(
            (
                viewport_center,
                viewport_normal,
                viewport_size.width,
                viewport_size.height,
                viewport_u_vector,
                image_size.width,
                image_size.height,
                lens_distance,
                lens_radius,
                number_of_circles,
                rays_per_circle,
            ),
            dtype=eye_camera_viewport_dtype,
        )
        # Create the lens
        lens_center = viewport_center + lens_distance * viewport_normal
        lens = Lens.build(
            center=lens_center,
            radius=lens_radius,
            normal=viewport_normal,
            focal_distance=lens_focal_distance
        )
        
        return EyeCamera(camera_array, lens)
    
    @property
    def viewport_center(self) -> np.ndarray:
        return self.array['middle_point']
    
    @property
    def pixel_columns(self) -> int:
        return self.array['pixel_columns']

    @property
    def pixel_rows(self) -> int:
        return self.array['pixel_rows']
    
    def get_output_image_initial_colors(self):
        """
        Get the initial colors for the output image.

        Returns:
            Array of colors (Nx3)
        """
        return np.zeros((self.pixel_rows * self.pixel_columns, 3))

    def get_rays(self, exporter: Exporter3D, ray_sampling_rate_for_3d_export: float):
        """
        Generate multiple rays per pixel that distribute across the lens surface and visualize in 3D.
        
        Args:
            exporter: 3D exporter instance
            ray_sampling_rate_for_3d_export: Fraction of rays to include in visualization
            
        Returns:
            Array of rays (ray_dtype) where each pixel has number_of_circles * rays_per_circle rays
        """
        # Add viewport and lens to 3D visualization
        exporter.add_rectangle(self.array)
        exporter.add_circle(self.lens.array)
        # Get pixel points on the viewport
        pixel_points = get_pixel_points(self.array)
        pixel_points = pixel_points.reshape(-1, 3)
        
        # Calculate lens center position
        lens_center = self.viewport_center + self.array['lens_distance'] * self.array['normal']
        
        # Generate circles on the lens
        num_circles = self.array['number_of_circles']
        rays_per_circle = self.array['rays_per_circle']
        lens_radius = self.array['lens_radius']
        
        # Generate points on each circle
        all_lens_points = []
        for circle_idx in range(num_circles):
            # Calculate radius for this circle
            r = lens_radius * (circle_idx + 1) / num_circles
            
            # Generate equally spaced points on this circle
            angles = np.linspace(0, 2 * np.pi, rays_per_circle, endpoint=False)
            circle_points = np.zeros((rays_per_circle, 3))
            circle_points[:, 0] = r * np.cos(angles)
            circle_points[:, 1] = r * np.sin(angles)
            
            # Transform points to lens plane
            u = self.array['u_vector']
            v = np.cross(self.array['normal'], u)
            transform = np.column_stack([u, v, self.array['normal']])
            circle_points = lens_center + np.dot(circle_points, transform.T)
            
            all_lens_points.append(circle_points)
        
        # Flatten all lens points
        all_lens_points = np.concatenate(all_lens_points)
        
        # Create rays from each pixel to each lens point
        origins = np.repeat(pixel_points, len(all_lens_points), axis=0)
        directions = np.tile(all_lens_points, (len(pixel_points), 1)) - origins
        directions = directions / np.linalg.norm(directions, axis=1)[:, np.newaxis]
        
        
        # Create initial rays to lens
        rays_to_lens = build_rays(origins, directions)
        
        # Calculate hit points on lens
        lens_ts = get_surface_hit_ts(rays_to_lens, self.lens.center, self.lens.normal)
        hit_mask = get_surface_hit_ts_mask(lens_ts)
        hit_points = get_ray_points_array_at_t_array(rays_to_lens[hit_mask], lens_ts[hit_mask])
        
        # Get refracted rays through lens
        refracted_rays = self.lens.get_new_rays(rays_to_lens[hit_mask], hit_points)
        
        # Sample rays for visualization
        tracing_mask = (np.random.rand(len(hit_points)) <= ray_sampling_rate_for_3d_export)
        for ray, hit_point in zip(rays_to_lens[hit_mask][tracing_mask], hit_points[tracing_mask]):
            exporter.add_line(ray['origin'], hit_point, group="camera_rays")
            exporter.add_point(hit_point, group="lens_hits")
            
        return refracted_rays

    def get_image_size(self):
        return IntegerSize(self.array['pixel_columns'], self.array['pixel_rows'])

    def convert_ray_colors_to_pixel_colors(self, colors):
        """
        Convert the colors of the rays to the colors of the pixels.

        Args:
            colors: Array of colors (Nx3) for the rays

        Returns:
            Array of colors (Nx3) for the pixels
        """
        # Average the colors for each pixel
        pixel_colors = colors.reshape(self.pixel_rows * self.pixel_columns, self.array['number_of_circles'] * self.array['rays_per_circle'], 3).mean(axis=1)
        return pixel_colors
