from typing import List
from optics_raytracer.camera.camera import Camera
from optics_raytracer.optics.colored_object import ColoredObject
from optics_raytracer.optics.lens import Lens
from optics_raytracer.rendering.color_tracer import ColorTracer
from optics_raytracer.rendering.export_3d import Exporter3D
from optics_raytracer.rendering.image_saver import ImageSaver


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
        ray_sampling_rate_for_3d_export: float = 0.01,
        compare_with_without_lenses: bool = False,
        include_missed_rays: bool = False,
    ):
        """
        Initialize the ray tracing engine.

        Args:
            camera: Camera configuration
            objects: List of colored objects in the scene
            lenses: List of lenses in the scene
            ray_sampling_rate_for_3d_export: Fraction of rays to include in 3D export
            compare_with_without_lenses: If True, render scene with and without lenses side by side
        """
        self.camera = camera
        self.objects = objects
        self.lenses = lenses
        self.ray_sampling_rate = ray_sampling_rate_for_3d_export
        self.compare_with_without_lenses = compare_with_without_lenses
        self.include_missed_rays = include_missed_rays
        self.exporter = Exporter3D()

    def render(
        self,
        output_image_path: str = None,
        output_3d_path: str = None,
        output_mtl_path: str = None,
    ):
        """
        Render the scene and optionally save outputs.

        Args:
            output_image_path: Path to save rendered image (optional)
            output_3d_path: Path to save 3D scene visualization (optional)
            output_mtl_path: Path to save material definition (optional)
        """
        if not self.compare_with_without_lenses:
            # Normal rendering
            return self._render_single(output_image_path, output_3d_path, output_mtl_path)
        
        # Render with lenses first
        with_lenses_image = self._render_single(None, output_3d_path, output_mtl_path)
        
        # Render without lenses
        original_lenses = self.lenses
        self.lenses = []  # Remove lenses
        without_lenses_image = self._render_single(None, None, None)
        self.lenses = original_lenses  # Restore lenses
        
        # Combine images side by side
        combined_image = self._combine_images_side_by_side(without_lenses_image, with_lenses_image)
        
        # Save combined image
        if output_image_path:
            combined_image.save(output_image_path)
        
        return combined_image
    
    def _render_single(
        self,
        output_image_path: str = None,
        output_3d_path: str = None,
        output_mtl_path: str = None,
    ):
        """
        Internal method to render a single scene.
        
        Args:
            output_image_path: Path to save rendered image (optional)
            output_3d_path: Path to save 3D scene visualization (optional)
            output_mtl_path: Path to save material definition (optional)
            
        Returns:
            PIL Image object of the rendered scene
        """
        # Initialize color tracer
        color_tracer = ColorTracer(
            self.exporter,
            self.objects,
            self.lenses,
            ray_sampling_rate_for_3d_export=self.ray_sampling_rate,
            include_missed_rays=self.include_missed_rays,
        )

        # Get rays from camera
        rays = self.camera.get_rays(self.exporter, self.ray_sampling_rate)

        # Create image saver
        image_size = self.camera.get_image_size()
        image_saver = ImageSaver(image_size.width, image_size.height)

        # Trace colors for all rays
        colors = color_tracer.get_colors(rays)
        pixel_colors = self.camera.convert_ray_colors_to_pixel_colors(colors)
        pixel_colors *= 255  # Convert to 8-bit RGB values
        image_saver.write_pixels(
            pixel_colors.reshape(image_size.height, image_size.width, 3)
        )

        # Save outputs if requested
        if output_image_path:
            image_saver.save(output_image_path)

        if output_3d_path:
            self.exporter.save_to_obj(output_3d_path, output_mtl_path)

        return image_saver.image
    
    def _combine_images_side_by_side(self, image1, image2):
        """
        Combine two images side by side.
        
        Args:
            image1: Left image (PIL Image) - without lenses
            image2: Right image (PIL Image) - with lenses
            
        Returns:
            Combined image (PIL Image)
        """
        # Check that images have the same height
        if image1.height != image2.height:
            raise ValueError("Images must have the same height for side-by-side comparison")
        
        # Create a new image twice as wide
        from PIL import Image
        combined = Image.new('RGB', (image1.width + image2.width, image1.height))
        
        # Paste the images side by side
        combined.paste(image1, (0, 0))
        combined.paste(image2, (image1.width, 0))
        
        return combined
