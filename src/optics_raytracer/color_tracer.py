import numpy as np
from typing import List

from optics_raytracer.circle import Circle, ColoredCircle
from optics_raytracer.inserted_image import InsertedImage
from optics_raytracer.rectangle import ColoredRectangle
from .ray import get_ray_points_array_at_t_array, ray_dtype
from .colored_object import ColoredObject
from .lens import Lens
from .surface import get_surface_hit_ts, get_surface_hit_ts_mask
from .export_3d import Exporter3D

class ColorTracer:
    """
    Class for tracing ray colors through a scene with colored objects and lenses.
    """
    def __init__(
        self,
        exporter: Exporter3D,
        colored_objects: List[ColoredObject],
        lenses: List[Lens],
        default_color: np.ndarray = np.array([0, 0, 0], dtype=np.float16)
    ):
        """
        Initialize the color tracer.
        
        Args:
            exporter: 3D exporter for visualization
            colored_objects: List of colored objects in the scene
            lenses: List of lenses in the scene
            default_color: Default color for rays that don't hit anything
        """
        self.exporter = exporter
        self.colored_objects = colored_objects
        self.lenses = lenses
        self.default_color = default_color
        
        for obj in colored_objects:
            if isinstance(obj, ColoredCircle):
                self.exporter.add_circle(obj.circle.array, 50)
            elif isinstance(obj, ColoredRectangle):
                self.exporter.add_rectangle(obj.rectangle.array)
            elif isinstance(obj, InsertedImage):
                self.exporter.add_rectangle(obj.rectangle.array)
            else:
                print(f"Unknown object type: {type(obj)}")
        
        for lens in lenses:
            self.exporter.add_circle(lens.array, 50)

    def get_colors(self, rays: np.ndarray) -> np.ndarray:
        """
        Get colors for an array of rays by tracing them through the scene.
        
        Args:
            rays: Array of rays to trace (ray_dtype)
            
        Returns:
            Array of colors (Nx3) in RGB format with values between 0 and 1
        """
        # Initialize output colors with default
        colors = np.tile(self.default_color, (len(rays), 1))
        
        # Find closest hits for all objects
        hit_ts = np.full(len(rays), np.inf)
        object_hit_masks = np.zeros(len(rays), dtype=bool)
        lens_hit_masks = np.zeros(len(rays), dtype=bool)
        hit_object_indices = np.full(len(rays), -1)
        
        # Check colored objects
        for obj_index, obj in enumerate(self.colored_objects):
            if isinstance(obj, ColoredRectangle) or isinstance(obj, InsertedImage):
                surface_point = obj.rectangle.middle_point
                surface_normal = obj.rectangle.normal
                
                # Get hit times and mask
                obj_ts = get_surface_hit_ts(rays, surface_point, surface_normal)
                obj_points = get_ray_points_array_at_t_array(rays, obj_ts)
                obj_mask = get_surface_hit_ts_mask(obj_ts)
                obj_mask &= obj.rectangle.get_hits_mask(obj.rectangle.array, obj_points)
                
            elif isinstance(obj, ColoredCircle):
                surface_point = obj.circle.center
                surface_normal = obj.circle.normal
                
                # Get hit times and mask
                obj_ts = get_surface_hit_ts(rays, surface_point, surface_normal)
                obj_points = get_ray_points_array_at_t_array(rays, obj_ts)
                obj_mask = get_surface_hit_ts_mask(obj_ts)
                obj_mask &= obj.circle.get_hits_mask(obj.circle.array, obj_points)
            else:
                print(f"Unknown object type: {type(obj)}")
                continue
            
            # Update closest hits
            closer_mask = obj_ts < hit_ts
            update_mask = obj_mask & closer_mask
            hit_ts[update_mask] = obj_ts[update_mask]
            object_hit_masks[update_mask] = True
            hit_object_indices[update_mask] = obj_index
            
        # Check lenses
        for lens in self.lenses:
            lens_ts = get_surface_hit_ts(rays, lens.center, lens.normal)
            lens_mask = get_surface_hit_ts_mask(lens_ts)
            lens_mask &= Circle.get_hits_mask(lens.array, rays['origin'])
            
            # Only process rays that hit this lens first
            first_hit_mask = lens_ts < hit_ts
            process_mask = lens_mask & first_hit_mask
            object_hit_masks[process_mask] = False
            hit_object_indices[process_mask] = -1
            
            if np.any(process_mask):
                # Get hit points and new rays
                hit_points = get_ray_points_array_at_t_array(rays[process_mask], lens_ts[process_mask])
                self._save_hit_rays(rays[process_mask], hit_points)
                new_rays = lens.get_new_rays(rays[process_mask], hit_points)
                
                # Recursively trace new rays
                new_colors = self.get_colors(new_rays)
                
                # Update colors for these rays
                colors[process_mask] = new_colors
                
                # Mark these rays as processed
                lens_hit_masks[process_mask] = True
                
        # Get colors for non-lens hits
        if np.any(object_hit_masks):
            hit_indices = np.where(object_hit_masks)[0]
            hit_points = get_ray_points_array_at_t_array(rays[object_hit_masks], hit_ts[object_hit_masks])
            
            # Save visualization of hit rays
            self._save_hit_rays(rays[object_hit_masks], hit_points)
            
            # Get colors from objects
            for point_index, (hit_index, obj_index) in enumerate(zip(hit_indices, hit_object_indices)):
                if obj_index is not None:
                    obj = self.colored_objects[obj_index]
                    colors[hit_index] = obj.get_colors(np.array([hit_points[point_index]]))[0]
        
        # Save visualization of missed rays
        missed_mask = ~(object_hit_masks | lens_hit_masks)
        if np.any(missed_mask):
            self._save_missed_rays(rays[missed_mask])
                    
        return colors

    def _save_hit_rays(self, rays, points):
        """
        Save visualization of rays that hit objects.
        
        Args:
            rays: Array of rays that hit objects (ray_dtype)
            points: Array of hit points (Nx3)
        """
        for ray, point in zip(rays, points):
            self.exporter.add_line(ray['origin'], point, group="rays")
            self.exporter.add_point(point, group="hits")

    def _save_missed_rays(self, rays, max_length=1):
        """
        Save visualization of rays that missed all objects.
        
        Args:
            rays: Array of rays that missed (ray_dtype)
            max_length: Length to draw missed rays
        """
        for ray in rays:
            end_point = ray['origin'] + ray['direction'] * max_length
            self.exporter.add_line(ray['origin'], end_point, group="rays")
