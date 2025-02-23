from typing import List
import numpy as np
from .camera import Camera
from .colored_object import ColoredObject
from .lens import Lens
from .color_tracer import ColorTracer
from .export_3d import Exporter3D
from .image_saver import ImageSaver

class OpticsRayTracingEngine:
    """
    Main engine for ray tracing optical systems.
    Handles scene setup, rendering, and output generation.
    """
    def __init__(
        self,
        camera: Camera,
        objects: List[ColoredObject],
        lenses: List[Lens],
        ray_sampling_rate_for_3d_export: float = 0.01
    ):
        """
        Initialize the ray tracing engine.
        
        Args:
            camera: Camera configuration
            objects: List of colored objects in the scene
            lenses: List of lenses in the scene
            ray_sampling_rate_for_3d_export: Fraction of rays to include in 3D export
        """
        self.camera = camera
        self.objects = objects
        self.lenses = lenses
        self.ray_sampling_rate = ray_sampling_rate_for_3d_export
        self.exporter = Exporter3D()

    def render(self, output_image_path: str = None, output_3d_path: str = None):
        """
        Render the scene and optionally save outputs.
        
        Args:
            output_image_path: Path to save rendered image (optional)
            output_3d_path: Path to save 3D scene visualization (optional)
        """
        # Initialize color tracer
        color_tracer = ColorTracer(
            self.exporter,
            self.objects,
            self.lenses,
            ray_sampling_rate_for_3d_export=self.ray_sampling_rate
        )

        # Get rays from camera
        rays = self.camera.get_rays(self.exporter, self.ray_sampling_rate)
        
        # Create image saver
        image_size = self.camera.get_image_size()
        image_saver = ImageSaver(image_size.width, image_size.height)
        
        # Trace colors for all rays
        colors = color_tracer.get_colors(rays)
        pixel_colors = self.camera.convert_ray_colors_to_pixel_colors(colors)
        for color in pixel_colors:
            image_saver.add_pixel(color)
        
        # Save outputs if requested
        if output_image_path:
            image_saver.save(output_image_path)
            
        if output_3d_path:
            self.exporter.save_to_obj(output_3d_path)
            
        return image_saver.image
