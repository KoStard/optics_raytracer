import numpy as np
from typing import List

from optics_raytracer.circle import Circle, ColoredCircle
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
        default_color: np.ndarray = np.array([0, 0, 0])
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
        hit_masks = np.zeros(len(rays), dtype=bool)
        hit_object_indices = np.full(len(rays), -1)
        
        # Check colored objects
        for obj_index, obj in enumerate(self.colored_objects):
            if isinstance(obj, ColoredRectangle):
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
            hit_masks[update_mask] = True
            hit_object_indices[update_mask] = obj_index
            
        # Check lenses
        for lens in self.lenses:
            lens_ts = get_surface_hit_ts(rays, lens.center, lens.normal)
            lens_mask = get_surface_hit_ts_mask(lens_ts)
            lens_mask &= Circle.get_hits_mask(lens.array, rays['origin'])
            
            # Only process rays that hit this lens first
            first_hit_mask = lens_ts < hit_ts
            process_mask = lens_mask & first_hit_mask
            
            if np.any(process_mask):
                # Get hit points and new rays
                hit_points = get_ray_points_array_at_t_array(rays[process_mask], lens_ts[process_mask])
                new_rays = lens.get_new_rays(rays[process_mask], hit_points)
                
                # Recursively trace new rays
                new_colors = self.get_colors(new_rays)
                
                # Update colors for these rays
                colors[process_mask] = new_colors
                
                # Mark these rays as processed
                hit_masks[process_mask] = True
                
        # Get colors for non-lens hits
        if np.any(hit_masks):
            hit_indices = np.where(hit_masks)[0]
            hit_points = get_ray_points_array_at_t_array(rays[hit_masks], hit_ts[hit_masks])
            
            # Get colors from objects
            for i, obj_index in zip(hit_indices, hit_object_indices):
                if obj_index is not None:
                    obj = self.colored_objects[obj_index]
                    colors[i] = obj.get_colors(np.array([hit_points[i]]))[0]
                    
        return colors
