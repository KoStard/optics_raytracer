import torch
from typing import List

from optics_raytracer.circle import Circle, ColoredCircle
from optics_raytracer.inserted_image import InsertedImage
from optics_raytracer.rectangle import ColoredRectangle
from .ray import get_ray_points_array_at_t_array, apply_mask_on_rays
from .colored_object import ColoredObject
from .lens import Lens
from .surface import get_surface_hit_ts, get_surface_hit_ts_mask
from .export_3d import Exporter3D
from .torch_details import device

class ColorTracer:
    """
    Class for tracing ray colors through a scene with colored objects and lenses.
    """
    def __init__(
        self,
        exporter: Exporter3D,
        colored_objects: List[ColoredObject],
        lenses: List[Lens],
        default_color: torch.Tensor = None,
        ray_sampling_rate_for_3d_export = None
    ):
        """
        Initialize the color tracer.
        
        Args:
            exporter: 3D exporter for visualization
            colored_objects: List of colored objects in the scene
            lenses: List of lenses in the scene
            default_color: Default color for rays that don't hit anything
        """
        if default_color is None:
            default_color = torch.tensor([0.0, 0.0, 0.0], dtype=torch.float32)
        if ray_sampling_rate_for_3d_export is None:
            ray_sampling_rate_for_3d_export = torch.float32(0.01)
        self.exporter = exporter
        self.colored_objects = colored_objects
        self.lenses = lenses
        self.default_color = default_color
        self.ray_sampling_rate_for_3d_export = ray_sampling_rate_for_3d_export
        
        for obj in colored_objects:
            if isinstance(obj, ColoredCircle):
                self.exporter.add_circle(obj.circle.circle_data, 50)
            elif isinstance(obj, ColoredRectangle):
                self.exporter.add_rectangle(obj.rectangle.rectangle_data)
            elif isinstance(obj, InsertedImage):
                self.exporter.add_rectangle(obj.rectangle.rectangle_data)
            else:
                print(f"Unknown object type: {type(obj)}")
        
        for lens in lenses:
            self.exporter.add_circle(lens.lens_data, 50)

    def get_colors(self, rays: torch.Tensor, depth=None) -> torch.Tensor:
        """
        Get colors for an array of rays by tracing them through the scene.
        
        Args:
            rays: Array of rays to trace
            
        Returns:
            Array of colors (Nx3) in RGB format with values between 0 and 1
        """
        # Initialize output colors with default
        colors = torch.tile(self.default_color, (len(rays['origin']), 1)).to(device)
        
        # Find closest hits for all objects
        closest_hit_ts = torch.full((len(rays['origin']), ), torch.inf, dtype=torch.float32).to(device)
        any_object_hit_mask = torch.zeros(len(rays['origin']), dtype=bool).to(device)
        ray_hits_any_lens_mask = torch.zeros(len(rays['origin']), dtype=bool).to(device)
        ray_hitting_object_indices_array = torch.full((len(rays['origin']), ), -1).to(device)
        hit_lens_indices_by_rays_order = torch.full((len(rays['origin']), ), -1).to(device)
        
        # Check colored objects
        for obj_index, lens in enumerate(self.colored_objects):
            if isinstance(lens, ColoredRectangle) or isinstance(lens, InsertedImage):
                surface_point = lens.rectangle.middle_point
                surface_normal = lens.rectangle.normal
                
                # Get hit times and mask
                obj_ts = get_surface_hit_ts(rays, surface_point, surface_normal)
                obj_points = get_ray_points_array_at_t_array(rays, obj_ts)
                obj_mask = get_surface_hit_ts_mask(obj_ts)
                obj_mask &= lens.rectangle.get_hits_mask(lens.rectangle.rectangle_data, obj_points)
                
            elif isinstance(lens, ColoredCircle):
                surface_point = lens.circle.center
                surface_normal = lens.circle.normal
                
                # Get hit times and mask
                obj_ts = get_surface_hit_ts(rays, surface_point, surface_normal)
                obj_points = get_ray_points_array_at_t_array(rays, obj_ts)
                obj_mask = get_surface_hit_ts_mask(obj_ts)
                obj_mask &= lens.circle.get_hits_mask(lens.circle.circle_data, obj_points)
            else:
                print(f"Unknown object type: {type(lens)}")
                continue
            
            # Update closest hits
            closer_mask = obj_ts < closest_hit_ts
            update_mask = obj_mask & closer_mask
            closest_hit_ts[update_mask] = obj_ts[update_mask]
            any_object_hit_mask[update_mask] = True
            ray_hitting_object_indices_array[update_mask] = obj_index
            
        # Check lenses
        for lens_index, lens in enumerate(self.lenses):
            lens_ts = get_surface_hit_ts(rays, lens.center, lens.normal)
            current_lens_hit_mask = get_surface_hit_ts_mask(lens_ts)
            current_lens_hit_mask[current_lens_hit_mask.clone()] &= Circle.get_hits_mask(lens.lens_data, get_ray_points_array_at_t_array(apply_mask_on_rays(rays, current_lens_hit_mask), lens_ts[current_lens_hit_mask]))
            
            ray_hits_any_lens_mask[current_lens_hit_mask] = True
            
            # Only process rays that hit this lens first
            first_hit_mask = lens_ts < closest_hit_ts
            update_mask = ray_hits_any_lens_mask & first_hit_mask
            
            closest_hit_ts[update_mask] = lens_ts[update_mask]
            any_object_hit_mask[update_mask] = False
            ray_hitting_object_indices_array[update_mask] = -1
            hit_lens_indices_by_rays_order[update_mask] = lens_index
            ray_hits_any_lens_mask[update_mask] = True
        
        # Getting lens hit colors
        if torch.any(ray_hits_any_lens_mask):
            # ray_hits_any_lens_mask has shape of (len(rays['origin']), )
            # So lens_hit_points is as big as torch.where(ray_hits_any_lens_mask)
            lens_hit_points = get_ray_points_array_at_t_array(apply_mask_on_rays(rays, ray_hits_any_lens_mask), closest_hit_ts[ray_hits_any_lens_mask])
            
            # Get the the possible lens indices
            lens_indices = torch.arange(len(self.lenses))

            # Create a dictionary of masks, where each mask shows the positions of the corresponding value.
            # Each mask has shape of ray_hitting_lens_indices_array, which has shape of (len(rays['origin']), )
            masks_by_lens_index = {current_lens_index: (hit_lens_indices_by_rays_order == current_lens_index) for current_lens_index in lens_indices}
            
            for current_lens_index, current_lens_hitting_rays_mask in masks_by_lens_index.items():
                if torch.any(current_lens_hitting_rays_mask):
                    lens = self.lenses[current_lens_index]
                    new_rays = lens.get_new_rays(apply_mask_on_rays(rays, current_lens_hitting_rays_mask), lens_hit_points[current_lens_hitting_rays_mask[ray_hits_any_lens_mask]])
                    # TODO: Optimization opportunity, collect all rays together and call get_colors once
                    colors[current_lens_hitting_rays_mask] = self.get_colors(new_rays, depth=depth+1 if depth else 1)
            
            # Save visualization of hit rays
            self._save_hit_rays(apply_mask_on_rays(rays, ray_hits_any_lens_mask), lens_hit_points, depth=depth)
                
        # Get colors for non-lens hits
        if torch.any(any_object_hit_mask):
            lens_hit_points = get_ray_points_array_at_t_array(apply_mask_on_rays(rays, any_object_hit_mask), closest_hit_ts[any_object_hit_mask])
            
            # Get the unique values.
            lens_indices = torch.arange(len(self.colored_objects))

            # Create a dictionary of masks, where each mask shows the positions of the corresponding value.
            masks_by_lens_index = {val: (ray_hitting_object_indices_array == val) for val in lens_indices}
            
            for hit_object_index, hit_object_mask in masks_by_lens_index.items():
                if torch.any(hit_object_mask):
                    # Get colors from objects
                    lens = self.colored_objects[hit_object_index]
                    colors[hit_object_mask] = lens.get_colors(lens_hit_points[hit_object_mask[any_object_hit_mask]])
            
            # Save visualization of hit rays
            self._save_hit_rays(apply_mask_on_rays(rays, any_object_hit_mask), lens_hit_points, depth=depth)
        
        # Save visualization of missed rays
        missed_mask = ~(any_object_hit_mask | ray_hits_any_lens_mask)
        if torch.any(missed_mask):
            self._save_missed_rays(apply_mask_on_rays(rays, missed_mask))
        
        return colors

    def _save_hit_rays(self, rays, points, depth=None):
        """
        Save visualization of rays that hit objects.
        
        Args:
            rays: Array of rays that hit objects
            points: Array of hit points (Nx3)
        """
        # Save visualization of hit rays
        tracing_mask = self._get_random_tracing_mask(len(rays['origin']))
        rays_group = "rays"
        if depth:
            rays_group += f"/{depth}_depth"
        for origin, point in zip(apply_mask_on_rays(rays, tracing_mask)['origin'], points[tracing_mask]):
            self.exporter.add_line(origin, point, group=rays_group)
            self.exporter.add_point(point, group="hits")

    def _save_missed_rays(self, rays, max_length=1000):
        """
        Save visualization of rays that missed all objects.
        
        Args:
            rays: Array of rays that missed
            max_length: Length to draw missed rays
        """
        # Save visualization of hit rays
        tracing_mask = self._get_random_tracing_mask(len(rays['origin']))
        rays_with_tracing_mask = apply_mask_on_rays(rays, tracing_mask)
        for origin, direction in zip(rays_with_tracing_mask['origin'], rays_with_tracing_mask['direction']):
            end_point = origin + direction * max_length
            self.exporter.add_line(origin, end_point, group="rays/missed")

    def _get_random_tracing_mask(self, l):
        return torch.rand(l) <= self.ray_sampling_rate_for_3d_export
